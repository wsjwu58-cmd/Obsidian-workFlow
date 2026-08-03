# langchain4j-study-notes-02-rag
## LangChain4j RAG 与知识库学习笔记 (二)

> 基于项目 `oj-microservice` 实战 + 官方文档整理  
> 版本: `1.12.2` | JDK 17+

---

## 1\. RAG 概述

**RAG（Retrieval-Augmented Generation，检索增强生成）** 的核心流程：

```
PDF/文档 → 解析(Parser) → 分割(Splitter) → 向量化(EmbeddingModel) → 存储(EmbeddingStore)
                                                                              │
用户提问 → 向量化(EmbeddingModel) ────→ 相似度搜索 ────→ 检索TopK片段 ────→ 注入LLM Prompt → 生成回答
```

---

## 2\. EmbeddingModel —— 文本向量化

### 2.1 概念

`EmbeddingModel` 将文本转换为向量（浮点数数组），是实现语义搜索的基础。

### 2.2 项目配置

```yaml
# oj-ai-service/src/main/resources/application.yml
langchain4j:
  open-ai:
    embedding-model:
      api-key: sk-xxx
      base-url: https://api.siliconflow.cn/v1
      model-name: BAAI/bge-large-zh-v1.5   # 中文优化嵌入模型
      log-requests: true
      log-responses: true
```

### 2.3 官方文档拓展 —— 本地嵌入模型

生产环境可以使用本地模型，避免 API 调用延迟：

```
// 使用 ONNX 格式的本地嵌入模型（无需网络）
EmbeddingModel embeddingModel = new AllMiniLmL6V2EmbeddingModel();

// 或使用 BGE-small-zh 中文模型（需额外依赖）
EmbeddingModel bgeModel = new BgeSmallZhEmbeddingModel();
```

本地嵌入模型的优势：

*   零延迟，无网络依赖
*   无 API 调用费用
*   数据不离开服务器，安全合规

---

## 3\. EmbeddingStore —— 向量存储

### 3.1 概念

`EmbeddingStore<TextSegment>` 存储文本片段及其对应的向量，支持相似度搜索。

### 3.2 项目实战 —— InMemoryEmbeddingStore

项目中两个服务都使用 `InMemoryEmbeddingStore`：

```
// oj-ai-service/src/main/java/com/oj/ai/config/LangChain4jConfig.java
@Bean
public EmbeddingStore<TextSegment> embeddingStore() {
    return new InMemoryEmbeddingStore<>();
}
```

```
// oj-problem-service 中相同配置
@Bean
public EmbeddingStore<TextSegment> embeddingStore() {
    return new InMemoryEmbeddingStore<>();
}
```

### 3.3 相似度搜索

```
// oj-ai-service/src/main/java/com/oj/ai/service/impl/KnowledgeRetrievalServiceImpl.java
@Autowired
private EmbeddingModel embeddingModel;

@Autowired
private EmbeddingStore<TextSegment> embeddingStore;

public List<String> retrieveKnowledge(String query, String context, int topK) {
    // 1. 将查询文本向量化
    Embedding queryEmbedding = embeddingModel.embed(query).content();

    // 2. 在向量存储中搜索 topK 个最相似的片段
    EmbeddingSearchRequest searchRequest = EmbeddingSearchRequest.builder()
        .queryEmbedding(queryEmbedding)
        .maxResults(topK)
        .minScore(0.7)  // 最低相似度阈值
        .build();

    EmbeddingSearchResult<TextSegment> result = embeddingStore.search(searchRequest);

    // 3. 提取文本
    return result.matches().stream()
        .map(match -> match.embedded().text())
        .collect(Collectors.toList());
}
```

### 3.4 官方文档拓展 —— 持久化向量存储

生产环境应使用持久化存储，避免服务重启丢失数据：

```
// PgVector (PostgreSQL 向量扩展)
EmbeddingStore<TextSegment> store = PgVectorEmbeddingStore.builder()
    .host("localhost")
    .port(5432)
    .database("oj_knowledge")
    .user("postgres")
    .password("password")
    .table("embeddings")
    .dimension(1024)  // BGE-large-zh 的维度
    .build();

// Redis Stack (支持向量搜索)
EmbeddingStore<TextSegment> store = RedisEmbeddingStore.builder()
    .host("localhost")
    .port(6379)
    .indexName("oj-knowledge")
    .dimension(1024)
    .build();

// Elasticsearch
EmbeddingStore<TextSegment> store = ElasticsearchEmbeddingStore.builder()
    .serverUrl("http://localhost:9200")
    .indexName("oj-knowledge")
    .build();
```

