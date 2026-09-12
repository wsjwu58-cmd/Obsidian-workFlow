# Clean Engineering, Unstable Measurement — 抓取记录

- **标题：** Clean Engineering, Unstable Measurement: A Preregistered Reliability Failure of Black-Box LLM Observers on Shared Endpoints
- **作者：** Haoyuan Zhu（hzhu51@sheffield.ac.uk）、Jie Zhang（jie.zhang@ranplanwireless.com，通讯作者）
- **机构：** School of Electronic and Electrical Engineering, University of Sheffield, Sheffield S10 2TN, UK；R&D Department, Ranplan Wireless Network Design Ltd., Cambridge CB23 3UY, UK；R&D Department, Cambridge AI+ Ltd., Cambridge CB23 3UY, UK
- **arXiv：** [2609.04198](https://arxiv.org/abs/2609.04198)（cs.AI；cs.LG）
- **版本：** v1（2026-09-03 在线提交，本抓取按 v1）
- **来源：** http://arxiv.org/abs/2609.04198v1
- **许可：** arXiv.org perpetual, non-exclusive license（作者保留版权）
- **性质：** 学术论文（摘要 + 正文 13 节 + 参考文献 + 附录 A–D）
- **抓取：** 2026-09-12，先用 `curl` 抓取 abs 页核对标题/作者/日期/版本；直接 `curl` 抓取 v1 HTML 全文，再用 firecrawl `scrape -f markdown --only-main-content` 抓取 v1 正文 Markdown
- **全文：** `candidates/20260912-080217/sources/Clean-Engineering-Unstable-Measurement-A-full.md`（约 128 KB，v1 全文，含表格、公式 alt 文本与内部引用链接）
- **官方中文版：** 无；译文以 v1 英文原文为唯一原文

---

## 摘要（v1 原文）

Language-model judges now gate training data, score generations, and drive leaderboards. The judge is then a measurement instrument, resting on one rarely stated assumption: the same request, sent to the same model name, reads the same tomorrow. We audited that assumption in two preregistered campaigns with every threshold fixed in advance; neither got past validating its instrument. Across 52,988 audited request attempts, same-window repeat rankings agreed at Spearman 0.400 against a required 0.90, and byte-identical next-day replays agreed at 0.78 against a required 0.99, each time with the execution record at ceiling. Three mechanisms explain the gap: a label-to-meaning mapping that biased readouts as strongly as the signal; candidate gaps seven orders of magnitude below the instrument's own noise floor; and byte-identical inputs returning different rankings, a noise that exact-permutation readouts compound. Neither metric substitution nor sampling repaired it on the tested grid. Preregistered follow-ups bound the problem: waiting did not help on the days sampled (0.805 versus 0.800, replicated over five further days); switching providers did not help (four providers share the floor, medians 0.74 to 0.88, predicted by none of the metadata fields they expose); self-hosting on batch-invariant kernels helped only while the server was quiet; and on constructed errors with known gaps, the readout's separation tracks error type, not size. We distill the evidence into a three-level snapshot-identity ladder, eight design rules, and a reporting checklist; a pilot at roughly 2% of the study's call volume would have exposed both unreachable gates in advance. All results concern externally measured behaviour on shared serving infrastructure. On a shared endpoint, a model name is not a frozen instrument; a preregistered evaluation must measure its instrument before freezing any gate on it.

## 关键词

LLM-as-judge、测量可靠性、预注册、可复现性、快照身份、推理端点非确定性、批不变核、Spearman 秩相关、元数据指纹、审计链

## 元数据核对

- abs 页 `citation_title` / `citation_author` / `citation_date` / `citation_online_date` / `citation_arxiv_id` 与 v1 正文首页一致（提交日期 2026-09-03）
- 作者字段 abs 页误拼为 “Haoyaun Zhu”，v1 正文首页为 “Haoyuan Zhu”，译文按正文首页
- v1 正文声称的关键数字：52,988 次请求尝试、Spearman 0.400（门槛 0.90）、次日字节复现 0.78（门槛 0.99）、748,000 次模拟设计 0/500 通过、四提供方中位数 0.74–0.88、自托管并发负载下分歧上升 8.4 倍
- 图表：Figure 1–6 与 Table 1–2（含 A–D 附录表）；HTML 未含可提取的外链图片文件，图注以文字保留
