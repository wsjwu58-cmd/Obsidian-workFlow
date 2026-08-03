# RAG处理优化
## 一、RAG 概述

### 1.1 什么是 RAG

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将信息检索（IR）与大型语言模型（LLM）结合的架构模式。其核心思想是：在 LLM 生成回答之前，先从外部知识库中检索与用户问题最相关的文档片段，将这些片段作为"事实依据"注入到 Prompt 中，从而使 LLM 能够基于外部知识而非仅依赖模型参数中的记忆来回答问题。

RAG 于 2020 年由 Lewis 等人在 Meta AI 的论文《Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks》中首次正式提出。该论文论证了参数化知识（存储在模型权重中）与非参数化知识（存储在外部检索索引中）的互补关系——参数化模型提供语言理解和生成能力，非参数化检索提供最新、可验证的事实支持。

### 1.2 RAG 解决了什么问题

LLM 存在三个根本性局限，RAG 正是为缓解这些局限而设计的：

| 局限 | 根源 | RAG 解决方案 |
| --- | --- | --- |
| **知识截止（Knowledge Cutoff）** | 模型训练数据有时间边界，无法获取训练后的新信息 | 从实时更新的外部知识库检索最新信息 |
| **幻觉（Hallucination）** | LLM 本质是概率式生成，可能输出看似合理但实际错误的内容 | 将回答锚定在检索到的真实文档上，提供可溯源的引用 |
| **领域知识不足** | 通用预训练模型缺乏垂直领域的专业知识 | 接入企业私有文档库、技术手册等垂直领域语料 |

### 1.3 RAG 的核心流程（五步流水线）

```
①索引构建（离线）:
  原始文档 → 文档解析 → 文本分片 → 向量化(Embedding) → 向量数据库存储

②查询处理（在线）:
  用户问题 → 查询理解/重写 → 向量化 →

③检索:
  向量相似度搜索 → 候选片段集(K个) → [可选: 重排序] →

④上下文组装:
  检索片段 + 用户问题 → Prompt 模板 → 完整上下文 →

⑤生成:
  LLM 推理 → 回答输出
```

**离线 vs 在线**：步骤①是一次性或批量更新的离线过程（索引构建）；步骤②-⑤是每次用户请求时实时执行的在线流程。理解这一划分对于系统设计至关重要——索引构建可以做更复杂的分片和预处理，而在线路径必须优化延迟。

### 1.4 RAG 的演化历程

| 阶段 | 时间 | 代表技术 | 特点 |
| --- | --- | --- | --- |
| **朴素 RAG** | 2020 | 基础检索-阅读 | 单次检索 + 单次生成 |
| **高级 RAG** | 2021-2022 | 重排序、HyDE、混合检索 | 多阶段检索优化 |
| **模块化 RAG** | 2023-2024 | 模块化流水线 | 可替换的检索器/生成器/重排器 |
| **Agentic RAG** | 2024+ | Agent 驱动的动态检索 | 多步推理 + 自适应检索策略 |

---

## 二、信息检索理论基础

理解 RAG 的第一步，是理解信息检索（IR）的基本原理。

### 2.1 布尔检索与 TF-IDF

**布尔检索**是信息检索的原始形式：用户输入关键词（如 `Java AND 虚拟机 AND 调优`），系统返回包含所有关键词的文档。它的缺陷是"有或无"——无法区分文档的相关程度。

**TF-IDF（词频-逆文档频率）** 解决了相关性排序问题。其核心直觉是：

*   **TF（Term Frequency）**：一个词在文档中出现的次数越多，该词越能代表文档主题
*   **IDF（Inverse Document Frequency）**：一个词在越少的文档中出现，该词的区分能力越强

```
TF(w, d) = 词 w 在文档 d 中出现的次数 / 文档 d 的总词数
IDF(w) = log(总文档数 / 包含词 w 的文档数)
TF-IDF(w, d) = TF(w, d) × IDF(w)
```

TF-IDF 将每个文档表示为一个稀疏向量（维度=词汇表大小），查询和文档的相关性通过向量的余弦相似度计算。这是现代语义检索的前身在数学上的基础。

### 2.2 BM25

