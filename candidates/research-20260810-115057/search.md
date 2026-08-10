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
session id: 019fe9cb-87b4-7791-b894-a5148cab3725
--------
user
# 技术情报搜索（Prompt A）

> 运行器：服务器 codex，由 `research.py` 第一段调用。只负责**搜索素材**，不做三档分流。

你是技术情报分析师。搜索以下领域过去 2 周（2026-07-27 ~ 2026-08-10）的高质量内容。

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

## 输出（每条；最多 2；未达门槛勿输出）

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

warning: Codex could not find bubblewrap on PATH. Install bubblewrap with your OS package manager. See the sandbox prerequisites: https://developers.openai.com/codex/concepts/sandboxing#prerequisites. Codex will use the bundled bubblewrap in the meantime.
warning: Model metadata for `deepseek-v4-flash` not found. Defaulting to fallback metadata; this can degrade performance and cause issues.
codex
我先检查环境：确认 Firecrawl CLI 可用性、读取去重列表。
exec
/bin/bash -lc 'which firecrawl; firecrawl --help 2>&1 | head -50' in /root/note-worker
 succeeded in 106ms:
Usage: firecrawl [options] [command]

CLI tool for Firecrawl web scraping

Options:
  -V, --version                                output the version number
  -k, --api-key <key>                          Firecrawl API key (or set FIRECRAWL_API_KEY env var)
  --api-url <url>                              API URL (or set FIRECRAWL_API_URL env var)
  --status                                     Show version, auth status, concurrency, and credits
  -h, --help                                   display help for command

Commands:
  scrape [options] [urls...]                   Scrape one or more URLs. Multiple URLs are scraped concurrently and saved to .firecrawl/
  crawl [options] [url-or-job-id]              Crawl a website using Firecrawl
  map [options] [url]                          Map URLs on a website using Firecrawl
  parse [options] <file>                       Parse a local file (HTML, PDF, DOCX, DOC, ODT, RTF, XLSX, XLS) into markdown, HTML, links, JSON, and more. Uses /v2/parse.
  monitor                                      Schedule recurring scrapes/crawls/searches and track content changes
  search [options] <query>                     Search the web using Firecrawl
  developer [options] <query>                  Search an index built for coding agents: GitHub issues, merged PRs, repository READMEs, and curated documentation sites. Use it for a programming question: code behaviour, a library or framework, an API contract, an error message, or a known bug. Returns ranked results with id, type, url, title, and the matched passages in markdown.
  research                                     Research arXiv papers and GitHub history using Firecrawl
  feedback [options] <endpoint> <jobId>        Send feedback on a Firecrawl endpoint job.
  search-feedback [options] <searchId>         Send feedback on a previous search result. Refunds 1 credit on first submission.
  agent [options] <prompt-or-job-id>           Run an AI agent to extract data from the web
  interact [options] [args...]                 Interact with a scraped page in a live browser session. Run AI prompts or execute code against any previous scrape.
  experimental|x                               Experimental commands (download)
  config [options]                             Configure Firecrawl (login if not authenticated)
  view-config                                  View current configuration and authentication status
  login [options]                              Login to Firecrawl (alias for config)
  logout                                       Logout and clear stored credentials
  init [options] [template]                    Set up Firecrawl: install CLI, authenticate, add integrations, and scaffold a template
  setup [options] [subcommand]                 Set up individual firecrawl integrations (skills, workflows, mcp, defaults)
  make [options] <target>                      Make Firecrawl the default provider for supported workflows
  launch|launcher [options] [agent] [args...]  Configure Firecrawl MCP for an AI agent, then launch it
  env [options]                                Pull FIRECRAWL_API_KEY into a local .env file
  credit-usage [options]                       Get team credit usage information
  doctor [options] [job-id]                    Run environment diagnostics, or diagnose a specific run by job ID
  version [options]                            Display version information
  help [command]                               display help for command

exec
/bin/bash -lc 'ls /root/note-worker; ls /root/note-worker/scripts 2>/dev/null | head' in /root/note-worker
 succeeded in 0ms:
LICENSE
README.md
agents.md
assets
candidates
docs
expand
prompts
references
scripts
templates
wiki
working
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

exec
/bin/bash -lc 'cd /root/note-worker && python scripts/retrack.py --list 2>&1 | head -60' in /root/note-worker
 succeeded in 0ms:
/bin/bash: line 1: python: command not found

exec
/bin/bash -lc 'cd /root/note-worker && cat prompts/ 2>/dev/null; ls prompts working wiki docs 2>/dev/null | head -40' in /root/note-worker
 succeeded in 0ms:
docs:
superpowers

prompts:
AGENTS.md
curate-review.md
curate.md
deep-research-tracker.md
feedback
ingest.md
research-search.md
research-tracker.md
worker.md

wiki:
01-编程语言
02-前端
03-后端
04-数据库
05-数据结构与算法
06-AI与LLM
07-Linux与工具链
08-逆向与安全
09-源码解读
10-求职面试
11-生活杂项
opencode项目解读

working:
AGENTS.md

exec
/bin/bash -lc 'cd /root/note-worker && python3 scripts/retrack.py --list 2>&1 | head -80' in /root/note-worker
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
/bin/bash -lc 'cd /root/note-worker && cat prompts/research-search.md 2>/dev/null | head -80' in /root/note-worker
 succeeded in 0ms:
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

codex
环境确认：Firecrawl CLI 可用，去重列表已读取。现在用 Firecrawl 执行多轮搜索。
exec
/bin/bash -lc 'firecrawl search --help 2>&1 | head -40' in /root/note-worker
 succeeded in 111ms:
Usage: firecrawl search [options] <query>

Search the web using Firecrawl

Arguments:
  query                       Search query

