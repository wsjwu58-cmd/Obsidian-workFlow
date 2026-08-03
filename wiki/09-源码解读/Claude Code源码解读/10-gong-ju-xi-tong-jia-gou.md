# 10-gong-ju-xi-tong-jia-gou
## 概述

Claude Code 的工具系统是支撑 Agentic Loop 运转的核心基础设施，负责定义、执行和管理 AI 模型可调用的各类工具。该系统采用分层架构设计，从底层的类型定义到上层的工具编排，形成了一套完整、可扩展的工具生命周期管理体系。

## 核心类型系统

工具系统的类型定义集中在 `src/Tool.ts` 中，定义了工具的完整接口规范。这个文件是整个工具系统的契约层，确保所有工具实现遵循统一的规范。

### 工具接口定义

工具通过 TypeScript 泛型接口 `Tool<Input, Output, P>` 进行定义，其中 Input 表示输入参数类型（Zod Schema），Output 表示执行结果类型，P 表示进度数据类型。核心方法包括：

```typescript
export type Tool<
  Input extends AnyObject = AnyObject,
  Output = unknown,
  P extends ToolProgressData = ToolProgressData,
> = {
  readonly name: string
  readonly inputSchema: Input
  call(
    args: z.infer<Input>,
    context: ToolUseContext,
    canUseTool: CanUseToolFn,
    parentMessage: AssistantMessage,
    onProgress?: ToolCallProgress<P>,
  ): Promise<ToolResult<Output>>
  description(
    input: z.infer<Input>,
    options: ToolPermissionContext
  ): Promise<string>
  // ... 更多属性和方法
}
```