BM25 是对 TF-IDF 的改进，是目前最常用的稀疏检索算法。它引入两个关键修正：

1.  **词频饱和**：`TF` 的增长效应递减（出现 10 次的词不会比出现 5 次的相关 2 倍）
2.  **文档长度归一化**：长文档不会仅因为包含更多词语而获得不合理的更高分数

```
BM25(q, d) = Σ IDF(w_i) × [TF(w_i, d) × (k1 + 1)] / [TF(w_i, d) + k1 × (1 - b + b × |d|/avgdl)]

其中：
  k1 = 词频饱和参数（通常 1.2~2.0）
  b = 文档长度归一化参数（通常 0.75）
  |d| = 文档长度
  avgdl = 平均文档长度
```

### 2.3 稠密检索与向量空间模型

传统检索的局限在于**词汇不匹配问题**（Vocabulary Mismatch）——“汽车”和“轿车”在关键词匹配中被视为完全不同的词，尽管语义相同。

**稠密检索**（Dense Retrieval）通过将文本映射到连续向量空间来解决这个问题。其核心假设是：语义相似的文本在向量空间中距离更近。

这一假设的基础是**分布语义假说**（Distributional Hypothesis）——"一个词的含义由它周围的词决定"（Firth, 1957）。BERT、GPT 等预训练语言模型正是基于这一假说，通过预测上下文来学习词的向量表示。

### 2.4 嵌入模型的工作原理

现代嵌入模型（如 text-embedding-3-small、BGE、E5）通常采用双编码器（Bi-Encoder）架构：

```
                   ┌──────────────┐
查询文本 → Tokenizer → 编码器(BERT) → 查询向量(q)
                   └──────────────┘

                   ┌──────────────┐
文档文本 → Tokenizer → 编码器(BERT) → 文档向量(d)
                   └──────────────┘

相似度 = cos(q, d) = q·d / (||q|| × ||d||)
```

训练目标通常是对比学习（Contrastive Learning）：拉近相关查询-文档对的向量距离，推远不相关对的向量距离。常用的损失函数是 InfoNCE：

```
L = -log[ exp(sim(q, d+) / τ) / Σ_{i} exp(sim(q, d_i) / τ) ]

其中：
  d+ = 正例文档
  d_i = 所有候选文档（包括负例）
  τ = 温度参数（控制分布锐度）
```

### 2.5 双编码器 vs 交叉编码器

| 特性 | 双编码器 (Bi-Encoder) | 交叉编码器 (Cross-Encoder) |
| --- | --- | --- |
| **工作原理** | 分别编码查询和文档，再计算相似度 | 将查询和文档拼接后联合编码 |
| **速度** | 极快（文档向量可预计算） | 慢（每个查询-文档对需完整推理） |
| **精度** | 较低（查询和文档独立编码，交互不足） | 高（查询和文档在全注意力层中充分交互） |
| **典型用途** | 第一阶段检索（粗排） | 第二阶段重排序（精排） |
| **代表模型** | BGE, E5, text-embedding-3 | Cohere Rerank, BGE-Reranker |

这是为什么 RAG 系统中通常采用"粗排 + 精排"两阶段架构：双编码器在海量候选集中快速筛选 Top-K，交叉编码器在 Top-K 中精细排序。

---

## 三、近似最近邻搜索（ANN）算法

向量检索的核心是近似最近邻（Approximate Nearest Neighbor, ANN）搜索——在可接受精度损失下，大幅提升搜索速度。

### 3.1 HNSW（Hierarchical Navigable Small World）

HNSW 是目前最广泛使用的 ANN 算法之一。它构建一个多层图结构：

```
层级 2 (稀疏，长距离边):   ●───────────────●
                           │               │
层级 1 (中等):      ●──────●──────●────────●
                    │      │      │        │
层级 0 (密集，短距离边): ●─●──●──●─●──●─●──●─●  ← 原始数据点
```

**搜索过程**（类似"跳表 + 小世界图"）：

1.  从顶层随机入口节点开始
2.  在当前层进行贪心搜索（只沿最近邻方向移动）
3.  到达当前层的局部最优后，下降到下一层
4.  重复直到第 0 层，返回最近邻结果

