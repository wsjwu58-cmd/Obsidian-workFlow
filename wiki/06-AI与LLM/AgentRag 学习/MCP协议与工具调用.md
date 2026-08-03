# MCP协议与工具调用
## 一、MCP 概述

### 1.1 什么是 MCP

MCP（Model Context Protocol）是 Anthropic 于 2024 年 11 月提出的开放性协议标准，旨在定义 LLM 应用与外部工具/数据源之间的标准化通信方式。截至 2025 年，MCP 已被广泛采用为 AI Agent 生态的基础设施标准。

### 1.2 背景：工具调用的演进

在 MCP 出现之前，LLM 工具调用经历了三个混乱阶段：

```
阶段一（2022前）：Prompt Engineering 方式
  在 prompt 中描述工具，用正则解析 LLM 输出
  
阶段二（2023）：OpenAI Function Calling
  OpenAI 定义了 function calling API 格式，但各家实现互不兼容
  
阶段三（2024+）：MCP 标准化
  统一的 JSON-RPC 协议，模型无关、厂商无关
```

**核心矛盾**：每个 LLM 平台（OpenAI, Anthropic, Google）都有各自的工具调用格式，每个工具/数据源需要为每个平台单独编写适配器。这导致了组合爆炸——M 个模型 × N 个工具 = M×N 个适配器。

### 1.3 M×N 问题的数学解释

```
传统集成: 每个(模型, 工具)对都需要独立适配
  OpenAI × GitHub API = 适配器1
  OpenAI × Slack API  = 适配器2
  Claude × GitHub API = 适配器3
  Claude × Slack API  = 适配器4
  ... (M×N 组合)

MCP 方案: 统一中间层
  OpenAI ─┐          ┌─ GitHub
          ├─ MCP ────┤
  Claude ─┘          └─ Slack
  (M + N 个连接)
```

### 1.4 MCP 架构

MCP 采用经典的 **Client-Server 架构**，以 JSON-RPC 2.0 作为通信协议：

```
┌──────────────────┐                        ┌──────────────────┐
│   MCP Client     │     JSON-RPC 2.0       │   MCP Server      │
│  (LLM 应用/Host)  │ ◄────────────────────► │  (工具/数据服务)  │
└──────────────────┘                        └──────────────────┘
       │                                              │
  ┌────┴────┐                                  ┌─────┴─────┐
  │ Claude  │                                  │  Database │
  │ GPT     │                                  │  API      │
  │ Gemini  │                                  │  Files    │
  └─────────┘                                  └───────────┘
```

### 1.5 MCP 三要素

| 概念 | 说明 | 与 LLM 的交互方式 |
| --- | --- | --- |
| **Tools** | 可由 LLM 调用执行的函数 | LLM 决定调用 → Server 执行 → 返回结果 |
| **Resources** | 可供 LLM 读取的结构化数据 | LLM 请求读取 → Server 返回数据 |
| **Prompts** | 预定义的提示模板 | Server 提供 → Client 注入到 LLM 对话中 |

**三要素的设计哲学**：借鉴了编程语言中的"函数-数据结构-模板"三元组。

---

## 二、JSON-RPC 2.0 协议基础

MCP 选择 JSON-RPC 2.0 作为通信协议，这是理解 MCP 底层机制的基础。

### 2.1 协议核心

JSON-RPC 2.0 是无状态的轻量级远程过程调用协议，定义了四种消息类型：

**请求（Request）**：

```
{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
        "name": "add",
        "arguments": {"a": 5, "b": 3}
    }
}
```

**响应（Response）**：

```
{
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
        "content": [{"type": "text", "text": "8"}]
    }
}
```

**错误（Error）**：

```
{
    "jsonrpc": "2.0",
    "id": 1,
    "error": {
        "code": -32601,
        "message": "Method not found",
        "data": "Tool 'divide_by_zero' does not exist"
    }
}
```

**通知（Notification）**：无 `id` 字段，不需要响应：

```
{
    "jsonrpc": "2.0",
    "method": "notifications/initialized"
}
```

### 2.2 MCP 核心方法

| 方法 | 方向 | 作用 |
| --- | --- | --- |
| `initialize` | Client→Server | 握手，协商协议版本和能力 |
| `tools/list` | Client→Server | 列出可用工具 |
| `tools/call` | Client→Server | 调用指定工具 |
| `resources/list` | Client→Server | 列出可用资源 |
| `resources/read` | Client→Server | 读取指定资源 |
| `resources/templates/list` | Client→Server | 列出资源 URI 模板 |
| `prompts/list` | Client→Server | 列出可用提示模板 |
| `prompts/get` | Client→Server | 获取指定提示 |
| `notifications/initialized` | Client→Server | 通知初始化完成 |
| `sampling/createMessage` | Server→Client | 反向请求 LLM 生成 |

