---
created: 2026-09-12
updated: 2026-09-12
type: analysis
status: 待评审
sources:
  - title: Knowledge Acquisition During Pre-training? Large Language Models Learn Better With Auxiliary Views
    url: http://arxiv.org/abs/2609.04180v1
    source: arxiv
    date: 2026-09-06
tags: [辅助视角, 预训练, 持续预训练, 知识获取, 复述, 层间偏置, 参数压缩, 数据多样性, 候选评审]
---

# 01 原文分析：Knowledge Acquisition During Pre-training?

## 原文信息

- **标题：** Knowledge Acquisition During Pre-training? Large Language Models Learn Better With Auxiliary Views
- **作者/机构：** Joseph Lee、Yidi Huang、Dokyoon Kim、Shu Yang、Li Shen（美国宾夕法尼亚大学；Li Shen 为通讯作者）
- **发布：** arXiv:2609.04180v1（cs.CL，交叉 cs.AI），2026-09-03
- **性质：** 学术论文（摘要 + 9 节正文 + 局限 + 致谢 + 参考文献 + 附录 A–G）
- **篇幅：** 约 14 万字节 Markdown；Figure 1–12、Table 1–13
- **代码/数据：** 数据集与代码均已开源（Hugging Face `jiosephlee/auxiliary-views-knowledge-acquisition`、GitHub `jiosephlee/auxiliary-views-knowledge-acquisition`）
- **抓取方式：** 2026-09-12 以 `curl` 抓 abs 页核对元数据；以 firecrawl `scrape -f markdown --only-main-content` 抓 v1 HTML 全文。完整全文见 `sources/Knowledge-Acquisition-During-Pre-trainin-full.md`

## 原文价值评估（高 / 中 / 低）

**高。** 这是一篇问题新颖、结论反直觉、且实验做得相当克制的预训练机制研究：它把「知识应当以何种形式表示」这一被语料级指标（去重/过滤/质量/多样性）长期掩盖的问题，收敛为一个可控制的变量——同一知识的「辅助视角」。文章得到若干与直觉相悖的结论（把 token 从原文重复挪给辅助视角，连逐字事实回忆都变好；辅助视角的效果不依赖教师模型强弱），并进一步给出参数层面的机制证据（层间偏置与压缩）。

- **优点：** 主结论在 4 个模型规模（1B/7B/13B/32B）、3 个领域（arXiv/法律/医学）、多指标（log-prob / target rank / MCQA）上一致；做了 token 匹配以排除 token 数混杂；用 upsampling 控制、预训练保真设置（batch 1024）、人类撰写视角、以及 Qwen-2.5-7B 交叉验证来加固结论；数据集与代码开源，可复现性高。
- **局限：** 规模止于 32B；仅 3 个领域，且上下文/前置知识的次级结论跨领域不一致；「预训练保真」仍是 100 步、从后期 checkpoint 续训而非从头预训练；医学领域缺失上下文知识对照；辅助视角依赖 LLM 生成，长尾专业知识下教师强度是否仍无关尚未回答。

## 关键概念与术语对照

- auxiliary view → 辅助视角
- reformulation (of knowledge) → （知识的）重新表述 / 改写
- view → 视角（本文中单数 view 指「一种知识呈现」）
- paraphrase → 复述
- continued pre-training (CPT) → 持续预训练
- pre-training-faithful setting → 预训练保真设置
- single-batch knowledge injection → 单批次知识注入
- token-matched / token budget → token 匹配 / token 预算
- upsampling → 上采样（重复采样）
- factual probe / inference probe → 事实探针 / 推理探针
- cloze statement → 完形填空式陈述
- multiple-choice question (MCQ) → 多项选择题
- log probability (log prob.) → 对数概率
- target rank → 目标词排名
- teacher model / generator → 教师模型 / 生成器
- contextual knowledge → 上下文知识
- prerequisite knowledge / foundational knowledge → 前置知识 / 基础知识
- prior-knowledge gap → 先验知识缺口
- layer-wise bias → 层间偏置
- feed-forward network (FFN) / MLP channel → 前馈网络 / MLP 通道
- gate / up / down projection → 门控 / 升维 / 降维投影
- relative delta norm → 相对增量范数
- cosine distance → 余弦距离
- Gini coefficient → 基尼系数
- compression → 压缩
- key–value memory → 键值记忆
- distillation → 蒸馏
- data augmentation → 数据增强
- lexical bias → 词汇偏置
- frequency / coverage → 频率 / 覆盖率
- LAMA-style probe → LAMA 风格探针
- Infini-gram → Infini-gram（专有名词，保留）