---

## 4\. 文档导入 Pipeline

### 4.1 概念

`EmbeddingStoreIngestor` 是一个完整的文档摄入管道，将文档自动解析、分割、向量化、存入向量库。

### 4.2 项目实战 —— PDF 知识导入

```
// oj-problem-service/src/main/java/com/oj/problem/service/impl/KnowledgeImportServiceImpl.java
private int processPdfFile(Path pdfPath, String category, String sourceName) {
    // Step 1: 解析 PDF
    DocumentParser parser = new ApachePdfBoxDocumentParser();
    Document document;
    try (InputStream inputStream = Files.newInputStream(pdfPath)) {
        document = parser.parse(inputStream);
    }

    // Step 2: 分割文档（每段350字符，重叠50字符）
    DocumentSplitter splitter = DocumentSplitters.recursive(350, 50);
    List<TextSegment> segments = splitter.split(document);

    // Step 3: 添加元数据
    List<Document> documentsToIngest = new ArrayList<>();
    for (TextSegment segment : segments) {
        Map<String, Object> metadataMap = new HashMap<>();
        metadataMap.put("category", category);
        metadataMap.put("source", sourceName);
        metadataMap.put("importTime", System.currentTimeMillis());
        Metadata metadata = new Metadata(metadataMap);
        documentsToIngest.add(Document.from(segment.text(), metadata));
    }

    // Step 4: 摄入向量库（自动向量化 + 存储）
    EmbeddingStoreIngestor.builder()
        .embeddingModel(embeddingModel)
        .embeddingStore(embeddingStore)
        .build()
        .ingest(documentsToIngest);

    return documentsToIngest.size();
}
```

### 4.3 官方文档拓展 —— 完整 Ingestor 配置

```
EmbeddingStoreIngestor ingestor = EmbeddingStoreIngestor.builder()
    // 文档转换器：为每个文档添加 userId 元数据
    .documentTransformer(document -> {
        document.metadata().put("userId", "12345");
        return document;
    })
    // 文档分割器：1000 token/段，200 token 重叠
    .documentSplitter(DocumentSplitters.recursive(
        1000, 200,
        new OpenAiTokenCountEstimator("gpt-4o-mini")
    ))
    // 文本段转换器：在内容前附加文件名
    .textSegmentTransformer(textSegment -> TextSegment.from(
        textSegment.metadata().getString("file_name") + "\n" + textSegment.text(),
        textSegment.metadata()
    ))
    .embeddingModel(embeddingModel)
    .embeddingStore(embeddingStore)
    .build();

ingestor.ingest(documents);
```

---

## 5\. Easy RAG —— 开箱即用的文档加载

### 5.1 概念

`langchain4j-easy-rag` 模块提供了自动文档格式检测和加载，无需手动指定 Parser。

### 5.2 依赖

```xml
<dependency>
    <groupId>dev.langchain4j</groupId>
    <artifactId>langchain4j-easy-rag</artifactId>
</dependency>
```

### 5.3 使用示例

```
// 加载单个文件（自动检测格式：PDF/Word/TXT/HTML 等）
List<Document> docs = FileSystemDocumentLoader.loadDocuments("/path/to/docs");

// 递归加载目录下所有文件
List<Document> allDocs = FileSystemDocumentLoader.loadDocumentsRecursively("/path/to/docs");

// 创建嵌入存储
InMemoryEmbeddingStore<TextSegment> embeddingStore = new InMemoryEmbeddingStore<>();

// 一行摄入
EmbeddingStoreIngestor.ingest(documents, embeddingStore);
```

---

## 6\. ContentRetriever —— 从向量库检索

### 6.1 概念

`ContentRetriever` 是 RAG 的检索抽象层。使用 `EmbeddingStoreContentRetriever` 可以从向量存储中检索相关内容。

### 6.2 官方文档示例