### 2.3 通信流程的生命周期

```
1. 连接建立（Transport 层: stdio/HTTP/SSE）
2. Client 发送 initialize 请求 → Server 返回能力声明
3. Client 发送 initialized 通知（握手完成）
4. 正常操作阶段（循环）
   - Client 查询 tools/resources/prompts
   - Client 调用 tools/call 或读取 resources/read
   - Server 可能发起 sampling/createMessage 反向请求
5. 连接关闭
```

---

## 三、MCP Server 开发

### 3.1 FastMCP 快速启动

FastMCP 是简化版的 MCP Server 框架，通过 Python 装饰器声明式定义能力：

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DemoServer", json_response=True)

# 定义工具
@mcp.tool()
def add(a: int, b: int) -> int:
    """将两个数相加"""
    return a + b

# 定义资源（动态 URI 模板）
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """获取个性化问候"""
    return f"你好，{name}！"

# 定义提示模板
@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """生成问候提示"""
    styles = {
        "friendly": "请写一段温暖友好的问候",
        "formal": "请写一段正式专业的问候",
        "casual": "请写一段轻松随意的问候",
    }
    return f"{styles.get(style, styles['friendly'])}，对象是{name}。"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
```

### 3.2 使用标准 MCPServer

对于需要更细粒度控制的场景：

```python
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("MyServer", json_response=True)

@mcp.tool()
def search_database(query: str, limit: int = 10) -> str:
    """搜索数据库"""
    results = db.search(query, limit=limit)
    return json.dumps(results, ensure_ascii=False)

@mcp.resource("file://{path}")
def read_file(path: str) -> str:
    """读取文件内容"""
    with open(path, "r") as f:
        return f.read()

@mcp.prompt()
def code_review(code: str, language: str) -> str:
    """代码审查提示模板"""
    return f"""请审查以下 {language} 代码：
1. 检查安全漏洞
2. 评估性能
3. 建议改进方案

```{language}
{code}
```"""

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
```

### 3.3 传输方式的深入对比

| 传输方式 | 底层协议 | 连接模式 | 优势 | 劣势 | 适用场景 |
| --- | --- | --- | --- | --- | --- |
| **stdio** | 标准 I/O | 进程管道 | 零网络开销，最简单 | 仅限本地进程，无并发 | IDE 插件、CLI 工具 |
| **Streamable HTTP** | HTTP/1.1 | Request-Response + SSE | 无需长连接，穿透防火墙 | 无服务端推送 | Web 服务、微服务 |
| **SSE** | HTTP/1.1 | 服务端→客户端单向流 | 实时推送，简单 | 单向，需要额外通道发请求 | 通知、日志流 |

**为什么 MCP 支持多种传输**：不同部署场景的约束不同。IDE 插件场景中，本地进程间通信用 stdio 最自然；云端微服务场景中，HTTP 是唯一可选方案；需要服务器主动推送通知时，SSE 是最简单的选择。

---

## 四、MCP Client 开发

### 4.1 基础 Client 连接

```python
import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client
from mcp.types import AnyUrl

server_params = {"command": "python", "args": ["my_mcp_server.py"]}

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 1. 初始化连接
            await session.initialize()

            # 2. 列出可用工具
            tools = await session.list_tools()
            print(f"可用工具: {[t.name for t in tools.tools]}")

            # 3. 调用工具
            result = await session.call_tool("add", arguments={"a": 5, "b": 3})
            print(f"工具结果: {result.structuredContent}")

            # 4. 列出资源模板
            templates = await session.list_resource_templates()
            for t in templates.resourceTemplates:
                print(f"  - {t.uriTemplate}")

            # 5. 读取资源
            content = await session.read_resource(AnyUrl("greeting://World"))
            print(f"资源内容: {content.contents[0].text}")

            # 6. 获取提示
            prompt = await session.get_prompt(
                "greet_user",
                arguments={"name": "张三", "style": "formal"}
            )
            print(f"提示内容: {prompt.messages[0].content}")

asyncio.run(run())
```

### 4.2 采样（Sampling）机制

采样是 MCP 中 Server 反向请求 Client 侧 LLM 生成能力的机制。这是 MCP 的独特设计——传统 Client-Server 模型中 Server 不请求 Client 的资源，但 MCP 允许这种反向模式。

**使用场景**：

*   Server 需要 LLM 来总结检索结果
*   Server 需要 LLM 对工具输出进行后处理
*   Server 需要 LLM 生成自然语言提示

```python
from mcp.types import CreateMessageRequestParams, CreateMessageResult

async def handle_sampling(context, params: CreateMessageRequestParams) -> CreateMessageResult:
    llm_response = await my_llm.generate(params.messages)
    return CreateMessageResult(
        role="assistant",
        content=TextContent(type="text", text=llm_response),
        model="gpt-4o",
        stopReason="endTurn",
    )

