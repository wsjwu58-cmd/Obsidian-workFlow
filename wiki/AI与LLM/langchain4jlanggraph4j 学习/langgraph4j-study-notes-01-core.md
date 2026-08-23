# langgraph4j-study-notes-01-core
## LangGraph4j 核心概念学习笔记 (一)

> 基于项目 `oj-microservice` 实战 + 官方文档整理  
> 版本: `1.8.11` | JDK 17+

---

## 1\. LangGraph4j 概述

LangGraph4j 是 LangGraph 的 Java 实现，用于构建 **带状态的、多 Agent 协作** 的 LLM 应用。核心理念是将 Agent 工作流建模为 **有向图 (DAG)**：

```
每个"节点" = 一个处理步骤 (Agent/工具调用)
每个"边" = 状态流转方向
"状态" = 在节点间传递的共享数据
```

---

## 2\. AgentState —— 图状态

### 2.1 概念

`AgentState` 是所有节点间共享的数据容器，通过 `Channel` 定义字段的类型和默认值。

### 2.2 项目实战 —— OJAgentState

项目中定义了完整的多 Agent 协作状态：

```jsp
// oj-ai-service/src/main/java/com/oj/ai/service/agent/graph/OJAgentState.java
public class OJAgentState extends AgentState {

    // 定义 Channel 键名
    public static final String USER_ID = "userId";
    public static final String SESSION_ID = "sessionId";
    public static final String TASK = "task";
    public static final String PROBLEM_ID = "problemId";
    public static final String ROUTING_RESULT = "routingResult";
    public static final String SOLUTION_RESULT = "solutionResult";
    public static final String CODE_RESULT = "codeResult";
    public static final String LEARNING_RESULT = "learningResult";
    public static final String KNOWLEDGE_RESULT = "knowledgeResult";
    public static final String FINAL_RESPONSE = "finalResponse";
    public static final String NEXT = "next";           // 控制流转方向

    // 定义 Schema：每个字段的类型和默认值
    public static final Map<String, Channel<?>> SCHEMA;

    static {
        Map<String, Channel<?>> schemaMap = new HashMap<>();
        schemaMap.put(USER_ID, Channels.base(() -> 0L));
        schemaMap.put(SESSION_ID, Channels.base(() -> "default"));
        schemaMap.put(TASK, Channels.base(() -> ""));
        schemaMap.put(PROBLEM_ID, Channels.base(() -> 0));
        schemaMap.put(CURRENT_AGENT, Channels.base(() -> "router"));
        schemaMap.put(ROUTING_RESULT, Channels.base(() -> ""));
        schemaMap.put(SOLUTION_RESULT, Channels.base(() -> ""));
        schemaMap.put(CODE_RESULT, Channels.base(() -> ""));
        schemaMap.put(LEARNING_RESULT, Channels.base(() -> ""));
        schemaMap.put(KNOWLEDGE_RESULT, Channels.base(() -> ""));
        schemaMap.put(FINAL_RESPONSE, Channels.base(() -> ""));
        schemaMap.put(NEXT, Channels.base(() -> ""));
        SCHEMA = Map.copyOf(schemaMap);
    }

    public OJAgentState(Map<String, Object> initData) {
        super(initData);
    }

    // 类型安全的访问器
    public Optional<Long> getUserId() {
        return value(USER_ID).map(obj -> ((Number) obj).longValue());
    }

    public String getTask() {
        return (String) value(TASK).orElse("");
    }

    public Optional<String> next() {
        return value(NEXT).map(Object::toString);
    }

    public String getFinalResponse() {
        return (String) value(FINAL_RESPONSE).orElse("");
    }
}
```

### 2.3 Channel 类型说明

| 方法 | 行为 | 适用场景 |
| --- | --- | --- |
| `Channels.base(() -> default)` | 直接覆盖，保留最后一个值 | 字符串、数字等单值字段 |
| `Channels.appender(ArrayList::new)` | 追加到列表末尾 | 消息历史、日志等累积数据 |

```jsp
// 单值 Channel —— 每个节点的新值会覆盖旧值
schemaMap.put("status", Channels.base(() -> "pending"));

// 追加 Channel —— 每个节点的新值会追加到列表
schemaMap.put("messages", Channels.appender(ArrayList::new));
```

---

## 3\. StateGraph —— 图构建器

### 3.1 概念

`StateGraph<S extends AgentState>` 是定义工作流的核心构建器。通过添加节点、边、条件边来构建图结构。

### 3.2 项目实战 —— 多 Agent 编排

