# Knowledge Acquisition During Pre-training? Large Language Models Learn Better With Auxiliary Views — 抓取记录

- **标题：** Knowledge Acquisition During Pre-training? Large Language Models Learn Better With Auxiliary Views
- **作者：** Joseph Lee、Yidi Huang、Dokyoon Kim、Shu Yang、Li Shen（† 通讯作者）
- **机构：** 宾夕法尼亚大学（University of Pennsylvania, Philadelphia, PA, USA）
- **arXiv：** [2609.04180](https://arxiv.org/abs/2609.04180)（cs.CL；cross-list cs.AI）
- **版本历史：** v1 2026-09-03（本抓取按 v1）
- **来源：** https://arxiv.org/abs/2609.04180
- **许可：** CC BY 4.0
- **性质：** 学术论文（摘要 + 正文 9 节 + 局限 + 致谢 + 参考文献 + 附录 A–G）
- **抓取：** 2026-09-12，先用 `curl` 抓 abs 页核对标题/作者/日期/版本/许可等元数据，再用 firecrawl `scrape -f markdown --only-main-content` 抓 v1 HTML 全文 Markdown
- **全文：** `candidates/20260912-080217/sources/Knowledge-Acquisition-During-Pre-trainin-full.md`（约 140 KB，v1 全文，含表格、图内外链；附录 F/G 的提示词原文含 base64 附件，译文从略）
- **官方中文版：** 无；译文以 v1 英文原文为唯一原文
- **代码/数据：** 数据集 https://huggingface.co/datasets/jiosephlee/auxiliary-views-knowledge-acquisition ；代码 https://github.com/jiosephlee/auxiliary-views-knowledge-acquisition

---

## 摘要（v1 原文）

Gaps remain in our understanding of how large language models (LLMs) acquire knowledge during pre-training. We posit that auxiliary views, reformulations of knowledge, are causally helpful for learning. We design controlled experiments to isolate this. First, we confirm that repetition is necessary for acquisition and clarify that paraphrasing helps only at smaller batch sizes. Second, holding the token budget fixed, allocating tokens from document repetition to auxiliary views improves learning, counterintuitively, even for factual recall. Third, the effectiveness of auxiliary views is not contingent on the strength of the teacher model that generates them. Fourth, we identify forms of knowledge, contextual and foundational, that aid learning in the presence of prior knowledge gaps. Finally, we examine how these effects manifest mechanistically via layer-wise biases and compression. Together, our findings suggest that auxiliary representations of knowledge, which arise naturally in large pre-training corpora, are a key factor in the success of pre-training and offer a plausible explanation for why data diversity matters.

## 关键词

辅助视角（auxiliary views）、预训练、持续预训练、知识获取、复述（paraphrasing）、重复、批量大小、教师模型强度、上下文知识、前置知识、层间偏置、参数压缩、数据多样性、OLMo-2

## 元数据核对

- abs 页 `citation_title`、`citation_author`（5 人）、`citation_date`（2026/09/03）、`citation_arxiv_id`（2609.04180）、`description` 与 v1 正文首页一致
- 提交历史：v1 Thu, 3 Sep 2026 17:57:02 UTC (708 KB)；`references/articles.md` 队列登记日期为 2026-09-06（采集入库日），二者不冲突
- 主学科 cs.CL，交叉 cs.AI；正文首页标注 `arXiv:2609.04180v1 [cs.CL] 03 Sep 2026`、`License: CC BY 4.0`
- 官方 author 列表：Joseph Lee, Yidi Huang, Dokyoon Kim, Shu Yang, Li Shen；通讯作者 Li Shen（正文脚注）
- 图表：Figure 1–12、Table 1–13；`full` 文件中保留图片外链（如 `aux_base_minus_source_base_cosine_distance_all_projections.png`、`1B_delta_parameters.png` 等）
- 关键数字锚点：36 篇文档（3 领域 × 12）、49 条复述/篇、1764 条复述、6,435 条 factual + 430 条 inference 探针、200 条人工验证/类、N=100 次注入、Para. 9 + Aux. ≫ Para. 9 ≫ Source、模型 1B/7B/13B/32B
