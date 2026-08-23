# 23-hooks-ji-zhi
Claude Code 的 Hooks 机制是一种强大的生命周期拦截系统，允许开发者在 Agent 执行过程中的关键节点注入自定义逻辑。通过 Hooks，你可以实现安全检查、上下文注入、工具调用拦截、自动化验证等多种功能。

## 架构概览

Hooks 系统的核心架构包含三个主要层次：事件定义层、匹配执行层和输出处理层。

```
flowchart TB
    subgraph 事件层
        HE[Hook 事件<br/>25 种事件类型]
    end
    
    subgraph 配置层
        SC[Settings 配置]
        RC[Registered Hooks<br/>SDK 注册]
        SH[Session Hooks<br/>运行时注册]
        FH[Function Hooks<br/>函数回调]
    end
    
    subgraph 执行层
        GM[getMatchingHooks<br/>匹配引擎]
        EH[execCommandHook<br/>命令执行]
        PH[execPromptHook<br/>提示执行]
        AH[execAgentHook<br/>Agent 执行]
        HH[execHttpHook<br/>HTTP 执行]
    end
    
    subgraph 输出层
        PO[processHookJSONOutput<br/>JSON 处理]
        AR[AggregatedHookResult<br/>结果聚合]
        PR[AsyncHookRegistry<br/>异步注册]
    end
    
    HE --> GM
    SC --> GM
    RC --> GM
    SH --> GM
    FH --> GM
    GM --> EH
    GM --> PH
    GM --> AH
    GM --> HH
    EH --> PO
    PH --> PO
    AH --> PO
    HH --> PO
    PO --> AR
    AR --> PR
```

## 25 种 Hook 事件

Claude Code 定义了 25 种 Hook 事件，覆盖完整的 Agent 生命周期（定义于 `src/entrypoints/sdk/coreTypes.ts:25-53`）：

| 阶段 | 事件 | 触发时机 | 匹配字段 |
| --- | --- | --- | --- |
| **会话** | `SessionStart` | 会话启动 | `source` |
|  | `SessionEnd` | 会话结束 | `reason` |
|  | `Setup` | 初始化完成 | `trigger` |
| **用户交互** | `UserPromptSubmit` | 用户提交消息 | — |
|  | `Stop` | Agent 停止响应 | — |
|  | `StopFailure` | Agent 停止失败 | `error` |
| **工具执行** | `PreToolUse` | 工具调用前 | `tool_name` |
|  | `PostToolUse` | 工具调用后（成功） | `tool_name` |
|  | `PostToolUseFailure` | 工具调用后（失败） | `tool_name` |
| **权限** | `PermissionRequest` | 权限请求 | `tool_name` |
|  | `PermissionDenied` | 权限被拒 | `tool_name` |
| **子 Agent** | `SubagentStart` | 子 Agent 启动 | `agent_type` |
|  | `SubagentStop` | 子 Agent 停止 | `agent_type` |
| **压缩** | `PreCompact` | 上下文压缩前 | `trigger` |
|  | `PostCompact` | 上下文压缩后 | `trigger` |
| **协作** | `TeammateIdle` | Teammate 空闲 | — |
|  | `TaskCreated` | 任务创建 | — |
|  | `TaskCompleted` | 任务完成 | — |
| **MCP** | `Elicitation` | MCP 服务器请求用户输入 | `mcp_server_name` |
|  | `ElicitationResult` | Elicitation 结果返回 | `mcp_server_name` |
| **环境** | `ConfigChange` | 配置变更 | `source` |
|  | `CwdChanged` | 工作目录变更 | — |
|  | `FileChanged` | 文件变更 | `file_path` |
|  | `InstructionsLoaded` | 指令加载 | `load_reason` |
|  | `WorktreeCreate` | Worktree 创建 | — |
|  | `WorktreeRemove` | Worktree 删除 | — |