async with ClientSession(read, write, sampling_callback=handle_sampling) as session:
    await session.initialize()
```

### 4.3 Task 模式（异步长任务）

对于执行时间可能很长的操作（如大文件处理、批量数据分析），MCP 提供了 Task 机制——将同步调用转为异步任务，支持状态轮询。

```python
# 创建异步任务
result = await session.experimental.call_tool_as_task(
    "long_running_operation", {"data": "..."}
)
task_id = result.task.taskId

# 轮询任务状态
async for status in session.experimental.poll_task(task_id):
    print(f"任务状态: {status.status}")
    if status.status == "input_required":
        # 处理需要用户输入的场景
        final = await session.experimental.get_task_result(task_id)
        break
    elif status.status == "completed":
        final = await session.experimental.get_task_result(task_id)
        break
```

**Task 状态机**：

```
created → running → (input_required → running)* → completed
                   ↘ failed
```

---

## 五、MCP 安全模型

### 5.1 OAuth 2.1 认证

MCP Server 可以作为 OAuth 2.1 的 Resource Server（RS），由独立的 Authorization Server（AS）管理认证：

```python
from mcp.server.auth.provider import AccessToken, TokenVerifier
from mcp.server.auth.settings import AuthSettings
from mcp.server.fastmcp import FastMCP
from pydantic import AnyHttpUrl

class SimpleTokenVerifier(TokenVerifier):
    async def verify_token(self, token: str) -> AccessToken | None:
        # 在此实现实际的 token 验证逻辑
        # 验证 JWT 签名、过期时间、scope 等
        pass

mcp = FastMCP(
    "Weather Service",
    json_response=True,
    token_verifier=SimpleTokenVerifier(),
    auth=AuthSettings(
        issuer_url=AnyHttpUrl("https://auth.example.com"),
        resource_server_url=AnyHttpUrl("http://localhost:3001"),
        required_scopes=["user"],
    ),
)
```

### 5.2 Client 侧 OAuth 流程

```python
from mcp.client.auth import OAuthClientProvider, TokenStorage

class InMemoryTokenStorage(TokenStorage):
    def __init__(self):
        self.tokens = None
    async def get_tokens(self):
        return self.tokens
    async def set_tokens(self, tokens):
        self.tokens = tokens

oauth_auth = OAuthClientProvider(
    server_url="http://localhost:8001",
    client_metadata=OAuthClientMetadata(...),
    storage=InMemoryTokenStorage(),
    redirect_handler=handle_redirect,
    callback_handler=handle_callback,
)

async with httpx.AsyncClient(auth=oauth_auth) as client:
    async with streamable_http_client(url, http_client=client) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
```

### 5.3 安全架构层级

```
┌──────────────────────────┐
│     身份认证 (OAuth)      │  ← 你是谁？
├──────────────────────────┤
│     权限控制 (Scopes)     │  ← 你能做什么？
├──────────────────────────┤
│     传输加密 (TLS/HTTPS)  │  ← 防止窃听
├──────────────────────────┤
│     输入验证 (Pydantic)   │  ← 防止注入
├──────────────────────────┤
│     资源隔离 (Sandbox)    │  ← 限制影响范围
└──────────────────────────┘
```

---

## 六、工具调用进阶

### 6.1 工具注册表模式

```python
class ToolRegistry:
    """中心化工具注册与发现"""

    def __init__(self):
        self._tools: dict[str, callable] = {}
        self._schemas: dict[str, dict] = {}

    def register(self, func: callable, schema: dict = None):
        """注册工具，自动推断 JSON Schema"""
        self._tools[func.__name__] = func
        self._schemas[func.__name__] = schema or self._infer_schema(func)

    def list_tools(self) -> list[dict]:
        return [{"name": name, "schema": schema}
                for name, schema in self._schemas.items()]

    def invoke(self, name: str, args: dict):
        if name not in self._tools:
            raise ValueError(f"未知工具: {name}")
        return self._tools[name](**args)

registry = ToolRegistry()
registry.register(search_web)
registry.register(get_weather)
```

### 6.2 安全的工具执行器

```python
class SafeToolExecutor:
    def __init__(self, allowed_tools: set[str], max_timeout: int = 30):
        self.allowed_tools = allowed_tools
        self.max_timeout = max_timeout

    def execute(self, tool_name: str, args: dict):
        # 1. 白名单校验
        if tool_name not in self.allowed_tools:
            raise PermissionError(f"工具 {tool_name} 不在允许列表中")

        # 2. 参数校验
        self._validate_args(tool_name, args)

        # 3. 超时控制
        with timeout(self.max_timeout):
            return self._invoke(tool_name, args)

    def _validate_args(self, tool_name: str, args: dict):
        for key, value in args.items():
            if isinstance(value, str) and len(value) > 10000:
                raise ValueError(f"参数 {key} 过长")
