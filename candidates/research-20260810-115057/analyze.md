已核对知识库现状（`references/articles.md` 15 条、`expand/thinking/` 2 条、`expand/06-AI与LLM/` 9 条、待处理队列 7 条）与 `research.py` 的三档分流逻辑。以下为完整分析。

## 1. 优先级排序

两条候选均为 AI Agent 域高价值内容，且与既有内容互补而非重复；跨平台侧无达标候选（不硬凑）。

| 优先级 | 候选 | 星级 | 与已收录/已跟踪内容的互补 | 对既有洞见的验证/挑战 | 对开放问题的回答 |
|---|---|---|---|---|---|
| 1 | Snowflake data-eng-bench | ⭐⭐⭐⭐⭐ | 编号 01–05 是任务级/领域级基准（模仿学习、HPO、文档抽取、战术推理、方程发现），**缺仓库级工程基准**；`ECC.md` 明确写着「盲区：缺少公开评测数据」，本候选直接补上 | **验证** `ECC.md`「harness 是工程化主战场」论点：harness 对质量差约 4pp、对成本差 3.9x，实证化「harness 操作系统」假设；同时**挑战**「选对模型即够用」的默认认知 | 正面回答「Agent 评测：model/harness 组件级归因」——给出 harness×model 双变量矩阵 |
| 2 | Simon Willison LLM 0.32 | ⭐⭐⭐⭐ | 待处理队列中的 Claude context engineering（prompt/上下文侧）与 Duolingo 平台案例（组织侧）均不覆盖**工具链与日志架构**；与 `MCP协议标准化的增量与边界`（thinking）形成「平台工具 ↔ 协议总线」对照 | **验证** MCP 思考条目的「外部能力总线」论点：llm-anthropic 0.26 的 `AnthropicMCP` 把 MCP 调用做成单请求服务端工具 | 部分回答「上下文/记忆策略的可复现实践」与「跨模型可移植性」两个缺口 |

与待处理队列关系：data-eng-bench 是 Harness-R1 / EvolveNet（harness 自我演进）所需要的**度量基底**；LLM 0.32 与 Raccoon Heist（同为 Simon Willison）主题不同，不构成重复采集。

## 2. 缺口分析

**被覆盖的缺口**
- Agent 评测组件级归因：harness×model 矩阵 + Pass@1/Pass^3 + 每试成本/token/工具调用/agent 步数，是目前唯一直接命中该缺口的素材。
- Agent harness 行为正确性与覆盖率：103 任务仓库级 dbt DAG（中位 4 个模型、最多 42 个）+ 每任务 10–50 条隐藏断言、整管道全对才计分，把「生成像样模型」与「管道正确」分开。
- 上下文/记忆可复现实践（部分）：内容寻址消息存储（Git 式）解决多轮日志膨胀；推理轨迹 stderr 分流是可复制的工具链标准做法。
- 跨模型可移植性（部分）：`llm openai endpoint` + `llm-chat-completions-server` 提供单命令对接任意 OpenAI 兼容端点的迁移路径。
- 成本数据（部分）：每试成本 0.358–0.756 美元、成本倍数 3.9x/1.5x，可作中小团队选型锚点（非完整案例，故算部分覆盖）。

**仍未触及的缺口**
- 多智能体编排反模式与成本：搜索仅触及 survey（`Multi-Agent Debate Strategies`），未入选。
- Harness/控制的激活策略（always-on / per-commit / conditional / human-summoned）。
- Agent 安全审计（轨迹违规、多智能体信息流、工具权限边界）。
- KMP / Compose Multiplatform 与 Flutter 架构选型、共享逻辑边界、工具链痛点。
- 跨平台 CI / 发布 / 性能基线。
- 衍生新缺口：data-eng-bench 只归因 harness 与 model 两变量，「环境/仓库规模」维度（数据仓库拓扑对结果的影响）未展开，可作后续追踪方向。

## 3. 趋势信号

- **Harness 效应实证化**：评测开始把 harness 作为独立变量（质量差 ~4pp、成本差 ~3.9x），与 `ECC.md` 的 harness 层论点一致；但 CoCo 的胜出提示「域原生 harness」比「通用分层 harness」更优——这是对 ECC 通用化路线的一个温和修正信号。
- **可靠性指标标准化**：Pass@1（单次）与 Pass^3（三试全过）并列披露，把 agent 非确定性显式化，呼应本库对 agent 可靠性的关注。
- **服务端工具 + 推理轨迹成为一等公民**：OpenAI `CodeInterpreter`/`WebSearch`、Anthropic `WebFetch`/`CodeExecution`/`AnthropicMCP` 表明工具托管在向 provider 侧迁移，与 MCP 的「协议分发」形成**双轨并存**（服务端托管 vs 外部工具总线），MCP 思考条目可据此补充对照。
- **Agent 对话日志架构化**：内容寻址日志（仿 Git）把「每条请求携带全量历史」的日志膨胀作为一等工程问题解决，是可复现的记账方案。
- **跨平台窗口偏薄**：两周内 KMP/Flutter 侧以 hotfix（Flutter 3.44.9）与营销内容为主，KotlinLLM 是 Kotlin/JVM 研究而非 KMP 域，未出现可收录级动态——建议下轮把 Compose Multiplatform 1.11.0、Kotlin 2.3.20 工具链作为定向搜索目标验证（本次两者仅侧面出现）。

## 4. 收录建议

| 候选 | verdict | lineage | 一句话理由 |
|---|---|---|---|
| Snowflake data-eng-bench | `index` | `agent/eval` | 首个仓库级 dbt agent 基准，harness×model 双变量质量/成本/可靠性归因数据开源，直接填「Agent 评测归因」与 `ECC.md` 缺公开评测数据的空白，建议随收录生成 `expand/06-AI与LLM/Agent研究与评测/` 条目并与 ECC、待处理 Harness-R1/EvolveNet 建立关联 |
| Simon Willison LLM 0.32 | `index` | `agent/platform` | Tier1 作者的工具链可复现实践（推理轨迹分流、内容寻址日志、服务端工具、任意兼容端点），补上下文日志与跨模型可移植性缺口；release notes 形态不值得整体翻译，索引核心实践即可 |

两者均不选 `translate`：data-eng-bench 价值在数据与归因结论（索引 + expand 加工吸收效率更高），LLM 0.32 为发布说明型长文（已有 7 条待处理翻译在队列，且同作者 Raccoon Heist 已在队列）；`observe` 也不适用——两条都有明确的可落地增量。

```json
{
  "analysis": {
    "priority": [
      "data-eng-bench 最高优先：首个仓库级 dbt agent 基准，harness×model 双变量归因 + 成本/可靠性数据，直接补 Agent 评测归因与 ECC 缺公开评测数据的空白",
      "LLM 0.32 次优：Tier1 作者可复现工具链实践（推理轨迹分流、内容寻址日志、服务端工具、任意兼容端点），补上下文日志与跨模型可移植性缺口",
      "跨平台窗口内无达标内容（KotlinLLM 为 Kotlin/JVM 研究、Flutter 3.44.9 为 hotfix），不硬凑；两条候选均为 AI Agent 域"
    ],
    "gaps_covered": [
      "Agent 评测组件级归因：data-eng-bench 的 harness×model 矩阵（Pass@1/Pass^3/每试成本/token/工具调用/步数）",
      "Agent harness 行为正确性与覆盖率：10–50 条隐藏断言整管道计分 + 103 任务仓库级 DAG 验证",
      "上下文/记忆可复现实践（部分）：LLM 0.32 内容寻址消息存储与推理轨迹 stderr 分流",
      "跨模型可移植性（部分）：llm openai endpoint + chat-completions-server 单命令对接任意兼容端点",
      "成本数据（部分）：每试成本与 3.9x/1.5x 成本倍数可作中小团队选型锚点"
    ],
    "gaps_open": [
      "多智能体编排反模式与成本（仅触及 survey，未入选）",
      "Harness/控制激活策略（always-on/per-commit/conditional/human-summoned）",
      "Agent 安全审计（轨迹违规、多智能体信息流、工具权限边界）",
      "KMP/Compose Multiplatform 与 Flutter 架构选型、共享逻辑边界、工具链痛点",
      "跨平台 CI/发布/性能基线",
      "data-eng-bench 未展开的『环境/仓库规模』维度归因"
    ],
    "trends": [
      "harness 效应实证化：评测把 harness 作为独立变量（质量差~4pp、成本差~3.9x），验证 ECC 论点并提示域原生 harness 专业化方向",
      "可靠性指标标准化：Pass@1 与 Pass^3 并列披露，把 agent 非确定性显式化",
      "服务端工具 + 推理轨迹成为一等公民，与 MCP 外部工具总线形成双轨并存",
      "Agent 对话日志架构化：内容寻址（Git 式）日志成为多轮记账的可复现方案",
      "跨平台两周窗口偏薄，Compose Multiplatform 1.11.0 / Kotlin 2.3.20 待下轮定向验证"
    ]
  },
  "candidates": [
    {
      "title": "Introducing Data-eng-bench: Why You Need \"Data-Native\" Harnesses for Data Engineering",
      "url": "https://www.snowflake.com/en/blog/engineering/data-eng-bench-data-engineering-agent-benchmark/",
      "verdict": "index",
      "lineage": "agent/eval",
      "reason": "首个仓库级 dbt agent 基准，harness×model 双变量质量/成本/可靠性归因数据开源，直接补 Agent 评测归因与 ECC 缺公开评测数据的空白",
      "stars": 5
    },
    {
      "title": "New release of LLM adds support for reasoning traces, OpenAI Responses, server-side tools, and smarter logging",
      "url": "https://simonwillison.net/2026/Aug/4/new-release-of-llm/",
      "verdict": "index",
      "lineage": "agent/platform",
      "reason": "Tier1 作者对 agent 工具链的可复现工程实践（推理轨迹分流、内容寻址日志、服务端工具、任意兼容端点），补上下文日志与跨模型可移植性缺口",
      "stars": 4
    }
  ]
}
```

Reading prompt from stdin...
OpenAI Codex v0.147.0
--------
workdir: /root/note-worker
model: deepseek-v4-flash
provider: deepseek
approval: never
sandbox: workspace-write [workdir, /tmp, $TMPDIR] (network access enabled)
reasoning effort: none
reasoning summaries: none
session id: 019fe9ce-9590-7ad1-96c3-401fec8fa1d7
--------
user
# 技术情报分析（Prompt B）

> 运行器：服务器 codex，由 `research.py` 第二段调用。输入为 Prompt A 的搜索结果；**不再负责搜索**。

以下是最近 2 周的技术情报搜索结果。请基于我们项目的已有内容，做以下分析：

https://daily.dev/blog/best-ai-coding-agents-comparison/","title":"The best AI coding agents in 2026, compared - daily.dev","description":"Compare five AI coding agents by autonomy, reliability, and cost to pick the right tool for your workflow and review capacity.","position":1},{"url":"https://www.morphllm.com/best-ai-coding-agents-2026","title":"Best AI Coding Agents (August 2026): Scored Leaderboard - Morph","description":"# Best AI Coding Agents (August 2026): The Scored Leaderboard, Updated After GPT-5.6 and Opus 5\n## The Scored Leaderboard: AI Coding Agents (August 2026)\n| Agent / Model | SWE-bench Verified | SWE-bench Pro | Terminal-Bench 2.1 | Pricing model | Updated |\n|-|-|-|-|-|-|\n| Codex CLI / GPT-5.6 Sol (default) | no entry yet | no entry yet | 89.5% (xhigh, model) | $20/mo Plus + credits | 2026-07-30 |\n| Codex CLI / GPT-5.5 | 88.7% (OpenAI) | 58.6% | 83.4% | $20/mo Plus + credits | 2026-05-01 |\n\n## 6. OpenCode\n```\n{\n  \"provider\": {\n    \"myprovider\": {\n      \"npm\": \"@ai-sdk/openai-compatible\",\n      \"options\": { \"baseURL\": \"https://api.myprovider.com/v1\" },\n      \"models\": { }\n    }\n  }\n}\n```\n\n## Frequently Asked Questions\n### Sources\n- [OpenAI Codex (openai/codex)](https://github.com/openai/codex)","position":2},{"url":"https://www.getpanto.ai/blog/codex-ai-statistics","title":"Codex AI Statistics 2026: Users, Revenue & Growth - Panto AI","description":"# Codex AI Statistics 2026: Users, Revenue & Growth\nCodex is OpenAI’s cloud-based software engineering agent, built to handle feature writing, bug fixing, refactors, and pull requests across sandboxes and developer workflows.","position":3},{"url":"https://flowtivity.ai/blog/graph-engineering-2026-guide-openclaw-codex/","title":"From Loops to Graphs: The Next Paradigm in AI Agent Engineering","description":"# From Loops to Graphs: The Next Paradigm in AI Agent Engineering\n## The 5-Stage Graph Engineering Methodology\n### Stage 4: IMPLEMENT — Build and Measure\n- **OpenAI Codex** — use the graph-max technique (draw → send → run)","position":4},{"url":"https://www.snowflake.com/en/blog/engineering/data-eng-bench-data-engineering-agent-benchmark/","title":"A Data Engineering Benchmark for AI Agents - Snowflake","description":"# Introducing Data-eng-bench: Why You Need \"Data-Native\" Harnesses for Data Engineering\n## Measuring agent quality and cost\n| Harness | Model | Pass@1 | Pass^3 | Cost per trial ($) | Cost multiplier | Total tokens per trial |\n|-|-|-|-|-|-|-|\n| Snowflake CoCo (Code) | Opus 5 | **73.8%** | **64.1%** | 0.756 | 1 | 1,070,515 |\n| Codex | GPT 5.6 Sol | 60.5% | 49.5% | 0.538 | 1.503 | 812,306 |","position":5},{"url":"https://www.firecrawl.dev/blog/best-ai-coding-agents","title":"Best AI Coding Agents in 2026: Harness, Cost, and ... - Firecrawl","description":"# Best AI Coding Agents in 2026: Harness, Cost, and Accuracy Compared\n## TL;DR: the best AI coding agents in 2026\n| Agent | Type | Model | Entry price | Harness depth | Remote/async | Best for |\n|-|-|-|-|-|-|-|\n| **OpenAI Codex** | CLI + Cloud | GPT-5.5 | $8 Go; $20 Plus | Deep | Codex Cloud, PR review | Cross-surface + autonomy |\n\n## What are the best AI coding agents in 2026?\n| Agent | Standout | Watch out |\n|-|-|-|\n| OpenAI Codex | One agent across CLI, cloud, app, mobile, Chrome | Mid-stream 5-hour usage-limit cuts |","position":6},{"url":"https://blog.cloudflare.com/engineering-standards-enforcement/","title":"How Cloudflare enforces engineering standards using AI","description":"Both systems draw from the Cloudflare Codex, a shared source of engineering guidance built for people and agents. This post explains why we built the Codex, how it supports the engineering lifecycle, and what we plan to do next.\n\nWe rebuilt this body of knowledge as the Cloudflare Codex: a governed set of engineering standards that agents can retrieve and apply at the point of work.\n\n## [Copy link](https://bl
exec
/bin/bash -lc 'firecrawl scrape --help 2>&1 | head -40' in /root/note-worker
 succeeded in 98ms:
Usage: firecrawl scrape [options] [urls...]

Scrape one or more URLs. Multiple URLs are scraped concurrently and saved to
.firecrawl/

Arguments:
  urls                      URL(s) to scrape

Options:
  -u, --url <url>           URL to scrape (alternative to positional argument)
  -H, --html                Output raw HTML (shortcut for --format html)
  -f, --format <formats>    Output format(s). Multiple formats can be specified
                            with commas (e.g., "markdown,links,images").
                            Available: markdown, html, rawHtml, links, images,
                            screenshot, summary, changeTracking, json,
                            attributes, branding. Single format outputs raw
                            content; multiple formats output JSON.
  --only-main-content       Include only main content (default: false)
  --wait-for <ms>           Wait time before scraping in milliseconds
  -S, --summary             Output summary (shortcut for --format summary)
  --screenshot              Take a screenshot (default: false)
  --full-page-screenshot    Take a full page screenshot (default: false)
  --include-tags <tags>     Comma-separated list of tags to include
  --exclude-tags <tags>     Comma-separated list of tags to exclude
  -k, --api-key <key>       Firecrawl API key (overrides global --api-key)
  --api-url <url>           API URL (overrides global --api-url)
  -o, --output <path>       Output file path (default: stdout)
  --json                    Output as JSON format (default: false)
  --pretty                  Pretty print JSON output (default: false)
  --timing                  Show request timing and other useful information
                            (default: false)
  --max-age <milliseconds>  Maximum age of cached content in milliseconds
  --country <code>          ISO country code for geo-targeted scraping (e.g.,
                            US, DE, BR)
  --languages <codes>       Comma-separated language codes for scraping (e.g.,
                            en,es)
  -Q, --query <prompt>      Ask a question about the page content (query format)
  --profile <name>          Persistent browser profile name for maintaining
                            state across scrapes
  --no-save-changes         Load existing profile data without saving changes

