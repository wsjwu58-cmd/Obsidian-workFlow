# 知识库 curate 流水线改造设计

> 日期：2026-08-09
> 状态：已获用户批准（分节确认）
> 目标：把「全自动加工 + 事后 review」重构为「AI 预处理 + 人类闸门 + 收录」的 curate-research 六阶段流水线

## 背景与动机

现有 V3 服务器执行引擎的缺陷：codex 一次调用直接写正式区（expand/thinking/、working/）+ 回写 articles.md 状态 + push 开 PR，人类只能在「合并 PR」时整体否决。违反两类原则：

1. **curate-research 的六阶段**：①抓取 → ②翻译 → ③评审[全自动] → 🚧人类闸门🚧 → ④收录 → ⑤校验 → ⑥清理——「AI 产出候选」与「人类决定收录」必须切开。
2. **目录产出者边界**：thinking/ 归人（codex 只建议）、prompts/ 只能人判"亲测有效"、wiki/ 只读；codex 不越界替人产出属于人的内容。

## 核心决策（已确认）

| 决策点 | 结论 |
|---|---|
| 人类闸门形态 | 候选分支 + 评审 PR |
| 候选产出物 | 完整三件套（sources/ + translations/ 过程稿 + works-ready/ + review.md） |
| 暂存区 | `candidates/<batch>/` tracked（随候选分支进 git） |
| 触发方式 | 自动每 3h 轮询 + 每次 1 条候选 |
| 产出边界 | codex = working/ 翻译草稿 + references/ 索引条目 + 归属建议；thinking 只给观点建议不写正文 |
| thinking 归属 | 归人，codex 只建议 |
| 收录执行者 | 候选 PR 合并后开「收录 PR」，你 approve 合并 |
| 校验强度 | 候选阶段轻量格式检查；收录阶段正式 K1-K7 |
| 采集策略 | codex 深度搜索全替代 collect.py（情报分析师提示词 + 去重注入） |
| 实现方案 | 拆两个脚本（curate.py 服务器 + finalize.py Actions） |

## 架构与数据流

```
①research.yml（新增，每周 + 手动）
   ├─ Actions 触发 → SSH 服务器 → research.py
   │     └─ 组装情报分析师提示词（prompts/research-tracker.md + 注入已知内容去重段）
   │         → codex exec 深度网络搜索（Tier1-3 信源）
   │         → 候选清单 → 机械去重（existing_urls + 队列查重）→ 入待处理队列
   └─ collect.py / collect.yml 退役

②dispatch-worker.yml（改）每 3h 轮询 count>0 → SSH → curate.py

③curate.py（服务器，新）
   ├─ git pull --rebase origin main
   ├─ 取 1 条待处理
   ├─ codex exec 产出 candidates/<batch>/ 三件套：
   │    sources/<slug>.md               原文快照（+ source-full.md 论文/长文）
   │    translations/<slug>/{01-analysis,02-prompt,translation}.md
   │    works-ready/<slug>-translation.md  发布候选
   │    review.md                       候选×定性×去向汇总表
   ├─ 轻量校验（frontmatter/文件名）
   ├─ 更新 articles.md：该条 → 评审中
   ├─ push 分支 candidates/<slug>
   └─ 开评审 PR「候选：<标题>」

④你 review（人类闸门）：approve / 请求修改 / close
   │ 合并候选 PR
   ▼
⑤finalize.yml（新增，监听候选 PR 合并）→ finalize.py（Actions）
   ├─ 读 review.md 收录标记
   ├─ 落位：works-ready/ → working/<slug>-translation.md
   ├─ 回写 articles.md：评审中 → 已收录（归属）/ 已淘汰（留 URL）
   ├─ 同步 expand/index.md、log.md、知识图谱.md
   ├─ 清理 candidates/<batch>/
   └─ 开「收录：<标题>」PR → 你 approve → 合并 → 正式 K1-K7 校验
```

## 状态机（articles.md）

```
待处理（队列行）─curate→ 评审中（候选 PR）─合并→ 已收录 / 已淘汰
                        └─close 不合并→ 需返工（可重跑）
```

## 目录产出者边界

| 落点 | codex 产出 | 人决定 |
|---|---|---|
| working/ | ✅ 翻译草稿（works-ready/） | 收录/返工/淘汰 |
| expand/thinking/ | ❌ 仅 review.md 观点建议 | 自己写正文 |
| prompts/ | ❌ 仅评审表推荐 | 判"亲测有效" |
| wiki/ | ❌ 永不触碰 | 只读 |
| references/ | ✅ 索引条目 + 评审 | 收录闸门 |
| tools/ | ❌ 建议（待实测标🔵） | 实测后入 |

## 归属分流（curate-research 减熵分流照搬）

- 实质长文/论文 → working/ 收录（编号正文条目）
- 边角材料（产品页/README/发布稿）→ articles.md「观察项」表（不计数）
- 工具类 → 建议实测后进 tools/（未实测标 🔵待实测）
- 淘汰 → 留 URL 防重复采集

## 组件清单

| 文件 | 类型 | 位置 | 职责 |
|---|---|---|---|
| research.py | 新增 | scripts/ | 情报分析师提示词组装 + codex 搜索 + 去重入队 |
| curate.py | 新增 | scripts/ | 取待处理 → codex 产三件套 → 开评审 PR |
| finalize.py | 新增 | scripts/ | 落位 + 回写 + 同步 + 清理 → 开收录 PR |
| prompts/research-tracker.md | 新增 | prompts/ | 情报分析师提示词资产（注入日期/已知内容） |
| prompts/curate.md | 新增 | prompts/ | codex 产三件套操作约定 |
| worker.py | 退役 | scripts/ | 被 curate.py 取代 |
| collect.py | 退役 | scripts/ | codex 深度搜索替代 |
| .github/workflows/research.yml | 新增 | workflows/ | 每周 + 手动触发 research.py |
| .github/workflows/finalize.yml | 新增 | workflows/ | 监听候选 PR 合并 → finalize.py |
| dispatch-worker.yml | 改 | workflows/ | SSH 命令 worker.py → curate.py |
| collect.yml | 退役 | workflows/ | 被 research.yml 替代 |
| references/articles.md | 改 | references/ | 状态机加「评审中」 |

## 去重设计（分层）

1. **提示词注入（软）**：research.py 读 articles.md，把已收录标题+URL 注入提示词「已知内容」段 → LLM 剔除语义重复
2. **机械去重（硬）**：入队前跑 existing_urls() URL 精确比对
3. **队列级去重**：检查 URL 是否已在待处理区

## 一致性门禁

- 候选阶段：curate.py 内轻量校验（frontmatter 存在、文件名合法、review.md 结构）
- 收录阶段：finalize.py 开收录 PR → CI K1-K7 全绿 + 凭据扫描 → 分支保护强制
- K1-K7 需扩展：`candidates/` 目录的轻量格式校验（或豁免）

## 错误处理

- codex 搜索/加工失败 → 条目标记「采集失败/加工失败」，留队列，下轮重试
- 评审 PR 合并时 finalize 失败 → 保留 candidates/，log.md 记录，可手动重跑 finalize
- 候选 PR close 不合并 → 条目保持评审中/需返工，队列不重复入队
