# langchain4j-study-notes-03-advanced
## LangChain4j 进阶学习笔记 (三)

> 基于项目 `oj-microservice` 实战 + 官方文档整理  
> 版本: `1.12.2` | JDK 17+

---

## 1\. MCP (Model Context Protocol) 集成

### 1.1 概念

MCP 是一种标准化协议，让 LLM 可以通过统一接口调用外部工具和数据源。LangChain4j 的 `langchain4j-mcp` 模块提供了完整的 MCP 客户端支持。

### 1.2 项目实战 —— Bing 搜索集成

```jsp
// oj-ai-service/src/main/java/com/oj/ai/config/McpClientConfiguration.java
@Configuration
@Slf4j
public class McpClientConfiguration {

    @Value("${oj.mcp.bing-search.enabled:false}")
    private boolean bingSearchEnabled;

    @Bean
    @ConditionalOnProperty(name = "oj.mcp.bing-search.enabled", havingValue = "true")
    public McpClient bingSearchMcpClient() {
        // 通过 stdio 协议启动外部 MCP Server (Node.js)
        List<String> command = List.of("npx.cmd", "bing-cn-mcp-enhanced");

        McpTransport transport = new StdioMcpTransport.Builder()
            .command(command)
            .logEvents(true)
            .build();

        McpClient mcpClient = new DefaultMcpClient.Builder()
            .transport(transport)
            .build();

        return mcpClient;
    }

    @Bean
    public ToolProvider mcpToolProvider(List<McpClient> mcpClients) {
        return new McpToolProvider.Builder()
            .mcpClients(mcpClients)
            .failIfOneServerFails(false)  // 单个失败不影响整体
            .build();
    }

    @PreDestroy
    public void cleanup() {
        for (McpClient client : mcpClients) {
            client.close();  // 释放资源
        }
    }
}
```

在 `AgentService` 中集成 MCP 工具：

```jsp
// 可选注入（当 MCP 启用时）
@Autowired(required = false)
@Qualifier("mcpToolProvider")
public void setMcpToolProvider(ToolProvider mcpToolProvider) {
    this.mcpToolProvider = mcpToolProvider;
}

// 构建时条件注入
if (mcpToolProvider != null) {
    agentAssistant = AiServices.builder(AgentAssistant.class)
        .chatModel(chatModel)
        .toolProvider(mcpToolProvider)  // 动态工具
        .tools(localTools...)          // 静态工具
        .build();
}
```

### 1.3 官方文档拓展 —— 多种传输方式

```jsp
// 方式一：Stdio（启动本地进程）
McpTransport transport = StdioMcpTransport.builder()
    .command(List.of("/usr/bin/npm", "exec", "@modelcontextprotocol/server-everything@0.6.2"))
    .logEvents(true)
    .build();

// 方式二：HTTP SSE（远程服务器）
McpTransport transport = StreamableHttpMcpTransport.builder()
    .url("http://localhost:3001/mcp")
    .logRequests(true)
    .logResponses(true)
    .build();

// 方式三：WebSocket
McpTransport transport = WebSocketMcpTransport.builder()
    .url("ws://localhost:3001/mcp/ws")
    .build();

// 方式四：Docker 容器
McpTransport transport = DockerMcpTransport.builder()
    .image("mcp/time")
    .dockerHost("unix:///var/run/docker.sock")
    .build();
```

### 1.4 MCP 架构

```
┌─────────────────────────────────────────────────────┐
│                   Spring Boot App                     │
│  ┌─────────────┐    ┌───────────────────────────┐   │
│  │ AiServices   │◀───│ McpToolProvider           │   │
│  │ (Agent)      │    │  ├── McpClient (Bing)     │   │
│  └─────────────┘    │  ├── McpClient (Github)   │   │
│                      │  └── McpClient (...)      │   │
│                      └───────────┬───────────────┘   │
└──────────────────────────────────┼──────────────────┘
                                   │ Stdio/HTTP/WS
                                   ▼
┌──────────────────────────────────────────────────────┐
│                MCP Servers (外部进程)                  │
│  ┌──────────────┐  ┌────────────┐  ┌─────────────┐  │
│  │ Bing Search  │  │  Github    │  │  Filesystem │  │
│  │ (Node.js)    │  │  (Node.js) │  │  (Python)   │  │
│  └──────────────┘  └────────────┘  └─────────────┘  │
└──────────────────────────────────────────────────────┘
```

