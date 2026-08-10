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