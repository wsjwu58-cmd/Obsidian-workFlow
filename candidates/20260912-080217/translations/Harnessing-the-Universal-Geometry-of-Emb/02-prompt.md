---
created: 2026-09-12
updated: 2026-09-12
type: translation-prompt
status: 已执行
sources:
  - title: Harnessing the Universal Geometry of Embeddings
    url: https://arxiv.org/abs/2505.12540
    source: hn
    date: 2026-09-06
tags: [翻译提示词, 文本嵌入, 向量空间, 无监督翻译, 论文翻译]
---

# 02 翻译提示词：Harnessing the Universal Geometry of Embeddings

## 使用的输入

> 原文全文（v4）已抓取到
> `candidates/20260912-080217/sources/Harnessing-the-Universal-Geometry-of-Emb-full.md`
> （firecrawl 主内容抓取，含 Table 1–11、Figure 1–8 外链、公式 alt 文本；abs 页与 v4 HTML 元数据经 curl 核对）。

## 提示词正文

```
你是一名资深技术译者（英→中），翻译康奈尔大学论文
《Harnessing the Universal Geometry of Embeddings》（arXiv:2505.12540v4，
2026-01-26 更新，https://arxiv.org/abs/2505.12540）。作者 Rishi Jha、Collin Zhang、
Vitaly Shmatikov、John X. Morris。原文研究「无配对数据的文本嵌入空间翻译」。

## 输入
- 原文：candidates/20260912-080217/sources/Harnessing-the-Universal-Geometry-of-Emb-full.md
  （正文从 "# Harnessing the Universal Geometry of Embeddings" 标题行开始，
   到 "## NeurIPS Paper Checklist" 之前结束；参考文献只保留 [n] 记号，
   不逐条翻译 70 条书目；附录 A–H 要点全译，检查表只摘与可复现性/伦理相关条目。）

## 输出要求
1. 完整逐译：摘要、第 1–9 节、致谢；表格与图注完整保留（Table 1–7 正文表，
   Table 8/9 附录表；Table 10/11 完整 OOD 大表用「要点 + 代表行」方式呈现并说明来源）。
   不压缩正文论述，不删节小节标题。
2. 保留全部图片外链与代码仓库链接：
   diagram.png、spaces.png、cosine_heatmaps.png、enron_heatmap.png、tweettopic_heatmap.png、
   https://github.com/rjha18/vec2vec、https://arxiv.org/abs/2505.12540。
   论文内引用保留为 [n]（完整参考书目见 arXiv 页面）。
3. 公式与符号：把 LaTeXML 双重渲染的数学还原为可读记法——
   M₁/M₂、u_i/v_i、F(u_i)、T(A₁(u_i))、θ={A₁,A₂,T,B₁,B₂}、
   L_adv、L_GAN、L_rec、L_CC、L_VSP、λ_gen/λ_rec/λ_CC/λ_VSP；
   张量维度的 ℝ^d、ℝ^Z 用 Unicode 上标；公式用行内 `$...$` 或代码块呈现。
   4.2 节的均值余弦公式按原文如实保留（含 `1 − cos`），不得自作主张改成
   `cos`，并在译文表格上方加一个「译者注」提示该处记号可能有误。
4. 术语表（必须一致）：
   - text embedding → 文本嵌入；embedding space → 嵌入空间；vector space → 向量空间
   - unsupervised embedding translation → 无监督嵌入翻译
   - paired data → 配对数据；encoder → 编码器；decoder → 解码器
   - adversarial loss → 对抗损失；GAN → 生成对抗网络（GAN）
   - cycle consistency → 循环一致性；reconstruction → 重建
   - vector space preservation (VSP) → 向量空间保持（VSP）
   - latent space / latent representation → 潜空间 / 潜表示（与「隐空间」择一，全文统一用「潜空间」）
   - input/output adapter → 输入/输出适配器；shared backbone → 共享主干
   - optimal transport / optimal assignment → 最优传输 / 最优分配
   - Hungarian algorithm → 匈牙利算法；Earth Mover's Distance → 推土机距离（EMD）
   - Gromov-Wasserstein → Gromov-Wasserstein；Sinkhorn → Sinkhorn
   - attribute inference → 属性推断；embedding inversion → 嵌入反转
   - zero-shot → 零样本；top-1 accuracy → Top-1 准确率；mean rank → 平均排名
   - out-of-distribution → 分布外；in-distribution → 分布内
   - multimodal → 多模态；modality → 模态；backbone → 主干
   - Platonic Representation Hypothesis → 柏拉图表示假说
   - retrieval → 检索；RAG → 检索增强生成（RAG）；clustering → 聚类
   - recall@16 → Recall@16；LLM judge → LLM 评判器
   - model family → 模型族；parameter count → 参数量
   模型名保留原文小写记号：gtr、clip、e5、gte、stella、granite、qwen；
   数据集名保留：Natural Questions (NQ)、TweetTopic、MIMIC-III、Enron Email Corpus、
   MS COCO；首次出现补中文说明。
5. 数字与结论逐一比对原文，不得改动：
   0.96（引言声称的最高余弦）、0.92/0.91/0.87（Table 2 最大值）、8000+、22M、65536、
   8192、800、19 主题、2673 MedCAT、50 封邮件、80% 邮件 / 67% 推文、
   10K/50K/100K/500K/1M 数据量、25 完整 + 30 部分模型、约 176 GPU 天、42 GPU 小时、
   45 CPU 小时、Qwen3 4000M 参数 / 2560 维 / 32K 上下文 / 比 GTE 大 37 倍、
   种子 14/15 与 3/15、R@16 0.23 vs 0.75。
   引言 0.96 与正文表格 0.92 的不一致：不得抹平，按原文分别保留。
6. 输出 Markdown，标题层级沿用原文（标题 + 九个 ## 节 + 附录 A–H），
   frontmatter：
   ---
   created: 2026-09-12
   updated: 2026-09-12
   title: 利用嵌入的普适几何
   sourceUrl: https://arxiv.org/abs/2505.12540
   sourceAuthor: Rishi Jha、Collin Zhang、Vitaly Shmatikov、John X. Morris（康奈尔大学）
   translatedAt: 2026-09-12
   sources: [references/articles.md 待处理队列]
   tags: [文本嵌入, 向量空间, 无监督翻译, 对抗学习, 循环一致性, 向量数据库安全, 属性推断, 嵌入反转, type/翻译]
   ---
7. 风格：学术论文语体，简洁准确，长句按中文习惯适度拆分；不加入原文没有的评论；
   表格中的英文表头（M1/M2、cos(·)、T-1、Rank）在首次表格里给出中文对照，
   后续沿用 `M₁`/`M₂`/`cos(·)`/`Top-1`/`Rank`。
```

## 执行备注

- 抓取方式：`curl` 抓 abs 页与 v4 HTML 核对 `<title>`、`citation_author`、`citation_date`、
  `citation_online_date`、`citation_arxiv_id`、许可；firecrawl 抓 v4 正文 Markdown。
- 翻译策略：正文完整逐译 + 表格数字零改动；公式做可读化还原（不改语义）；
  引用保留 [n]；附录要点全译。
- 关键数字比对：0.96/0.92/0.91/0.87、8000+、22M/65536/8192/800、19/2673、50、80%/67%、
  10K/50K/1M、176 GPU 天、Qwen3 4000M/2560/32K、14/15 与 3/15、R@16 0.23/0.75
  已在译文抽查，与 v4 原文一致；引言 0.96 与 Table 2 的 0.92 差异按原文保留并加译者注。
- 该提示词本身不直接沉淀进 prompts/（curate 产出边界：不写 prompts/），
  留待评审通过、实测后再考虑复用。
