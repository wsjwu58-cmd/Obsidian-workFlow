---
created: 2026-08-09
updated: 2026-08-09
type: workflow
status: 待验证
product: null
source: curate-research 六阶段
---

# curate 候选加工约数

> 运行器：服务器 codex，由 curate.py 调用。每篇候选产三件套 + 串行评审。

## 输入

- references/articles.md 待处理队列中的一条：标题 / URL / 来源 / 日期

## 对每条待处理做 4 步

1. **抓原文**：用 webfetch 抓取 URL 真实内容 → 存 `candidates/<batch>/sources/<slug>.md`；
   论文/长文额外抓 HTML 全文到 `sources/<slug>-full.md`。
2. **翻译**：按流程生成三件套到 `candidates/<batch>/translations/<slug>/`：
   - `01-analysis.md`：原文分析 + 收录建议（含原文价值/翻译质量/契合度初判）
   - `02-prompt.md`：本次翻译使用的提示词（过程稿）
   - `translation.md`：中文翻译过程稿
   再把最终候选写到 `candidates/<batch>/works-ready/<slug>-translation.md`。
3. **回写 articles.md**：该条状态 → `评审中`，附候选路径 `candidates/<batch>/`。
4. **输出候选文件**：所有产物落在 `candidates/<batch>/` 下（tracked）。

## 产出边界（不可逾越）

- **working/（works-ready/）**：✅ 翻译草稿
- **expand/thinking/**：❌ 不写正文；只在 `01-analysis.md` 里给观点建议（供人类参考）
- **prompts/**：❌ 不写；只在评审表推荐"可复用 prompt"
- **wiki/**：❌ 永不触碰（只读）
- **references/ 编号正文**：❌ 不在本阶段写；finalize 收录时才写

## 质量要求

- 中文正文，术语到位，保留原文超链接
- 关键数字/结论与原文抽查比对
- frontmatter 含 created/updated/sources/tags
