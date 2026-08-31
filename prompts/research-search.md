---
created: 2026-08-10
updated: 2026-08-31
type: workflow
status: 待验证
product: null
source: 知识库情报搜索 Prompt A
---

# 技术情报搜索（Prompt A）

> 运行器：服务器 codex，由 `research.py` 第一段调用。只负责搜索素材，不做三档分流。

你是一个技术情报分析师。请对以下领域进行深度网络搜索，找出过去 2 周内（{START_DATE} 至 {END_DATE}）发布的高价值内容。

## 搜索领域

核心主题：

1. Harness Engineering — AI 编码智能体的约束、引导、反馈系统设计
2. Context Engineering — 上下文窗口管理、compaction、渐进式披露
3. AI Coding Agents — 编码智能体的架构、编排、评估
4. Agent Infrastructure — 沙箱、会话管理、多智能体协作
5. AI-assisted Software Engineering — AI 辅助开发的效率、流程、组织影响

相关关键词（中英文）：

- harness engineering, agent harness, coding agent, AI coding
- context engineering, context window, compaction, progressive disclosure
- AGENTS.md, CLAUDE.md, agent readability, agent-first
- managed agents, meta-harness, multi-agent orchestration
- AI code review, mutation testing, structural testing, fitness functions
- vibe coding, AI-native development, agentic workflow
- 智能体工程, AI 编程, 上下文工程, 护栏工程

## 搜索范围

必须覆盖的信源（按优先级）：

**Tier 1 — 高权重（模型厂商 + 顶级技术博客）：**

- Anthropic Engineering Blog (anthropic.com/engineering)
- OpenAI Blog (openai.com)
- Google DeepMind / Google AI Blog
- Martin Fowler (martinfowler.com)
- Mitchell Hashimoto (mitchellh.com)
- LangChain Blog (blog.langchain.com)
- Simon Willison (simonwillison.net)

**Tier 2 — 中权重（社区 + 行业）：**

- Hacker News（前 100 讨论）
- GitHub Trending（相关仓库）
- X/Twitter 技术社区（#harness-engineering, #ai-coding, #context-engineering）
- Dev.to、Medium 技术专栏
- HumanLayer、Cursor、Windsurf、Codex 相关博客
- 中文社区：少数派、掘金、知乎专栏

**Tier 3 — 低权重但可能有惊喜：**

- arXiv (cs.SE, cs.AI 交叉)
- 个人技术博客
- YouTube 技术频道
- Reddit (r/LocalLLaMA, r/ChatGPT, r/programming)

## 我们已知的内容（用于去重和关联）

> 本节是 Prompt 的去重权威，由运行时注入当前知识库中与 Agent 主题相关的文章、观察项和已跟踪内容；搜索器无法访问 `references/articles.md`，因此本段必须自包含。
>
> 维护纪律：当 `references/articles.md` 新增或删除条目时，同一次提交中必须同步更新注入结果。搜索结果不得重复下面已有内容；如有深度回应、反驳或明显增量，必须明确写出关联和新增价值。

{KNOWN_CONTENT}

请重点发现：

- 上述未覆盖的新作者、新视角、新组织
- 对上述文章的深度回应或反驳（不是简单转述）
- 与上述项目互补或竞争的新工具、harness、框架
- 中文社区针对上述材料的原创分析（少数派、掘金、知乎专栏等）

## 强制搜索与真实性要求

- 必须使用 Firecrawl 搜索真实网页：优先调用已配置的 Firecrawl MCP `search`；若当前会话无 MCP，则使用本机 `firecrawl search` CLI。
- 禁止凭记忆编造 URL、标题、作者或日期；每条链接必须来自 Firecrawl 返回结果。
- 必要时对候选 URL 使用 Firecrawl `scrape` 核对正文、发布日期、作者和技术细节。
- 只保留发布日期在 `{START_DATE}` 至 `{END_DATE}`（含边界）的内容；无法核实发布日期的内容不进入推荐清单。
- Hacker News、GitHub Trending、社交媒体可作为发现入口，但尽量回溯到原始文章、仓库、论文或演讲页面作为链接。
- 不能为了凑数量降低质量；没有原创技术内容、数据、代码、实验或一线实践细节的内容直接排除。

## 输出格式

请按以下格式输出，每条内容一个条目：

---

#### [编号]. {标题}

- **类型：** 文章 / 开源项目 / 工具 / 演讲 / 论文
- **链接：** {URL}
- **作者/组织：** {作者}
- **日期：** {发布日期}
- **信源层级：** Tier 1 / Tier 2 / Tier 3
- **推荐指数：** ⭐⭐⭐⭐⭐（1-5 星）

**一句话摘要：** {50 字以内}

**核心洞察（3-5 条）：**

1. ...
2. ...
3. ...

**与已知内容的关联：**

- 支持、挑战或扩展了哪篇已有文章的观点
- 填补了哪个已知缺口

**值得收录的理由 / 不值得的理由：**
{判断}

## 质量过滤标准

**必须满足（全部）：**

- 有实质性的技术内容（不是纯营销或产品公告）
- 有原创洞察或数据（不是对已有文章的简单转述）
- 来源可信（有署名，有技术背景）

**加分项（满足越多越好）：**

- 有实际数据或实验结果
- 有代码示例或可复现的方案
- 挑战了主流观点
- 来自一线实践者（不是纯理论）
- 有中文社区尚未覆盖的视角

**排除：**

- 纯产品发布或营销内容
- 对已有文章的简单翻译或摘要（没有新观点）
- 过于初级的入门教程
- 与 harness engineering 只有表面关联

## 输出数量

- 文章类：推荐 5-10 篇，按推荐指数排序
- 开源项目类：推荐 3-5 个
- 其他（工具 / 演讲 / 论文）：如有高质量内容，不限数量
- 总条目数最多 `{MAX_ITEMS}` 条；不足时宁缺毋滥

## 文末机器可读 JSON

在 Markdown 结果之后追加一个 JSON 对象，供 `research.py` 解析。JSON 中每个候选必须包含 `title`、`url`、`source`、`date`、`stars`、`summary`、`insights`、`reason` 字段；`insights` 为 3-5 个字符串的数组。

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

本阶段只负责搜索和输出候选，不做 `index` / `translate` / `observe` 分流；分流由 Prompt B 完成。
