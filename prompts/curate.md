---
created: 2026-08-09
updated: 2026-08-10
type: workflow
status: 待验证
product: null
source: curate-research 六阶段
---

# curate 候选加工操作约定

> 运行器：服务器 codex，由 `curate.py` 调用。每篇候选产三件套；**落位与索引回写由脚本完成**，不再调用 curate-review。

## 输入

- `references/articles.md` 待处理队列中的一条：标题 / URL / 来源 / 日期
- 批次目录：`candidates/<batch>/`，slug 由脚本给出

## 对每条待处理做

1. **抓原文**：用网络抓取 URL 真实内容 → 存 `candidates/<batch>/sources/<slug>.md`；
   论文/长文额外抓 HTML 全文到 `sources/<slug>-full.md`。
2. **翻译**：生成过程稿到 `candidates/<batch>/translations/<slug>/`：
   - `01-analysis.md`：原文分析（可含观点建议，**不写** expand/thinking 正文）
   - `02-prompt.md`：本次翻译使用的提示词
   - `translation.md`：中文翻译过程稿
   再把最终候选写到 `candidates/<batch>/works-ready/<slug>-translation.md`。

## 产出边界（不可逾越）

- **working/（works-ready/）**：✅ 翻译草稿（脚本随后落位）
- **expand/thinking/**：❌ 不写正文；只在 `01-analysis.md` 给观点建议
- **prompts/**：❌ 不写
- **wiki/**：❌ 永不触碰（只读）
- **references/ 编号正文 / expand/index·log·图谱**：❌ 不在本提示词阶段写；由 `curate.py` 内联落位

## 质量要求

- 中文正文，术语到位，保留原文超链接
- 关键数字/结论与原文抽查比对
- frontmatter 含 created/updated/sources/tags（works-ready）
