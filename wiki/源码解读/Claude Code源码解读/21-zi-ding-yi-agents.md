# 21-zi-ding-yi-agents
Claude Code 的 Agent 系统是一套完整的多智能体协作框架，涵盖从 Markdown 文件定义到运行时工具过滤的全链路设计。本文档从源码层面揭示自定义 Agent 的完整生命周期、配置格式、工具过滤机制以及与 AgentTool 的联动细节。

## Agent 定义的三层架构

Claude Code 采用分层加载策略，支持三种来源的 Agent 定义，按优先级合并实现灵活的覆盖机制：

```
flowchart TB
    subgraph sources["Agent 来源分层"]
        A["🔧 Built-in Agents<br/>src/tools/AgentTool/built-in/"]
        B["📦 Plugin Agents<br/>插件系统注册"]
        C["👤 User/Project/Policy<br/>.claude/agents/*.md"]
    end
    
    subgraph merge["合并流程"]
        D["getActiveAgentsFromList()"]
        E["按 agentType 去重"]
        F["后者覆盖前者"]
    end
    
    A --> D
    B --> D
    C --> D
    D --> E
    E --> F
    
    style C fill:#90EE90
    style F fill:#FFD700
```

合并逻辑实现于 `getActiveAgentsFromList()` 函数中，按以下优先级排序：Built-in < Plugin < User Settings < Project Settings < Flag Settings < Policy Settings。当同名 `agentType` 出现时，后加载的来源覆盖先加载的来源，这意味着你可以在项目级 `.claude/agents/` 中定义同名 Agent 来完全替换内置行为。

| 来源 | 位置 | 优先级 | 典型用途 |
| --- | --- | --- | --- |
| **Built-in** | `src/tools/AgentTool/built-in/` 硬编码 | 最低 | Explore、Plan、General Purpose |
| **Plugin** | 通过插件系统注册 | 中 | 第三方扩展 |
| **User Settings** | `~/.claude/agents/*.md` | 中高 | 用户个人偏好 Agent |
| **Project Settings** | `.claude/agents/*.md` | 高 | 项目特定角色 |
| **Policy Settings** | 托管策略配置 | 最高 | 企业强制 Agent |

