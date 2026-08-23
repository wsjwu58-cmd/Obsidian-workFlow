# langchain4j-study-notes-01-core
## LangChain4j 核心概念学习笔记 (一)

> 基于项目 `oj-microservice` 实战 + 官方文档整理  
> 版本: `1.12.2` | JDK 17+

---

## 1\. ChatModel —— 与 LLM 对话的基础

### 1.1 概念

`ChatModel` 是 LangChain4j 中最核心的接口，封装了与 LLM 的同步对话能力。所有 LLM 提供商（OpenAI、Ollama、Azure、Google Gemini 等）都实现了该接口。

### 1.2 项目实战

项目中通过 Spring Boot Starter 自动配置，在 `application.yml` 中声明即可注入：

```yaml
# oj-ai-service/src/main/resources/application.yml
langchain4j:
  open-ai:
    chat-model:
      api-key: sk-xxx
      base-url: https://api.siliconflow.cn/v1
      model-name: Qwen/Qwen3-Coder-30B-A3B-Instruct
      temperature: 0.7
      max-tokens: 4096
      log-requests: true
      log-responses: true
```

```jsp
// 直接注入即可使用
@Autowired
private ChatModel chatModel;

// 同步调用
String response = chatModel.generate("什么是动态规划？");
```

### 1.3 官方文档拓展 —— 手动构建 ChatModel

当不使用 Spring Boot Starter 或需要完全控制参数时：

```jsp
ChatModel chatModel = OpenAiChatModel.builder()
    .apiKey(System.getenv("OPENAI_API_KEY"))
    .baseUrl("https://api.siliconflow.cn/v1")  // 自定义 Base URL
    .modelName("Qwen/Qwen3-Coder-30B-A3B-Instruct")
    .temperature(0.7)
    .maxTokens(4096)
    .logRequests(true)
    .logResponses(true)
    .build();
```

其他提供商的构建方式：

```jsp
// Ollama (本地模型)
ChatModel ollamaModel = OllamaChatModel.builder()
    .baseUrl("http://localhost:11434")
    .modelName("llama3.1")
    .build();

// Google Gemini
ChatModel geminiModel = GoogleAiGeminiChatModel.builder()
    .apiKey(System.getenv("GOOGLE_AI_GEMINI_API_KEY"))
    .modelName("gemini-1.5-flash")
    .build();
```

---

## 2\. StreamingChatModel —— 流式对话

### 2.1 概念

`StreamingChatModel` 是 `ChatModel` 的流式版本，支持 Token-by-Token 输出，适用于需要实时显示 AI 回复的场景（如 SSE）。

### 2.2 项目实战 —— 底层 Streaming 方式

项目在 `RAGServiceImpl.java` 中直接使用 `StreamingChatModel.chat()` 配合 `StreamingChatResponseHandler`：

```jsp
// oj-ai-service/src/main/java/com/oj/ai/service/impl/RAGServiceImpl.java:86
StreamingChatModel streamingChatModel; // 自动注入

List<ChatMessage> messages = new ArrayList<>();
messages.add(SystemMessage.from("你是一位专业的编程导师..."));
messages.add(UserMessage.from(userQuestion));

ChatRequest request = ChatRequest.builder().messages(messages).build();

streamingChatModel.chat(request, new StreamingChatResponseHandler() {
    @Override
    public void onPartialResponse(String partialResponse) {
        // 每收到一个 Token 就通过 SSE 推送给前端
        emitter.send(SseEmitter.event().data(partialResponse));
    }

    @Override
    public void onCompleteResponse(ChatResponse completeResponse) {
        // 流结束，保存对话历史
        emitter.complete();
    }

    @Override
    public void onError(Throwable error) {
        emitter.completeWithError(error);
    }
});
```

### 2.3 官方文档拓展 —— AiServices + TokenStream 方式

推荐使用 `AiServices` 高层 API + `TokenStream`，更简洁：

