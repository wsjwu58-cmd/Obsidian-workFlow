# 11-nei-zhi-gong-ju-xiang-jie
Claude Code 的内置工具系统是连接 AI 大语言模型与真实世界操作的核心桥梁。本章节深入解析 50+ 内置工具的架构设计、分类体系、执行机制和安全模型，帮助开发者理解工具系统如何让 AI 从"纸上谈兵"进化到"动手实干"。

## 工具系统架构总览

Claude Code 的工具系统建立在三个核心抽象之上：**Tool 接口定义**（`src/Tool.ts`）、**工具注册中心**（`src/tools.ts`）和**工具执行引擎**。这三层架构确保了工具的标准化、可扩展性和安全可控。

```
flowchart TB
    subgraph Tool接口层["Tool 接口层 (src/Tool.ts)"]
        A["buildTool<T> 工厂函数"]
        B["Tool<T> 泛型类型定义"]
        C["35+ 字段结构化接口"]
    end
    
    subgraph 工具注册中心["工具注册中心 (src/tools.ts)"]
        D["getAllBaseTools()"]
        E["getTools(permissionContext)"]
        F["filterToolsByDenyRules()"]
    end
    
    subgraph 工具执行层["工具执行层"]
        G["QueryEngine 编排"]
        H["StreamingToolExecutor"]
        I["findToolByName()"]
    end
    
    subgraph 工具实例["50+ 工具实例"]
        J["FileReadTool / FileEditTool / FileWriteTool"]
        K["BashTool / PowerShellTool"]
        L["AgentTool / Task*Tool"]
        M["WebSearchTool / WebFetchTool"]
        N["MCPTool / LSPTool"]
    end
    
    A --> B
    B --> C
    D --> E
    E --> F
    G --> H
    H --> I
    I --> J
    I --> K
    I --> L
    I --> M
    I --> N
```

**架构核心原则**：

*   **类型安全优先**：所有工具通过 `buildTool()` 工厂创建，`satisfies ToolDef` 确保编译时检查
*   **权限分层控制**：工具注册时过滤 blanket deny 规则，运行时执行细粒度权限检查
*   **延迟加载优化**：低频工具标记 `shouldDefer`，通过 ToolSearch 按需加载
*   **dead code elimination**：条件工具通过 `feature()` gates 在构建时剔除

