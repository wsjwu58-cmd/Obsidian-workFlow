---
created: 2026-09-12
updated: 2026-09-12
type: translation-prompt
status: 已执行
sources:
  - title: Knowledge Acquisition During Pre-training? Large Language Models Learn Better With Auxiliary Views
    url: http://arxiv.org/abs/2609.04180v1
    source: arxiv
    date: 2026-09-06
tags: [翻译提示词, 辅助视角, 预训练, 知识获取, 论文翻译]
---

# 02 翻译提示词：Knowledge Acquisition During Pre-training?

## 使用的输入

> 原文全文（v1）已抓取到
> `candidates/20260912-080217/sources/Knowledge-Acquisition-During-Pre-trainin-full.md`
> （firecrawl 主内容抓取，含 Figure 1–12 图注、Table 1–13 与外链；附录 F/G 的提示词原文含 base64 附件，译文从略）。

## 提示词正文

```
你是一名资深技术译者（英→中），翻译宾夕法尼亚大学论文
《Knowledge Acquisition During Pre-training? Large Language Models Learn Better
With Auxiliary Views》（arXiv:2609.04180v1，2026-09-03，
https://arxiv.org/abs/2609.04180）。作者 Joseph Lee、Yidi Huang、Dokyoon Kim、
Shu Yang、Li Shen（宾夕法尼亚大学）。论文通过可控实验研究预训练中「知识该以何种
形式表示」，提出 auxiliary views（同一知识的多样化改写：博客、问答、教科书）比
单纯复述/重复更能促进知识获取。

## 输入
- 原文：candidates/20260912-080217/sources/Knowledge-Acquisition-During-Pre-trainin-full.md
  （正文从 "# Knowledge Acquisition During Pre-training?" 标题行开始，到 References
   之前结束；参考文献不逐条翻译，只保留正文的作者-年份引用；附录 A–E 全译，
   附录 F/G 为提示词原文，仅作说明不逐字翻译。）

## 输出要求
1. 完整逐译：摘要、第 1–9 节、Acknowledgements、Limitations；附录 A（数据构建与
   合成数据统计）、附录 B（探针生成）、附录 C（补充图）、附录 D（补充表）、
   附录 E（超参与复现细节）完整保留；附录 F/G 只译标题并说明其内容为提示词清单
   （原文包含大量 base64 附件，不逐字搬运）。不压缩正文论述，不删节小节标题。
2. 保留全部图片外链与链接：Figure 1–12 图注、Hugging Face 数据集链接
   https://huggingface.co/datasets/jiosephlee/auxiliary-views-knowledge-acquisition 、
   代码链接 https://github.com/jiosephlee/auxiliary-views-knowledge-acquisition 、
   论文页 https://arxiv.org/abs/2609.04180。正文引用保留作者-年份形式
   （如 Chang et al. (2024)），完整参考书目见 arXiv 页面。
3. 公式与符号：把 LaTeXML 双重渲染的数学还原为可读记法——
   L(θ) = −Σ_{m=1}^{M} Σ_{i=1}^{n_m} log P(t_{m,i} | t_{m,<i}; θ)、
   C_K = { d_i ∈ C | d_i 含关于 K 的信息 }、N=100、Para. M 每 (M+1) 个批次循环一次、
   β log Z(x)、π*、r=−0.14（n=6）、r=−0.24（n=10, p=0.50）、r=+0.62（p≈0.04）。
   公式用行内 `$...$` 或代码块呈现，下标/上标用 Unicode 或 LaTeX 记法，全文统一。
4. 术语表（必须一致）：
   auxiliary view→辅助视角；view→视角；paraphrase→复述；
   continued pre-training (CPT)→持续预训练；single-batch knowledge injection→单批次知识注入；
   token-matched→token 匹配；upsampling→上采样；factual probe→事实探针；
   inference probe→推理探针；cloze statement→完形填空式陈述；
   multiple-choice question (MCQ/MCQA)→多项选择题/多选问答；
   log probability→对数概率；target rank→目标词排名；teacher model/generator→教师模型/生成器；
   contextual knowledge→上下文知识；prerequisite/foundational knowledge→前置知识/基础知识；
   prior-knowledge gap→先验知识缺口；layer-wise bias→层间偏置；
   feed-forward network (FFN)/MLP channel→前馈网络/MLP 通道；
   gate/up/down projection→门控/升维/降维投影；relative delta norm→相对增量范数；
   cosine distance→余弦距离；Gini coefficient→基尼系数；compression→压缩；
   key–value memory→键值记忆；distillation→蒸馏；data augmentation→数据增强；
   lexical bias→词汇偏置；frequency/coverage→频率/覆盖率；
   pre-training-faithful setting→预训练保真设置。
   专有名词保留英文：OLMo-2、DCLM、Infini-gram、LAMA、Qwen-2.5、GPT-4.1、
   gpt-5-mini、gpt-oss、Gemma、GLM、TRL、AdamW、BF16。
5. 表格（Table 1–13）与图注（Figure 1–12）完整翻译，保留表格行列结构与数值。
6. 关键数字必须与原文逐一比对，不得改动：36 篇文档、1764 条复述、6,435/430 条探针、
   4,515/322 条 MCQ、200 条人工验证、N=100、1B/7B/13B/32B、batch 256/1024、
   Table 3/4/5/6/9/10/11/12/13 的数值、r 值与 p 值、超参数。
7. 文风：学术、准确、通顺；中文正文，保留必要英文术语首现括注；不添加原文没有的
   结论或评测。输出纯 Markdown，标题层级与原文一致。

## 输出
- 最终候选：candidates/20260912-080217/works-ready/Knowledge-Acquisition-During-Pre-trainin-translation.md
  （frontmatter 含 created/updated/title/sourceUrl/sourceAuthor/translatedAt/sources/tags）
```

## 执行说明

- 逐节翻译正文（摘要、1–9 节、致谢、局限）。
- 附录 A–E 完整翻译；附录 F/G 记为提示词清单，不搬运 base64 正文。
- 参考文献只保留正文引用，不逐条列出。
