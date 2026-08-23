# 12-mcp-xie-yi-ji-cheng
MCP（Model Context Protocol）协议集成是 Claude Code 连接外部工具和数据源的核心机制。通过 MCP，Claude Code 可以将任意 MCP 服务器暴露的工具、资源和提示词作为原生工具使用，实现与文件系统、数据库、API 等外部系统的深度集成。

## 架构总览

MCP 集成采用分层架构设计，从配置层到工具执行层形成完整的数据流链路。

```
flowchart TB
    subgraph Config["配置层"]
        settings["settings.json<br/>mcpServers 配置"]
        mcpJson[".mcp.json<br/>项目级配置"]
        managed["managed-mcp.json<br/>企业托管配置"]
    end

    subgraph Service["服务层"]
        config["config.ts<br/>多级配置合并"]
        client["client.ts<br/>MCP 客户端核心"]
        auth["auth.ts<br/>OAuth 认证"]
    end

    subgraph Connection["连接管理层"]
        hook["useManageMCPConnections.ts<br/>生命周期管理"]
        manager["MCPConnectionManager.tsx<br/>React Context"]
    end

    subgraph Tool["工具层"]
        fetch["fetchToolsForClient<br/>工具发现"]
        mcpTool["MCPTool.ts<br/>工具抽象"]
    end

    Config --> Service
    Service --> Connection
    Connection --> Tool
    settings --> config
    mcpJson --> config
    managed --> config
```

配置层支持三种作用域：用户级（`~/.claude/settings.json`）、项目级（`.mcp.json`）和企业托管（`managed-mcp.json`）。`getAllMcpConfigs()` 函数负责合并这三级配置，其中企业托管配置的优先级最高。

