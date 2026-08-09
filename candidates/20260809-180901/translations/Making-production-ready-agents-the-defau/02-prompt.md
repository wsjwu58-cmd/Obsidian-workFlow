---
created: 2026-08-09
updated: 2026-08-09
type: prompt-draft
status: 过程稿
sources:
  - url: https://blog.duolingo.com/production-ready-ai-agent-platform/
tags: [AI Agent, 智能体平台, 翻译, prompt]
---

# 02 本次翻译使用的提示词（过程稿）

> 本次翻译用如下提示词驱动。原文已抓取到
> `candidates/20260809-180901/sources/Making-production-ready-agents-the-defau.md`
> （firecrawl markdown 主内容），全文 HTML 存于同名 `-full.md`。

## 提示词正文

```
你是一名资深技术译者（英→中），翻译 Duolingo 工程博客
《Making production-ready agents the default: building Duolingo's agent platform》。

## 输入
- 原文：candidates/20260809-180901/sources/Making-production-ready-agents-the-defau.md
  （正文从 "At Duolingo, teams were repeatedly rebuilding the same infrastructure"
  到 "we're hiring!" 的招聘 CTA 为止；
  忽略作者头像行、TAGS / SHARE ARTICLE / RELATED ARTICLES 等站点噪音。）

## 输出要求
1. 完整逐译正文全部段落与小标题（TL;DR、Every team was rebuilding the same infrastructure、
   Defining an agent、Why Temporal?、Decoupling definition from execution（含 A new runtime）、
   Evaluating agents（含 How grading works、Running evals as workflows）、
   From weeks to minutes、What's next?、Conclusion），不压缩、不删节。
2. 保留原文全部超链接（Markdown 链接写法原样保留，链接文字翻译成中文）；
   代码块（AgentDefinition、AgentWorkflow 调用、YAML 评测用例）整体原样保留不译。
3. 术语表（必须一致）：
   - production-ready → 生产就绪
   - productionizing → 生产化（首现可注 productionizing）
   - registry → 注册表（首现可注 registry）
   - durable workflow engine → 持久化工作流引擎
   - durable state → 持久化状态
   - activity → 活动（Temporal 概念，首现可注 Activity）
   - query → 查询（Temporal Query）
   - side effect → 副作用
   - decouple definition from execution → 定义与执行解耦
   - runtime → 运行时
   - LLM Gateway → LLM 网关
   - agent eval / agent evals → 智能体评测
   - authored scenario → 编写好的场景
   - grader → 评分器
   - structured_output / diff_assertions / no_op_consistency → 评分器名保留原文，
     正文说明处可译「结构化输出 / 差异断言 / 空操作一致性」并保留原名
   - LLM-as-judge → LLM 作为裁判（首现可注 LLM-as-judge）
   - brittle → 脆弱
   - suite workflow → 套件工作流
   - child workflow → 子工作流
   - multi-entry-point invocation → 多入口调用
   - orchestration → 编排
   - observability → 可观测性
   - abstraction → 抽象
   - Temporal / MCP / OpenAI Agents SDK / Claude Agents SDK / Codex CLI / Slack /
     gpt-5.5 / AgentWorkflow / AgentDefinition 等专名与代码标识符保留原文
4. 数字与专名逐一比对原文，不得改动：2026-08-04、10 分钟、数周、gpt-5.5、
   mcp_servers=("github", "sentry")、max_changed_files: 1、incident_summary、
   fix_ci / missing_requests_import / fixtures/missing_requests_repo /
   prompts/fix_ci_eval_prompt.md、Temporal UI、LLM Gateway。
5. 标题译名：主标题「让生产就绪的智能体成为默认：构建 Duolingo 的智能体平台」；
   副标题「看看我们如何让 AI 智能体在生产环境中易于构建、运行与改进」。
6. 中文表达通顺自然，术语到位；输出 Markdown，标题层级沿用原文；frontmatter：
   ---
   created: 2026-08-09
   updated: 2026-08-09
   title: 让生产就绪的智能体成为默认：构建 Duolingo 的智能体平台
   sourceUrl: https://blog.duolingo.com/production-ready-ai-agent-platform/
   sourceAuthor: Guadalupe Aliseda-Canton（Duolingo 工程博客）
   translatedAt: 2026-08-09
   sources: [references/articles.md 待处理队列]
   tags: [AI Agent, 智能体平台, 生产就绪, Temporal, MCP, 评测, type/翻译]
   ---
```

## 执行备注

- 抓取方式：`firecrawl scrape -f markdown --only-main-content`（17KB）；
  全文 HTML 用 `-f html --only-main-content` 抓取（47KB）备用核对；
  页面署名 Guadalupe Aliseda-Canton，发布日期 2026-08-04。
- 翻译策略：术语优先 + 完整逐译；三处代码块（AgentDefinition、AgentWorkflow 调用、
  YAML 评测用例）整体保留不译；站点头部/分享/相关文章噪音剔除。
- 关键数字比对：2026-08-04、10 分钟 vs 数周、gpt-5.5、("github","sentry")、
  max_changed_files: 1、四步 AgentWorkflow 流程、三类评分器 + 可选 LLM-as-judge
  已抽查一致。
- 该提示词本身不直接沉淀进 prompts/（curate 产出边界：不写 prompts/），
  留待评审通过、实测后再考虑复用。
