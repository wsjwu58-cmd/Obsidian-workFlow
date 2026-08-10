---
created: 2026-08-10
updated: 2026-08-10
title: Meta 发布 Muse Code：用持久化 AI 代理处理复杂软件工程
sourceUrl: https://www.infoworld.com/article/4206084/meta-launches-muse-code-for-complex-software-work-with-persistent-ai-agents.html
sourceAuthor: Prasanth Aby Thomas（InfoWorld）
translatedAt: 2026-08-10
sources: [references/articles.md 待处理队列]
tags: [Meta, Muse Code, AI Agent, 编码代理, Harness, type/翻译]
---

# Meta 发布 Muse Code：用持久化 AI 代理处理复杂软件工程

> Meta 将 Muse Spark 1.2 模型与其终端版 Muse Code 代理进行了联合训练，但分析师认为，
> 这一做法目前还不足以让它与竞争对手拉开差距。

Meta 发布了一款 beta 版编码代理，专为大型代码库中的复杂软件任务而设计。

Muse Code 支持 macOS 与 Linux，基于 Meta 新的 Muse Spark 1.2 模型。它内置多个专用后台代理，
这些代理在整个会话期间保持活跃，而不是为单个任务单独创建。

后台代理异步执行工作，并自行决定何时向主代理汇报结果。Meta 表示，让它们保持常驻可以减少
重复的信息收集，也减少在困难的多步任务中需要开发人员引导的次数。

「Muse Code 使用本地事件日志，每次模型调用、工具运行、审批和编辑都会被追加记录，」
Meta 在一篇帖子中表示，并补充说，该记录「让运行时可精确重放（replay-exact）且可安全重启
（restart-safe）」，使代理在崩溃后能精确地从上次中断的位置继续执行。

[Muse Spark 1.2](https://www.infoworld.com/article/4192724/metas-ai-chief-says-new-muse-spark-update-will-sharpen-coding-agentic-ai.html)
可通过 Muse Code 与 Meta Model API 使用，Meta 同时宣布扩大该 API 的全球访问范围。

## 训练与评测

Meta 表示，他们用 Muse Code 对 Muse Spark 1.2 进行了联合训练，以提升模型在配合该代理使用时的
性能与易用性。训练过程纳入了 Muse Code 的工具与代理工作流，同时 Meta 增加了用于编码的计算资源，
并扩大了开发环境的覆盖范围。

该模型还针对更长的任务进行了训练，包括整个代码库的生成以及大型端到端软件项目。

Omdia 首席分析师 [Lian Jye Su](https://omdia.tech.informa.com/authors/lian-jye-su) 表示，Meta 的联合训练方法不太可能带来明显优势，因为竞争对手也在
紧密协调地开发自己的编码模型与 [agent 执行框架](https://www.infoworld.com/article/4164601/harness-teams-of-coding-agents-with-squad.html)。

「OpenAI、Anthropic 等厂商早已把执行框架工程（harness engineering）视为训练过程的一部分，」Su 说。

Pareekh Consulting 首席执行官 [Pareekh Jain](https://pareekh.com/) 表示，联合优化模型与代理确实能
改善规划与上下文处理，但任何竞争优势都需要通过在真实企业项目上拿出更好的结果、同时减少人工干预来证明。

Meta 报告称，Muse Spark 1.2 在 Terminal-Bench 2.1 上取得了 82.9% 的 pass@1 分数，落后于
Claude Opus 5，但略高于 GPT-5.6 Terra。在 DeepSWE 1.1 上，该模型得分为 59.3%，落后于这两个对手。

对于 Terminal-Bench 2.1 与 DeepSWE 1.1，Meta 用各家模型各自选定的编码代理进行评测，而不是全程
使用同一个代理。Meta 也承认，如果为竞争对手的专有模型专门设计工具与提示词，它们的表现可能会有所不同。

Counterpoint Research 研究副总裁 [Neil Shah](https://counterpointresearch.com/en/opinion-leader/10) 表示，
如果用第三方工具或在同一个 agent 执行框架内评测模型，跨厂商的比较会更有意义。

「对 CIO 来说，关键指标是在企业自有流水线上的通过率，它将决定『模型+执行框架』组合的成败——
在这里就是 Meta 的 Muse Spark 1.2 与 Muse Code，」Shah 说。「这才是真正的[基准测试](https://www.infoworld.com/article/4033758/why-benchmarks-are-key-to-ai-progress.html)。」

## 企业采用的门槛

Su 表示，安全与治理要求可能会拖慢企业采用速度，尤其是在编码代理必须接入现有身份系统的场景。

「许多企业仍然不太愿意向 AI 工具集成开放自己的 CI/CD 环境，」Su 说。

Shah 表示，企业需要管控代理访问代码仓库的权限，并保留模型与代理工作流如何处理企业数据的记录。
他还提到，预测 token 消耗量及其对成本的影响十分困难。

Meta 的定价结构还带来一个数据治理上的选择：该公司表示，价格较低的 Contributor 档可能被用来改进
其产品，而标准档则不会用于这一目的。

Contributor 档的价格为每百万输入 token 0.10 美元、每百万输出 token 0.20 美元；标准档则分别为
1.25 美元与 4.25 美元。

「此外还存在对厂商锁定与依赖的担忧，因为它可能损害长期灵活性与系统互操作性，」Su 补充道。

Jain 表示，在企业允许持久化代理修改关键生产代码之前，采用很可能会先从范围明确、风险较低的
工作开始。