```jsp
interface StreamingAssistant {
    TokenStream chat(String message);
}

StreamingChatModel model = OpenAiStreamingChatModel.builder()
    .apiKey(System.getenv("OPENAI_API_KEY"))
    .modelName("gpt-4o-mini")
    .build();

StreamingAssistant assistant = AiServices.create(StreamingAssistant.class, model);

CompletableFuture<ChatResponse> future = new CompletableFuture<>();

assistant.chat("Tell me a joke")
    .onPartialResponse(System.out::print)
    .onCompleteResponse(response -> {
        System.out.println("\nDone!");
        future.complete(response);
    })
    .onError(future::completeExceptionally)
    .start();

future.join();
```

### 2.4 官方文档拓展 —— Spring Boot Reactive Flux

引入 `langchain4j-reactor` 后可使用 `Flux<String>` 作为返回值：

```xml
<dependency>
    <groupId>dev.langchain4j</groupId>
    <artifactId>langchain4j-reactor</artifactId>
</dependency>
```

```jsp
// 项目中的用法
@SystemMessage("你是一个专业的OJ AI助手...")
Flux<String> chatStream(@MemoryId String memoryId, @UserMessage String userMessage);
```

---

## 3\. AiServices —— 声明式 AI 服务

### 3.1 概念

`AiServices` 是 LangChain4j 的核心高层 API。通过定义一个 **接口** + **注解**，即可将 LLM 调用、工具调用、记忆管理、RAG 检索等能力组合成一个完整的 AI 服务。

### 3.2 项目实战 —— AgentAssistant

```jsp
// oj-ai-service/src/main/java/com/oj/ai/service/agent/AgentAssistant.java
public interface AgentAssistant {

    @SystemMessage("""
            你是一个专业的OJ（在线判题系统）AI助手，具备以下能力：
            1. **题解生成**：根据题目要求生成详细的解题思路和参考代码
            2. **学情分析**：分析用户的学习进度、薄弱点并给出建议
            3. **AI判题**：分析用户提交的代码，判断正确性，给出改进建议
            4. **知识检索**：从知识库中检索相关的编程知识
            5. **网络搜索**：通过MCP协议连接搜索服务器
            
            ## 工具调用规则
            - 如果用户的问题涉及具体题目，请先调用 getProblemDetail 获取题目详情
            - 如果用户要求生成题解，请调用 generateSolution
            - 如果用户提供了代码并要求检查分析，请调用判题工具
            - 当用户询问编程概念时，优先调用 searchKnowledge
            """)
    String chat(@MemoryId String memoryId, @UserMessage String userMessage);

    Flux<String> chatStream(@MemoryId String memoryId, @UserMessage String userMessage);
}
```

**关键注解：**

| 注解 | 作用 |
| --- | --- |
| `@SystemMessage` | 设置系统提示词，定义 Agent 的角色和行为规则 |
| `@UserMessage` | 标记用户输入参数 |
| `@MemoryId` | 标记会话 ID，用于隔离不同用户的对话上下文 |

### 3.3 项目实战 —— 构建 AgentService

```jsp
// oj-ai-service/src/main/java/com/oj/ai/service/agent/AgentService.java:87
agentAssistant = AiServices.builder(AgentAssistant.class)
    .chatModel(chatModel)
    .streamingChatModel(streamingChatModel)
    .tools(solutionGeneratorTool, learningAnalyzerTool, aiJudgeTool, knowledgeRetrievalTool)
    .chatMemoryProvider(memoryId -> MessageWindowChatMemory.builder()
            .id(memoryId)
            .maxMessages(20)
            .chatMemoryStore(redisChatMemoryStore)
            .build())
    .build();
```

**AiServices.builder() 配置项：**

