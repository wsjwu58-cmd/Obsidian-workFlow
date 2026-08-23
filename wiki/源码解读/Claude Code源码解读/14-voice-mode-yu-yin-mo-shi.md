# 14-voice-mode-yu-yin-mo-shi
Voice Mode 是 Claude Code 的按键说话（Push-to-Talk）语音输入功能。用户通过长按空格键录音，音频通过 WebSocket 流式传输到 Anthropic STT 端点（Nova 3），实时转录显示在终端中，转录文本直接作为用户消息提交到对话。

Sources: [docs/features/voice-mode.md](#root/b3q2Y8LC6LLy)

## 一、核心特性与用户交互

### 1.1 交互模式

Voice Mode 支持两种激活方式：

| 激活方式 | 触发条件 | 适用场景 |
| --- | --- | --- |
| **Push-to-Talk** | 长按空格键 | 主动输入命令、描述任务 |
| **Focus Mode** | 终端获得焦点时自动录音 | 多窗口协作、连续语音对话 |

### 1.2 用户操作流程

```
sequenceDiagram
    participant User
    participant Terminal
    participant VoiceModule
    participant WebSocket
    participant STT

    User->>Terminal: 长按空格键
    Terminal->>VoiceModule: 开始录音
    VoiceModule->>WebSocket: 建立连接
    WebSocket->>STT: 流式传输音频
    STT-->>Terminal: 中间转录结果 (实时预览)
    User->>Terminal: 释放空格键
    Terminal->>VoiceModule: 停止录音
    VoiceModule->>WebSocket: 发送 CloseStream
    STT-->>Terminal: 最终转录
    Terminal->>User: 插入输入框并提交
```

### 1.3 音频后端选择

系统按以下优先级选择音频录制后端：

```
flowchart TD
    A[开始录音] --> B{原生模块可用?}
    B -->|macOS/Linux/Windows + cpal| C[使用 Native Audio<br/>低延迟·无依赖]
    B -->|否| D{平台}
    D -->|Linux + arecord 可用| E[使用 arecord<br/>ALSA 录制]
    D -->|Linux + SoX 可用| F[使用 SoX rec<br/>跨平台兼容]
    D -->|Windows| G[返回失败<br/>无回退方案]
```

Sources: [src/services/voice.ts](#root/stCjGSWAXkHj)

## 二、三层门控架构

Voice Mode 的可用性由三层检查共同决定：

```
flowchart TD
    A[用户请求] --> B{Feature Flag}
    B -->|FEATURE_VOICE_MODE=1| C{GrowthBook Kill-Switch}
    B -->|关闭| H[不可用]
    C -->|tengu_amber_quartz_disabled<br/>默认 false| D{Auth 检查}
    C -->|true| H
    D -->|hasVoiceAuth<br/>OAuth Token 有效| I[Voice Mode 可用]
    D -->|无 Token| H
```

### 2.1 门控函数详解

| 函数 | 职责 | 缓存策略 |
| --- | --- | --- |
| `isVoiceGrowthBookEnabled()` | Feature Flag + GrowthBook 负向门控 | 每次调用读取缓存 |
| `hasVoiceAuth()` | OAuth Token 存在性检查 | `getClaudeAIOAuthTokens()` 自带 memoize |
| `isVoiceModeEnabled()` | 组合检查（命令路径） | 无缓存，调用时实时检查 |
| `useVoiceEnabled()` | 组合检查（React 路径） | auth 版本号 memoize |

Sources: [src/voice/voiceModeEnabled.ts](#root/d0Bd1itGiFz4)

### 2.2 OAuth 独占性

**重要设计决策**：Voice Mode 使用 `voice_stream` 端点，该端点**仅限 Anthropic OAuth 用户**可用。

以下用户**无法使用** Voice Mode：

*   API Key 用户
*   AWS Bedrock 用户
*   Google Vertex AI 用户
*   Microsoft Azure Foundry 用户

Sources: [src/voice/voiceModeEnabled.ts](#root/fT4lU4StvuYX)

## 三、核心模块交互

### 3.1 模块职责矩阵

| 模块路径 | 核心职责 | 关键技术 |
| --- | --- | --- |
| `src/voice/voiceModeEnabled.ts` | 三层门控逻辑 | GrowthBook, Keychain |
| `src/hooks/useVoice.ts` | 录音状态机 + WebSocket 管理 | React Hook, 状态机 |
| `src/hooks/useVoiceIntegration.tsx` | 键盘事件处理 + 输入框集成 | 终端按键监听 |
| `src/hooks/useVoiceEnabled.ts` | React 用门控检查 | useMemo 缓存 |
| `src/services/voiceStreamSTT.ts` | WebSocket 流式 STT | ws 库, Deepgram Nova 3 |
| `src/services/voice.ts` | 音频录制（原生 + SoX） | cpal NAPI, SoX/arecord |
| `src/services/voiceKeyterms.ts` | STT 关键词优化 | 项目名/分支名/文件名 |
| `src/context/voice.tsx` | 语音状态全局共享 | React Context + Store |

Sources: [src/hooks/useVoice.ts](#root/v2rrZtLHE9ok), [src/services/voiceStreamSTT.ts](#root/Ku7Qz37LUSWt)

### 3.2 录音状态机

`useVoice` hook 内部维护三状态机：

```
stateDiagram-v2
    [*] --> idle: 初始状态
    idle --> recording: handleKeyEvent<br/>检测到按键
    recording --> processing: finishRecording<br/>释放按键/超时
    processing --> idle: 转录完成/失败
    recording --> idle: cleanup<br/>意外中断
    processing --> idle: cleanup<br/>强制停止
```

**状态转换触发条件**：

| 源状态 | 目标状态 | 触发事件 |
| --- | --- | --- |
| idle | recording | 首次 keypress + `startRecordingSession()` |
| recording | processing | `finishRecording()` - 释放空格/超时 |
| recording | idle | `cleanup()` - 中途禁用/错误 |
| processing | idle | 转录完成或最终超时 |

Sources: [src/hooks/useVoice.ts](#root/wlSf4oODdPQO)

## 四、WebSocket 流式传输架构

### 4.1 连接建立流程

```
sequenceDiagram
    participant Client as useVoice
    participant WS as WebSocket
    participant Server as voice_stream API
    participant Deepgram as Nova 3 STT

    Client->>WS: connectVoiceStream()
    WS->>Server: HTTP Upgrade + Bearer Token
    Server-->>WS: 101 Switching Protocols
    WS-->>Client: onReady(connection)
    Client->>WS: 发送 KeepAlive
    Client->>WS: 流式发送音频 Chunk
    WS->>Deepgram: 转发音频流
    Deepgram-->>WS: TranscriptText (中间结果)
    WS-->>Client: onTranscript(text, false)
    Deepgram-->>WS: TranscriptEndpoint (语句结束)
    WS-->>Client: onTranscript(text, true)
    Client->>WS: 发送 CloseStream
    WS->>Server: 关闭音频流
    Server-->>WS: 最终 TranscriptEndpoint
    WS-->>Client: finalize resolved
```

### 4.2 关键设计：音频缓冲与合并

在 WebSocket 连接建立期间（`onReady` 触发前），音频数据被缓冲：

```typescript
// 连接建立前的音频路由
onData(chunk: Buffer) {
  if (connectionRef.current) {
    // WebSocket 已就绪 → 直接发送
    connectionRef.current.send(owned)
  } else {
    // 仍在连接中 → 缓冲
    audioBuffer.push(owned)
  }
}
```

缓冲策略：将音频切片合并为约 32KB（~1秒 16kHz/16-bit/单声道）的帧，减少 WebSocket 帧数量。

Sources: [src/hooks/useVoice.ts](#root/c84U4Dk6LuMV)

### 4.3 Finalize 解析时机

`finalize()` 返回的 Promise 有四个解析来源：

| 解析来源 | 超时时间 | 触发条件 |
| --- | --- | --- |
| `post_closestream_endpoint` | ~300ms | CloseStream 后收到 TranscriptEndpoint |
| `no_data_timeout` | 1.5s | CloseStream 后无数据到达 |
| `safety_timeout` | 5s | 最终保底超时 |
| `ws_close` | WebSocket 关闭时 | 连接异常断开 |

**静默丢弃重放机制**：当检测到服务器接收了音频但返回零转录时（`no_data_timeout` + `hadAudioSignal=true`），系统在 250ms 后重放完整音频缓冲到新连接。

Sources: [src/services/voiceStreamSTT.ts](#root/VfFXfJwy7cwt)

## 五、语言支持与关键词优化

### 5.1 STT 语言代码映射

系统将用户设置的语言名称规范化为 BCP-47 代码：

```typescript
const LANGUAGE_NAME_TO_CODE: Record<string, string> = {
  'english': 'en',
  'español': 'es', 'espanol': 'es',
  'français': 'fr', 'francais': 'fr',
  '日本語': 'ja',
  'deutsch': 'de',
  // ... 20 种支持的语言
}
```

**支持的语言**：`en`, `es`, `fr`, `ja`, `de`, `pt`, `it`, `ko`, `hi`, `id`, `ru`, `pl`, `tr`, `nl`, `uk`, `el`, `cs`, `da`, `sv`, `no`

Sources: [src/hooks/useVoice.ts](#root/isxxDpnllgdK)

### 5.2 关键词优化（Keyterms）

`voiceKeyterms` 服务为 STT 提供领域特定词汇提示：

```typescript
const GLOBAL_KEYTERMS = [
  'MCP', 'symlink', 'grep', 'regex', 'localhost',
  'codebase', 'TypeScript', 'JSON', 'OAuth',
  'webhook', 'gRPC', 'dotfiles', 'subagent', 'worktree'
]
```

动态添加：

*   项目根目录名称
*   Git 分支名称（按标识符拆分）
*   最近文件名称（最多 50 个关键词）

Sources: [src/services/voiceKeyterms.ts](#root/OWVyaE4N0FXI)

## 六、Focus Mode 专注模式

Focus Mode 允许在终端获得焦点时自动开始录音，适用于"多 Claude 协作"工作流。

### 6.1 行为特点

| 特性 | Push-to-Talk | Focus Mode |
| --- | --- | --- |
| 激活方式 | 长按空格键 | 终端获得焦点 |
| 结束方式 | 释放空格键 | 终端失去焦点 |
| 转录提交 | 整句提交 | 实时提交（每句） |
| 静音超时 | 无 | 5秒无语音自动结束 |

### 6.2 Focus Mode 状态流转

```
flowchart TD
    A[终端获得焦点] --> B{之前静默超时?}
    B -->|是| A
    B -->|否| C[开始录音 + 启动静音计时器]
    C --> D[收到中间转录]
    D --> E[重置静音计时器]
    E --> D
    D --> F[收到最终转录]
    F --> G[立即注入输入框]
    G --> E
    F --> H[5秒无语音]
    H --> I[结束录音 + 关闭连接]
    I --> J[终端失去焦点]
    J --> A
```

Sources: [src/hooks/useVoice.ts](#root/Y7U4vou5JdsB)

## 七、使用配置

### 7.1 启用 Voice Mode

```
# 方式一：环境变量
FEATURE_VOICE_MODE=1 bun run dev

# 方式二：命令切换
/voice
```

### 7.2 前置检查

启用前系统执行以下检查：

| 检查项 | 失败处理 |
| --- | --- |
| OAuth 认证 | 提示运行 `/login` |
| 麦克风权限 | 提示前往系统设置授权 |
| 音频录制工具 | 提示安装 SoX |
| GrowthBook Kill-Switch | 静默禁用 |

Sources: [src/commands/voice/voice.ts](#root/NHnkp1waZOk5)

### 7.3 依赖要求

| 平台 | 原生模块 | 回退方案 |
| --- | --- | --- |
| macOS | cpal (CoreAudio) | 无需回退 |
| Linux | cpal (ALSA/PulseAudio) | arecord 或 SoX |
| Windows | cpal (WASAPI) | 无回退（必须原生模块） |

Sources: [src/services/voice.ts](#root/l0Y8JZMF7F9k)

## 八、关键设计决策

### 8.1 延迟加载与 TCC 权限

**问题**：加载 `audio-capture-napi` 触发 macOS TCC 麦克风权限弹窗。

**解决方案**：使用懒加载（lazy import），仅在首次语音激活时才加载原生模块：

```typescript
useEffect(() => {
  if (enabled && !voiceModule) {
    void import('../services/voice.js').then(mod => {
      voiceModule = mod
    })
  }
}, [enabled])
```

Sources: [src/hooks/useVoice.ts](#root/jgXnUlYZhq8L)

### 8.2 Nova 3 模型路由

系统通过 GrowthBook Feature Flag `tengu_cobalt_frost` 控制是否使用 Nova 3：

```typescript
const isNova3 = getFeatureValue_CACHED_MAY_BE_STALE('tengu_cobalt_frost', false)
if (isNova3) {
  params.set('use_conversation_engine', 'true')
  params.set('stt_provider', 'deepgram-nova3')
}
```

Nova 3 的特性：

*   中间转录累积（不自动 final）
*   按话语端点解析最终结果

Sources: [src/services/voiceStreamSTT.ts](#root/OYQRtcnbp12Y)

### 8.3 会话代数（Session Generation）

防止僵尸连接覆盖当前连接状态：

```typescript
const sessionGenRef = useRef(0)

function startRecordingSession() {
  sessionGenRef.current++
  const myGen = sessionGenRef.current
  const isStale = () => sessionGenRef.current !== myGen
  // callbacks 中检查 isStale() 拒绝过期事件
}
```

Sources: [src/hooks/useVoice.ts](#root/6eZ0PDIgOYWU)

## 九、遥测事件

| 事件名 | 触发时机 | 关键维度 |
| --- | --- | --- |
| `tengu_voice_recording_started` | 开始录音 | sttLanguage, focusTriggered |
| `tengu_voice_recording_completed` | 录音结束 | transcriptChars, hadAudioSignal |
| `tengu_voice_silent_drop_replay` | 静默丢弃重放 | recordingDurationMs |
| `tengu_voice_stream_early_retry` | 早期错误重试 | \- |
| `tengu_voice_toggled` | 开关切换 | enabled |

Sources: [src/hooks/useVoice.ts](#root/Pl0e7V37WKab)

## 十、文件索引

| 文件路径 | 行数 | 职责摘要 |
| --- | --- | --- |
| `src/voice/voiceModeEnabled.ts` | 55 | 三层门控逻辑 |
| `src/hooks/useVoice.ts` | 1145 | 核心录音状态机 |
| `src/hooks/useVoiceIntegration.tsx` | 677 | 键盘事件与输入框集成 |
| `src/hooks/useVoiceEnabled.ts` | 26 | React 门控 Hook |
| `src/services/voiceStreamSTT.ts` | 545 | WebSocket STT 客户端 |
| `src/services/voice.ts` | 526 | 音频录制服务 |
| `src/services/voiceKeyterms.ts` | 107 | 关键词优化 |
| `src/context/voice.tsx` | 88 | 语音状态全局上下文 |
| `src/commands/voice/index.ts` | 21 | /voice 命令定义 |
| `src/commands/voice/voice.ts` | 151 | /voice 命令实现 |
| `packages/audio-capture-napi/src/index.ts` | 153 | 原生音频 NAPI 封装 |

---

## 下一步探索

*   [MCP 协议集成](12-mcp-xie-yi-ji-cheng.md) — Voice Mode 通过 MCP 关键词优化提升专业术语识别
*   [工具系统架构](10-gong-ju-xi-tong-jia-gou.md) — 理解 Voice Mode 如何与传统工具系统协同
*   [Permission Model 权限模型](15-quan-xian-mo-xing-yu-gui-ze-yin-qing.md) — 麦克风权限的安全管理机制

## 相关条目
- [[13-computer-use-dian-nao-cao-kong]]
- [[19-agent-xie-diao-mo-shi]]