Sources: [coreTypes.ts](#root/U1PgAWrr6nCk)

## 六种 Hook 类型

Hooks 配置支持六种执行方式（定义于 `src/schemas/hooks.ts`）：

| 类型 | 执行方式 | 适用场景 |
| --- | --- | --- |
| `command` | Shell 命令（bash/PowerShell） | 通用脚本、CI 检查 |
| `prompt` | 启动 LLM 评估 | 复杂语义分析 |
| `agent` | 启动子 Agent 执行 | 复杂多步骤验证 |
| `http` | HTTP POST 请求 | 远程服务、Webhook |
| `callback` | 内部 JS 函数 | 系统内置 Hook |
| `function` | 运行时注册的函数 Hook | Agent/Skill 内部使用 |

### Command Hook 配置

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "check-security.sh ${CLAUDE_PROJECT_DIR}",
        "shell": "bash",
        "timeout": 30,
        "if": "Bash(git push*)",
        "async": false,
        "asyncRewake": false
      }]
    }]
  }
}
```

Sources: [hooks.ts](#root/3tAEZ8z6MuV1)

## 核心执行引擎

### 命令型 Hook 执行

`execCommandHook()`（`src/utils/hooks.ts:829-1417`）是命令型 Hook 的执行核心，其执行流程如下：

```
sequenceDiagram
    participant Caller
    participant execCommandHook
    participant Shell
    participant Sandbox
    participant AsyncRegistry
    
    Caller->>execCommandHook: 执行 hook
    execCommandHook->>execCommandHook: 解析 shell 类型
    Note over execCommandHook: bash: Git Bash on Windows<br/>powershell: pwsh
    
    execCommandHook->>execCommandHook: 变量替换
    Note over execCommandHook: ${CLAUDE_PLUGIN_ROOT}<br/>${CLAUDE_PLUGIN_DATA}<br/>${user_config.X}
    
    execCommandHook->>Sandbox: 应用网络沙箱
    Note over Sandbox: 命令型 Hook 仅网络限制<br/>文件系统自由访问
    
    alt asyncRewake 模式
        execCommandHook->>execCommandHook: spawn 并注册退出处理
        execCommandHook-->>Caller: 立即返回
    else 标准执行
        execCommandHook->>Shell: spawn 子进程
        Shell-->>execCommandHook: stdout/stderr 流
        loop 直到完成/超时/中止
            execCommandHook->>execCommandHook: 检查第一行是否为 {"async":true}
        end
        
        alt 检测到异步标记
            execCommandHook->>AsyncRegistry: 注册后台 Hook
            execCommandHook-->>Caller: backgrounded: true
        else 同步执行完成
            execCommandHook-->>Caller: 返回 stdout/stderr
        end
    end
```

Sources: [hooks.ts](#root/i7QueOpferQq)

### 变量替换机制

Hook 命令支持多种变量替换（`src/utils/hooks.ts:880-950`）：

| 变量 | 说明 | 适用事件 |
| --- | --- | --- |
| `${CLAUDE_PLUGIN_ROOT}` | 插件根目录 | 所有事件 |
| `${CLAUDE_PLUGIN_DATA}` | 插件数据目录 | 所有事件 |
| `${user_config.X}` | 用户配置值 | 所有事件 |
| `$CLAUDE_PROJECT_DIR` | 项目根目录（环境变量） | 所有事件 |
| `$CLAUDE_ENV_FILE` | 环境变量文件 | SessionStart/Setup/CwdChanged/FileChanged |

### 环境变量注入

```typescript
const envVars: NodeJS.ProcessEnv = {
  ...subprocessEnv(),
  CLAUDE_PROJECT_DIR: toHookPath(projectDir),
}

