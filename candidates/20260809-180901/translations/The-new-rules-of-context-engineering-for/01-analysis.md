---
created: 2026-08-09
updated: 2026-08-09
type: analysis
status: 待评审
sources:
  - title: The new rules of context engineering for Claude 5 generation models
    url: https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models
    source: research
    date: 2026-08-09
tags: [Claude, 上下文工程, AI Agent, Harness, 候选评审]
---

# 01 原文分析：The new rules of context engineering for Claude 5 generation models

## 原文信息

- **标题：** The new rules of context engineering for Claude 5 generation models
- **作者：** Thariq Shihipar（Anthropic technical staff）
- **发布：** 2026-07-24，claude.com/blog（分类：Claude Code / Agents）
- **篇幅：** 约 5 分钟阅读（正文约 1,900 英文词，抓取 Markdown 约 15KB）

## 原文价值评估（高 / 中 / 低）

**高。** 不是发布稿或产品页，而是 Anthropic 官方对新一代 Claude 模型（Opus 5 / Fable 5）
上下文工程的**第一手工程经验**，且给出了可执行的动作：

- 核心实证数字：**对 Opus 5 / Fable 5 删除 Claude Code 系统提示词 80%+，编码评测无可测量损失**。
- 给出 6 组「旧规则 → 新规则」对照（规则→判断、示例→接口设计、全量前置→渐进披露、
  重复强调→精简工具描述、CLAUDE.md 记忆→自动记忆、简单 spec→富引用）。
- 落地工具：`claude doctor`（/doctor）自动精简 skills 与 CLAUDE.md；工具描述 vs 系统提示词
  的职责分工；Skill 渐进披露；References 用代码/HTML 制品/评分标准（rubrics）而非文字描述。
- 隐含方法论：「unhobbling」——为旧模型设计的护栏在新模型上反而成为约束，需按模型代际
  重新评估约束成本。这个判断框架可迁移到任何自建 agent harness。

局限：文章是经验分享，无基准细节（哪些评测、降幅多大未披露）；部分建议（如 auto-memory、
deferred loading）依赖 Claude Code 生态内能力，迁移到其他 harness 需自行等价实现。

## 翻译质量评估（本次初判）

- 计划**完整逐译**正文（非压缩摘要），保留全部超链接与术语（system prompt / context engineering /
  progressive disclosure / deferred loading / rubrics 等）。
- 术语表初定：context engineering=上下文工程；progressive disclosure=渐进披露（渐进式揭示）；
  deferred loading=延迟加载；unhobbling=解除束缚；rubrics=评分标准/准则；artifacts=制品；
  harness=执行框架/工作台（保留英文首现标注）。
- 关键数字抽查锚点：80%+ 系统提示词削减、Opus 5/Fable 5、Todo 状态枚举 pending/in_progress/completed。
- 预计质量为「精品级」：短篇、结构清晰、术语密集但可精确对应。

## 与知识库契合度

- 主题位于知识库核心区：AI Agent / Harness Engineering（references 编号 01-15 中 agent 相关条目
  多为工具/协议/评测，本文补的是**系统提示词与上下文组装策略**这一薄弱环节）。
- 与既有条目关系：`expand/thinking/MCP协议标准化的增量与边界.md`（协议 vs 上下文组装互补）、
  `expand/06-AI与LLM/Agent工具与平台/`（Claude Code 工具链）、待处理队列中
  "AGENTS.md Contract"（dev.to）与 "Auto mode in production" 可作对照阅读。
- 无重复风险：expand 层目前没有上下文工程/提示词工程条目。

## 收录建议

- **建议去向：working/ 正式收录**（译文作品，可独立理解，适合对外分享）。
- 理由：官方一手经验 + 可迁移方法 + 与知识库 Agent 主题强相关；译文可独立成篇，
  也可作为后续「上下文工程」概念条目的素材源。
- 评审后可考虑：① 补一条 expand/thinking 观点条目（约束成本随模型代际迁移的框架）；
  ② 将 `claude doctor` 工作流沉淀进 prompts/（待实测后）。

## 观点建议（供人类评审参考，不写 expand 正文）

1. 「删掉 80% 系统提示词无损失」的本质是**约束收益递减**：旧护栏防的是旧模型的「最坏情况」，
   新模型的判断力使约束的边际成本超过边际收益。迁移到自建 harness 时应做「约束审计」：
   逐条问「这条规则防的是哪种失败？当前模型还会犯吗？」
2. 「示例约束探索空间」与直觉相反，但解释了 Claude Code 逐步转向 ToolSearch/延迟加载的设计动机：
   提示词的职责是「给方向」，工具的职责是「给接口」。接口表达力 > 示例堆砌。
3. 本文可与 Anthropic 工程博客《Effective context engineering for AI agents》对照读：
   前一篇讲组装，本文讲「减重」。两篇合起来才是完整方法论。
