# langgraph4j-study-notes-02-advanced
## LangGraph4j 进阶学习笔记 (二)

> 基于项目 `oj-microservice` 实战 + 官方文档整理  
> 版本: `1.8.11` | JDK 17+

---

## 1\. Checkpoint —— 状态持久化与回放

### 1.1 概念

Checkpoint（检查点）是 LangGraph4j 的关键特性。每个节点执行后自动保存当前状态快照，支持：

*   **暂停/恢复**：人工介入后继续执行
*   **时间旅行**：回放历史状态
*   **断点续传**：服务重启后从上次中断处继续

### 1.2 项目实战 —— MemorySaver

```jsp
// oj-ai-service: LangGraphAgentOrchestrator.java:57
private final MemorySaver checkpointSaver = new MemorySaver();

@PostConstruct
public void init() throws GraphStateException {
    CompileConfig config = CompileConfig.builder()
        .checkpointSaver(checkpointSaver)  // 内存检查点
        .build();

    this.compiledGraph = graph.compile(config);
}
```

图执行时通过 `threadId` 区分不同会话的检查点：

```jsp
RunnableConfig config = RunnableConfig.builder()
    .threadId(sessionId)   // 不同 session 的 checkpoint 互相隔离
    .build();

compiledGraph.invoke(initialState, config);
```

### 1.3 官方文档拓展 —— Human-in-the-Loop

通过 `interruptBefore` 在关键节点前暂停，等待人工确认：

```jsp
var saver = new MemorySaver();

var compileConfig = CompileConfig.builder()
    .checkpointSaver(saver)
    .interruptBefore("approve")   // 在 "approve" 节点前暂停
    .build();

var graph = new StateGraph<>(AgentState::new)
    .addNode("prepare", node_async(s -> Map.of("prepared", true)))
    .addNode("approve",  node_async(s -> Map.of("approved", true)))
    .addNode("finalize", node_async(s -> Map.of("finalized", true)))
    .addEdge(START, "prepare")
    .addEdge("prepare", "approve")
    .addEdge("approve", "finalize")
    .addEdge("finalize", END)
    .compile(compileConfig);

var config = RunnableConfig.builder().threadId("workflow-1").build();

// Step 1: 执行到 "approve" 前暂停
for (var out : graph.stream(Map.of("request", "process-me"), config)) {
    System.out.println("Yielded at: " + out.node());
}

// Step 2: 检查当前状态
StateSnapshot<AgentState> snap = graph.getState(config);
System.out.println("Next node: " + snap.next()); // → "approve"

// Step 3: 人工批准后更新状态并恢复
graph.updateState(config, Map.of("humanApproval", "granted"), "approve");

// Step 4: 继续执行
for (var out : graph.stream(null, config)) {
    System.out.println("Resumed at: " + out.node());
}
```

### 1.4 时间旅行

```jsp
// 查看完整的历史状态快照
for (var snapshot : graph.getStateHistory(config)) {
    System.out.println(snapshot.node() + " → next: " + snapshot.next());
}
```

---

## 2\. AgentExecutor —— 开箱即用的 Agent 模式

### 2.1 概念

`AgentExecutor` 是 langgraph4j-agent-executor 模块提供的预构建 Agent 模式，封装了 **LLM 调用 → 工具执行 → 循环** 的标准 ReAct 模式。

### 2.2 依赖

```xml
<!-- oj-ai-service/pom.xml -->
<dependency>
    <groupId>org.bsc.langgraph4j</groupId>
    <artifactId>langgraph4j-agent-executor</artifactId>
</dependency>
```

### 2.3 官方文档示例

```jsp
import org.bsc.langgraph4j.agentexecutor.AgentExecutor;
import dev.langchain4j.agent.tool.Tool;
import dev.langchain4j.agent.tool.P;

// 定义工具
public class TestTool {
    private String lastResult;

    @Tool("tool for test AI agent executor")
    String execTest(@P("test message") String message) {
        lastResult = "test tool executed: " + message;
        return lastResult;
    }
}

// 构建 AgentExecutor
var agentExecutor = AgentExecutor.builder()
    .chatModel(chatModel)
    .toolsFromObject(new TestTool())                       // 扫描 @Tool 方法
    .tool(toolSpecification, toolExecutor)                 // 手动注册工具
    .build();

// 编译为 LangGraph4j 图
var workflow = agentExecutor.compile();

// 流式执行
var iterator = workflow.stream(
    Map.of("messages", UserMessage.from("Run my test!"))
);

for (var step : iterator) {
    System.out.println(step);
}
```

### 2.4 AgentExecutor 内部结构

AgentExecutor 自动构建的图：

