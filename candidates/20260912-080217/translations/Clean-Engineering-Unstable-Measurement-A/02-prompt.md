---
created: 2026-09-12
updated: 2026-09-12
type: prompt
status: 本次使用
sources:
  - http://arxiv.org/abs/2609.04198v1
tags: [翻译提示词, arxiv, LLM-as-judge, 测量可靠性, 候选加工]
---

# 02 本次翻译使用的提示词

> 说明：本文件记录 2026-09-12 加工本条候选时实际使用的翻译提示词。按产出边界，
> 该提示词只落在 `translations/<slug>/`，**不写入 `prompts/`**；如后续经评审与实测
> 证明可复用，再由人工决定是否沉淀到 `prompts/`。

## 系统角色

你是一位严谨的学术翻译，负责把一篇英文 arXiv 测量方法学论文完整翻译为中文，
供中文工程读者阅读。你熟悉 LLM 评测、统计测量学与可复现性工程。

## 翻译任务提示词

```text
把以下论文完整翻译为简体中文，写成一个 Markdown 文件。

原文：sources/Clean-Engineering-Unstable-Measurement-A-full.md
输出：translations/Clean-Engineering-Unstable-Measurement-A/translation.md

硬性要求：
1. 完整逐译：摘要、第 1–13 节、附录 A–D 全部翻译；不得跳节、不得缩写正文。
   参考文献（References）按学术惯例保留英文原样，不逐条翻译。
2. 术语到位（首次出现给中英对照，之后用中文）：
   LLM-as-judge 译为「LLM 判官」；preregistration 译为「预注册」；
   instrument 在测量语境译为「仪器 / 测量仪器」；readout 译为「读出」；
   noise floor 译为「噪声底线」；measurand 译为「测量对象」；
   snapshot identity 译为「快照身份」；audit chain 译为「审计链」；
   Spearman 保留 Spearman，加「秩相关」；permutation 译为「排列」；
   top-1 agreement 译为「top-1 一致率」；pairwise agreement 译为「成对一致率」；
   batch-invariant kernels 译为「批不变核」；fail-closed 译为「失效即拒绝」；
   equivalence band 译为「等价带」；detection limit 译为「检出限」；
   operating characteristic 译为「工作特性」；nonzero/nondeterminism 统一为「非确定性」。
3. 超链接保留：原文中的 Markdown 链接（尤其 arXiv HTML 的 bib.bibNN 引用链接与
   vendor 文档链接）原样保留，不改写、不删除。
4. 公式与数字：
   - firecrawl 抓取的 LaTeXML 数学存在双重渲染（如 `0.920.92`、`≥\\geq`、
     `zsym=(z(+)+z(−))/2z\_{\\mathrm{sym}}=...`），一律还原为可读记法：
     z_sym、b_map、ε = 10⁻⁴、|Δr_sym|、Spearman ≥ 0.90、3.04×10⁻¹⁰ 等；
   - 所有数字零改动，逐字核对；原文自相矛盾处按原文分别保留并加译者注；
   - 表格完整保留，表头如有英文缩写（p01、q95、SE、OC 等）首次出现给出中文对照。
5. 图注：Figure 1–6 的文字图注完整翻译；HTML 中无可提取的外链图片，保留图注文字即可。
6. 风格：学术语体，准确、简洁；长句按中文习惯拆分；不加入原文没有的评论，
   必要的澄清以「译者注：」标注并与原文区分。
7. frontmatter：
   ---
   created: 2026-09-12
   updated: 2026-09-12
   title: 洁净工程，不稳测量：共享端点上黑箱 LLM 观察者的预注册可靠性失败
   sourceUrl: http://arxiv.org/abs/2609.04198v1
   sourceAuthor: Haoyuan Zhu、Jie Zhang（谢菲尔德大学；Ranplan Wireless / Cambridge AI+）
   translatedAt: 2026-09-12
   sources: [references/articles.md 待处理队列]
   tags: [LLM判官, 测量可靠性, 预注册, 可复现性, 非确定性, 批不变核, 快照身份, 审计链, type/翻译]
   ---
8. 输出到 translation.md 后，把同一内容写入
   works-ready/Clean-Engineering-Unstable-Measurement-A-translation.md。
```

## 执行备注

- **关键数字比对**（已在译文抽查，与 v1 原文一致）：52,988、0.400 vs 0.90、
  0.78 vs 0.99、748,000 / 0-of-500、0.005、8.4×、0.74–0.88、31/32、3,060、
  0.006710、3.04×10⁻¹⁰、0.9872 / 0.8925、0.7604–0.9860。
- **公式还原**：`z_sym = (z⁺ + z⁻)/2`、`b_map = (z⁺ − z⁻)/2`、
  `r = e^{ℓ⁺}/(e^{ℓ⁺} + e^{ℓ⁻})`、`ε = 10⁻⁴`、`p̂ = (m + ½)/(M + 1)`。
- **术语锁定**：instrument→仪器；readout→读出；noise floor→噪声底线；
  measurand→测量对象；permutation→排列；snapshot identity→快照身份。
- 该提示词本身不沉淀进 `prompts/`（curate 产出边界：不写 prompts/），
  留待评审通过、实测后再考虑复用。
