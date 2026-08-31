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

目标：扫描 Agent 工程相关领域最近的信息，输出结构化候选。完整、可执行的 Prompt A 以 `prompts/research-search.md` 为准。

```
Prompt A 的搜索范围固定为 Harness Engineering、Context Engineering、AI Coding Agents、Agent Infrastructure 和 AI-assisted Software Engineering；去重清单由运行时注入当前 `references/articles.md` 中的相关内容。
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
