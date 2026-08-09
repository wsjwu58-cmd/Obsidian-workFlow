# references/ — 外部资源索引 + 候选素材库

持续输入源头（Phase 0）。替代原 `raw/`：既是采集素材的物理存放，也是外部文章的去重权威索引。

## 结构约定（两层）

### 1. `raw/` 子目录 —— 采集素材（由 collect.yml 写入）

- 兼容 `raw/` 原名：采集脚本写入 `references/raw/*.md`，文件名格式 `{源}-{日期}-{hash}.md`（原有格式不变）
- 每个素材 frontmatter：`title / url / source / date / status / collected`（status ∈ pending/processed/rejected）
- **状态机走原 K1 规则**：ingest 处理后标 processed + `processed_hash`

### 2. `articles.md` —— 去重权威索引（顶层）

- 每条已收录的外部文章一行：`| 编号 | 标题 | 作者 | 日期 | 对应条目/链接 |状态|`
- **采集前先查 articles.md 避免重复收集**（deep-research-tracker 的「已知内容去重段」以它为准）
- 由 research.yml（Codex 情报追踪）每 1-2 周增量更新

## 索引→产出的分流规则（读完一篇文章后去处）

| 产出方向 | 落点 | 何时 |
|---------|------|------|
| concepts / 深度笔记 | `expand/`（AI 加工条目） | 有技术深度的文章 |
| thinking / 观点 | `expand/01-.../我见/` 观点类条目 | 想表达自己的看法 |
| 作品（翻译/原创） | `working/` | 想输出可展示成果 |
| 提示词沉淀 | `prompts/` | 该文章提炼出有效 prompt |
| 仅收录 | articles.md 标记已收录 | 无深度加工价值，仅存档 |

## 与其他目录的关系

- `expand/` ← 加工产物（concepts 层）
- `working/` ← 作品输出（Phase 5）
- `prompts/` ← 验证有效提示词
- `feedback/` ← 复盘迭代（lint 巡检报告 + failure 记录）
- `references/` ← **源头 + 去重闸门**