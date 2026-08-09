# prompts/ — 有效提示词积累

学习与自动化过程中**验证有效**的提示词，按场景或工作流沉淀。**只收录亲测有效的，不收录未验证的。**

## 文件形态（两种合法形式）

### 形式 A：单条 Prompt（按场景命名）

- 文件名：`{场景}.md`，如 `code-generation.md`、`code-review.md`
- 必备字段：用途、提示词正文
- 建议字段：效果评价（好/中/差）、改进记录、适用模型 / 不适用场景

### 形式 B：Prompt 工作流（按工具链命名）

- 文件名：`{工作流名称}.md`，如 `deep-research-tracker.md`
- 必备字段：工作流目标、各步 Prompt 正文（A/B/C…）、链路图
- 适合多模型 / 多步骤协作的场景

## 与知识库的关系

- `prompts/` 是**提示词资产库**，不属于 wiki/expand 知识图谱，不参与一致性门禁（K1-K7 只检查 raw/wiki/expand）
- `scripts/*.py` 里的 LLM 提示词是「生产代码」，此处是「资产沉淀」——**以 scripts 为唯一权威源**；本目录条目指向 `scripts/xxx.py` 的对应行，效果评价随时间更新，正文不再重复维护
- 用了某条 Prompt 之后，把效果记到 [feedback/](feedback/)；积累到一定量再回到本目录补"效果评价 / 改进记录"

## 已有内容

| 文件 | 形态 | 来源 | 状态 |
|------|------|------|------|
| [ingest.md](ingest.md) | 工作流 | `scripts/ingest.py:176` | 已用于每日 AI 加工 |

## 下一步

- 把 `check_consistency.py` 的 K 检查输出 / `gc_report.py` 的隔离建议固化到 `scripts/`，需要时沉淀为条目
- 跑满 2 周后补 ingest 的效果评价与改进记录
