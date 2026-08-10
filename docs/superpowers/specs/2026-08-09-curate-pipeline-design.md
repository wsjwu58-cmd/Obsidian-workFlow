# 知识库 curate 流水线改造设计

> 日期：2026-08-09 · 修订：2026-08-10  
> 状态：已按「单终审 PR + 双段 research」落地  
> 目标：research（搜索→分析分流）→ curate（翻译+落位）→ **唯一人工终审 PR** → main

## 核心决策（2026-08-10）

| 决策点 | 结论 |
|---|---|
| PR 次数 | **整库只开一次**：curate 终审 PR；research / finalize 不开 PR |
| Research | Prompt A `research-search.md`（文内强制 Firecrawl MCP）→ Prompt B `research-tracker.md`（长分析 + 三档分流） |
| 三档分流 | `translate` 入待处理；`index` 写编号正文；`observe` 写观察项表 |
| 队列持久化 | research push `pipeline/queue`（force-with-lease），curate 合并后加工 |
| 后置 AI 打分 | **取消** `curate-review.md` |
| 落位 / 索引 | curate 内联：`working/` + articles + `expand/index.md` + log + 知识图谱 + `working/AGENTS.md` |
| finalize.yml | 退役 |

## 数据流

```
research.yml → SSH → research.py
  ├─ Prompt A（Firecrawl MCP）→ candidates/research-<ts>/search.md
  ├─ Prompt B（长分析）→ analyze.md + JSON triage
  ├─ 写 articles.md（待处理 / 编号 / 观察项）
  └─ push origin/pipeline/queue（无 PR）

dispatch-worker.yml → SSH → curate.py
  ├─ merge pipeline/queue articles
  ├─ codex 产三件套 → land_translations（内联落位 + 同步索引）
  └─ 开唯一 PR review/<ts> → 人工合并 main
```

## 组件

| 文件 | 职责 |
|---|---|
| `prompts/research-search.md` | Prompt A 搜索 |
| `prompts/research-tracker.md` | Prompt B 长分析 + 分流 |
| `prompts/curate.md` | 产三件套 |
| `prompts/curate-review.md` | 已废弃 |
| `scripts/research.py` | 两段 codex + 分档 + queue 分支 |
| `scripts/curate.py` | 翻译 + 落位 + 唯一 PR |
| `scripts/kb_common.py` | slug / 落位 / index·log·图谱同步 |
| `scripts/finalize.py` | 退役 CLI（仅手动补跑） |

## 状态机

```
research translate → 待处理 → curate 落位 → 已收录（归属 working/…）
research index     → 已收录（核心含脉络:…）
research observe   → 观察项表
```
