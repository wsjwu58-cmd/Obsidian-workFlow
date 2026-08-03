# 18-remote-control-yuan-cheng-kong-zhi
Remote Control（远程控制）是 Claude Code 的核心功能之一，允许用户通过 claude.ai 网页界面远程控制本地运行的 Claude Code 实例。本地 CLI 作为"执行者"（worker），接受来自远程控制面的指令并执行，同时将执行结果实时回传至网页界面。

## 一、架构概述

### 1.1 核心设计理念

Remote Control 采用**桥接模式（Bridge Pattern）**，将本地终端转变为可远程驱动的执行环境。远程用户可以在 claude.ai 上查看会话、发送指令、审批权限请求，而所有实际操作都在本地机器上执行。

```
flowchart TB
    subgraph Remote["claude.ai 控制面"]
        A[Web UI]
        B[Session Manager]
        C[Permission Approval]
    end
    
    subgraph Local["本地 Claude Code"]
        D[Bridge Module]
        E[REPL Session]
        F[Tools Executor]
    end
    
    subgraph Protocol["通信协议"]
        G[Environments API]
        H[Session Ingress WS]
        I[CCR v2 Protocol]
    end
    
    A --> B
    B --> G
    G -->|poll/ack/heartbeat| D
    D --> H
    D --> I
    H <--> E
    E --> F
    C <-->|control_response| D
    
    style Remote fill:#e1f5fe
    style Local fill:#fff3e0
    style Protocol fill:#f3e5f5
```

### 1.2 版本演进

| 版本 | 实现文件 | 架构特点 | GrowthBook 门控 |
| --- | --- | --- | --- |
| **v1 (env-based)** | `src/bridge/replBridge.ts` | 基于 Environments API 的工作轮询模式 | `tengu_ccr_bridge` |
| **v2 (env-less)** | `src/bridge/remoteBridgeCore.ts` | 直接连接 Session Ingress，无需 Environments 层 | `tengu_bridge_repl_v2` |

v2 版本通过 `POST /v1/code/sessions/{id}/bridge` 端点直接获取 worker JWT，省去了 Environments API 的注册/轮询/确认/停止/心跳/注销完整生命周期，连接更简洁高效。

