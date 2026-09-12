---
created: 2026-09-12
updated: 2026-09-12
type: prompt-draft
status: 过程稿
sources:
  - url: https://github.com/langchain-ai/langchain
tags: [LangChain, 翻译, prompt, GitHub README]
---

# 02 本次翻译使用的提示词（过程稿）

> 本次翻译用如下提示词驱动。原文（英文 README）已抓取到
> `candidates/20260912-080217/sources/langchain-ai-langchain---The-agent-engin.md`
> （GitHub API `repos/langchain-ai/langchain/readme` raw 取得权威正文，仓库元数据取
> `repos/langchain-ai/langchain`，并与 firecrawl 页面主内容交叉核对）。

## 提示词正文

```
你是一名资深技术译者（英→中），翻译 GitHub 开源仓库 langchain-ai/langchain 的主 README
（标题：The agent engineering platform.）。

## 输入
- 原文：candidates/20260912-080217/sources/langchain-ai-langchain---The-agent-engin.md
  （正文从 "LangChain is a framework for building agents and LLM-powered applications"
   到 "community guidelines and standards" 为止；忽略文件头部的采集元信息块。）
- 仓库元数据（2026-09-12）：stars 146,137 / forks 24,416 / open issues 486 /
  subscribers 919，主语言 Python，许可证 MIT，仓库创建 2022-10-17，默认分支 master。

## 输出要求
1. 完整逐译正文全部段落、小标题、列表与代码块，不压缩、不删节；
   顶部 <picture> logo 与 shields.io 徽章 HTML（PyPI License / Downloads / Version、
   Twitter/X）原样保留，不翻译其 alt 周边文案。
2. 保留原文全部超链接（Markdown 链接写法原样保留，链接文字翻译成中文）；
   代码与标识符原样保留：uv add langchain、init_chat_model、
   openai:gpt-5.5、model.invoke("Hello, world!")、LangGraph、LangChain.js、
   LangSmith、LangSmith Deployment、Deep Agents、Integrations。
3. 术语表（必须一致）：
   - agent / agentic → Agent / Agentic（首现可注「智能体」）
   - agent engineering platform → Agent 工程平台
   - LLM-powered applications → LLM 应用
   - chains → 链
   - embeddings → 嵌入
   - vector stores → 向量存储
   - retrievers → 检索器
   - integrations → 集成
   - real-time data augmentation → 实时数据增强
   - model interoperability → 模型互操作性
   - rapid prototyping → 快速原型开发
   - production-ready → 生产就绪
   - orchestration → 编排
   - subagents → 子 Agent
   - file system usage → 文件系统使用
   - future-proofing → 面向未来 / 前瞻性
   - Code of Conduct → 行为准则
   - good first issues → 适合新手的问题
   - Deep Agents / LangGraph / LangSmith / LangSmith Deployment / LangChain.js 保留原文
4. 数字与结论逐一比对原文，不得改动：146,137 stars / 24,416 forks / 486 open issues、
   生态五点、六点价值主张、资源七条、模型示例 openai:gpt-5.5。
5. 中文表达通顺自然，术语到位；输出 Markdown，标题层级沿用原文；frontmatter：
   ---
   created: 2026-09-12
   updated: 2026-09-12
   title: langchain-ai/langchain —— Agent 工程平台
   sourceUrl: https://github.com/langchain-ai/langchain
   sourceAuthor: LangChain（LangChain, Inc. 官方 GitHub 仓库）
   translatedAt: 2026-09-12
   sources: [references/articles.md 待处理队列]
   tags: [LangChain, Agent, LLM, LangGraph, Deep Agents, LangSmith, 框架, type/翻译]
   ---
```

## 执行备注

- 抓取方式：GitHub API `repos/langchain-ai/langchain/readme`（raw）取得权威正文；
  `repos/langchain-ai/langchain` 取 stars/forks/issues/license/language 等元数据；
  firecrawl `scrape -f markdown --only-main-content` 抓仓库页面主内容交叉核对。
- 翻译策略：术语优先 + 完整逐译；「Quickstart」「LangChain ecosystem」「Why use LangChain?」
  「Resources」等小节结构与英文版一致。
- 关键数字比对：README 正文本身只在徽章里出现动态数字，译文以 2026-09-12 采集快照为准，
  属于时点值；stars 146,137 / forks 24,416 / open issues 486 已抽查与 API 一致。
- 该提示词本身不直接沉淀进 prompts/（curate 产出边界：不写 prompts/），
  留待评审通过、实测后再考虑复用。
