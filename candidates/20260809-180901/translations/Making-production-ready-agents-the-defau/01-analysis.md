---
created: 2026-08-09
updated: 2026-08-09
type: analysis
status: 待评审
sources:
  - title: Making production-ready agents the default: building Duolingo's agent platform
    url: https://blog.duolingo.com/production-ready-ai-agent-platform/
    source: research
    date: 2026-08-09
tags: [AI Agent, 智能体平台, 生产就绪, Temporal, MCP, 评测, 候选评审]
---

# 01 原文分析：Making production-ready agents the default

## 原文信息

- **标题：** Making production-ready agents the default: building Duolingo's agent platform
- **作者：** Guadalupe Aliseda-Canton（Duolingo 工程博客，官方署名）
- **发布：** 2026-08-04（blog.duolingo.com；采集自 references/articles.md 待处理队列，日期 2026-08-09）
- **篇幅：** 正文约 2,000 英文词，抓取 Markdown 约 17KB（含 3 段 Python/YAML 代码块）；HTML 全文 47KB 存 `-full.md` 备用

## 原文价值评估（高 / 中 / 低）

**中高。** 一方工程博客，讲 Duolingo 如何把「生产就绪」从每个团队反复重建的负担，变成平台默认能力：

- 核心主张：**「定义与执行解耦」**——开发者只描述智能体做什么（系统提示词）、用什么工具（启用哪些 MCP）、能访问什么（克隆哪些仓库），其余（执行、编排、可观测性、评测）由平台兜底；智能体定义进 registry，可跨 Slack / 内部站点 / CLI / Temporal 工作流等多入口复用。
- 平台架构实证：`AgentDefinition`（含 model="gpt-5.5"、mcp_servers=("github", "sentry")、output_type）→ 由 Temporal `AgentWorkflow` 包装执行（加载定义 → 准备环境 → 用 LLM 提供商 SDK 运行 → 返回输出）；运行时可插拔（Claude Agents SDK、Codex CLI、OpenAI Agents SDK 都是同一抽象背后的实现）。
- 两个值得记的工程点：① Temporal 插件把 MCP 工具调用变成 activity，工具失败复用与工作流一致的 retry/状态管理，且每次调用（含输入/输出/失败/重试）在 Temporal UI 可见；② 通过 OpenAI Agents SDK 的代理路由接入内部 LLM 网关，统一成本/用量追踪与提供商切换，避免逐个 SDK 集成。
- 评测基础设施：真实智能体跑真实场景，捕获输出 + 改动文件 + git diff 再评分；评分器分三层——`structured_output`（结构化字段）、`diff_assertions`（repo diff：要求/排除/限制改动文件数/限定路径）、`no_op_consistency`（报告结论与仓库状态一致性，双向校验）；diff 断言太脆弱时才用可选 LLM-as-judge，**确定性评分器是地基**；评测本身也跑成 Temporal 工作流（子工作流 + 并行重复 + 结果持久化）。
- 量化信号：创建生产就绪智能体从「数周」→「约 10 分钟」；现状用例——修 CI 失败、处理代码评审意见、发布经理 Slack 机器人（多专用智能体组合：调查崩溃 → 定位相关改动 → 汇总发现）。
- 路线图：从工程师反馈自动化创建评测用例（低投入持续改进闭环）；智能体以工作流运行 → 可作为工具暴露给其他智能体 → 智能体互触发的大规模自主系统（编排层）。

局限：数字偏少且为孤例（「数周 → 10 分钟」无样本量与方法学，未给出平台上的智能体数量/调用量/成本数据）；一方宣传性质明显（文末招人）；`gpt-5.5` 等具体选型会过时；无失败教训或踩坑细节。

## 翻译质量评估（本次初判）