## 关键数字锚点（翻译时逐一比对）

- 36 篇文档 = 3 领域 × 12（arXiv 计算机科学论文 / 美国联邦上诉法院法律意见 / PubMed Central 医学病例报告）；均发表于 OLMo-2 语料截止日之后，并经 Infini-gram API 验证零命中。
- 每篇原文生成 49 条复述，共 1764 条复述；辅助视角覆盖 Blog、Stack Exchange Q&A、Textbook 三类。
- 探针规模：6,435 条事实探针 + 430 条推理探针；多选题变体 4,515 条事实 MCQ + 322 条推理 MCQ；每类人工验证 200 条。
- 主实验：N=100 次注入；Source / Para. M / Para. M + Aux. 三条件，token 匹配。
- 排序关系：Para. 9 + Aux. ≫ Para. 9 ≫ Source；Source 在前 ~20 步事实探针上学得更快。
- 模型：OLMo-2 base 1B / 7B / 13B / 32B；交叉验证 Qwen-2.5-7B。
- 复述饱和点：约 20 次曝光后 Source 饱和并急剧退化；Para. 9 可支撑到约 40 次曝光。批量 256 时 Source 与 Para. 9 基本持平。
- 保真设置（Table 5，OLMo-2 7B，batch 1024，从 step 925,000 续训）：Auxiliary views 事实 log prob −9.56 / 事实 MCQA 0.403 / 推理 log prob −10.82 / 推理 MCQA 0.492；Source 对应 −10.00 / 0.372 / −12.85 / 0.421；Para. 9 对应 −10.33 / 0.375 / −12.53 / 0.417。
- 教师强度（Table 13）：下游事实 MCQA 0.405–0.422，全部高于 Para. 9 基线 0.396；与生成器规模 r=−0.14（n=6），与生成器自身准确率 r=−0.24（n=10，p=0.50），与生成文本量 r=+0.62（p≈0.04）；gpt-oss-20B 领域知识最少却教得最好（0.422）。
- 机制：复述的参数变动幅度最大；辅助视角降低变动幅度，且在上中层（约 16–24 层）改动更少、在中层与末层改动更多；1B 模型上该层间结构几乎消失。
- 默认超参：峰值学习率 4e-5、上下文 4096、batch 256、weight decay 0.1、cosine 调度（warm-up 0.1、最小学习率比 0.1）、seed 42、max grad norm 1、AdamW（β1=0.9, β2=0.999, ε=1e-8）、BF16。
- 先验知识缺口（Table 6）：OLMo-2-0425-1B 从 0.4380 → 0.5454；OLMo-2-1124-7B 从 0.6859 → 0.7272。

## 观点建议（供 expand / thinking 参考，本阶段不写正文）

1. **「多样性」的可操作化。** 本文最有价值的迁移点，是把语料级的「多样性」下降到「围绕单条知识构造互补视角」这一可执行单元。对个人知识库/领域适配，这意味着：与其泛泛追求语料来源多，不如对每个核心知识点主动补齐教科书式、问答式、博客式三种改写。
2. **反直觉结论值得单独成篇。** 「把 token 从原文重复挪给辅助视角，逐字事实回忆反而更好」直接挑战「记忆靠重复」的朴素直觉，可结合本文的压缩/层间偏置证据，讨论「泛化表示反而更利于记忆」这一机制。
3. **与「数据质量 vs 数据配方」的对话。** 本文可被读作对 scaling law 语料讨论的补充：决定预训练效果的，可能不只是 token 数或质量分，而是同一知识被表述的方式。
4. **可复现的小实验。** 该论文实验设计（token 匹配 + 探针 + 参数增量分析）成本可控，适合作为「小规模可验证预训练结论」的模板；若要写 thinking，可提炼这套「去除混杂因子」的实验范式。
5. **落到日常实践。** 对持续预训练/领域适配，作者给出三条建议（补前置知识、数据稀缺时用复述、用辅助视角做合成增强）；其中「数据量少时复述有效、批量变大后收益递减」对资源有限者尤其有指导意义。
