---
created: 2026-09-12
updated: 2026-09-12
type: prompt-draft
status: 过程稿
sources:
  - url: https://github.com/langgenius/dify
tags: [Dify, 翻译, prompt, GitHub README]
---

# 02 本次翻译使用的提示词（过程稿）

> 本次翻译用如下提示词驱动。原文（英文 README）已抓取到
> `candidates/20260912-080217/sources/langgenius-dify---Build-Agentic-workflow.md`
> （GitHub API `repos/langgenius/dify/readme` + firecrawl 页面主内容交叉核对；
> 官方 `docs/zh-CN/README.md` 仅作术语对照，不改动英文原文结构）。

## 提示词正文

```
你是一名资深技术译者（英→中），翻译 GitHub 开源仓库 langgenius/dify 的主 README
（标题：Build Agentic workflows, RAG pipelines, with rich AI model and tool support
on one collaborative workspace）。

## 输入
- 原文：candidates/20260912-080217/sources/langgenius-dify---Build-Agentic-workflow.md
  （正文从 "Dify is an open-source LLM app development platform" 到
   "based on Apache 2.0 with additional conditions" 为止；
   忽略文件头部的采集元信息块、shields.io 状态徽章、语言切换徽章、
   Star History 图表、contrib.rocks 贡献者图片等站点噪声。）
- 仓库元数据（2026-09-12）：stars 155,457 / forks 24,552 / open issues 1,067，
  主语言 TypeScript，仓库创建 2023-04-12。

## 输出要求
1. 完整逐译正文全部段落、小标题、列表与代码块，不压缩、不删节；
   徽章 / 图表等 HTML 与图片链接原样保留，不翻译其中的 alt 周边文案。
2. 保留原文全部超链接（Markdown 链接写法原样保留，链接文字翻译成中文）；
   代码与标识符原样保留：docker compose up -d、cp .env.example .env、
   http://localhost/install、README.md、CONTRIBUTING.md、ADVANCED_SETUP.md、
   self-hosting、Backend-as-a-Service、LLMOps、Prompt IDE、ReAct 等。
3. 术语表（必须一致）：
   - workflow / AI workflow → 工作流 / AI 工作流
   - RAG pipeline → RAG 管道
   - agent / agentic → Agent / Agentic（首现可注「智能体」）
   - model management → 模型管理
   - observability → 可观测性
   - self-hosting → 自托管
   - cloud → 云服务
   - Function Calling → 函数调用
   - document ingestion → 文档摄入
   - retrieval → 检索
   - starter guide → 入门指南
   - Contribution Guide → 贡献指南
   - good first issues → 适合新手的问题
   - Dify Open Source License 保留原文
4. 数字与结论逐一比对原文，不得改动：CPU >= 2 Core、RAM >= 4 GiB、
   Docker Compose v2.24.0 或更高、50+ 内置工具、200 次免费 GPT-4 调用、
   七大核心功能编号 1–7。
5. 中文表达通顺自然，术语到位；输出 Markdown，标题层级沿用原文；frontmatter：
   ---
   created: 2026-09-12
   updated: 2026-09-12
   title: langgenius/dify —— 在一个协作工作区里构建 Agentic 工作流与 RAG 管道
   sourceUrl: https://github.com/langgenius/dify
   sourceAuthor: LangGenius（Dify 官方 GitHub 仓库）
   translatedAt: 2026-09-12
   sources: [references/articles.md 待处理队列]
   tags: [Dify, LLMOps, AI 工作流, RAG, Agent, 低代码, type/翻译]
   ---
```

## 执行备注

- 抓取方式：GitHub API `repos/langgenius/dify/readme`（raw）取得权威正文；
  firecrawl `scrape -f markdown --only-main-content` 抓仓库页面主内容交叉核对，
  `-f html` 抓页面 HTML 备用；仓库另有官方 `docs/zh-CN/README.md` 仅用于术语对照。
- 翻译策略：术语优先 + 完整逐译；「Key features」「Using Dify」等小节结构与英文版一致
  （官方 zh-CN 版结构与英文版不同，本次不采用其分节方式）。
- 关键数字比对：2 Core / 4 GiB / Compose v2.24.0 / 50+ 工具 / 200 次 GPT-4 调用 /
  1–7 编号已抽查一致；仓库热度数据以 2026-09-12 采集快照为准，属于时点值。
- 该提示词本身不直接沉淀进 prompts/（curate 产出边界：不写 prompts/），
  留待评审通过、实测后再考虑复用。