**关键参数**：

*   `M`：每个节点的最大连接数（影响内存和精度，通常 16-64）
*   `efConstruction`：构建时的搜索宽度（越大精度越高，构建越慢）
*   `efSearch`：查询时的搜索宽度（越大召回越高，查询越慢）

### 3.2 IVF（Inverted File Index）

IVF 通过聚类减少搜索空间：

```
训练阶段：
  1. 对所有向量进行 K-Means 聚类，得到 C 个聚类中心
  2. 将每个向量分配到最近的聚类中心

查询阶段：
  1. 计算查询向量与所有 C 个聚类中心的距离
  2. 只在与查询最近的 nprobe 个聚类中搜索（nprobe << C）
```

*   **优点**：内存效率高，适合大规模数据集
*   **缺点**：如果查询向量落在聚类边界附近，可能漏掉边界外的相关向量

### 3.3 PQ（Product Quantization）

PQ 是一种向量压缩技术，通过将高维向量分解为多个低维子向量并分别量化来实现压缩：

```
原始向量 (768维) → 分为 8 个子向量 (各 96维) → 每个子向量用最近的码字索引表示

存储代价：768 × 4字节 = 3072字节 → 8 × 1字节 = 8字节（压缩比 384:1）
```

### 3.4 算法选择指南

| 场景 | 推荐算法 | 原因 |
| --- | --- | --- |
| <10万向量，高精度 | 暴力搜索（Flat） | 数据量小，无需近似 |
| 10万-1000万，高召回 | HNSW | 召回率最高，内存消耗中等 |
| \>1000万，内存受限 | IVF+PQ | 索引压缩比高，内存友好 |
| 混合场景 | IVF+HNSW | 结合两种算法的优势 |

---

## 四、文档加载与解析

### 4.1 文档解析的挑战

不同文档格式有着本质不同的结构特征：

*   **纯文本**：无结构，仅依赖换行和空行暗示段落边界
*   **PDF**：视觉导向布局，文本提取需处理多栏、表格和图片中的文字
*   **HTML**：标记语言，标签提供了明确的语义结构（`<h1>`, `<p>`, `<table>`）
*   **Markdown**：轻量标记，标题层级和代码块有明确语法
*   **代码**：具有严格语法规则，必须保持语义完整性

解析质量直接影响后续分片效果——如果 PDF 的多栏内容被错误地拼接在一起，任何分片策略都于事无补。

### 4.2 支持的文档类型与加载器

```python
from langchain_community.document_loaders import (
    TextLoader,                # 纯文本
    PDFPlumberLoader,         # PDF（基于 plumber）
    PyPDFLoader,              # PDF（基于 PyPDF）
    CSVLoader,                # CSV
    UnstructuredMarkdownLoader,  # Markdown
    WebBaseLoader,            # 网页
    DirectoryLoader,          # 目录批量加载
)

# 批量加载目录下所有 Markdown 文件
loader = DirectoryLoader(
    "./docs/", glob="**/*.md",
    use_multithreading=True, show_progress=True
)
documents = loader.load()
```

### 4.3 文档元数据

每个 Document 对象包含两个核心字段：

*   `page_content`：文本内容
*   `metadata`：元数据字典（source, page, author, date 等）

元数据不仅用于溯源，更是**高级检索策略**（如自查询检索、元数据过滤）的基础。

---

## 五、分片策略（Chunking）

分片是 RAG 流程中**最关键也最容易被低估**的一环。分片质量决定了检索精度的天花板——如果关键信息被切碎分散到不同的片，再好的检索算法也无法找回完整上下文。

### 5.1 分片的核心矛盾

```
片太大 → 包含过多无关内容 → 检索精度低 → LLM 被噪声干扰
片太小 → 丢失上下文 → 语义不完整 → LLM 无法理解片段含义
```

**最佳分片大小的经验法则**：

*   对大多数场景：300-800 token（约 400-1000 中文汉字）
*   对 FAQ 类短问答：100-300 token
*   对长文档分析：1000-2000 token

### 5.2 固定大小分片（CharacterTextSplitter）

按字符数进行机械切割，优先在分隔符处切割。