- 计划**完整逐译**正文（含 TL;DR、全部小标题、两段 Python 调用示例与 YAML 评测用例），代码块原样保留不译；站点头部作者行、TAGS/SHARE/RELATED ARTICLES 等站点噪音不译。
- 术语表初定：production-ready=生产就绪；productionizing=生产化（首现注原文）；registry=注册表；durable workflow engine=持久化工作流引擎；durable state=持久化状态；activity=活动（Temporal 概念，首现注 Activity）；query=查询（Temporal Query）；side effect=副作用；decouple definition from execution=定义与执行解耦；runtime=运行时；LLM Gateway=LLM 网关；agent eval=智能体评测；authored scenario=编写好的场景；grader=评分器；structured_output=结构化输出（评分器名保留）；diff_assertions=差异断言（评分器名保留）；no_op_consistency=空操作一致性（评分器名保留）；LLM-as-judge=LLM 作为裁判；brittle=脆弱；suite workflow=套件工作流；child workflow=子工作流；multi-entry-point invocation=多入口调用；orchestration=编排；observability=可观测性；abstraction=抽象；MCP/Temporal/OpenAI Agents SDK/Claude Agents SDK/Codex CLI/Slack 等专名保留原文。
- 关键数字抽查锚点：2026-08-04 发布日期、10 分钟 vs 数周、gpt-5.5、mcp_servers=("github","sentry")、max_changed_files: 1、四步操作（加载定义/准备环境/运行/返回输出）、评分器三类 + 可选 LLM-as-judge。
- 预计质量为「良好级」：散文式工程叙事，无复杂表格；难点在 Temporal 术语（activity/query）与代码块边界的准确处理。

## 与知识库契合度

- 主题位于知识库核心区：AI Agent 基础设施 / 生产化实践。本文补的是知识库薄弱环节——**「智能体平台」的落地形态**（registry + 持久化工作流 + 评测 + 网关的统一抽象），区别于已有条目的工具/协议/评测基准视角。
- 与既有条目关系：`expand/thinking/MCP协议标准化的增量与边界.md`（本文给出 MCP 工具调用变 Temporal activity 的真实工程化收益，可互为印证）；同批 "Six Agent Orchestration Patterns"（Vercel）讲编排模式选型，本文讲编排/执行/评测的平台化承载，一个选型一个落地；"The new rules of context engineering"（Claude 官方）关注上下文，本文关注执行层抽象；`expand/06-AI与LLM/Agent研究与评测/`（DungeonBench 等）偏能力评测，本文的 agent eval 是**生产场景评测**（diff/no-op 断言），视角互补。
- 无重复风险：expand 层目前没有「智能体平台 / 生产化」条目。

## 收录建议

- **建议去向：working/ 正式收录**（译文作品，可独立理解，适合对外分享）。
- 理由：平台化生产智能体的完整参考架构（定义/执行解耦 + 持久化 + 评测 + 多入口），与知识库 Agent 主题强相关，代码示例可操作性强。
- 评审后可考虑：① 补一条 expand/thinking 观点条目（「生产就绪应该是默认能力而不是每个团队的自选项」：抽象层把基础设施问题集中解决一次，AI 生成代码越多，这类保证质量的抽象越值钱）；② 「评测必须是确定性的、检查产物而非文字」这条原则可沉淀进 prompts/ 评审提示词素材（待实测后）。

## 观点建议（供人类评审参考，不写 expand 正文）

1. 「定义与执行解耦」是本文最值得迁移的抽象：它把「运行时/模型/工具链/评测可以独立演进」变成平台能力。与 Vercel 六模式文互相印证——选型发生在基础设施之前，而本文说基础设施一旦平台化，选型成本趋近于零。
2. 评测三件套（结构化输出 / diff 断言 / no-op 一致性）本质是把「模型说了什么」与「系统实际变成什么样」对齐——这正是 harness engineering 里「程序化闸门」的评测侧镜像：先有确定性检查，LLM-as-judge 只补脆弱的边角。
3. 「把评测也跑成工作流」是个容易被低估的决策：评测与生产同构后，长用例、失败捕获、并行重复、结果持久化都免费获得，评测从本地脚本升级为平台资产。
4. 注意证据等级：这是一方宣传稿，「数周 → 10 分钟」缺样本与方法学；把它当「架构清单」读（平台应该有什么），别当「收益证明」引用。
5. 「智能体可以作为工具暴露给其他智能体」与本文路线图里的编排，和同批 Six-Agent 文的 orchestrator-worker 是同一件事的两端：定义层支持组合，执行层负责持久化。
