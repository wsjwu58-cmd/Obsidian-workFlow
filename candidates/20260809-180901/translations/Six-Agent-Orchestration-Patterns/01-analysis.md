---
created: 2026-08-09
updated: 2026-08-09
type: analysis
status: 待评审
sources:
  - title: Six Agent Orchestration Patterns
    url: https://vercel.com/i/agent-orchestration-patterns
    source: research
    date: 2026-08-09
tags: [AI Agent, 编排, Agent 架构, Vercel, AI SDK, 候选评审]
---

# 01 原文分析：Six Agent Orchestration Patterns

## 原文信息

- **标题：** Six Agent Orchestration Patterns
- **作者：** Vercel（官方平台指南，vercel.com/i/ 系列「Build with AI」；无个人署名，无显式发布日期）
- **发布：** 采集自 references/articles.md 待处理队列，日期 2026-08-09；正文含「July 2026 AI Gateway Production Index」引用，推断发布于 2026-07/08
- **篇幅：** 正文约 2,400 英文词，抓取 Markdown 约 20KB（含 6 行模式对照表）；HTML 全文 114KB 存 `-full.md` 备用

## 原文价值评估（高 / 中 / 低）

**中高。** 不是发布稿，而是 Vercel 把自家多智能体生产经验（AI SDK 7 + Workflows + AI Gateway + Sandbox）
整理成的**可执行模式选型指南**，六种模式各给出「适用 / token 成本 / 何时避免」：

- 核心主张：**从最低复杂度模式起步，按能力缺口升级**；「过早扇出」（premature fan-out）反模式——
  工作量没有独立子任务就加 agent，会同时放大成本与故障面。
- 实证数字密集：多智能体 token 用量最高为普通聊天的 **15×**（引 Anthropic 多智能体研究）；
  95%/步 × 10 步链式精度 → 端到端约 **60%**（90% → 约 35%）；AI SDK 7 `ToolLoopAgent` 默认 20 步上限；
  Okara 在 AI Gateway 层跑 CMO agent，服务 **12 万+ 企业、日处理 40 亿 token**；
  General Intelligence「Cofounder」：每位工程师每天 **10 个 PR / 70+ commits**，横跨 **4,000+ 预览分支**，
  **90% SRE 工作自动化**；Turborepo 性能改造 8 天、最高 **96% 提速**。
- 平台四件套与模式一一对应：Fluid compute（活动 CPU 计费，$0.128/小时基础费率，解决扇出 I/O 等待计费）、
  Workflows（`use workflow` 指令 + 检查点 + 暂停/恢复，步骤最长 1,800 秒）、AI Gateway（统一模型路由、零加价）、
  Sandbox（Firecracker 微虚拟机，Hobby 45 分钟 / Pro & Enterprise 24 小时执行上限）。
- 独立信号：**等计算预算下，单智能体循环在多跳推理上不输甚至超过多智能体**（Qwen3 / DeepSeek-R1 / Gemini 2.5），
  与 Anthropic「15× token」数据点互为张力，可作为选型判断的锚。

局限：本质是 Vercel 平台推广（四件套都是自家产品），对照表是相对估计值、无方法学细节；
「单智能体≥多智能体」引用的 arXiv 论文未展开；FLORA / Okara / General Intelligence 案例为官方口径，未独立核验。

## 翻译质量评估（本次初判）

- 计划**完整逐译**正文（含全部小标题、对照表、FAQ 与「Key takeaways」），保留全部超链接；
  「More Build with AI articles」「Ready to deploy」等站点导航噪音不译。
- 术语表初定：orchestration=编排；single-agent loop=单智能体循环；prompt chaining=提示词链（链式提示词）；
  routing=路由；parallelization=并行化；orchestrator-worker=编排器-工作器；evaluator-optimizer=评估器-优化器；
  multi-hop reasoning=多跳推理；fan-out=扇出；anti-pattern=反模式；human-in-the-loop=人在回路；
  context window=上下文窗口；durable/durability=持久化；checkpoint=检查点；subagent=子智能体；
  microVM=微虚拟机；session correlation=会话关联；runaway critique loop=失控评审循环。
- 关键数字抽查锚点：15×、20 步默认上限、95%→60% / 90%→35%、61% 支出占 32% token、12 万+ 企业、
  40 亿 token/日、50+ 图像模型、10 PR / 70+ commits / 4,000+ 分支 / 90% SRE、96% 提速、$0.128/小时、
  1,800 秒、45 分钟 / 24 小时。
- 预计质量为「精品级」：结构规整（六个模式 + 四平台行为 + FAQ），术语可精确对应，表格是天然对照体。

## 与知识库契合度

- 主题位于知识库核心区：AI Agent 架构 / 编排模式（references 编号正文中 agent 条目多为工具/协议/评测/单一实践，
  本文补的是**多智能体编排模式的系统性选型框架**这一薄弱环节）。
- 与既有条目关系：`expand/thinking/MCP协议标准化的增量与边界.md`（协议 vs 编排，可互为背景）；
  `expand/06-AI与LLM/Agent研究与评测/`（DungeonBench 等评测条目可承接「多智能体 vs 单智能体」结论）；
  待处理队列中 "The new rules of context engineering"（Claude 官方）与本文同属「harness 组装」主题，
  一个讲上下文减重、一个讲调用结构选型，可对照阅读。
- 无重复风险：expand 层目前没有编排模式 / orchestrator-worker 条目。

## 收录建议

- **建议去向：working/ 正式收录**（译文作品，可独立理解，适合对外分享）。
- 理由：系统性选型框架 + 密集实证数字 + 与知识库 Agent 主题强相关；六模式对照表可独立复用。
- 评审后可考虑：① 补一条 expand/thinking 观点条目（「过早扇出」与「单智能体基线优先」的本质：
  编排复杂度是负债，只有出现能力缺口才值得买入）；② 对照表 + 升级判定清单可沉淀进 prompts/
  作为「agent 架构评审」提示词的素材（待实测后）。

## 观点建议（供人类评审参考，不写 expand 正文）

1. 全文最值得记住的不是六种模式，而是「**选择发生在任何基础设施决策之前**」：
   成本结构（token、I/O 等待计费、上下文窗口隔离）先于框架定生死；Vercel 把四件套挂在选型之后，
   暗示平台竞争已从「模型能力」转向「编排层基础设施」。
2. 「等计算预算下单智能体 ≥ 多智能体」与 Anthropic「15× token」同框出现，说明多智能体的收益
   常被算力差掩盖——评估这类论文/案例时，先问「预算是否对齐」，再谈架构优势。
3. 链式精度复利（95%×10 ≈ 60%）与「程序化闸门不可省略」是同一枚硬币的两面：
   任何把中间结果直接喂给下一步的流水线，都必须把校验做成硬闸门而非提示词约定。
4. 对照表是规划工具而非价格表——「token 成本是相对估计」这个限定条件值得保留，
   否则容易被当成固定费率用于预算预测。
