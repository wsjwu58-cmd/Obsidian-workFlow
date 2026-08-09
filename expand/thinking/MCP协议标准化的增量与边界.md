---
created: 2026-08-09
updated: 2026-08-09
sources: [references/articles.md#14]
tags: [MCP, AI Agent, 协议标准化, type/想法]
---

# MCP 协议标准化的增量与边界

> 论点：官方文档把 MCP 比作「AI 应用的 USB-C」，这个类比在**接口/传输层**成立，在**语义层**不成立——协议标准化把集成成本从「每个模型 × 每个工具的协议适配」转移成了「每个 server 的语义适配与质量治理」，M×N 问题没有消失，只是换了战场。2026-07-28 版本文档的增量（MCP Apps / Agent Skills / Registry / `server/discover`）恰好说明：MCP 正在从「工具调用协议」长成「AI 应用平台层」。

## 一、官方文档说了什么（压缩）

MCP 是连接 AI 应用与外部系统（数据 / 工具 / 工作流）的开放标准，口号是「build once, integrate everywhere」，官方类比是「AI 应用的 USB-C」。

## 二、类比成立到哪一层

### 成立：接口层（传输 + 原语枚举）

- 架构文档把 MCP 拆成两层：**数据层**（JSON-RPC 2.0 消息、`server/discover` 能力发现、tools / resources / prompts 三个原语、通知与进度）与**传输层**（本地 stdio、远程 Streamable HTTP + OAuth）。
- 这两层才是「插头规格」：客户端生态（Claude、ChatGPT、VSCode、Cursor）只需实现一次连接逻辑，就能连上任何符合规范的 server——USB-C 类比真正的成立处是**接口一致 → 即插即用**。

### 不成立：语义层（每个 tool 仍是私有协议）

- USB-C 的语义（供电协商、DP / Thunderbolt 备选模式）由协议完整定义，插上就知道能干什么；MCP 只定义「信封」和三个粗粒度原语，**每个 tool 的输入输出 schema、错误语义、权限边界仍由各家 server 自治**。
- 后果：集成方（或 LLM 本身）依然要为每个 server 读文档、写调用示例、做 prompt 适配，还要防备「工具描述与实现不符」「长尾 server 质量参差」。M×N 从「协议适配」转为「语义适配 + 质量适配」，成本换了个名字，没消失。
- 更关键的不等式：**USB-C 插错设备最多不通电，MCP 接错权限可能泄露数据或触发副作用**。协议不解决信任问题——OAuth 2.1 授权、沙箱、审计仍是 host 的责任，官方只给 best practices 而非强制。

## 三、2026-07-28 版本文档的实质增量（相对知识库既有笔记）

知识库既有 [[MCP协议与工具调用]] 覆盖的是 2024–2025 经典视图（Client-Server、JSON-RPC、三原语）。本次官方文档可提取的新信号：

| 增量 | 含义 | 我的判断 |
|------|------|---------|
| `server/discover` 强制发现 | 版本 / 能力协商前置，请求自带 `_meta` 版本与能力 | 生态规模大到必须治理兼容性，走向「规范即契约」 |
| Sampling 原语废弃 | 服务器向用户采样被移除 | 收缩边界：server 只做「能力提供」，不做「用户交互」 |
| MCP Apps（扩展） | 可在 host 内渲染交互 UI 的应用 | 从「工具调用」扩展到「应用平台」，最值得注意的方向性变化 |
| Agent Skills over MCP | 技能经 MCP 分发的标准化工作组 | 与 Claude Code skills / ECC 技能体系同源，工程化赛道 |
| Registry + SEPs | 服务器注册表 + 规范增强提案流程 | 治理架构成型：谁来收录、怎么演进、如何淘汰 |
| 远程 server 一等公民 | Streamable HTTP + OAuth 2.1 教程 | 从本地 stdio 主场景走向企业远程部署 |

判断：这些增量共同说明 MCP 的野心不是「又一个工具调用格式」，而是 **AI 应用的外部能力总线 + 分发平台**。风险随之放大：Active / Deprecated / Removed 生命周期会带来版本碎片化成本，2025→2026 的 breaking change（sampling 废弃、discover 引入）已让旧 SDK 代码需要迁移。

## 四、对本知识库 / 自动化管线的启示

- 本仓库 worker（codex-cli + GitHub Actions）目前是「脚本编排」；若未来要把外部工具（搜索 / 文档解析 / 数据库）接进自动化管线，MCP 是比各家私有 API 更稳的接入层候选——但接入前必须**锁定 spec/SDK 版本并验证授权边界**（见下方最小示例）。
- 与 [[ECC]]（harness 操作系统）、[[n8n]]（可视化编排）对照：MCP 解决「连接」层，ECC / n8n 解决「编排」层，三层正交、可组合。

## 五、结论与开放问题

结论：MCP 值得收录。2026-07-28 版本文档给出可落地的协议结构（双层、强制发现、原语收缩）与治理机制（Registry / SEP / 生命周期），官方 Python SDK（`mcp` 2.x）已把复杂度收进 `Client` / `MCPServer` 两个类。

开放问题（留给后续素材）：

1. 「语义适配 M×N」最终靠什么解决——靠 Server Card / Registry 的质量治理，还是靠 Agent 推理能力消化？目前两者都在路上。
2. 规范演进 vs 生态碎片：sampling 废弃、discover 引入这类 breaking change，会不会让 MCP 重演 HTTP / GraphQL 的版本碎片化？Feature Lifecycle 能否兜底？
3. MCP Apps 若成气候，「host 内交互应用」的代码执行边界与安全模型由谁定义？

## 六、最小可运行示例（Python 官方 SDK，版本锁定）

环境：Python >= 3.10；依赖锁定 `mcp>=2.0,<3`（2026-08 最新 2.0.x，API 以 2026-07-28 文档为准）。

`server.py`：

```python
"""最小 MCP server：验证 tools/list → tools/call 全链路。"""
from mcp.server import MCPServer

mcp = MCPServer("echo-demo")


@mcp.tool()
async def echo(text: str) -> str:
    """原样返回输入，用于链路验证。"""
    return text


if __name__ == "__main__":
    mcp.run(transport="stdio")  # 本地进程间通信
```

`client.py`：

```python
"""最小 MCP client：启动 stdio server → 列工具 → 调用 echo。"""
import asyncio
import sys

from mcp import Client, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("用法: python client.py <server.py>")
    params = StdioServerParameters(command="python", args=[sys.argv[1]])
    async with Client(stdio_client(params)) as client:
        tools = await client.list_tools()
        print("发现工具:", [t.name for t in tools.tools])
        try:
            result = await client.call_tool("echo", {"text": "hello mcp"})
            print("调用结果:", result.content)
        except Exception as e:  # 协议/IO 异常统一上抛，避免裸奔
            print(f"调用失败: {e}", file=sys.stderr)


if __name__ == "__main__":
    asyncio.run(main())
```

运行：`python client.py server.py`——`async with` 负责拉起 / 关闭子进程与协议握手。

## 相关条目

- [[MCP协议与工具调用]]（wiki 既有笔记，单向链接）
- [[12-mcp-xie-yi-ji-cheng]]（Claude Code 的 MCP 集成实现）
- [[ECC]]
- [[自动化工作流设计]]
- [[n8n]]