```
START → agent (LLM 调用)
         │
    ┌────▼────┐
    │ 条件路由  │ ← 检查是否有 toolExecutionRequests
    └────┬────┘
         │
    ┌────▼────┐
    │  tools  │ (工具执行) → agent (循环)
    └────┬────┘
         │
        END  (无工具调用时退出)
```

---

## 3\. LangGraph4j + LangChain4j 深度集成

### 3.1 概念

`langgraph4j-langchain4j` 桥接模块提供了：

*   `LC4jToolService`：在 LangGraph4j 节点中调用 LangChain4j 的 `@Tool` 方法
*   `LC4jStateSerializer`：LangChain4j 消息的序列化支持
*   `MessagesState`：预构建的消息状态

### 3.2 依赖

```xml
<dependency>
    <groupId>org.bsc.langgraph4j</groupId>
    <artifactId>langgraph4j-langchain4j</artifactId>
</dependency>
```

### 3.3 官方文档示例 —— Agent + Tool 循环

```jsp
import org.bsc.langgraph4j.prebuilt.MessagesStateGraph;
import org.bsc.langgraph4j.langchain4j.tool.LC4jToolService;
import org.bsc.langgraph4j.langchain4j.serializer.LC4jStateSerializer;

// 使用 LC4jToolService 包装 LangChain4j 工具
var tools = LC4jToolService.builder()
    .toolsFromObject(new SearchTool())
    .build();

// 节点：调用 LLM
NodeAction<MessagesState<ChatMessage>> callModel = state -> {
    var request = ChatRequest.builder()
        .parameters(ChatRequestParameters.builder()
            .toolSpecifications(tools.toolSpecifications())
            .build())
        .messages(state.messages())
        .build();

    var response = model.chat(request);
    return Map.of("messages", response.aiMessage());
};

// 节点：执行工具
AsyncNodeAction<MessagesState<ChatMessage>> invokeTool = state -> {
    var lastMessage = (AiMessage) state.lastMessage().get();
    return tools.execute(lastMessage.toolExecutionRequests(),
            InvocationContext.builder().build(), "messages")
        .thenApply(result -> result.update());
};

// 边：路由决策
EdgeAction<MessagesState<ChatMessage>> routeMessage = state -> {
    var lastMessage = state.lastMessage();
    if (lastMessage.get() instanceof AiMessage msg && msg.hasToolExecutionRequests())
        return "next";
    return "exit";
};

// 构建图
var stateSerializer = new LC4jStateSerializer<>(State::new);
var workflow = new MessagesStateGraph<ChatMessage>(stateSerializer)
    .addNode("agent", node_async(callModel))
    .addNode("tools", invokeTool)
    .addEdge(START, "agent")
    .addConditionalEdges("agent",
        edge_async(routeMessage),
        Map.of("next", "tools", "exit", END))
    .addEdge("tools", "agent");

// 编译（带 checkpoint）
var compileConfig = CompileConfig.builder()
    .checkpointSaver(new MemorySaver())
    .releaseThread(false)  // 完成后不释放线程
    .build();

var graph = workflow.compile(compileConfig);
```

---

## 4\. LangGraph Studio —— 可视化调试

### 4.1 概念

LangGraph Studio 是一个嵌入式的 Web UI，用于可视化和调试 Agent 图。可以：

*   查看图的拓扑结构
*   实时追踪状态流转
*   手动触发节点执行
*   检查每个节点的输入输出

### 4.2 依赖

```xml
<dependency>
    <groupId>org.bsc.langgraph4j</groupId>
    <artifactId>langgraph4j-studio-springboot</artifactId>
</dependency>
```

### 4.3 项目实战 —— AgentStudioConfig

```jsp
// oj-ai-service/src/main/java/com/oj/ai/config/AgentStudioConfig.java
@Configuration
public class AgentStudioConfig extends LangGraphStudioConfig {

    @Autowired
    private LangGraphAgentOrchestrator orchestrator;

    @Override
    public Map<String, LangGraphStudioServer.Instance> instanceMap() {
        LangGraphStudioServer.Instance instance = LangGraphStudioServer.Instance.builder()
            .title("OJ AI Agent")
            .graph(orchestrator.getStateGraph())  // 暴露 StateGraph
            .build();

        return Map.of("oj-agent", instance);  // 注册名为 "oj-agent" 的实例
    }
}
```

启动后访问内置的 Studio UI，可以看到 Agent 图的完整结构和执行路径。

### 4.4 官方文档拓展 —— 带参数的 Studio 配置

