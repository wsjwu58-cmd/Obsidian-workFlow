# Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning — 抓取记录

- **标题：** Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning
- **作者：** Ye-Chan Kim、Seunghee Choi、SeungJu Cha、Si-Woo Kim、Hwiseon Kim、Hyungee Kim、Dong-Jin Kim（† 通讯作者）
- **机构：** 韩国汉阳大学（Hanyang University, South Korea）
- **arXiv：** [2609.04183](https://arxiv.org/abs/2609.04183)（cs.CV；cross-list cs.AI）
- **版本历史：** v1 2026-09-03（本抓取按 v1）
- **来源：** https://arxiv.org/abs/2609.04183
- **许可：** CC BY 4.0
- **性质：** 学术论文（摘要 + 正文 5 节 + 局限 + 致谢 + 参考文献 + 附录 A–C）
- **抓取：** 2026-09-12，先用 `curl` 抓 abs 页核对标题/作者/日期/版本/许可等元数据，再用 firecrawl `scrape -f markdown --only-main-content` 抓 v1 HTML 全文 Markdown
- **全文：** `candidates/20260912-080217/sources/Seeing-Before-Synthesizing-VLM-Guided-Tr-full.md`（约 84 KB，v1 全文，含表格、公式 alt 文本与图内外链）
- **官方中文版：** 无；译文以 v1 英文原文为唯一原文
- **代码/项目页：** abs 页与正文均未给出开源仓库链接

---

## 摘要（v1 原文）

Weakly-Supervised Dense Video Captioning aims to localize and describe multiple events in untrimmed videos given only an ordered set of event-level captions per video. Recent work synthesizes auxiliary transition captions via LLM to provide additional vision-language alignment, but these captions lack visual grounding and are rigidly assigned to every inter-event gap at a fixed location and duration. To address these, we propose Seeing Before Synthesizing (SBS), a framework that adaptively provides visually grounded linguistic guidance only where warranted. Leveraging a VLM, we generate frame-level narratives for the inter-event gaps and detect transitions from the semantic variation across them. For identified transitions, we then refine inter-event temporal masks by blending the temporal midpoint with the semantic change point and selecting the width that maximizes vision-language alignment. Experiments on ActivityNet Captions and YouCook2 demonstrate state-of-the-art performance in both captioning and localization.

## 关键词

弱监督密集视频描述（WSDVC）、过渡事件、VLM 引导、帧级叙述、自适应门控、自适应事件间掩码、语义变化点、高斯掩码、视觉-语言对齐、ActivityNet Captions、YouCook2

## 元数据核对

- abs 页 `citation_title` / `citation_author`（7 人）/ `citation_date` / `citation_online_date` / `citation_arxiv_id` 与 v1 正文首页一致
- `citation_date` 与 `citation_online_date` 均为 `2026/09/03`；`references/articles.md` 队列登记日期为 2026-09-06（采集入库日），二者不冲突
- 主学科 cs.CV，交叉 cs.AI；正文正文首页标注 `arXiv:2609.04183v1 [cs.CV] 03 Sep 2026`、`License: CC BY 4.0`
- 正文声称的关键数字：ActivityNet 上 CIDEr 36.87 / F1 58.18、YouCook2 上 CIDEr 16.28 / F1 22.17；消融全开 36.87/58.18；门控人工验证集 95 个间隙（36 有 / 59 无），门控 F1 69.23；训练开销 1H 52M 53S / 7M 51S / 33.13 GiB
- 图表：Figure 1–4、Table 1–9、Table A.1、Figure A.1–A.2；图片外链（teaser_0526_sh.png、main_fig.png、Interevent_qual_sh_0526_final.png、anet_suppl.png、yc2_suppl.png）与 Figure 4 的 SVG（text_peak_2.svg）在 full 文件中保留