```

### 6.3 并行工具调用

当 LLM 在一次响应中返回多个 tool\_calls 时，这些工具调用通常是相互独立的（无数据依赖），可以并行执行：

```python
import asyncio

async def parallel_tool_execution(tool_calls: list):
    """并行执行多个独立工具调用，显著降低延迟"""
    async def execute_one(call):
        tool = tools_by_name[call["name"]]
        return await tool.ainvoke(call["args"])

    results = await asyncio.gather(*[execute_one(c) for c in tool_calls])
    return results
```

**何时并行**：工具间无数据依赖时 **何时串行**：工具 A 的输出是工具 B 的输入时

---

## 七、Skill 概念与实现

### 7.1 Skill 的定位：能力封装单元

Skill 是比 Tool 更高层次的抽象——它将完成特定任务所需的所有资源打包为一个可组合的单元：

| 维度 | Tool | Skill |
| --- | --- | --- |
| **粒度** | 原子操作 | 组合能力 |
| **组成** | 单个函数 | Tools + Prompts + Instructions + 逻辑 |
| **复用单位** | 函数级 | 模块级 |
| **认知负载** | LLM 需理解每个 Tool | LLM 只需理解 Skill 的"是什么" |

### 7.2 Skill 架构实现

```python
class Skill:
    """Skill 基类——能力的模块化封装"""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def get_tools(self) -> list:
        raise NotImplementedError

    def get_prompts(self) -> list:
        raise NotImplementedError

    def get_instructions(self) -> str:
        raise NotImplementedError


class CodeReviewSkill(Skill):
    """代码审查 Skill——将代码审查能力封装为独立模块"""

    def __init__(self):
        super().__init__("code-review", "执行多维度代码审查")

    def get_tools(self):
        return [
            static_analysis_tool,
            security_scan_tool,
            dependency_check_tool,
        ]

    def get_prompts(self):
        return [code_review_prompt, security_audit_prompt]

    def get_instructions(self):
        return """
审查流程：
1. 静态分析（语法树检查、复杂度计算）
2. 安全扫描（注入漏洞、硬编码密钥）
3. 依赖审查（版本过期、已知漏洞）
4. 风格检查（命名规范、代码格式）
5. 生成结构化的审查报告
        """
```

### 7.3 Skill 的加载与组合

Agent 可以动态加载不同的 Skill 组合，根据任务类型激活对应的能力集。Skill 之间的组合遵循"高内聚、低耦合"原则——每个 Skill 独立工作，通过共享的工具注册表或 MCP 协议进行交互。

---

## 八、MCP 在企业架构中的定位

### 8.1 分层架构

```
┌─────────────────────────────────────────────────┐
│              AI 应用层（Agent 编排）               │
│     ┌─────────┐  ┌──────────┐  ┌──────────┐    │
│     │Agent A  │  │ Agent B  │  │ Agent C  │    │
│     └────┬────┘  └────┬─────┘  └────┬─────┘    │
│          │             │              │          │
├──────────┼─────────────┼──────────────┼─────────┤
│          │       MCP Client Layer               │
│          │       (标准 JSON-RPC)                 │
├──────────┼─────────────┼──────────────┼─────────┤
│          │             │              │          │
│   ┌──────┴───┐  ┌──────┴───┐  ┌──────┴───┐    │
│   │MCP Server│  │MCP Server│  │MCP Server│    │
│   │ (搜索)   │  │ (数据库) │  │ (文件)   │    │
│   └──────────┘  └──────────┘  └──────────┘    │
│                                                 │
│          MCP Server 层（工具/数据源）             │
└─────────────────────────────────────────────────┘
```

### 8.2 MCP 带来的架构优势

| 特性 | 传统方式 | MCP 方式 |
| --- | --- | --- |
| **集成成本** | O(M×N) 自定义适配 | O(M+N) 标准接口 |
| **服务发现** | 硬编码工具列表 | 动态 list\_tools() |
| **版本管理** | 无标准化方案 | initialize 协商版本 |
| **安全模型** | 各自实现 | 统一的 OAuth 2.1 + Scopes |
| **传输方式** | 厂商自定义 | stdio/HTTP/SSE 标准切换 |
| **工具复用** | 紧耦合 | 松耦合，独立部署 |

### 8.3 何时为工具创建 MCP Server

**应该**创建 MCP Server：

*   工具被多个 Agent 或应用共享
*   工具需要独立部署和扩缩容
*   工具有独立的认证授权需求
*   工具由不同团队开发维护

**暂时不需要**创建 MCP Server：

*   工具仅被单个 Agent 使用
*   工具逻辑简单（几行代码的计算函数）
*   处于原型验证阶段

## 相关条目
- [[Agent搭建]]
- [[面试]]
- [[12-mcp-xie-yi-ji-cheng]]