Options:
  --limit <number>            Maximum number of results (default: 5, max: 100)
  --sources <sources>         Comma-separated sources to search: web, images,
                              news (default: web)
  --categories <categories>   Comma-separated categories to filter: github,
                              research, pdf, developer (developer searches
                              indexed GitHub issues, merged PRs, READMEs, and
                              docs)
  --tbs <value>               Time-based search: qdr:h (hour), qdr:d (day),
                              qdr:w (week), qdr:m (month), qdr:y (year)
  --location <location>       Location for geo-targeting (e.g., "Germany", "San
                              Francisco,California,United States")
  --country <code>            ISO country code for geo-targeting (default: US)
  --timeout <ms>              Timeout in milliseconds (default: 60000)
  --ignore-invalid-urls       Exclude URLs invalid for other Firecrawl endpoints
                              (default: false)
  --highlights                Return query-relevant highlights for each search
                              result
  --no-highlights             Keep the original search snippets instead of
                              returning highlights
  --scrape                    Enable scraping of search results (default: false)
  --scrape-formats <formats>  Comma-separated scrape formats when --scrape is
                              enabled: markdown, html, rawHtml, links, etc.
                              (default: markdown)
  --only-main-content         Include only main content when scraping (default:
                              true)
  -k, --api-key <key>         Firecrawl API key (overrides global --api-key)
  --api-url <url>             API URL (overrides global --api-url)
  -o, --output <path>         Output file path (default: stdout)
  --json                      Output as compact JSON (default: false)
  -h, --help                  display help for command

exec
/bin/bash -lc 'firecrawl --status 2>&1 | head -20' in /root/note-worker
 succeeded in 1686ms:

  [38;5;208m🔥 [1mfirecrawl[0m [2mcli[0m [2mv1.19.30[0m

  [32m●[0m Authenticated [2mvia FIRECRAWL_API_KEY[0m
  [2mConcurrency:[0m 0/2 jobs [2m(parallel scrape limit)[0m
  [2mCredits:[0m 1,019 / 1,000 [2m(102% left this cycle)[0m
  [2m.firecrawl:[0m present [2m- 0 sites[0m
  [2m.gitignore:[0m present [2m- .firecrawl ignored: yes[0m


codex
Firecrawl 已认证。开始多轮搜索，限定近一月窗口。
exec
/bin/bash -lc 'firecrawl search "agent harness orchestration context engineering 2026" --limit 10 --tbs qdr:m --json 2>/dev/null | head -c 6000' in /root/note-worker
exec
/bin/bash -lc 'firecrawl search "langchain4j langgraph4j RAG evaluation August 2026" --limit 10 --tbs qdr:m --json 2>/dev/null | head -c 6000' in /root/note-worker
 succeeded in 6430ms:
{"success":true,"data":{"web":[{"url":"https://parallel.ai/articles/what-is-an-agent-harness","title":"What is an agent harness?","description":"# \\# What is an agent harness?\nAn agent harness is the layer around a model that manages tools, memory, and orchestration, and it explains why the same model performs differently in different products.\n\n## \\## How does an agent harness work?\n1. ****Intent capture & orchestration:**** First, the user’s request or high-level goal is captured. Often an __orchestrator__ (another component of the system) will break this goal into sub-tasks or decide on a sequence of actions the AI should take. The harness works closely with this orchestrator by providing it the means to execute those actions. For example, the orchestrator might prompt the model for a plan or next step; the harness then ensures the model gets any needed context or tools at that step.\n\n## \\## Key components and features of agent harnesses\n- - ****Context engineering & prompt management:**** Feeding the right prompt to the model is a science in itself. Harnesses perform context engineering, deciding what information to include or exclude at each model call. This involves techniques like __context isolation__ (keeping different subtasks separate so they don’t confuse each other), __context reduction__ (dropping or compressing irrelevant info to avoid context rot), and __context retrieval__ (injecting fresh info such as documentation or search results at the right time). The harness may have modules that dynamically retrieve documents (RAG systems), or that rewrite the prompt for the first run versus subsequent runs (Anthropic describes using “a different prompt for the very first context window” in their harness structure to initialize things properly). All of this falls under the harness’s responsibility, ensuring the model is __prompted optimally__ at each step.\n\n## \\## Harness vs. orchestration vs. framework: Clarifying the stack\nIt’s useful to distinguish an AI harness from related concepts like __agent frameworks__ and __orchestrators__, since these terms can overlap:","position":1},{"url":"https://github.com/ai-boost/awesome-harness-engineering","title":"ai-boost/awesome-harness-engineering","description":"# Awesome Harness Engineering\n## Foundations\n- [Supercharge Your AI Agents: The New ADK Integrations Ecosystem](https://developers.googleblog.com/en/supercharge-your-ai-agents-adk-integrations-ecosystem/) — Google's 2026 update to Agent Development Kit expanding the ecosystem integrations (Hugging Face, GitHub, Daytona, Notion, etc.) and providing reference patterns for how orchestration harnesses wire external services without losing determinism or state coherence.\n- [Harness Engineering: Structured Workflows for AI-Assisted Development](https://developers.redhat.com/articles/2026/04/07/harness-engineering-structured-workflows-ai-assisted-development) — Red Hat's enterprise perspective on harness engineering (April 7, 2026): AI writes better code when you design the environment it works in. Emphasizes structured context over free-form tickets, expanding the agent's toolbox through MCP integrations (CI status, deployment logs, runtime metrics) as real data sources, and a four-pillar model (vibes, specs, skills, agents) for organizing how humans and agents collaborate.\n- [A Practical Guide to Building AI Agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/) — OpenAI's April 2026 comprehensive guide distilling production deployment patterns into actionable best practices: single-agent vs. multi-agent orchestration (manager vs. decentralized handoffs), tool design for many-to-many agent-tool relationships, and layered guardrail patterns combining input validation, output filtering, tool-risk ratings, and human-intervention triggers.\n\n## Design Primitives\n### Task Runners & Orchestration\n- [Building a C Compiler with a Team of Parallel Claudes](https://www.anthropic.com/engineering/building-c-compiler) — Anthropic's account of coordinating 16 Claude instances in parallel on a shared git repo without a central orchestrator: agents claim tasks via files in `current_tasks/`, git forces collision resolution naturally, and a continuous restart loop spawns fresh sessions that resume where predecessors left off. Key harness lesson: verbose test output pollutes agent context — the feedback loop must emit only a few summary lines, log detail to file.\n- [LangGraph](https://github.com/langchain-ai/langgraph) — Graph-based state machine framework for multi-agent harnesses: models supervisor/subagent topologies, error-recovery branches, and checkpoint persistence as first-class primitives. The most widely adopted harness orchestration layer in production. ![Stars](https://camo.githubusercontent.com/c6c2bd861e48586569c1b6e63388caeed9191b7168839bd117a48197fe67bc78/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f73746172732f6c616e67636861696e2d61692f6c616e6767726170683f7374796c653d666c61742d737175617265266c6162656c3d25453225393825383526636f6c6f723d79656c6c6f77)\n- [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) — Lightweight multi-agent framework built around handoffs and guardrails; the production successor to Swarm. Complements LangGraph for harnesses where delegation patterns are simpler than full graph orchestration. ![Stars](https://camo.githubusercontent.com/9ceac5fd149cd031fd7037b1825ee383a3e5d6bf185964c3466f6fb07a7a8f47/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f73746172732f6f70656e61692f6f70656e61692d6167656e74732d707974686f6e3f7374796c653d666c61742d737175617265266c6162656c3d25453225393825383526636f6c6f723d79656c6c6f77)\n- [Codex SDK](https://developers.openai.com/codex/sdk) — OpenAI's official SDK for programmatically controlling local Codex agents from TypeScript or Python: start threads, run prompts, resume sessions, and choose sandbox presets (
 succeeded in 20192ms:
{"success":true,"data":{"web":[{"url":"https://atlan.com/know/ai-agent/knowledge-graph/neo4j-graphrag-vs-llamaindex-vs-langchain/","title":"Neo4j GraphRAG vs. LlamaIndex vs. LangChain","description":"# Neo4j GraphRAG vs. LlamaIndex vs. LangChain Graph Transformer\n## Neo4j GraphRAG vs. LlamaIndex vs. LangChain: what's the difference?\n### The three approaches include:\n| Dimension | Neo4j GraphRAG | LlamaIndex (PropertyGraphIndex) | LangChain (LLMGraphTransformer) |\n|-|-|-|-|\n| Community signal | 1.2k stars, 457 commits (dated 2026-08-03), narrow by design | 50,531 stars, +15/day (dated 2026-06-30) | 140,570 stars, +46/day, highest delta tracked (dated 2026-06-30) |\n\n## Neo4j GraphRAG vs. LlamaIndex vs. LangChain: head-to-head comparison\n| Dimension | Neo4j GraphRAG | LlamaIndex | LangChain |\n|-|-|-|-|\n| Ecosystem and community size | 1.2k stars, narrow by design (dated 2026-08-03) | 50,531 stars, +15/day (dated 2026-06-30) | 140,570 stars, +46/day (dated 2026-06-30) |","position":1},{"url":"https://aimultiple.com/rag-frameworks","title":"RAG Frameworks: LangChain vs LangGraph vs LlamaIndex","description":"# RAG Frameworks: LangChain vs LangGraph vs LlamaIndex\n## The shared agentic RAG architecture\n### Workflow Examples\n```\n1{\n2      \"question\": \"If a train travels 120 km in 1.5 hours, what is its average speed?\",\n3      \"final_answer\": \"80.0\",\n4      \"answer_is_refusal\": false,\n5      \"answer_grounded\": false,\n6      \"answer_complete\": false,\n7      \"hallucination_detected\": false,\n8      \"tools_used\": [\\\n9        \"calculator\"\\\n10      ],\n11      \"execution_path\": [\\\n12        \"router\",\\\n13        \"calculator\"\\\n14      ],\n15}\n```\n\n## Cite this benchmark\n### BibTeX    For LaTeX documents and academic reference managers.\n```\n@misc{dilmegani2026,\n  author = {Dilmegani, Cem and Sarı, Ekrem},\n  title  = {{RAG Frameworks: LangChain vs LangGraph vs LlamaIndex}},\n  year   = {2026},\n  month  = aug,\n  howpublished    = {\\url{https://aimultiple.com/rag-frameworks}},\n  note   = {AIMultiple. Retrieved August 4, 2026}\n}\n```\n\n## Next to Read\n[Backup & Recovery\\\n\\\nOpen World Evaluation\\\n\\\nAug 4\\\n**Disaster Recovery Benchmark: Acronis vs Comet vs MSP360** \\\n\\\n![Ekrem Sarı](https://aimultiple.com/wp-content/uploads/2025/03/ekrem_sari-removebg-preview-150x150.png.webp)\\\n\\\nEkrem Sarı](https://aimultiple.com/disaster-recovery-solutions)\n\n[RAG\\\n\\\nBenchmark\\\n\\\nAug 4\\\n**Reranker Benchmark: Top 8 Models Compared** \\\n\\\n![Ekrem Sarı](https://aimultiple.com/wp-content/uploads/2025/03/ekrem_sari-removebg-preview-150x150.png.webp)\\\n\\\nEkrem Sarı](https://aimultiple.com/rerankers)","position":2},{"url":"https://www.reddit.com/r/Rag/comments/1vbl7qb/rag_from_scratch_vs_langchain_what_actually/","title":"RAG from scratch vs LangChain — what actually tipped ...","description":"I'm building a RAG pipeline (chunking, embeddings, retrieval) from scratch right now, mostly to understand each step instead of trusting a framework's ...","position":3},{"url":"https://www.linkedin.com/posts/rakesh-minglani-4095aa18_rag-knowledgegraphs-neo4j-activity-7487448656271331328-j0zH","title":"Why Knowledge Graphs Outperform RAG Systems in AI ...","description":"Most RAG systems are built wrong. in 2026, it's hitting a wall—and. Great for massive, fast-changing raw docs, but stateless and loses context.","position":4}]},"id":"019fe9cb-c126-74a8-a414-55069b93150d","creditsUsed":2}

codex
继续搜索跨平台开发与其他信源。
exec
/bin/bash -lc 'firecrawl search "Kotlin Multiplatform Compose Multiplatform release August 2026" --limit 10 --tbs qdr:m --json 2>/dev/null | head -c 5000' in /root/note-worker
exec
/bin/bash -lc 'firecrawl search "Flutter architecture toolchain news August 2026" --limit 10 --tbs qdr:m --json 2>/dev/null | head -c 5000' in /root/note-worker
 succeeded in 3749ms:
{"success":true,"data":{"web":[{"url":"https://www.instagram.com/bytesyntax.dev/reel/Dbvh-EGMsXo/","title":"Flutter 3.44.9 is out — a stable hotfix. If you were debugging an iOS ...","description":"0 likes, 0 comments - bytesyntax.dev on August 7, 2026: \"Flutter 3.44.9 is out — a stable hotfix. If you were debugging an iOS app and it crashed, ...","position":1},{"url":"https://medium.com/@blurbrahlab/chatgpt-is-now-a-login-provider-top-10-ai-flutter-news-august-3-2026-0da6b2bc7cd2","title":"ChatGPT Is Now a Login Provider — Top 10 AI & Flutter ... - Medium","description":"Flutter News August 3, 2026. The biggest architectural shift: ChatGPT on August 26. to the IDE toolchain).","position":2},{"url":"https://www.instagram.com/p/Dbtc4yEOeEr/","title":"Flutter 3.44.9 is now available! The latest stable release ... - Instagram","description":"Flutter 3.44.9 is now available! The latest stable release is here, bringing more polish, reliability and improvements across the Flutter ecosystem.","position":3},{"url":"https://www.instagram.com/reel/DbNZK7As-xf/","title":"Flutter 3.44.8 is out — a stable hotfix. Two fixes worth ... - Instagram","description":"0 likes, 0 comments - bytesyntax.dev on July 25, 2026: \"Flutter 3.44.8 is out — a stable hotfix. Two fixes worth knowing about: • Builds on macOS/iOS ...","position":4},{"url":"https://www.linkedin.com/posts/amorna_googleioextended-ioextendedbangkok-flutter-activity-7484928318040068098-z837","title":"Optimizing Flutter with Rust at Google I/O Extended Bangkok","description":"Flutter team released their 2026 roadmap. Flutter is moving toward AI-generated interfaces and making Dart work across the full stack.","position":5},{"url":"https://www.instagram.com/reel/Dbc9HnzBngG/","title":"Want this Flutter package? Comment “SRC” below and I ... - Instagram","description":"Want to Build Apps Like These? Good news. Watch the full Flutter setup tutorial on the channel and start building your first app today. #flutter #flutterdev # ...","position":6},{"url":"https://www.automotivelinux.org/","title":"Automotive Grade Linux","description":"AGL releases open source SoDeV reference platform for SDVs and welcomes five new members.\n\nSearch\n\n## **Now Available: AGL SoDeV**\nApply to be included in the Vendor Marketplace. [**SUBMIT**](https://www.automotivelinux.org/vendor-marketplace-2/)","position":7},{"url":"https://www.facebook.com/WordPress/posts/bo-english-wiczling-will-keynote-wordcamp-us-2026-in-phoenix-on-monday-august-17/1431229148816720/","title":"Bo English-Wiczling will keynote WordCamp US 2026 in Phoenix on ...","description":"Bo English-Wiczling will keynote WordCamp US 2026 in Phoenix on Monday, August 17. You're not just learning React, Node, or Flutter.","position":8},{"url":"https://labusa.com/insight/ai-assisted-flutter-mobile-development","title":"Building an AI-Assisted Mobile Engineering Capability - LABUSA","description":"An executive case study on how LABUSA built reusable engineering standards and AI tooling for mobile applications it deliberately does not own.","position":9},{"url":"https://www.goodbarber.com/blog/best-app-builders-for-mobile-apps-a-guide-for-2025-a1419/","title":"The 10 Best No-Code App Builders in 2026 review - GoodBarber","description":"# The 10 best No-Code App Builders in 2026\n## Flutterflow\n06\n\n120 / 170\n\n- Canvas performance degraded noticeably past a dozen screens: \"transitions stuttering and undo operations hesitating\" — an editor cost that compounds with project scope.\n- No CMS found: \"There is simply no content management interface in FlutterFlow — the canvas is built for development, not for daily content operation.\" Publishing new AURORA destinations required returning to the canvas.\n\nFlutterFlow generates real Flutter code that compiles to native iOS, Android, web, and desktop.\n\n### 17-criterion assessment\n| Criterion | Score /10 | Assessment |\n|-|-|-|\n| **Security** | 7 | Firebase-based auth (Google infrastructure). Enterprise SSO via Firebase Auth or custom providers. Standard GDPR configuration. |\n| **Scalability** | 8 | Flutter output performs natively. Firebase and Supabase backends scale well. Code export lets teams manage scaling independently. |\n| **Open Source** | 8 | Code export is FlutterFlow's signature differentiator — generated Flutter code is fully exportable. Flutter itself is open-source (Google). |\n| **Low-code vs. No-code** | 5 | Visual builder accessible to non-developers for simple apps. Understanding Flutter's widget model is required for anything beyond basic screens — this is low-code in practice. |\n| **AI Integration** | 7 | FlutterFlow Copilot generates UI and logic from natural language prompts. AI Action node for integrating OpenAI and other LLMs into app logic. Well-integrated native AI features. |\n| **Integrations** | 8 | Firebase (Firestore, Auth, Storage, Functions), Supabase, custom REST APIs, GraphQL. Stripe, RevenueCat for monetization. 
 succeeded in 4485ms:
{"success":true,"data":{"web":[{"url":"https://blog.jetbrains.com/kotlin/category/multiplatform/","title":"Multiplatform - Kotlin - The JetBrains Blog","description":"Compose Multiplatform 1.11.0 has been released with improvements to the iOS and web experience and a refreshed approach to UI testing.","position":1},{"url":"https://kotlinlang.org/lp/shipaton/","title":"Ship Kotlin Everywhere Award | Shipaton 2026","description":"# Ship Kotlin Everywhere\n## Recommended stack\n[Compose Multiplatform](https://www.jetbrains.com/compose-multiplatform/)","position":2},{"url":"https://www.decipherzone.com/blog-detail/cross-platform-development-trends","title":"Cross-Platform Development Trends to Watch in 2026 - Decipher Zone","description":"Compose Multiplatform for iOS reached stable status in May 2025 with version 1.8.0. That milestone means teams can now share actual screens, not just logic, ...","position":3},{"url":"https://www.nibblesoftware.com/flutter-vs-react-native-vs-kotlin-multiplatform/","title":"Flutter vs React Native vs Kotlin Multiplatform: 2026 - Nibble Software","description":"# Flutter vs React Native vs Kotlin Multiplatform: What to Choose in 2026?\n## Kotlin Multiplatform (KMP) in 2026: The Native Bridge Gets Serious\n### The 2026 KMP landscape\n1. **Compose Multiplatform for iOS (Beta with production apps).** You can now write shared UI in Compose that runs natively on both Android and iOS. While still not as polished as Jetpack Compose on Android, it’s stable enough for production apps that are willing to invest in fine-tuning platform-specific UI.","position":4},{"url":"https://www.coderio.com/blog/software-development/swift-vs-kotlin-native-app-development/","title":"Swift vs Kotlin for Native App Development: Complete 2026 Guide","description":"The tooling has matured substantially: the Kotlin Multiplatform plugin for Android Studio and Xcode, the Compose Multiplatform framework for shared UI on non- ...","position":5},{"url":"https://ktor.io/docs/releases.html","title":"Ktor releases | Ktor Documentation","description":"Release details﻿. The following table lists details of the latest Ktor releases. Version. Release Date. Highlights. 3.5.2. August 4, 2026. A patch release ...","position":6},{"url":"https://kotlinlang.org/docs/multiplatform/compose-desktop-top-level-windows-management.html","title":"Top-level windows management | Kotlin Multiplatform Documentation","description":"Compose Multiplatform for desktop provides various features for managing windows. You can hide windows in the tray, make them draggable, adapt their size, ...","position":7},{"url":"https://www.threads.com/@githubprojects/post/DbIxpu2mzhE/people-in-space-is-a-kotlin-multiplatform-project-that-shares-a-single-codebase/","title":"PeopleInSpace is a Kotlin Multiplatform project that shares a single ...","description":"PeopleInSpace is a Kotlin Multiplatform project that shares a single codebase across Android, iOS, Wear OS, Desktop, Web, and an MCP server. - SwiftUI, Jetpack ...","position":8},{"url":"https://johnoreilly.dev/posts/galwaybus-scan-stop-kmp/","title":"Scanning bus stop codes with ML Kit and Vision in the GalwayBus ...","description":"Scanning bus stop codes with ML Kit and Vision in the GalwayBus Compose Multiplatform app. Posted on August 7, 2026 ... It's all written in Kotlin against the ...","position":9},{"url":"https://github.com/chrisbanes/skills","title":"GitHub - chrisbanes/skills: Skills for Kotlin, Jetpack Compose, and ...","description":"Release versions use SemVer-compatible CalVer: YYYY.M.D without zero-padded month or day values, for example 2026.6.17 . Keep .claude-plugin/plugin.json ...","position":10,"category":"github"}]},"id":"019fe9cc-170a-71cb-9d79-efaf4c87da5d","creditsUsed":2}

codex
发现几个候选。继续挖掘 JetBrains 发布博客与 Tier 1 信源。
exec
/bin/bash -lc 'firecrawl search "Compose Multiplatform 1.11.0 release blog jetbrains" --limit 8 --tbs qdr:m --json 2>/dev/null | head -c 5000' in /root/note-worker
exec
/bin/bash -lc 'firecrawl search "Anthropic engineering blog agents August 2026" --limit 8 --tbs qdr:m --json 2>/dev/null | head -c 5000' in /root/note-worker
 succeeded in 5343ms:
{"success":true,"data":{"web":[{"url":"https://www.aisi.gov.uk/blog/incident-report-unsanctioned-agent-behaviour-during-cyber-testing","title":"Incident Report: unsanctioned agent behaviour during cyber testing","description":"AISI identified an incident in which AI agents took sustained, unsanctioned action directed at real people and organisations. Anthropic's Mythos","position":1},{"url":"https://www.herohunt.ai/blog/how-to-recruit-ai-agent-engineers-in-2026/","title":"How to Recruit AI Agent Engineers in 2026 - HeroHunt.ai","description":"A practical 2026 guide to recruiting AI agent engineers: what the role is, where to source them, how to screen without code, comp benchmarks, and the tools.","position":2},{"url":"https://pub.towardsai.net/how-id-learn-to-build-ai-agents-in-2026-the-8-week-path-2323d654ea46","title":"How I'd Learn to Build AI Agents in 2026 (The 8-Week Path)","description":"The explanatory guide for persistent memory, multi-agent orchestration, token budgeting, and production-ready Claude Code projects.","position":3},{"url":"https://www.aibuilderclub.com/blog/graph-engineering-with-claude-code","title":"Graph Engineering with Claude Code: Anthropic's Agent Graph","description":"'Graph engineering' surfaced on X in mid-July 2026; the Claude Code and Claude Agent SDK capabilities described here are drawn from Anthropic's official docs ...","position":4},{"url":"https://www.truefoundry.com/blog/graph-engineering-enterprise-guide","title":"Graph Engineering for Multi-Agent Systems - Truefoundry","description":"# Graph Engineering for Multi-Agent Systems: Architecture, Governance, and Observability\n## Recent Blogs\n[![](https://cdn.prod.website-files.com/6295808d44499cde2ba36c71/6a6d1376b8d66c96d640e52a_Screenshot%202026-08-01%20at%202.58.20%E2%80%AFAM.png)\\\n\\\n**Agno Alternatives: Top 5 Options for 2026** \\\n\\\nAugust 3, 2026\\\n\\\nSahajmeet Kaur](https://www.truefoundry.com/blog/agno-alternatives)","position":5},{"url":"https://www.crossmint.com/learn/ai-agent-conference-calendar","title":"AI Agent Conference Calendar 2026 & 2027 - Crossmint","description":"The most comprehensive AI agent conference calendar for 2026. Speakers come from OpenAI, Anthropic, LangChain, Berkeley Agentic AI Summit 2026 | August 1-2, ...","position":6},{"url":"https://www.anthropic.com/news/claude-opus-5","title":"Introducing Claude Opus 5 - Anthropic","description":"Opus 5 is a step change improvement for the Opus tier powering long-running agents while delivering improvements in coding and professional work.","position":7},{"url":"https://socket.dev/blog/ai-agent-open-source-malware","title":"UK Cyber Test: AI Agent Attempted to Social Engineer Open So...","description":"An AI agent powered by Anthropic's Mythos 5 created a malicious pull request, fabricated identities, targeted open source maintainers, and planted instructions ...","position":8}]},"id":"019fe9cc-3894-72fa-b6ce-a87edb7af5ce","creditsUsed":2}

 succeeded in 6626ms:
{"success":true,"data":{"web":[{"url":"https://blog.jetbrains.com/kotlin/category/multiplatform/","title":"Multiplatform - Kotlin - The JetBrains Blog","description":"Compose Multiplatform 1.11.0 has been released with improvements to the iOS and web experience and a refreshed approach to UI testing.","position":1},{"url":"https://developer.android.com/jetpack/androidx/releases/compose-runtime","title":"Compose Runtime | Jetpack - Android Developers","description":"This is the first stable release of Compose. Please see the official Compose Release blog for more details! Known Issues. If you are using Android Studio ...","position":2},{"url":"https://kotlinlang.org/docs/multiplatform/multiplatform-add-dependencies.html","title":"Adding dependencies on multiplatform libraries - Kotlin","description":"A Kotlin Multiplatform project can depend on multiplatform libraries that work for all target platforms, platform-specific libraries, and other multiplatform ...","position":3},{"url":"https://developer.android.com/jetpack/androidx/releases/compose-foundation","title":"Compose Foundation | Jetpack - Android Developers","description":"This is the first stable release of Compose. Please see the official Compose Release blog for more details! Known Issues. If you are using Android Studio ...","position":4},{"url":"https://kotlinlang.org/docs/multiplatform/multiplatform-compatibility-guide.html","title":"Compatibility guide for Kotlin Multiplatform","description":"This guide summarizes incompatible changes you might encounter while developing projects with Kotlin Multiplatform. Supported and developed by JetBrains","position":5},{"url":"https://blog.knifelf.club/tag/kmp-tips/page/2/","title":"KMP-Tips - Knifelf Blog (Page 2)","description":"Compose Multiplatform 1.11.0 带来了v2 UI Testing API —— StandardTestDispatcher 成为默认调度器，配合awaitIdle() 让你写出真正可靠的跨平台测试。… KMP 新默认项目 ...","position":6},{"url":"https://developer.android.com/jetpack/androidx/releases/compose-ui","title":"Compose UI | Jetpack - Android Developers","description":"This is the first stable release of Compose. Please see the official Compose Release blog for more details! Known Issues. If you are using Android Studio ...","position":7},{"url":"https://github.com/pkgforge-dev/Termux-Packages","title":"GitHub - pkgforge-dev/Termux-Packages: Markdown List (Table ...","description":"Compose is a tool for defining and running multi-container Docker applications. High-level, multiplatform C++ network packet sniffing and crafting library.","position":8,"category":"github"}]},"id":"019fe9cc-358c-751c-b46b-807b66e591fe","creditsUsed":2}

exec
/bin/bash -lc 'firecrawl search "site:blog.jetbrains.com Compose Multiplatform 1.11.0" --limit 8 --tbs qdr:m --json 2>/dev/null | head -c 4000' in /root/note-worker
exec
/bin/bash -lc 'firecrawl search "langgraph4j OR langchain4j release August 2026" --limit 8 --tbs qdr:m --json 2>/dev/null | head -c 4000' in /root/note-worker
 succeeded in 3942ms:
{"success":true,"data":{"web":[{"url":"https://www.infoq.com/news/2026/07/java-news-roundup-jul13-2026/","title":"Java News Roundup: Value Objects, WildFly 41, TornadoVM ... - InfoQ","description":"LangChain4j The formal release. LangChain4j 1.18.0 provides bug fixes and new features such as: a new Belief-Desire-Intention (BDI) agentic pattern","position":1},{"url":"https://blog.jetbrains.com/idea/2026/08/java-annotated-monthly-august-2026/","title":"Java Annotated Monthly – August 2026 - The JetBrains Blog","description":"Java Annotated Monthly – August 2026. Donald Raab joins us as this month's featured author. A LangChain4j Experiment Conferences and Events","position":2},{"url":"https://www.instagram.com/reel/DbvXNaxNKPu/","title":"¿Cuál es el papel de Java en la era de la IA Generativa y el ...","description":"on August 7, 2026: Artificial Generativa con LangChain4j ya no es hablar del futuro: es hablar del presente. #LangChain4j. August 01, 2026.","position":3},{"url":"https://www.instagram.com/reel/Dbqm1FQyoot/","title":"Did Java just pull off the biggest comeback in tech? We ... - Instagram","description":"... likes, 0 comments - hetish01 on August 5, 2026: \"Did Java just pull off the biggest comeback ... - Point releases of TornadoVM, Apache TomEE, Java Operator SDK ...","position":4},{"url":"https://mvnrepository.com/artifact/io.quarkiverse.langchain4j","title":"io.quarkiverse.langchain4j - Maven Repository","description":"Last Release on Jul 9, 2026. Easy RAG Runtime Last Release on Aug 3, 2026. Indexed Repositories (3352)","position":5},{"url":"https://www.javacodegeeks.com/2026/08/langchain4j-rag-in-java-embedding-chunking-and-retrieval-without-the-python-envy.html","title":"LangChain4j RAG in Java: Embedding, Chunking, and Retrieval ...","description":"A practical pipeline for document ingestion, embedding, and retrieval, all on the JVM, with a Spring AI comparison for good measure.","position":6},{"url":"https://www.infoq.com/articles/self-building-agent-langchain4j/","title":"The Self-Building Agent: a LangChain4j Experiment - InfoQ","description":"An experiment demonstrated that a code assistant using LangChain4j could autonomously design a coding system, effectively rewriting and debugging code","position":7},{"url":"https://www.linkedin.com/pulse/java-ai-revolution-how-transformed-from-enterprise-rama-chandra-rao-zmvpf","title":"The Java AI Revolution: How Java Transformed From Enterprise ...","description":"LangChain4j 1.0 released — enterprise grade Java AI library. Aug 4, 2026 Java + GenAI in 2026: The Generative AI...","position":8}]},"id":"019fe9cc-5fdd-71ea-a403-9211dc605578","creditsUsed":2}

 succeeded in 13524ms:
{"success":true,"data":{"web":[{"url":"https://blog.jetbrains.com/kotlin/category/multiplatform/","title":"Multiplatform - Kotlin - The JetBrains Blog","description":"## Multiplatform\n[![Compose Multiplatform 1.11.0](https://blog.jetbrains.com/wp-content/uploads/2026/05/CMP-releases-BlogFeatured-1280x720-1.png)\\\n**Compose Multiplatform 1.11.0 Is Now Available**\\\n\\\nCompose Multiplatform 1.11.0 has been released with improvements to the iOS and web experience and a refreshed approach to UI testing.\\\n\\\n![Elvira Mustafina](https://blog.jetbrains.com/wp-content/uploads/2023/10/Elvira_Mustafina-50x50.jpg)\\\n\\\nElvira MustafinaMay 15, 2026\\\n\\\n0](https://blog.jetbrains.com/kotlin/2026/05/compose-multiplatform-1-11-0/)","position":1}]},"id":"019fe9cc-5db0-749f-83f1-12e989dce52f","creditsUsed":2}

codex
Compose 1.11.0 是 5 月发布，超出窗口，排除。继续找窗口内内容。
exec
/bin/bash -lc 'firecrawl search "LangChain4j 1.18.0 release BDI agentic pattern" --limit 8 --tbs qdr:m --json 2>/dev/null | head -c 4000' in /root/note-worker
exec
/bin/bash -lc 'firecrawl search "simonwillison.net August 2026" --limit 8 --tbs qdr:m --json 2>/dev/null | head -c 4000' in /root/note-worker
 succeeded in 6276ms:
{"success":true,"data":{"web":[{"url":"https://simonwillison.net/2026/Aug/6/simon-willison-on-technical-blogging/","title":"Simon Willison on Technical Blogging","description":"# [Simon Willison’s Weblog](https://simonwillison.net/)\n6th August 2026 - Link Blog\n\nPosted [6th August 2026](https://simonwillison.net/2026/Aug/6/) at 6:04 pm\n\n## Recent articles\n- [Now we have a timeline of the OpenAI accidental attack against Hugging Face](https://simonwillison.net/2026/Aug/7/openai-timeline/) - 7th August 2026\n- [One-shotting a Raccoon Heist game using Claude Fable 5](https://simonwillison.net/2026/Aug/5/raccoon-heist/) - 5th August 2026\n- [New release of LLM adds support for reasoning traces, OpenAI Responses, server-side tools, and smarter logging](https://simonwillison.net/2026/Aug/4/new-release-of-llm/) - 4th August 2026\n\nThis is a **link post** by Simon Willison, posted on [6th August 2026](https://simonwillison.net/2026/Aug/6/).\n\n### Monthly briefing\n- [2026](https://simonwillison.net/2026/)","position":1},{"url":"https://simonwillison.net/2026/Aug/3/devtools-must-be-open-source-exedev/","title":"Comment: Devtools must be open source (exe.dev)","description":"# [Simon Willison’s Weblog](https://simonwillison.net/)\n3rd August 2026\n\nPosted [3rd August 2026](https://simonwillison.net/2026/Aug/3/) at 3:30 pm\n\n## Recent articles\n- [Now we have a timeline of the OpenAI accidental attack against Hugging Face](https://simonwillison.net/2026/Aug/7/openai-timeline/) - 7th August 2026\n- [One-shotting a Raccoon Heist game using Claude Fable 5](https://simonwillison.net/2026/Aug/5/raccoon-heist/) - 5th August 2026\n- [New release of LLM adds support for reasoning traces, OpenAI Responses, server-side tools, and smarter logging](https://simonwillison.net/2026/Aug/4/new-release-of-llm/) - 4th August 2026\n\nThis is a **beat** by Simon Willison, posted on [3rd August 2026](https://simonwillison.net/2026/Aug/3/).\n\n### Monthly briefing\n- [2026](https://simonwillison.net/2026/)","position":2},{"url":"https://simonwillison.net/2026/Aug/8/john-gruber/","title":"A quote from John Gruber","description":"# [Simon Willison’s Weblog](https://simonwillison.net/)\n8th August 2026\n\n— [John Gruber](https://daringfireball.net/linked/2026/08/07/simon-willison-on-blogging), responding to my [blogging tips](https://simonwillison.net/2026/Aug/6/simon-willison-on-technical-blogging/)\n\nPosted [8th August 2026](https://simonwillison.net/2026/Aug/8/) at 12:10 am\n\n## Recent articles\n- [Now we have a timeline of the OpenAI accidental attack against Hugging Face](https://simonwillison.net/2026/Aug/7/openai-timeline/) - 7th August 2026\n- [One-shotting a Raccoon Heist game using Claude Fable 5](https://simonwillison.net/2026/Aug/5/raccoon-heist/) - 5th August 2026\n- [New release of LLM adds support for reasoning traces, OpenAI Responses, server-side tools, and smarter logging](https://simonwillison.net/2026/Aug/4/new-release-of-llm/) - 4th August 2026\n\nThis is a **quotation** collected by Simon Willison, posted on [8th August 2026](https://simonwillison.net/2026/Aug/8/).\n\n- [2026](https://simonwillison.net/2026/)","position":3},{"url":"https://simonwillison.net/2026/Aug/4/llm/","title":"Release: llm 0.32","description":"# [Simon Willison’s Weblog](https://simonwillison.net/)\n4th August 2026\n\nSee [my detailed blog post about this release](https://simonwillison.net/2026/Aug/4/new-release-of-llm/).\n\nPosted [4th August 2026](https://simonwillison.net/2026/Aug/4/) at 5:15 pm\n\n## Recent articles\n- [Now we have a timeline of the OpenAI accidental attack against Hugging Face](https://simonwillison.net/2026/Aug/7/openai-timeline/) - 7th August 2026\n- [One-shotting a Raccoon Heist game using Claude Fable 5](https://simonwillison.net/2026/Aug/5/raccoon-heist/) - 5th August 2026\n- [New release of LLM adds support for reasoning traces, OpenAI Responses, server-side tools, and smarter logging](https://simonwillison.net/2026/Aug/
codex
Simon Willison 有多篇窗口内文章。现在抓取核对详情。
 succeeded in 17824ms:
{"success":true,"data":{"web":[{"url":"https://www.infoq.com/news/2026/07/java-news-roundup-jul13-2026/","title":"Java News Roundup: Value Objects, WildFly 41, TornadoVM ... - InfoQ","description":"# Java News Roundup: Value Objects, WildFly 41, TornadoVM, LangChain4j, Oracle AI Agent Studio\n#### LangChain4j\nThe _formal release_ (along with the _twenty-eighth beta release_) of [LangChain4j](https://github.com/langchain4j) 1.18.0 provides bug fixes and new features such as: a new [Belief-Desire-Intention](https://jumpcloud.com/it-index/what-is-bdi-belief-desire-intention-architecture) (BDI) agentic pattern that \" _provides a structured method to formalize psychological concepts for software and robotic systems_;\" a new **`TextToSpeechModel`** interface to support for the OpenAI [Text-to-Speech](https://developers.openai.com/api/docs/guides/text-to-speech) API; and a new **`MistralAiBatchChatModel`** class to support the [Mistral Batch](https://mistral.ai/news/batch-api/) API.","position":1}]},"id":"019fe9cc-9ba8-76ab-b882-1729b64f9f59","creditsUsed":2}

exec
/bin/bash -lc 'firecrawl scrape https://simonwillison.net/2026/Aug/4/new-release-of-llm/ --formats markdown --only-main-content 2>/dev/null | head -c 6000' in /root/note-worker
 succeeded in 102ms:
exec
/bin/bash -lc 'firecrawl search "Kotlin 2.3 release August 2026 Kotlin Multiplatform" --limit 8 --tbs qdr:m --json 2>/dev/null | head -c 4000' in /root/note-worker
 succeeded in 7105ms:
{"success":true,"data":{"web":[{"url":"https://kotlinlang.org/docs/releases.html","title":"Kotlin release process | Kotlin Documentation","description":"This page explains the Kotlin release cycle and the different types of releases we ship. It also includes details about past and upcoming Kotlin releases, ...","position":1},{"url":"https://endoflife.date/kotlin","title":"Kotlin","description":"Check end-of-life, release policy and support schedule for Kotlin. Kotlin is a cross-platform, statically typed, general-purpose programming language with type ...","position":2},{"url":"https://kotlinlang.org/docs/whatsnew-eap.html","title":"What's new in Kotlin 2.4.20-Beta2","description":"To update to the new Kotlin version, make sure your IDE is updated to the latest version and change the Kotlin version to 2.4.20-Beta2 in your build scripts.","position":3},{"url":"https://ktor.io/docs/releases.html","title":"Ktor releases | Ktor Documentation","description":"Release details﻿ ; 2.3.3. August 1, 2023. A patch release that includes client and server support for linuxArm64 and various bug fixes. See changelog on GitHub.","position":4},{"url":"https://plugins.gradle.org/plugin/io.github.dev-vikas-soni.lighthouse","title":"Plugin: io.github.dev-vikas-soni.lighthouse","description":"Kotlin Multiplatform projects. Created 01 August 2026. Enterprise-grade Gradle diagnostic engine: health scoring, dependency analysis, build performance ...","position":5},{"url":"https://developer.android.com/jetpack/androidx/versions/all-channel","title":"Recent Release Notes","description":"Kotlin Multiplatform Quality. Each version of an AndroidX library passes through four release channels while being developed. This page lists the components in ...","position":6},{"url":"https://www.i-programmer.info/news/98-languages/19049-jetbrains-has-announced-that-kotlinllm-its-research-prototype-for-delegating-runtime-logic-to-a-large-language-model-llm-from-kotlin-code-will-now-be-available-as-open-source-and-will-be-public-kotlin-is-the-open-source-language-originated-by-jetbr.html","title":"JetBrains Makes Kotlin LLM Open Source","description":"Kotlin LLM, which was announced in July, is an IntelliJ IDEA plugin prototype. It adds a language feature JetBrains calls smart macros, which can be used for ...","position":7},{"url":"https://androidweekly.net/","title":"Android Weekly - Free weekly Android & Kotlin development ...","description":"Kotlin Multiplatform sample sharing one codebase across Android, iOS, desktop, and web using Compose Multiplatform. Issue #738 August 2, 2026 Issue","position":8}]},"id":"019fe9cc-ebbe-742a-9f89-f51540443da2","creditsUsed":2}

exec
/bin/bash -lc 'firecrawl scrape https://simonwillison.net/2026/Aug/4/new-release-of-llm/ --formats markdown --only-main-content 2>&1 | head -c 8000' in /root/note-worker
 succeeded in 80ms:
error: unknown option '--formats'
(Did you mean --format?)

exec
/bin/bash -lc 'firecrawl search "openai engineering blog Codex agents August 2026" --limit 8 --tbs qdr:m --json 2>/dev/null | head -c 4000' in /root/note-worker
 succeeded in 6349ms:
{"success":true,"data":{"web":[{"url":"https://daily.dev/blog/best-ai-coding-agents-comparison/","title":"The best AI coding agents in 2026, compared - daily.dev","description":"Compare five AI coding agents by autonomy, reliability, and cost to pick the right tool for your workflow and review capacity.","position":1},{"url":"https://www.morphllm.com/best-ai-coding-agents-2026","title":"Best AI Coding Agents (August 2026): Scored Leaderboard - Morph","description":"# Best AI Coding Agents (August 2026): The Scored Leaderboard, Updated After GPT-5.6 and Opus 5\n## The Scored Leaderboard: AI Coding Agents (August 2026)\n| Agent / Model | SWE-bench Verified | SWE-bench Pro | Terminal-Bench 2.1 | Pricing model | Updated |\n|-|-|-|-|-|-|\n| Codex CLI / GPT-5.6 Sol (default) | no entry yet | no entry yet | 89.5% (xhigh, model) | $20/mo Plus + credits | 2026-07-30 |\n| Codex CLI / GPT-5.5 | 88.7% (OpenAI) | 58.6% | 83.4% | $20/mo Plus + credits | 2026-05-01 |\n\n## 6. OpenCode\n```\n{\n  \"provider\": {\n    \"myprovider\": {\n      \"npm\": \"@ai-sdk/openai-compatible\",\n      \"options\": { \"baseURL\": \"https://api.myprovider.com/v1\" },\n      \"models\": { }\n    }\n  }\n}\n```\n\n## Frequently Asked Questions\n### Sources\n- [OpenAI Codex (openai/codex)](https://github.com/openai/codex)","position":2},{"url":"https://www.getpanto.ai/blog/codex-ai-statistics","title":"Codex AI Statistics 2026: Users, Revenue & Growth - Panto AI","description":"# Codex AI Statistics 2026: Users, Revenue & Growth\nCodex is OpenAI’s cloud-based software engineering agent, built to handle feature writing, bug fixing, refactors, and pull requests across sandboxes and developer workflows.","position":3},{"url":"https://flowtivity.ai/blog/graph-engineering-2026-guide-openclaw-codex/","title":"From Loops to Graphs: The Next Paradigm in AI Agent Engineering","description":"# From Loops to Graphs: The Next Paradigm in AI Agent Engineering\n## The 5-Stage Graph Engineering Methodology\n### Stage 4: IMPLEMENT — Build and Measure\n- **OpenAI Codex** — use the graph-max technique (draw → send → run)","position":4},{"url":"https://www.snowflake.com/en/blog/engineering/data-eng-bench-data-engineering-agent-benchmark/","title":"A Data Engineering Benchmark for AI Agents - Snowflake","description":"# Introducing Data-eng-bench: Why You Need \"Data-Native\" Harnesses for Data Engineering\n## Measuring agent quality and cost\n| Harness | Model | Pass@1 | Pass^3 | Cost per trial ($) | Cost multiplier | Total tokens per trial |\n|-|-|-|-|-|-|-|\n| Snowflake CoCo (Code) | Opus 5 | **73.8%** | **64.1%** | 0.756 | 1 | 1,070,515 |\n| Codex | GPT 5.6 Sol | 60.5% | 49.5% | 0.538 | 1.503 | 812,306 |","position":5},{"url":"https://www.firecrawl.dev/blog/best-ai-coding-agents","title":"Best AI Coding Agents in 2026: Harness, Cost, and ... - Firecrawl","description":"# Best AI Coding Agents in 2026: Harness, Cost, and Accuracy Compared\n## TL;DR: the best AI coding agents in 2026\n| Agent | Type | Model | Entry price | Harness depth | Remote/async | Best for |\n|-|-|-|-|-|-|-|\n| **OpenAI Codex** | CLI + Cloud | GPT-5.5 | $8 Go; $20 Plus | Deep | Codex Cloud, PR review | Cross-surface + autonomy |\n\n## What are the best AI coding agents in 2026?\n| Agent | Standout | Watch out |\n|-|-|-|\n| OpenAI Codex | One agent across CLI, cloud, app, mobile, Chrome | Mid-stream 5-hour usage-limit cuts |","position":6},{"url":"https://blog.cloudflare.com/engineering-standards-enforcement/","title":"How Cloudflare enforces engineering standards using AI","description":"Both systems draw from the Cloudflare Codex, a shared source of engineering guidance built for people and agents. This post explains why we built the Codex, how it supports the engineering lifecycle, and what we plan to do next.\n\nWe rebuilt this body of knowledge as the Cloudflare Codex: a governed set of engineering standards that agents can retrieve and apply at the point of work.\n\n## [Copy link](https://bl
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
