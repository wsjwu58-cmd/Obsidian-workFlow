# 6-wu-ceng-jia-gou-she-ji
Claude Code 采用分层架构设计，从上到下划分为五个层次，每层职责清晰、边界分明。这种架构确保了系统的可维护性、可扩展性和可测试性，同时为高级用户提供了深度定制的可能性。

## 架构总览

```
graph TB
    subgraph 交互层["🔤 交互层 (Interaction Layer)"]
        REPL["REPL.tsx<br/>终端UI组件"]
        Input["用户输入处理<br/>PromptInput"]
        Messages["消息展示<br/>Messages/MessageRow"]
    end
    
    subgraph 编排层["🎯 编排层 (Orchestration Layer)"]
        QE["QueryEngine.ts<br/>会话编排器"]
        State["状态管理<br/>AppState/Store"]
        Transcript["持久化<br/>Transcript"]
    end
    
    subgraph 核心循环层["🔄 核心循环层 (Core Loop Layer)"]
        Query["query.ts<br/>Agentic Loop"]
        Compact["上下文压缩<br/>compact.ts"]
        AutoCompact["自动压缩<br/>autoCompact.ts"]
    end
    
    subgraph 工具层["🔧 工具层 (Tool Layer)"]
        Tools["tools.ts<br/>工具注册表"]
        ToolDef["Tool.ts<br/>工具接口定义"]
        MCP["MCP集成<br/>mcp/"]
    end
    
    subgraph 通信层["🌐 通信层 (Communication Layer)"]
        API["claude.ts<br/>API客户端"]
        Stream["流式处理<br/>Streaming"]
        Providers["多Provider<br/>Anthropic/AWS/Vertex"]
    end
    
    REPL --> QE
    QE --> Query
    Query --> Tools
    Tools --> API
    
    State -.-> QE
    Transcript -.-> QE
    Compact -.-> Query
    AutoCompact -.-> Query
```

| 层次 | 职责范围 | 核心源码 | 关键技术 |
| --- | --- | --- | --- |
| **交互层** | 终端UI、用户输入、消息渲染 | `src/screens/REPL.tsx` | React/Ink |
| **编排层** | 多轮会话管理、状态持久化、成本追踪 | `src/QueryEngine.ts` | AsyncGenerator |
| **核心循环层** | 单轮执行循环、上下文压缩、工具调度 | `src/query.ts` | 状态机 |
| **工具层** | AI能力扩展、文件/Shell操作、MCP集成 | `src/tools.ts` → `src/Tool.ts` | 插件化架构 |
| **通信层** | API通信、流式处理、多Provider支持 | `src/services/api/claude.ts` | SSE流 |