| 方法 | 说明 |
| --- | --- |
| `.chatModel(ChatModel)` | 注入聊天模型 |
| `.streamingChatModel(StreamingChatModel)` | 注入流式模型（用于 Flux 返回值） |
| `.tools(Object...)` | 注册工具对象（包含 `@Tool` 注解的方法） |
| `.chatMemoryProvider(Function)` | 为每个 memoryId 提供独立的 ChatMemory |
| `.chatMemory(ChatMemory)` | 全局共享的 ChatMemory |
| `.contentRetriever(ContentRetriever)` | 注册 RAG 检索器 |
| `.toolProvider(ToolProvider)` | 动态工具提供者（比如 MCP） |

---

## 4\. @Tool —— 工具注解

### 4.1 概念

`@Tool` 让 LLM 能够调用 Java 方法。LLM 会根据用户问题自动决策是否调用工具、调用哪个工具、传递什么参数。

### 4.2 项目实战 —— KnowledgeRetrievalTool

```jsp
// oj-ai-service/src/main/java/com/oj/ai/service/tools/KnowledgeRetrievalTool.java
@Component
public class KnowledgeRetrievalTool {

    @Autowired
    private KnowledgeRetrievalService knowledgeRetrievalService;

    @Tool("检索知识库，获取与用户问题相关的知识片段")
    public String searchKnowledge(
            @P("用户的问题或查询内容") String query,
            @P("上下文信息，如题目描述、代码片段等，可以为空") String context,
            @P("返回的相关知识数量，默认为3，范围1-5") Integer topK) {
        List<String> results = knowledgeRetrievalService.retrieveKnowledge(query, context, topK);
        // 格式化返回给 LLM
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < results.size(); i++) {
            sb.append("【知识").append(i + 1).append("】\n").append(results.get(i)).append("\n\n");
        }
        return sb.toString();
    }
}
```

**关键点：**

*   `@Tool("描述")` —— 描述越详细，LLM 越能正确决策是否调用
*   `@P("参数说明")` —— 为每个参数提供语义说明
*   工具方法返回值会被当作上下文注入到 LLM 的对话中

### 4.3 官方文档拓展 —— 简单工具示例

```jsp
class Calculator {

    @Tool("Adds two given numbers")
    double add(double a, double b) {
        return a + b;
    }

    @Tool("Multiplies two given numbers")
    String multiply(double a, double b) {
        return String.valueOf(a * b);
    }

    @Tool("Calculates the square root")
    double squareRoot(double x) {
        return Math.sqrt(x);
    }
}

interface MathGenius {
    String ask(String question);
}

MathGenius genius = AiServices.builder(MathGenius.class)
    .chatModel(model)
    .tools(new Calculator())
    .build();

String answer = genius.ask("What is the square root of 475695037565?");
System.out.println(answer); // The square root of 475695037565 is 689706.486532.
```

### 4.4 官方文档拓展 —— 带元数据的工具

可以通过 `metadata` 属性提供输入示例，帮助 LLM 更准确地调用：

```jsp
@Tool(metadata = """
    {
        \"input_examples\": [
            {\"location\": \"San Francisco, CA\", \"unit\": \"FAHRENHEIT\"},
            {\"location\": \"Tokyo, Japan\", \"unit\": \"CELSIUS\"}
        ]
    }
    """)
String getWeather(String location,
                  @P(value = "temperature unit", required = false) Unit unit) {
    return "sunny";
}
```

---

## 5\. ChatMemory —— 对话记忆

### 5.1 概念

`ChatMemory` 负责管理 LLM 对话的历史记录。LangChain4j 提供了 `MessageWindowChatMemory`（滑动窗口）和 `TokenWindowChatMemory`（按 Token 数限制）。

### 5.2 项目实战 —— RedisChatMemoryStore

项目中实现了自定义 `ChatMemoryStore`，将对话持久化到 Redis：

