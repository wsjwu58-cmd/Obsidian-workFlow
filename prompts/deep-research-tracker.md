---
created: 2026-08-09
updated: 2026-08-09
type: workflow
status: 待验证
product: null
source: references/ 情报追踪
---

# 深度情报追踪工作流（Deep Research Tracker）

> 仿 harness-engineering `prompts/deep-research-tracker.md` 三层结构，适配本知识库
> 运行频率：每周 1-2 次（GitHub Actions `research.yml` / 服务器 Codex）

## 工作流（三层）

```
Layer 1: 广度发现（搜索/抓取）→ 输出候选清单
Layer 2: 深度分析（LLM 判断）→ 过滤 + 分类去向
Layer 3: 注入（回写 references/articles.md 去重权威）
```

### Prompt A — 广度发现

目标：扫描指定领域最近的信息，输出结构化候选。

```
你是技术情报分析师。搜索以下领域过去 2 周（{START} ~ {END}）的高质量内容：

领域：
1. AI Agent 开发：RAG / Agent 工程（harness / 编排 / 上下文管理 / 调度）/ 多智能体 / 评测 / 工具平台（langchain4j / langgraph4j / Claude Code / Codex）
2. 跨平台开发：Kotlin 多平台（KMP / Compose Multiplatform）/ Flutter 架构与工具链

信源优先级：
- Tier 1：Anthropic / OpenAI / Google / LangChain 官方博客、Martin Fowler、Simon Willison、Addy Osmani
- Tier 2：HackerNews、GitHub Trending、掘金、知乎专栏
- Tier 3：arXiv (cs.SE/cs.AI)、个人技术博客

去重权威（本知识库）：
已收录的完整列表见 references/articles.md（LLM 无法访问，但本部分由代码注入；
运行时系统会先执行 'python scripts/retrack.py --list' 再拼入本 Prompt）

输出（每条）：
## {编号}. {标题}
- 链接：{url}
- 作者/来源：{source}
- 日期：{date}
- 推荐指数：⭐⭐⭐（3-5）
一句话摘要：{50 字内}
核心洞察（3条）：...
值得收录理由：{判断}

质量门槛：
- 必须：有实质技术内容 / 原创洞察 / 来源可信
- 加分：有数据 / 可复现代码 / 挑战主流观点
- 排除：纯营销 / 纯摘要 / 草稿级入门教程
```

### Prompt B 深度分析与去向决策（给 Codex/agent）

```
下面是最近 2 周候选情报列表。基于本知识库已有内容（expand/ 条目 + references/raw 素材），
对每条候选做两件事：

1. 判重：是否已在 references/ 或 expand/ 收录？去重权威是 references/articles.md（读取它）
2. 指定去向，从这些中选一：
   - 「加工」→ 放入 references/raw/ 标 status=pending 供后续 ingest 加工成 expand 条目
   - 「观点」→ 建议生成 thinking 类条目（expand/ 下）
   - 「收录」→ 仅在 references/articles.md 加一行，不加工
   - 「淘汰」→ 忽略，理由一句话
   - 「作品」→ 如值得翻译/教程，建议进 working/

输出：以 Markdown 表格总结去向决策。
```

### Prompt C：注入去重权威（执行）

```
将的去向决策写入 references/articles.md：
- 对新增文章，在索引表末尾追加一行（编号递增）
- 状态：系统在 collections/raw/ 中 / articles.md 中 / working/ 中

注意：不要改动 references/articles.md 中已存在的行。
若去重冲突（提示已收录），保留原文，仅更新状态字段。
```

## 执行上下文

- 本 Prompt 的运行时是 `research.yml`（GitHub Actions）+ codex CLI
- 去重闸门由 `scripts/retrack.py` 提供（查询 references/articles.md）
- `references/agents.md` 是 references/ 目录的规则文件（先读它）

## 注意

- 本文件为**验证前草稿**：等真实跑通一次后补「效果评价」到 prompts/feedback/