Sources: [src/Tool.ts](#root/u2u9NOITcx76)

### 工具工厂函数

`buildTool` 是创建工具实例的标准工厂函数，它接受一个工具定义对象并填充默认值。这种设计确保了所有工具都具有一致的基础行为，同时允许按需覆盖。

```typescript
export function buildTool<D extends AnyToolDef>(def: D): BuiltTool<D> {
  return {
    ...TOOL_DEFAULTS,
    userFacingName: () => def.name,
    ...def,
  } as BuiltTool<D>
}
```

默认行为包括：`isEnabled` 返回 true、`isConcurrencySafe` 返回 false（保守假设）、`isReadOnly` 返回 false、`checkPermissions` 默认允许执行。

Sources: [src/Tool.ts](#root/fP8PPM7Utl29)

## 工具注册与过滤机制

### 工具注册中心

`src/tools.ts` 实现了工具的集中注册管理。`getAllBaseTools` 函数返回所有内置工具的完整列表，采用条件导入模式支持功能开关控制的工具。

```typescript
export function getAllBaseTools(): Tools {
  return [
    AgentTool,
    TaskOutputTool,
    BashTool,
    ...(hasEmbeddedSearchTools() ? [] : [GlobTool, GrepTool]),
    ExitPlanModeV2Tool,
    // ... 更多工具
  ]
}
```

Sources: [src/tools.ts](#root/8f6zQ3tJewkM)

### 工具池组装

`assembleToolPool` 函数是工具池组装的唯一入口，负责合并内置工具和 MCP 工具，并处理去重逻辑。内置工具始终优先于同名 MCP 工具。

```typescript
export function assembleToolPool(
  permissionContext: ToolPermissionContext,
  mcpTools: Tools,
): Tools {
  const builtInTools = getTools(permissionContext)
  const allowedMcpTools = filterToolsByDenyRules(mcpTools, permissionContext)
  return uniqBy(
    [...builtInTools].sort(byName).concat(allowedMcpTools.sort(byName)),
    'name',
  )
}
```

Sources: [src/tools.ts](#root/WjsnSZyQhGr6)

### 权限过滤

`filterToolsByDenyRules` 函数根据权限规则过滤工具，支持服务器级别的批量过滤（如 `mcp__server` 前缀规则）和单个工具的精确过滤。

Sources: [src/tools.ts](#root/xxAv40CJByiB)

## 工具分类体系

### 工具可用性矩阵

`src/constants/tools.ts` 定义了不同执行上下文中允许使用的工具集合：

| 集合名称 | 用途 | 示例工具 |
| --- | --- | --- |
| `ALL_AGENT_DISALLOWED_TOOLS` | 主会话禁止使用的工具 | AgentTool, TaskOutputTool, ExitPlanModeTool |
| `ASYNC_AGENT_ALLOWED_TOOLS` | 异步 Agent 允许的工具 | FileReadTool, WebSearchTool, GrepTool |
| `COORDINATOR_MODE_ALLOWED_TOOLS` | 协调者模式工具 | AgentTool, TaskStopTool, SendMessageTool |
| `IN_PROCESS_TEAMMATE_ALLOWED_TOOLS` | 进程内队友专用 | TaskCreateTool, TaskListTool, CRON\_\* |

Sources: [src/constants/tools.ts](#root/8IiZjU6C82jr)

### 工具能力属性

每个工具通过实现特定方法声明其能力：

*   `isConcurrencySafe(input)` — 标识工具是否可与其他工具并行执行
*   `isReadOnly(input)` — 标识工具是否只读取数据
*   `isDestructive(input)` — 标识工具是否执行不可逆操作
*   `isSearchOrReadCommand(input)` — 标识 Bash 命令是否为搜索/读取操作（用于折叠显示）

Sources: [src/Tool.ts](#root/PlvtfP77mKX5)

## 工具执行架构

### 编排层

`src/services/tools/toolOrchestration.ts` 实现了工具执行的编排逻辑，采用智能分区策略优化执行效率。

```
flowchart TD
    A[ToolUseBlock 列表] --> B[partitionToolCalls]
    B --> C{是否为并发安全?}
    C -->|是| D[合并到当前批次]
    C -->|否| E[创建新批次]
    D --> F[runToolsConcurrently]
    E --> G[runToolsSerially]
    F --> H[结果收集]
    G --> H
    H --> I[上下文更新]
```

分区算法将工具调用分为两类批次：单个非并发安全工具，或多个连续的并发安全工具。这种设计确保了数据修改操作的串行执行，同时允许读取操作并行处理。

Sources: [src/services/tools/toolOrchestration.ts](#root/GEVONKac9KlW)

### 流式执行器

`StreamingToolExecutor` 类处理流式场景下的工具执行，支持工具边接收边启动执行的模式。它维护每个工具的执行状态（queued/executing/completed/yielded），并根据并发安全约束动态调度。

Sources: [src/services/tools/StreamingToolExecutor.ts](#root/jbI7dZeayKGE)

### 单个工具执行

`runToolUse` 函数是工具执行的原子单位，负责：

1.  验证输入参数
2.  检查执行权限
3.  执行 PreToolUse Hooks
4.  调用工具的 `call` 方法
5.  处理进度消息
6.  执行 PostToolUse Hooks
7.  存储结果

Sources: [src/services/tools/toolExecution.ts](#root/cb8XdKjXsnT9)

## 权限与安全系统

### 权限检查流程

`useCanUseTool` Hook 实现了权限检查的核心逻辑，其决策流程如下：

```
sequenceDiagram
    participant Model
    participant PermissionSystem
    participant Hooks
    participant UI
    
    Model->>PermissionSystem: 工具调用请求
    PermissionSystem->>PermissionSystem: hasPermissionsToUseTool()
    alt 自动允许
        PermissionSystem->>Model: allow
    else 自动拒绝
        PermissionSystem->>Model: deny
    else 需要确认
        alt Coordinator 模式
            PermissionSystem->>Hooks: handleCoordinatorPermission
        end
        alt Swarm Worker
            PermissionSystem->>Hooks: handleSwarmWorkerPermission
        end
        alt 自动分类器批准
            PermissionSystem->>Hooks: 检查 BashClassifier
        end
        PermissionSystem->>UI: 显示权限对话框
        UI->>Model: 用户决策
    end
```

Sources: [src/hooks/useCanUseTool.tsx](#root/Yi1lXRi4eZj0)

### 权限规则引擎

权限规则支持多种匹配模式：

*   **精确匹配**: `Bash(npm test)`
*   **通配符匹配**: `Bash(npm *)`
*   **服务器级别**: `mcp__github *` (拒绝整个 MCP 服务器的工具)
*   **命令语义分析**: 检测 git commit、rm -rf 等高风险操作

Sources: [src/utils/permissions/permissions.ts](#root/jeGNp4EDifwc) Sources: [src/utils/permissions/permissionRuleParser.ts](#root/ETvJXuCSlLvB)

## 工具目录结构

```
src/tools/
├── AgentTool/          # Agent 创建与管理
├── BashTool/           # Shell 命令执行
├── FileEditTool/       # 文件编辑
├── FileReadTool/       # 文件读取
├── FileWriteTool/      # 文件写入
├── GlobTool/           # 模式匹配文件查找
├── GrepTool/           # 内容搜索
├── MCPTool/            # MCP 协议工具
├── TaskStopTool/       # 任务停止
├── WebSearchTool/      # 网络搜索
├── WebFetchTool/       # HTTP 请求
├── WorkflowTool/       # 工作流脚本
├── SkillTool/          # 技能调用
├── LSPTool/            # 语言服务器协议
├── REPLTool/           # 交互式 REPL
└── shared/             # 共享工具函数
```

每个工具目录遵循统一结构：

*   `*.tsx` 或 `*.ts` — 工具主实现
*   `UI.tsx` — 用户界面组件
*   `prompt.ts` — 工具提示词定义
*   `constants.ts` — 常量定义
*   `__tests__/` — 单元测试

Sources: [src/tools](#root/6tkcsdlevMc0)

## 进度报告机制

工具通过 `ToolCallProgress<P>` 回调机制报告执行进度，进度数据被封装在 `ProgressMessage` 中传输。UI 层根据 `renderToolUseProgressMessage` 方法渲染进度展示。

常见的进度类型包括：

*   `BashProgress` — Shell 命令执行进度
*   `TaskOutputProgress` — 长时间任务输出
*   `MCPProgress` — MCP 工具调用进度
*   `SkillToolProgress` — 技能执行进度

Sources: [src/types/tools.ts](#root/3jTl2pvvqugm)

## 上下文传递

`ToolUseContext` 是工具执行上下文的载体，包含：

```typescript
export type ToolUseContext = {
  options: {
    commands: Command[]           // 可用命令列表
    tools: Tools                   // 可用工具列表
    mcpClients: MCPServerConnection[]  // MCP 客户端
    maxBudgetUsd?: number          // 预算限制
  }
  abortController: AbortController
  readFileState: FileStateCache    // 文件状态缓存
  getAppState(): AppState
  setAppState: (f: (prev: AppState) => AppState) => void
  // ... 更多上下文属性
}
```

Sources: [src/Tool.ts](#root/aGGq3x33NqZc)

## 总结

工具系统采用模块化、可扩展的架构设计，通过清晰的类型契约、集中的注册管理、智能的执行编排和完善的权限控制，为 Claude Code 提供了强大而安全的工具执行能力。这种设计使得添加新工具变得简单，同时确保了系统的整体一致性和可靠性。

## 相关文档

*   [内置工具详解](11-nei-zhi-gong-ju-xiang-jie.md) — 深入了解各类内置工具的实现细节
*   [MCP 协议集成](12-mcp-xie-yi-ji-cheng.md) — 外部工具协议的支持机制
*   [权限模型与规则引擎](15-quan-xian-mo-xing-yu-gui-ze-yin-qing.md) — 安全模型的完整说明
*   [Agentic Loop 核心循环](7-agentic-loop-he-xin-xun-huan.md) — 工具如何融入整体循环

## 相关条目
- [[6-wu-ceng-jia-gou-she-ji]]
- [[11-nei-zhi-gong-ju-xiang-jie]]