```
// 方式一：直接构建
ContentRetriever contentRetriever = EmbeddingStoreContentRetriever.builder()
    .embeddingStore(embeddingStore)
    .embeddingModel(embeddingModel)
    .maxResults(5)
    .minScore(0.75)
    .build();

// 方式二：快速创建
ContentRetriever contentRetriever = new EmbeddingStoreContentRetriever(
    embeddingStore, embeddingModel
);

// 集成到 AiServices
interface DocumentAssistant {
    String chat(String userMessage);
}

DocumentAssistant assistant = AiServices.builder(DocumentAssistant.class)
    .chatModel(model)
    .contentRetriever(contentRetriever)
    .chatMemory(MessageWindowChatMemory.withMaxMessages(10))
    .build();

String answer = assistant.chat("How do I configure the application?");
```

---

## 7\. 项目 RAG 实战 —— 多场景应用

### 7.1 编程答疑（带知识检索）

```
// RAGServiceImpl.chatWithKnowledge() - 完整的 RAG 对话流程
public SseEmitter chatWithKnowledge(AiChatDTO dto) {
    // 1. 获取题目上下文
    ProblemFeignDTO problem = problemClient.getProblemById(dto.getProblemId());

    // 2. 构建检索上下文
    String context = "题目: " + problem.getTitle() + "\n代码: " + dto.getCode();

    // 3. 知识检索
    List<String> knowledge = knowledgeRetrievalService.retrieveKnowledge(
        dto.getMessage(), context, 3);

    // 4. 拼装增强 Prompt
    StringBuilder augmented = new StringBuilder();
    augmented.append("## 相关知识\n");
    for (int i = 0; i < knowledge.size(); i++) {
        augmented.append((i + 1)).append(". ").append(knowledge.get(i)).append("\n\n");
    }
    augmented.append("## 用户问题\n").append(dto.getMessage());

    // 5. 调用 LLM 流式生成
    List<ChatMessage> messages = new ArrayList<>();
    messages.add(SystemMessage.from("你是一位专业的编程导师..."));
    messages.add(UserMessage.from(augmented.toString()));

    ChatRequest request = ChatRequest.builder().messages(messages).build();
    streamingChatModel.chat(request, new StreamingChatResponseHandler() {
        @Override public void onPartialResponse(String partial) {
            emitter.send(SseEmitter.event().data(partial));
        }
        @Override public void onCompleteResponse(ChatResponse complete) {
            emitter.complete();
        }
    });
}
```

### 7.2 错误分析（带知识检索）

```
// RAGServiceImpl.analyzeErrorWithKnowledge() - 错误分析流程
// 检索与错误类型相关的知识，辅助 LLM 给出精准分析
List<String> knowledge = knowledgeRetrievalService.retrieveKnowledge(
    "代码错误分析: " + errorInfo,
    "题目: " + problem.getTitle() + "\n代码: " + code,
    3
);
```

### 7.3 解题提示（渐进式引导）

```
// RAGServiceImpl.getHintWithKnowledge() - 只给提示不给答案
// 通过 SystemMessage 约束 LLM 行为：
messages.add(SystemMessage.from(
    "你是一位专业的编程导师，擅长引导学生思考。只给提示，不要直接给出完整答案。"
));
```

---

## 8\. RAG 架构总结

```
┌──────────────────────────────────────────────────────────┐
│                      知识导入 Pipeline                     │
│                                                            │
│   PDF/文档  ──▶  ApachePdfBoxDocumentParser  ──▶           │
│   (MultipartFile)           │                              │
│                             ▼                              │
│                  DocumentSplitters.recursive(350, 50)     │
│                             │                              │
│                             ▼                              │
│   EmbeddingStoreIngestor                                   │
│     ├── embeddingModel (BAAI/bge-large-zh-v1.5)           │
│     └── embeddingStore (InMemoryEmbeddingStore)            │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│                       知识检索 Pipeline                    │
│                                                            │
│   用户提问 ──▶  EmbeddingModel.embed()  ──▶  向量         │
│                                                 │          │
│   向量 ──▶  EmbeddingStore.search()  ──▶  TopK 文本片段   │
│                                                 │          │
│   文本片段 + 用户问题 ──▶  Prompt 拼接  ──▶  LLM 生成     │
└──────────────────────────────────────────────────────────┘
```

---

上一篇：[LangChain4j 核心概念](./langchain4j-study-notes-01-core.md)  
下一篇：[LangChain4j 进阶](./langchain4j-study-notes-03-advanced.md)

## 相关条目
- [[langchain4j-study-notes-01-core]]
- [[RAG处理优化]]