```jsp
// oj-ai-service/src/main/java/com/oj/ai/service/memory/RedisChatMemoryStore.java
@Component
public class RedisChatMemoryStore implements ChatMemoryStore {

    private static final String KEY_PREFIX = "agent:lc4j:chat:";
    private static final long TTL_SECONDS = 86400L * 7; // 7天过期

    @Autowired
    private StringRedisTemplate redisTemplate;

    @Override
    public List<ChatMessage> getMessages(Object memoryId) {
        String key = toKey(memoryId);
        String json = redisTemplate.opsForValue().get(key);
        if (json == null || json.isBlank()) return new ArrayList<>();
        return ChatMessageDeserializer.messagesFromJson(json);
    }

    @Override
    public void updateMessages(Object memoryId, List<ChatMessage> messages) {
        String key = toKey(memoryId);
        if (messages == null || messages.isEmpty()) {
            redisTemplate.delete(key);
            return;
        }
        String json = ChatMessageSerializer.messagesToJson(messages);
        redisTemplate.opsForValue().set(key, json, TTL_SECONDS, TimeUnit.SECONDS);
    }

    @Override
    public void deleteMessages(Object memoryId) {
        redisTemplate.delete(toKey(memoryId));
    }

    private static String toKey(Object memoryId) {
        return KEY_PREFIX + (memoryId == null ? "null" : memoryId.toString().replace(':', '_'));
    }
}
```

在 `AgentService` 中使用 Redis 存储的 ChatMemory：

```jsp
.chatMemoryProvider(memoryId -> MessageWindowChatMemory.builder()
    .id(memoryId)
    .maxMessages(20)               // 保留最近20条消息
    .chatMemoryStore(redisChatMemoryStore)  // 持久化到 Redis
    .build())
```

### 5.3 官方文档拓展 —— ChatMemoryProvider 模式

通过 `@MemoryId` 和 `chatMemoryProvider`，每个用户会话拥有独立的记忆：

```jsp
interface Assistant {
    String chat(@MemoryId int memoryId, @UserMessage String message);
}

Assistant assistant = AiServices.builder(Assistant.class)
    .chatModel(model)
    .chatMemoryProvider(memoryId -> MessageWindowChatMemory.withMaxMessages(10))
    .build();

String answer1 = assistant.chat(1, "Hello, my name is Klaus");
String answer2 = assistant.chat(2, "Hello, my name is Francine");
// 两个会话的记忆完全隔离
```

---

## 6\. 核心数据模型

```jsp
// 消息类型
import dev.langchain4j.data.message.SystemMessage;   // 系统提示
import dev.langchain4j.data.message.UserMessage;     // 用户消息
import dev.langchain4j.data.message.AiMessage;       // AI 回复

// 构建消息列表
List<ChatMessage> messages = List.of(
    SystemMessage.from("你是一个助手"),
    UserMessage.from("你好")
);

// 请求与响应
ChatRequest request = ChatRequest.builder()
    .messages(messages)
    .build();
ChatResponse response = chatModel.chat(request);
String text = response.aiMessage().text();
```

---

## 7\. 整体架构图

```
┌─────────────────────────────────────────────────┐
│                  AiServices                       │
│  ┌───────────┐  ┌──────────┐  ┌──────────────┐  │
│  │ ChatModel  │  │  Tools   │  │ ChatMemory   │  │
│  └───────────┘  └──────────┘  └──────────────┘  │
│        │              │               │          │
│        ▼              ▼               ▼          │
│  ┌──────────────────────────────────────────┐   │
│  │         AgentAssistant (接口)             │   │
│  │  @SystemMessage / @MemoryId / @Tool      │   │
│  └──────────────────────────────────────────┘   │
│                      │                           │
│                      ▼                           │
│            chat()  /  chatStream()               │
└─────────────────────────────────────────────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  Redis (memory)  │
              └─────────────────┘
```

---

下一篇：[LangChain4j RAG 与知识库](./langchain4j-study-notes-02-rag.md)

## 相关条目
- [[langchain4j-study-notes-02-rag]]
- [[langchain4j-study-notes-03-advanced]]
- [[langgraph4j-study-notes-01-core]]
