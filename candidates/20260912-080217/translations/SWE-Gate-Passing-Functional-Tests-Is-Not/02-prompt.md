---
created: 2026-09-12
updated: 2026-09-12
type: translation-prompt
status: 已执行
sources:
  - title: "SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents"
    url: http://arxiv.org/abs/2609.04167v1
    source: arxiv
    date: 2026-09-06
tags: [翻译提示词, 编码智能体, 仓库级修复, 代码评审, 评测基准, 论文翻译]
---

# 02 翻译提示词：SWE-Gate — 通过功能测试还不够

## 使用的输入

> 原文全文（v1）已抓取到
> `candidates/20260912-080217/sources/SWE-Gate-Passing-Functional-Tests-Is-Not-full.md`
> （firecrawl 主内容抓取，含 Figure 1/2 图注、Table 1–5、参考文献外链）。

## 提示词正文

```
你是一名资深技术译者（英→中），翻译论文
《SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering
Agents》（arXiv:2609.04167v1，2026-09-03，https://arxiv.org/abs/2609.04167）。
作者 Xin He、Yanlin Wang（通讯）、Mingwei Liu、Jiachi Chen、Hongyu Zhang、
Guanbin Li，单位包括中山大学、浙江大学、重庆大学。论文提出 SWE-Gate：首个
在仓库级编码智能体评测中，把"评审衍生的验收约束"（review constraints）作为
独立可执行维度、与功能正确性分离评估的基准；包含 303 个实例、75 个 Python 仓库。

## 输入
- 原文：candidates/20260912-080217/sources/SWE-Gate-Passing-Functional-Tests-Is-Not-full.md
  （正文从 "# SWE-Gate: Passing Functional Tests..." 标题行开始，到 "## Conclusion"
   之后结束；"## References" 一节不逐条翻译。）

## 输出要求
1. 完整逐译：摘要、第 1–5 节；不压缩正文论述，不删节小节标题。
2. 保留全部超链接：正文中的外链（Pydantic PR #12657、复现包 GitHub 仓库、
   图 1 图片地址）按 Markdown 原样保留；形如 #bib.bibNN 的参考文献锚点链接
   在译文中改为对应的数字引用 [N]，不逐条展开。
3. 保留全部表格（Table 1–5），表头与数据不得改动；表题、图注需翻译。
4. 关键数字必须与原文一致：303 实例、75 仓库、644 功能通过、221 隐藏失败、
   34.3% HFR、FSR/CFR/JSR 各模型数值、+C/−C 消融数值、各约束类别计数。
5. 中文正文，术语到位（采用 01-analysis.md 的术语对照表）：review constraints →
   评审约束；hidden failure → 隐藏失败；constraint seed → 约束种子；synthesis
   anchor → 合成锚点；non-compliant patch → 不合规补丁；gold patch → 金标准补丁；
   FSR/CFR/JSR → 功能成功率 / 约束遵循率 / 联合成功率。
6. 数学符号（N、N_F、N_{F∩C}、ΔM 等）用行内代码或普通文本呈现，保持可读。
7. 结尾加"关于参考文献"小节，说明完整英文参考文献对照原文 v1。

## 禁止
- 不得增删作者观点，不得加入译者评论（分析意见只放 01-analysis.md）。
- 不得改写表格数值以"看起来更整齐"。
- 不得省略任何一章或任何一条要点/子弹。

## 产物
- 过程稿：candidates/20260912-080217/translations/<slug>/translation.md
- 最终候选：candidates/20260912-080217/works-ready/<slug>-translation.md
```

## 执行记录

- **输入完整性：** 全文抓取成功，含 Figure 1/2 图注、Table 1–5 与参考文献；未见内容缺失（论文无附录，补充材料另附）。
- **数字抽查：** 翻译完成后与原文逐项比对关键数字与结论（303 / 75 / 644 / 221 / 34.3% / FSR·CFR·JSR / Δ 值 / 类别计数）。
- **术语一致性：** 全文统一使用"评审约束""隐藏失败""联合成功率"等译名，英文原词在首次出现处以括号标注。
- **链接保留：** Pydantic PR #12657、复现包仓库地址、Figure 1 图片外链均保留；`#bib.bibNN` 锚点转为数字引用。
