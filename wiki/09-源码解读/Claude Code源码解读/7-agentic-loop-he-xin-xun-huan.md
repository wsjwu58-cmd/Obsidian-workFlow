# 7-agentic-loop-he-xin-xun-huan
本章节深入解析 Claude Code 的核心执行引擎——**Agentic Loop**（智能体循环）。这是 `src/query.ts` 中 `queryLoop()` 异步生成器函数实现的状态机，驱动 AI 从接收用户请求到返回最终响应的完整生命周期。Agentic Loop 不仅是技术实现，更是 Claude Code 区别于传统聊天机器人的核心范式：**逐步推理、动态执行、错误恢复**。

Sources: [src/query.ts](#root/qWi2ilWD3c6u)

## 核心范式：为什么需要 Agentic Loop

传统聊天机器人的交互模式是**一问一答**：用户发送消息，AI 生成回复，交互结束。这种模式在简单问答场景足够有效，但无法处理需要多步骤操作的任务——如"找到项目中所有未使用的导入语句并删除它们"，这类任务需要：

*   **思考→行动→观察→再思考**的反复迭代
*   **动态上下文管理**：每步操作的结果影响下一步的决策
*   **即时错误恢复**：工具执行失败时能修正策略继续执行

Agentic Loop 将这种能力封装在一个 `while(true)` 无限循环中，每次迭代代表一个完整的**思考-行动-观察**周期，直到任务完成或遇到不可恢复的错误。

Sources: [src/query.ts](#root/LgQ6uJF7VGMU)

## 循环结构：四阶段架构

Agentic Loop 的每次迭代包含四个串行阶段，形成完整的状态机周期：

```
flowchart TB
    subgraph Phase1["阶段 1：上下文预处理"]
        A[messagesForQuery 原始消息]
        A --> B[applyToolResultBudget]
        B --> C[snipCompact 微片压缩]
        C --> D[microcompact 工具结果摘要]
        D --> E[contextCollapse 上下文折叠]
        E --> F[autocompact 自动压缩]
        F --> G[处理后的消息]
    end
    
    subgraph Phase2["阶段 2：流式 API 调用"]
        G --> H[deps.callModel 发起请求]
        H --> I[收集 assistantMessages]
        I --> J[提取 toolUseBlocks]
        J --> K[streamingToolExecutor 并行执行]
    end
    
    subgraph Phase3["阶段 3：工具执行"]
        K --> L{needsFollowUp?}
        L -->|Yes| M[执行工具]
        L -->|No| N[检查终止条件]
        M --> O[toolResults 累积]
    end
    
    subgraph Phase4["阶段 4：终止/继续"]
        N --> P{7种终止条件?}
        P -->|满足| Q[return Terminal]
        P -->|不满足| R[continue 下一轮]
        O --> R
    end
```

### 阶段 1：上下文预处理管道

在调用 API 之前，消息数组依次经过 5 个压缩/优化步骤：

| 步骤 | 函数 | 功能 | 特征 |
| --- | --- | --- | --- |
| `applyToolResultBudget` | `src/utils/toolResultStorage.ts` | 工具结果按 `maxResultSizeChars` 截断 | 缓存安全 |
| `snipCompact` | `src/services/compact/snipCompact.ts` | 历史 Snip 压缩 | HISTORY\_SNIP feature |
| `microcompact` | `src/services/compact/microCompact.ts` | 工具结果摘要化 | 缓存编辑支持 |
| `contextCollapse` | `src/services/contextCollapse/index.ts` | 上下文折叠 | CONTEXT\_COLLAPSE feature |
| `autocompact` | `src/services/compact/autoCompact.ts` | 超阈值时自动压缩 | 跨迭代追踪 |

每个步骤的输出是下一步的输入，形成串行管道。**Snip 和 Microcompact 释放的 token 数会传递给 autocompact 的阈值计算**（`snipTokensFreed`），避免重复压缩。

Sources: [src/query.ts](#root/MMx84LEsYYAs) Sources: [src/query/deps.ts](#root/0erQvVgitiaL)

### 阶段 2：流式 API 调用

`deps.callModel()` 发起流式请求，返回 `AsyncGenerator`。在流式过程中，关键机制包括：

**并行工具执行**：当 `streamingToolExecution` 特性启用时，`StreamingToolExecutor` 在流式过程中就开始并行执行工具，不等流结束：

```typescript
// src/query.ts:519-530
const streamingToolExecutor = useStreamingToolExecution
  ? new StreamingToolExecutor(
      toolUseContext.options.tools,
      canUseTool,
      toolUseContext,
    )
  : null
```

**错误暂扣机制**：可恢复的错误（`prompt-too-long`、`max-output-tokens`）被**暂扣**（withheld），先尝试恢复再决定是否暴露给用户：

```typescript
// src/query.ts:750-780
if (reactiveCompact?.isWithheldPromptTooLong(message as Message)) {
  withheld = true
}
if (isWithheldMaxOutputTokens(message)) {
  withheld = true
}
if (!withheld) {
  yield yieldMessage
}
```

**流式降级检测**：当 `streamingFallbackOccured` 时，已收集的 `assistantMessages` 被标记为 tombstone，清空后重试。

Sources: [src/query.ts](#root/Xsskwe3MkSFF) Sources: [src/services/tools/StreamingToolExecutor.ts](#root/N9HQm7ZnyWyO)

### 阶段 3：工具执行

工具执行支持两种模式，通过 `streamingToolExecutor` 标志切换：

```typescript
// src/query.ts:1393-1398
const toolUpdates = streamingToolExecutor
  ? streamingToolExecutor.getRemainingResults()  // 流式：获取已完成的+等待中的
  : runTools(toolUseBlocks, assistantMessages, canUseTool, toolUseContext)
```

**并行安全分区**：`partitionToolCalls()` 将工具分为并发安全和串行执行批次：

```
flowchart LR
    subgraph "并发安全工具 (并行)"
        A[Glob] --> B[Grep]
        B --> C[Read]
        C --> D[...]
    end
    
    subgraph "非并发安全工具 (串行)"
        E[Bash] --> F[Write]
        F --> G[Edit]
    end
```

Sources: [src/services/tools/toolOrchestration.ts](#root/JihrTcx0Nxc4)

### 阶段 4：终止条件判定

每次迭代结束时，根据条件决定 `return`（终止）或 `continue`（继续）：

```typescript
// src/query.ts:1095-1100
if (!needsFollowUp) {
  // ... 恢复路径检查 ...
  return { reason: 'completed' }
}
```

Sources: [src/query.ts](#root/lRykS00jfFF5)

## 状态机：State 对象

循环状态通过 `State` 类型在迭代间传递，采用**不可变更新**模式：

```typescript
// src/query.ts:204-217
type State = {
  messages: Message[]                           // 当前对话消息
  toolUseContext: ToolUseContext               // 工具上下文（含权限）
  autoCompactTracking: AutoCompactTrackingState // 压缩跟踪
  maxOutputTokensRecoveryCount: number         // 输出截断恢复计数
  hasAttemptedReactiveCompact: boolean         // 是否已尝试即时压缩
  maxOutputTokensOverride: number | undefined  // 输出 token 上限覆盖
  pendingToolUseSummary: Promise<...> | undefined // 异步工具摘要
  stopHookActive: boolean | undefined          // Stop hook 是否激活
  turnCount: number                            // 轮次计数
  transition: Continue | undefined              // 上一次继续的原因
}
```

每次 `continue` 创建新的 State 对象（不可变更新），而非就地修改。`transition` 字段记录继续原因，让后续迭代能检测特定恢复路径避免循环。

Sources: [src/query.ts](#root/L6Yzh7un47Yf)

## 七种终止条件

| 终止原因 | 触发机制 | 源码位置 |
| --- | --- | --- |
| **completed** | AI 未发出 tool\_use → `needsFollowUp = false` | `src/query.ts:1380` |
| **blocking\_limit** | Token 超过硬限制（非 autocompact 模式） | `src/query.ts:646` |
| **aborted\_streaming** | `abortController.signal.aborted` | `src/query.ts:1054` |
| **model\_error** | `callModel()` 抛出异常 | `src/query.ts:999` |
| **prompt\_too\_long** | 413 错误且恢复失败 | `src/query.ts:1178` |
| **image\_error** | 图片尺寸/大小错误 | `src/query.ts:980` |
| **stop\_hook\_prevented** | Stop hook 返回 `preventContinuation` | `src/query.ts:1282` |

Sources: [src/query.ts](#root/VJgmO6G16Gyr)

## 四种恢复路径

Agentic Loop 不仅处理正常流程，还包含多种错误恢复机制：

### 1\. max\_output\_tokens 恢复

当 AI 输出被截断时（`apiError === 'max_output_tokens'`）：

```typescript
// src/query.ts:1200-1255
// 首次：尝试将 maxOutputTokens 提升到 64K，静默重试
if (capEnabled && maxOutputTokensOverride === undefined) {
  state = { ...state, maxOutputTokensOverride: ESCALATED_MAX_TOKENS }
  continue
}
// 后续：注入恢复消息，最多重试 3 次
if (maxOutputTokensRecoveryCount < MAX_OUTPUT_TOKENS_RECOVERY_LIMIT) {
  const recoveryMessage = createUserMessage({
    content: "Output token limit hit. Resume directly...",
    isMeta: true,
  })
  // ...
}
```

Sources: [src/query.ts](#root/meGLGYexHX7B) Sources: [src/utils/context.ts](#root/AfaV6CFSJPUe)

### 2\. Prompt-Too-Long 恢复

当遇到 413 错误时，有两个恢复阶段：

```
flowchart TD
    A[413 Prompt Too Long] --> B{CONTEXT_COLLAPSE?}
    B -->|Yes| C[Context Collapse Drain]
    C --> D{有 staged collapses?}
    D -->|Yes| E[提交折叠，释放空间]
    E --> F[重试]
    D -->|No| G[Reactive Compact]
    B -->|No| G
    G --> H{压缩成功?}
    H -->|Yes| F
    H -->|No| I[暴露错误，终止]
```

Sources: [src/query.ts](#root/wJEOO4zy65Kq)

### 3\. 流式降级恢复

当主模型不可用时（`FallbackTriggeredError`）：

```typescript
// src/query.ts:897-910
if (innerError instanceof FallbackTriggeredError && fallbackModel) {
  currentModel = fallbackModel
  attemptWithFallback = true
  // 清除已收集的消息，切换模型重试
  assistantMessages.length = 0
  toolUseBlocks.length = 0
  needsFollowUp = false
  continue
}
```

Sources: [src/query.ts](#root/186OSRRRw3Ur)

### 4\. Stop Hook 阻塞重试

Stop hook 可以注入阻塞错误消息，强制 AI 重新思考：

```typescript
// src/query.ts:1285-1308
if (stopHookResult.blockingErrors.length > 0) {
  state = {
    messages: [...messagesForQuery, ...assistantMessages, ...stopHookResult.blockingErrors],
    stopHookActive: true,
    transition: { reason: 'stop_hook_blocking' },
  }
  continue
}
```

Sources: [src/query/stopHooks.ts](#root/GaOn7GFwVYDY)

## 完整迭代示例

以用户请求"找到项目中所有未使用的导入语句"为例：

```
┌─────────────────────────────────────────────────────────────────────┐
│  迭代 1: 思考 → 行动                                                │
├─────────────────────────────────────────────────────────────────────┤
│  预处理: 无需压缩（上下文很短）                                      │
│  API: 返回 tool_use(Glob, "**/*.ts")                                │
│  工具: 返回 42 个文件路径                                           │
│  → needsFollowUp = true, continue                                   │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  迭代 2: 思考 → 行动                                                │
├─────────────────────────────────────────────────────────────────────┤
│  预处理: 42 个文件结果仍在预算内                                     │
│  API: 返回 tool_use(Grep, "import.*from")                           │
│  工具: 在 15 个文件中找到 120 条 import                             │
│  → needsFollowUp = true, continue                                   │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  迭代 3: 多轮微调                                                   │
├─────────────────────────────────────────────────────────────────────┤
│  预处理: 120 条结果触发 microcompact → 摘要化                        │
│  API: 返回 3 个 tool_use(FileEdit, ...)                             │
│  工具: 删除 5 条未使用导入                                           │
│  → needsFollowUp = true, continue                                   │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  迭代 4: 总结                                                       │
├─────────────────────────────────────────────────────────────────────┤
│  API: 返回纯文本响应                                                 │
│  → needsFollowUp = false                                            │
│  → Stop hooks 通过                                                   │
│  → return { reason: 'completed' }                                   │
└─────────────────────────────────────────────────────────────────────┘
```

Sources: [src/query.ts](#root/4QTA0twRpZea)

## 与 QueryEngine 的关系

**QueryEngine**（`src/QueryEngine.ts`）是 Agentic Loop 之上的**会话编排器**，管理跨多轮对话的状态：

| 维度 | QueryEngine | Agentic Loop |
| --- | --- | --- |
| **作用域** | 整个会话 | 单次用户输入 |
| **生命周期** | 整个 REPL 会话 | 一次 `submitMessage()` 调用 |
| **核心职责** | 会话状态、transcript 持久化、成本追踪 | API 调用、工具执行、错误恢复 |

```
sequenceDiagram
    participant User as 用户
    participant REPL as REPL
    participant QE as QueryEngine
    participant AL as Agentic Loop
    
    User->>REPL: 输入命令
    REPL->>QE: submitMessage()
    loop 多轮 Agentic Loop
        QE->>AL: query()
        AL->>AL: 上下文预处理 → API 调用 → 工具执行
        alt needsFollowUp = true
            AL->>AL: continue
        else needsFollowUp = false
            AL-->>QE: Terminal
        end
    end
    QE-->>REPL: yield SDKMessage
    REPL-->>User: 显示结果
```

Sources: [src/QueryEngine.ts](#root/wADuyEuC2jNy)

## 设计原则

| 原则 | 实现方式 | 价值 |
| --- | --- | --- |
| **流式优先** | `deps.callModel()` 返回 AsyncGenerator，StreamingToolExecutor 在流式过程中并行执行工具 | 响应延迟从 N×API延迟降至 1×API延迟 |
| **不可变状态** | State 对象采用不可变更新模式 | 可追踪性、测试性、并行安全 |
| **错误隔离** | 可恢复错误暂扣，不立即暴露 | 给 AI 自我修正的机会 |
| **上下文感知** | 每轮迭代前重新评估压缩需求 | 精确的资源管理 |
| **用户可控** | `abortController.signal` 在多个检查点被检测 | 用户随时可优雅中断 |

Sources: [src/query.ts](#root/f033F1QtTSqD)

## 下一步

了解 Agentic Loop 的核心循环后，建议继续学习：

*   [QueryEngine 编排机制](8-queryengine-bian-pai-ji-zhi.md) - 深入了解会话编排层如何调用 Agentic Loop
*   [会话状态管理](9-hui-hua-zhuang-tai-guan-li.md) - 了解消息持久化和成本追踪
*   [工具系统架构](10-gong-ju-xi-tong-jia-gou.md) - 了解 AI 的"双手"如何被调用

## 相关条目
- [[6-wu-ceng-jia-gou-she-ji]]
- [[8-queryengine-bian-pai-ji-zhi]]