exec
/bin/bash -lc 'firecrawl search "Snowflake data-eng-bench data engineering benchmark AI agents" --limit 5 --json 2>/dev/null | head -c 3000' in /root/note-worker
 succeeded in 2006ms:
{"success":true,"data":{"web":[{"url":"https://www.snowflake.com/en/blog/engineering/data-eng-bench-data-engineering-agent-benchmark/","title":"A Data Engineering Benchmark for AI Agents","description":"# Introducing Data-eng-bench: Why You Need \"Data-Native\" Harnesses for Data Engineering\nThe strongest configuration we benchmarked, Snowflake CoCo with Opus 5, successfully solves 73.8% of tasks on the first attempt (average Pass@1 across 3 trials), but only 64.1% of tasks pass on all three runs (Pass^3).\n\n## Measuring agent quality and cost\nWe test three models spanning proprietary families — Opus 5 (Anthropic), Sonnet 5 (Anthropic) and GPT 5.6 Sol (OpenAI), run with several harnesses that differ in context management, planning and tool interfaces: Snowflake CoCo, Claude Code and Codex.\n\n| Harness | Model | Pass@1 | Pass^3 | Cost per trial ($) | Cost multiplier | Total tokens per trial |\n|-|-|-|-|-|-|-|\n| Snowflake CoCo (Code) | Opus 5 | **73.8%** | **64.1%** | 0.756 | 1 | 1,070,515 |\n|  | GPT 5.6 Sol | 64.1% | 55.3% | 0.358 | 1 | 436,236 |\n\n- **Explore the benchmark:** [here](https://github.com/Snowflake-Labs/data-eng-bench)\n\n### Learn more about the author\n[![Snowflake AI Research](https://www.snowflake.com/adobe/dynamicmedia/deliver/dm-aid--249da901-4810-48b7-ab40-99208c5e3b73/default-author-image.png?preferwebp=true&quality=85)\\\n\\\n**Snowflake AI Research**](https://www.snowflake.com/en/blog/authors/snowflake-ai-research/)","position":1},{"url":"https://www.linkedin.com/posts/gilberto-hernandez_a-data-engineering-benchmark-for-ai-agents-activity-7491563856020791296-ZvZ3","title":"A Data Engineering Benchmark for AI Agents | Gilberto ...","description":"Snowflake just open-sourced data-eng-bench, a data engineering benchmark that measures how well AI agents can build and fix production data ...","position":2},{"url":"https://www.welcome.ai/content/snowflake-coco-sets-new-benchmark-for-cost-effective-ai-agents","title":"Snowflake CoCo Sets New Benchmark for Cost-Effective AI ...","description":"Data-eng-bench is designed to evaluate the performance of AI agents in data engineering tasks, providing a realistic testbed for measuring their ...","position":3},{"url":"https://github.com/Snowflake-Labs/data-eng-bench","title":"Snowflake-Labs/data-eng-bench: Data-engineering ...","description":"## Repository files navigation\ndata-eng-bench measures how well coding agents do real dbt data-engineering work on a\n\n## About\nData-engineering benchmark for coding agents (DuckDB + Snowflake dbt tasks).","position":4,"category":"github"},{"url":"https://windowsforum.com/windows-news.4/snowflake-data-eng-bench-agent-harnesses-change-dbt-scores.442001/?amp","title":"Snowflake data-eng-bench: Agent Harnesses Change dbt ...","description":"Discover data-eng-bench, an open-source data engineering benchmark for AI agents. Compare Claude Code, Codex, and Snowflake CoCo on dbt and SQL ...","position":5}]},"id":"019fe9cd-350b-71aa-94a2-1facf3ba
exec
/bin/bash -lc 'firecrawl scrape https://www.snowflake.com/en/blog/engineering/data-eng-bench-data-engineering-agent-benchmark/ --format markdown --only-main-content 2>&1 | head -c 9000' in /root/note-worker
exec
/bin/bash -lc 'firecrawl scrape https://simonwillison.net/2026/Aug/4/new-release-of-llm/ --format markdown --only-main-content 2>&1 | head -c 9000' in /root/note-worker
 succeeded in 1697ms:
Scrape ID: 019fe9cd-4747-72c5-a2bc-80d5f23dcea2
Warning: Could not save scrape session. Use --scrape-id 019fe9cd-4747-72c5-a2bc-80d5f23dcea2 with interact.
[Skip to content](https://www.snowflake.com/en/blog/engineering/data-eng-bench-data-engineering-agent-benchmark/#responsive-grid-main-content)

[Blog](https://www.snowflake.com/en/blog/engineering/)/ [Data Engineering](https://www.snowflake.com/en/blog/engineering/data-engineering/)/Introducing Data-eng-bench: Why You Need "Data-Native" Harnesses for Data Engineering

Aug 6, 2026/10 min readData Engineering

Copy post link

Open in ClaudeOpen in ChatGPT

# Introducing Data-eng-bench: Why You Need "Data-Native" Harnesses for Data Engineering

[![Snowflake AI Research](https://www.snowflake.com/adobe/dynamicmedia/deliver/dm-aid--249da901-4810-48b7-ab40-99208c5e3b73/default-author-image.png?preferwebp=true&quality=85)\\
\\
Snowflake AI Research](https://www.snowflake.com/en/blog/authors/snowflake-ai-research/)

![](https://www.snowflake.com/adobe/dynamicmedia/deliver/dm-aid--85d72614-270b-4273-9e68-6bb4ddc3a612/sf-eng-blog-ml-3.png?preferwebp=true&quality=85)

As AI agents move from writing individual functions to owning end-to-end workflows, data teams face a harsh reality: general-purpose coding agents, regardless of their proficiency in Python or SQL, can struggle with production-grade data engineering. They often fail to complete tasks or incur high costs. This is a demanding test of an agent's ability to navigate a large warehouse, reason about business logic and handle edge cases. This is precisely the kind of work that has historically been difficult to measure.

To measure this capability, we're open sourcing data-eng-bench, a benchmark for repository-level data engineering created in joint work with [Bespoke Labs](https://bespokelabs.ai/). Tasks in data-eng-bench hand an agent a live dbt project connected to an enterprise-scale data warehouse and ask it to build and fix real data pipelines. Resulting dbt models are then evaluated against the business rules and edge cases a working pipeline must satisfy. Relative to [ADE-Bench](https://github.com/dbt-labs/ade-bench), one of few other open benchmarks in this domain, data-eng-bench offers higher scale (103 tasks versus 63 tasks), robust tests that check invariants of the output data pipeline, and more complex task specifications.

Our testing on data-eng-bench reveals a clear divide between generic agent harnesses, including Claude Code and OpenAI Codex, and the data-native agent harness [Snowflake CoCo](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code). Specifically, CoCo leverages its understanding of the data platform to consistently offer higher quality (that is, task completion rate) while incurring significantly lower cost. In more detail:

- **The harness matters for quality; the effect varies by model:** Holding the harness fixed at CoCo, Pass@1 varies drastically across models: from 73.8% with Opus 5 to 64.1% with GPT 5.6 Sol to 56.6% with Sonnet 5, a 17-point spread. _The impact of the harness on quality depends on the model:_ Opus 5 performs the best with CoCo, dropping by ~4pp in Pass@1 with Claude Code; Sonnet 5 performs equally well with both CoCo and Claude Code; GPT 5.6 Sol performs the best with CoCo, dropping by 3.6pp with Codex.
- **The harness matters significantly for cost efficiency:** CoCo achieves higher quality at lower cost than other harnesses: With Opus 5, CoCo reports a 4pp higher Pass@1 at 3.9x lower cost than Claude Code. With Sonnet 5, CoCo reports the same Pass@1 at 2.3x lower cost than Claude Code. With GPT 5.6 Sol, CoCo reports a 3.6pp higher Pass@1 than Codex with Codex incurring 1.5x the cost of CoCo. CoCo completes tasks with 1.5x fewer tool operations and 2.2x fewer agent steps than Claude Code. Task solving patterns show that CoCo adopts a more efficient exploration and validation strategy, requiring 1.7x fewer SQL queries and 1.2x fewer file reads during these phases. CoCo also stays on scope in 2.2x more instances, skipping unnecessary DuckDB cross-validation that Claude Code performs by default.

While these results indicate that frontier agents have made big strides in tackling data engineering tasks, there is still headroom for further improvement. The strongest configuration we benchmarked, Snowflake CoCo with Opus 5, successfully solves 73.8% of tasks on the first attempt (average Pass@1 across 3 trials), but only 64.1% of tasks pass on all three runs (Pass^3). Sonnet 5 reports Pass^3 at 40.8% and GPT 5.6 Sol reports Pass^3 at <56% across harnesses.

![Figure 1. Quality (calculated as the mean Pass@1 rate across 3 independent trials for each task) versus cost per trial by harness and model on data-eng-bench; up-and-left is better.](https://www.snowflake.com/adobe/dynamicmedia/deliver/dm-aid--e1443c2c-1528-442a-830a-42f145760cdd/figure-1.-introducing-data-eng-bench--why-you-need-data-native-harnesses-for-data-engineering.png?preferwebp=true&quality=85)

Figure 1. Quality (calculated as the mean Pass@1 rate across 3 independent trials for each task) versus cost per trial by harness and model on data-eng-bench; up-and-left is better.

In the rest of this blog, we provide an overview of the data-eng-bench benchmark, report how frontier agents perform on it in terms of quality, token and cost efficiency, and what it means for teams adopting coding agents for data engineering tasks.

[_Get the benchmark_](https://github.com/Snowflake-Labs/data-eng-bench).

## The data-eng-bench benchmark

We designed data-eng-bench to mirror how enterprise data engineering teams actually operate: many source systems, layered staging-to-mart development and a shared project that must be maintained by many users. Here is a breakdown:

**One shared data warehouse:** Every task runs against a single, persistent retail data warehouse — 579 source tables across 19 schemas, roughly 8,000 columns in total — spanning orders, finance, procurement, marketing, inventory and more. That's broader than prior data engineering benchmarks, and each task requires navigating the same schema with different requirements.

**103 tasks of two variants:** Each task gives the agent an instruction in natural language, a starting dbt project, and the data warehouse, then asks it to produce or correct models that materialize the right tables. The two variants are as follows:

- **Build (84 tasks):** Author new models and keep the existing pipeline running. Build tasks can be further divided into (a) **Greenfield: Scaffold a brand new dbt project** from an empty state; and (b) **Brownfield: Add new models into an existing multi-layer project** while reusing and preserving dozens of production models.
- **Fix (19 tasks):** Diagnose and repair a subtly broken production model.

**Real dbt mechanics, not free-form SQL:** Agents work through dbt primitives: source declarations (45 tasks), reusable macros (13 tasks) and per-model materializations across staging, intermediate and mart layers. And 82% of gold solutions wire models together through explicit `ref` dependencies, averaging roughly nine `ref` calls each, which the agent must resolve into a coherent, compilable DAG. Those DAGs are meaningfully large: a median of four models per solution, and up to 42 for the biggest pipelines.

**Diverse, high-difficulty business rules:** The tasks live in domains where data engineering is proven difficult — finance (ledger reconciliation, revenue recognition, multi-currency settlement), inventory (LIFO/FIFO costing, turnover, stockout risk), marketing (multi-touch attribution, campaign ROI) and customer analytics (RFM segmentation, churn, lifetime value). The business rules depend on the order and timing of events, accumulated or allocated values across many interdependent tables, and edge cases that should be handled exactly as defined.

**Graded by what the pipeline does, not what it looks like:** Each task ships with a hidden verifier suite of 10–50 assertions that materializes the agent's models and interrogates the resulting tables directly. Those assertions encode the invariants a correct solution must satisfy (for example, output grain and column contracts, formula-level correctness, edge-case handling, idempotency across re-runs) and for the hardest tasks, independently recompute the expected result in Python.

**Scoring is two-fold:** At the test level, assertions provide partial credit (the fraction that pass). At the task level, a task counts as resolved _only if every assertion passes_ — so a pipeline that's directionally right but wrong at the edges earns no task-level credit. This lets us separate "can generate a plausible model" from "got the whole pipeline correct" and pinpoint exactly where solutions fail.

## Measuring agent quality and cost

We evaluate a combination of harnesses and models on data-eng-bench, isolating how much of an agent's performance comes from the scaffold versus the underlyi
 succeeded in 1717ms:
Scrape ID: 019fe9cd-4967-73d6-a90e-d113b206f129
Warning: Could not save scrape session. Use --scrape-id 019fe9cd-4967-73d6-a90e-d113b206f129 with interact.
# [Simon Willison’s Weblog](https://simonwillison.net/)

[Subscribe](https://simonwillison.net/about/#subscribe)

**Sponsored by:** Dynatrace — When agents enter the SDLC, observability becomes the enabler to move from code generation to scalable engineering. [Read the blog for a framework to get started](https://fandf.co/4fwyS92)

## New release of LLM adds support for reasoning traces, OpenAI Responses, server-side tools, and smarter logging

4th August 2026

I released [LLM 0.32](https://llm.datasette.io/en/stable/changelog.html#v0-32) this morning, the most significant new version of LLM since the initial launch of the project. The new version includes support for visible reasoning traces, server-side provider tools, redesigned content-addressable SQLite logs, new models, and new features enabled by the OpenAI Responses API. I also released a new version of the [llm-anthropic plugin](https://github.com/simonw/llm-anthropic) with substantial updates of its own.

#### Headline features for LLM CLI users [\#](https://simonwillison.net/2026/Aug/4/new-release-of-llm/\#headline-features-for-llm-cli-users)

Running LLM against reasoning models now **displays their reasoning traces** to standard error, so you can see what they are “thinking” without that information being included in the standard output that you might pipe to another tool. Add `-R/--hide-reasoning` to turn this off.

![Running llm "think about the best thing about pelicans" in the macOS terminal window - grey text outputs saying Exploring pelican qualities, then after a paragraph of that a white paragraph of text comes out saying: The best thing about pelicans is their wonderfully oversized, practical design: that enormous bill and pouch look comical, but they make pelicans remarkably skilled fishers. Even better, many species cooperate—working together to herd fish before scooping them up. They’re a great mix of goofy, graceful, and surprisingly clever.](https://static.simonwillison.net/static/2026/best-pelicans.gif)

LLM includes support out-of-the-box for the **GPT-5.6 model family**, and the new default model used with `llm "prompt"` is now the inexpensive but capable **GPT-5.6 Luna**.

LLM calls can now use **server-side tools** from various providers. OpenAI provide [a code execution environment](https://llm.datasette.io/en/stable/openai-models.html#code-interpreter) as a server-side tool; LLM can now run prompts that benefit from that like so:

```
llm --tool CodeInterpreter 'Show current python and SQLite versions'
```

OpenAI also gets a [WebSearch](https://llm.datasette.io/en/stable/openai-models.html#web-search) tool.

The [llm-anthropic](https://github.com/simonw/llm-anthropic) plugin adds [WebSearch](https://github.com/simonw/llm-anthropic/blob/0.26/README.md#web-search), [WebFetch](https://github.com/simonw/llm-anthropic/blob/0.26/README.md#web-fetch), [CodeExecution](https://github.com/simonw/llm-anthropic/blob/0.26/README.md#code-execution), and [AnthropicMCP](https://github.com/simonw/llm-anthropic/blob/0.26/README.md#mcp-connector), which looks like this:

```
llm -m claude-sonnet-5 -T 'AnthropicMCP("https://datasette.simonwillison.net/-/mcp")' \
  'how many rows in the blog_blogmark table?'
```

That causes Anthropic to execute MCP calls against my new [datasette-mcp](https://simonwillison.net/2026/Jul/31/stateless-mcp/#datasette-mcp) plugin as part of a single request/response interaction with their API.

The new **llm openai endpoint** command provides a tool for [executing prompts against _any_ OpenAI compatible endpoint](https://llm.datasette.io/en/stable/other-models.html#run-against-an-endpoint-without-configuring-it) as a one-liner. These aren’t logged, which makes this a handy tool for running one-off prompts against anything that speaks the lingua franca of the LLM API world.

Here’s how I use that to run prompts against Gemma 4 12B running in my localhost [LM Studio](https://lmstudio.ai/) API, via `uvx` (no LLM installation required) and mixing in the [llm-tools-quickjs](https://github.com/simonw/llm-tools-quickjs) tool plugin for good measure:

```
uvx --with llm-tools-quickjs \
  llm openai endpoint http://localhost:1234/v1 -m google/gemma-4-12b \
  -T QuickJS 'Use QuickJS to multiply 3434 * 2434' --td
```

![Output reads Tool call: QuickJS_execute_javascript({'javascript': '3434 * 2434'})  8358356 The result of 3434 * 2434 is 8,358,356.](https://static.simonwillison.net/static/2026/openai-endpoint-gemma.webp)

#### New features in the Python API [\#](https://simonwillison.net/2026/Aug/4/new-release-of-llm/\#new-features-in-the-python-api)

LLM’s Python API previously required you to create a conversation and then send messages to it one at a time. This was an abstraction over the true nature of LLMs, where each request carries a complete history of the messages that came before it. That abstraction started to get in the way for some more advanced cases, so the new release introduces a `model.prompt(messages=[])` parameter that can be used like this:

```
import llm
from llm import user, assistant, system

model = llm.get_model("gpt-5.6-luna")

response = model.prompt(messages=[\
    system("You are a helpful pirate."),\
    user("What is the capital of France?"),\
    assistant("Paris, matey."),\
    user("And Germany?"),\
])
print(response.text())
```

LLM previously returned an iterable sequence of strings from each prompt. This worked great when models returned a string response, but failed to predict the weird shape that models would evolve towards. Today many models return a mix of reasoning text, output strings, tool calls, and even image attachments. With LLM 0.32 you can [do this instead](https://llm.datasette.io/en/stable/python-api.html#structured-messages-and-streaming-events):

```
for event in model.prompt("Explain cats").stream_events():
    if event.type == "reasoning":
        print(f"[thinking] {event.chunk}", end="", flush=True)
    elif event.type == "text":
        print(event.chunk, end="", flush=True)
    else:
        print(f"Other event: {event}")
```

Combine these features and we can _finally_ provide a robust implementation of the semi-standard OpenAI chat completions API, which I’ve now released as the [llm-chat-completions-server](https://github.com/simonw/llm-chat-completions-server) plugin:

```
llm install llm-chat-completions-server
llm chat-completions-server --port 9000
# Server is now running on http://127.0.0.1:9000/v1
```

Now you can run prompts against LLM via that server, using the new `llm openai endpoint` command!

```
llm openai endpoint http://127.0.0.1:9000/v1 'hello' -m gpt-5.4-mini
```

The bigger challenge with that kind of API concerns logging. If we’re going to support the pattern where the message sequence is appended to on every request, ideally we can avoid logging all of that duplicate JSON for every turn.

The solution is the new [content-addressable message store](https://llm.datasette.io/en/stable/logging.html#the-message-store), modeled after Git. You can see the new schema for that [in the documentation](https://llm.datasette.io/en/stable/logging.html#sql-schema), but the `llm logs` and `llm logs --json` commands have both been upgraded to convert that format back into something that’s easy to consume.

#### And the rest [\#](https://simonwillison.net/2026/Aug/4/new-release-of-llm/\#and-the-rest)

There is a whole lot more in this release. The [0.32 release notes](https://llm.datasette.io/en/stable/changelog.html#v0-32) are pretty comprehensive, and the notes for [0.32rc2](https://llm.datasette.io/en/stable/changelog.html#rc2-2026-07-30), [0.32rc](https://llm.datasette.io/en/stable/changelog.html#rc1-2026-07-30), [0.32a3](https://llm.datasette.io/en/stable/changelog.html#a3-2026-06-09), [0.32a2](https://llm.datasette.io/en/stable/changelog.html#a2-2026-05-12), and [0.32a0](https://llm.datasette.io/en/stable/changelog.html#a0-2026-04-28) should fill in any gaps.

Existing LLM plugins should all continue to work, but plugins that provide extra models will need to be upgraded to 0.32 in order to participate fully in the new streaming events system. There’s a guide to implementing plugins with [Structured messages and streaming events](https://llm.datasette.io/en/stable/plugins/advanced-model-plugins.html#structured-messages-and-streaming-events) in the documentation.

I’ve updated some of my own plugins:

- [llm-anthropic 0.26](https://github.com/simonw/llm-anthropic/releases/tag/0.26) adds support for the Claude 5 family of models, plus `WebSearch`, `WebFetch`, `CodeExecution`, and `AnthropicMCP` server-side tools.
- [llm-gemini](https://github.com/simonw/llm-gemini) and [llm-openrouter](https://github.com/simonw/llm-openrouter) and [llm-mistral](https://github.com/simonw/llm-mistral) are nearl
codex
两条强候选已核实（Snowflake data-eng-bench、Simon Willison LLM 0.32）。再补几轮跨平台与 arXiv 搜索，确保覆盖面。
exec
/bin/bash -lc 'firecrawl search "Kotlin LLM JetBrains smart macros open source" --limit 6 --tbs qdr:m --json 2>/dev/null | head -c 3500' in /root/note-worker
exec
/bin/bash -lc 'firecrawl search "Flutter 3.44.9 release notes stable" --limit 6 --tbs qdr:m --json 2>/dev/null | head -c 3500' in /root/note-worker
 succeeded in 4660ms:
{"success":true,"data":{"web":[{"url":"https://flutterreleases.com/release/3.44.9","title":"Flutter 3.44.9 — Dart 3.12.2 | FlutterReleases","description":"Flutter 3.44.9 Stable release. OS, Linux, and Windows. Hotfix release with stability improvements for the 3.44 series. Release Notes View release notes →","position":1},{"url":"https://developers.google.com/maps/documentation/javascript/releases","title":"Maps JavaScript API Release Notes - Google for Developers","description":"Updates focus on improved developer experience, user accessibility, and platform stability through bug fixes and feature enhancements. 3.17 is now stable.","position":2},{"url":"https://gist.github.com/brayan19coo-max/f27876e35bb9c9c91c37e03e1e1d208e","title":"flutter_doctor.txt - GitHub Gist","description":"instantly share code, notes, and snippets. Flutter (Channel stable, 3.44.9, on Microsoft Windows. Flutter version 3.44.9 on channel stable. DK bundled with the ...","position":3,"category":"github"},{"url":"https://gist.github.com/brayan19coo-max","title":"brayan19coo-max - GitHub Gist","description":"Instantly share code, notes, and snippets. Flutter (Channel stable, 3.44.9, on Microsoft Windows. Flutter version 3.44.9 on channel stable","position":4,"category":"github"},{"url":"https://fossies.org/linux/misc/","title":"linux/misc - The Fossies Software Archive","description":"Flutter is Google's SDK for crafting beautiful apps for mobile, web, and desktop from a single codebase. Stable release (maintained). Latest stable release. ...","position":5},{"url":"https://www.instagram.com/fluttervividvibes/reel/DboJTttp7iT/","title":"Full Guide to setState....no more confusions . . . . Follow ... - Instagram","description":"Flutter 3.44.8 is out — a stable hotfix. Two fixes worth knowing about: • Builds on macOS/iOS using the Xcode 27 toolchain were failing with a lipo ...","position":6}]},"id":"019fe9cd-64a1-709e-8bf8-8ba3c7a6205d","creditsUsed":2}

 succeeded in 4947ms:
{"success":true,"data":{"web":[{"url":"https://blog.jetbrains.com/research/2026/07/kotlinllm-open-source/","title":"KotlinLLM is Going Open Source","description":"# KotlinLLM is Going Open Source\n## What is KotlinLLM?Copy heading link\nIt adds a language feature we call **Smart macros**. A Smart macro is a regular Kotlin function call whose body is generated Kotlin code. The public API has the following two Smart macros:\n\n## We’re making it public Copy heading link\n- The IntelliJ plugin prototype and the stable Smart macro API.","position":1},{"url":"https://www.marktechpost.com/2026/07/31/jetbrains-research-open-sources-kotlinllm-intellij-plugin-kotlin-runtime-llm/","title":"JetBrains Open-Sources KotlinLLM: Smart Macros That ...","description":"[Home](https://www.marktechpost.com/)[Editors Pick](https://www.marktechpost.com/category/editors-pick/)[Agentic AI](https://www.marktechpost.com/category/editors-pick/agentic-ai/)JetBrains Open-Sources KotlinLLM: Smart Macros That Generate Kotlin Source Code at Runtime...\n\nJetBrains Research Open-Sources **[KotlinLLM.](https://github.com/JetBrains-Research/kotlinllm-plugin)** [KotlinLLM is an IntelliJ IDEA plugin for Kotlin/JVM projects](https://blog.jetbrains.com/research/2026/07/kotlinllm-open-source/) that adds a language feature called **Smart macros**.\n\n## **Explainer: how a Smart macro evolves**\n### KotlinLLM Smart Macros: generate once, run as plain Kotlin\n```\n// asLlm converts an input of type F into a typed value T\n// (data class, enum, list, or primitive).\nimport com.jetbrains.kotlinllm.asLlm\n\nval issuesApiUrl: String = asLlm(repoInput,\n    hint = \"GitHub API URL: get all issues, including closed\")\n\nval issues: List<Issue> = asLlm(response,\n    hint = \"Return all beginner-friendly issues for this repository\")\n```\n\nSources: JetBrains Research blog, July 28, 2026; kotlinllm-plugin README.\n\n## **Key Takeaways**\n- Smart macros generate Kotlin source that is committed, reviewed, and run without the plugin.","position":2},{"url":"https://www.i-programmer.info/news/98-languages/19049-jetbrains-has-announced-that-kotlinllm-its-research-prototype-for-delegating-runtime-logic-to-a-large-language-model-llm-from-kotlin-code-will-now-be-available-as-open-source-and-will-be-public-kotlin-is-the-open-source-language-originated-by-jetbr.html","title":"JetBrains Makes Kotlin LLM Open Source","description":"|  |\n|-|\n| JetBrains Makes Kotlin LLM Open Source |\n\n|  |\n|-|\n| JetBrains has announced that KotlinLLM, its research prototype for delegating runtime logic to a large language model (LLM) from Kotlin code, will now be available as open source and will be public. |\n\nKotlin is the open source language originated by JetBrains and promoted by Google as a first class language for Android to replace or supplement Java. It adds a language feature JetBrains calls smart macros, which can be used for code generation, runtime updates, and hot-reloading.\n\nThe repository contains the KotlinLLM IntelliJ IDEA plugin, the smart macro API, and example projects.","position":3},{"url":"https://www.instagram.com/p/DbdHfigkRTm/","title":"𝗝𝗲𝘁𝗕𝗿𝗮𝗶𝗻𝘀 𝗢𝗽𝗲𝗻-𝗦𝗼𝘂𝗿𝗰𝗲𝘀 𝗞𝗼𝘁𝗹𝗶𝗻𝗟𝗟𝗠: ...","description":"JetBrains Research has open-sourced KotlinLLM under the Apache License 2.0. The IntelliJ IDEA plugin prototype adds Smart macros, asLlm and mockLlm, whose ...","position":4},{"url":"https://www.infoworld.c
exec
/bin/bash -lc 'firecrawl scrape https://blog.jetbrains.com/research/2026/07/kotlinllm-open-source/ --format markdown --only-main-content 2>&1 | head -c 7000' in /root/note-worker
exec
/bin/bash -lc 'firecrawl search "arXiv cs.AI multi-agent LLM evaluation benchmark August 2026" --limit 8 --tbs qdr:m --categories research --json 2>/dev/null | head -c 4000' in /root/note-worker
 succeeded in 2949ms:
Scrape ID: 019fe9cd-81e2-76d8-b5a3-b7698e1672d8
Warning: Could not save scrape session. Use --scrape-id 019fe9cd-81e2-76d8-b5a3-b7698e1672d8 with interact.
[**JetBrains Research**](https://blog.jetbrains.com/research/)

Research is crucial for progress and innovation, which is why at JetBrains we are passionate about both scientific and market research

[About JetBrains Research](https://www.jetbrains.com/research/)

[Kotlin](https://blog.jetbrains.com/research/category/kotlin/) [Research](https://blog.jetbrains.com/research/category/research/)

# KotlinLLM is Going Open Source

![Anastasia Birillo](https://blog.jetbrains.com/wp-content/uploads/2026/03/1_1.png)![Stanislav Sandler](https://secure.gravatar.com/avatar/c875873c4592cc1954447d630998412b?s=200&r=g)

[Anastasia Birillo](https://blog.jetbrains.com/author/anastasia-birillo) [Stanislav Sandler](https://blog.jetbrains.com/author/stanislav-sandler)

July 28, 2026

## TL;DRCopy heading link

**KotlinLLM is now public**. It’s a **research prototype** for delegating runtime logic to an LLM from Kotlin code. Instead of calling an LLM on every request or running a separate agent, you can write an explicit Kotlin call. Its body is **generated Kotlin source code**, and that code is updated as your application hits new runtime scenarios.

👉 [**Check it out**](https://github.com/JetBrains-Research/kotlinllm-plugin)

👉 **KotlinConf 2026 [talk](https://kotlinconf.com/talks/1085233/)**

## What is KotlinLLM?Copy heading link

KotlinLLM is an **IntelliJ IDEA plugin** for Kotlin/JVM projects. It adds a language feature we call **Smart macros**. A Smart macro is a regular Kotlin function call whose body is generated Kotlin code. The public API has the following two Smart macros:

- **`asLlm<F, T>(from, hint)`** converts an input of type F into a typed value T (data class, enum, list, or primitive). Use it to parse unstructured or semi-structured data into typed Kotlin values at runtime.
- **`mockLlm<T>()`** generates a stateful implementation of an interface T. Its behavior depends on which methods are called on it, so it works as a test double that you don’t have to write by hand.

Plain text

Copy to clipboard

Open code in new window

EnlighterJS 3 Syntax Highlighter

// One level of abstraction higher: describe intent, let KotlinLLM fill in the logic.

val issuesApiUrl: String = asLlm(repoInput, hint = "GitHub API URL: get all issues, including closed")

val issues: List<Issue> = asLlm(response, hint = "Return all beginner-friendly issues for this repository")

// One level of abstraction higher: describe intent, let KotlinLLM fill in the logic.
val issuesApiUrl: String = asLlm(repoInput, hint = "GitHub API URL: get all issues, including closed")
val issues: List<Issue> = asLlm(response, hint = "Return all beginner-friendly issues for this repository")

```
// One level of abstraction higher: describe intent, let KotlinLLM fill in the logic.
val issuesApiUrl: String = asLlm(repoInput, hint = "GitHub API URL: get all issues, including closed")
val issues: List<Issue> = asLlm(response, hint = "Return all beginner-friendly issues for this repository")
```

The behavior comes from actual runtime usage rather than being fully specified before the program runs. The call site stays compact and explicit: a clear, keyword-like API over generated code.

## The problem it solvesCopy heading link

In software engineering, LLMs are used during **development**, for code completion, code generation, and program comprehension. Using an LLM at the **runtime** of a compiled application is less common, and the existing options have clear trade-offs:

- **Direct runtime delegation** (calling the model on every invocation) is slow, non-deterministic, and costly. It also makes the application depend on an LLM service at runtime.
- **External agent workflows** keep the generated logic outside the codebase, where it’s harder to review, test, and ship.
- Most prior work (e.g. [byLLM](https://arxiv.org/abs/2405.08965), [nightjar](https://openreview.net/forum?id=E7ZZRnBQU7), [Healer](https://arxiv.org/abs/2408.01055)) targets **interpreted languages** like Python, not a compiled, statically typed language like Kotlin.

KotlinLLM is built around three properties:

- **Explicit** – the call site shows that a feature is LLM-backed, so it’s visible in code review.
- **Persistent** – generated behavior is saved as an ordinary Kotlin source, not kept only in the runtime session. It can be committed, reviewed, tested, and distributed like any other code.
- **Portable** – once generated, the code runs as plain Kotlin without the plugin. For scenarios that are already covered, there’s no further LLM call, so no added latency or cost, and the result is reproducible.

## Does it actually work?Copy heading link

We tested the approach on two Kotlin/JVM projects:

- **An adapted Spring Petclinic Kotlin** – 18 `asLlm` call sites, **24/24** application scenarios completed after Smart macro evolution, with a **100% hot-reload success rate** and compilation/redefinition adding ~1% of total runtime overhead.
- **A synthetic “GitHub Beginner Issue Radar”** – parsing real GitHub issue data across 20 repositories (30k+ issues), reaching **~0.89 recall** on ground-truth beginner labels.

These results show that persistent runtime evolution for compiled Kotlin is feasible. The evaluation also documents the current limits.

## We’re making it public Copy heading link

KotlinLLM is **open source** under the **Apache License 2.0**. The repository contains:

- The IntelliJ plugin prototype and the stable Smart macro API.
- Runnable **example projects** (GitHub Issue Radar, an adapted Petclinic), including _committed generated sources,_ so you can inspect what the LLM produced and run it as ordinary Kotlin.
- The **KotlinConf2026 talk [recording](https://www.youtube.com/watch?v=tmPZajBUsKg)** and the **theoretical [write-up](https://github.com/JetBrains-Research/kotlinllm-plugin/blob/main/thesis.pdf)** with the full design rationale and evaluation.

## Try it and tell us what you think Copy heading link

KotlinLLM is a **research prototype**, so feedback is useful at this stage. A few ways to help:

- **Start and [explore the repo](https://github.com/JetBrains-Research/kotlinllm-plugin)**
- **Try it on your own Kotlin/JVM project**. Add the `KotlinLLM.kt` API file, launch with the _Run with KotlinLLM_ executor, and let the Smart macros evolve. Setup steps are in the README.
- **Open issues** for anything you run into: rough edges, unexpected LLM behavior, missing cases, or behavior you’d expect to be different.
- **Send PRs with use cases.** Real scenarios where `asLlm/mockLlm` work well – or break – are the most useful. New examples, target types, and agent tools are all welcome.

If you find a place where runtime logic delegation fits your code, open an issue. If you build something with it, send a PR.

[KotlinLLM](https://blog.jetbrains
 succeeded in 3952ms:
{"success":true,"data":{"web":[{"url":"https://arxiv.org/html/2608.01645v1","title":"A Practitioner-Sourced Benchmark for Evaluating LLM Agents on ...","description":"arXiv:2608.01645v1 [cs.AI] 03 Aug 2026. GISAgentBench: A Practitioner-Sourced Benchmark for Evaluating LLM Agents on GIS Tasks. Abhinav Pothuri 1, Zhe Jiang 1 ...","position":1,"category":"research"},{"url":"https://arxiv.org/html/2607.26212v1","title":"Multi-Agent Debate Strategies: Survey, Taxonomy, and Challenges","description":"# Multi-Agent Debate Strategies: Survey, Taxonomy, and Challenges\n## References\n- S. Guan, J. Wang, J. Bian, et al. (2026)Evaluating LLM-based agents for multi-turn conversations: a survey.\nACM Transactions on Intelligent Systems and Technology17 (4).\nCited by: [§1](https://arxiv.org/html/2607.26212v1#S1.p4.1).","position":2,"category":"research"},{"url":"https://arxiv.org/html/2607.19336v1","title":"Agents in the Wild: Where Research Meets Deployment - arXiv","description":"This tutorial brings together researchers and practitioners to explore advances in reasoning and planning, multi-agent coordination, and evaluation,","position":3,"category":"research"},{"url":"https://arxiv.org/list/cs.AI/current?ref=digioneer.pro","title":"Artificial Intelligence Aug 2026 - arXiv","description":"Authors and titles for August 2026 Total of 1119 entries. Enhancing LLMs with Context-Specific Knowledge. Self-Evolving LLM Agents Perform Under Streaming ...","position":4,"category":"research"},{"url":"https://arxiv.org/html/2608.01149v1","title":"PATH-Bench: Path-Dependent Evaluation of Lifelong Agents - arXiv","description":"In this work, we establish PATH-Bench, a benchmark for path-dependent evaluation of lifelong agents. PATH-Bench estimates directed task relationships via multi- ...","position":5,"category":"research"},{"url":"https://arxiv.org/html/2608.02827v1","title":"Emergence of Biased Consensus in Multi-Agent LLM Debates - arXiv","description":"Multi-agent LLM debates achieve strong performance on decision-making tasks as well as problem-solving benchmarks, yet their safety and fairness risks remain ...","position":6,"category":"research"},{"url":"https://arxiv.org/list/cs/2026-07?skip=9600","title":"Computer Science Jul 2026 - arXiv","description":"# Computer Science\n## Authors and titles for July 2026\nSubjects:Artificial Intelligence (cs.AI); Multiagent Systems (cs.MA)","position":7,"category":"research"},{"url":"https://arxiv.org/pdf/2608.01425","title":"[PDF] Training Small LLMs as Spatial Multi-Agent Policies - arXiv","description":"Training LLM-based multi-agent systems with multi-agent reinforcement learning is rapidly gaining traction, competent play across three games and four small ...","position":8,"category":"research"}]},"id":"019fe9cd-820b-76ed-bdc2-3be3aa5fdda4","creditsUsed":2}

exec
/bin/bash -lc 'firecrawl search "Compose Multiplatform news August 2026 iOS" --limit 8 --tbs qdr:m --json 2>/dev/null | head -c 4000' in /root/note-worker
exec
/bin/bash -lc 'firecrawl search "Flutter roadmap 2026 Dart AI interface Google developers" --limit 8 --tbs qdr:m --json 2>/dev/null | head -c 4000' in /root/note-worker
 succeeded in 3844ms:
{"success":true,"data":{"web":[{"url":"https://blog.jetbrains.com/kotlin/category/multiplatform/","title":"Multiplatform - Kotlin - The JetBrains Blog","description":"Compose Multiplatform 1.11.0 has been released with improvements to the iOS and web experience and a refreshed approach to UI testing.","position":1},{"url":"https://www.coderio.com/blog/software-development/swift-vs-kotlin-native-app-development/","title":"Swift vs Kotlin for Native App Development: Complete 2026 ...","description":"the Compose Multiplatform framework for shared UI on non-iOS platforms, for more idiomatic Swift interop from iOS code.","position":2},{"url":"https://www.facebook.com/JetBrains/posts/-build-with-kotlin-ship-it-everywherejoin-shipaton-2026-and-compete-for-the-ship/1075329254821974/","title":"🚀 Build with Kotlin. Ship it everywhere. Join Shipaton 2026 ...","description":"✓ Supports cross-platform development — build apps for Android, iOS, desktop, and web from one codebase using Kotlin Multiplatform. ✓ Built for speed ...","position":3},{"url":"https://andbible.org/2026/08/01/the-road-ahead-q3-q4-2026/","title":"The Road Ahead – Q3/Q4 2026","description":"... iOS with Kotlin Multiplatform and Compose Multiplatform — the iOS app is built from that same code. Looking back, I take that time as God's leading: without ...","position":4},{"url":"https://www.threads.com/@githubprojects/post/DbIxpu2mzhE/people-in-space-is-a-kotlin-multiplatform-project-that-shares-a-single-codebase/","title":"PeopleInSpace is a Kotlin Multiplatform project that shares ...","description":"PeopleInSpace is a Kotlin Multiplatform project that shares a single codebase across Android, iOS, Wear OS, Desktop, Web, and an MCP server. - SwiftUI, Jetpack ...","position":5},{"url":"https://androidweekly.net/","title":"Android Weekly - Free weekly Android & Kotlin development ...","description":"A Kotlin Multiplatform sample sharing one codebase across Android, iOS, desktop, and web using Compose Multiplatform. ... Issue #738 August 2, 2026; Issue ...","position":6},{"url":"https://blog.jetbrains.com/kotlin/2026/07/know-kotlin-ship-it-everywhere-and-win-at-shipaton-2026/","title":"Know Kotlin? Ship It Everywhere and Win at Shipaton 2026","description":"Multiplatform News. Know Kotlin? Ship It Everywhere and Win at Shipaton 2026 ... iOS, desktop, and web, with Kotlin Multiplatform and Compose Multiplatform.","position":7}]},"id":"019fe9cd-ba2e-71bb-a4b2-6b817786cc25","creditsUsed":2}

 succeeded in 5592ms:
{"success":true,"data":{"web":[{"url":"https://www.linkedin.com/posts/erdipakrana_flutter-flutterdev-dart-activity-7490957131907641345-jMuX","title":"Flutter Becomes AI-Powered Development Platform with ...","description":"Google is expanding Dart support across Firebase, allowing developers to use a single language for both frontend and backend development.","position":1},{"url":"https://www.instagram.com/reel/Dbik6VYNeIo/","title":"\" Flutter Developer Roadmap — Follow me for more futuristic ...","description":"✓ Flutter is a UI framework used to build beautiful cross-platform applications. Flutter SDK is the complete development kit that includes: Flutter ...","position":2},{"url":"https://medium.com/@flutter-app/flutter-4-0-doesnt-exist-yet-here-s-what-google-actually-shipped-instead-87fa23538abf","title":"Flutter 4.0 Doesn't Exist Yet — Here's What Google Actually ...","description":"# Flutter 4.0 Doesn’t Exist Yet — Here’s What Google Actually Shipped Instead\n### The rumor mill is loud. The changelog isn’t.\nWhile Google’s public roadmap for 2026 says that they promise **four stable releases** it doesn’t say what a version-4 looks like. 0 branding change.\n\n## Why does the rumor of “4.0” continue to circulate?\nFlutter Developer | Building beautiful, high-performance mobile apps with Dart & Firebase","position":3},{"url":"https://www.instagram.com/p/DbdxnDlkytT/","title":"Flutter is an open-source framework created by Google ...","description":"This roadmap will help you learn Flutter step by step—from Dart fundamentals to publishing production-ready apps.","position":4},{"url":"https://play.google.com/store/apps/details?id=com.technology.creativedesign&hl=en_AU","title":"SkillUpFlutter: Learn Flutter – Apps on Google Play","description":"ROADMAP We cover the full spectrum of mobile development: • Dart Essentials: Logic building, Variables, and OOPs concepts. Updated on 24 July 2026 Education ...","position":5},{"url":"https://ripenapps.com/blog/flutter-4-0-outlook-new-features/","title":"Flutter 4.0 Features & Updates 2026","description":"Discover Flutter 4.0's latest features and UI upgrades. See how it helps businesses build powerful cross-platform apps in 2026.","position":6},{"url":"https://www.facebook.com/groups/learnwithnaemazam/posts/1566096621684002/","title":"How to start a career as an independent Flutter app ...","description":"Want to become a Flutter Developer in 2026? Follow this step-by-step roadmap: 1️⃣ Master Dart Variables, functions, OOP Async, Future, Stream Null safety 2️⃣ Learn ...","position":7},{"url":"https://www.secondtalent.com/hire-developers/flutter/","title":"Hire Senior Flutter Developers | Onboard in Aug, 2026","description":"Google's 2026 developer survey shows 68% growth in Flutter adoption across Asia. UI/UX development. Focus on code organization and best practices","position":8}]},"id":"019fe9cd-bf3c-722e-9552-70fc66f5f2ea","creditsUsed":2}

codex
跨平台侧窗口内多为营销/补丁内容。再做两轮针对性搜索后定稿。
exec
/bin/bash -lc 'firecrawl search "Kotlin Multiplatform Gradle build cache KMP tooling improvement July 2026" --limit 8 --tbs qdr:m --json 2>/dev/null | head -c 4000' in /root/note-worker
exec
/bin/bash -lc 'firecrawl search "Anthropic Claude Code research engineering August 2026" --limit 8 --tbs qdr:m --json 2>/dev/null | head -c 4000' in /root/note-worker
 succeeded in 5075ms:
{"success":true,"data":{"web":[{"url":"https://www.facebook.com/groups/claudecommunity/posts/1082823480924983/","title":"Claude AI updates for August 2026 - Facebook","description":"Claude Opus 5 is out — faster, more cost-efficient for coding, knowledge work and scientific research. ends Aug 31, 2026. Standard pricing ($3/$15) kicks in ...","position":1},{"url":"https://medium.com/the-programmer/claude-decided-2026-was-fake-then-it-hacked-a-real-company-ad4701d05196","title":"Claude Decided 2026 Was Fake. Then It Hacked a Real Company.","description":"AI decided the year 2026 was fake. AI labs test their models by giving them fake security puzzles. August 1, 2026.","position":2},{"url":"https://www.anthropic.com/news/rare-disease-research-grants","title":"Apply for Anthropic's AI for Science rare disease research grants","description":"Accepted applicants will receive up to $50,000 in Claude credits. We will be accepting applications through August 2, 2026 at 11:59 PM PST. Accepted applicants ...","position":3},{"url":"https://www.anthropic.com/news/claude-opus-5","title":"Introducing Claude Opus 5 - Anthropic","description":"Opus 5 is a step change improvement for the Opus tier powering long-running agents while delivering improvements in coding and professional work.","position":4},{"url":"https://www.instagram.com/reel/Dbs_Jl0RGvW/","title":"Coditas on Instagram: \"Claude Code in Action. Real engineering ...","description":"82 likes, 1 comments - coditas_hq on August 6, 2026: \"Claude Code in Action. Real engineering. Real lessons. Join us for an afternoon with engineers and AI ...","position":5},{"url":"https://releasebot.io/updates/anthropic/claude","title":"Claude Updates by Anthropic - August 2026 - Releasebot","description":"# Claude Updates & Release Notes\n## Run Claude Code sessions on your own compute\n### Getting started\n- Aug 6, 2026\n  - Date parsed from source:\nAug 6, 2026","position":6},{"url":"https://x.com/iHarnoorSingh/article/2086191148327178430","title":"Every Anthropic Opportunity for Fresh Grads and Researchers in 2026","description":"Anthropic listed 68 AI Research and Engineering roles when I checked on August 8. They cover alignment, interpretability, reinforcement learning, pretraining,","position":7},{"url":"https://www.morphllm.com/comparisons/opencode-vs-claude-code","title":"OpenCode vs Claude Code (August 2026) - Morph","description":"# OpenCode vs Claude Code: 161K Stars, Agent View, and the Provider War (August 2026)\n## Context Management & Compaction\n### Claude Code Context Strategy\n#### Claude Code Context Management\n```\n// Claude Code uses automatic compaction\n// Triggered near context limit\n\n// Compaction process:\n1. Detect approaching context limit\n2. Summarize previous messages (utility prompt)\n3. Preserve critical context (file contents, etc.)\n4. Continue with reduced token count\n\n// Manual compaction:\n$ /compact     # Slash command to force compaction\n\n// Context advice from Anthropic:\n// \"If using Claude in an agent harness that compacts context,\n// add this to your prompt so Claude can behave accordingly.\n// Otherwise Claude may try to wrap up work as it\n// approaches the context limit.\"\n```\n\n## Frequently Asked Questions\n### Sources\n- [Anthropic: Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)","position":8}]},"id":"019fe9cd-f740-7682-ad0d-f44e705d1753","creditsUsed":2}

 succeeded in 5989ms:
{"success":true,"data":{"web":[{"url":"https://kotlinlang.org/docs/whatsnew2320.html","title":"What's new in Kotlin 2.3.20","description":"# What's new in Kotlin 2.3.20﻿\n## Kotlin/Native﻿\n### New DSL for disabling compilation cache﻿\nIf you do need to disable the compilation cache in your project, update the `binaries {}` block in your Gradle build file as follows:","position":1},{"url":"https://kotlinlang.org/docs/releases.html","title":"Kotlin release process | Kotlin Documentation","description":"A tooling release for Kotlin 2.0.0 containing performance improvements and bug fixes. Features also include concurrent marking in Kotlin/Native's garbage ...","position":2},{"url":"https://www.instagram.com/p/Da0VGTnieSh/?img_index=8","title":"Android Developer - Jetpack Compose,Kotlin Multiplatform,Flutter ...","description":"codingambitions on July 15, 2026: \"Gradle is a build tool for kmp and android. So we should know about some commands which are really useful and used in day ...","position":3},{"url":"https://ktor.io/docs/releases.html","title":"Ktor releases | Ktor Documentation","description":"June 26, 2026. A patch release including OpenAPI plugin improvements, expanded authentication KDoc documentation, and a wide range of bug fixes covering Kotlin ...","position":4},{"url":"https://www.linkedin.com/posts/gradle-technologies_how-the-gradle-team-adopted-isolated-projects-activity-7486114181730181121-SL2h","title":"Gradle Isolated Projects Boosts Build Speed - LinkedIn","description":"Isolated Projects is an experimental Gradle feature that parallelizes project configuration. Kotlin Multiplatform, Web, or Backend applications.","position":5},{"url":"https://developer.android.com/jetpack/androidx/releases/compose-ui","title":"Compose UI | Jetpack - Android Developers","description":"- On this page\n\n- On this page\n\n# Compose UI    Stay organized with collections      Save and categorize content based on your preferences.\n## Declaring dependencies\n```\ndependencies {\n    implementation \"androidx.compose.ui:ui:1.11.4\"\n}\n\nandroid {\n    buildFeatures {\n        compose true\n    }\n\n    composeOptions {\n        kotlinCompilerExtensionVersion = \"1.5.15\"\n    }\n\n    kotlinOptions {\n        jvmTarget = \"1.8\"\n    }\n}\n```\n\n```\ndependencies {\n    implementation(\"androidx.compose.ui:ui:1.11.4\")\n}\n\nandroid {\n    buildFeatures {\n        compose = true\n    }\n\n    composeOptions {\n        kotlinCompilerExtensionVersion = \"1.5.15\"\n    }\n\n    kotlinOptions {\n        jvmTarget = \"1.8\"\n    }\n}\n```","position":6},{"url":"https://mvpfactory.io/blog/","title":"Blog - MVP Factory","description":"Walk through how Gradle's build cache actually works at the hash. Gradle configuration cache compatibility in multi-module KMP projects, build cache hit ...","position":7},{"url":"https://www.instagram.com/p/DbttigBoK_v/","title":"R8 makes Kotlin Coroutines on Android 2x faster ⁠ ⁠ With AGP 9.2 ...","description":"This is a great example of how compiler and tooling improvements can make Android apps faster without requiring developers to rewrite their code. Swipe through ...","position":8}]},"id":"019fe9cd-f578-7072-b470-037b17b59dde","creditsUsed":2}

codex
搜索完成，两轮验证均通过。最终选定 2 条（均为 AI Agent 域；跨平台窗口内未发现达标内容，最接近的 JetBrains KotlinLLM 为 Kotlin/JVM 研究、非 KMP 域，未入选）。

## 1. 引入 Data-eng-bench：为什么数据工程需要"数据原生"的 Agent Harness

- 链接：https://www.snowflake.com/en/blog/engineering/data-eng-bench-data-engineering-agent-benchmark/
- 作者/来源：Snowflake AI Research（联合 Bespoke Labs）/ Snowflake Engineering Blog
- 日期：2026-08-06
- 推荐指数：⭐⭐⭐⭐⭐

一句话摘要：开源 103 任务 dbt 数据工程基准，量化证明 harness 选择比模型更能左右 agent 质量与成本。

核心洞察（3条）：

1. Harness 对质量影响依模型而异：同模型跨 harness 的 Pass@1 最多差约 4pp——Opus 5 配 CoCo 最佳（73.8%），配 Claude Code 降 4pp；Sonnet 5 在两 harness 下持平；GPT 5.6 Sol 配 CoCo 比 Codex 高 3.6pp。
2. Harness 对成本影响远大于质量：CoCo 以 3.9x 更低成本实现比 Claude Code 高 4pp 的 Pass@1，且工具调用少 1.5x、agent 步数少 2.2x——数据原生 harness 的"少做"本身就是效率来源。
3. Pass@1 与 Pass^3 落差暴露可靠性缺口：最强配置一次成功率 73.8%，但三试全过仅 64.1%；评测用 10–50 条隐藏断言按"整条管道全对"计分，能区分"能生成像样模型"与"整个管道正确"。

值得收录理由：首个仓库级 dbt agent 评测（103 任务 > ADE-Bench 63），给出 harness×模型 双变量质量/成本矩阵并开源，直接服务 agent 评测与 harness 选型。

## 2. LLM 0.32 发布：推理轨迹、服务端工具与内容寻址日志

- 链接：https://simonwillison.net/2026/Aug/4/new-release-of-llm/
- 作者/来源：Simon Willison
- 日期：2026-08-04
- 推荐指数：⭐⭐⭐⭐

一句话摘要：LLM CLI 里程碑版本：推理轨迹独立输出、OpenAI Responses 服务端工具、Git 式内容寻址 SQLite 日志。

核心洞察（3条）：

1. 推理轨迹默认写 stderr、与 stdout 分离（`-R` 关闭），保证管道仍可安全消费纯模型输出——agent 工具链处理 reasoning 流的标准做法。
2. 日志重构为内容寻址消息存储（仿 Git），多轮对话不再逐轮重复记录完整 JSON 历史，解决"每条请求都带全量历史"带来的日志膨胀。
3. 以 `stream_events()` 统一 reasoning/text/tool-call 事件流，并新增 `llm openai endpoint` 一条命令对接任意 OpenAI 兼容端点，配合 llm-chat-completions-server 可自建兼容服务。

值得收录理由：Tier 1 作者对 LLM 工具平台的深度工程复盘，含可复现代码，覆盖推理轨迹、服务端工具、日志架构等 agent 工具链核心议题。

```json
{
  "candidates": [
    {
      "title": "Introducing Data-eng-bench: Why You Need \"Data-Native\" Harnesses for Data Engineering",
      "url": "https://www.snowflake.com/en/blog/engineering/data-eng-bench-data-engineering-agent-benchmark/",
      "source": "Snowflake AI Research (Snowflake Engineering Blog)",
      "date": "2026-08-06",
      "stars": 5,
      "summary": "开源103任务dbt数据工程基准，量化证明harness选择比模型更能左右agent质量与成本。",
      "insights": [
        "同模型跨harness的Pass@1最多差约4pp，且harness效果依赖模型（Opus5配CoCo最佳、Sonnet5两harness持平）。",
        "CoCo以3.9x更低成本实现比Claude Code高4pp的Pass@1，工具调用少1.5x、agent步数少2.2x。",
        "Pass@1(73.8%)与Pass^3(64.1%)落差暴露可靠性缺口，10-50条隐藏断言按整管道全对计分。"
      ],
      "reason": "首个仓库级dbt agent评测（103任务）并开源，harness×模型双变量质量/成本数据直接服务agent评测与选型。"
    },
    {
      "title": "New release of LLM adds support for reasoning traces, OpenAI Responses, server-side tools, and smarter logging",
      "url": "https://simonwillison.net/2026/Aug/4/new-release-of-llm/",
      "source": "Simon Willison (simonwillison.net)",
      "date": "2026-08-04",
      "stars": 4,
      "summary": "LLM CLI里程碑版本：推理轨迹独立输出、OpenAI Responses服务端工具、Git式内容寻址SQLite日志。",
      "insights": [
        "推理轨迹默认写stderr与stdout分离，保证管道仍可安全消费纯模型输出。",
        "日志改内容寻址消息存储（仿Git），避免多轮对话逐轮重复记录完整JSON历史。",
        "stream_events统一reasoning/text/tool-call事件流，llm openai endpoint一条命令对接任意兼容端点。"
      ],
      "reason": "Tier1作者对LLM工具平台的深度工程复盘，含可复现代码，覆盖推理轨迹、服务端工具与日志架构。"
    }
  ]
}
```
tokens used
41,174


### 请分析：

1. **优先级排序**：哪些内容最值得我们收录？考虑因素：
   - 对**已收录文章 + 已跟踪内容**（完整清单见下方「已知内容」，或 `references/articles.md` / `python scripts/retrack.py --list` 注入段）的补充价值
   - 对 `expand/thinking/` 中已有洞见的验证或挑战
   - 对开放问题清单的回答程度

2. **缺口分析**：这批内容覆盖了我们的哪些知识缺口？还有哪些缺口未被触及？
   当前已知缺口（对齐本知识库两大方向）：
   - Agent harness 行为正确性与覆盖率评估
   - 上下文 / compaction / 记忆策略的可复现实践
   - 多智能体编排反模式与成本
   - Agent 评测：model / harness / 环境的组件级归因
   - 跨模型可移植性与迁移指南
   - 中小团队 Agent 工程落地案例与成本数据
   - Harness / 控制的激活策略（always-on / per-commit / conditional / human-summoned）
   - Agent 安全审计（轨迹违规、多智能体信息流、工具权限边界）
   - KMP / Compose Multiplatform 与 Flutter 的架构选型、共享逻辑边界、工具链痛点
   - 跨平台 CI / 发布 / 性能基线

3. **趋势信号**：这批内容中是否有新的趋势或方向？与既有 Agent 工程 / 跨平台实践是否一致或冲突？

4. **收录建议**：对每条推荐内容给出具体建议（三选一，互斥）：
   - 收录到 references/articles.md（哪个脉络 lineage）→ verdict=`index`
   - 值得翻译到 working/ → verdict=`translate`
   - 暂不收录，持续观察 → verdict=`observe`

### 已知内容

[01] When Does On-Policy Interaction Help? Representational Tradeoffs in Value-Based Imitation Learning | http://arxiv.org/abs/2607.29617v1 | 已收录
[02] AgentHPOBench: A Benchmark For Evaluating LLM Agents as Sequential Hyperparameter Optimizers | http://arxiv.org/abs/2607.29626v1 | 已收录
[03] ExtractBench: A Benchmark for Schema-Guided Enterprise Document Extraction | http://arxiv.org/abs/2607.29677v1 | 已收录
[04] DungeonBench: A Benchmark for Rules-Rich Tactical Reasoning in Dungeons & Dragons Combat | http://arxiv.org/abs/2607.29577v1 | 已收录
[05] MOT-SR: Multi-Objective Tool-Augmented Scientific Equation Discovery with Large Language Models | http://arxiv.org/abs/2607.29561v1 | 已收录
[06] affaan-m/ECC — The agent harness performance optimization system | https://github.com/affaan-m/ECC | 已收录
[07] n8n-io/n8n — Fair-code workflow automation platform with native AI capabilities | https://github.com/n8n-io/n8n | 已收录
[08] microsoft/markitdown — Python tool for converting files to Markdown | https://github.com/microsoft/markitdown | 已收录
[09] NousResearch/hermes-agent — The agent that grows with you | https://github.com/NousResearch/hermes-agent | 已收录
[10] Snailclimb/JavaGuide — Java 面试 & 后端通用面试指南 | https://github.com/Snailclimb/JavaGuide | 已收录
[11] Bonsai: Janestreet's UI Library | https://github.com/janestreet/bonsai | 已收录
[12] Prevent cognitive debt by manually retyping LLM-generated code | https://ankursethi.com/blog/prevent-cognitive-debt-by-manually-retyping-llm-generated-code/ | 已淘汰
[13] Qwen3.8-Max: A New Bar for Coding and Cowork | https://qwen.ai/blog?id=qwen3.8 | 已淘汰
[14] MCP 官方文档：Model Context Protocol 介绍 | https://modelcontextprotocol.io/introduction | 已收录
[15] Rust 2025 官方博客：Rust 1.85 版本说明（Move 语义 / Borrow Checker 演进） | https://blog.rust-lang.org/2025/02/20/Rust-1.85.0.html | 已收录

### 输出要求

先用中文写出上述 1–4 的完整分析（可含表格与列表），再在文末附机器可读 JSON：

```json
{
  "analysis": {
    "priority": ["..."],
    "gaps_covered": ["..."],
    "gaps_open": ["..."],
    "trends": ["..."]
  },
  "candidates": [
    {
      "title": "...",
      "url": "...",
      "verdict": "index|translate|observe",
      "lineage": "agent/harness",
      "reason": "一句话",
      "stars": 4
    }
  ]
}
```

脉络（lineage）建议取值：`agent/rag` · `agent/harness` · `agent/orchestration` · `agent/context` · `agent/multi-agent` · `agent/eval` · `agent/platform` · `crossplatform/kmp` · `crossplatform/flutter` · `crossplatform/toolchain` · `general`（慎用）。

warning: Codex could not find bubblewrap on PATH. Install bubblewrap with your OS package manager. See the sandbox prerequisites: https://developers.openai.com/codex/concepts/sandboxing#prerequisites. Codex will use the bundled bubblewrap in the meantime.
warning: Model metadata for `deepseek-v4-flash` not found. Defaulting to fallback metadata; this can degrade performance and cause issues.
codex
我先查看项目的现有内容（`references/articles.md`、`expand/thinking/`、`scripts/retrack.py`），再基于候选内容做分析。
exec
/bin/bash -lc "ls -la /root/note-worker && echo '---' && find /root/note-worker -maxdepth 2 -type d | head -40" in /root/note-worker
 succeeded in 0ms:
total 104
drwxr-xr-x 19 root root  4096 Aug 10 11:54 .
dr-xr-x--- 14 root root  4096 Aug 10 00:07 ..
dr-xr-xr-x  2 root root    40 Aug 10 11:54 .agents
dr-xr-xr-x  2 root root    40 Aug 10 11:54 .codex
drwxr-xr-x  2 root root  4096 Aug 10 06:18 .firecrawl
drwxr-xr-x  8 root root  4096 Aug 10 11:50 .git
drwxr-xr-x  2 root root  4096 Aug  9 13:37 .githooks
drwxr-xr-x  3 root root  4096 Aug  9 13:37 .github
-rw-r--r--  1 root root   738 Aug  9 17:25 .gitignore
drwxr-xr-x  3 root root  4096 Aug  9 13:37 .obsidian
-rw-r--r--  1 root root  1066 Aug  9 13:37 LICENSE
-rw-r--r--  1 root root  9864 Aug  9 13:37 README.md
-rw-r--r--  1 root root 14623 Aug  9 13:37 agents.md
drwxr-xr-x  2 root root  4096 Aug  9 13:37 assets
drwxr-xr-x  4 root root  4096 Aug 10 11:50 candidates
drwxr-xr-x  3 root root  4096 Aug  9 17:25 docs
drwxr-xr-x  5 root root  4096 Aug 10 11:50 expand
drwxr-xr-x  3 root root  4096 Aug 10 11:38 prompts
drwxr-xr-x  2 root root  4096 Aug 10 11:50 references
drwxr-xr-x  3 root root  4096 Aug 10 11:50 scripts
drwxr-xr-x  2 root root  4096 Aug  9 13:37 templates
drwxr-xr-x 14 root root  4096 Aug  9 13:37 wiki
drwxr-xr-x  2 root root  4096 Aug 10 11:50 working
---
/root/note-worker
/root/note-worker/.firecrawl
/root/note-worker/assets
/root/note-worker/working
/root/note-worker/prompts
/root/note-worker/prompts/feedback
/root/note-worker/templates
/root/note-worker/.githooks
/root/note-worker/expand
/root/note-worker/expand/06-AI与LLM
/root/note-worker/expand/thinking
/root/note-worker/expand/03-后端
/root/note-worker/.git
/root/note-worker/.git/info
/root/note-worker/.git/objects
/root/note-worker/.git/hooks
/root/note-worker/.git/branches
/root/note-worker/.git/refs
/root/note-worker/.git/logs
/root/note-worker/.agents
/root/note-worker/wiki
/root/note-worker/wiki/06-AI与LLM
/root/note-worker/wiki/08-逆向与安全
/root/note-worker/wiki/opencode项目解读
/root/note-worker/wiki/04-数据库
/root/note-worker/wiki/05-数据结构与算法
/root/note-worker/wiki/01-编程语言
/root/note-worker/wiki/03-后端
/root/note-worker/wiki/10-求职面试
/root/note-worker/wiki/09-源码解读
/root/note-worker/wiki/07-Linux与工具链
/root/note-worker/wiki/02-前端
/root/note-worker/wiki/11-生活杂项
/root/note-worker/references
/root/note-worker/.github
/root/note-worker/.github/workflows
/root/note-worker/scripts
/root/note-worker/scripts/__pycache__
/root/note-worker/.obsidian
/root/note-worker/.obsidian/plugins

exec
/bin/bash -lc 'cd /root/note-worker && python scripts/retrack.py --list 2>&1 | head -80' in /root/note-worker
 succeeded in 0ms:
/bin/bash: line 1: python: command not found

exec
/bin/bash -lc 'cd /root/note-worker && ls scripts/ references/ expand/thinking/ working/ candidates/ 2>&1 | head -60' in /root/note-worker
 succeeded in 0ms:
candidates/:
20260809-180901
research-20260810-115057

expand/thinking/:
AGENTS.md
MCP协议标准化的增量与边界.md
Rust2024版次的语义收紧与异步闭合.md

references/:
agents.md
articles.md

scripts/:
__pycache__
bing_search.py
check_consistency.py
codex_task.ps1
collect.py
count_pending.py
curate.py
feedback_capture.py
fetch_full.py
filter.py
finalize.py
firecrawl_cli.py
firecrawl_search.py
gc_report.py
ingest.py
kb_common.py
lint.py
media.py
redact_aliyun_key.py
requirements-semantic.txt
requirements.txt
research.py
retrack.py
scan_secrets.py
semantic_search.py
setup_secrets.py
translator.py
weekly_report.py
worker.py

working/:
AGENTS.md

exec
/bin/bash -lc "cd /root/note-worker && sed -n '1,120p' scripts/retrack.py" in /root/note-worker
 succeeded in 0ms:
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""references 去重查询接口（适配 harness 格式 articles.md）。

把 references/ 变为"持续输入的源头"：采集/追踪前查询 articles.md 去重权威，
判定给定 URL / 标题是否已收录（含已淘汰，防止重复采集）。

用法：
  python scripts/retrack.py --url "https://x.com/y"
  python scripts/retrack.py --title "Harness Engineering"
  python scripts/retrack.py --list            # 列出全部索引条目（供 collect/research 注入）

退出码：0 = 未收录（可收集）；1 = 已收录（含已淘汰）；2 = 索引不可读。
"""
import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ARTICLES = ROOT / "references" / "articles.md"

# articles.md 编号条目结构：
#   ### N. 标题
#   - **标题：** …
#   - **链接：** [x](url)
#   - **作者：** … | **日期：** …
#   - **状态：** 已收录 | **归属：** …
#   - **核心：** …
#   - **关联：** …
ENTRY_RE = re.compile(r"^### (\d+)\s*\.\s*(.+)$", re.M)
TITLE_FIELD_RE = re.compile(r"- \*\*标题：\*\*\s*(.+)$", re.M)
URL_FIELD_RE = re.compile(r"- \*\*链接：\*\*\s*\[[^\]]*\]\(([^)]+)\)", re.M)
STATE_FIELD_RE = re.compile(r"- \*\*状态：\*\*\s*([^|]+)", re.M)


def read_articles():
    if not ARTICLES.exists():
        sys.stderr.write("references/articles.md 不存在\n")
        return None
    try:
        return ARTICLES.read_text(encoding="utf-8")
    except OSError as e:
        sys.stderr.write(f"读取失败：{e}\n")
        return None


def parse_entries(text):
    """解析编号正文条目 -> [(编号, 标题, url, 状态, 归属)]。

    「## 待处理」队列中的占位行不计入；待处理队列用独立标记行表示，不写 ### 编号。
    """
    out = []
    starts = list(ENTRY_RE.finditer(text))
    for i, m in enumerate(starts):
        nxt = starts[i + 1].start() if i + 1 < len(starts) else len(text)
        seg = text[m.end():nxt]
        num = int(m.group(1))
        tm = TITLE_FIELD_RE.search(seg)
        title = tm.group(1).strip() if tm else m.group(2).strip()
        um = URL_FIELD_RE.search(seg)
        url = um.group(1).strip() if um else ""
        sm = STATE_FIELD_RE.search(seg)
        state = sm.group(1).strip() if sm else ""
        om = re.search(r"\*\*归属：\*\*\s*(.+)", seg, re.M)
        belong = om.group(1).strip() if om else ""
        out.append((num, title, url, state, belong))
    return out


def check(url="", title="", threshold=0.6):
    text = read_articles()
    if text is None:
        return 2, "索引不可读"
    entries = parse_entries(text)
    known_urls = {e[2] for e in entries if e[2]}
    known_titles = [e[1] for e in entries]

    if url:
        for u in known_urls:
            if u == url or u.rstrip("/").split("?")[0] == url.rstrip("/").split("?")[0]:
                return 1, f"URL 已收录：{u}"
        core = re.sub(r"^https?://", "", url).split("?")[0].rstrip("/")
        for u in known_urls:
            u_core = re.sub(r"^https?://", "", u).split("?")[0].rstrip("/")
            if u_core and u_core == core:
                return 1, f"URL（归一化）已收录：{u}"

    if title:
        tl = title.lower().strip()
        for t in known_titles:
            if t and tl and (tl in t.lower() or t.lower() in tl):
                return 1, f"标题近似匹配：{t}"
        set_t = set(re.sub(r"\W+", "", tl))
        for t in known_titles:
            st = set(re.sub(r"\W+", "", t.lower()))
            if set_t and st:
                sim = len(set_t & st) / max(len(set_t), len(st))
                if sim >= threshold:
                    return 1, f"标题模糊匹配：{t}"
    return 0, "未收录，可收集"


def list_all(text):
    out = []
    for num, title, url, state, _bl in parse_entries(text):
        out.append(f"[{num:02d}] {title} | {url} | {state}")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="")
    ap.add_argument("--title", default="")
    ap.add_argument("--threshold", type=float, default=0.4,
                    help="标题 jaccard 相似度阈值（默认 0.4）")
    ap.add_argument("--list", action="store_true", help="输出全部已收录条目清单")
    args = ap.parse_args()

    if args.list:

exec
/bin/bash -lc 'cd /root/note-worker && python3 scripts/retrack.py --list 2>&1 | head -120' in /root/note-worker
 succeeded in 0ms:
[01] When Does On-Policy Interaction Help? Representational Tradeoffs in Value-Based Imitation Learning | http://arxiv.org/abs/2607.29617v1 | 已收录
[02] AgentHPOBench: A Benchmark For Evaluating LLM Agents as Sequential Hyperparameter Optimizers | http://arxiv.org/abs/2607.29626v1 | 已收录
[03] ExtractBench: A Benchmark for Schema-Guided Enterprise Document Extraction | http://arxiv.org/abs/2607.29677v1 | 已收录
[04] DungeonBench: A Benchmark for Rules-Rich Tactical Reasoning in Dungeons & Dragons Combat | http://arxiv.org/abs/2607.29577v1 | 已收录
[05] MOT-SR: Multi-Objective Tool-Augmented Scientific Equation Discovery with Large Language Models | http://arxiv.org/abs/2607.29561v1 | 已收录
[06] affaan-m/ECC — The agent harness performance optimization system | https://github.com/affaan-m/ECC | 已收录
[07] n8n-io/n8n — Fair-code workflow automation platform with native AI capabilities | https://github.com/n8n-io/n8n | 已收录
[08] microsoft/markitdown — Python tool for converting files to Markdown | https://github.com/microsoft/markitdown | 已收录
[09] NousResearch/hermes-agent — The agent that grows with you | https://github.com/NousResearch/hermes-agent | 已收录
[10] Snailclimb/JavaGuide — Java 面试 & 后端通用面试指南 | https://github.com/Snailclimb/JavaGuide | 已收录
[11] Bonsai: Janestreet's UI Library | https://github.com/janestreet/bonsai | 已收录
[12] Prevent cognitive debt by manually retyping LLM-generated code | https://ankursethi.com/blog/prevent-cognitive-debt-by-manually-retyping-llm-generated-code/ | 已淘汰
[13] Qwen3.8-Max: A New Bar for Coding and Cowork | https://qwen.ai/blog?id=qwen3.8 | 已淘汰
[14] MCP 官方文档：Model Context Protocol 介绍 | https://modelcontextprotocol.io/introduction | 已收录
[15] Rust 2025 官方博客：Rust 1.85 版本说明（Move 语义 / Borrow Checker 演进） | https://blog.rust-lang.org/2025/02/20/Rust-1.85.0.html | 已收录

exec
/bin/bash -lc "cd /root/note-worker && wc -l references/articles.md && sed -n '1,80p' references/articles.md" in /root/note-worker
 succeeded in 0ms:
188 references/articles.md
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
<!-- 当前：7 条待处理 -->
| The new rules of context engineering for Claude 5 generation models | https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models | research | 2026-08-09 | 🔄评审中 candidates/20260809-180901/
| One-shotting a Raccoon Heist game using Claude Fable 5 | https://simonwillison.net/2026/Aug/5/raccoon-heist/ | research | 2026-08-09 | 🔄评审中 candidates/20260809-180901/
| Six Agent Orchestration Patterns | https://vercel.com/i/agent-orchestration-patterns | research | 2026-08-09 | 🔄评审中 candidates/20260809-180901/
| Making production-ready agents the default: building Duolingo's agent platform | https://blog.duolingo.com/production-ready-ai-agent-platform/ | research | 2026-08-09 | 🔄评审中 candidates/20260809-180901/
| Meta launches Muse Code for complex software work with persistent AI agents | https://www.infoworld.com/article/4206084/meta-launches-muse-code-for-complex-software-work-with-persistent-ai-agents.html | research | 2026-08-09 |
| Harness-R1: Learning to Edit Executable Runtime Harnesses from Agent Failure Trajectories | https://arxiv.org/abs/2608.02276 | research | 2026-08-09 |
| EvolveNet: Collaborative Harness Evolution for Agent Self-Improvement | https://arxiv.org/abs/2608.04968 | research | 2026-08-09 |
| The Shape of Things to Come, Part 1: The Continuous Thunderdome | https://yegge.ai/essays/the-shape-of-things-to-come/ | research | 2026-08-09 |
| Claude Code v2.1.224 — self-hosted environments | https://github.com/anthropics/claude-code/releases/tag/v2.1.224 | research | 2026-08-09 |
| I Gave Claude Code an AGENTS.md Contract and Stopped Babysitting It | https://dev.to/daymondhyper/i-gave-claude-code-an-agentsmd-contract-and-stopped-babysitting-it-53m | research | 2026-08-09 |
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

exec
/bin/bash -lc "cd /root/note-worker && ls candidates/20260809-180901/ candidates/research-20260810-115057/ 2>&1 && echo '--- expand/thinking ---' && head -60 expand/thinking/MCP协议标准化的增量与边界.md" in /root/note-worker
 succeeded in 0ms:
candidates/20260809-180901/:
review.md
sources
translations
works-ready

candidates/research-20260810-115057/:
search.md
--- expand/thinking ---
---
created: 2026-08-09
updated: 2026-08-09
sources: [references/articles.md#14]
tags: [MCP, AI Agent, 协议标准化, type/想法]
---

# MCP 协议标准化的增量与边界

> 论点：官方文档把 MCP 比作「AI 应用的 USB-C」，这个类比在**接口/传输层**成立，在**语义层**不成立——协议标准化把集成成本从「每个模型 × 每个工具的协议适配」转移成了「每个 server 的语义适配与质量治理」，M×N 问题没有消失，只是换了战场。2026-07-28 版本文档的增量（MCP Apps / Agent Skills / Registry / `server/discover`）恰好说明：MCP 正在从「工具调用协议」长成「AI 应用平台层」。

## 一、官方文档说了什么（压缩）

MCP 是连接 AI 应用与外部系统（数据 / 工具 / 工作流）的开放标准，口号是「build once, integrate everywhere」，官方类比是「AI 应用的 USB-C」。

## 二、类比成立到哪一层

### 成立：接口层（传输 + 原语枚举）

- 架构文档把 MCP 拆成两层：**数据层**（JSON-RPC 2.0 消息、`server/discover` 能力发现、tools / resources / prompts 三个原语、通知与进度）与**传输层**（本地 stdio、远程 Streamable HTTP + OAuth）。
- 这两层才是「插头规格」：客户端生态（Claude、ChatGPT、VSCode、Cursor）只需实现一次连接逻辑，就能连上任何符合规范的 server——USB-C 类比真正的成立处是**接口一致 → 即插即用**。

### 不成立：语义层（每个 tool 仍是私有协议）

- USB-C 的语义（供电协商、DP / Thunderbolt 备选模式）由协议完整定义，插上就知道能干什么；MCP 只定义「信封」和三个粗粒度原语，**每个 tool 的输入输出 schema、错误语义、权限边界仍由各家 server 自治**。
- 后果：集成方（或 LLM 本身）依然要为每个 server 读文档、写调用示例、做 prompt 适配，还要防备「工具描述与实现不符」「长尾 server 质量参差」。M×N 从「协议适配」转为「语义适配 + 质量适配」，成本换了个名字，没消失。
- 更关键的不等式：**USB-C 插错设备最多不通电，MCP 接错权限可能泄露数据或触发副作用**。协议不解决信任问题——OAuth 2.1 授权、沙箱、审计仍是 host 的责任，官方只给 best practices 而非强制。

## 三、2026-07-28 版本文档的实质增量（相对知识库既有笔记）

知识库既有 [[MCP协议与工具调用]] 覆盖的是 2024–2025 经典视图（Client-Server、JSON-RPC、三原语）。本次官方文档可提取的新信号：

| 增量 | 含义 | 我的判断 |
|------|------|---------|
| `server/discover` 强制发现 | 版本 / 能力协商前置，请求自带 `_meta` 版本与能力 | 生态规模大到必须治理兼容性，走向「规范即契约」 |
| Sampling 原语废弃 | 服务器向用户采样被移除 | 收缩边界：server 只做「能力提供」，不做「用户交互」 |
| MCP Apps（扩展） | 可在 host 内渲染交互 UI 的应用 | 从「工具调用」扩展到「应用平台」，最值得注意的方向性变化 |
| Agent Skills over MCP | 技能经 MCP 分发的标准化工作组 | 与 Claude Code skills / ECC 技能体系同源，工程化赛道 |
| Registry + SEPs | 服务器注册表 + 规范增强提案流程 | 治理架构成型：谁来收录、怎么演进、如何淘汰 |
| 远程 server 一等公民 | Streamable HTTP + OAuth 2.1 教程 | 从本地 stdio 主场景走向企业远程部署 |

判断：这些增量共同说明 MCP 的野心不是「又一个工具调用格式」，而是 **AI 应用的外部能力总线 + 分发平台**。风险随之放大：Active / Deprecated / Removed 生命周期会带来版本碎片化成本，2025→2026 的 breaking change（sampling 废弃、discover 引入）已让旧 SDK 代码需要迁移。

## 四、对本知识库 / 自动化管线的启示

- 本仓库 worker（codex-cli + GitHub Actions）目前是「脚本编排」；若未来要把外部工具（搜索 / 文档解析 / 数据库）接进自动化管线，MCP 是比各家私有 API 更稳的接入层候选——但接入前必须**锁定 spec/SDK 版本并验证授权边界**（见下方最小示例）。
- 与 [[ECC]]（harness 操作系统）、[[n8n]]（可视化编排）对照：MCP 解决「连接」层，ECC / n8n 解决「编排」层，三层正交、可组合。

## 五、结论与开放问题

结论：MCP 值得收录。2026-07-28 版本文档给出可落地的协议结构（双层、强制发现、原语收缩）与治理机制（Registry / SEP / 生命周期），官方 Python SDK（`mcp` 2.x）已把复杂度收进 `Client` / `MCPServer` 两个类。

开放问题（留给后续素材）：

1. 「语义适配 M×N」最终靠什么解决——靠 Server Card / Registry 的质量治理，还是靠 Agent 推理能力消化？目前两者都在路上。
2. 规范演进 vs 生态碎片：sampling 废弃、discover 引入这类 breaking change，会不会让 MCP 重演 HTTP / GraphQL 的版本碎片化？Feature Lifecycle 能否兜底？
3. MCP Apps 若成气候，「host 内交互应用」的代码执行边界与安全模型由谁定义？

## 六、最小可运行示例（Python 官方 SDK，版本锁定）


exec
/bin/bash -lc "cd /root/note-worker && sed -n '80,188p' references/articles.md" in /root/note-worker
 succeeded in 0ms:
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

## 观察项

> 暂不收录、持续观察的 URL（防重复采集，不计入编号正文主计数）。由 research Prompt B（`observe`）写入。

| 标题 | 链接 | 来源 | 日期 | 备注 |
| --- | --- | --- | --- | --- |

## 统计

- **正式收录：** 12 篇（编号 01-10、14、15）｜**已淘汰隔离：** 3 篇（编号 11-13，不计入收录数，仅防重复采集）

## 待补充

- [ ] 占位：外部新文章先查编号 01-15 确认未收，再由采集层写入「待处理」队列

exec
/bin/bash -lc "cd /root/note-worker && find expand/06-AI与LLM -type f | sort && echo '---' && cat working/AGENTS.md" in /root/note-worker
 succeeded in 0ms:
expand/06-AI与LLM/Agent工具与平台/ECC.md
expand/06-AI与LLM/Agent工具与平台/Hermes-Agent.md
expand/06-AI与LLM/Agent工具与平台/MarkItDown.md
expand/06-AI与LLM/Agent工具与平台/n8n.md
expand/06-AI与LLM/Agent研究与评测/AgentHPOBench.md
expand/06-AI与LLM/Agent研究与评测/DungeonBench.md
expand/06-AI与LLM/Agent研究与评测/ExtractBench.md
expand/06-AI与LLM/Agent研究与评测/MOT-SR.md
expand/06-AI与LLM/Agent研究与评测/在线策略交互与模仿学习.md
---
# working/ — 作品输出（Phase 5）

可展示的成果：译文、工具、模板、教程。**作品应可独立理解，不依赖知识库其他上下文**——适合分享到博客/GitHub。

## 文件约定

- 每个作品一个文件或子目录：`{简述}.md`
- 译文沿用 `scripts/translator.py` 产出的 frontmatter 约定（title/sourceUrl/sourceAuthor/translatedAt…）
- 作品应是**完成态**：不是草稿（草稿放 `expand/` 相关分类）

## 与 expand 的关系

- `expand/` 是内部加工稿（concepts 层），`working/` 是最终对外输出
- 加工稿 → 打磨 → 移到 working/ 即"毕业"

## 已有作品 ｜（待建设）
exec
/bin/bash -lc "cd /root/note-worker && sed -n '1,200p' agents.md" in /root/note-worker
 succeeded in 0ms:
# 知识库规则（agents.md）

## 身份

你是个人知识库的管理助手。你的任务是阅读外部素材索引，将其加工为结构化、互相链接的知识条目，并按内容性质归入对应产出模块（expand/thinking、working/、prompts/）。

## 目录结构

```
D:\note\
├── references/  ← 第一层：持续输入源头（Phase 0）——纯索引，非内容（原 raw/ 素材已回填索引后删除）
│   ├── agents.md   ← references 规则（分拣引导 + 状态机）
│   └── articles.md ← 文章收录权威索引（### N. 编号正文 + 待处理队列，harness 格式，状态/归属字段机器可读）
├── wiki/          ← 第二层：个人学习笔记（只读，仅用户本人修改；AI 不写入）
│   └── 01-编程语言/ ... 11-生活杂项/   ← 个人笔记分类目录
├── expand/        ← 第三层：AI 加工产物（thinking 思考主导 + 存量概念/深度笔记 + 索引与自动化文档）
│   ├── index.md   ← 内容总目录（AI 维护）
│   ├── log.md     ← 变更日志（AI 维护）
│   ├── 知识图谱.md ← 关系中枢（AI 维护）
│   ├── thinking/   ← 独立思考/观点类条目（AI 主导；新加工的对外观点统一放这里）
│   └── 01-编程语言/ ... 11-生活杂项/   ← AI 生成条目按分类存放（存量保留）
├── working/       ← Phase 4：作品输出（译文/工具/模板，可独立理解）
├── scripts/       ← 自动化管线：collect.py（采集入队）/ worker.py（服务器执行引擎）等
├── prompts/       ← 有效提示词积累（只收录验证有效的；不属知识图谱，不参与一致性门禁）
│   └── feedback/  ← 提示词实测效果反馈（好/中/差/翻车），驱动积累闭环
├── 私密/          ← 敏感信息（密码/令牌等，禁止进入知识图谱）
└── agents.md      ← 本规则文件
```

## 分类体系（wiki/ 顶层目录，如无法分类到其中，可以自行创建相关目录，更新目录结构）

| 目录 | 内容 | 来源 |
| --- | --- | --- |
| `01-编程语言` | C++ / Python 语言基础 | 原 c++、python |
| `02-前端` | HTML/JS/Vue/Layui/ECharts | 原 前端 |
| `03-后端` | Java/JavaWeb/中间件/项目（java、javaweb、中间件、OJ项目、苍穹 子目录） | 原 后端 |
| `04-数据库` | MySQL 及存储引擎（Mysql 子目录） | 原 数据库 |
| `05-数据结构与算法` | 排序/树/DP/BFS/贪心 | 原 数据结构和算法 |
| `06-AI与LLM` | Agent/RAG/MCP/微调/langchain4j/langgraph4j（AgentRag 学习、langchain4jlanggraph4j 学习 子目录） | 原 大模型 |
| `07-Linux与工具链` | Linux/Shell/Git | 原 Linux、git |
| `08-逆向与安全` | 汇编/花指令/CTF 题解 | 原 逆向 |
| `09-源码解读` | 项目源码分析（Claude Code源码解读、juedge0解析文档、Free-fs 子目录） | 原 Claude Code源码解读、juedge0解析文档、Free-fs |
| `10-求职面试` | 面试准备 | 原 AI-Agent代码审查系统 |
| `11-生活杂项` | 与编程无关的个人笔记 | 原 c++/Untitled.md |

## 核心操作

### 知识流水线（学习型体系，仿经典 Phase 结构）

```
Phase 0 references/  ← 持续输入源头（采集 + 去重权威 articles.md）
Phase 1 wiki/        ← 个人学习笔记（只读）
Phase 2 expand/      ← AI 加工产物（概念/深度笔记 = concepts 层）
Phase 3 prompts/     ← 验证有效提示词（另含 feedback/ 效果台账）
Phase 4 working/     ← 作品输出（译文/工具/模板）
```

读完一篇文章后的去处：判值 → `references/articles.md`（编号正文标记 已收录/已淘汰/归属）→ 有观点进 `expand/thinking/`；想输出 → `working/`；有有效提示词 → `prompts/`。

### Ingest（摄入）
当我说"摄入 [索引条目]"时：
1. 读取 `references/articles.md` 的「待处理」队列或编号条目（含 URL/标题，不存素材正文）
2. 抓取原文后按「AI 生成条目模板」加工（含强制补全与 `[补充]` 溯源）
3. 检查 `expand/` 与 `wiki/` 中相关条目；**AI 生成/更新的条目一律写入 `expand/`**（`wiki/` 只读，绝不写入）——独立思考/观点统一写 `expand/thinking/`
4. 在 `expand/` 条目之间建立双向链接 `[[]]`，并更新相关条目的 `## 相关条目` 段；链接 `wiki/` 个人笔记为单向，回链由用户自行决定
5. 更新 `expand/index.md` 内容目录
6. 在 `expand/log.md` 中追加变更记录
7. 更新 `expand/知识图谱.md` 关系描述
8. 回写 `references/articles.md` 该条目的「状态/归属」字段

### Query（查询）
当我提出问题时：
1. 搜索 `wiki/` 中所有相关条目
2. 综合多个条目的信息，给出完整的回答
3. 如果发现知识缺口，建议需要补充的素材

### Lint（检查）
当我说"检查知识库"时：
1. 检查各条目之间是否存在矛盾
2. 找出孤立的（没有其他条目链接到的）条目
3. 标记可能过时的信息
4. 报告发现的问题和建议

### 一致性门禁（Consistency Gate）
> 自动执行，无需手动触发。`scripts/check_consistency.py` 实现 K1-K7 不变量检查；`.githooks/pre-commit` 本地提交前运行，`.github/workflows/consistency.yml` 在 CI 运行（分支保护下为必需检查）。

**K1-K7 违规自动修正原则（AI 在 Ingest / 编辑时需遵守）**：
1. 新增 `expand/` 条目**必须**同时更新 `expand/index.md`（计数 + 条目表），否则 K2/K5 拦截
2. AI 条目 frontmatter 必须含 `created / updated / sources / tags`（K3）
3. 只能在真实存在的条目之间建立 `[[]]` 链接，禁止对不存在目标链接（K4）
4. `expand/` 必检文档中的 markdown 表格必须形状对齐（K6）
5. `references/articles.md` 编号条目的「状态：」必须 ∈ {待处理, 已收录, 已淘汰}；归属字段若指向 `expand/` 必须真实存在（K1）
- 本地校验：`python scripts/check_consistency.py`（需 `git config core.hooksPath .githooks`）

## 知识条目格式

每个 wiki 条目遵循以下格式（注意：**现有个人笔记内容保持不变**，仅在末尾追加 `## 相关条目`）：

    ---
    created: YYYY-MM-DD
    updated: YYYY-MM-DD
    sources: [来源文件列表]
    tags: [内容标签, type/论文|工具|教程|想法, status/待验证|已实践, 情绪标签(启发/反直觉)]
    ---

    # 条目标题

    一句话概述这个概念。

    ## 详细说明

    正文内容...

    ## 相关条目
    - [[相关条目A]]
    - [[相关条目B]]

### AI 生成条目：深度技术笔记模板（存量概念类，2026-08 起 expand 定位为 thinking）

> **当前默认：** expand/ 只承担 thinking（独立思考）作用。新摄入的外部素材默认进 `expand/thinking/`，
> 采用下方模板的「学习型相位结构」但聚焦独立观点；纯概念拆解/深度笔记（本模板）不再作为新条目默认，
> 仅当素材确实需要（技术深度大于观点价值）且用户明确要求时使用，写入对应 `expand/01-xx` 分类目录。

摄入外部素材（采集文章 / 论文 / 项目 / 视频）时，AI 按以下「深度技术笔记」模板加工。素材类型不适用的章节可精简，但核心章节不可省略；本模板取代原六维框架作为 AI 条目的输出标准。

**角色设定**：资深技术架构师，专注**两大追踪方向**：
1. **AI Agent 开发**：RAG、Agent 工程化（harness / 编排 / 上下文管理 / 调度）、多智能体架构、Agent 评测、Agent 工具与平台（LangChain/LangGraph、Claude Code、Codex 生态）
2. **跨平台开发**：Kotlin 多平台（KMP / Compose Multiplatform）、Flutter，共享逻辑 + 多端 UI 的落地架构

目标是让读者 15 分钟内理解核心原理并能直接应用于生产项目。素材与上述方向无关但确有技术价值时归入「通用技术」分类，不强行套用 Agent/跨平台视角。

**质量门槛（摄入前先过滤，不达标不要硬写）**：
- **必须满足（全部）**：有实质技术内容（非营销/软文）；有原创洞察、方案或可复现信息（非转述他人结论）；有可信来源（署名作者 / 官方文档 / 可验证链接）支撑 `[补充]` 溯源
- **加分项**：有实验数据/基准/成本对比；有可运行最小示例或架构图；直面失败案例/反模式/权衡；是 2 周内新进展或更新陈旧认知
- **直接排除**：纯标题空壳；纯榜单/招聘/无关娱乐；与知识库已有条目高度重复、无增量（见「知识关联地图」去重检查）
- 素材不达标时**不生成条目**，返回 `skip: true` 并附 `skip_reason`（ingest 时素材标为 `rejected`）

**加工规则**：
1. **强制补全与深度融合**：素材浅薄、逻辑不完整或缺代码示例时，主动补充外部权威知识（官方文档 / 源码解析 / 最新架构演进），并**直接融入正文结构**（概念拆解、方案对比、代码示例），不得仅作附加说明
2. **来源溯源**：补充内容在句末/段末用 `[补充]` 显式标注；**笔记必须标注参考素材（references/articles.md 编号条目）与相关官方网站链接**（专门的「参考素材与官方链接」章节）
3. **人话解释**：禁止照抄学术/教程表述，核心概念必须给"一句话人话解释"（生活化类比或底层逻辑推演）
4. **代码规范**：涉及代码必须给**生产级最小可运行示例**（含异常捕获、依赖锁定、安全边界），标注语言、框架、适用版本（如 "Kotlin 2.0 + KMP 1.9" 或 "langchain4j 2.x"）
5. **工程视角**：所有方案补充生产级落地考量（性能、安全、成本、异常处理）
6. **排版**：严格 Markdown，多用表格、列表、加粗，拒绝长篇段落

**输出结构**（不可省略章节）：

    ## 本周主题：{动态提取主题}
    ### 一句话总结
    > 不超过 50 字，概括素材核心价值与底层逻辑
    ### 记忆锚点（3 个关键记忆点）
    1. 一句话记忆点（可含选型口诀）
    ### 核心概念拆解
    - **概念名称**
      - 🗣️ 人话：通俗类比
      - 🔧 本质：底层原理一句话
      - 📍 定位：AI Agent（RAG / Agent 工程 / 调度）或跨平台（KMP / Flutter）哪一环
      - 💡 补充：[补充]（附官方链接）
    ### 架构与方案对比（如有选型）
    - **决策流程图**：先用 Mermaid 画极简决策树（如"扫描件→上云；普通文件→本地"）
    - 对比表：| 维度 | 方案A | 方案B | 方案C |（适用场景 / 核心优势 / 主要劣势 / 生产级成熟度（谨慎评级）/ 架构师推荐；[补充] 在单元格标注）
    ### 代码与实操速查
    - 生产级最小示例（异常捕获 / 版本锁定 / 安全边界，[补充] 生成需标注）/ 关键配置 / 常见报错 Top3
    ### 避坑清单（Anti-patterns）
    - 错误做法 → 正确做法（原因），至少 4 条（含大文件/内存、安全、依赖、性能类）
    ### 知识关联地图
    - 前置知识 / 横向关联（`[[条目]]` #标签，可点击可检索）/ 纵向延伸（具体资源名）——**去重检查**：与既有条目高度重复时，在「相关条目」引用而非重建
    ### 本周素材盲区与知识增量
    - 原文盲区 → 转化为「下周探索方向」（候选选题）/ 知识增量总结（2-3 条）
    ### 参考素材与官方链接
    - 原始素材索引：references/articles.md 编号条目（含来源 URL）
    - 官方文档 / 网站链接列表（带用途说明）
    ### 本周行动清单
    - [ ] 行动描述（预计耗时 / 关联知识点）✅ Done when：完成标准
    ### 相关条目
    - [[相关条目A]]

**技术说明**：管道已接入 Firecrawl Search 联网检索——`ingest.py` 会用素材主题检索并将真实结果注入 Prompt，`[补充]` 内容以检索结果为准并标注来源 URL；可用环境变量 `FIRECRAWL_SEARCH_DISABLED=1` 禁用检索。

## index.md 格式

内容目录应列出所有 wiki 条目及其一句话摘要，按分类目录组织：

    ## 01-编程语言
    - [[条目A]]：一句话描述
    - [[条目B]]：一句话描述

## log.md 格式

变更日志按时间倒序排列：

    ## [YYYY-MM-DD] ingest | 来源标题
    - 新增：[[条目X]]
    - 更新：[[条目Y]]（新增关于...的内容）

## 链接约定

1. 优先使用短链接 `[[文件名]]`；文件名不唯一时（如两个 `集合.md`、两个 `free-fs.md`）使用路径链接 `[[分类/子目录/文件名]]`
2. 文件名含特殊字符（`#`、空格、长乱码）的笔记无法被链接解析，应建议重命名后再入图谱
3. 每次新增/更新条目后，同步维护 `wiki/知识图谱.md` 的关系描述

exec
/bin/bash -lc "cd /root/note-worker && cat references/AGENTS.md && echo '=== expand/index.md (head) ===' && head -80 expand/index.md" in /root/note-worker
 exited 1 in 0ms:
cat: references/AGENTS.md: No such file or directory

exec
/bin/bash -lc "cd /root/note-worker && sed -n '1,160p' scripts/research.py" in /root/note-worker
 succeeded in 0ms:
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""情报层：Prompt A（Firecrawl 搜索）→ Prompt B（长分析三档分流）→ 分档写入 articles。

由 research.yml（每周 + 手动）SSH 触发，运行在服务器。

职责：
1. 注入已知内容（retrack.py --list）
2. codex × Prompt A（提示词内强制调用 Firecrawl MCP/search）→ 搜索条目卡
3. codex × Prompt B（长分析）→ index | translate | observe
4. 按档写入 references/articles.md（编号 / 待处理 / 观察项）
5. 不开 PR；commit 后 push 到长期分支 pipeline/queue（供 curate 合并）

仅依赖标准库 + codex CLI（需能调用 Firecrawl）。
"""
import argparse
import datetime
import json
import os
import pathlib
import re
import shlex
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import collect
from kb_common import (
    append_numbered_entries,
    append_observe_row,
    fmt_article_entry,
    next_article_number,
)


def sh(cmd, cwd=None, check=True):
    r = subprocess.run(cmd, shell=True, cwd=cwd or ROOT,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if check and r.returncode != 0:
        print(f"[research] 命令失败: {cmd}\n{r.stdout}\n{r.stderr}")
        sys.exit(r.returncode)
    return r


def known_content_block():
    """优先 retrack --list；失败则回退标题/URL 拼装。"""
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "retrack.py"), "--list"],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if r.returncode == 0 and r.stdout.strip():
        return r.stdout.strip()
    art = ROOT / "references" / "articles.md"
    if not art.exists():
        return "（暂无）"
    t = art.read_text(encoding="utf-8", errors="replace")
    titles = re.findall(r"### \d+\. (.+)", t)
    urls = collect.existing_urls()
    lines = [f"- {x}" for x in titles[:80]]
    lines.append("URL 清单（已收录 + 待处理，去重用）：")
    lines += [f"  - {u}" for u in sorted(urls)[:120]]
    return "\n".join(lines) or "（暂无）"


def run_codex(prompt, prompt_name, timeout=1200):
    prompt_file = pathlib.Path(__import__("tempfile").gettempdir(), prompt_name)
    prompt_file.write_text(prompt, encoding="utf-8")
    cmd = (
        f"set -a; source /etc/environment; set +a; "
        f"codex exec -C {shlex.quote(str(ROOT))} "
        f"--sandbox workspace-write -c sandbox_workspace_write.network_access=true "
        f"< {shlex.quote(str(prompt_file))}"
    )
    try:
        r = subprocess.run(
            cmd, shell=True, cwd=ROOT, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=timeout,
        )
        return r.stdout + "\n" + r.stderr, r.returncode
    except Exception as e:
        print(f"[research] codex 调用失败：{type(e).__name__}: {e}")
        return "", 1


def extract_json_obj(stdout):
    """从 codex 输出提取 JSON 对象。"""
    text = stdout or ""
    m = re.search(r"codex\n(.*)", text, re.S)
    if m:
        text = m.group(1)
    fences = re.findall(r"```json\s*(.*?)```", text, re.S)
    for f in fences:
        try:
            return json.loads(f.strip())
        except json.JSONDecodeError:
            continue
    dec = json.JSONDecoder()
    for m in re.finditer(r"\{", text):
        try:
            obj, _ = dec.raw_decode(text, m.start())
            if isinstance(obj, dict):
                return obj
        except json.JSONDecodeError:
            continue
    return {}


def apply_triage(candidates):
    """按 verdict 写入 articles.md。返回 (translate_n, index_n, observe_n)。"""
    art = ROOT / "references" / "articles.md"
    if not art.exists():
        print("[research] articles.md 不存在")
        return 0, 0, 0
    known = collect.existing_urls()
    t = art.read_text(encoding="utf-8")
    tn = ix = ob = 0
    today = datetime.date.today().isoformat()
    for c in candidates:
        url = (c.get("url") or "").strip()
        title = (c.get("title") or "").strip()
        if not url or not title:
            continue
        verdict = (c.get("verdict") or "observe").strip().lower()
        if verdict not in ("index", "translate", "observe"):
            verdict = "observe"
        lineage = (c.get("lineage") or "general").strip()
        reason = (c.get("reason") or "").strip()
        row = {
            "title": title,
            "url": url,
            "source": c.get("source") or "research",
            "date": c.get("date") or today,
        }
        if url in known and verdict != "translate":
            # 已在索引：跳过 index/observe；translate 仍可能已在队列
            print(f"[research] 去重跳过（{verdict}）：{title[:50]}")
            continue
        if verdict == "translate":
            if url in known:
                print(f"[research] 去重跳过（translate）：{title[:50]}")
                continue
            msg = collect.save_item("research", {**row, "title": title, "url": url})
            print(f"[research] translate → {msg}")
            if msg and msg.startswith("入队"):
                known.add(url)
                tn += 1
                t = art.read_text(encoding="utf-8")  # save_item 已写盘
            continue
        if url in known:
            print(f"[research] 去重跳过（{verdict}）：{title[:50]}")
            continue
        if verdict == "index":
            n = next_article_number(t)
            entry = fmt_article_entry(
                n, row, "已收录", moved_file=None,
                core=reason or title[:80], lineage=lineage,
            )
            t = append_numbered_entries(t, [entry])

exec
/bin/bash -lc "cd /root/note-worker && sed -n '160,320p' scripts/research.py" in /root/note-worker
 succeeded in 0ms:
            t = append_numbered_entries(t, [entry])
            art.write_text(t, encoding="utf-8")
            known.add(url)
            ix += 1
            print(f"[research] index → #{n:02d} {title[:40]} ({lineage})")
            continue
        # observe
        t = append_observe_row(t, row, reason)
        art.write_text(t, encoding="utf-8")
        known.add(url)
        ob += 1
        print(f"[research] observe → {title[:40]}")
    return tn, ix, ob


def push_queue_branch():
    """把 articles（及 research 落盘）推到 pipeline/queue，不开 PR。"""
    sh("git add references/articles.md candidates 2>/dev/null || git add references/articles.md",
       check=False)
    changed = sh("git status --porcelain", check=False).stdout.strip()
    if not changed:
        print("[research] 无变更，跳过 push")
        return 0
    sh("git config user.name note-worker || true", check=False)
    sh("git config user.email note-worker@users.noreply.github.com || true", check=False)
    # 在当前 HEAD 上提交，再推送到 pipeline/queue
    r = sh('git commit -m "research: 情报搜索分流入队（无 PR）"', check=False)
    if r.returncode != 0 and "nothing to commit" not in (r.stdout + r.stderr):
        # 可能已在别处提交；继续尝试 push
        pass
    r = sh("git push --force-with-lease origin HEAD:pipeline/queue", check=False)
    if r.returncode != 0:
        print(f"[research] push pipeline/queue 失败：{r.stderr[-400:]}")
        return 1
    print("[research] 已推送 origin/pipeline/queue（不开 PR）")
    return 0


def main():
    lock = pathlib.Path(__import__("tempfile").gettempdir(), ".research.lock")
    if lock.exists():
        age = time.time() - lock.stat().st_mtime
        if age < 7200:  # 2h 内视为占用
            print("[research] 检测到运行中的 research 实例（锁存在），退出")
            return 0
        print(f"[research] 清除过期锁（age={int(age)}s）")
        lock.unlink(missing_ok=True)
    lock.touch()
    try:
        return _run()
    finally:
        lock.unlink(missing_ok=True)


def _run():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=14)
    ap.add_argument("--max", type=int, default=10)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    today = datetime.date.today()
    start = today - datetime.timedelta(days=args.days)
    git_ref = os.environ.get("NOTE_GIT_REF", "main")
    if not args.dry_run:
        subprocess.run(f"git fetch origin {git_ref}", shell=True, cwd=ROOT,
                       capture_output=True, text=True)
        subprocess.run(f"git checkout {git_ref}", shell=True, cwd=ROOT,
                       capture_output=True, text=True)
        subprocess.run(f"git pull --rebase origin {git_ref}", shell=True, cwd=ROOT,
                       capture_output=True, text=True)
        # 若本地跟踪不到远程分支，硬对齐 origin/<ref>
        subprocess.run(f"git reset --hard origin/{git_ref}", shell=True, cwd=ROOT,
                       capture_output=True, text=True)

    known = known_content_block()
    search_tpl = (ROOT / "prompts" / "research-search.md").read_text(encoding="utf-8")
    # 去掉 YAML frontmatter，避免干扰模型
    if search_tpl.startswith("---"):
        search_tpl = re.sub(r"^---\s*\n.*?\n---\s*\n", "", search_tpl, count=1, flags=re.S)
    prompt_a = (search_tpl
                .replace("{START_DATE}", start.isoformat())
                .replace("{END_DATE}", today.isoformat())
                .replace("{KNOWN_CONTENT}", known)
                .replace("{MAX_ITEMS}", str(args.max)))

    if args.dry_run:
        snippet = prompt_a[:2000]
        try:
            print("[research] dry-run Prompt A（截断）：\n", snippet)
        except UnicodeEncodeError:
            sys.stdout.buffer.write(("[research] dry-run Prompt A:\n" + snippet + "\n").encode("utf-8", "replace"))
        return 0

    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = ROOT / "candidates" / f"research-{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)

    print("[research] Prompt A：搜索（要求调用 Firecrawl）…")
    stdout_a, rc_a = run_codex(prompt_a, ".research_search_prompt.md")
    (out_dir / "search.md").write_text(stdout_a, encoding="utf-8")
    if rc_a != 0:
        print(f"[research] Prompt A 失败 rc={rc_a}")
        print(stdout_a[-1500:])
        return rc_a

    analyze_tpl = (ROOT / "prompts" / "research-tracker.md").read_text(encoding="utf-8")
    if analyze_tpl.startswith("---"):
        analyze_tpl = re.sub(r"^---\s*\n.*?\n---\s*\n", "", analyze_tpl, count=1, flags=re.S)
    prompt_b = (analyze_tpl
                .replace("{SEARCH_OUTPUT}", stdout_a[-60000:])
                .replace("{KNOWN_CONTENT}", known))

    print("[research] Prompt B：长分析 + 三档分流…")
    stdout_b, rc_b = run_codex(prompt_b, ".research_analyze_prompt.md")
    (out_dir / "analyze.md").write_text(stdout_b, encoding="utf-8")
    if rc_b != 0:
        print(f"[research] Prompt B 失败 rc={rc_b}")
        print(stdout_b[-1500:])
        return rc_b

    data = extract_json_obj(stdout_b)
    cands = data.get("candidates") if isinstance(data, dict) else None
    if not isinstance(cands, list):
        # 兜底：尝试从 Prompt A JSON 取候选并默认 observe
        data_a = extract_json_obj(stdout_a)
        cands = data_a.get("candidates", []) if isinstance(data_a, dict) else []
        for c in cands:
            c.setdefault("verdict", "observe")
        print("[research] Prompt B JSON 解析失败，回退 A 候选且默认 observe")

    print(f"[research] 分流候选 {len(cands)} 条")
    tn, ix, ob = apply_triage(cands)
    print(f"[research] 完成：translate={tn} index={ix} observe={ob}")
    return push_queue_branch()


if __name__ == "__main__":
    sys.exit(main())

exec
/bin/bash -lc "cd /root/note-worker && head -60 candidates/research-20260810-115057/search.md && echo '=== references/agents.md head ===' && head -60 references/agents.md" in /root/note-worker
 succeeded in 0ms:
搜索完成，两轮验证均通过。最终选定 2 条（均为 AI Agent 域；跨平台窗口内未发现达标内容，最接近的 JetBrains KotlinLLM 为 Kotlin/JVM 研究、非 KMP 域，未入选）。

## 1. 引入 Data-eng-bench：为什么数据工程需要"数据原生"的 Agent Harness

- 链接：https://www.snowflake.com/en/blog/engineering/data-eng-bench-data-engineering-agent-benchmark/
- 作者/来源：Snowflake AI Research（联合 Bespoke Labs）/ Snowflake Engineering Blog
- 日期：2026-08-06
- 推荐指数：⭐⭐⭐⭐⭐

一句话摘要：开源 103 任务 dbt 数据工程基准，量化证明 harness 选择比模型更能左右 agent 质量与成本。

核心洞察（3条）：

1. Harness 对质量影响依模型而异：同模型跨 harness 的 Pass@1 最多差约 4pp——Opus 5 配 CoCo 最佳（73.8%），配 Claude Code 降 4pp；Sonnet 5 在两 harness 下持平；GPT 5.6 Sol 配 CoCo 比 Codex 高 3.6pp。
2. Harness 对成本影响远大于质量：CoCo 以 3.9x 更低成本实现比 Claude Code 高 4pp 的 Pass@1，且工具调用少 1.5x、agent 步数少 2.2x——数据原生 harness 的"少做"本身就是效率来源。
3. Pass@1 与 Pass^3 落差暴露可靠性缺口：最强配置一次成功率 73.8%，但三试全过仅 64.1%；评测用 10–50 条隐藏断言按"整条管道全对"计分，能区分"能生成像样模型"与"整个管道正确"。

值得收录理由：首个仓库级 dbt agent 评测（103 任务 > ADE-Bench 63），给出 harness×模型 双变量质量/成本矩阵并开源，直接服务 agent 评测与 harness 选型。

## 2. LLM 0.32 发布：推理轨迹、服务端工具与内容寻址日志

- 链接：https://simonwillison.net/2026/Aug/4/new-release-of-llm/
- 作者/来源：Simon Willison
- 日期：2026-08-04
- 推荐指数：⭐⭐⭐⭐

一句话摘要：LLM CLI 里程碑版本：推理轨迹独立输出、OpenAI Responses 服务端工具、Git 式内容寻址 SQLite 日志。

核心洞察（3条）：

1. 推理轨迹默认写 stderr、与 stdout 分离（`-R` 关闭），保证管道仍可安全消费纯模型输出——agent 工具链处理 reasoning 流的标准做法。
2. 日志重构为内容寻址消息存储（仿 Git），多轮对话不再逐轮重复记录完整 JSON 历史，解决"每条请求都带全量历史"带来的日志膨胀。
3. 以 `stream_events()` 统一 reasoning/text/tool-call 事件流，并新增 `llm openai endpoint` 一条命令对接任意 OpenAI 兼容端点，配合 llm-chat-completions-server 可自建兼容服务。

值得收录理由：Tier 1 作者对 LLM 工具平台的深度工程复盘，含可复现代码，覆盖推理轨迹、服务端工具、日志架构等 agent 工具链核心议题。

```json
{
  "candidates": [
    {
      "title": "Introducing Data-eng-bench: Why You Need \"Data-Native\" Harnesses for Data Engineering",
      "url": "https://www.snowflake.com/en/blog/engineering/data-eng-bench-data-engineering-agent-benchmark/",
      "source": "Snowflake AI Research (Snowflake Engineering Blog)",
      "date": "2026-08-06",
      "stars": 5,
      "summary": "开源103任务dbt数据工程基准，量化证明harness选择比模型更能左右agent质量与成本。",
      "insights": [
        "同模型跨harness的Pass@1最多差约4pp，且harness效果依赖模型（Opus5配CoCo最佳、Sonnet5两harness持平）。",
        "CoCo以3.9x更低成本实现比Claude Code高4pp的Pass@1，工具调用少1.5x、agent步数少2.2x。",
        "Pass@1(73.8%)与Pass^3(64.1%)落差暴露可靠性缺口，10-50条隐藏断言按整管道全对计分。"
      ],
      "reason": "首个仓库级dbt agent评测（103任务）并开源，harness×模型双变量质量/成本数据直接服务agent评测与选型。"
    },
    {
      "title": "New release of LLM adds support for reasoning traces, OpenAI Responses, server-side tools, and smarter logging",
      "url": "https://simonwillison.net/2026/Aug/4/new-release-of-llm/",
      "source": "Simon Willison (simonwillison.net)",
      "date": "2026-08-04",
      "stars": 4,
      "summary": "LLM CLI里程碑版本：推理轨迹独立输出、OpenAI Responses服务端工具、Git式内容寻址SQLite日志。",
=== references/agents.md head ===
# references/ — 外部资源索引

指外：持续输入的源头（Phase 0 采集层）。**这里是指针，不是内容本身。** 原始素材不做留存，
只做「收录 → 判值 → 归入产出模块」的跟踪索引，避免重复采集。

## 文件约定

| 文件 | 职责 | 谁维护 |
|------|------|--------|
| `articles.md` | 文章收录权威索引（编号正文 + 待处理 + 观察项） | `research.py` 分流写入；`curate.py` 落位回写 |
| `agents.md` | 本目录规则（本文） | 人工 + AI |

- 每条记录包含：编号、标题、链接、作者、日期、状态（待处理/已收录/已淘汰）、归属（产出模块路径）
- **状态机**：research `translate`→`待处理`→curate 落位→`已收录`；`index` 直接`已收录`；`observe`→观察项表；或`已淘汰`

## 索引 → 产出的分流规则（codex 处理素材时判定归属）

| 产出方向 | 落点 | 何时 |
|---------|------|------|
| 值得翻译 | `working/`（经 curate 唯一终审 PR） | research `translate` |
| 仅索引收录 | articles.md `已收录`（核心含脉络） | research `index` |
| 持续观察 | articles.md「观察项」表 | research `observe` |
| 独立思考 / 观点 | `expand/thinking/` | 人写；codex 只建议 |
| 提示词沉淀 | `prompts/` | 人判亲测有效 |

## 与其他目录的关系

- `expand/` ← AI 独立思考产物（thinking 主导，concepts/深度笔记存量保留）
- `working/` ← 作品输出（Phase 输出层）
- `prompts/` ← 验证有效提示词
- `feedback/` ← 复盘迭代（lint 巡检报告 + failure 记录）
- 一致性：K1 状态机在本文 + `scripts/check_consistency.py` 把关
exec
/bin/bash -lc 'cd /root/note-worker && cat prompts/research-tracker.md 2>/dev/null | head -120' in /root/note-worker
 succeeded in 0ms:
---
created: 2026-08-09
updated: 2026-08-10
type: workflow
status: 待验证
product: null
source: 知识库情报分析 Prompt B（搜后长分析）
---

# 技术情报分析（Prompt B）

> 运行器：服务器 codex，由 `research.py` 第二段调用。输入为 Prompt A 的搜索结果；**不再负责搜索**。

以下是最近 2 周的技术情报搜索结果。请基于我们项目的已有内容，做以下分析：

{SEARCH_OUTPUT}

### 请分析：

1. **优先级排序**：哪些内容最值得我们收录？考虑因素：
   - 对**已收录文章 + 已跟踪内容**（完整清单见下方「已知内容」，或 `references/articles.md` / `python scripts/retrack.py --list` 注入段）的补充价值
   - 对 `expand/thinking/` 中已有洞见的验证或挑战
   - 对开放问题清单的回答程度

2. **缺口分析**：这批内容覆盖了我们的哪些知识缺口？还有哪些缺口未被触及？
   当前已知缺口（对齐本知识库两大方向）：
   - Agent harness 行为正确性与覆盖率评估
   - 上下文 / compaction / 记忆策略的可复现实践
   - 多智能体编排反模式与成本
   - Agent 评测：model / harness / 环境的组件级归因
   - 跨模型可移植性与迁移指南
   - 中小团队 Agent 工程落地案例与成本数据
   - Harness / 控制的激活策略（always-on / per-commit / conditional / human-summoned）
   - Agent 安全审计（轨迹违规、多智能体信息流、工具权限边界）
   - KMP / Compose Multiplatform 与 Flutter 的架构选型、共享逻辑边界、工具链痛点
   - 跨平台 CI / 发布 / 性能基线

3. **趋势信号**：这批内容中是否有新的趋势或方向？与既有 Agent 工程 / 跨平台实践是否一致或冲突？

4. **收录建议**：对每条推荐内容给出具体建议（三选一，互斥）：
   - 收录到 references/articles.md（哪个脉络 lineage）→ verdict=`index`
   - 值得翻译到 working/ → verdict=`translate`
   - 暂不收录，持续观察 → verdict=`observe`

### 已知内容

{KNOWN_CONTENT}

### 输出要求

先用中文写出上述 1–4 的完整分析（可含表格与列表），再在文末附机器可读 JSON：

```json
{
  "analysis": {
    "priority": ["..."],
    "gaps_covered": ["..."],
    "gaps_open": ["..."],
    "trends": ["..."]
  },
  "candidates": [
    {
      "title": "...",
      "url": "...",
      "verdict": "index|translate|observe",
      "lineage": "agent/harness",
      "reason": "一句话",
      "stars": 4
    }
  ]
}
```

脉络（lineage）建议取值：`agent/rag` · `agent/harness` · `agent/orchestration` · `agent/context` · `agent/multi-agent` · `agent/eval` · `agent/platform` · `crossplatform/kmp` · `crossplatform/flutter` · `crossplatform/toolchain` · `general`（慎用）。

exec
/bin/bash -lc "cd /root/note-worker && head -50 expand/thinking/AGENTS.md && echo '=== ECC.md head ===' && head -40 'expand/06-AI与LLM/Agent工具与平台/ECC.md'" in /root/note-worker
 succeeded in 0ms:
# thinking/ — 独立思考（AI 主导）

expand/ 下的思考层。**读文章后的独立观点、质疑、延伸、综合**放这里；
纯概念拆解/深度笔记（存量）仍在 `expand/01-xx` 分类目录。

## 文件约定

- 文件名：自由命名，建议用问题或论点（如 `codex-as-execution-engine.md`、`harness-vs-mcp.md`）
- 结构：问题/论点 → 自己的分析 → 结论或开放问题
- frontmatter 沿用 AI 条目规范（created / updated / sources / tags）
- 鼓励质疑、反直觉，不做原文复述

## 与 references/articles.md 的联动

codex 处理一条文章（`### N.` 条目）后在此论坛所属：
- 有独立见解 → 在本目录生成 thinking 条目，并在 articles.md 该条目的「归属：」字段指向本文件
- 可产出作品 → `working/`
- 提炼有效 prompt → `prompts/`
- 无增量 → 仅标记已收录/已淘汰，不生成

## 已有思考

| 文件 | 话题 | 核心论点 |
|------|------|---------|
| （待首个条目） | — | — |=== ECC.md head ===
---
created: 2026-08-04
updated: 2026-08-04
sources: [raw/github-2026-08-03-08c2bad9.md]
tags: [AI, Agent, 编程代理, 工具系统, type/工具, status/待验证, 启发]
---

# ECC

给编程代理装一套"操作系统"：技能、本能、记忆、安全一应俱全，Claude Code / Codex / Cursor 都能插上。

## 检索问题（Q&A）
- 编程代理除了模型还缺什么基础设施？→ 本条目：ECC 的技能 / 本能 / 记忆 / 安全分层
- Agent 工程化参考实现？→ ECC 的 npm 包 + GitHub App 架构

## 结构化提炼

### 核心论点
ECC 把编程代理的工程化需求（技能管理、持久记忆、安全防护、多运行时）沉淀为可插拔的"代理工具操作系统"，跨 Claude Code / Codex / Cursor 等前端使用。

### 逻辑骨架
- 问题：编程代理各自为战，缺少可复用的能力层
- 方案：Agent Harness 分层——技能（skills）、本能（instincts）、记忆（memory）、安全（AgentShield）
- 形态：npm 包（ecc-universal / ecc-agentshield）+ GitHub App + Pro 订阅（私有仓库协作）
- 运行时：Shell / TypeScript / Python / Go / Java / Perl / Markdown

### 关键概念（费曼式）
- Agent Harness：把"代理怎么干活"的公共部分（工具、记忆、权限）抽出来，像操作系统管硬件一样管能力
- 本能（instincts）：预设的行为倾向 / 检查点，让代理不用每次重新想"该不该这么干"

## 深度追问

### 苏格拉底式质疑
1. "跨前端"是否只是薄封装？各家 agent 的钩子能力差异如何抹平？
2. 安全层（AgentShield）的防护边界在哪——能否拦截恶意 prompt 注入？
3. 个人项目 + GitHub App 的权限模型，是否与"最小权限"原则冲突？

### 背景与盲区
- 背景：编程代理（Claude Code / Codex）已成为 Agent 主战场，能力层正在工具化
- 盲区：缺少公开评测数据；社区规模小，长期维护风险

exec
/bin/bash -lc "cd /root/note-worker && head -50 'expand/06-AI与LLM/Agent研究与评测/AgentHPOBench.md' && echo '=== Hermes-Agent head ===' && head -35 'expand/06-AI与LLM/Agent工具与平台/Hermes-Agent.md'" in /root/note-worker
 succeeded in 0ms:
---
created: 2026-08-04
updated: 2026-08-04
sources: [raw/arxiv-2026-08-03-8bf73671.md]
tags: [AI, Agent, 超参数优化, 评测基准, type/论文, status/待验证, 启发]
---

# AgentHPOBench

LLM Agent 能否像研究员一样"读懂实验证据并调整下一步"？AgentHPOBench 用 30 个可执行 ML 任务来回答这个问题。

## 检索问题（Q&A）
- Agent 做实验/调参的能力怎么评测？→ 本条目：AgentHPOBench 基准设计、任务与结论
- LLM Agent 目前最大的短板是什么？→ 持续迭代改进、复杂日志诊断、稳定逼近参考性能

## 结构化提炼

### 核心论点
现有基准只测"最终答案"不测"实验过程"；AgentHPOBench 把 Agent 当作顺序超参数优化器来评估——每次观察累积的配置、指标和日志后提出下一个配置。

### 逻辑骨架
- 问题：LLM 已从代码补全走向自主科学代理，但缺少"过程性实验能力"的评测
- 方案：顺序基准，7 个研究类别、30 个可执行 ML 任务，每任务从验证过的基线运行开始
- 评估：统一协议下对比 12 种主流 Agent 与传统 HPO 基线
- 结论：Agent 有可测量的优化能力，但迭代改进、日志诊断、稳定收敛仍有明显局限

### 关键概念（费曼式）
- 顺序超参数优化：不是一次性调好参数，而是"调→看结果→再调"的闭环，像调水温一样逐步逼近
- 基线运行（baseline run）：给 Agent 一个已跑通的起点，避免从零开始

## 深度追问

### 苏格拉底式质疑
1. 30 个任务是否覆盖真实科研场景的多样性？跨领域泛化结论是否过强？
2. "诊断复杂日志"失败，是模型能力不足，还是评测日志格式对 Agent 不友好？
3. 传统 HPO 基线（贝叶斯优化）计算成本远低于 LLM Agent——能力提升的性价比是否值得？

### 背景与盲区
- 背景：HPO 领域经典基线是贝叶斯优化（SMBO / Tree Parzen），LLM Agent 的定位是"用常识推理替代昂贵搜索"
- 盲区：未覆盖 Agent 主动设计实验（而非仅调参）、多轮长程实验的记忆成本、评测 token 开销

### 溯源与验证
- 论文 2607.29626，任务公开可复现；结论基于 12 个 Agent 的统一协议对比

## 联想与缝合

### 跨学科类比
像"实习研究员带教考核"：只考论文答辩（静态答案）不够，还要查实验记录本（过程性决策）——AgentHPOBench 就是这本记录本的评分表。

### 与知识库联系
=== Hermes-Agent head ===
---
created: 2026-08-04
updated: 2026-08-04
sources: [raw/github-2026-08-03-7033561e.md]
tags: [AI, Agent, 记忆机制, 技能学习, 自动化, type/工具, status/待验证, 启发]
---

# Hermes-Agent

一个会"长记性"的代理：任务做完自动沉淀技能、技能越用越顺手、隔几天还记得你是谁——把学习循环做进 Agent 本体。

## 检索问题（Q&A）
- Agent 怎么实现跨会话记忆 / 持续学习？→ 本条目：Hermes 的闭环学习循环设计
- 想要能定时干活、多端聊天的自托管 Agent？→ Hermes 的 cron + Telegram / Discord / CLI 网关

## 结构化提炼

### 核心论点
Hermes Agent 的核心差异是内置闭环学习循环：从经验创建技能 → 使用中改进技能 → 主动维护记忆 → 跨会话构建用户画像，且模型无锁定、部署轻量。

### 逻辑骨架
- 问题：主流 Agent 无状态，会话结束就"失忆"，技能不沉淀
- 方案：技能（任务后自动创建，使用中自改进，兼容 agentskills.io）+ 记忆（FTS5 会话搜索 + LLM 摘要 + Honcho 用户建模）
- 形态：单网关多端（Telegram / Discord / Slack / WhatsApp / CLI / TUI）+ 内置 cron 定时 + 子代理委派
- 部署：5 美元 VPS / 无服务器（Modal / Daytona），模型任意切换

### 关键概念（费曼式）
- 闭环学习：做任务 → 总结成技能 → 下次直接复用并改进，像老员工积累工作手册
- FTS5 会话搜索：全库全文检索历史对话，配合 LLM 摘要实现"我记得聊过这个"

## 深度追问

### 苏格拉底式质疑
1. "技能自改进"的评估机制是什么？会不会越改越偏？
2. 记忆膨胀（FTS5 + 摘要）的成本与隐私边界——会话内容存哪里、谁可读？

exec
/bin/bash -lc "cd /root/note-worker && git log --oneline -15 && echo '---' && cat expand/log.md 2>/dev/null | head -40" in /root/note-worker
 succeeded in 0ms:
d2a51f2 fix: E2E clears research/curate locks before start (#28)
aa10b94 fix: expire stale research lock and clear locks in E2E (#27)
3577843 fix: E2E run research/curate via nohup to avoid SSH broken pipe (#25)
3475a0f feat: single review PR + dual research prompts (#24)
83fe6f2 fix: finalize 按 review.md 判定 + github.token + SSH nohup 后台 (#23)
218b20b curate: 候选批次（待人工评审） (#21)
ec5f2f1 research: 情报搜索新增候选条目 (#20)
4ce09d0 fix: parse_candidates 定位模型回复区 JSON，防贪婪匹配到提示词回显 (#19)
6b2cf0d fix: codex 候选 JSON 输出到 stderr，run_codex 合并 stdout+stderr 解析 (#18)
a019285 fix: research 改为分支+PR（main 受保护不可直推）；运行前同步 main (#17)
ff47dc0 feat: curate 六阶段流水线（research 采集 + 候选评审 + 人类闸门 + finalize 收录） (#16)
2293660 refactor: worker prompt 移出工作区到系统临时目录；git rm .worker_prompt.md (#15)
15ccb7d worker: 服务器 codex 加工结果（待 review） (#13)
ee08225 fix: dispatch-worker.yml heredoc 缩进导致 YAML 语法错误（workflow 无法注册） (#12)
4f85c16 fix: worker 启动时自动 git pull 同步最新队列 (#11)
---
---
created: 2026-08-03
updated: 2026-08-09
tags: [知识库, 日志]
---

# 变更日志

> 时间倒序排列

## [2026-08-09] ingest | Rust 2025 官方博客：Rust 1.85 版本说明（Move 语义 / Borrow Checker 演进）

- 处理：`references/articles.md` 待处理 → 已收录（编号 15，归属 `expand/thinking/`）
- 新增：[[Rust2024版次的语义收紧与异步闭合]]——Rust 1.85 / 2024 版次判值思考（采集器「Move 语义」标签纠偏；edition ≈ 语义债务清偿机制；unsafe 边界从 lint 升级为语言规则；async closures 补齐「闭包 × 借用 × await」三角；版本号不承载语义里程碑）
- 更新：[[index]]（thinking 段 + 计数 132→133）、[[知识图谱]]（编程语言簇补 Rust 思考节点）、`references/articles.md`（待处理清空 + 编号 15 + 统计 11→12）

## [2026-08-09] ingest | MCP 官方文档：Model Context Protocol 介绍

- 处理：`references/articles.md` 待处理 → 已收录（编号 14）
- 新增：[[MCP协议标准化的增量与边界]]——expand/thinking/ 首条独立思考条目（USB-C 类比只到接口层 / 语义适配 M×N / 2026-07-28 版增量：MCP Apps、Agent Skills、Registry、server/discover）
- 更新：[[index]]（thinking 段 + 计数 131→132）、[[知识图谱]]（AI 主题簇补 MCP 思考节点）、[[ECC]]（相关条目回链）

## [2026-08-09] maintenance | 素材层迁移：raw/ → references/raw/ + working/ + Codex 情报追踪

- 迁移：`raw/`（14 个素材）物理移入 `references/raw/`，`references/` 成为 Phase 0 顶层（素材库 + 去重索引）
- 新增：`references/agents.md`——references 层规则（raw 素材状态机 + articles.md 去重权威双层约定）
- 新增：`references/articles.md`——文章去重索引表（模板，`scripts/retrack.py --list/--url` 查询）
- 新增：`working/` + `working/AGENTS.md`——Phase 4 作品输出层（译文/工具/模板，可独立理解）
- 新增：`scripts/retrack.py`——文章去重权威查询 CLI
- 更新：`scripts/check_consistency.py` K1 改为检查 `references/raw/` 状态机
- 更新：`scripts/collect.py` existing_urls 合并 `references/articles.md` URL 作为去重输入
- 更新：`scripts/ingest.py` build_prompt 注入 `{art_titles}`（references/articles.md 去重权威段）
- 更新：9 个脚本 + codex_task.ps1 + 2 个 workflow（collect.yml / ingest.yml）+ pre-commit 的 `raw/` 路径批量改为 `references/raw/`
- 新增：`.github/workflows/research.yml` + `prompts/deep-research-tracker.md`——Codex 情报追踪自动化（三层 prompt：广度/分析/注入，术语每周 1-2 次）
- agents.md 目录结构同步（raw/ 迁入 references/、新增 working/、Phase 0-4 映射表）

## [2026-08-09] maintenance | prompts/ 有效提示词积累目录落地

- 新增：`prompts/AGENTS.md`——目录规则（只收录验证有效的提示词，两种形态，效果评价闭环）
- 新增：`prompts/ingest.md`——ingest 深度加工提示词沉淀（权威源 `scripts/ingest.py:176`，含质量门槛/skip/补充溯源设计说明）

codex
已核对知识库现状（`references/articles.md` 15 条、`expand/thinking/` 2 条、`expand/06-AI与LLM/` 9 条、待处理队列 7 条）与 `research.py` 的三档分流逻辑。以下为完整分析。

## 1. 优先级排序

两条候选均为 AI Agent 域高价值内容，且与既有内容互补而非重复；跨平台侧无达标候选（不硬凑）。

| 优先级 | 候选 | 星级 | 与已收录/已跟踪内容的互补 | 对既有洞见的验证/挑战 | 对开放问题的回答 |
|---|---|---|---|---|---|
| 1 | Snowflake data-eng-bench | ⭐⭐⭐⭐⭐ | 编号 01–05 是任务级/领域级基准（模仿学习、HPO、文档抽取、战术推理、方程发现），**缺仓库级工程基准**；`ECC.md` 明确写着「盲区：缺少公开评测数据」，本候选直接补上 | **验证** `ECC.md`「harness 是工程化主战场」论点：harness 对质量差约 4pp、对成本差 3.9x，实证化「harness 操作系统」假设；同时**挑战**「选对模型即够用」的默认认知 | 正面回答「Agent 评测：model/harness 组件级归因」——给出 harness×model 双变量矩阵 |
| 2 | Simon Willison LLM 0.32 | ⭐⭐⭐⭐ | 待处理队列中的 Claude context engineering（prompt/上下文侧）与 Duolingo 平台案例（组织侧）均不覆盖**工具链与日志架构**；与 `MCP协议标准化的增量与边界`（thinking）形成「平台工具 ↔ 协议总线」对照 | **验证** MCP 思考条目的「外部能力总线」论点：llm-anthropic 0.26 的 `AnthropicMCP` 把 MCP 调用做成单请求服务端工具 | 部分回答「上下文/记忆策略的可复现实践」与「跨模型可移植性」两个缺口 |

与待处理队列关系：data-eng-bench 是 Harness-R1 / EvolveNet（harness 自我演进）所需要的**度量基底**；LLM 0.32 与 Raccoon Heist（同为 Simon Willison）主题不同，不构成重复采集。

## 2. 缺口分析

**被覆盖的缺口**
- Agent 评测组件级归因：harness×model 矩阵 + Pass@1/Pass^3 + 每试成本/token/工具调用/agent 步数，是目前唯一直接命中该缺口的素材。
- Agent harness 行为正确性与覆盖率：103 任务仓库级 dbt DAG（中位 4 个模型、最多 42 个）+ 每任务 10–50 条隐藏断言、整管道全对才计分，把「生成像样模型」与「管道正确」分开。
- 上下文/记忆可复现实践（部分）：内容寻址消息存储（Git 式）解决多轮日志膨胀；推理轨迹 stderr 分流是可复制的工具链标准做法。
- 跨模型可移植性（部分）：`llm openai endpoint` + `llm-chat-completions-server` 提供单命令对接任意 OpenAI 兼容端点的迁移路径。
- 成本数据（部分）：每试成本 0.358–0.756 美元、成本倍数 3.9x/1.5x，可作中小团队选型锚点（非完整案例，故算部分覆盖）。

**仍未触及的缺口**
- 多智能体编排反模式与成本：搜索仅触及 survey（`Multi-Agent Debate Strategies`），未入选。
- Harness/控制的激活策略（always-on / per-commit / conditional / human-summoned）。
- Agent 安全审计（轨迹违规、多智能体信息流、工具权限边界）。
- KMP / Compose Multiplatform 与 Flutter 架构选型、共享逻辑边界、工具链痛点。
- 跨平台 CI / 发布 / 性能基线。
- 衍生新缺口：data-eng-bench 只归因 harness 与 model 两变量，「环境/仓库规模」维度（数据仓库拓扑对结果的影响）未展开，可作后续追踪方向。

## 3. 趋势信号

- **Harness 效应实证化**：评测开始把 harness 作为独立变量（质量差 ~4pp、成本差 ~3.9x），与 `ECC.md` 的 harness 层论点一致；但 CoCo 的胜出提示「域原生 harness」比「通用分层 harness」更优——这是对 ECC 通用化路线的一个温和修正信号。
- **可靠性指标标准化**：Pass@1（单次）与 Pass^3（三试全过）并列披露，把 agent 非确定性显式化，呼应本库对 agent 可靠性的关注。
- **服务端工具 + 推理轨迹成为一等公民**：OpenAI `CodeInterpreter`/`WebSearch`、Anthropic `WebFetch`/`CodeExecution`/`AnthropicMCP` 表明工具托管在向 provider 侧迁移，与 MCP 的「协议分发」形成**双轨并存**（服务端托管 vs 外部工具总线），MCP 思考条目可据此补充对照。
- **Agent 对话日志架构化**：内容寻址日志（仿 Git）把「每条请求携带全量历史」的日志膨胀作为一等工程问题解决，是可复现的记账方案。
- **跨平台窗口偏薄**：两周内 KMP/Flutter 侧以 hotfix（Flutter 3.44.9）与营销内容为主，KotlinLLM 是 Kotlin/JVM 研究而非 KMP 域，未出现可收录级动态——建议下轮把 Compose Multiplatform 1.11.0、Kotlin 2.3.20 工具链作为定向搜索目标验证（本次两者仅侧面出现）。

## 4. 收录建议

| 候选 | verdict | lineage | 一句话理由 |
|---|---|---|---|
| Snowflake data-eng-bench | `index` | `agent/eval` | 首个仓库级 dbt agent 基准，harness×model 双变量质量/成本/可靠性归因数据开源，直接填「Agent 评测归因」与 `ECC.md` 缺公开评测数据的空白，建议随收录生成 `expand/06-AI与LLM/Agent研究与评测/` 条目并与 ECC、待处理 Harness-R1/EvolveNet 建立关联 |
| Simon Willison LLM 0.32 | `index` | `agent/platform` | Tier1 作者的工具链可复现实践（推理轨迹分流、内容寻址日志、服务端工具、任意兼容端点），补上下文日志与跨模型可移植性缺口；release notes 形态不值得整体翻译，索引核心实践即可 |

两者均不选 `translate`：data-eng-bench 价值在数据与归因结论（索引 + expand 加工吸收效率更高），LLM 0.32 为发布说明型长文（已有 7 条待处理翻译在队列，且同作者 Raccoon Heist 已在队列）；`observe` 也不适用——两条都有明确的可落地增量。

```json
{
  "analysis": {
    "priority": [
      "data-eng-bench 最高优先：首个仓库级 dbt agent 基准，harness×model 双变量归因 + 成本/可靠性数据，直接补 Agent 评测归因与 ECC 缺公开评测数据的空白",
      "LLM 0.32 次优：Tier1 作者可复现工具链实践（推理轨迹分流、内容寻址日志、服务端工具、任意兼容端点），补上下文日志与跨模型可移植性缺口",
      "跨平台窗口内无达标内容（KotlinLLM 为 Kotlin/JVM 研究、Flutter 3.44.9 为 hotfix），不硬凑；两条候选均为 AI Agent 域"
    ],
    "gaps_covered": [
      "Agent 评测组件级归因：data-eng-bench 的 harness×model 矩阵（Pass@1/Pass^3/每试成本/token/工具调用/步数）",
      "Agent harness 行为正确性与覆盖率：10–50 条隐藏断言整管道计分 + 103 任务仓库级 DAG 验证",
      "上下文/记忆可复现实践（部分）：LLM 0.32 内容寻址消息存储与推理轨迹 stderr 分流",
      "跨模型可移植性（部分）：llm openai endpoint + chat-completions-server 单命令对接任意兼容端点",
      "成本数据（部分）：每试成本与 3.9x/1.5x 成本倍数可作中小团队选型锚点"
    ],
    "gaps_open": [
      "多智能体编排反模式与成本（仅触及 survey，未入选）",
      "Harness/控制激活策略（always-on/per-commit/conditional/human-summoned）",
      "Agent 安全审计（轨迹违规、多智能体信息流、工具权限边界）",
      "KMP/Compose Multiplatform 与 Flutter 架构选型、共享逻辑边界、工具链痛点",
      "跨平台 CI/发布/性能基线",
      "data-eng-bench 未展开的『环境/仓库规模』维度归因"
    ],
    "trends": [
      "harness 效应实证化：评测把 harness 作为独立变量（质量差~4pp、成本差~3.9x），验证 ECC 论点并提示域原生 harness 专业化方向",
      "可靠性指标标准化：Pass@1 与 Pass^3 并列披露，把 agent 非确定性显式化",
      "服务端工具 + 推理轨迹成为一等公民，与 MCP 外部工具总线形成双轨并存",
      "Agent 对话日志架构化：内容寻址（Git 式）日志成为多轮记账的可复现方案",
      "跨平台两周窗口偏薄，Compose Multiplatform 1.11.0 / Kotlin 2.3.20 待下轮定向验证"
    ]
  },
  "candidates": [
    {
      "title": "Introducing Data-eng-bench: Why You Need \"Data-Native\" Harnesses for Data Engineering",
      "url": "https://www.snowflake.com/en/blog/engineering/data-eng-bench-data-engineering-agent-benchmark/",
      "verdict": "index",
      "lineage": "agent/eval",
      "reason": "首个仓库级 dbt agent 基准，harness×model 双变量质量/成本/可靠性归因数据开源，直接补 Agent 评测归因与 ECC 缺公开评测数据的空白",
      "stars": 5
    },
    {
      "title": "New release of LLM adds support for reasoning traces, OpenAI Responses, server-side tools, and smarter logging",
      "url": "https://simonwillison.net/2026/Aug/4/new-release-of-llm/",
      "verdict": "index",
      "lineage": "agent/platform",
      "reason": "Tier1 作者对 agent 工具链的可复现工程实践（推理轨迹分流、内容寻址日志、服务端工具、任意兼容端点），补上下文日志与跨模型可移植性缺口",
      "stars": 4
    }
  ]
}
```
tokens used
50,072