```python
from langchain.text_splitter import CharacterTextSplitter

text_splitter = CharacterTextSplitter(
    separator="\n\n",   # 优先按段落分隔
    chunk_size=1000,
    chunk_overlap=200
)
chunks = text_splitter.split_documents(documents)
```

**原理**：从文档开头扫描，累计字符数达到 `chunk_size` 后，在当前分隔符处切割，然后回退 `chunk_overlap` 个字符继续下一片的扫描。

### 5.3 递归字符分割（RecursiveCharacterTextSplitter）

递归分割是 LangChain 推荐的默认分片策略。它的核心思想是：按**由大到小的分隔符优先级列表**递归尝试切割，尽可能在自然语义边界（段落 > 句子 > 短语 > 字）处分割。

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", "。", ".", "？", "！", " ", ""]
)

# 针对代码的语言感知分割
python_splitter = RecursiveCharacterTextSplitter.from_language(
    language="python", chunk_size=500, chunk_overlap=0
)
```

**递归算法流程**：

1.  尝试用最高优先级分隔符切割文本
2.  如果某个片段仍然超过 `chunk_size`，降到下一优先级分隔符重新切割
3.  重复直到所有片段都小于 `chunk_size` 或达到最低优先级（逐字符切割）

### 5.4 语义分片（Semantic Chunking）

语义分片超越了"按字符/句子切割"的静态策略，利用**嵌入相似度动态判断切分点**。

**原理**：

1.  将文档逐句拆分
2.  计算相邻句子的嵌入向量
3.  计算相邻句子嵌入的余弦相似度
4.  当相似度显著下降（低于阈值）时，在此处切分——这表示话题出现了转变

```python
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

text_splitter = SemanticChunker(
    OpenAIEmbeddings(),
    breakpoint_threshold_type="percentile",   # 基于百分位
    # breakpoint_threshold_type="standard_deviation",  # 基于标准差
    # breakpoint_threshold_type="interquartile",       # 基于四分位距
    breakpoint_threshold_amount=90  # 90 百分位
)
chunks = text_splitter.split_documents(documents)
```

**阈值类型的选择**：

*   `percentile`：将相似度最低的 X% 视为断点，适合大多数文档
*   `standard_deviation`：将低于均值 N 个标准差的视为断点，适合相似度分布均匀的文档
*   `interquartile`：基于四分位距检测异常低相似度，适合包含异常段落的文档

### 5.5 分片策略对比

| 策略 | 原理 | 优点 | 缺点 |
| --- | --- | --- | --- |
| **固定大小** | 按字符数机械切割 | 简单，可预测 | 可能在句中切断 |
| **递归分割** | 按分隔符优先级递归 | 优先在自然边界切割 | 无法感知语义 |
| **语义分片** | 嵌入相似度判断 | 保持语义完整性 | 速度慢，成本高 |
| **Token Splitter** | 按 token 数切割 | 精确控制 token 消耗 | 同上 |
| **Agentic Chunking** | LLM 自主决策 | 最优语义完整性 | 极慢，极高成本 |
| **Multi-Modal** | 保留结构化信息 | 适合表格/图表 | 实现复杂 |

### 5.6 chunk\_overlap 的选择理论基础

`chunk_overlap`（片间重叠）的存在是为了缓解"关键信息被切分到两个不同片"的问题。

```
文档：...AAA BBB CCC DDD EEE FFF GGG HHH III JJJ KKK...

chunk_size=3, overlap=0:
  [AAA BBB CCC] [DDD EEE FFF] [GGG HHH III] [JJJ KKK]
  问题："BBB DDD"的语义被切断了

chunk_size=3, overlap=1:
  [AAA BBB CCC] [CCC DDD EEE] [EEE FFF GGG] [GGG HHH III] ...
  每个词的上下文都至少在一个完整片中出现了