```jsp
// oj-ai-service/src/main/java/com/oj/ai/service/agent/LangGraphAgentOrchestrator.java
@Service
public class LangGraphAgentOrchestrator {

    private final RouterAgent routerAgent;
    private final SolutionAgent solutionAgent;
    private final CodeJudgeAgent codeJudgeAgent;
    private final LearningAgent learningAgent;
    private final KnowledgeAgent knowledgeAgent;
    private final SupervisorAgent supervisorAgent;

    private CompiledGraph<OJAgentState> compiledGraph;

    @PostConstruct
    public void init() throws GraphStateException {
        StateGraph<OJAgentState> graph = buildGraph();

        CompileConfig config = CompileConfig.builder()
            .checkpointSaver(new MemorySaver())  // 内存检查点
            .build();

        this.compiledGraph = graph.compile(config);
    }

    private StateGraph<OJAgentState> buildGraph() throws GraphStateException {
        var builder = new StateGraph<>(OJAgentState.SCHEMA, OJAgentState::new);

        // 1. 添加节点：每个节点对应一个 Agent
        builder.addNode("router", node_async(routerAgent));
        builder.addNode("solution", node_async(solutionAgent));
        builder.addNode("code", node_async(codeJudgeAgent));
        builder.addNode("learning", node_async(learningAgent));
        builder.addNode("knowledge", node_async(knowledgeAgent));
        builder.addNode("supervisor", node_async(supervisorAgent));

        // 2. 添加入口边：START → router
        builder.addEdge(START, "router");

        // 3. 条件边：router 根据状态决定下一步
        AsyncEdgeAction<OJAgentState> routingCondition = state ->
            CompletableFuture.completedFuture(state.next().orElse("supervisor"));

        builder.addConditionalEdges("router", routingCondition,
            Map.of(
                "solution", "solution",
                "code", "code",
                "learning", "learning",
                "knowledge", "knowledge",
                "supervisor", "supervisor"
            ));

        // 4. 聚合边：所有 Agent 完成后都到 supervisor
        builder.addEdge("solution", "supervisor");
        builder.addEdge("code", "supervisor");
        builder.addEdge("learning", "supervisor");
        builder.addEdge("knowledge", "supervisor");

        // 5. 出口边：supervisor → END
        builder.addEdge("supervisor", END);

        return builder;
    }
}
```

### 3.3 图结构可视化

```
                        ┌──────────┐
                        │  START   │
                        └────┬─────┘
                             │
                             ▼
                        ┌──────────┐
                        │  router  │ (意图识别)
                        └────┬─────┘
                             │ 条件分支
              ┌──────────────┼──────────────┬──────────────┐
              ▼              ▼              ▼              ▼
        ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
        │ solution │  │   code   │  │ learning │  │knowledge │
        └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘
              │              │              │              │
              └──────────────┼──────────────┼──────────────┘
                             │              │
                             ▼              ▼
                        ┌──────────┐
                        │supervisor│ (结果整合)
                        └────┬─────┘
                             │
                             ▼
                        ┌──────────┐
                        │   END    │
                        └──────────┘
```

### 3.4 图执行

```jsp
public String chat(String sessionId, String task, Long userId, Integer problemId) {
    // 初始状态
    Map<String, Object> initialState = Map.of(
        OJAgentState.SESSION_ID, sessionId,
        OJAgentState.TASK, task,
        OJAgentState.USER_ID, userId != null ? userId : 0L,
        OJAgentState.PROBLEM_ID, problemId != null ? problemId : 0
    );

    // 线程配置（threadId 用于 checkpoint 隔离）
    RunnableConfig config = RunnableConfig.builder()
        .threadId(sessionId)
        .build();

    // 执行图：invoke() 同步执行，stream() 流式执行
    Optional<OJAgentState> result = compiledGraph.invoke(initialState, config);

    return result.map(OJAgentState::getFinalResponse)
        .orElse("抱歉，处理您的请求时遇到了错误。");
}
```

---

## 4\. NodeAction —— 节点逻辑

### 4.1 概念

每个节点实现了 `NodeAction<S>` 接口，其 `apply()` 方法接收当前状态，返回需要更新的字段。

### 4.2 项目实战 —— RouterAgent（路由节点）