Sources: [loadAgentsDir.ts](#root/sT4ainNzh7mH)

## Markdown Agent 文件格式

自定义 Agent 通过 Markdown 文件定义，采用 YAML frontmatter 声明元数据，文件正文作为 system prompt。

### 完整字段参考

```gfm
---
# === 必需字段 ===
name: "reviewer"                    # Agent 标识（agentType）
description: "Code review specialist, read-only analysis"

# === 工具控制 ===
tools: "Read,Glob,Grep,Bash"        # 允许的工具列表
disallowedTools: "Write,Edit"      # 显式禁止的工具

# === 模型配置 ===
model: "haiku"                      # 指定模型或 "inherit"
effort: "high"                      # 推理努力：low/medium/high

# === 行为控制 ===
maxTurns: 10                        # 最大 agentic 轮次
permissionMode: "plan"              # 权限模式
background: true                    # 始终后台运行
initialPrompt: "/search TODO"       # 首轮消息前缀

# === 隔离与持久化 ===
isolation: "worktree"               # git worktree 隔离
memory: "project"                   # 持久记忆范围

# === MCP 服务器 ===
mcpServers:
  - "slack"                         # 引用已配置服务器
  - database:                       # 内联定义
      command: "npx"
      args: ["mcp-db"]

# === Hooks ===
hooks:
  PreToolUse:
    - command: "audit-log.sh"
      timeout: 5000

# === Skills ===
skills: "code-review,security-review"

# === 显示控制 ===
color: "blue"
---

你是代码审查专家。你的职责是分析代码质量...

（正文内容 = 完整 system prompt）
```

### 字段语义详解

**`tools` 字段**的解析逻辑支持三种语义：

*   **未指定**：Agent 可使用全部工具（默认全能模式）
*   **空数组 `[]`**：Agent 禁止使用任何工具
*   **具体工具列表**：白名单模式，只能使用列出的工具

```typescript
// src/utils/markdownConfigLoader.ts:89-103
export function parseAgentToolsFromFrontmatter(
  toolsValue: unknown,
): string[] | undefined {
  const parsed = parseToolListString(toolsValue)
  if (parsed === null) {
    return toolsValue === undefined ? undefined : []
  }
  if (parsed.includes('*')) {
    return undefined  // 通配符 = 全部工具
  }
  return parsed
}
```

**`memory` 字段**启用后，系统自动注入 `Write`/`Edit`/`Read` 工具，并在 system prompt 末尾追加记忆操作指令：

*   **`local`**：当前项目、当前机器有效（`.claude/agent-memory-local/`）
*   **`project`**：项目级共享，可提交到版本控制（`.claude/agent-memory/`）
*   **`user`**：用户级跨项目共享（`~/.claude/agent-memory/`）

Sources: [loadAgentsDir.ts](#root/vuUQ0wTFrVlQ), [agentMemory.ts](#root/Q8WBrFmGUVng)

## 加载与发现机制

`getAgentDefinitionsWithOverrides()` 是 Agent 加载的核心入口，被 memoize 缓存以避免重复文件系统扫描：

```
sequenceDiagram
    participant Caller as AgentTool.call()
    participant Loader as getAgentDefinitionsWithOverrides()
    participant FS as 文件系统
    participant Plugins as 插件系统
    participant Memory as Memory Snapshot

    Caller->>Loader: getAgentDefinitionsWithOverrides(cwd)
    alt SIMPLE 模式
        Loader-->>Caller: 仅返回 Built-in Agents
    else 标准模式
        Loader->>FS: loadMarkdownFilesForSubdir('agents', cwd)
        Note over FS: 扫描多层级目录结构
        Loader->>Plugins: loadPluginAgents()
        alt AGENT_MEMORY_SNAPSHOT 启用
            Loader->>Memory: initializeAgentMemorySnapshots()
        end
        Loader->>Loader: getActiveAgentsFromList() 合并去重
        Loader->>Loader: setAgentColor() 分配颜色
        Loader-->>Caller: {activeAgents, allAgents, failedFiles}
    end
```

### 目录扫描策略

`loadMarkdownFilesForSubdir()` 从三个层级收集 Agent 定义：

1.  **托管目录**（最高优先级）：`getManagedFilePath()/.claude/agents/*.md`
2.  **用户目录**：`~/.claude/agents/*.md`（需要 `userSettings` 功能开启）
3.  **项目目录**：从当前目录向上遍历到 git 根目录，收集所有 `.claude/agents/*.md`

```typescript
// src/utils/markdownConfigLoader.ts:221-280
export const loadMarkdownFilesForSubdir = memoize(
  async function (subdir, cwd) {
    const userDir = join(getClaudeConfigHomeDir(), subdir)
    const managedDir = join(getManagedFilePath(), '.claude', subdir)
    const projectDirs = getProjectDirsUpToHome(subdir, cwd)
    
    // 优先级：managed > user > project
    const allFiles = [...managedFiles, ...userFiles, ...projectFiles]
    
    // inode 去重：处理符号链接指向同一物理文件的情况
    const fileIdentities = await Promise.all(
      allFiles.map(file => getFileIdentity(file.filePath))
    )
    // ...
  }
)
```

目录遍历在 git 根目录处停止，防止项目外部的配置泄露。对于 git worktree，如果 worktree 本身没有 `agents/` 子目录，则自动回退到主仓库的 `agents/` 目录。

Sources: [loadAgentsDir.ts](#root/2LPoHucbrs4F)

## 工具过滤的实现

当 Agent 被派生时，`AgentTool` 根据定义中的 `tools` / `disallowedTools` 对可用工具列表进行双层过滤：

```
flowchart LR
    subgraph "第一层：系统过滤"
        A["全部工具"] --> B{"permissionMode"}
        B -->|plan| C["+ ExitPlanMode"]
        B -->|其他| D["常规过滤"]
    end
    
    subgraph "第二层：Agent 定义过滤"
        D --> E{"disallowedTools"}
        E -->|有| F["移除禁用工具"]
        E -->|无| G["保留全部"]
        
        F --> H{"tools 白名单"}
        G --> H
    end
    
    H -->|未指定| I["全部可用"]
    H -->|已指定| J["仅白名单工具"]
    H -->|"*"| I
```

**过滤层级解析**：

1.  **系统级禁止**：`ALL_AGENT_DISALLOWED_TOOLS` 集合中的工具对所有 Agent 禁用
2.  **自定义禁止**：`CUSTOM_AGENT_DISALLOWED_TOOLS` 对非内置 Agent 额外禁用
3.  **异步限制**：`ASYNC_AGENT_ALLOWED_TOOLS` 限制后台运行的 Agent 工具集
4.  **Agent 定义**：`disallowedTools` 从上述结果中进一步移除
5.  **Agent 定义**：`tools` 白名单（如果指定）限制为仅允许的工具

```typescript
// src/tools/AgentTool/agentToolUtils.ts:66-100
export function filterToolsForAgent({
  tools,
  isBuiltIn,
  isAsync = false,
  permissionMode,
}: {
  tools: Tools
  isBuiltIn: boolean
  isAsync?: boolean
  permissionMode?: PermissionMode
}): Tools {
  return tools.filter(tool => {
    // MCP 工具始终允许
    if (tool.name.startsWith('mcp__')) return true
    
    // plan 模式下允许 ExitPlanMode
    if (toolMatchesName(tool, EXIT_PLAN_MODE_V2_TOOL_NAME) && 
        permissionMode === 'plan') return true
    
    // 系统级禁用
    if (ALL_AGENT_DISALLOWED_TOOLS.has(tool.name)) return false
    if (!isBuiltIn && CUSTOM_AGENT_DISALLOWED_TOOLS.has(tool.name)) return false
    if (isAsync && !ASYNC_AGENT_ALLOWED_TOOLS.has(tool.name)) return false
    
    return true
  })
}
```

以内置 Explore Agent 为例，其 `disallowedTools` 配置确保只读行为：

```typescript
// src/tools/AgentTool/built-in/exploreAgent.ts
export const EXPLORE_AGENT: BuiltInAgentDefinition = {
  agentType: 'Explore',
  disallowedTools: [
    AGENT_TOOL_NAME,           // 不能嵌套调用 Agent
    EXIT_PLAN_MODE_TOOL_NAME,  // 不需要 plan mode
    FILE_EDIT_TOOL_NAME,       // 只读
    FILE_WRITE_TOOL_NAME,      // 只读
    NOTEBOOK_EDIT_TOOL_NAME,   // 只读
  ],
  // 外部用户使用 haiku，内置用户继承主线程模型
  model: process.env.USER_TYPE === 'ant' ? 'inherit' : 'haiku',
  omitClaudeMd: true,  // 跳过 CLAUDE.md 层级以节省 token
}
```

Sources: [agentToolUtils.ts](#root/QTkcNMe6qkiH), [exploreAgent.ts](#root/LnccoK3gNNOs)

## System Prompt 注入机制

Agent 的 system prompt 通过 `getSystemPrompt()` 闭包实现延迟生成，这一设计允许在 agent 启动时根据运行时状态动态调整 prompt 内容：

```typescript
// src/tools/AgentTool/loadAgentsDir.ts:620-635
const agentDef: CustomAgentDefinition = {
  agentType: agentType,
  getSystemPrompt: () => {
    if (isAutoMemoryEnabled() && memory) {
      const memoryPrompt = loadAgentMemoryPrompt(agentType, memory)
      return systemPrompt + '\n\n' + memoryPrompt
    }
    return systemPrompt
  },
  // ...
}
```

**关键设计原则**：

1.  **Markdown 正文 = 完整 system prompt**：不是追加到默认 prompt，而是完全替换主线程的 system prompt
2.  **Memory 指令延迟追加**：memory 提示在 `getSystemPrompt()` 调用时才计算，支持在文件加载后动态启用 memory 功能
3.  **Built-in Agent 的动态调整**：内置 Agent 的 `getSystemPrompt` 接受 `toolUseContext` 参数，可根据运行时状态（如是否使用嵌入式搜索工具）调整 prompt

```typescript
// src/tools/AgentTool/built-in/exploreAgent.ts
function getExploreSystemPrompt(): string {
  // 根据是否使用嵌入式搜索工具调整指引
  const embedded = hasEmbeddedSearchTools()
  const globGuidance = embedded
    ? `- Use \`find\` via ${BASH_TOOL_NAME} for broad file pattern matching`
    : `- Use ${GLOB_TOOL_NAME} for broad file pattern matching`
  // ...
}
```

Sources: [loadAgentsDir.ts](#root/88CmScRwYfCr)

## AgentTool 调用链路

当主 Agent 调用 `AgentTool` 派生子 Agent 时，执行以下完整流程：

```
flowchart TD
    A["AgentTool.call()"] --> B["查找 agent 定义"]
    B --> C{"subagent_type 指定?"}
    C -->|是| D["使用指定类型"]
    C -->|否| E{"Fork 实验启用?"}
    E -->|是| F["走 Fork 路径"]
    E -->|否| G["默认 general-purpose"]
    
    D --> H["检查 MCP 服务器要求"]
    G --> H
    F --> H
    H --> I{"要求满足?"}
    I -->|否| J["抛出错误"]
    I -->|是| K["过滤工具列表"]
    
    K --> L["解析模型配置"]
    L --> M{"isolation 模式"}
    M -->|"worktree"| N["创建 git worktree"]
    M -->|"remote"| O["远程执行（ant-only）"]
    M -->|"无"| P["使用当前目录"]
    
    N --> Q["获取/构建 system prompt"]
    O --> Q
    P --> Q
    Q --> R{"后台运行?"}
    
    R -->|是| S["registerAsyncAgent()"]
    R -->|否| T["runAgent() 同步执行"]
    
    S --> U["<task-notification> 结果"]
    T --> V["返回结果"]
```

**模型解析优先级**：

1.  `AgentTool.call()` 的 `model` 参数（显式覆盖）
2.  Agent 定义的 `model` 字段
3.  主线程模型（通过 `"inherit"` 或默认值）

**隔离模式**：`worktree` 模式创建独立的 git worktree，使 Agent 在代码库的隔离副本上工作，避免与主线程产生冲突。`remote` 模式仅在内部构建（`USER_TYPE === 'ant'`）中可用。

Sources: [AgentTool.tsx](#root/o9MS30jraDo6)

## 内置 Agent 参考

| Agent | agentType | 角色描述 | 工具限制 | 适用场景 |
| --- | --- | --- | --- | --- |
| **General Purpose** | `general-purpose` | 默认子 Agent | 全部工具 | 通用任务执行 |
| **Explore** | `Explore` | 代码搜索专家 | 只读 | 快速定位文件、搜索代码 |
| **Plan** | `Plan` | 规划专家 | 只读 + ExitPlanMode | 制定实施计划 |
| **Verification** | `verification` | 结果验证 | feature flag 控制 | 验证代码变更 |
| **Code Guide** | `claude-code-guide` | Claude Code 使用指南 | 只读 | 帮助用户学习 CLI |
| **Statusline Setup** | `statusline-setup` | 状态栏配置 | 有限 | 配置终端 UI |

**Explore Agent 的特殊优化**：`omitClaudeMd: true` 标志跳过 CLAUDE.md 层级注入，对应节省约 5-15 Gtok/周（基于 3400 万+ Explore 调用统计）。

SDK 入口点（`sdk-ts`/`sdk-py`/`sdk-cli`）不加载 Code Guide Agent，可通过 `CLAUDE_AGENT_SDK_DISABLE_BUILTIN_AGENTS` 环境变量完全禁用内置 Agent。

Sources: [builtInAgents.ts](#root/qBa5vRoucvUM), [exploreAgent.ts](#root/LnccoK3gNNOs)

## Hooks 与插件集成

Agent 支持通过 frontmatter 的 `hooks` 字段注册会话级钩子，在特定事件触发时执行自定义逻辑：

```typescript
// src/schemas/hooks.ts
const AgentHookSchema = z.object({
  type: z.literal('agent'),
  prompt: z.string().describe(
    '验证提示（使用 $ARGUMENTS 占位符获取钩子输入 JSON）'
  ),
  if: IfConditionSchema(),  // 权限规则语法过滤
  timeout: z.number().positive().optional(),
  model: z.string().optional(),
  statusMessage: z.string().optional(),
  once: z.boolean().optional(),
})
```

**插件 Agent 的限制**：出于安全考虑，插件 Agent 的 frontmatter 中 `permissionMode`、`hooks`、`mcpServers` 字段被忽略。插件 Agent 可以通过插件清单级别注册这些功能，但单个 Agent 定义不能覆盖。

```typescript
// src/utils/plugins/loadPluginAgents.ts:140-150
// permissionMode, hooks, and mcpServers are intentionally NOT parsed for
// plugin agents. Plugins are third-party marketplace code; these fields
// escalate what the agent can do beyond what the user approved at install time.
for (const field of ['permissionMode', 'hooks', 'mcpServers'] as const) {
  if (frontmatter[field] !== undefined) {
    logForDebugging(
      `Plugin agent file ${filePath} sets ${field}, which is ignored.`
    )
  }
}
```

Sources: [loadPluginAgents.ts](#root/1VpYGlzELPbD)

## 颜色管理系统

Agent 通过 `color` 字段指定在终端 UI 中的颜色标识，便于区分不同 Agent 的输出：

```typescript
// src/tools/AgentTool/agentColorManager.ts
export type AgentColorName =
  | 'red' | 'blue' | 'green' | 'yellow'
  | 'purple' | 'orange' | 'pink' | 'cyan'

export function setAgentColor(
  agentType: string,
  color: AgentColorName | undefined,
): void {
  const agentColorMap = getAgentColorMap()
  if (color && AGENT_COLORS.includes(color)) {
    agentColorMap.set(agentType, color)
  }
}
```

颜色在 `getAgentDefinitionsWithOverrides()` 加载时统一分配，存储于全局 `agentColorMap`，供 UI 层渲染时查询。

Sources: [agentColorManager.ts](#root/PoGVrZrabfNZ)

## 性能与最佳实践

**缓存机制**：`getAgentDefinitionsWithOverrides()` 使用 lodash `memoize` 缓存结果，在同一工作目录下重复调用不会触发文件系统扫描。缓存可通过 `clearAgentDefinitionsCache()` 清除。

**并发加载**：Plugin Agent 加载与 Memory Snapshot 初始化并行执行：

```typescript
// src/tools/AgentTool/loadAgentsDir.ts:305-325
if (feature('AGENT_MEMORY_SNAPSHOT') && isAutoMemoryEnabled()) {
  const [pluginAgents_] = await Promise.all([
    pluginAgentsPromise,
    initializeAgentMemorySnapshots(customAgents),
  ])
  pluginAgentsPromise = Promise.resolve(pluginAgents_)
}
```

**按需派生子 Agent**：使用 `AgentTool` 时，优先选择一次性 Agent（Explore、Plan）而非通用 Agent，减少不必要的上下文开销。定义专用 Agent 时，使用 `disallowedTools` 而非 `tools` 白名单可以减少维护负担（新增工具自动可用）。

---

## 下一步

*   深入了解 [Skills 技能开发](22-skills-ji-neng-kai-fa.md)：如何为 Agent 扩展可复用技能
*   探索 [Hooks 机制](23-hooks-ji-zhi.md)：深度定制 Agent 行为
*   查看 [Agent 协调模式](19-agent-xie-diao-mo-shi.md)：多 Agent 协作的高级编排

## 相关条目
- [[20-memory-ji-yi-xi-tong]]
- [[22-skills-ji-neng-kai-fa]]