```

**理论推导**：假设关键信息平均需要 `n` 个 token 的上下文才能完整理解，则 `overlap >= n/2` 可保证任何关键信息至少在一个完整的片中可用。

**经验参数**：

*   通用场景：`overlap = chunk_size × 10%~20%`
*   `chunk_size=500` → `overlap=50~100`
*   `chunk_size=1000` → `overlap=100~200`

---

## 六、嵌入模型与向量数据库

### 6.1 嵌入模型的选择

| 模型 | 维度 | 最大Token | 特点 | 适用场景 |
| --- | --- | --- | --- | --- |
| OpenAI text-embedding-3-small | 512/1536 | 8191 | 性价比高，维度可调 | 通用英文/多语言 |
| OpenAI text-embedding-3-large | 1024/3072 | 8191 | 精度最高 | 高精度需求 |
| BGE-M3 (BAAI) | 1024 | 8192 | 多语言，支持稠密+稀疏混合 | 中英文混合 |
| BGE-Large-zh (BAAI) | 1024 | 512 | 中文最优 | 纯中文场景 |
| E5-mistral-7b-instruct | 4096 | 32768 | 任务指令可调 | 需动态调整检索行为 |
| Cohere embed-multilingual-v3 | 1024 | 512 | 多语言，压缩效率高 | 多语言+大规模 |
| Nomic-embed-text | 768 | 8192 | 开源可复现，支持本地部署 | 离线/隐私需求 |

### 6.2 常用向量数据库深度对比

| 数据库 | 架构 | 索引算法 | 扩展性 | 特色 | 最佳场景 |
| --- | --- | --- | --- | --- | --- |
| **Chroma** | 嵌入式 | HNSW | 单机 | 零配置，API 简洁 | 原型验证、小项目 |
| **Milvus** | 云原生分布式 | IVF/HNSW/PQ | 十亿级 | GPU加速，多索引类型 | 企业级大规模 |
| **Qdrant** | Rust单机/集群 | HNSW | 百万-亿级 | 过滤查询极快 | 性能敏感 |
| **Pinecone** | 全托管云 | 自动选择 | 自动扩展 | 零运维，内置RAG | 快速上线 |
| **Weaviate** | Go/云原生 | HNSW+倒排 | 水平扩展 | 内置混合搜索+向量化 | 多模态 |
| **Elasticsearch** | Java/集群 | HNSW+BM25 | PB级文本 | 全文+向量混合 | ES生态集成 |
| **FAISS** | C++库 | 全部主流算法 | GPU集群 | Meta开源，极致性能 | 研究/离线批处理 |
| **Redis** | 内存+持久化 | HNSW(RediSearch) | 集群 | ms级延迟 | 缓存+实时检索 |

### 6.3 向量检索实操

```python
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# 入库
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

# 相似性搜索
results = vectorstore.similarity_search("什么是 RAG？", k=4)

# 带分数的相似性搜索
results_with_scores = vectorstore.similarity_search_with_relevance_scores(
    "什么是 RAG？", k=4
)

# MMR 搜索（最大边际相关，详见 7.2 节）
results = vectorstore.max_marginal_relevance_search(
    "什么是 RAG？", k=4, fetch_k=10, lambda_mult=0.5
)
```

---

## 七、检索策略

### 7.1 基础相似度检索

使用查询向量与文档库中所有文档向量之间的余弦相似度进行排序。

```
余弦相似度: cos(θ) = (A·B) / (||A|| × ||B||) = Σ(A_i × B_i) / √(ΣA_i²) × √(ΣB_i²)

取值区间 [-1, 1]，对于 LLM 嵌入通常为 [0, 1]
```

```python
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4}
)
```

### 7.2 MMR 检索（最大边际相关）

MMR（Maximal Marginal Relevance）解决了基础检索的"冗余问题"——当 Top-K 个检索结果高度相似时，LLM 看到的是重复信息。

**MMR 贪心选择公式**：

```
MMR(q, C, R, λ) = argmax_{d∈C\R} [ λ × sim(q, d) - (1-λ) × max_{r∈R} sim(d, r) ]

其中：
  q = 查询向量
  C = 候选文档集
  R = 已选文档集
  sim(q, d) = 文档与查询的相关性
  max sim(d, r) = 文档与已选文档集的"最大冗余度"
  λ = 相关性-多样性权衡参数
