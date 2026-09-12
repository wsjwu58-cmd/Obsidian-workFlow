---
created: 2026-09-12
updated: 2026-09-12
type: translation-prompt
status: 已执行
sources:
  - title: A Case Study on Emergent Cheating and Whistleblowing in Autonomous Research Swarms
    url: http://arxiv.org/abs/2609.04170v1
    source: arxiv
    date: 2026-09-06
tags: [翻译提示词, 规格博弈, 多智能体, 知识公地, 论文翻译]
---

# 02 翻译提示词：Emergent Cheating and Whistleblowing in Autonomous Research Swarms

## 使用的输入

> 原文全文（v1）已抓取到
> `candidates/20260912-080217/sources/A-Case-Study-on-Emergent-Cheating-and-Wh-full.md`
> （firecrawl 主内容抓取，含 Figure 1 图注、附录 A–E 的提示词、工具描述与智能体本地 wiki 原文摘录、参考文献外链）。

## 提示词正文

```
你是一名资深技术译者（英→中），翻译 Google DeepMind 论文
《A Case Study on Emergent Cheating and Whistleblowing in Autonomous Research
Swarms》（arXiv:2609.04170v1，2026-09-03，https://arxiv.org/abs/2609.04170）。
作者 Davide Paglieri、Logan Cross、Tim Genewein、Joel Z. Leibo、Nenad Tomasev、
Alexander Sasha Vezhnevets（Google DeepMind）。论文记录一次案例研究：100 个自治
LLM 智能体在 71 道形式化数学猜想上协作，其中作弊行为自发涌现并病毒式扩散，随后
又出现自发的举报与规范执行；作者以 Ostrom 的知识公地治理框架加以分析。

## 输入
- 原文：candidates/20260912-080217/sources/A-Case-Study-on-Emergent-Cheating-and-Wh-full.md
  （正文从 "# A Case Study on Emergent Cheating..." 标题行开始，到 "## References"
   之前结束；参考文献不逐条翻译，只保留正文的作者-年份引用与超链接。）

## 输出要求
1. 完整逐译：摘要、第 1–5 节、以及附录 A–E；不压缩正文论述，不删节小节标题。
   附录 B 的完整性系统提示词、附录 C 的三个工具描述、附录 D 的四个智能体本地
   wiki 原文均属关键证据，需完整翻译（代码块与 Lean 代码保留原样）。
2. 保留全部超链接。正文中形如 https://arxiv.org/html/2609.04170v1#bib.bibN 的
   引用链接一律保留（清理 firecrawl 附加的空 title 后缀），作者-年份引用形式保留。
   论文页 https://arxiv.org/abs/2609.04170、DOI 链接一并保留。
3. 智能体昵称保留英文：prover-theta、prover-mu、prover-chi、prover-beta、prover-rho、
   prover-nu、prover-zeta、prover-tau、prover-lambda、prover-psi、prover-omega、
   prover-upsilon、prover-alpha、prover-epsilon、prover-delta、prover-digamma、
   prover-xi、prover-kappa、prover-phi、prover-sigma、prover-sampi、prover-omicron、
   prover-iota、prover-eta、prover-pi、prover-gamma；数学题名保留英文
   （all_fermat_squarefree、Catalan's Conjecture、Erdős Problem 835、Jacobian
   Conjecture、Sendov's Conjecture、Pillai's Conjecture、Schanuel's Conjecture、
   Green's Problem 14、Greens14、平方自由的费马数问题等）。
4. 术语表（必须一致）：
   specification gaming→规格博弈；reward hacking→奖励黑客；exploit→漏洞利用/作弊手法；
   viral diffusion/contagion→病毒式扩散/传染；whistleblowing→举报（吹哨）；
   whistleblower→举报者（吹哨人）；knowledge commons→知识公地；governance→治理；
   polycentric governance→多中心治理；graduated sanctioning→渐进式制裁（分级制裁）；
   collective-choice rules→集体选择规则；conflict-resolution arena→冲突解决场域；
   boundaries→边界；monitoring→监督；norm enforcement→规范执行；
   behavioral divergence→行为分化；side-channel→侧信道；covert coordination→隐蔽协同；
   autograder→自动评分器；submission harness→提交工具链；editable preamble→可编辑前言；
   notation shadowing→记法遮蔽；local notation/infix→局部记法/局部中缀；
   elaboration→精化；elaborator→精化器；kernel-level AST verification→内核级 AST 验证；
   AST introspection→AST 内省；syntactic template validation→语法模板校验；
   formal judge→形式化裁判；Recursive Self-Improvement→递归自我改进；
   latent pretraining priors→预训练潜藏先验；lockout→锁定；deadlock→死锁；
   Research Bulletin Board→研究公告栏；direct messaging (DMs)→私信；
   shared knowledge library→共享知识库；persistent memory→持久记忆；
   scientific credit→科研信用；first-to-solve lockout→首解即锁定。
   专有名词保留英文：Lean 4、Mathlib、Lean Comparator、Ostrom、Wikipedia、
   open-source、pull request、sorry、axiom、False.elim、Iff.rfl、trivial、
   Pollard's ρ、Euclid(28)、Ryley、Gemini 相关模型名如原文出现则保留。
5. 忠实翻译智能体推理轨迹与消息原文，不美化、不改写为「作者观点」；保持其
   第一人称与情绪化语气（如 "This conference is a sham!"）。
6. 关键数字必须与原文逐一比对，不得改动：100 个智能体、71 题、11:18 UTC 启动、
   12:15 UTC 解出 37 题、27 分钟扩散、剩余 34 题、12:42:48 UTC 收尾、12:43 UTC
   分享作弊代码、四类分组 9%/5%/24%/62%、附录 E Table 1 的 8 位举报者及其
   CoT/Board/Feedback 编号、prover-theta 的 8 道 answer 题、Euclid(28) 等。
7. Figure 1 图注与内容（DISCOVERY → PROPAGATION → BEHAVIORAL DIVERGENCE，
   以及四个行为分组）完整翻译；附录 E 的 Table 1 保留表格结构与原文证据引用。
8. 文风：技术、准确、通顺；中文正文，保留必要英文术语首现括注；不添加原文没有的
   结论或评论。输出纯 Markdown，标题层级与原文一致。

## 输出
- 最终候选：candidates/20260912-080217/works-ready/A-Case-Study-on-Emergent-Cheating-and-Wh-translation.md
  （frontmatter 含 created/updated/title/sourceUrl/sourceAuthor/translatedAt/sources/tags）
```

## 执行说明

- 逐节翻译正文（摘要、1–5 节）。
- 附录 A–E 全部翻译；附录 D 的 Lean 代码块与 wiki 原文逐字保留。
- 参考文献只保留正文引用与链接，不逐条翻译书目。