```jsp
@Configuration
public class LangGraphStudioConfiguration extends LangGraphStudioConfig {

    @Override
    public Map<String, LangGraphStudioServer.Instance> instanceMap() {
        return Map.of("sample", LangGraphStudioServer.Instance.builder()
            .title("LangGraph Studio Demo")
            .addInputStringArg("messages", true,
                v -> new UserMessage(Objects.toString(v)))
            .graph(workflow)
            .compileConfig(CompileConfig.builder()
                .checkpointSaver(new MemorySaver())
                .releaseThread(true)
                .build())
            .build());
    }
}
```

---

## 5\. 流式执行

### 5.1 `invoke()` vs `stream()` vs `streamSnapshots()`

| 方法 | 返回 | 说明 |
| --- | --- | --- |
| `invoke(input)` | `Optional<State>` | 同步执行，返回最终状态 |
| `stream(input)` | `Iterator<NodeOutput>` | 流式执行，每步返回节点输出 |
| `streamSnapshots(input)` | `Iterator<StateSnapshot>` | 流式执行，每步返回完整状态快照 |

### 5.2 使用示例

```jsp
// 流式执行 —— 实时获取每个节点的输出
for (var step : compiledGraph.stream(initialState, config)) {
    System.out.println("Node: " + step.node());
    System.out.println("State: " + step.state());
}

// 流式快照 —— 获取完整状态（含 checkpoint 元数据）
for (var snapshot : compiledGraph.streamSnapshots(initialState, config)) {
    System.out.println("Node: " + snapshot.node());
    System.out.println("Next: " + snapshot.next());
    System.out.println("Values: " + snapshot.values());
}
```

---

## 6\. 项目依赖总览

```xml
<!-- oj-ai-service/pom.xml 中的 LangGraph4j 完整依赖 -->

<!-- 核心 -->
<dependency>
    <groupId>org.bsc.langgraph4j</groupId>
    <artifactId>langgraph4j-core</artifactId>
</dependency>

<!-- LangChain4j 桥接 -->
<dependency>
    <groupId>org.bsc.langgraph4j</groupId>
    <artifactId>langgraph4j-langchain4j</artifactId>
</dependency>

<!-- 预构建 Agent Executor -->
<dependency>
    <groupId>org.bsc.langgraph4j</groupId>
    <artifactId>langgraph4j-agent-executor</artifactId>
</dependency>

<!-- Studio 可视化 -->
<dependency>
    <groupId>org.bsc.langgraph4j</groupId>
    <artifactId>langgraph4j-studio-springboot</artifactId>
</dependency>
```

---

## 7\. 多 Agent 模式总结

| 模式 | 描述 | 项目应用 |
| --- | --- | --- |
| **Router → Specialists** | 路由节点分发到不同专家节点 | OJ 系统的意图路由（题解/判题/学习/知识） |
| **Supervisor 聚合** | 专家节点结果汇聚到监督节点整合 | SupervisorAgent 整合所有子 Agent 结果 |
| **ReAct 循环** | LLM ↔ 工具循环调用直到完成 | AgentExecutor 预构建模式 |
| **Human-in-the-Loop** | 在关键节点暂停等待人工决策 | 通过 `interruptBefore` 实现 |

### 7.1 项目的完整架构

```
oj-microservice AI 服务架构
│
├── LangChain4j (基础 LLM 调用)
│   ├── ChatModel / StreamingChatModel (Qwen/Qwen3-Coder)
│   ├── AiServices (声明式 Agent)
│   ├── @Tool (工具注解)
│   ├── EmbeddingModel + EmbeddingStore (RAG)
│   ├── ChatMemory (Redis 持久化)
│   └── MCP (外部工具协议)
│
├── LangGraph4j (多 Agent 编排)
│   ├── StateGraph (工作流定义)
│   ├── NodeAction (6 个 Agent 节点)
│   ├── Conditional Edges (意图路由)
│   ├── MemorySaver (检查点)
│   └── Studio (可视化调试)
│
└── 前端交互
    ├── SSE 流式响应
    └── REST API (/user/agent/chat)
```

---

## 8\. 最佳实践

| 建议 | 原因 |
| --- | --- |
| 使用 `node_async()` 包装 NodeAction | 更好的并发性能 |
| 为每个会话使用独立 `threadId` | Checkpoint 隔离，避免状态混淆 |
| 生产环境替换 InMemoryEmbeddingStore | 推荐 PgVector/Redis/Elasticsearch |
| 工具描述尽量详细 | LLM 依赖描述来决定是否调用工具 |
| 使用 ChatMemoryProvider 而非全局 Memory | 多用户对话隔离 |
| 通过 MCP 扩展外部工具 | 解耦工具实现，便于独立维护和扩展 |

---

上一篇：[LangGraph4j 核心概念](./langgraph4j-study-notes-01-core.md)

## 相关条目
- [[langgraph4j-study-notes-01-core]]
- [[多智能体与记忆机制]]
