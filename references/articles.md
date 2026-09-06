# 文章索引

> **本文件是文章索引与计数的最佳事实来源（single source of truth）。**
>
> **计数规则（machine-checkable）：**
> 一篇文章 = 一个 `### N. {标题}` 形式的编号小节，且不属于本文末尾的「已淘汰 / 待补充」段落。
> 占位条目（"待处理 / 待补充"）**不写在编号正文里**，而是统一进本文末尾的「待处理队列」，避免污染计数。
> 全局连续编号（不按来源重置），最大编号 = 文章总数。
>
> **状态字段（流程机器码）：** `待处理`（research 判定值得翻译，入队） / `已收录`（索引收录或译文已落 working） / `已淘汰`（判定不值，保留 URL 防重复采集）。
> **归属字段：** `working/…` 作品路径，或仅索引时的 `脉络:<lineage>`，或 `prompts/…` / `expand/…`。
> **观察项：** 见文末「观察项」表（不进编号正文、不计入主计数）；research 分流 `observe` 写入。
>
> **流水线（2026-08-10）：** research 写入 `pipeline/queue`（不开 PR）→ curate 落位并开**唯一终审 PR** → 人工合并 main。
>
> **下游引用都是本文的冗余缓存：** 根 `AGENTS.md`、`expand/index.md`、`references/AGENTS.md` 的概览表。
> 新增/更新文章时，必须**同一次提交**更新本文 + 相关下游缓存。

## 待处理（采集队列，计入编号正文前的暂存区）

> 由 `research.py`（verdict=`translate`）写入。curate 加工落位后移入编号正文。

<!-- pending:start -->
<!-- 采集自动化维护，按 `| 标题 | 链接 | 来源 | 日期 |` 追加一行；处理完移入编号正文 -->
<!-- 当前：1 条待处理 -->
| The new rules of context engineering for Claude 5 generation models | https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models | research | 2026-08-09 | 🔄评审中 candidates/20260809-180901/
| One-shotting a Raccoon Heist game using Claude Fable 5 | https://simonwillison.net/2026/Aug/5/raccoon-heist/ | research | 2026-08-09 | 🔄评审中 candidates/20260809-180901/
| Six Agent Orchestration Patterns | https://vercel.com/i/agent-orchestration-patterns | research | 2026-08-09 | 🔄评审中 candidates/20260809-180901/
| Making production-ready agents the default: building Duolingo's agent platform | https://blog.duolingo.com/production-ready-ai-agent-platform/ | research | 2026-08-09 | 🔄评审中 candidates/20260809-180901/
<!-- pending:end -->

## 已收录（编号正文）

### 01. arxiv — When Does On-Policy Interaction Help?