// 插件选项暴露为环境变量
if (pluginOpts) {
  for (const [key, value] of Object.entries(pluginOpts)) {
    const envKey = key.replace(/[^A-Za-z0-9_]/g, '_').toUpperCase()
    envVars[`CLAUDE_PLUGIN_OPTION_${envKey}`] = String(value)
  }
}
```

Sources: [hooks.ts](#root/JMhC3TD4FQ3E)

## 异步 Hook 协议

### async 模式

当 Hook 进程的 stdout 第一行是 `{"async":true}` 时，系统将其转为后台任务（`src/utils/hooks.ts:1199-1246`）：

```typescript
const firstLine = firstLineOf(stdout).trim()
if (isAsyncHookJSONOutput(parsed)) {
  executeInBackground({
    processId: `async_hook_${child.pid}`,
    asyncResponse: parsed,
    ...
  })
}
```

后台 Hook 通过 `registerPendingAsyncHook()` 注册到 `AsyncHookRegistry`，完成后通过 `enqueuePendingNotification()` 通知主线程。

Sources: [AsyncHookRegistry.ts](#root/HaHflLv61wnu)

### asyncRewake 模式

`asyncRewake` 模式的 Hook 绕过 `AsyncHookRegistry`。当 Hook 退出码为 2 时，通过 `enqueuePendingNotification()` 以 `task-notification` 模式注入消息，唤醒空闲的模型：

```typescript
if (result.code === 2) {
  enqueuePendingNotification({
    value: wrapInSystemReminder(
      `Stop hook blocking error from command "${hookName}": ${stderr || stdout}`,
    ),
    mode: 'task-notification',
  })
}
```

Sources: [hooks.ts](#root/NMwMHUZym4TU)

## Hook 输出 Schema

### 同步输出结构

同步 Hook 的输出遵循严格的 Zod schema（`src/types/hooks.ts:49-180`）：

```json
{
  "continue": false,
  "suppressOutput": true,
  "stopReason": "安全检查失败",
  "decision": "approve" | "block",
  "reason": "原因说明",
  "systemMessage": "警告内容",
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow" | "deny" | "ask",
    "permissionDecisionReason": "匹配了安全规则",
    "updatedInput": { ... },
    "additionalContext": "额外上下文"
  }
}
```

Sources: [hooks.ts](#root/1WDEsCgjcSzg)

### 事件特定输出

| 事件 | 专有字段 | 作用 |
| --- | --- | --- |
| `PreToolUse` | `permissionDecision`, `updatedInput`, `additionalContext` | 拦截/修改工具输入 |
| `UserPromptSubmit` | `additionalContext` | 注入额外上下文 |
| `PostToolUse` | `additionalContext`, `updatedMCPToolOutput` | 修改 MCP 工具输出 |
| `SessionStart` | `initialUserMessage`, `watchPaths` | 设置初始消息和文件监控 |
| `PermissionDenied` | `retry` | 指示是否重试 |
| `Elicitation` | `action`, `content` | 控制用户输入对话框 |

Sources: [hooks.ts](#root/2drr2VNuETwz)

## 匹配机制

### 多来源合并

`getHooksConfig()`（`src/utils/hooks.ts:1600-1720`）从多个来源收集 Hook 配置：

```
flowchart LR
    subgraph getHooksConfig
        HSC[Settings Snapshot<br/>user/project/local]
        RH[Registered Hooks<br/>SDK 回调]
        SH[Session Hooks<br/>运行时注册]
        FH[Function Hooks<br/>内存函数]
    end
    
    HSC --> |合并| MC[HookMatchers]
    RH --> |合并| MC
    SH --> |合并| MC
    FH --> |合并| MC
```

Sources: [hooks.ts](#root/iWlsHXhuQW71)

### 匹配规则

`matcher` 字段支持四种模式（`src/utils/hooks.ts:1420-1460`）：

| 模式 | 示例 | 说明 |
| --- | --- | --- |
| 精确匹配 | `"Write"` | 完全匹配工具名 |
| 多值匹配 | `"Write\|Edit"` | 管道分隔的多个值 |
| 正则匹配 | `"^Bash(git.*)"` | 正则表达式 |
| 通配匹配 | `"*"` 或 `""` | 匹配所有 |

```typescript
function matchesPattern(matchQuery: string, matcher: string): boolean {
  if (!matcher || matcher === '*') return true
  if (matcher.includes('|')) {
    return matcher.split('|').some(m => matchesPattern(matchQuery, m.trim()))
  }
  if (matcher.startsWith('^')) {
    const regex = new RegExp(matcher)
    return regex.test(matchQuery)
  }
  return matcher === matchQuery
}
```

Sources: [hooks.ts](#root/rW8EKvDbRgHV)

### if 条件过滤

Hook 可以指定 `if` 条件，使用权限规则语法进行精细过滤（`src/utils/hooks.ts:1472-1520`）：

```json
{
  "hooks": [{
    "matcher": "Bash",
    "hooks": [{
      "type": "command",
      "command": "check-git-branch.sh",
      "if": "Bash(git push*)"
    }]
  }]
}
```

`if` 条件通过 `prepareIfConditionMatcher()` 预编译匹配器，支持 Bash 工具的 AST 级别命令解析。

Sources: [hooks.ts](#root/xgcvqwNkIH8Z)

### Hook 去重

同一 Hook 命令在不同配置层级可能重复。系统按 `pluginRoot\0command` 做 Map 去重，保留最后合并的层级：

```typescript
function hookDedupKey(m: MatchedHook, payload: string): string {
  return `${m.pluginRoot ?? m.skillRoot ?? ''}\0${payload}`
}
```

Sources: [hooks.ts](#root/ktA9c40cDis2)

## 安全机制

### 工作区信任检查

所有 Hook 都要求工作区信任（`src/utils/hooks.ts:286-310`）。这是纵深防御措施——防止恶意仓库的 `.claude/settings.json` 在未信任的情况下执行任意命令：

```typescript
export function shouldSkipHookDueToTrust(): boolean {
  const isInteractive = !getIsNonInteractiveSession()
  if (!isInteractive) return false  // SDK 模式隐式信任
  
  const hasTrust = checkHasTrustDialogAccepted()
  return !hasTrust
}
```

Sources: [hooks.ts](#root/iJ8AMcVUuI5G)

### 网络沙箱

命令型 Hook 启用时，系统对其应用网络限制（`src/utils/hooks.ts:1020-1060`）：

```typescript
if (SandboxManager.isSandboxingEnabled()) {
  sandboxedCommand = await SandboxManager.wrapWithSandbox(
    finalCommand,
    undefined,
    {
      network: {
        allowedDomains: [],  // 拒绝所有出站
        deniedDomains: [],
      },
      filesystem: {
        allowWrite: ['/'],  // 允许读写项目文件
        denyWrite: [],
        allowRead: [],
        denyRead: [],
      },
    },
    signal,
  )
}
```

Sources: [hooks.ts](#root/Hx5zX2pmS02Z)

### HTTP Hook 策略

HTTP Hook 支持 URL 白名单和请求头环境变量插值（`src/utils/hooks/execHttpHook.ts`）：

```typescript
function getHttpHookPolicy() {
  const settings = settingsModule.getInitialSettings()
  return {
    allowedUrls: settings.allowedHttpHookUrls,
    allowedEnvVars: settings.httpHookAllowedEnvVars,
  }
}
```

Sources: [execHttpHook.ts](#root/Kvdq0jexLEg2)

## 生命周期钩子实战

### PreToolUse：拦截工具调用

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "security-check.sh",
        "if": "Bash(curl|wget|nc|ssh)"
      }]
    }]
  }
}
```