---

## 2\. Spring Boot Starter 自动配置

### 2.1 依赖

```xml
<!-- oj-ai-service/pom.xml -->
<dependency>
    <groupId>dev.langchain4j</groupId>
    <artifactId>langchain4j-open-ai-spring-boot-starter</artifactId>
</dependency>
<dependency>
    <groupId>dev.langchain4j</groupId>
    <artifactId>langchain4j-reactor</artifactId>
</dependency>
```

### 2.2 自动配置原理

Spring Boot Starter 会根据 `application.yml` 配置自动创建 Bean：

```yaml
langchain4j:
  open-ai:
    chat-model:
      api-key: sk-xxx
      model-name: gpt-4o-mini            # → ChatModel Bean
    streaming-chat-model:
      api-key: sk-xxx
      model-name: gpt-4o-mini            # → StreamingChatModel Bean
    embedding-model:
      api-key: sk-xxx
      model-name: text-embedding-3-small # → EmbeddingModel Bean
```

注入后可直接使用：

```jsp
@Autowired private ChatModel chatModel;
@Autowired private StreamingChatModel streamingChatModel;
@Autowired private EmbeddingModel embeddingModel;
```

---

## 3\. SSE 流式响应实战

### 3.1 项目完整流程

项目中使用 Spring MVC 的 `SseEmitter` 实现服务端推送：

```jsp
// Controller 层
@GetMapping("/chat/stream")
public SseEmitter chatStream(@RequestParam String sessionId, @RequestParam String message) {
    return agentService.processAgentRequestStream(request);
}

// Service 层
public Flux<String> chatStream(String sessionId, String message) {
    return agentAssistant.chatStream(sessionId, message);
}
```

底层 `RAGServiceImpl` 使用线程池 + `StreamingChatResponseHandler` 实现：

```jsp
private final ExecutorService executor = Executors.newCachedThreadPool();

public SseEmitter chatWithKnowledge(AiChatDTO dto) {
    SseEmitter emitter = new SseEmitter(120_000L); // 2分钟超时

    executor.execute(() -> {
        try {
            // 知识检索...
            // 构建消息...

            streamingChatModel.chat(request, new StreamingChatResponseHandler() {
                @Override
                public void onPartialResponse(String partialResponse) {
                    // 逐 Token 推送
                    emitter.send(SseEmitter.event().data(partialResponse));
                }
                @Override
                public void onCompleteResponse(ChatResponse completeResponse) {
                    emitter.complete();
                }
                @Override
                public void onError(Throwable error) {
                    emitter.completeWithError(error);
                }
            });
        } catch (Exception e) {
            emitter.completeWithError(e);
        }
    });

    return emitter;
}
```

### 3.2 前端 SSE 接收

```javascript
// Vue 3 前端示例
const eventSource = new EventSource('/api/user/agent/chat/stream?sessionId=' + sessionId);

eventSource.onmessage = (event) => {
    responseText.value += event.data;  // 逐字追加显示
};

eventSource.onerror = () => {
    eventSource.close();
};
```

---

## 4\. Redis ChatMemoryStore 深入

### 4.1 序列化机制

LangChain4j 内置了 JSON 序列化/反序列化支持：

```jsp
// 序列化：ChatMessage 列表 → JSON 字符串
String json = ChatMessageSerializer.messagesToJson(messages);

// 反序列化：JSON 字符串 → ChatMessage 列表
List<ChatMessage> messages = ChatMessageDeserializer.messagesFromJson(json);
```

### 4.2 Redis 存储策略