- **标题：** When Does On-Policy Interaction Help? Representational Tradeoffs in Value-Based Imitation Learning
- **链接：** [arxiv.org/abs/2607.29617v1](http://arxiv.org/abs/2607.29617v1)
- **作者：** arxiv 论文 | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/06-AI与LLM/Agent研究与评测/在线策略交互与模仿学习.md`
- **核心：** 专家交互放宽模仿学习表征需求，提出 OVI 算法。
- **关联：** Agent 模仿学习；`references/raw/` 已删除，素材散点见 expand 条目 sources 字段

### 02. AgentHPOBench — LLM Agents as Sequential Hyperparameter Optimizers

- **标题：** AgentHPOBench: A Benchmark For Evaluating LLM Agents as Sequential Hyperparameter Optimizers
- **链接：** [arxiv.org/abs/2607.29626v1](http://arxiv.org/abs/2607.29626v1)
- **作者：** arxiv 论文 | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/06-AI与LLM/Agent研究与评测/AgentHPOBench.md`
- **核心：** 7 类 30 任务，评估 LLM Agent 作为顺序超参数优化器。
- **关联：** Agent 评测基准

### 03. ExtractBench — Schema-Guided Enterprise Document Extraction

- **标题：** ExtractBench: A Benchmark for Schema-Guided Enterprise Document Extraction
- **链接：** [arxiv.org/abs/2607.29677v1](http://arxiv.org/abs/2607.29677v1)
- **作者：** arxiv 论文 | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/06-AI与LLM/Agent研究与评测/ExtractBench.md`
- **核心：** 370 文档 / 4869 页，模式引导的企业文档提取基准。
- **关联：** RAG + 文档解析

### 04. DungeonBench — Rules-Rich Tactical Reasoning

- **标题：** DungeonBench: A Benchmark for Rules-Rich Tactical Reasoning in Dungeons & Dragons Combat
- **链接：** [arxiv.org/abs/2607.29577v1](http://arxiv.org/abs/2607.29577v1)
- **作者：** arxiv 论文 | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/06-AI与LLM/Agent研究与评测/DungeonBench.md`
- **核心：** D&D 规则密集型战术推理基准（遭遇战 + 一日冒险双轨道）。
- **关联：** Agent 推理评测

### 05. MOT-SR — Multi-Objective Scientific Equation Discovery

- **标题：** MOT-SR: Multi-Objective Tool-Augmented Scientific Equation Discovery with Large Language Models
- **链接：** [arxiv.org/abs/2607.29561v1](http://arxiv.org/abs/2607.29561v1)
- **作者：** arxiv 论文 | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/06-AI与LLM/Agent研究与评测/MOT-SR.md`
- **核心：** 多目标工具增强符号回归框架（双 LLM 模块 + 帕累托前沿）。
- **关联：** 科学发现 + 工具调用

### 06. ECC — agent harness 操作系统

- **标题：** affaan-m/ECC — The agent harness performance optimization system
- **链接：** [github.com/affaan-m/ECC](https://github.com/affaan-m/ECC)
- **作者：** github | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/06-AI与LLM/Agent工具与平台/ECC.md`
- **核心：** 面向编程代理的 harness 操作系统：技能 / 记忆 / 安全 / 跨 harness 编排。
- **关联：** Agent 工程化 / harness

### 07. n8n — AI 原生工作流自动化平台

- **标题：** n8n-io/n8n — Fair-code workflow automation platform with native AI capabilities
- **链接：** [github.com/n8n-io/n8n](https://github.com/n8n-io/n8n)
- **作者：** github | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/06-AI与LLM/Agent工具与平台/n8n.md`
- **核心：** 可视化画布 + 1500+ 集成，自托管或云上 AI 原生工作流。
- **关联：** Workflow / Agent 调度

### 08. MarkItDown — 文件/文档转 Markdown

- **标题：** microsoft/markitdown — Python tool for converting files to Markdown
- **链接：** [github.com/microsoft/markitdown](https://github.com/microsoft/markitdown)
- **作者：** github | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/06-AI与LLM/Agent工具与平台/MarkItDown.md`
- **核心：** 任意文件转 LLM 友好 Markdown（架构 / 插件 / Azure 集成 / 安全实践）。
- **关联：** 数据管线 / 文档解析

### 09. Hermes-Agent — the agent that grows with you

- **标题：** NousResearch/hermes-agent — The agent that grows with you
- **链接：** [github.com/NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)
- **作者：** github | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/06-AI与LLM/Agent工具与平台/Hermes-Agent.md`
- **核心：** 自我改进 AI 代理——闭环学习与跨会话记忆。
- **关联：** Agent 自我改进

### 10. JavaGuide — Java 面试 & 后端面试指南

- **标题：** Snailclimb/JavaGuide — Java 面试 & 后端通用面试指南
- **链接：** [github.com/Snailclimb/JavaGuide](https://github.com/Snailclimb/JavaGuide)
- **作者：** github | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/03-后端/java/JavaGuide.md`
- **核心：** 计算机基础 / 数据库 / 分布式 / 高并发 / 系统设计 / AI 应用开发。
- **关联：** 后端 / 求职面试

### 11. Bonsai: Janestreet's UI Library

- **标题：** Bonsai: Janestreet's UI Library
- **链接：** [github.com/janestreet/bonsai](https://github.com/janestreet/bonsai)
- **作者：** HN | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** 淘汰
- **核心：** UI 库一个（排除原因：非本知识库范围，无 AI/后端关联，仅留 URL 防重复采集）
- **关联：** —

### 12. Prevent cognitive debt by manually retyping LLM-generated code

- **标题：** Prevent cognitive debt by manually retyping LLM-generated code
- **链接：** [ankursethi.com](https://ankursethi.com/blog/prevent-cognitive-debt-by-manually-retyping-llm-generated-code/)
- **作者：** HN | **日期：** 2026-08-03
- **状态：** 已淘汰 | **归属：** —
- **核心：** 独立已学，判定无深度加工价值
- **关联：** —

### 13. Qwen3.8-Max: A New Bar for Coding and Cowork

- **标题：** Qwen3.8-Max: A New Bar for Coding and Cowork
- **链接：** [qwen.ai](https://qwen.ai/blog?id=qwen3.8)
- **作者：** HN | **日期：** 2026-08-03
- **状态：** 已淘汰 | **归属：** —
- **核心：** 官方营销博文，技术增量有限
- **关联：** —

### 14. MCP 官方文档：Model Context Protocol 介绍

- **标题：** MCP 官方文档：Model Context Protocol 介绍
- **链接：** [modelcontextprotocol.io/introduction](https://modelcontextprotocol.io/introduction)
- **作者：** MCP 官方文档（modelcontextprotocol.io） | **日期：** 2026-08-09
- **状态：** 已收录 | **归属：** `expand/thinking/MCP协议标准化的增量与边界.md`
- **核心：** 官方入门与架构——「AI 应用的 USB-C」定位、数据层/传输层双层、2026-07-28 版增量（MCP Apps / Agent Skills / Registry / server/discover）。思考：协议只标准化「连接信封」，工具语义仍靠 server 自治，M×N 适配成本转移而非消失。
- **关联：** MCP / Agent 工具生态；既有笔记 [[MCP协议与工具调用]]、Claude Code [[12-mcp-xie-yi-ji-cheng]]

### 15. Rust 2025 官方博客：Rust 1.85 版本说明（Move 语义 / Borrow Checker 演进）

- **标题：** Rust 2025 官方博客：Rust 1.85 版本说明（Move 语义 / Borrow Checker 演进）
- **链接：** [blog.rust-lang.org/2025/02/20/Rust-1.85.0.html](https://blog.rust-lang.org/2025/02/20/Rust-1.85.0.html)
- **作者：** The Rust Release Team（blog.rust-lang.org） | **日期：** 2025-02-20（采集 2026-08-09）
- **状态：** 已收录 | **归属：** `expand/thinking/Rust2024版次的语义收紧与异步闭合.md`
- **核心：** Rust 1.85.0 同步稳定 2024 Edition（官方口径「史上最大版次」）：RPIT 生命周期捕获规则、临时作用域/drop 顺序、match 擦除保留、unsafe extern/属性/static mut 收缩、set_var 转 unsafe、async closures（AsyncFn）稳定、元组 collect 扩展至 12 元。思考：采集器「Move 语义」标签失焦——真正主线是「版次语义收紧 + unsafe 显式化 + 异步借用补课」，edition 约三年一拍是 Rust 的语义债务清偿机制。
- **关联：** Rust / 版次 / 借用检查；对照 [[c++核心编程]]、思考层 [[MCP协议标准化的增量与边界]]

### 16. Meta launches Muse Code for complex software work with persistent AI agents

- **标题：** Meta launches Muse Code for complex software work with persistent AI agents
- **链接：** [www.infoworld.com/article/4206084/meta-launches-muse-code-for-complex-software-work-with-persistent-ai-agents.html](https://www.infoworld.com/article/4206084/meta-launches-muse-code-for-complex-software-work-with-persistent-ai-agents.html)
- **作者：** research | **日期：** 2026-08-09
- **状态：** 已收录 | **归属：** `working/Meta-launches-Muse-Code-for-complex-soft-translation.md`
- **核心：** Meta launches Muse Code for complex software work with persistent AI agents

### 17. Claude Code v2.1.224 — self-hosted environments

- **标题：** Claude Code v2.1.224 — self-hosted environments
- **链接：** [github.com/anthropics/claude-code/releases/tag/v2.1.224](https://github.com/anthropics/claude-code/releases/tag/v2.1.224)
- **作者：** research | **日期：** 2026-08-09
- **状态：** 已收录 | **归属：** `working/Claude-Code-v2-1-224-self-hosted-environ-translation.md`
- **核心：** Claude Code v2.1.224 — self-hosted environments

### 18. EvolveNet: Collaborative Harness Evolution for Agent Self-Improvement

- **标题：** EvolveNet: Collaborative Harness Evolution for Agent Self-Improvement
- **链接：** [arxiv.org/abs/2608.04968](https://arxiv.org/abs/2608.04968)
- **作者：** research | **日期：** 2026-08-09
- **状态：** 已收录 | **归属：** `working/EvolveNet-Collaborative-Harness-Evolutio-translation.md`
- **核心：** EvolveNet: Collaborative Harness Evolution for Agent Self-Improvement

### 19. Harness-R1: Learning to Edit Executable Runtime Harnesses from Agent Failure Trajectories

- **标题：** Harness-R1: Learning to Edit Executable Runtime Harnesses from Agent Failure Trajectories
- **链接：** [arxiv.org/abs/2608.02276](https://arxiv.org/abs/2608.02276)
- **作者：** research | **日期：** 2026-08-09
- **状态：** 已收录 | **归属：** `working/Harness-R1-Learning-to-Edit-Executable-R-translation.md`
- **核心：** Harness-R1: Learning to Edit Executable Runtime Harnesses from Agent Failure Tra…

### 20. I Gave Claude Code an AGENTS.md Contract and Stopped Babysitting It

- **标题：** I Gave Claude Code an AGENTS.md Contract and Stopped Babysitting It
- **链接：** [dev.to/daymondhyper/i-gave-claude-code-an-agentsmd-contract-and-stopped-babysitting-it-53m](https://dev.to/daymondhyper/i-gave-claude-code-an-agentsmd-contract-and-stopped-babysitting-it-53m)
- **作者：** research | **日期：** 2026-08-09
- **状态：** 已收录 | **归属：** `working/I-Gave-Claude-Code-an-AGENTS-md-Contract-translation.md`
- **核心：** I Gave Claude Code an AGENTS.md Contract and Stopped Babysitting It

### 21. The Shape of Things to Come, Part 1: The Continuous Thunderdome

- **标题：** The Shape of Things to Come, Part 1: The Continuous Thunderdome
- **链接：** [yegge.ai/essays/the-shape-of-things-to-come/](https://yegge.ai/essays/the-shape-of-things-to-come/)
- **作者：** research | **日期：** 2026-08-09
- **状态：** 已收录 | **归属：** `working/The-Shape-of-Things-to-Come-Part-1-The-C-translation.md`
- **核心：** The Shape of Things to Come, Part 1: The Continuous Thunderdome

## 观察项

> 暂不收录、持续观察的 URL（防重复采集，不计入编号正文主计数）。由 research Prompt B（`observe`）写入。

| 标题 | 链接 | 来源 | 日期 | 备注 |
| --- | --- | --- | --- | --- |
| 憋了 7 周没动静，OpenClaw 2.0 带着 16000 个 PR 杀回来了 | https://juejin.cn/post/7680352383386107940 | 一点一木, 稀土掘金 | 2026-09-01 | 窗口内中文社区原创深度分析，覆盖会话管理/沙箱/多 agent 编排并含一手数据，非英文转述 |
| AgentRoom: Concurrent Multi-Agent Coding in a CRDT-Backed Shared Workspace | http://arxiv.org/abs/2608.23740 | arXiv (Seonglae Cho, Donghyun Lee) | 2026-08-24 | 多 agent 协作方向少见的机制级开放实验，与 SWE-Touch 构成 agent-agent vs 人机触碰互补 |
| Making Your Data Ready for Agentic AI | https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html | Pramod Sadalage & Prem Chandrasekaran, martinfowler.com (Thoughtworks) | 2026-08-27 | Tier 1 双作者长文，把 agent 数据准备上升为第一方框架，扩展已知数据×agent 方向 |
| Context Engineering for Coding Agents (Building a Coding Agent From Scratch, Lesson 4) | https://www.decodingai.com/p/context-engineering-for-coding-agents | Paul Iusztin, Decoding AI Magazine | 2026-08-25 | 一线实践+可复现代码直击 context engineering 主题，与 FrontierHarness 量化结论互相印证 |
| Maybe We Shouldn't Be Reviewing All This Code | https://martinfowler.com/rachels-ramblings/code-review.html | Rachel Laycock, martinfowler.com | 2026-09-02 | Tier 1 作者对主流流程的原创反驳，有明确辩论对象与数据，直接服务 AI 代码评审主题 |
| Headlong: a microharness for persistent agents (Laude/MIT) | https://www.laude.org/updates/headlong-a-microharness-for-persistent-agents | Laude Institute；github.com/laude-institute/headlong（1.1k stars） | 2026-08-24 | 可运行参考实现 + 透明失败教训，同时命中 harness/context/infra/评测四主题且与已知内容无重复 |
| Introducing FrontierHarness Eval: 9 harnesses, same model, cost per pass varies 17x | https://runta.com/blog/introducing-frontierharness-eval | Runta (Shilin Zhu, Shiqi Mei)；HN 81 分 | 2026-09-01 | 首个开源可复现的跨 harness 成本×通过率评测（含数据与任务），直接支撑 harness 选型与工程论点 |
| What's in Your Agent's Context? Context Privilege Escalation Attacks against AI Agent Harness | http://arxiv.org/abs/2609.01222 | arXiv (Zichuan Li, Luyi Xing 等) | 2026-09-01 | 为 context engineering 引入此前缺失的安全攻击面视角，含 12 系统实测，原创性强 |
| SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents | http://arxiv.org/abs/2609.04167 | arXiv cs.SE (Xin He, Yanlin Wang 等) | 2026-09-03 | 与 SWE-Touch、Data-eng-bench 互补的新评测维度，且与 code review 辩论直接互证 |
| A Few Pages of Markdown: Committed AI Configuration and Lower Quality Cost after Coding-Agent Adoption | http://arxiv.org/abs/2608.25241 | arXiv cs.SE (Yegor Denisov-Blanch 等) | 2026-08-26 | 把 AGENTS.md 实践从个案升级为 441 仓库量化研究，直接填补 AI 配置与代码质量关系的实证缺口 |
| Klibs.io Grows to 4200+ KMP Projects With Smarter Discovery and New AI Integrations | https://blog.jetbrains.com/kotlin/2026/08/klibsio-grows-to-4200-kmp-projects-with-smarter-discovery-and-new-ai-integrations/ | JetBrains Kotlin 博客 | 2026-08-17 | JetBrains 官方把 KMP 生态目录做成 agent 可调用工具，含评测数据与 AGENTS.md 实践，双领域交集标杆。 |
| What's new in Kotlin 2.4.20-RC | https://kotlinlang.org/docs/whatsnew-eap.html | Kotlin 官方文档 | 2026-08-12 | 官方 EAP 公告，覆盖标准库、K/N、K/Wasm、K/JS 多层实质变更，KMP 工具链风向标。 |
| What's new in Flutter 3.47 | https://flutter.dev/blog/whats-new-in-flutter-3-47 | Flutter 官方博客 | 2026-08-12 | 官方发布说明中设计系统解耦是长期架构调整信号，影响依赖管理与跨端构建策略。 |
| Conceptual integrity and counting lines of code | https://simonwillison.net/2026/Aug/19/conceptual-integrity-and-counting-lines-of-code/ | Simon Willison 博客 | 2026-08-19 | Tier 1 作者原创观点，挑战主流 LOC 无意义论，对 agent 工程管理/评测有启发。 |
| Introducing LangSmith Tuned Evaluators, starting with Perceived Error | https://www.langchain.com/blog/introducing-langsmith-tuned-evaluators-starting-with-perceived-error | LangChain 官方博客 | 2026-08-18 | 官方评测产品但技术实质充分（后训练法官+82% 成本数据+接入流程），对 agent 评测域有参考价值。 |
| Agentic Transaction: Towards ACID-Compliant Agent Systems | https://arxiv.org/abs/2608.13900 | arXiv cs.DB/cs.AI | 2026-08-14 | 原创理论框架+可运行系统，是 agent 可靠执行方向少见的系统性工作。 |
| The Devil Is in the Interface: Evaluating How Tool Architecture Shapes Coding Agent Behavior | https://arxiv.org/abs/2608.11386 | arXiv cs.SE | 2026-08-11 | 大样本受控实验+量化结论，为 harness/工具平台设计提供可复现证据。 |
| DeepSeek Harness 开发者预览：一切皆插件 | https://news.ycombinator.com/item?id=49285244 | DeepSeek 官方（Hacker News） | 2026-08-13 | 开源 agent harness 标杆事件，插件化架构与可追踪事件流直接回应 harness/编排主题，官方一级内容。 |
| Exploring Compose HTML for Server-Side Rendering | https://blog.jetbrains.com/kotlin/2026/08/exploring-compose-html-for-server-side-rendering/ | JetBrains | 2026-08-14 | 官方博客对 CMP 服务端渲染方向的原创前瞻，含可复现代码 |
| LiveMem: Maintaining Memory State Continuity in Long-Running LLM Inference | https://arxiv.org/abs/2608.02515 | arXiv cs.CL | 2026-08-03 | 为 agent 长会话记忆与上下文管理提供新抽象视角 |
| Everything we launched during Agents Week | https://blog.cloudflare.com/agents-week-review-august-2026/ | Cloudflare | 2026-08-10 | 云厂商对 agent 运行时与生命周期的一次系统性落子，平台趋势观察 |
| Announcing Dart 3.13 | https://dart.dev/blog/announcing-dart-3-13 | Dart / Google | 2026-08-12 | 官方稳定版发布，语言/工具链/编译优化多维实质更新 |
| IntelliJ IDEA Goes LSP: Java and Kotlin Intelligence Comes to VS Code, Cursor, and Agentic Flows | https://blog.jetbrains.com/idea/2026/08/intellij-idea-goes-lsp/ | JetBrains | 2026-08-04 | Kotlin 工具链×agent 工作流交叉的一手官方进展 |
| Deep Agents vs LangChain vs LangGraph | https://www.langchain.com/blog/deep-agents-vs-langchain-vs-langgraph | LangChain | 2026-08-06 | 官方对 agent 栈分层与 harness 定义的权威界定，指导选型 |
| SHE: Trajectory-driven Safety Harness Evolution for LLM Agents | https://arxiv.org/abs/2608.09885 | arXiv cs.AI | 2026-08-10 | 首个可演化安全 harness 系统化框架，有数据与复现链接 |
| SWE-Touch: Benchmarking Coding Agents When Users Touch the Code | https://arxiv.org/abs/2608.02499 | arXiv cs.SE | 2026-08-03 | 填补人机协作共享工作区评测盲区，有数据与开源实现，挑战单干基准范式 |
| DeepSeek Harness developer preview: Everything is a plugin | https://deepseek.com/harness/en/ | DeepSeek | 2026-08-14 | 开源 harness 平台级发布，Claude Code 直接竞品，HN 732 分高热 |
| Auto mode is now the default in Claude Code for Pro, Max, and Team plans | https://claude.com/blog/auto-mode-default-in-claude-code | Anthropic | 2026-08-07 | Tier 1 官方一手安全数据，直接塑造 agent 权限与安全架构设计 |
| New release of LLM adds support for reasoning traces, OpenAI Responses, server-side tools, and smarter logging | https://simonwillison.net/2026/Aug/4/new-release-of-llm/ | Simon Willison (simonwillison.net) | 2026-08-04 | Tier1作者对LLM工具平台的深度工程复盘，含可复现代码，覆盖推理轨迹、服务端工具与日志架构。 |
| Introducing Data-eng-bench: Why You Need "Data-Native" Harnesses for Data Engineering | https://www.snowflake.com/en/blog/engineering/data-eng-bench-data-engineering-agent-benchmark/ | Snowflake AI Research (Snowflake Engineering Blog) | 2026-08-06 | 首个仓库级dbt agent评测（103任务）并开源，harness×模型双变量质量/成本数据直接服务agent评测与选型。 |

## 统计

- **正式收录：** 12 篇（编号 01-10、14、15）｜**已淘汰隔离：** 3 篇（编号 11-13，不计入收录数，仅防重复采集）

## 待补充

- [ ] 占位：外部新文章先查编号 01-15 确认未收，再由采集层写入「待处理」队列
