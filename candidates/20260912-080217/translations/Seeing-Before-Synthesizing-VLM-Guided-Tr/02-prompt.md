---
created: 2026-09-12
updated: 2026-09-12
type: translation-prompt
status: 已执行
sources:
  - title: Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning
    url: http://arxiv.org/abs/2609.04183v1
    source: arxiv
    date: 2026-09-06
tags: [翻译提示词, 弱监督密集视频描述, 过渡事件, VLM, 论文翻译]
---

# 02 翻译提示词：Seeing Before Synthesizing

## 使用的输入

> 原文全文（v1）已抓取到
> `candidates/20260912-080217/sources/Seeing-Before-Synthesizing-VLM-Guided-Tr-full.md`
> （firecrawl 主内容抓取，含 Table 1–9、Table A.1、Figure 1–4 与附录图外链、公式 alt 文本；abs 页元数据经 curl 核对）。

## 提示词正文

```
你是一名资深技术译者（英→中），翻译汉阳大学论文
《Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for
Weakly-Supervised Dense Video Captioning》（arXiv:2609.04183v1，2026-09-03，
https://arxiv.org/abs/2609.04183）。作者 Ye-Chan Kim、Seunghee Choi、SeungJu Cha、
Si-Woo Kim、Hwiseon Kim、Hyungee Kim、Dong-Jin Kim（汉阳大学）。论文提出 SBS 框架，
用 VLM 生成帧级叙述并据此自适应地决定 WSDVC 中「是否」与「何处」注入过渡监督。

## 输入
- 原文：candidates/20260912-080217/sources/Seeing-Before-Synthesizing-VLM-Guided-Tr-full.md
  （正文从 "# Seeing Before Synthesizing..." 标题行开始，到 References 之前结束；
   参考文献不逐条翻译，只保留正文的作者-年份引用；附录 A–C 全译。）

## 输出要求
1. 完整逐译：摘要、第 1–5 节、Limitations、Acknowledgments；表格（Table 1–9、Table A.1）
   与图注（Figure 1–4、Figure A.1–A.2）完整保留。不压缩正文论述，不删节小节标题。
2. 保留全部图片外链与 DOI 页链接：
   teaser_0526_sh.png、main_fig.png、Interevent_qual_sh_0526_final.png、
   anet_suppl.png、yc2_suppl.png、text_peak_2.svg（Figure 4，SVG 折线图），
   https://arxiv.org/abs/2609.04183。正文引用保留作者-年份形式
   （如 Kim et al. (2026)），完整参考书目见 arXiv 页面。
3. 公式与符号：把 LaTeXML 双重渲染的数学还原为可读记法——
   c_n = Sig(FC_c(o_n))、w_n = Sig(FC_w(o_n))、
   M^{evt}_{n,i} = G(r_i; c_n, w_n) = exp(−(r_i−c_n)² / (2(w_n/τ_m)²))、
   r_i = (i−1)/(N_v−1)、
   d_i = 1 − (z_i · z_{i+1}) / (‖z_i‖‖z_{i+1}‖)、
   η^{adap}_n = μ(D_n) + β·σ(D_n)、g_n = Sig(max(D_n) − η^{adap}_n)、
   p_n = (i*_n − 1)/(N_v − 1)、i*_n = argmax_{i∈{b^s_n,…,b^e_n−1}} d_i、
   c^{inter*}_n = (1−α)·c^{inter}_n + α·p_n、
   w^{inter*}_n = argmax_{w^(k)∈Ω} cos(v̄′_n(w^(k)), z_{j_n})、
   s*_n = max_{w^(k)∈Ω} cos(v̄′_n(w^(k)), z_{j_n})、
   M^{inter*}_{n,i} = G(r_i; c^{inter*}_n, w^{inter*}_n)、
   L^attr_n = g_n·(1 − cos(v̄′*_n, z_{j_n}))、
   L^attr = (1/|A|)·Σ_{n∈A} L^attr_n、L = L^cap + L^con + λ^attr·L^attr、
   κ(x) = clip(⌊x(N_v−1)⌋+1, 1, N_v)。
   公式用行内 `$...$` 或代码块呈现，下标/上标用 Unicode 或 LaTeX 记法，全文统一。
4. 术语表（必须一致）：
   - Weakly-Supervised Dense Video Captioning (WSDVC) → 弱监督密集视频描述
   - Dense Video Captioning (DVC) → 密集视频描述
   - transition event / transitional event → 过渡事件
   - inter-event gap → 事件间间隙；inter-event → 事件间
   - frame-level narrative → 帧级叙述；narrative flow → 叙述流
   - Narrative-Aware Inter-Event Selection → 叙述感知的事件间选择
   - adaptive gate / gating → 自适应门控 / 门控
   - Adaptive Inter-Event Masks → 自适应事件间掩码
   - semantic change point → 语义变化点
   - Gaussian mask → 高斯掩码；soft Gaussian mask → 软高斯掩码
   - temporal center / width → 时间中心 / 宽度
   - Vision-Language Model (VLM) → 视觉语言模型
   - vision-language (VL) alignment → 视觉-语言对齐
   - visually grounded / grounded → 有视觉依据的 / 视觉接地（择一，全文统一为「有视觉依据」）
   - cosine dissimilarity → 余弦不相似度；cosine similarity → 余弦相似度
   - average-pooled representation → 平均池化表示
   - cross-modal alignment → 跨模态对齐
   - gated attraction loss → 门控吸引损失；attraction loss → 吸引损失
   - margin ranking loss → 边际排序损失
   - similarity filtering → 相似度过滤
   - ablation study → 消融实验
   - state-of-the-art → 当前最优（SOTA）
   - offline caption generation → 离线描述生成
   - hallucinate → 产生幻觉 / 臆造
   模型/数据集名保留原文：BLIP-2、InternVL3、Qwen2.5-VL、xGen-MM、SmolVLM2、
   CLIP ViT-L/14、Distilled-GPT2、ActivityNet Captions、YouCook2、SODA_c、METEOR、
   CIDEr、ROUGE-L、BLEU-N、IoU；首次出现补中文说明。
5. 数字与结论逐一比对原文，不得改动：
   20K 视频 / 平均 120 秒 / 约 3.7 个事件；约 2K 视频 / 平均 320 秒 / 平均 7.7 个事件；
   IoU {0.3, 0.5, 0.7, 0.9}；学习率 1e-4；10 / 10 epoch（ActivityNet）与 4 / 25 epoch（YouCook2）；
   α=0.5、β=2、θ=0.2、Ω={0.2, 0.4, 0.6}、λ_attr=0.4；事件查询 22 / 18；帧采样 32 / 100；
   Conv1D 核大小 5；间隙至少 4 帧；单张 NVIDIA A6000；
   Table 1：6.49 / 8.87 / 36.87 / 15.60 / 2.47 / 56.13 / 60.38 / 58.18，对照 SAIL 6.29 / 8.63 /
   35.38 / 15.29 / 2.30 / 54.39 / 59.87 / 57.00；
   Table 2：4.24 / 3.99 / 16.28 / 5.80 / 3.25 / 22.39 / 21.95 / 22.17，对照 SAIL 4.08 / 3.63 /
   14.61 / 5.42 / 2.94 / 20.76 / 21.13 / 20.94；
   消融 35.03/56.86 → 35.73/57.73 → 36.61/57.67 → 36.51/57.80 → 36.87/58.18；
   Table 6 余弦 0.1460 / 0.2624 / 0.2699；Table 7 参数 133M 对比 7B/5.9B；
   人工验证集 200 → 95（36 有 / 59 无），门控 74.99 / 64.29 / 69.23；
   开销 1H42M31S/7M16S/33.08GiB、1H49M50S/7M35S/33.11GiB、1H52M53S/7M51S/33.13GiB；
   离线生成 1H46M vs 1H38M。
6. 输出 Markdown，标题层级沿用原文（标题 + 摘要 + Related Work + Proposed Method 的
   3.1/3.2/3.3 + Experiments 的 4.1/4.2 + Conclusion + Limitations + Acknowledgments +
   Appendix A–C）。译文写入 translation.md。
```

## 执行记录

- 执行日期：2026-09-12
- 执行方式：单次完整翻译，写 `translations/Seeing-Before-Synthesizing-VLM-Guided-Tr/translation.md`，再复制到 `works-ready/Seeing-Before-Synthesizing-VLM-Guided-Tr-translation.md` 并补齐 frontmatter
- 偏离说明：Figure 4 为内嵌 SVG 折线图（`text_peak_2.svg`），译文保留外链并在正文补一句图意说明；参考文献仅保留文中作者-年份引用，未逐条翻译
