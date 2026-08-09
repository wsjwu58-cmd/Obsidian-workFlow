---
created: 2026-08-09
updated: 2026-08-09
type: prompt-draft
status: 过程稿
sources:
  - url: https://vercel.com/i/agent-orchestration-patterns
tags: [AI Agent, 编排, 翻译, prompt]
---

# 02 本次翻译使用的提示词（过程稿）

> 本次翻译用如下提示词驱动。原文已抓取到
> `candidates/20260809-180901/sources/Six-Agent-Orchestration-Patterns.md`
> （firecrawl markdown 主内容），全文 HTML 存于同名 `-full.md`。

## 提示词正文

```
你是一名资深技术译者（英→中），翻译 Vercel 官方平台指南
《Six Agent Orchestration Patterns》。

## 输入
- 原文：candidates/20260809-180901/sources/Six-Agent-Orchestration-Patterns.md
  （正文从 "Once an AI feature grows past a single prompt" 到 FAQ 最后一问
  "resume from the last checkpoint" 为止；
  忽略 [Skip to content]、More Build with AI articles、Ready to deploy 等站点噪音。）

## 输出要求
1. 完整逐译正文全部段落、小标题、对照表与 FAQ，不压缩、不删节；
   站点头部导航 / 相关文章 / 部署 CTA 不译。
2. 保留原文全部超链接（Markdown 链接写法原样保留，链接文字翻译成中文）；
   代码标识符（ToolLoopAgent、stopWhen: stepCountIs(20)、prepareStep、
   runtimeContext、WorkflowAgent、use workflow、Sandbox.fork() 等）原样保留。
3. 术语表（必须一致）：
   - orchestration → 编排
   - single-agent loop → 单智能体循环
   - prompt chaining → 提示词链（首现可注 prompt chaining）
   - routing → 路由
   - parallelization → 并行化
   - orchestrator-worker → 编排器-工作器（首现可注 orchestrator-worker）
   - evaluator-optimizer → 评估器-优化器（首现可注 evaluator-optimizer）
   - multi-hop reasoning → 多跳推理
   - fan-out → 扇出
   - anti-pattern → 反模式
   - human-in-the-loop → 人在回路
   - context window → 上下文窗口
   - durable / durability → 持久化
   - checkpoint → 检查点
   - subagent → 子智能体
   - microVM → 微虚拟机
   - session correlation → 会话关联
   - run away critique loop → 失控评审循环
   - premature fan-out → 过早扇出
   - Fluid compute / AI Gateway / Vercel Workflows / Vercel Sandbox /
     OpenTelemetry / Firecracker / AGENTS.md 等专名保留原文
4. 数字与结论逐一比对原文，不得改动：15×、20 步、95%→约 60%、90%→约 35%、
   61% 支出 / 32% token、120,000+ 企业、4 billion tokens、50+ 图像模型、
   10 PR / 70+ commits / 4,000+ 分支 / 90% SRE、96%、$0.128/小时、
   1,800 秒、45 分钟 / 24 小时。
5. 六模式对照表保留为 Markdown 表格，表头译成中文，单元格内容译为中文。
6. 中文表达通顺自然，术语到位；输出 Markdown，标题层级沿用原文；frontmatter：
   ---
   created: 2026-08-09
   updated: 2026-08-09
   title: 六种智能体编排模式
   sourceUrl: https://vercel.com/i/agent-orchestration-patterns
   sourceAuthor: Vercel（官方平台指南）
   translatedAt: 2026-08-09
   sources: [references/articles.md 待处理队列]
   tags: [AI Agent, 编排, Agent 架构, Vercel, AI SDK, type/翻译]
   ---
```

## 执行备注

- 抓取方式：`firecrawl scrape -f markdown --only-main-content`（20KB）；
  全文 HTML 用 `-f html --only-main-content` 抓取（114KB）备用核对；
  页面无作者署名与发布日期，sourceAuthor 记为 Vercel（官方平台指南）。
- 翻译策略：术语优先 + 完整逐译；六个模式标题保留「1. … 6. …」编号；
  「Key takeaways」用列表保留；对照表整体翻译并校验表头与原文一一对应。
- 关键数字比对：15×、20 步、95%/90% 精度复利、61%/32%、120,000+、4 billion、
  50+、10 PR/70+ commits/4,000+ 分支/90%、96%、$0.128/小时、1,800 秒、
  45 分钟/24 小时共 13 组已抽查一致。
- 该提示词本身不直接沉淀进 prompts/（curate 产出边界：不写 prompts/），
  留待评审通过、实测后再考虑复用。