```

*   `λ=1`：退化为纯相似度排序
*   `λ=0`：选择与已选文档最不相似的新文档（最大化多样性）
*   `λ=0.5`：均衡（推荐默认值）

```python
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 4, "fetch_k": 20, "lambda_mult": 0.5}
)
```

### 7.3 多查询检索（Multi-Query）

多查询检索利用 LLM 的生成能力来缓解"查询-文档语义鸿沟"——用户可能用不精确的语言提问，多查询从不同角度重写问题，提高召回覆盖。

```python
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_openai import ChatOpenAI

retriever = MultiQueryRetriever.from_llm(
    retriever=base_retriever,
    llm=ChatOpenAI(model="gpt-4o", temperature=0),
)
```

**工作流程**：

1.  LLM 从用户问题生成 N 个不同角度的查询
2.  对每个查询分别检索 K 个文档
3.  合并所有结果并去重
4.  返回最相关的 Top-K

### 7.4 自查询检索（Self-Query）

自查询检索将自然语言查询转化为"语义向量搜索 + 结构化元数据过滤"的组合查询。其理论基础是：用户的很多提问包含隐含的过滤条件。

```
用户："2024年张三关于微服务的文章"
↓ LLM 解析
{
  "query": "微服务",           ← 用于向量搜索
  "filter": {                  ← 用于元数据过滤
    "author": "张三",
    "year": 2024
  }
}
```

```python
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo

metadata_field_info = [
    AttributeInfo(name="source", description="文档来源", type="string"),
    AttributeInfo(name="date", description="发布日期", type="string"),
    AttributeInfo(name="author", description="作者", type="string"),
]

retriever = SelfQueryRetriever.from_llm(
    llm=ChatOpenAI(model="gpt-4o"),
    vectorstore=vectorstore,
    document_contents="技术文档集合",
    metadata_field_info=metadata_field_info,
)
```

### 7.5 混合检索（Hybrid Search）

混合检索结合了稠密检索（语义匹配）和稀疏检索（关键词匹配，通常是 BM25）的优势：

*   **稠密检索**擅长捕捉语义相似性（"汽车" ≈ "轿车"）
*   **稀疏检索**擅长精确匹配专有名词、代码、编号（"RFC 2616"、"ErrorCode 503"）

**RRF（Reciprocal Rank Fusion）** 是最常用的融合算法：

```
RRF_score(d, q) = Σ_{r∈retrievers} 1 / (k + rank_r(d, q))

其中：
  rank_r(d, q) = 文档 d 在检索器 r 中的排名
  k = 平滑常数（通常 60），防止第一名权重过高
```

**RRF 为什么有效**：取倒数的设计使得排名靠前的文档获得显著更高的分数（#1 得分约 1/61，#100 得分约 1/160），同时不同检索器的排名尺度差异被自然规范化。

```python
# Elasticsearch 混合检索示例
from langchain_community.vectorstores import ElasticsearchStore
from langchain_elasticsearch import DenseVectorStrategy

db = ElasticsearchStore.from_documents(
    docs, embeddings,
    es_url="http://localhost:9200",
    index_name="docs",
    strategy=DenseVectorStrategy(hybrid=True),
)
```

### 7.6 重排序（Reranking）

重排序是两阶段检索架构的第二阶段：先用快速的双编码器粗排（Top-100），再用高精度的交叉编码器精排（Top-5）。

**为什么需要重排序**：

*   双编码器独立编码查询和文档，无法学习细粒度的交互模式
*   交叉编码器在 `[CLS] query [SEP] document [SEP]` 的联合输入上进行全注意力计算
*   精度提升通常为 10%-30%（取决于基准线）

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain_cohere import CohereRerank

compressor = CohereRerank(model="rerank-multilingual-v3.0", top_n=4)
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=base_retriever
)
```

### 7.7 检索策略决策矩阵

| 场景特征 | 推荐策略 | 原因 |
| --- | --- | --- |
| 文档<1K，问题简单 | 相似度检索 | 开销最小 |
| 文档冗余度高 | MMR | 增加结果多样性 |
| 用户提问不精确 | 多查询 | 提高召回覆盖 |
| 需要精确匹配（编号/代码） | 混合检索 | 语义+关键词互补 |
| 包含时间/作者等元数据 | 自查询 | 自动元数据过滤 |
| 高精度需求 | 重排序 | 精排提升相关性 |
| 需要多步推理 | 迭代检索(Self-Ask) | 按需逐步深入 |

