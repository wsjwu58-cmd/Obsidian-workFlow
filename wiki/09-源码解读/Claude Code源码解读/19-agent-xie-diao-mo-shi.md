# 19-agent-xie-diao-mo-shi
Agent 协调模式（Coordinator Mode）是一种多 Agent 编排架构，将 Claude Code 从"执行者"转变为"编排者"角色。该模式通过星型拓扑实现任务分发与并行执行，适用于大型任务拆分、并行研究、实现与验证分离等复杂场景。

Sources: [coordinatorMode.ts](#root/DOjKQE4q2GPJ), [coordinator-and-swarm.mdx](#root/qMOklzZV7EqG)

## 架构概述

Coordinator Mode 采用**星型编排架构**，编排者（Coordinator）居中协调，多个工作者（Worker）在外围并行执行。这种设计将决策与执行分离，确保复杂任务得到系统化处理。

```
graph TB
    subgraph Coordinator["编排者 (Coordinator)"]
        A[用户请求] --> B[理解与分析]
        B --> C[任务分解]
        C --> D[并行派发 Worker]
    end
    
    subgraph Workers["工作者 (Workers)"]
        D --> E1[Worker A<br/>研究]
        D --> E2[Worker B<br/>实现]
        D --> E3[Worker C<br/>验证]
    end
    
    subgraph Results["结果聚合"]
        E1 --> F1[&lt;task-notification&gt;]
        E2 --> F2[&lt;task-notification&gt;]
        E3 --> F3[&lt;task-notification&gt;]
        F1 --> G[综合分析]
        F2 --> G
        F3 --> G
    end
    
    G --> H[向用户报告]
    
    style Coordinator fill:#e1f5fe
    style Workers fill:#fff3e0
    style Results fill:#e8f5e9
```

Sources: [coordinatorMode.ts](#root/liVNepO0Mqsa)

## 双门控激活机制

Coordinator Mode 采用**双重门控设计**，确保功能可控启用：

| 门控层级 | 配置方式 | 作用 |
| --- | --- | --- |
| **构建时门控** | `FEATURE_COORDINATOR_MODE=1` | 控制代码可用性，允许编译时包含但不默认启用 |
| **运行时门控** | `CLAUDE_CODE_COORDINATOR_MODE=1` | 控制实际激活状态 |

启用命令：

```
FEATURE_COORDINATOR_MODE=1 CLAUDE_CODE_COORDINATOR_MODE=1 bun run dev
```

Sources: [coordinatorMode.ts](#root/H1f0y6ZCfd7Z)

### 会话模式恢复

`matchSessionMode()` 函数确保会话恢复时模式一致性：

```typescript
export function matchSessionMode(
  sessionMode: 'coordinator' | 'normal' | undefined,
): string | undefined {
  const currentIsCoordinator = isCoordinatorMode()
  const sessionIsCoordinator = sessionMode === 'coordinator'

  if (currentIsCoordinator === sessionIsCoordinator) {
    return undefined
  }

  // 自动翻转环境变量以匹配恢复的会话模式
  if (sessionIsCoordinator) {
    process.env.CLAUDE_CODE_COORDINATOR_MODE = '1'
  } else {
    delete process.env.CLAUDE_CODE_COORDINATOR_MODE
  }

  return sessionIsCoordinator
    ? 'Entered coordinator mode to match resumed session.'
    : 'Exited coordinator mode to match resumed session.'
}
```

Sources: [coordinatorMode.ts](#root/HrA9gKyDSQGN)

## 工具集约束

### 编排者受限工具集

编排者被剥夺了所有"动手"工具，仅保留编排能力：

| 工具 | 用途 | 限制 |
| --- | --- | --- |
| **Agent** | 启动新 Worker（`subagent_type: "worker"`） | 只能派发任务 |
| **SendMessage** | 向已有 Worker 发送后续指令 | 定向续传 |
| **TaskStop** | 中途停止走错方向的 Worker | 错误修正 |
| **subscribe\_pr\_activity** | 订阅 GitHub PR 事件 | 可选功能 |

编排者**不写代码、不读文件、不执行命令**——它只做三件事：理解需求、分配任务、综合结果。

Sources: [coordinatorMode.ts](#root/jkuavdwh0lP6)

### Worker 完整工具集

Worker 的可用工具由 `getCoordinatorUserContext()` 动态注入：

```typescript
const workerTools = isEnvTruthy(process.env.CLAUDE_CODE_SIMPLE)
  ? [BASH_TOOL_NAME, FILE_READ_TOOL_NAME, FILE_EDIT_TOOL_NAME]  // Simple 模式
  : Array.from(ASYNC_AGENT_ALLOWED_TOOLS)
      .filter(name => !INTERNAL_WORKER_TOOLS.has(name))  // 标准模式
```

标准模式包含：`FileRead`、`Bash`、`Grep`、`Glob`、`WebSearch`、`WebFetch`、`Edit`、`Write`、`NotebookEdit`、`Skill`、`ToolSearch`、`EnterWorktree`、`ExitWorktree`、`TodoWrite`。

Sources: [coordinatorMode.ts](#root/WYsTJm1fnrBt), [tools.ts](#root/Z2AwX2cFO9Ra)

### 内部工具排除

`INTERNAL_WORKER_TOOLS` 显式排除以下工具，防止不可控的递归：

*   `TeamCreate` - Worker 不能嵌套创建团队
*   `TeamDelete` - Worker 不能删除团队
*   `SendMessage` - Worker 不能发送消息
*   `SyntheticOutput` - Worker 不能生成合成输出

Sources: [coordinatorMode.ts](#root/mXb0sr7b5ozg)

## Scratchpad 跨 Worker 知识共享

当 GrowthBook `tengu_scratch` 功能启用时，Coordinator 拥有一个 Scratchpad 目录供 Worker 共享知识：

```typescript
if (scratchpadDir && isScratchpadGateEnabled()) {
  content += `\n\nScratchpad directory: ${scratchpadDir}\nWorkers can read and write here without permission prompts.`
}
```

这是关键的协作原语——Worker A 的研究结果可写入 Scratchpad，Worker B 直接读取，无需通过 Coordinator 中转。

Sources: [coordinatorMode.ts](#root/9UUiw06hPI1E)

## `<task-notification>` 通信协议

Worker 完成后，结果以 XML 格式的 `<task-notification>` 送达：

```xml
<task-notification>
  <task-id>agent-a1b</task-id>
  <status>completed|failed|killed</status>
  <summary>Agent "调查 auth bug" completed</summary>
  <result>在 src/auth/validate.ts:42 发现 null pointer...</result>
  <usage>
    <total_tokens>N</total_tokens>
    <tool_uses>N</tool_uses>
    <duration_ms>N</duration_ms>
  </usage>
</task-notification>
```

通知以 `user-role message` 形式到达，Coordinator 通过 `<task-id>` 实现定向续传。

Sources: [coordinatorMode.ts](#root/EIj0VkDk0mcF)

## 任务工作流

典型任务遵循四阶段流程：

```
flowchart LR
    A[用户请求] --> B[研究阶段<br/>Workers 并行调查]
    B --> C[综合阶段<br/>Coordinator 理解问题]
    C --> D[实现阶段<br/>Workers 执行修改]
    D --> E[验证阶段<br/>Workers 独立验证]
    E --> F[报告结果]
    
    style B fill:#e3f2fd
    style C fill:#fff3e0
    style D fill:#e8f5e9
    style E fill:#fce4ec
```

| 阶段 | 执行者 | 目的 |
| --- | --- | --- |
| **Research** | Workers（并行） | 调查代码库、理解问题 |
| **Synthesis** | **Coordinator**（独占） | 阅读发现、理解问题、编写实现规格 |
| **Implementation** | Workers | 根据规格进行针对性修改 |
| **Verification** | Workers | 证明代码工作，独立验证 |

Sources: [coordinatorMode.ts](#root/oQD31xlBy0nx)

## 综合（Synthesis）核心约束

Coordinator System Prompt 明确要求**不能懒惰地委派理解**：

```
反模式（禁止）：
  "Based on your findings, fix the auth bug"
  → 把理解的责任推给了 Worker

正确做法：
  "Fix the null pointer in src/auth/validate.ts:42.
   The user field on Session (src/auth/types.ts:15) is
   undefined when sessions expire but the token remains cached.
   Add a null check before user.id access."
  → Coordinator 自己理解问题，给出精确指令
```

这是 Coordinator Mode 最核心的设计约束：Coordinator 必须先理解，再分配。

Sources: [coordinatorMode.ts](#root/gqWPb3p8xC5R)

## 继续 vs 新建决策表

| 情境 | 机制 | 原因 |
| --- | --- | --- |
| 研究探索了恰好需要编辑的文件 | **继续**（SendMessage） | Worker 已有上下文，现在获得明确计划 |
| 研究范围广但实现范围窄 | **新建**（Agent） | 避免携带探索噪声，聚焦上下文更干净 |
| 修正失败或延续最近工作 | **继续** | Worker 有错误上下文，知道刚尝试了什么 |
| 验证其他 Worker 刚写的代码 | **新建** | 验证者应独立审视，不带实现假设 |
| 第一次实现使用了完全错误的方法 | **新建** | 错误方法上下文污染；干净开始避免锚定失败路径 |
| 完全无关的任务 | **新建** | 无有用上下文可复用 |

Sources: [coordinatorMode.ts](#root/2qLy4F4DkUAw)

## 典型工作流示例

```
用户: "修复 auth 模块的 null pointer"

编排者:
  1. 并行派发两个 worker:
     - Agent({ description: "调查 auth bug", prompt: "..." })
     - Agent({ description: "研究 auth 测试", prompt: "..." })

  2. 收到 <task-notification>:
     - Worker A: "在 validate.ts:42 发现 null pointer"
     - Worker B: "测试覆盖情况..."

  3. 综合发现，继续 Worker A:
     - SendMessage({ to: "agent-a1b", message: "修复 validate.ts:42..." })

  4. 收到修复结果，派发验证:
     - Agent({ description: "验证修复", prompt: "..." })
```

Sources: [coordinatorMode.ts](#root/9E1IIjV9AcEy)

## 文件索引

| 文件 | 职责 | 核心函数/类型 |
| --- | --- | --- |
| `src/coordinator/coordinatorMode.ts` | 模式检测、用户上下文、系统提示 | `isCoordinatorMode()`, `getCoordinatorUserContext()`, `getCoordinatorSystemPrompt()` |
| `src/coordinator/workerAgent.ts` | Worker agent 定义（当前为 stub） | `getCoordinatorAgents()` |
| `src/tools/AgentTool/AgentTool.tsx` | Agent 工具实现、异步任务注册 | `AgentTool.call()` |
| `src/tools/AgentTool/prompt.ts` | Agent 工具描述生成 | `getPrompt()` |
| `src/constants/tools.ts` | 异步 Agent 允许的工具白名单 | `ASYNC_AGENT_ALLOWED_TOOLS` |
| `src/tools/AgentTool/builtInAgents.ts` | 内置 Agent 加载逻辑 | `getBuiltInAgents()` |

Sources: [workerAgent.ts](#root/cRvAVX0FgB3d), [AgentTool.tsx](#root/drHjbWATXZDn), [builtInAgents.ts](#root/7mN6LCxQOE9n)

## 配置选项

```
# 基本启用
FEATURE_COORDINATOR_MODE=1 CLAUDE_CODE_COORDINATOR_MODE=1 bun run dev

# 配合 Fork Subagent（实验性）
FEATURE_COORDINATOR_MODE=1 FEATURE_FORK_SUBAGENT=1 \
CLAUDE_CODE_COORDINATOR_MODE=1 bun run dev

# Simple 模式（Worker 只有 Bash/Read/Edit）
FEATURE_COORDINATOR_MODE=1 CLAUDE_CODE_COORDINATOR_MODE=1 \
CLAUDE_CODE_SIMPLE=1 bun run dev

# 配合 MCP 服务器
FEATURE_COORDINATOR_MODE=1 CLAUDE_CODE_COORDINATOR_MODE=1 \
mcp__server-name__tool-name bun run dev
```

Sources: [docs/features/coordinator-mode.md](#root/vurYpqAMutZi)

## 与 Agent Swarms 的对比

| 维度 | Coordinator Mode | Agent Swarms |
| --- | --- | --- |
| **拓扑** | 星型：Coordinator 居中，Worker 外围 | 网状：对等 Agent 共享任务列表 |
| **角色** | 明确分工：Coordinator 编排、Worker 执行 | 模糊：每个 Agent 自主认领任务 |
| **通信** | `SendMessage` 定向通信 + `<task-notification>` | 任务文件系统 + 邮箱广播 |
| **适用** | 需要集中决策的复杂任务 | 并行度高的独立子任务 |

两者不是互斥的——Coordinator Mode 可以在 Swarm 架构之上运行，将 Coordinator 作为特殊的 Leader Agent。

Sources: [coordinator-and-swarm.mdx](#root/a8wWRQO0VpDW)

## 后续阅读

*   [Memory 记忆系统](20-memory-ji-yi-xi-tong.md) — 了解跨会话记忆与 Worker 共享知识
*   [自定义 Agents](21-zi-ding-yi-agents.md) — 学习定义专用 Agent 类型
*   [工具系统架构](10-gong-ju-xi-tong-jia-gou.md) — 深入理解 Agent 工具机制

## 相关条目
- [[7-agentic-loop-he-xin-xun-huan]]
- [[20-memory-ji-yi-xi-tong]]
