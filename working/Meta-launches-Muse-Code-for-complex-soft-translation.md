---
created: 2026-08-10
updated: 2026-08-10
title: Meta 推出 Muse Code：以持久化 AI 智能体处理复杂软件工程
sourceUrl: https://www.infoworld.com/article/4206084/meta-launches-muse-code-for-complex-software-work-with-persistent-ai-agents.html
sourceAuthor: Prasanth Aby Thomas（InfoWorld）
translatedAt: 2026-08-10
sources: [references/articles.md 待处理队列]
tags: [AI Agent, 编程智能体, Meta, Muse Code, Muse Spark, type/翻译]
---

# Meta 推出 Muse Code：以持久化 AI 智能体处理复杂软件工程

新闻 | 2026 年 8 月 6 日 | 阅读约 4 分钟

Meta 发布了一款测试版编程智能体（coding agent），用于在大型代码库上处理复杂的软件任务。

Muse Code 支持 macOS 与 Linux，使用公司新的 Muse Spark 1.2 模型。它包含专门的**后台智能体（background agents）**，这些智能体在整个会话期间保持活跃，而不是为单个任务单独创建。

这些智能体以异步方式执行工作，并自行决定何时向主智能体汇报结果。Meta 表示，让它们保持活跃可以减少重复的信息收集，并降低在困难的多步骤任务中对开发者指令的需求。

「Muse Code 使用一个本地事件日志（local event log），每次模型调用、工具运行、审批和编辑都会追加写入其中，」Meta 在一篇帖子中表示，并补充说这份记录「让运行时能够精确重放（replay-exact）且重启安全（restart-safe）」，使智能体在崩溃后可以从停止的位置精确恢复。

[Muse Spark 1.2](https://www.infoworld.com/article/4192724/metas-ai-chief-says-new-muse-spark-update-will-sharpen-coding-agentic-ai.html) 可通过 Muse Code 与 Meta Model API 使用，Meta 宣布扩大了两者的全球访问范围。

## 训练与评估

Meta 表示，它与 Muse Code 联合训练（co-trained）了 Muse Spark 1.2，以提高模型在智能体中使用时的性能与易用性。训练过程纳入了 Muse Code 的工具和智能体工作流，同时 Meta 增加了用于编码的计算资源，并拓宽了开发环境的范围。

该模型还在更长的任务上进行了训练，包括整个代码库的生成和大型端到端软件项目。

[Omdia 首席分析师 Lian Jye Su](https://omdia.tech.informa.com/authors/lian-jye-su) 表示，Meta 的联合训练方法不太可能带来明显优势，因为竞争对手也在紧密协同地开发自己的编码模型和[智能体框架（agent harnesses）](https://www.infoworld.com/article/4164601/harness-teams-of-coding-agents-with-squad.html)。

「其他厂商，如 OpenAI 和 Anthropic，一直把框架工程（harness engineering）视为训练过程的一部分，」Su 说。

[Pareekh Consulting 首席执行官 Pareekh Jain](https://pareekh.com/) 表示，同时优化模型与智能体可以改进规划与上下文处理能力，但任何竞争优势都需要通过在企业的项目上取得更好的结果、同时减少对人工干预的需求来证明。

Meta 报告称，Muse Spark 1.2 在 Terminal-Bench 2.1 上取得了 82.9% 的 pass@1 成绩，落后于 Claude Opus 5，但略高于 GPT-5.6 Terra。在 DeepSWE 1.1 上，该模型的得分为 59.3%，落后于上述两家竞争对手。

对于 Terminal-Bench 2.1 与 DeepSWE 1.1，Meta 是让每个模型使用其各自选定的编码智能体进行评估，而不是全程使用同一个智能体。它还承认，竞争对手的专有模型在专门为其设计的工具和提示词下，表现可能有所不同。

[Counterpoint Research 研究副总裁 Neil Shah](https://counterpointresearch.com/en/opinion-leader/10) 表示，如果使用第三方工具或在同一个智能体框架内评估模型，跨厂商的比较会更有意义。

「对 CIO 来说，关键指标是模型在企业自身流水线上的通过率，它将决定『模型 + 框架』组合的成败——也就是这里的 Meta Muse Spark 1.2 与 Muse Code，」Shah 说。「这才是真正的[基准](https://www.infoworld.com/article/4033758/why-benchmarks-are-key-to-ai-progress.html)。」

## 企业采用的障碍

Su 表示，安全与治理要求可能会拖慢企业的采用速度，尤其是在编程智能体必须接入现有身份系统的情况下。

「许多企业仍然不太愿意为 AI 工具集成开放自己的 CI/CD 环境，」Su 说。

Shah 表示，企业需要管控智能体如何访问代码仓库的控制机制，以及模型和智能体工作流如何处理企业数据的记录。他还提到，预测 token 消耗及其对成本的影响存在困难。

Meta 的定价结构也带来一个数据治理上的选择。该公司表示，价格较低的 Contributor 档（Contributor tier）可用于改进其产品，而标准档（standard tier）不用于这一目的。

Contributor 档的价格为每百万输入 token 0.10 美元、每百万输出 token 0.20 美元；标准档则分别为 1.25 美元与 4.25 美元。

「此外还存在对供应商锁定（vendor lock-in）与依赖的担忧，因为它可能损害长期的灵活性与系统互操作性，」Su 补充道。

Jain 表示，企业的采用很可能会从界定明确、风险较低的工作开始，之后才会允许持久化智能体修改关键的生产代码。