```jsp
// oj-ai-service/src/main/java/com/oj/ai/service/agent/specialized/RouterAgent.java
@Component
public class RouterAgent implements NodeAction<OJAgentState> {

    private final RoutingService routingService;

    @Autowired
    public RouterAgent(ChatModel chatModel) {
        // 使用 AiServices 创建轻量级路由服务
        this.routingService = AiServices.builder(RoutingService.class)
            .chatModel(chatModel)
            .build();
    }

    @Override
    public Map<String, Object> apply(OJAgentState state) {
        String task = state.getTask();
        String routingResult = routingService.route(task);

        // 解析路由结果为下一节点
        String nextAgent = determineNextAgent(routingResult);

        // 返回需要更新的状态字段
        return Map.of(
            OJAgentState.ROUTING_RESULT, routingResult,
            OJAgentState.CURRENT_AGENT, nextAgent,
            OJAgentState.NEXT, nextAgent       // 控制流转的字段
        );
    }

    private String determineNextAgent(String routingResult) {
        String lower = routingResult.toLowerCase();
        if (lower.contains("solution") || lower.contains("题解")) return "solution";
        if (lower.contains("code") || lower.contains("代码")) return "code";
        if (lower.contains("learning") || lower.contains("学习")) return "learning";
        if (lower.contains("knowledge") || lower.contains("知识")) return "knowledge";
        return "supervisor";
    }

    // 内嵌 AiService 接口
    public interface RoutingService {
        @SystemMessage("""
            你是一个意图识别助手，分析用户问题并确定最合适的处理Agent。
            可选Agent：solution(题解), code(代码分析), learning(学情分析), knowledge(知识检索)。
            只返回Agent名称。
            """)
        String route(@UserMessage String userMessage);
    }
}
```

### 4.3 项目实战 —— SupervisorAgent（聚合节点）

```jsp
// oj-ai-service/src/main/java/com/oj/ai/service/agent/specialized/SupervisorAgent.java
@Component
public class SupervisorAgent implements NodeAction<OJAgentState> {

    private final SupervisorService supervisorService;

    @Override
    public Map<String, Object> apply(OJAgentState state) {
        String task = state.getTask();

        // 收集所有子 Agent 的结果
        String solutionResult = state.getSolutionResult();
        String codeResult = state.getCodeResult();
        String learningResult = state.getLearningResult();
        String knowledgeResult = state.getKnowledgeResult();

        if (hasAnyResult(solutionResult, codeResult, learningResult, knowledgeResult)) {
            // 有子结果 → 整合生成最终回复
            StringBuilder context = new StringBuilder();
            context.append("用户任务：").append(task).append("\n\n各Agent处理结果：");
            if (!solutionResult.isEmpty()) context.append("\n【Solution】").append(solutionResult);
            if (!codeResult.isEmpty()) context.append("\n【Code】").append(codeResult);
            if (!learningResult.isEmpty()) context.append("\n【Learning】").append(learningResult);
            if (!knowledgeResult.isEmpty()) context.append("\n【Knowledge】").append(knowledgeResult);

            String finalResponse = supervisorService.summarize(context.toString());
            return Map.of(OJAgentState.FINAL_RESPONSE, finalResponse);
        } else {
            // 无子结果 → 直接回答
            String directResponse = supervisorService.summarizeSimple(task);
            return Map.of(OJAgentState.FINAL_RESPONSE, directResponse);
        }
    }

    public interface SupervisorService {
        @SystemMessage("你是OJ AI助手监督者，整合各Agent结果生成最终回复。")
        String summarize(@UserMessage String fullContext);

        @SystemMessage("你是OJ AI助手，直接回答用户问题。")
        String summarizeSimple(@UserMessage String userMessage);
    }
}
```

---

## 5\. EdgeAction —— 边逻辑

### 5.1 概念

`EdgeAction<S>` 用于条件边，根据状态决定跳转到哪个节点。返回值是目标节点的名称。

### 5.2 项目实战 —— 路由条件边

```jsp
// LangGraphAgentOrchestrator.java:80
AsyncEdgeAction<OJAgentState> routingCondition = state ->
    CompletableFuture.completedFuture(state.next().orElse("supervisor"));

builder.addConditionalEdges("router", routingCondition,
    Map.of(
        "solution", "solution",
        "code", "code",
        "learning", "learning",
        "knowledge", "knowledge",
        "supervisor", "supervisor"
    ));
```

### 5.3 官方文档拓展 —— 工具调用循环

典型的 Agent 模式：ChatModel → ToolCall → ChatModel → ... 直到不再需要工具：