Sources: [config.ts](#root/Td6Z4lLD9sTj) Sources: [client.ts](#root/4ixHw4vBKngR)

## 传输层实现

Claude Code 支持 7 种 MCP 传输类型，每种适用于不同场景：

| 传输类型 | Transport 类 | 适用场景 | 认证方式 | 并发限制 |
| --- | --- | --- | --- | --- |
| `stdio`（默认） | `StdioClientTransport` | 本地子进程 | 无 | 3 |
| `sse` | `SSEClientTransport` | 远程 SSE 服务 | OAuth + ClaudeAuthProvider | 20 |
| `http` | `StreamableHTTPClientTransport` | HTTP 流式 | OAuth + ClaudeAuthProvider | 20 |
| `sse-ide` | `SSEClientTransport` | IDE 集成 | IDE lockfile token | 20 |
| `ws-ide` | `WebSocketTransport` | IDE WebSocket | `X-Claude-Code-Ide-Authorization` | 20 |
| `ws` | `WebSocketTransport` | WebSocket 服务 | Session ingress token | 20 |
| `claudeai-proxy` | `StreamableHTTPClientTransport` | claude.ai 代理 | OAuth bearer | 20 |

### stdio 传输的进程管理

本地 MCP 服务器作为子进程运行，采用信号升级策略进行优雅关闭：

```
sequenceDiagram
    participant CC as Claude Code
    participant MCP as MCP Server Process
    participant Kernel as OS Kernel

    CC->>MCP: SIGINT (100ms)
    MCP-->>Kernel: 优雅退出
    Kernel-->>CC: Process Exited
    Note over CC,MCP: 成功退出 ✓

    rect rgb(255, 240, 230)
    Note over MCP: 如果进程未响应
    CC->>MCP: SIGTERM (400ms)
    MCP-->>Kernel: 强制退出
    Kernel-->>CC: Process Exited

    rect rgb(255, 220, 220)
    Note over MCP: 如果仍未退出
    CC->>MCP: SIGKILL
    end
```

总清理时间上限 600ms，防止 MCP 服务器关闭阻塞 CLI 退出。进程监控通过 `process.kill(pid, 0)` 检查进程是否存在。

Sources: [client.ts](#root/wk0bDHrEi5sa)

### 远程传输的认证状态机

SSE/HTTP 类型使用 `ClaudeAuthProvider` 实现 OAuth 认证流程。认证失败时进入 `needs-auth` 状态，并写入 15 分钟 TTL 的缓存文件（`mcp-needs-auth-cache.json`），避免重复弹出认证提示：

```
stateDiagram-v2
    [*] --> Connecting: connectToServer()
    Connecting --> Connected: 连接成功
    Connecting --> NeedsAuth: 401 Unauthorized
    NeedsAuth --> Connecting: 用户授权完成
    Connected --> Reconnecting: 连接错误 × 3
    Reconnecting --> Connected: 重连成功
    Reconnecting --> Failed: 重连失败
    Failed --> [*]
```

Sources: [auth.ts](#root/cuRVZvSiSGg2) Sources: [client.ts](#root/Cup0jxByvrQ3)

## 工具发现与执行链路

`fetchToolsForClient()` 使用 `memoizeWithLRU` 缓存（上限 20），将 MCP 工具转换为 Claude Code 的统一 Tool 接口：

```typescript
const fullyQualifiedName = buildMcpToolName(client.name, tool.name)
// 结果: "mcp__my-db__query"
```

### 工具能力标注

每个 MCP 工具根据 `tool.annotations` 自动标注能力：

| MCP 注解 | Claude Code 方法 | 含义 |
| --- | --- | --- |
| `readOnlyHint: true` | `isReadOnly()` + `isConcurrencySafe()` | 只读，可并行执行 |
| `destructiveHint: true` | `isDestructive()` | 破坏性操作 |
| `openWorldHint: true` | `isOpenWorld()` | 开放世界，不可枚举 |
| `title` | `userFacingName()` | 显示名称 |

### MCP 工具的执行链路

```
sequenceDiagram
    participant AI as AI Model
    participant MCPTool as MCPTool.call()
    participant Client as MCP Client
    participant Server as MCP Server
    participant Storage as 结果存储

    AI->>MCPTool: tool_use: {name: "mcp__my-db__query"}
    MCPTool->>Client: ensureConnectedClient()
    Client->>Server: client.request({method: 'tools/call'})
    Server-->>Client: 工具执行结果
    Client->>Storage: persistBinaryContent() / truncateMcpContentIfNeeded()
    Storage-->>Client: 处理后的结果
    Client-->>MCPTool: { data: content, mcpMeta }
    MCPTool-->>AI: 工具结果
```

会话过期自动重试机制：HTTP 传输的 MCP session 可能过期，检测到 `McpSessionExpiredError` 后自动重试一次。

Sources: [client.ts](#root/1D2FmdPhvSi7) Sources: [mcpStringUtils.ts](#root/4X1TPx39EQDi)

## 连接缓存与重连机制

`connectToServer` 使用 lodash `memoize` 缓存连接对象，缓存 key 为 `${name}-${JSON.stringify(config)}`：

```typescript
export const connectToServer = memoize(
  async (name: string, serverRef: ScopedMcpServerConfig) => {
    // 创建 Transport
    // new Client() from @modelcontextprotocol/sdk
    // client.connect(transport)
    // 返回 MCPServerConnection
  },
  (name, serverRef) => getServerCacheKey(name, serverRef)
)
```

### 缓存失效触发

当连接关闭时（`client.onclose`），清除所有相关缓存：

```typescript
client.onclose = () => {
  const key = getServerCacheKey(name, serverRef)
  fetchToolsForClient.cache.delete(name)      // 工具缓存
  fetchResourcesForClient.cache.delete(name) // 资源缓存
  fetchCommandsForClient.cache.delete(name)   // 命令缓存
  connectToServer.cache.delete(key)            // 连接缓存
}
```

### 连接降级检测

远程传输有连续错误计数器（`MAX_ERRORS_BEFORE_RECONNECT = 3`），遇到终端错误（ECONNRESET、ETIMEDOUT、EPIPE 等）连续 3 次后主动关闭 transport 触发重连。

Sources: [client.ts](#root/FoaklSbG9Zww)

## MCP Skills 功能

当启用 `FEATURE_MCP_SKILLS=1` 时，MCP 服务器暴露的 `skill://` URI 资源会被发现并转换为可调用的技能命令：

```
flowchart LR
    subgraph MCP["MCP Server"]
        resources["resources<br/>skill:// URIs"]
    end

    subgraph CC["Claude Code"]
        fetcher["fetchMcpSkillsForClient"]
        skillCmd["mcpSkills → Command[]"]
    end

    resources --> fetcher
    fetcher --> skillCmd
    skillCmd --> SkillTool["SkillTool 调用"]
```

技能获取函数维护 `.cache`（Map），在连接关闭、配置变化或收到 `prompts/list_changed`/`resources/list_changed` 通知时清除缓存。

Sources: [docs/features/mcp-skills.md](#root/XgFUA9p0GPjC)

## 配置与策略管理

### 多级配置合并

```
flowchart TB
    subgraph Priority["优先级（高→低）"]
        managed["managed-mcp.json<br/>企业托管"]
        user["settings.json<br/>用户级"]
        project[".mcp.json<br/>项目级"]
    end

    subgraph Filter["策略过滤"]
        policy["allowlist / denylist"]
        dedup["重复服务器去重"]
    end

    managed --> Filter
    user --> Filter
    project --> Filter
    Filter --> merged["合并后配置"]
```

策略管理支持基于服务器名称、命令数组（stdio 服务器）或 URL 模式（远程服务器）的白名单/黑名单控制。

### 服务器审批对话框

首次发现 `.mcp.json` 中的新服务器时，弹出 `MCPServerApprovalDialog` 供用户选择：

```typescript
const choices = [
  { label: "使用此项目中的所有 MCP 服务器", value: "yes_all" },
  { label: "仅使用此 MCP 服务器", value: "yes" },
  { label: "不使用此 MCP 服务器", value: "no" },
]
```

Sources: [config.ts](#root/lZlemFGFRR9z) Sources: [components/MCPServerApprovalDialog.tsx](#root/4UvavxFNS84U)

## Elicitation 用户交互

MCP 服务器可以通过 `ElicitRequestSchema` 请求用户交互（如确认对话框、URL 打开等）：

```
sequenceDiagram
    participant Server as MCP Server
    participant CC as Claude Code
    participant User as 用户

    Server->>CC: elicitation request (URL 模式)
    CC->>User: 显示 URL + "打开浏览器" 按钮
    CC->>CC: 轮询等待状态
    User->>Server: 在浏览器中完成操作
    Server-->>CC: ElicitationComplete notification
    CC-->>Server: 返回用户响应
```

Elicitation 支持两种模式：`form`（表单确认）和 `url`（URL 打开确认）。

Sources: [elicitationHandler.ts](#root/FjfTaJp4RGK1)

## 实际配置示例

```
// settings.json 或 .mcp.json
{
  "mcpServers": {
    // 本地 stdio 服务器
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/projects"]
    },
    // 远程 HTTP 服务器
    "github": {
      "type": "http",
      "url": "https://api.github.com/mcp",
      "headers": {
        "Authorization": "Bearer ${GITHUB_TOKEN}"
      }
    },
    // WebSocket 服务器
    "custom-api": {
      "type": "ws",
      "url": "wss://api.example.com/mcp",
      "headersHelper": "getCustomHeaders"
    }
  }
}
```

配置后，AI 的工具列表中会出现 `mcp__filesystem__read_file`、`mcp__github__*` 等工具——与内置工具使用相同的权限检查链路和 UI 渲染。

## 下一步

*   了解 MCP 工具如何进入权限检查链路：[权限模型与规则引擎](15-quan-xian-mo-xing-yu-gui-ze-yin-qing.md)
*   探索 MCP 与 Claude.ai 的深度集成：[Voice Mode 语音模式](14-voice-mode-yu-yin-mo-shi.md)
*   查看 MCP 技能的实验性发现功能：[MCP\_SKILLS 功能说明](#root/YaZGxeUiEB5Y)

## 相关条目
- [[11-nei-zhi-gong-ju-xiang-jie]]
- [[MCP协议与工具调用]]