---

## 八、完整 RAG 管线

```python
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers import ContextualCompressionRetriever
from langchain_cohere import CohereRerank

# 1. 加载文档
loader = DirectoryLoader("./docs/", glob="**/*.md", show_progress=True)
documents = loader.load()

# 2. 智能分片
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, chunk_overlap=50,
    separators=["\n\n", "\n", "。", ".", " ", ""]
)
chunks = text_splitter.split_documents(documents)

# 3. 向量化存储
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory="./db")

# 4. 多阶段检索
base_retriever = vectorstore.as_retriever(search_kwargs={"k": 20})
compressor = CohereRerank(model="rerank-multilingual-v3.0", top_n=5)
retriever = ContextualCompressionRetriever(
    base_compressor=compressor, base_retriever=base_retriever
)

# 5. Prompt 模板
prompt = ChatPromptTemplate.from_template("""基于以下上下文回答问题。如果无法回答，请说明不知道。

上下文：
{context}

问题：{question}

回答：""")

# 6. LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# 7. 组装链
def format_docs(docs):
    return "\n\n---\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

answer = rag_chain.invoke("什么是 RAG？")
```

---

## 九、RAG 效果评测

### 9.1 评测为什么难

RAG 评测的困难在于需要同时评估两个子系统的质量：

1.  **检索系统**：返回的文档是否相关、是否全面？
2.  **生成系统**：基于检索到的文档，生成的内容是否正确、忠实？

而且这两个子系统相互影响——检索错误会导致生成错误，反之则不一定。

### 9.2 检索质量指标

