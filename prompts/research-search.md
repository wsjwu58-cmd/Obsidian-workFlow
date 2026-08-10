---
created: 2026-08-10
updated: 2026-08-10
type: workflow
status: 待验证
product: null
source: 知识库情报搜索 Prompt A
---

# 技术情报搜索（Prompt A）

> 运行器：服务器 codex，由 `research.py` 第一段调用。只负责**搜索素材**，不做三档分流。

你是技术情报分析师。搜索以下领域过去 2 周（{START_DATE} ~ {END_DATE}）的高质量内容。

## 强制工具（必须遵守）

- 必须使用 **Firecrawl** 搜索真实网页：优先调用已配置的 Firecrawl MCP `search`；若当前会话无 MCP，则使用本机 `firecrawl search` CLI。
- 禁止凭记忆编造 URL / 标题；每条链接须来自 Firecrawl 返回结果。
- 可对候选 URL 再用 Firecrawl `scrape` 核对摘要与发布日期；日期窗外的丢弃。

## 领域

1. AI Agent 开发：RAG / Agent 工程（harness / 编排 / 上下文管理 / 调度）/ 多智能体 / 评测 / 工具平台（langchain4j / langgraph4j / Claude Code / Codex）
2. 跨平台开发：Kotlin 多平台（KMP / Compose Multiplatform）/ Flutter 架构与工具链

## 建议查询（可多轮，中英均可，经 Firecrawl 执行）

- agent harness orchestration context engineering
- langchain4j langgraph4j RAG evaluation
- Kotlin Multiplatform Compose Multiplatform
- Flutter architecture toolchain

## 信源优先级

- Tier 1：Anthropic / OpenAI / Google / LangChain 官方博客、Martin Fowler、Simon Willison、Addy Osmani
- Tier 2：HackerNews、GitHub Trending、掘金、知乎专栏
- Tier 3：arXiv (cs.SE/cs.AI)、个人技术博客

## 去重权威（本知识库）

已收录完整列表由代码注入（运行时 `python scripts/retrack.py --list`）：

{KNOWN_CONTENT}

## 输出（每条；最多 {MAX_ITEMS}；未达门槛勿输出）

## {编号}. {标题}

- 链接：{url}
- 作者/来源：{source}
- 日期：{date}
- 推荐指数：⭐⭐⭐（3-5）

一句话摘要：{50 字内}

核心洞察（3条）：

1. …
2. …
3. …

值得收录理由：{判断}

## 质量门槛

- 必须：有实质技术内容 / 原创洞察 / 来源可信
- 加分：有数据 / 可复现代码 / 挑战主流观点
- 排除：纯营销 / 纯摘要 / 草稿级入门教程

## 文末机器可读 JSON

```json
{
  "candidates": [
    {
      "title": "...",
      "url": "...",
      "source": "...",
      "date": "YYYY-MM-DD",
      "stars": 4,
      "summary": "50字内",
      "insights": ["...", "...", "..."],
      "reason": "一句话"
    }
  ]
}
```

本阶段**不做** index / translate / observe 分流（由 Prompt B 分析完成）。
