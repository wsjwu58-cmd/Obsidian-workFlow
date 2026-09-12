# Harnessing the Universal Geometry of Embeddings — 抓取记录

- **标题：** Harnessing the Universal Geometry of Embeddings
- **作者：** Rishi Jha、Collin Zhang、Vitaly Shmatikov、John X. Morris
- **机构：** Department of Computer Science, Cornell University
- **arXiv：** [2505.12540](https://arxiv.org/abs/2505.12540)（cs.LG）
- **版本历史：** v1 2025-05-18；v2 2025-05-20；v3 2025-06-25；v4 2026-01-26（**本抓取按最新版 v4**）
- **来源：** https://arxiv.org/abs/2505.12540
- **代码：** https://github.com/rjha18/vec2vec
- **许可：** CC BY 4.0
- **性质：** 学术论文（摘要 + 正文 9 节 + 致谢 + 参考文献 + 附录 A–H + NeurIPS Paper Checklist）
- **抓取：** 2026-09-12，先用 `curl` 抓取 abs 页与 v4 HTML 核对标题/作者/日期/版本/许可等元数据，再用 firecrawl `scrape -f markdown --only-main-content` 抓取 v4 全文 Markdown
- **全文：** `candidates/20260912-080217/sources/Harnessing-the-Universal-Geometry-of-Emb-full.md`（约 87 KB，v4 全文，含表格、公式 alt 文本与内部引用链接）
- **官方中文版：** 无；译文以 v4 英文原文为唯一原文

---

## 摘要（v4 原文）

We introduce the first method for translating text embeddings from one vector space to another without any paired data, encoders, or predefined sets of matches. Our unsupervised approach translates any embedding to and from a universal latent representation (i.e., a universal semantic structure conjectured by the Platonic Representation Hypothesis). Our translations achieve high cosine similarity across model pairs with different architectures, parameter counts, and training datasets.

The ability to translate unknown embeddings into a different space while preserving their geometry has serious implications for security. An adversary with access to a database of only embedding vectors can extract sensitive information about underlying documents, sufficient for classification and attribute inference.

## 关键词

text embeddings、embedding translation、unsupervised translation、adversarial learning、cycle consistency、vector space preservation、Platonic Representation Hypothesis、vector database security、attribute inference、embedding inversion

## 元数据核对

- abs 页 `citation_title` / `citation_author` / `citation_date` / `citation_online_date` / `citation_arxiv_id` 与 v4 正文首页一致
- v4 正文声称的关键数字：余弦相似度最高 0.96、8000+ 洗牌嵌入完美匹配、平均排名低至 1、零样本反转对部分模型对可提取 80% 邮件 / 67% 推文信息
- 图表：Figure 1–8 与 Table 1–11；图片外链（diagram.png、spaces.png、cosine_heatmaps.png、enron_heatmap.png、tweettopic_heatmap.png）在 full 文件中保留