Sources: [remoteBridgeCore.ts](#root/q3cwPIu3HdQP) Sources: [replBridge.ts](#root/oSOTPx5SuznE)

## 二、模块架构详解

### 2.1 目录结构

```
src/bridge/
├── bridgeApi.ts           # Environments API HTTP 客户端
├── bridgeConfig.ts        # 认证与 URL 配置解析
├── bridgeEnabled.ts      # 功能开关与权限检查
├── bridgeMain.ts         # 多会话桥接主循环
├── bridgeMessaging.ts     # 消息解析与路由
├── bridgePermissionCallbacks.ts  # 权限请求处理
├── bridgePointer.ts      # 活跃桥接状态指针
├── bridgeStatusUtil.ts   # 状态显示工具
├── bridgeUI.ts           # UI 组件
├── capacityWake.ts       # 容量唤醒机制
├── createSession.ts      # 会话创建/归档 API
├── envLessBridgeConfig.ts # v2 配置参数
├── flushGate.ts          # 刷新控制
├── inboundAttachments.ts # 入站附件处理
├── inboundMessages.ts    # 入站消息处理
├── initReplBridge.ts     # REPL 桥接初始化入口
├── jwtUtils.ts           # JWT 令牌刷新调度
├── peerSessions.ts       # 对等会话管理
├── pollConfig.ts         # 轮询间隔配置
├── remoteBridgeCore.ts   # v2 核心实现
├── replBridge.ts         # v1 核心实现
├── replBridgeHandle.ts   # 桥接句柄管理
├── replBridgeTransport.ts # 传输层抽象
├── sessionIdCompat.ts    # session_* 与 cse_* ID 兼容
├── sessionRunner.ts      # 子进程会话运行器
├── trustedDevice.ts      # 可信设备令牌管理
├── types.ts              # 核心类型定义
├── workSecret.ts         # 工作密钥编解码
└── src/entrypoints/sdk/  # SDK 控制协议类型
```

Sources: [types.ts](#root/R6zyxR4cIrCO)

### 2.2 API 协议设计

Bridge API Client 提供 9 个核心操作，通过 `src/bridge/bridgeApi.ts` 实现：

| 操作 | HTTP 方法 | 端点 | 说明 |
| --- | --- | --- | --- |
| `registerBridgeEnvironment` | POST | `/v1/environments/bridge` | 注册本地环境 |
| `pollForWork` | GET | `/v1/environments/{id}/work/poll` | 长轮询等待任务 |
| `acknowledgeWork` | POST | `/v1/environments/{id}/work/{workId}/ack` | 确认接收任务 |
| `stopWork` | POST | `/v1/environments/{id}/work/{workId}/stop` | 停止任务 |
| `heartbeatWork` | POST | `/v1/environments/{id}/work/{workId}/heartbeat` | 续约任务租约 |
| `deregisterEnvironment` | DELETE | `/v1/environments/bridge/{id}` | 注销环境 |
| `archiveSession` | POST | `/v1/sessions/{id}/archive` | 归档会话 |
| `sendPermissionResponseEvent` | POST | `/v1/sessions/{id}/events` | 发送权限审批结果 |
| `reconnectSession` | POST | `/v1/environments/{id}/bridge/reconnect` | 重连已存在会话 |

Sources: [bridgeApi.ts](#root/QSnuSW9SVNRr)

### 2.3 传输层抽象

`replBridgeTransport.ts` 定义了统一的传输接口，同时支持 v1 和 v2 两种传输协议：

```typescript
export type ReplBridgeTransport = {
  write(message: StdoutMessage): Promise<void>
  writeBatch(messages: StdoutMessage[]): Promise<void>
  close(): void
  isConnectedStatus(): boolean
  getStateLabel(): string
  setOnData(callback: (data: string) => void): void
  setOnClose(callback: (closeCode?: number) => void): void
  setOnConnect(callback: () => void): void
  connect(): void
  getLastSequenceNum(): number
  reportState(state: SessionState): void
  reportMetadata(metadata: Record<string, unknown>): void
  reportDelivery(eventId: string, status: 'processing' | 'processed'): void
  flush(): Promise<void>
}
```

**v1 传输**：使用 `HybridTransport`（WebSocket 读取 + HTTP POST 写入） **v2 传输**：使用 `SSETransport`（Server-Sent Events 读取）+ `CCRClient`（CCR v2 协议写入）

Sources: [replBridgeTransport.ts](#root/tDLCRV31Ja6J)

## 三、安全设计

### 3.1 认证体系

Remote Control 依赖 claude.ai OAuth 认证，与 Bedrock/Vertex/Console API 等部署方式隔离：

```typescript
function isBridgeEnabled(): boolean {
  return feature('BRIDGE_MODE')
    ? isClaudeAISubscriber() &&
        getFeatureValue_CACHED_MAY_BE_STALE('tengu_ccr_bridge', false)
    : false
}
```

**前置条件检查**：

1.  `FEATURE_BRIDGE_MODE` 编译时特性开关已启用
2.  用户已通过 `claude.ai` OAuth 登录（非 API Key）
3.  用户 token 包含 `user:profile` scope
4.  GrowthBook 门控 `tengu_ccr_bridge` 已开启

Sources: [bridgeEnabled.ts](#root/zIkhzi6gDlzc)

### 3.2 可信设备认证

v2 桥接会话使用 SecurityTier=ELEVATED，需要可信设备令牌增强安全性：

```
sequenceDiagram
    participant CLI
    participant Keychain
    participant Server
    participant GrowthBook
    
    CLI->>GrowthBook: 检查门控状态
    GrowthBook-->>CLI: tengu_sessions_elevated_auth_enforcement
    CLI->>Keychain: 读取 trustedDeviceToken
    CLI->>Server: POST /auth/trusted_devices
    Server-->>Keychain: 存储 device_token (90d)
    CLI->>Server: Bridge API 调用 + X-Trusted-Device-Token
```

可信设备注册在 `/login` 期间完成（server 端限制 `created_at < 10min`）。

Sources: [trustedDevice.ts](#root/XnWtrHbJ8G03)

### 3.3 安全防护措施

| 防护机制 | 实现位置 | 说明 |
| --- | --- | --- |
| **ID 白名单验证** | `bridgeApi.ts:validateBridgeId()` | 使用 `/^[a-zA-Z0-9_-]+$/` 验证所有服务端 ID |
| **致命错误处理** | `BridgeFatalError` | 401/403/404/410 直接抛出，阻止重试循环 |
| **OAuth 自动刷新** | `withOAuthRetry()` | 401 时自动刷新 token 并重试一次 |
| **JWT 主动刷新** | `jwtUtils.ts` | 提前 5 分钟刷新 worker JWT |

Sources: [bridgeApi.ts](#root/BGHqScsrf0UX)

## 四、会话生命周期

### 4.1 v1 (env-based) 流程

```
sequenceDiagram
    participant CLI
    participant BridgeAPI as Environments API
    participant SessionIngress as Session Ingress
    participant WebUI as claude.ai
    
    CLI->>BridgeAPI: POST /v1/environments/bridge
    BridgeAPI-->>CLI: environment_id + environment_secret
    
    loop 长轮询
        CLI->>BridgeAPI: GET .../work/poll (10s 超时)
        alt 有新工作
            BridgeAPI-->>CLI: WorkResponse { sessionId, secret }
            CLI->>CLI: decodeWorkSecret(secret)
            CLI->>SessionIngress: WebSocket 连接
            CLI->>BridgeAPI: POST .../work/{id}/ack
            CLI->>CLI: 启动子进程 REPL
            loop 任务执行中
                CLI->>BridgeAPI: heartbeatWork (续约)
                CLI->>SessionIngress: writeMessages()
            end
            CLI->>BridgeAPI: archiveSession
        else 无工作
            BridgeAPI-->>CLI: null
        end
    end
    
    WebUI->>SessionIngress: control_response (权限审批)
    SessionIngress->>CLI: 转发权限请求
    CLI->>CLI: 等待用户审批
    CLI->>SessionIngress: 回复审批结果
```

### 4.2 v2 (env-less) 流程

```
sequenceDiagram
    participant CLI
    participant SessionsAPI as Sessions API
    participant SessionIngress as Session Ingress
    participant CCRClient as CCRClient
    
    CLI->>SessionsAPI: POST /v1/code/sessions
    SessionsAPI-->>CLI: session_id
    
    CLI->>SessionsAPI: POST /v1/code/sessions/{id}/bridge
    SessionsAPI-->>CLI: { worker_jwt, expires_in, api_base_url, worker_epoch }
    
    CLI->>CCRClient: 初始化 (worker_jwt, epoch)
    CLI->>SessionIngress: SSETransport 连接
    
    loop 运行中
        CCRClient->>SessionsAPI: heartbeat (20s 间隔, ±10% jitter)
        alt Token 即将过期
            CLI->>SessionsAPI: 重新调用 /bridge 获取新 JWT
        end
    end
    
    Note over CLI: 无需 Environments API<br/>更简洁的连接流程
```

Sources: [remoteBridgeCore.ts](#root/gzojkfNfcjBQ)

### 4.3 子进程会话管理

`sessionsRunner.ts` 负责创建和管理子进程 Claude Code 实例：

```typescript
export type SessionSpawnOpts = {
  sessionId: string
  sdkUrl: string
  accessToken: string
  useCcrV2?: boolean      // v2 传输协议
  workerEpoch?: number    // v2 需要
  // ...其他选项
}
```

会话通过 spawn 创建子进程，stdin/stdout 通过 IPC 与父进程通信，捕获工具调用活动用于状态显示。

Sources: [sessionRunner.ts](#root/96uEF7o9u8zz)

## 五、权限管理

### 5.1 权限请求流程

当远程会话中的 Claude 需要执行敏感操作（如编辑文件、运行命令）时：

```
sequenceDiagram
    participant RemoteAgent
    participant Bridge as Bridge Module
    participant Ingress as Session Ingress
    participant Web as claude.ai UI
    participant User
    
    RemoteAgent->>Bridge: can_use_tool 控制请求
    Bridge->>Ingress: 转发请求
    Ingress->>Web: 推送 permission_request
    Web->>User: 显示审批对话框
    User->>Web: 批准/拒绝
    Web->>Ingress: control_response
    Ingress->>Bridge: 转发响应
    Bridge->>RemoteAgent: 执行或拒绝
```

权限回调通过 `bridgePermissionCallbacks.ts` 实现：

```typescript
export type BridgePermissionCallbacks = {
  onPermissionRequest: (
    toolName: string,
    toolInput: Record<string, unknown>,
    toolUseId: string,
  ) => Promise<BridgePermissionResponse>
}
```

Sources: [bridgePermissionCallbacks.ts](#root/eSjBNswrebZK)

### 5.2 权限响应类型

```typescript
export type BridgePermissionResponse =
  | { behavior: 'allow'; updatedInput?: Record<string, unknown> }
  | { behavior: 'deny'; message?: string }
  | { behavior: 'bypass'; updatedInput?: Record<string, unknown> }
```

Sources: [bridgePermissionCallbacks.ts](#root/IMrsYkZG8xiI)

## 六、CLI 命令

### 6.1 /remote-control 命令

通过 `src/commands/bridge/` 实现：

```typescript
const bridge = {
  type: 'local-jsx',
  name: 'remote-control',
  aliases: ['rc'],
  description: 'Connect this terminal for remote-control sessions',
  argumentHint: '[name]',
  isEnabled: () => isBridgeEnabled(),
  immediate: true,
  load: () => import('./bridge.js'),
}
```

**使用方式**：

```
# 启用远程控制
/remote-control

# 启用并命名会话
/remote-control "My Dev Session"

# 别名
/rc
```

Sources: [bridge/index.ts](#root/BYLnl8QlX85f) Sources: [bridge/bridge.tsx](#root/0zFiGHUnvK9U)

### 6.2 启动时自动连接

通过 GrowthBook 门控 `tengu_cobalt_harbor` 控制启动时自动连接：

```typescript
export function getCcrAutoConnectDefault(): boolean {
  return feature('CCR_AUTO_CONNECT')
    ? getFeatureValue_CACHED_MAY_BE_STALE('tengu_cobalt_harbor', false)
    : false
}
```

可通过配置 `remoteControlAtStartup: false` 禁用自动连接。

Sources: [bridgeEnabled.ts](#root/93TdFqhmV1kK)

## 七、配置参数

### 7.1 v2 桥接配置

通过 `tengu_bridge_repl_v2_config` GrowthBook 标志配置：

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `init_retry_max_attempts` | 3 | 初始化重试次数 |
| `init_retry_base_delay_ms` | 500 | 重试基础延迟 |
| `http_timeout_ms` | 10,000 | HTTP 请求超时 |
| `uuid_dedup_buffer_size` | 2000 | UUID 去重缓冲区大小 |
| `heartbeat_interval_ms` | 20,000 | 心跳间隔（Server TTL 60s） |
| `heartbeat_jitter_fraction` | 0.1 | 心跳抖动系数 |
| `token_refresh_buffer_ms` | 300,000 | JWT 刷新提前量（5min） |
| `connect_timeout_ms` | 15,000 | 连接超时 |

Sources: [envLessBridgeConfig.ts](#root/aiMOxhIdSCDQ)

### 7.2 轮询配置

通过 `tengu_bridge_poll_interval_config` GrowthBook 标志配置：

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `poll_interval_ms_not_at_capacity` | 2,000 | 空闲时轮询间隔 |
| `poll_interval_ms_at_capacity` | 600,000 | 满载时轮询间隔（10min） |
| `reclaim_older_than_ms` | 5,000 | 拾取超时任务的阈值 |
| `session_keepalive_interval_v2_ms` | 120,000 | WS 保活帧间隔 |

Sources: [pollConfigDefaults.ts](#root/yavGBfxxqKCo)

## 八、状态管理

### 8.1 React Hook 集成

`useReplBridge` Hook 管理桥接生命周期：

```typescript
export function useReplBridge(
  messages: Message[],
  setMessages: SetStateAction<Message[]>,
  abortControllerRef: RefObject<AbortController | null>,
  commands: readonly Command[],
  mainLoopModel: string
): { sendBridgeResult: () => void }
```

**核心功能**：

*   监听 `replBridgeEnabled` AppState 变化
*   管理 `initReplBridge` 调用和 teardown
*   防止重复初始化（连续失败熔断）
*   消息同步（已发送 UUID 去重）

Sources: [useReplBridge.tsx](#root/7gxJFe9zl3qF)

### 8.2 BridgeState 状态机

```typescript
export type BridgeState = 'ready' | 'connected' | 'reconnecting' | 'failed'
```

状态转换图：

```
stateDiagram-v2
    [*] --> ready: 初始化
    ready --> connected: 注册成功
    ready --> failed: 前置条件失败
    connected --> reconnecting: 连接断开
    reconnecting --> connected: 重连成功
    reconnecting --> failed: 重连超时
    failed --> ready: 重试
```

## 九、最佳实践

### 9.1 生产环境使用

```
# 启用桥接模式（编译时）
export FEATURE_BRIDGE_MODE=1

# 运行 CLI
claude

# 在 REPL 中启用远程控制
/remote-control
```

### 9.2 多会话支持

```
# 启动多个桥接环境
claude --spawn 4

# 查看桥接状态
/bridge status
```

### 9.3 调试配置

```
# 设置调试文件输出
claude --debug-file /tmp/bridge-debug.log

# 查看详细日志
claude --verbose
```

## 十、相关文档

*   [权限模型与规则引擎](15-quan-xian-mo-xing-yu-gui-ze-yin-qing.md) — 了解 Remote Control 的权限决策机制
*   [Agent 协调模式](19-agent-xie-diao-mo-shi.md) — 了解多 Agent 协作场景
*   [工具系统架构](10-gong-ju-xi-tong-jia-gou.md) — 了解远程执行工具的基础
*   [Auto Mode 自动模式](16-auto-mode-zi-dong-mo-shi.md) — 了解与 Remote Control 的交互

## 相关条目
- [[17-sha-xiang-an-quan-ji-zhi]]
- [[14-voice-mode-yu-yin-mo-shi]]