Sources: [src/Tool.ts:650-793](#root/VN6Bb77fRWOr) Sources: [src/tools.ts:150-260](#root/GOEicE3kUgUA)

## Tool 接口：35+ 字段的统一契约

### 核心四要素

每个工具必须实现四个核心字段，定义了工具的身份、能力边界和执行逻辑：

| 字段 | 类型 | 职责 | 示例 |
| --- | --- | --- | --- |
| `name` | `string` | 全局唯一标识符 | `"Bash"`, `"Read"`, `"Agent"` |
| `description()` | `(input) => Promise<string>` | **动态描述生成器** | `"Execute skill: lint"` 根据参数变化 |
| `inputSchema` | `z.ZodType` | 输入参数的类型定义和校验 | `z.object({command: z.string()})` |
| `call()` | `(args, context, ...) => Promise<ToolResult>` | 实际执行逻辑 | BashTool 解析命令 → Shell.exec() |

```typescript
// BashTool.tsx:1-50 — 典型的工具定义模式
export const BashTool = buildTool({
  name: 'Bash',
  inputSchema: lazySchema(() => z.object({
    command: z.string().describe('The bash command to execute'),
    timeout: z.number().optional().describe('Timeout in milliseconds'),
    // ... 其他参数
  })),
  maxResultSizeChars: 30_000,
  async description(input) {
    return `Execute shell command: ${input.command}`
  },
  async call(args, context, canUseTool, parentMessage, onProgress) {
    // 执行逻辑
    return { data: execResult }
  }
} satisfies ToolDef<Input, Output>)
```

Sources: [src/Tool.ts:370-420](#root/NavBgoOSEC97) Sources: [src/tools/BashTool/BashTool.tsx:1-150](#root/sAYBInkiwX4Y)

### 安全与权限字段

工具的安全能力通过一组可选方法实现分层防护：

| 方法 | 返回类型 | 触发时机 | 默认行为 |
| --- | --- | --- | --- |
| `validateInput()` | `ValidationResult` | **权限检查之前** | 返回 `{result: true}` |
| `checkPermissions()` | `PermissionResult` | 校验通过后 | `{behavior: 'allow'}` |
| `isReadOnly()` | `boolean` | 权限判定辅助 | `false` |
| `isDestructive()` | `boolean` | 不可逆操作标记 | `false` |
| `preparePermissionMatcher()` | `(pattern) => boolean` | Hook 条件匹配准备 | 无 |
| `interruptBehavior()` | `'cancel' \| 'block'` | 用户中断处理 | `'block'` |

**分层防护示例**（BashTool）：

```typescript
// BashTool.tsx:437-470 — 权限检查的典型实现
async validateInput(input) {
  // 1. 基础语法校验
  if (!input.command?.trim()) {
    return { result: false, message: 'Empty command', errorCode: 1 }
  }
  // 2. 危险命令检测
  const dangerous = detectDestructivePatterns(input.command)
  if (dangerous) {
    return { result: false, message: `Dangerous: ${dangerous}`, errorCode: 2 }
  }
  return { result: true }
}

async checkPermissions(input, context) {
  // 只读命令自动放行
  if (this.isReadOnly(input)) {
    return { behavior: 'allow', updatedInput: input }
  }
  // 其他命令走通用权限规则匹配
  return bashToolHasPermission(input, context)
}

isReadOnly(input) {
  const result = checkReadOnlyConstraints(input)
  return result.behavior === 'allow'
}
```

Sources: [src/Tool.ts:500-520](#root/q1TVHxvJwDb1) Sources: [src/tools/BashTool/bashPermissions.ts](#root/8rmsNsV04qTf)

### UI 渲染字段

工具结果的展示通过 React 组件定制化实现：

| 渲染方法 | 触发时机 | 用途 |
| --- | --- | --- |
| `renderToolUseMessage()` | 工具调用时 | 显示 "正在执行 Bash: npm test..." |
| `renderToolUseProgressMessage()` | 执行过程中 | 实时显示进度输出 |
| `renderToolResultMessage()` | 执行完成后 | 展示结果 diff、搜索匹配等 |
| `renderToolUseErrorMessage()` | 执行失败时 | 自定义错误展示 |
| `renderGroupedToolUse()` | 并行工具调用 | 批量显示结果 |

```typescript
// FileEditTool/UI.tsx — 渲染方法的典型实现
renderToolResultMessage(output: FileEditOutput) {
  return (
    <FileEditToolUpdatedMessage
      input={output.input}
      result={output.result}
      style={options.style}
      theme={options.theme}
    />
  )
}

renderToolUseMessage(input: Partial<EditInput>) {
  return (
    <MessageRow
      tool={<ToolUseLoader toolName="Edit" />}
      content={<span>Editing <FilePathLink path={input.file_path} /></span>}
    />
  )
}
```

Sources: [src/Tool.ts:540-650](#root/1O0w0AHE4D2J) Sources: [src/tools/FileEditTool/UI.tsx](#root/uZAGYNhlpBP0)

## 工具分类体系

### 按功能领域分类

Claude Code 的 50+ 工具可划分为六大功能域：

```
mindmap
  root((内置工具))
    文件操作
      FileReadTool
      FileEditTool
      FileWriteTool
      NotebookEditTool
      GlobTool
      GrepTool
    命令执行
      BashTool
      PowerShellTool
    Web能力
      WebSearchTool
      WebFetchTool
      WebBrowserTool
    任务管理
      TodoWriteTool
      TaskCreateTool
      TaskUpdateTool
      TaskListTool
      TaskStopTool
    对话协作
      AgentTool
      SendMessageTool
      AskUserQuestionTool
      TeamCreateTool
      TeamDeleteTool
    规划控制
      EnterPlanModeTool
      ExitPlanModeTool
      EnterWorktreeTool
      ExitWorktreeTool
```

### 按加载策略分类

| 加载策略 | 工具示例 | 说明 |
| --- | --- | --- |
| **始终加载** | AgentTool, BashTool, Read, Edit, Write | 核心工具，turn 1 可见 |
| **条件加载** | GrepTool, GlobTool | `hasEmbeddedSearchTools()` 返回 false 时加载 |
| **延迟加载** | WebSearchTool, ToolSearchTool | 标记 `shouldDefer: true`，需 ToolSearch 激活 |
| **Feature Flag** | WebBrowserTool, SleepTool | `feature('WEB_BROWSER_TOOL')` 开启 |
| **Ant-Only** | REPLTool, ConfigTool | `process.env.USER_TYPE === 'ant'` |

Sources: [src/tools.ts:180-250](#root/DibBHwWr1hfD)

## 核心工具详解

### 文件操作工具三角

FileRead、FileEdit、FileWrite 三大工具构成了 Claude Code 文件操作的基础，其设计遵循**风险分级原则**：

| 工具 | 权限级别 | 核心安全机制 | 结果预算 |
| --- | --- | --- | --- |
| **Read** | 只读（免审批） | 设备文件屏蔽、二进制拒绝 | `Infinity`（不走持久化） |
| **Edit** | 写入（需确认） | mtime 校验、原子性读-改-写 | 100,000 字符 |
| **Write** | 写入（需确认） | fileHistory 备份、行尾标准化 | 100,000 字符 |

**Read 工具的关键设计**：

```typescript
// FileReadTool.ts:530-573 — 去重机制防止 token 浪费
const existingState = readFileState.get(fullFilePath)
if (existingState && !existingState.isPartialView) {
  const mtimeMs = await getFileModificationTimeAsync(fullFilePath)
  // 文件未修改且范围相同 → 返回 file_unchanged
  if (mtimeMs === existingState.timestamp) {
    return { data: { type: 'file_unchanged', file: { filePath } } }
  }
}
```

**Edit 工具的原子性保证**：

```typescript
// FileEditTool.ts — 临界区设计
// 步骤 1-2 在临界区外（异步操作）
await fileHistoryTrackEdit()  // 备份旧内容
// 步骤 3-8 在临界区内（同步，无 await）
const fileContent = readFileSyncWithMetadata()  // 同步读取
getFileModificationTime()                         // mtime 校验
findActualString()                                // 引号标准化
writeTextContent()                                // 原子写入
readFileState.set()                               // 更新缓存
```

Sources: [src/tools/FileReadTool/FileReadTool.ts:530-573](#root/eqENhWYt13xw) Sources: [src/tools/FileEditTool/FileEditTool.ts](#root/M8Nm9B9JAuyx)

### BashTool：命令执行的精密控制

BashTool 是 Claude Code 最复杂的工具之一，其设计融合了安全、效率和用户体验的多重考量。

**只读命令判定**（自动免审批）：

```typescript
// BashTool.tsx:60-120 — 四类命令集合
const BASH_SEARCH_COMMANDS = new Set(['find', 'grep', 'rg', 'ag', ...])
const BASH_READ_COMMANDS = new Set(['cat', 'head', 'tail', 'wc', 'stat', ...])
const BASH_LIST_COMMANDS = new Set(['ls', 'tree', 'du'])
const BASH_SEMANTIC_NEUTRAL_COMMANDS = new Set(['echo', 'printf', 'true', ...])

// 复合命令必须所有非中性段都属于上述集合
```

**AST 安全解析**（防止语义混淆）：

```typescript
// bashPermissions.ts — tree-sitter 解析
async preparePermissionMatcher({ command }) {
  const parsed = await parseForSecurity(command)  // tree-sitter bash 解析
  if (parsed.kind !== 'simple') {
    return () => true  // 解析失败 → fail-safe
  }
  // 拆分为子命令列表
  const subcommands = parsed.commands.map(c => c.argv.join(' '))
  return pattern => subcommands.some(cmd => matchWildcardPattern(pattern, cmd))
}
```

**自动后台化机制**：

```
命令执行 → 15 秒未完成（ASSISTANT_BLOCKING_BUDGET_MS）
         → 检查 isAutobackgroundingAllowed(command)
         → 前台任务 → 后台任务（backgroundExistingForegroundTask）
         → 返回 taskId，AI 继续其他工作
         → 后台完成后通知机制汇报结果
```

Sources: [src/tools/BashTool/BashTool.tsx:60-120](#root/zw0Q9xL3mgyy) Sources: [src/tools/BashTool/bashPermissions.ts](#root/8rmsNsV04qTf) Sources: [src/tools/BashTool/shouldUseSandbox.ts](#root/mF6kNTy9sJ13)

### 任务管理双轨架构

Claude Code 维护两套并行的任务管理系统，通过 `isTodoV2Enabled()` 切换：

| 维度 | V1: TodoWrite | V2: TaskCreate/TaskList |
| --- | --- | --- |
| **存储** | 内存（Zustand store） | 文件系统（`~/.claude/tasks/`） |
| **持久化** | 进程退出丢失 | 跨进程存活 |
| **数据模型** | 扁平三元组 | 完整实体（id, subject, owner, blocks, blockedBy） |
| **并发安全** | 无 | 文件锁 + 高水位标记 |

**V2 任务认领的并发控制**：

```typescript
// tasks.ts — 原子性任务认领
async function claimTask(taskListId, agentId, taskId, options) {
  const release = await lockfile.lock(lockPath, LOCK_OPTIONS)
  try {
    const tasks = await listTasks(taskListId)
    const task = tasks.find(t => t.id === taskId)
    
    // 检查前置条件
    if (task.owner && task.owner !== agentId) {
      return { reason: 'already_claimed' }
    }
    if (task.status === 'completed') {
      return { reason: 'already_resolved' }
    }
    if (task.blockedBy.some(id => !isCompleted(tasks, id))) {
      return { reason: 'blocked' }
    }
    
    // 原子更新
    await updateTask(taskListId, taskId, { 
      status: 'in_progress',
      owner: agentId 
    })
  } finally {
    await release()
  }
}
```

Sources: [src/tools/TodoWriteTool/TodoWriteTool.ts](#root/hoxJDmA1RP1N) Sources: [src/utils/tasks.ts](#root/15aH57bn3yDJ)

### AgentTool：多 Agent 协作核心

AgentTool 允许 AI 派生子 Agent 执行任务，支持工作树隔离、团队协作和远程执行：

```typescript
// AgentTool.tsx — 输入参数定义
const fullInputSchema = lazySchema(() => 
  z.object({
    description: z.string().describe('简短任务描述'),
    prompt: z.string().describe('详细任务指令'),
    subagent_type: z.string().optional(),
    model: z.enum(['sonnet', 'opus', 'haiku']).optional(),
    run_in_background: z.boolean().optional(),
    // 多 Agent 参数
    name: z.string().optional().describe('Agent 名称，用于 SendMessage'),
    team_name: z.string().optional(),
    mode: permissionModeSchema().optional(),
    // 隔离参数
    isolation: z.enum(['worktree', 'remote']).optional(),
    cwd: z.string().optional(),
  })
)
```

**异步 Agent 的权限控制**：

```typescript
// constants/tools.ts — 异步 Agent 的工具白名单
export const ASYNC_AGENT_ALLOWED_TOOLS = new Set([
  FILE_READ_TOOL_NAME,
  WEB_SEARCH_TOOL_NAME,
  TODO_WRITE_TOOL_NAME,
  GREP_TOOL_NAME,
  WEB_FETCH_TOOL_NAME,
  GLOB_TOOL_NAME,
  ...SHELL_TOOL_NAMES,
  FILE_EDIT_TOOL_NAME,
  FILE_WRITE_TOOL_NAME,
  NOTEBOOK_EDIT_TOOL_NAME,
  SKILL_TOOL_NAME,
])

// 禁止的工具（防止递归）
export const ALL_AGENT_DISALLOWED_TOOLS = new Set([
  TASK_OUTPUT_TOOL_NAME,
  EXIT_PLAN_MODE_V2_TOOL_NAME,
  ENTER_PLAN_MODE_TOOL_NAME,
  AGENT_TOOL_NAME,  // 防止 Agent 嵌套调用 Agent
  TASK_STOP_TOOL_NAME,
])
```

Sources: [src/tools/AgentTool/AgentTool.tsx:80-100](#root/94Cc6U9km4N1) Sources: [src/constants/tools.ts:1-80](#root/zSISrVTg8kij)

## 工具执行链路

### 完整调用序列

从 AI 发出 `tool_use` 到结果回传，经过十个关键步骤：

```
sequenceDiagram
    participant AI as AI Model
    participant QE as QueryEngine
    participant STE as StreamingToolExecutor
    participant Tool as Tool Registry
    participant Perm as Permission System
    participant Impl as Tool Implementation

    AI->>QE: tool_use { name: "Bash", input: {...} }
    QE->>STE: addTool(tool_use)
    STE->>Tool: findToolByName("Bash")
    Tool-->>STE: BashTool instance
    STE->>BashTool: validateInput(input)
    BashTool-->>STE: { result: true }
    
    alt 非只读命令
        STE->>Perm: canUseTool(tool)
        Perm-->>STE: Pending (等待用户确认)
        Note over STE: UI 显示权限对话框
    end
    
    STE->>BashTool: checkPermissions(input, context)
    BashTool-->>STE: { behavior: "allow" }
    
    STE->>Impl: call(args, context, onProgress)
    Impl-->>STE: ToolResult { data: execResult }
    
    STE->>STE: mapToolResultToToolResultBlockParam()
    STE->>QE: 返回 ToolResult
    QE->>AI: 新消息追加到对话
```

### 工具结果的预算控制

每个工具声明 `maxResultSizeChars` 控制输出上限，超出时持久化到磁盘：

```typescript
// toolResultStorage.ts — 结果持久化逻辑
export async function applyToolResultBudget(
  content: string,
  toolName: string,
  toolUseId: string
): Promise<{ preview: string; path: string; isPersisted: boolean }> {
  if (content.length <= maxResultSizeChars) {
    return { preview: content, path: '', isPersisted: false }
  }
  
  // 持久化到磁盘
  const path = await getToolResultPath(toolUseId)
  await writeFile(path, content, 'utf-8')
  
  // 返回预览 + 文件路径
  const preview = content.substring(0, PREVIEW_SIZE_BYTES) + '\n[...truncated...]'
  return { preview, path, isPersisted: true }
}
```

| 工具 | maxResultSizeChars | 特殊处理 |
| --- | --- | --- |
| FileReadTool | `Infinity` | 永不持久化（避免循环 Read→file→Read） |
| BashTool | 30,000 | 超长输出截断 |
| SkillTool | 100,000 | 技能执行结果 |
| WebSearchTool | 100,000 | 搜索结果列表 |

Sources: [src/utils/toolResultStorage.ts](#root/znORjWfVb738)

## MCP 工具集成

### MCPTool 的动态适配机制

MCP Server 提供的工具通过统一的 `MCPTool` 模板动态实例化：

```typescript
// MCPTool.ts — 基础模板
export const MCPTool = buildTool({
  isMcp: true,
  name: 'mcp',  // 会被 mcpClient.ts 覆盖为 mcp__server__tool
  maxResultSizeChars: 100_000,
  inputSchema: z.object({}).passthrough(),  // 允许任意输入
  
  // 关键：description/prompt/call 在 mcpClient.ts 中动态覆盖
  async description() { return DESCRIPTION },
  async call() { return { data: '' } },
})
```

### MCP 工具的权限处理

MCP 工具通过 `mcpInfo` 字段标记来源，支持服务器级别的 blanket deny：

```typescript
// mcpClient.ts — MCP 工具注册
function registerMcpTool(serverName: string, toolDef: MCPToolDefinition) {
  const mcpTool = Object.assign({}, MCPTool, {
    name: `mcp__${serverName}__${toolDef.name}`,
    mcpInfo: { serverName, toolName: toolDef.name },
    description: () => toolDef.description,
    inputSchema: convertJsonSchemaToZod(toolDef.inputSchema),
    call: (args) => executeMcpTool(serverName, toolDef.name, args)
  })
}
```

Sources: [src/tools/MCPTool/MCPTool.ts](#root/ZmERFEJTHXLj) Sources: [src/services/mcp/mcpClient.ts](#root/3gaKu1cZpRAc)

## 工具搜索与发现

### ToolSearch 的加权算法

当工具数量超过 50 个时，AI 可能不知道该用哪个。ToolSearch 提供了关键词发现机制：

```typescript
// ToolSearchTool.ts — 搜索评分算法
function scoreToolMatch(tool: Tool, keywords: string[]): number {
  let score = 0
  
  // 工具名精确匹配: 10 分
  if (keywords.some(k => tool.name.toLowerCase().includes(k))) {
    score += 10
  }
  
  // searchHint 匹配: 4 分
  const hintWords = tool.searchHint?.split(' ') ?? []
  keywords.forEach(k => {
    if (hintWords.includes(k)) score += 4
  })
  
  // 描述匹配: 2 分
  const desc = await tool.description()
  keywords.forEach(k => {
    if (desc.toLowerCase().includes(k)) score += 2
  })
  
  return score
}

// 延迟加载工具的实际加载
async function loadDeferredTool(toolName: string): Promise<Tool> {
  const tool = deferredTools.find(t => t.name === toolName)
  if (!tool) throw new Error(`Deferred tool not found: ${toolName}`)
  
  // 执行实际的工具初始化
  return await tool.loader()
}
```

Sources: [src/tools/ToolSearchTool/ToolSearchTool.ts](#root/Fs0Wo0RO8ZVo)

## 特殊场景工具

### LSPTool：语言服务器集成

LSPTool 提供了对 Language Server Protocol 的访问，支持代码导航和静态分析：

```typescript
// LSPTool.ts — 支持的 LSP 操作
const SUPPORTED_OPERATIONS = [
  'goToDefinition',      // 跳转到定义
  'findReferences',      // 查找引用
  'hover',               // 悬停信息
  'documentSymbol',      // 文档符号
  'workspaceSymbol',     // 工作区符号搜索
  'goToImplementation',   // 跳转到实现
  'prepareCallHierarchy', // 调用层次结构
  'incomingCalls',       // 传入调用
  'outgoingCalls',       // 传出调用
]
```

Sources: [src/tools/LSPTool/LSPTool.ts:50-80](#root/hFD4XYO1MZJY)

### SkillTool：技能执行框架

SkillTool 允许 AI 执行预定义的技能/提示，支持内置技能和 MCP 技能：

```typescript
// SkillTool.ts — 技能执行入口
async call({ command, args }, context, canUseTool, parentMessage, onProgress) {
  const commandDef = await getCommand(command)
  
  if (command.type === 'prompt') {
    // 技能型命令 → 派生子 Agent 执行
    return executeForkedSkill(commandDef, args, context)
  } else {
    // 普通命令 → 本地执行
    return executeLocalCommand(commandDef, args)
  }
}
```

Sources: [src/tools/SkillTool/SkillTool.ts:150-250](#root/NyB9SsfvIOgF)

## 总结与进阶路径

内置工具系统是 Claude Code 能力的核心延伸。通过理解以下关键设计，开发者可以更有效地使用和扩展工具：

**核心设计理念**：

*   **类型安全**：通过 `buildTool()` + `satisfies ToolDef` 实现编译时检查
*   **权限分层**：工具级 `validateInput` → 权限系统 `checkPermissions` → UI 确认
*   **延迟加载**：通过 `shouldDefer` 减少 turn 1 的 token 开销
*   **原子性保证**：临界区设计防止并发冲突

**进阶学习路径**：

*   想深入理解工具的 UI 渲染机制 → 参见 [MCP 协议集成](12-mcp-xie-yi-ji-cheng.md)
*   想了解如何创建自定义工具 → 参见 [自定义 Agents](21-zi-ding-yi-agents.md)
*   想理解工具的权限模型 → 参见 [权限模型与规则引擎](15-quan-xian-mo-xing-yu-gui-ze-yin-qing.md)
*   想探索 Computer Use 能力 → 参见 [Computer Use 电脑操控](13-computer-use-dian-nao-cao-kong.md)

## 相关条目
- [[10-gong-ju-xi-tong-jia-gou]]
- [[12-mcp-xie-yi-ji-cheng]]