```
Key 格式:   agent:lc4j:chat:{memoryId}
Value 格式: JSON 数组，包含所有 ChatMessage
TTL:       7 天（604800 秒）

示例:
Key:   agent:lc4j:chat:user_123_session_abc
Value: [{"type":"SYSTEM","text":"你是一个助手"},{"type":"USER","text":"什么是递归？"}]
```

### 4.3 消息窗口策略

```jsp
// 滑动窗口：保留最近 20 条消息
MessageWindowChatMemory.builder()
    .id(memoryId)
    .maxMessages(20)
    .chatMemoryStore(redisChatMemoryStore)
    .build();

// Token 窗口：按 Token 数量限制（更精确的控制）
TokenWindowChatMemory.builder()
    .id(memoryId)
    .maxTokens(4000, new OpenAiTokenCountEstimator("gpt-4"))
    .chatMemoryStore(redisChatMemoryStore)
    .build();
```

---

## 5\. 多模型配置

### 5.1 概念

同一个应用可以配置多个不同用途的模型。

### 5.2 配置示例

```yaml
langchain4j:
  open-ai:
    # 主力对话模型
    chat-model:
      model-name: Qwen/Qwen3-Coder-30B-A3B-Instruct
      temperature: 0.7
      max-tokens: 4096
    # 流式模型
    streaming-chat-model:
      model-name: Qwen/Qwen3-Coder-30B-A3B-Instruct
      temperature: 0.7
    # 嵌入模型
    embedding-model:
      model-name: BAAI/bge-large-zh-v1.5
```

### 5.3 动态切换模型

```jsp
// 使用 @Qualifier 区分多个 ChatModel Bean
@Autowired @Qualifier("creativeModel")
private ChatModel creativeModel;

@Autowired @Qualifier("preciseModel")
private ChatModel preciseModel;

// 根据场景选择模型
ChatModel model = isCodeReview ? preciseModel : creativeModel;
```

---

## 6\. 项目依赖总览

```xml
<!-- oj-ai-service/pom.xml 中的完整依赖 -->

<!-- 核心：OpenAI 协议兼容的 LLM（含 ChatModel + EmbeddingModel 自动配置）-->
<dependency>
    <groupId>dev.langchain4j</groupId>
    <artifactId>langchain4j-open-ai-spring-boot-starter</artifactId>
</dependency>

<!-- Reactive 流支持（Flux 返回值）-->
<dependency>
    <groupId>dev.langchain4j</groupId>
    <artifactId>langchain4j-reactor</artifactId>
</dependency>

<!-- Easy RAG：自动文档格式检测和加载 -->
<dependency>
    <groupId>dev.langchain4j</groupId>
    <artifactId>langchain4j-easy-rag</artifactId>
</dependency>

<!-- MCP 协议客户端 -->
<dependency>
    <groupId>dev.langchain4j</groupId>
    <artifactId>langchain4j-mcp</artifactId>
</dependency>
```

`oj-problem-service` 额外依赖：

```xml
<!-- PDF 解析器 -->
<dependency>
    <groupId>dev.langchain4j</groupId>
    <artifactId>langchain4j-document-parser-apache-pdfbox</artifactId>
</dependency>
```

---

## 7\. 最佳实践总结

| 场景 | 推荐方案 |
| --- | --- |
| 快速原型 | Spring Boot Starter 自动配置 + `InMemoryEmbeddingStore` |
| 生产环境 | 持久化向量存储（PgVector/Redis/ES） + 本地 EmbeddingModel |
| 多用户会话 | `@MemoryId` + `ChatMemoryProvider` + Redis `ChatMemoryStore` |
| 工具扩展 | `@Tool` 注解 + MCP 协议（外部工具） |
| 流式响应 | `Flux<String>` / `TokenStream` + SSE |
| 知识库管理 | `EmbeddingStoreIngestor` 管道 + `FileSystemDocumentLoader` |

---

上一篇：[LangChain4j RAG 与知识库](./langchain4j-study-notes-02-rag.md)  
下一篇：[LangGraph4j 核心概念](./langgraph4j-study-notes-01-core.md)

## 相关条目
- [[langchain4j-study-notes-01-core]]
- [[langgraph4j-study-notes-02-advanced]]