Sources: [src/QueryEngine.ts](#root/MAP5Oq9uKyQz), [src/query.ts](#root/XpiH0TLKKrgi), [src/Tool.ts](#root/I8piHBSE2KIE)

---

## 第一层：交互层 (Interaction Layer)

交互层是用户与 Claude Code 交互的前端界面，基于 React 和 Ink（自定义终端渲染框架）构建。这一层负责接收用户输入、渲染 AI 响应、处理键盘快捷键和权限对话框等 UI 交互。

### 核心组件

```
graph LR
    subgraph 交互层组件
        REPL["REPL.tsx<br/>根组件"]
        Messages["Messages.tsx<br/>消息列表"]
        PromptInput["PromptInput/<br/>输入处理"]
        Permissions["permissions/<br/>权限对话框"]
    end
    
    User[用户输入] --> REPL
    REPL --> Messages
    REPL --> PromptInput
    PromptInput --> QueryEngine
    Messages --> User
```

**REPL 组件**（`src/screens/REPL.tsx`）是整个 CLI 的主入口，负责：

*   管理消息历史和渲染
*   处理用户输入（支持斜杠命令、文件附件、图片）
*   协调权限请求和工具执行反馈
*   支持 Vim 模式、搜索、历史记录等高级编辑功能

```typescript
// REPL.tsx 中的关键状态管理
const [messages, setMessages] = useState<Message[]>([])
const [isQuerying, setIsQuerying] = useState(false)
const toolExecutor = useRef<StreamingToolExecutor | null>(null)
```

Sources: [src/screens/REPL.tsx](#root/s16UN6CL8iDC), [src/components/Messages.tsx](#root/BrsBcCJvEgPm)

### 输入处理管道

用户输入经过 `processUserInput()` 函数处理，支持多种输入模式：

```
sequenceDiagram
    participant User as 用户输入
    participant Input as PromptInput
    participant Process as processUserInput()
    participant Query as QueryEngine
    
    User->>Input: 输入文本/命令
    Input->>Process: 解析输入
    Process->>Process: 识别斜杠命令
    Process->>Process: 处理文件附件
    Process->>Process: 识别@提及
    Process->>Query: submitMessage()
```

| 输入类型 | 处理方式 | 源码位置 |
| --- | --- | --- |
| 普通文本 | 直接作为用户消息 | `src/utils/processUserInput/` |
| 斜杠命令 | `/model`, `/compact`, `/plan` 等 | `src/commands.ts` |
| 文件附件 | 生成 AttachmentMessage | `src/utils/attachments.ts` |
| 图片输入 | 验证尺寸、压缩、Base64编码 | `src/utils/imageValidation.ts` |

Sources: [src/utils/processUserInput/processUserInput.ts](#root/Gh4nPfTUDbcg), [src/history.ts](#root/3mQ9egtyVeGu)

---

## 第二层：编排层 (Orchestration Layer)

编排层由 `QueryEngine` 类主导，它是 REPL 与核心循环之间的中间层，负责管理多轮对话的完整生命周期。

### QueryEngine 的核心职责

```
classDiagram
    class QueryEngine {
        +mutableMessages: Message[]
        +totalUsage: NonNullableUsage
        +readFileState: FileStateCache
        +submitMessage(): AsyncGenerator
        +queryEngine.query(): AsyncGenerator
        +accumulateUsage()
        +recordTranscript()
        +fileHistoryMakeSnapshot()
    }
    
    class AppState {
        +messages: Message[]
        +mcpClients: MCPServerConnection[]
        +toolPermissionContext: ToolPermissionContext
    }
    
    QueryEngine --> AppState
```

**会话状态管理**：`QueryEngine` 维护以下跨轮次状态：

| 状态字段 | 类型 | 说明 |
| --- | --- | --- |
| `mutableMessages` | `Message[]` | 对话历史，支持原地修改 |
| `totalUsage` | `NonNullableUsage` | 累计 token 用量 |
| `readFileState` | `FileStateCache` | 文件读取缓存 |
| `permissionDenials` | `SDKPermissionDenial[]` | 权限拒绝记录 |

```typescript
// QueryEngine 构造函数
export class QueryEngine {
  private mutableMessages: Message[]
  private abortController: AbortController
  private permissionDenials: SDKPermissionDenial[]
  private totalUsage: NonNullableUsage
  private readFileState: FileStateCache
  
  constructor(config: QueryEngineConfig) {
    this.mutableMessages = config.initialMessages ?? []
    this.abortController = config.abortController ?? createAbortController()
  }
}
```

Sources: [src/QueryEngine.ts](#root/0RJCb7YBZT4D)

### 成本追踪与持久化

QueryEngine 集成了成本追踪和会话持久化功能：

```typescript
// 成本累积
import { accumulateUsage, updateUsage } from 'src/services/api/claude.js'
this.totalUsage = accumulateUsage(this.totalUsage, usage)

// Transcript 持久化
import { recordTranscript } from 'src/utils/sessionStorage.js'
await recordTranscript(sessionId, messages, {
  compactBoundaries: this.compactBoundaries,
  attribution: attributionState,
})
```

Sources: [src/QueryEngine.ts](#root/4OVUWlHgBoYA), [src/cost-tracker.ts](#root/XzCeKbHa0hDX)

---

## 第三层：核心循环层 (Core Loop Layer)

核心循环层是 Claude Code 的"大脑"，由 `query.ts` 中的 `query()` 异步生成器实现。这层处理单轮对话的完整执行流程。

### Agentic Loop 状态机

```
stateDiagram-v2
    [*] --> 上下文预处理
    上下文预处理 --> API调用
    API调用 --> 流式接收
    流式接收 --> 工具检测
    工具检测 --> 工具执行: 发现 tool_use
    工具检测 --> 终止: 无工具调用
    工具执行 --> API调用: 继续循环
    工具执行 --> 终止: 达到最大轮次
    终止 --> [*]
```

### 循环迭代的完整流程

`query()` 函数的 `while(true)` 循环每轮迭代执行以下步骤：

```
sequenceDiagram
    participant QE as QueryEngine
    participant Query as query.ts
    participant API as API客户端
    participant Tools as 工具层
    participant Compact as 压缩模块
    
    Note over Query: ① 上下文预处理管道
    Query->>Compact: applyToolResultBudget()
    Query->>Compact: microcompact()
    Query->>Compact: contextCollapse()
    Query->>Compact: autocompact()
    
    Note over Query: ② 流式API调用
    Query->>API: callModel()
    API-->>Query: StreamEvent | Message
    
    Note over Query: ③ 工具执行
    loop 每个 tool_use 块
        Query->>Tools: StreamingToolExecutor
        Tools-->>Query: toolResults[]
    end
    
    Note over Query: ④ 终止判定
    Query->>Query: needsFollowUp ? continue : return
```

**关键状态类型**（`src/query.ts:204`）：

```typescript
type State = {
  messages: Message[]                    // 消息历史
  toolUseContext: ToolUseContext          // 工具执行上下文
  autoCompactTracking: AutoCompactTrackingState | undefined
  maxOutputTokensRecoveryCount: number    // 输出截断恢复计数
  hasAttemptedReactiveCompact: boolean    // 是否尝试过响应式压缩
  maxOutputTokensOverride: number | undefined
  pendingToolUseSummary: Promise | undefined
  stopHookActive: boolean | undefined
  turnCount: number                       // 当前轮次
  transition: Continue | undefined        // 上一轮继续原因
}
```

Sources: [src/query.ts](#root/DfccpBESLUN2), [src/query.ts](#root/7aYeAmALXBiy)

### 上下文压缩机制

Claude Code 实现了多层次的上下文压缩，确保长对话不会超出 token 限制：

| 压缩类型 | 触发条件 | 源码 |
| --- | --- | --- |
| **Snip** | HISTORY\_SNIP feature | `src/services/compact/snipCompact.ts` |
| **Microcompact** | 每次 API 调用前 | `src/services/compact/microCompact.ts` |
| **Auto-compact** | 超过 token 阈值 | `src/services/compact/autoCompact.ts` |
| **Context Collapse** | CONTEXT\_COLLAPSE feature | `src/services/contextCollapse/` |

```typescript
// 压缩执行示例
queryCheckpoint('query_autocompact_start')
const { compactionResult, consecutiveFailures } = await deps.autocompact(
  messagesForQuery,
  toolUseContext,
  { systemPrompt, userContext, systemContext, toolUseContext },
  querySource,
  tracking,
  snipTokensFreed,
)
queryCheckpoint('query_autocompact_end')
```

Sources: [src/services/compact/compact.ts](#root/LcAbeIEBqQU3), [src/services/compact/autoCompact.ts](#root/7LyXTeBr7hnM)

---

## 第四层：工具层 (Tool Layer)

工具层是 Claude Code 的"双手"，通过可扩展的工具系统赋予 AI 执行各种操作的能力。

### 工具架构

```
classDiagram
    class Tool~Input, Output, Progress~ {
        <<interface>>
        +name: string
        +description: string
        +inputSchema: z.ZodType
        +isEnabled(): boolean
        +isConcurrencySafe(input): boolean
        +call(input, context): Promise~ToolResult~
    }
    
    class BashTool {
        +call(): 执行Shell命令
        +isConcurrencySafe(): false
    }
    
    class FileEditTool {
        +call(): 编辑文件
        +isConcurrencySafe(): true
    }
    
    class MCPTool {
        +call(): 调用MCP工具
        +isConcurrencySafe(): 根据MCP定义
    }
    
    Tool <|-- BashTool
    Tool <|-- FileEditTool
    Tool <|-- MCPTool
```

### 工具注册表

`src/tools.ts` 中的 `getAllBaseTools()` 函数组装完整的工具列表：

```typescript
export function getAllBaseTools(): Tools {
  return [
    AgentTool,           // Agent 创建
    TaskOutputTool,       // 任务输出
    BashTool,            // Shell 执行
    GlobTool,            // 文件搜索
    GrepTool,            // 内容搜索
    ExitPlanModeV2Tool,  // 退出 Plan 模式
    FileEditTool,        // 文件编辑
    FileReadTool,        // 文件读取
    FileWriteTool,       // 文件写入
    NotebookEditTool,    // Jupyter 笔记本
    WebFetchTool,        // 网页获取
    WebSearchTool,       // 网页搜索
    TodoWriteTool,        // 任务管理
    // ... 更多工具
  ]
}
```

Sources: [src/tools.ts](#root/jKAUGKEKPUpD), [src/Tool.ts](#root/I8piHBSE2KIE)

### 工具执行器

`StreamingToolExecutor` 支持流式工具执行和并发控制：

```
graph LR
    subgraph 工具执行
        TE["StreamingToolExecutor"]
        Q["队列"]
        E1["并发安全工具1"]
        E2["并发安全工具2"]
        X["独占工具"]
    end
    
    Stream["API流"] --> TE
    TE --> Q
    Q --> E1
    Q --> E2
    Q --> X
    
    style X fill:#ffcccc
    style E1 fill:#ccffcc
    style E2 fill:#ccffcc
```

**并发控制规则**：

*   **并发安全工具**：可以并行执行（`isConcurrencySafe() === true`）
*   **独占工具**：必须单独执行（`isConcurrencySafe() === false`，如 BashTool）
*   **工具错误**：当一个工具出错时，其"兄弟"工具也会被取消

```typescript
private canExecuteTool(isConcurrencySafe: boolean): boolean {
  const executingTools = this.tools.filter(t => t.status === 'executing')
  return (
    executingTools.length === 0 ||
    (isConcurrencySafe && executingTools.every(t => t.isConcurrencySafe))
  )
}
```

Sources: [src/services/tools/StreamingToolExecutor.ts](#root/N9HQm7ZnyWyO)

### MCP 集成

MCP（Model Context Protocol）工具通过 `MCPTool` 集成到系统中：

```typescript
import { isToolFromMcpServer } from 'src/services/mcp/utils.js'

// 工具来源标记
interface MCPToolInfo {
  serverName: string
  serverType: 'stdio' | 'sse' | 'http'
  mcpInfo: true
}
```

Sources: [src/tools/MCPTool/](#root/pmcUYxHgjraq), [src/services/mcp/](#root/kZwPZV03XaDe)

---

## 第五层：通信层 (Communication Layer)

通信层负责与 Claude API 的所有网络通信，支持多种 Provider 和高级特性。

### 多 Provider 支持

```
graph TB
    subgraph 通信层
        API["claude.ts<br/>API客户端"]
        Providers["Provider路由"]
        Anthropic["Anthropic Direct"]
        AWS["AWS Bedrock"]
        Vertex["Google Vertex"]
        Azure["Azure"]
        OpenAI["OpenAI兼容"]
    end
    
    API --> Providers
    Providers --> Anthropic
    Providers --> AWS
    Providers --> Vertex
    Providers --> Azure
    Providers --> OpenAI
```

| Provider | 环境变量 | 认证方式 |
| --- | --- | --- |
| **Anthropic Direct** | `ANTHROPIC_API_KEY` | API Key |
| **AWS Bedrock** | `ANTHROPIC_BEDROCK_BASE_URL` | AWS 凭证 |
| **Google Vertex** | `ANTHROPIC_VERTEX_PROJECT_ID` | GCP 认证 |
| **Azure** | 自定义 base URL | Azure AD |
| **OpenAI 兼容** | `CLAUDE_CODE_USE_OPENAI=1` | API Key |

Sources: [src/services/api/claude.ts](#root/JpS5XSq20L7b), [src/utils/model/providers.ts](#root/4sG3291HSS3O)

### 流式通信机制

Claude Code 采用完全的流式架构，API 响应以 SSE 事件流返回：

```
sequenceDiagram
    participant Client as claude.ts
    participant SDK as Anthropic SDK
    participant Server as Claude API
    
    Client->>SDK: messages.create streaming
    SDK->>Server: POST /v1/messages
    loop SSE Stream
        Server-->>SDK: content_block_start
        Server-->>SDK: content_block_delta
        Server-->>SDK: content_block_stop
        Server-->>SDK: message_delta
        Server-->>SDK: message_stop
    end
    SDK-->>Client: BetaRawMessageStreamEvent[]
```

**支持的高级 API 特性**：

| 特性 | Beta Header | 说明 |
| --- | --- | --- |
| Prompt Caching | `prompt-caching-2024-07-31` | 缓存系统提示 |
| Thinking Blocks | `native-tool-errors` | 扩展思考能力 |
| Extended Thinking | 启用 max\_thinking\_length | 模型思考 token |
| Tool Results Budget | task\_budgets-2026-03-13 | 控制工具输出 |

Sources: [src/services/api/claude.ts](#root/R9IGFMRWnDqa)

### 请求构建

```typescript
// 构建 API 请求参数
const params: BetaMessageStreamParams = {
  model: currentModel,
  max_tokens: maxTokens,
  system: systemPromptParts,
  messages: normalizedMessages,
  tools: toolSchemas,
  betas: getMergedBetas(),
  // 高级特性
  thinking: thinkingConfig,
  stream: true,
}
```

Sources: [src/services/api/claude.ts](#root/dvRjllatl4Bt), [src/constants/betas.ts](#root/iNyHnfSF9wkK)

---

## 层间数据流

### 完整请求路径

```
sequenceDiagram
    participant User as 用户
    participant REPL as REPL.tsx
    participant QE as QueryEngine
    participant Query as query.ts
    participant Tools as 工具层
    participant API as claude.ts
    
    User->>REPL: "修复这个bug"
    REPL->>QE: submitMessage(input)
    QE->>Query: query(params)
    
    Note over Query: 上下文预处理
    Query->>Query: microcompact()
    Query->>Query: autocompact()
    
    Query->>API: callModel()
    API-->>Query: StreamEvent[]
    
    loop tool_use 检测
        Query->>Tools: StreamingToolExecutor
        Tools-->>Query: toolResults
        Query->>API: 继续流式接收
    end
    
    Query-->>QE: Message[]
    QE-->>REPL: 渲染响应
    REPL-->>User: 显示结果
```

### 权限检查管道

每次工具调用都经过严格的权限验证：

```
flowchart LR
    subgraph 权限检查
        V["validateInput()"]
        P["checkPermissions()"]
        C["canUseTool()"]
    end
    
    ToolCall["工具调用"] --> V
    V --> C
    C --> P
    
    P -->|"允许"| Execute["执行工具"]
    P -->|"拒绝"| Deny["返回拒绝错误"]
    
    subgraph 规则来源
        S1["Session"]
        S2["Project"]
        S3["User"]
        S4["Managed"]
        S5["Default"]
    end
```

Sources: [src/Tool.ts](#root/i2Fju1jsIJx1), [src/hooks/useCanUseTool.ts](#root/ZYXSKzfSqMmg)

---

## 架构设计原则

### 四大核心原则

| 原则 | 实现方式 | 源码位置 |
| --- | --- | --- |
| **流式优先 (Streaming-first)** | 所有 API 通信流式化，工具并行执行 | `src/services/tools/StreamingToolExecutor.ts` |
| **工具即能力 (Tool as Capability)** | `Tool<Input, Output, Progress>` 结构化类型 | `src/Tool.ts` |
| **权限即边界 (Permission as Boundary)** | 五层权限规则汇聚 | `src/types/permissions.ts` |
| **上下文即记忆 (Context as Memory)** | 多层压缩 + 自动摘要 | `src/services/compact/` |

### Feature Flag 机制

Claude Code 使用 feature flag 控制功能启用，实现代码的动态配置：

```typescript
import { feature } from 'bun:bundle'

// 条件加载模块
const coordinatorModeModule = feature('COORDINATOR_MODE')
  ? require('./coordinator/coordinatorMode.js')
  : null

// 条件注册工具
const WebBrowserTool = feature('WEB_BROWSER_TOOL')
  ? require('./tools/WebBrowserTool/WebBrowserTool.js').WebBrowserTool
  : null
```

Sources: [scripts/defines.ts](#root/3YAgWdmlg97c), [src/types/internal-modules.d.ts](#root/Q2O32gyjLkII)

---

## 与其他文档的关联

| 层级 | 相关文档 |
| --- | --- |
| 交互层 | [Agentic Loop 核心循环](7-agentic-loop-he-xin-xun-huan.md) |
| 核心循环层 | [QueryEngine 编排机制](8-queryengine-bian-pai-ji-zhi.md) |
| 工具层 | [工具系统架构](10-gong-ju-xi-tong-jia-gou.md), [MCP 协议集成](12-mcp-xie-yi-ji-cheng.md) |
| 通信层 | [会话状态管理](9-hui-hua-zhuang-tai-guan-li.md) |
| 全部 | [架构全景](#root/21irnynmYRsG) |

---

## 总结

Claude Code 的五层架构体现了以下设计理念：

1.  **清晰的分层边界**：每层只关注自己的职责，通过定义良好的接口进行通信
2.  **流式优先设计**：从 API 通信到工具执行，全程流式化，最大化用户体验
3.  **插件化架构**：工具层支持灵活扩展，MCP 协议进一步扩展生态
4.  **上下文管理**：多层次压缩机制确保长对话可持续运行
5.  **安全第一**：权限模型贯穿整个执行流程，工具调用必须经过验证

这种架构使 Claude Code 能够同时支持轻量级交互和复杂的自动化任务，同时保持代码的可维护性和可扩展性。

## 相关条目
- [[1-xiang-mu-gai-lan]]
- [[7-agentic-loop-he-xin-xun-huan]]
- [[10-gong-ju-xi-tong-jia-gou]]