返回 `permissionDecision: "deny"` 将阻止工具执行并显示阻塞错误。

### SessionStart：初始化上下文

```json
{
  "hooks": {
    "SessionStart": [{
      "matcher": "",
      "hooks": [{
        "type": "prompt",
        "prompt": "分析项目结构，返回关键文件列表：\n$ARGUMENTS",
        "model": "claude-sonnet-4-6"
      }]
    }]
  }
}
```

返回 `initialUserMessage` 可设置会话的初始用户消息。

### PostToolUse：修改 MCP 工具输出

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Read",
      "hooks": [{
        "type": "agent",
        "prompt": "验证读取的文件不包含敏感信息：\n$ARGUMENTS"
      }]
    }]
  }
}
```

返回 `updatedMCPToolOutput` 可替换 MCP 工具的原始输出。

Sources: [hooks.ts](#root/ZlGvsop5oe4C)

## 性能优化

### 快速路径

当所有 Hook 都是内部回调时，系统使用快速路径（`src/utils/hooks.ts:2190-2220`）：

```typescript
if (matchedHooks.every(
  m => m.hook.type === 'callback' || m.hook.type === 'function',
)) {
  // 跳过 span/progress/resultLoop
  // 测量：6.01µs → ~1.8µs (-70%)
  for (const { hook } of matchedHooks.entries()) {
    if (hook.type === 'callback') {
      await hook.callback(hookInput, toolUseID, signal, i, context)
    }
  }
  return
}
```

Sources: [hooks.ts](#root/iYVpEVtE1XJy)

### 事件过滤

`hasHookForEvent()` 函数用于快速检查是否存在匹配的 Hook，避免不必要的初始化开销：

```typescript
function hasHookForEvent(hookEvent, appState, sessionId): boolean {
  const snap = getHooksConfigFromSnapshot()?.[hookEvent]
  if (snap?.length > 0) return true
  const reg = getRegisteredHooks()?.[hookEvent]
  if (reg?.length > 0) return true
  if (appState?.sessionHooks.get(sessionId)?.hooks[hookEvent]) return true
  return false
}
```

Sources: [hooks.ts](#root/OZtW9sMySNkB)

## 下一步

*   了解如何通过 [Skills 开发](22-skills-ji-neng-kai-fa.md) 创建可复用的 Hook 打包
*   探索 [MCP 协议集成](12-mcp-xie-yi-ji-cheng.md) 与 Hooks 的结合使用
*   参考 [权限模型](15-quan-xian-mo-xing-yu-gui-ze-yin-qing.md) 理解 Hooks 在安全体系中的位置

## 相关条目
- [[22-skills-ji-neng-kai-fa]]
- [[20-memory-ji-yi-xi-tong]]