```jsp
// 条件路由：检查最后一条消息是否需要工具调用
EdgeAction<MessageState> routeMessage = state -> {
    var lastMessage = state.lastMessage();
    if (!lastMessage.isPresent()) return "exit";

    if (lastMessage.get() instanceof AiMessage message) {
        if (message.hasToolExecutionRequests()) return "next"; // 需要调用工具
    }
    return "exit"; // 不需要工具，直接结束
};

// 图结构
var workflow = new StateGraph<>(MessageState.SCHEMA, stateSerializer)
    .addNode("agent", node_async(callModel))
    .addNode("tools", node_async(invokeTool))
    .addEdge(START, "agent")
    .addConditionalEdges("agent",
        edge_async(routeMessage),
        Map.of("next", "tools", "exit", END))
    .addEdge("tools", "agent");  // 工具调用后回到 agent
```

---

## 6\. 同步 vs 异步 Action

| 类型 | 接口 | 返回类型 | 使用方式 |
| --- | --- | --- | --- |
| 同步节点 | `NodeAction<S>` | `Map<String,Object>` | `.addNode("n", action)` |
| 异步节点 | `AsyncNodeAction<S>` | `CompletableFuture<Map>` | `.addNode("n", node_async(action))` |
| 同步边 | `EdgeAction<S>` | `String` | `.addConditionalEdges(..., action, ...)` |
| 异步边 | `AsyncEdgeAction<S>` | `CompletableFuture<String>` | `.addConditionalEdges(..., edge_async(action), ...)` |

项目使用异步版本以获得更好的并发性能：

```jsp
import static org.bsc.langgraph4j.action.AsyncNodeAction.node_async;
import static org.bsc.langgraph4j.action.AsyncEdgeAction.edge_async;

builder.addNode("router", node_async(routerAgent));
builder.addConditionalEdges("router", edge_async(routingCondition), ...);
```

---

## 7\. 完整的工作流数据流

```
用户输入: "题目123的解题思路是什么？"

  ┌─────────────────────────────────────────────────────────────┐
  │ OJAgentState                                                │
  │   task = "题目123的解题思路是什么？"                          │
  │   problemId = 123                                           │
  └──────────────┬──────────────────────────────────────────────┘
                 │
        ┌────────▼────────┐
        │  RouterAgent     │  → LLM 分析意图 → "solution"
        │  返回:           │
        │  routingResult   │  = "solution"
        │  next = "solution"│
        └────────┬────────┘
                 │
        ┌────────▼────────┐
        │  SolutionAgent   │  → 调用 getProblemDetail(123)
        │  返回:           │  → LLM 生成题解
        │  solutionResult  │  = "本题考察动态规划..."
        └────────┬────────┘
                 │
        ┌────────▼────────┐
        │  SupervisorAgent │  → 整合结果
        │  返回:           │
        │  finalResponse   │  = "## 题解\n本题考察..."
        └────────┬────────┘
                 │
           用户收到回答
```

---

## 8\. 官方文档拓展 —— 简化版 StateGraph

```jsp
import org.bsc.langgraph4j.StateGraph;
import static org.bsc.langgraph4j.StateGraph.START;
import static org.bsc.langgraph4j.StateGraph.END;
import static org.bsc.langgraph4j.action.AsyncNodeAction.node_async;
import static org.bsc.langgraph4j.action.AsyncEdgeAction.edge_async;

// 1. 定义状态
class MyState extends AgentState {
    public static final Map<String, Channel<?>> SCHEMA = Map.of(
        "messages", Channels.appender(ArrayList::new),
        "status",   Channels.base(() -> "pending")
    );
    public MyState(Map<String, Object> data) { super(data); }
    public List<String> messages() { return this.<List<String>>value("messages").orElse(List.of()); }
}

// 2. 构建和编译图
var graph = new StateGraph<>(MyState.SCHEMA, MyState::new)
    .addNode("fetch",  node_async(state -> Map.of("messages", "fetched")))
    .addNode("process", node_async(state -> Map.of("messages", "processed", "status", "done")))
    .addNode("error",  node_async(state -> Map.of("status", "error")))
    .addEdge(START, "fetch")
    .addConditionalEdges("fetch",
        edge_async(state -> state.messages().contains("fetched") ? "ok" : "fail"),
        Map.of("ok", "process", "fail", "error"))
    .addEdge("process", END)
    .addEdge("error", END);

var compiled = graph.compile();

// 3. 执行
var result = compiled.invoke(Map.of("messages", "start"));
result.ifPresent(s -> System.out.println("Status: " + s.status()));
```

---

上一篇：[LangChain4j 进阶](./langchain4j-study-notes-03-advanced.md)  
下一篇：[LangGraph4j 进阶](./langgraph4j-study-notes-02-advanced.md)

## 相关条目
- [[langgraph4j-study-notes-02-advanced]]
- [[langchain4j-study-notes-01-core]]
- [[Agent搭建]]