| 指标 | 公式 | 含义 |
| --- | --- | --- |
| **Hit Rate@K** |  | {relevant} ∩ {retrieved@K} |
| **MRR** | (1/ | Q |
| **Recall@K** |  | {retrieved@K} ∩ {relevant} |
| **Precision@K** |  | {retrieved@K} ∩ {relevant} |
| **NDCG@K** | DCG@K / IDCG@K | 考虑排序位置的归一化折扣累积增益 |

### 9.3 RAGAS 评测框架

RAGAS 是目前最流行的 RAG 端到端评测框架，定义了五个核心指标：

```python
from ragas import evaluate
from ragas.metrics import (
    faithfulness,          # 忠实度
    answer_relevancy,      # 答案相关性
    context_precision,     # 上下文精度
    context_recall,        # 上下文召回
    context_relevancy,     # 上下文相关性
)
from datasets import Dataset

eval_dataset = Dataset.from_dict({
    "question": ["什么是 RAG？", "RAG 有哪些优势？"],
    "answer": ["RAG 是检索增强生成...", "RAG 可以减少幻觉..."],
    "contexts": [
        ["RAG 全称 Retrieval-Augmented Generation..."],
        ["RAG 通过注入外部知识减少幻觉..."]
    ],
    "ground_truth": ["RAG 是...", "RAG 的优势包括..."]
})

result = evaluate(eval_dataset, metrics=[
    faithfulness, answer_relevancy,
    context_precision, context_recall, context_relevancy,
])
print(result)
```

### 9.4 指标深度解析

**Faithfulness（忠实度）**：回答是否完全基于检索到的上下文。这是**RAG最重要的指标**。

*   计算方法：将回答拆解为原子声明 → 逐条检查是否在上下文中有原文支撑
*   分数 = 有支撑的声明数 / 总声明数
*   低忠实度 = 模型在"编造"（幻觉）

**Context Precision（上下文精度）**：检索到的文档中，相关文档是否排在靠前位置。

*   CP@k = Σ(Precision@i × Relevance\_i) / 总相关文档数，i 从 1 到 k
*   高精度 = 不相关文档没有污染 Top-K

**Context Recall（上下文召回）**：标准答案所需的信息，检索系统找回了多少。

*   召回率 = 检索到的相关文档数 / 标准答案引用的文档总数
*   低召回 = 关键信息没被检索到

**Answer Relevancy（答案相关性）**：答案是否切题。

*   通过从答案反向生成伪问题，检查伪问题与原问题的语义相似度
*   低相关性 = 答非所问

### 9.5 评测最佳实践

1.  **构建分层测试集**：简单问答、复杂推理、多跳问题、边界情况各 20-30 条
2.  **多指标同时评估**：单一指标容易"刷分"，多指标交叉验证
3.  **人工抽检 20%**：自动化指标与人工判断仍有差距，定期抽检校准
4.  **A/B 测试**：在线对比不同分片策略 / 检索算法 / Prompt 的实际效果
5.  **持续监控**：数据分布变化会导致 RAG 效果退化（Data Drift）

---

## 十、高级 RAG 优化策略

### 10.1 HyDE（Hypothetical Document Embedding）

**核心洞察**：用户问题通常很短而文档很长，导致查询向量和文档向量在嵌入空间中分布不匹配。HyDE 先让 LLM 生成一个"假设性答案文档"，用这个假设文档的向量去检索——因为假设文档与实际文档在嵌入空间中更接近。

```
用户问题 → LLM 生成假设答案 → 嵌入假设答案 → 向量检索 → 返回真实文档
```

### 10.2 Small-to-Big / Parent Document Retriever

**核心洞察**：小的检索片段（200 token）适合精确匹配，但缺少足够上下文供 LLM 回答；大的返回片段（1000 token）提供丰富上下文，但精确匹配效果差。

**解决方案**：两个独立的分片器——小片段用于向量检索，检索到小片段后，返回其所属的大片段（父文档）。

```python
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore

retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=InMemoryStore(),
    child_splitter=RecursiveCharacterTextSplitter(chunk_size=200),
    parent_splitter=RecursiveCharacterTextSplitter(chunk_size=1000),
)
```

### 10.3 查询路由（Query Routing）

当知识库包含多种类型的数据时（代码库 + 文档 + FAQ），不同查询需要不同的检索策略。查询路由根据问题类型将查询分发到不同的检索管道。

### 10.4 Graph RAG（知识图谱增强 RAG）

将文档中的实体和关系提取为知识图谱，检索时进行图遍历发现间接关联。适合需要理解实体间复杂关系的任务（如法律案例分析、药物相互作用查询）。

### 10.5 多阶段检索架构总结

```
用户查询
   │
   ▼
查询理解层（重写/分解/意图分类）
   │
   ▼
第一阶段检索（双编码器，快速粗排 Top-100）
   │
   ▼
第二阶段检索（交叉编码器/BM25，精排 Top-10）
   │
   ▼
上下文压缩（LLM 提取最相关句，输出 Top-5）
   │
   ▼
LLM 生成（基于精选上下文）
```

---

## 十一、总结：RAG 调优决策树

```
是否需要 RAG？
 ├── 是 → 数据来源分析
 │    ├── 结构化数据（DB）→ Self-Query 检索
 │    ├── 非结构化文档 → 选择分片策略
 │    │    ├── 长文本/报告 → RecursiveCharacter Splitter (chunk_size=500-1000)
 │    │    ├── 代码 → 语言感知分片（保留函数完整性）
 │    │    ├── 对话/FAQ → 按 Q&A 对分片
 │    │    └── 语义完整性优先 → Semantic Chunking
 │    └── 多模态（文本+表格+图片）→ 分别处理 + 元数据关联
 │
 ├── 检索精度不足？
 │    ├── 查询不精确 → Multi-Query / HyDE
 │    ├── 专有名词漏检 → 混合检索（Hybrid = Dense + BM25）
 │    ├── 结果冗余 → MMR
 │    ├── 缺失结构化过滤 → Self-Query
 │    └── 精度依然不足 → Reranker（Cohere/BGE-Reranker）
 │
 └── 生成质量不足？
      ├── 幻觉 → 检查 Faithfulness 指标，降低温度，优化 Prompt
      ├── 信息不全 → 增大 k 值，减小 chunk_size，增加 overlap
      ├── 答非所问 → 优化 Prompt 模板，添加"不知道就说不知道"
      └── 整体质量差 → 升级嵌入模型，使用更强的 LLM
```

## 相关条目
- [[Agent搭建]]
- [[面试]]
- [[langchain4j-study-notes-02-rag]]
- [[多智能体与记忆机制]]
