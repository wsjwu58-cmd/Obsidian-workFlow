---
created: 2026-08-09
updated: 2026-08-09
type: workflow
status: 待验证
product: null
source: curate-research 评审模板
---

# 候选自动评审

> 运行器：服务器 codex，由 curate.py 串行调用。对一批 3-4 篇候选统一打分。

## 任务

你是知识库的内容评审。知识库主题：AI Agent 开发 / 跨平台开发（KMP·Flutter）/ Harness Engineering / 通用技术。

读以下每篇候选的三件套，逐篇回答。候选位于 `candidates/<batch>/`：

{ITEMS}

逐篇回答（每篇独立小节，标题为篇名）：

### 篇名
- **原文价值**：原创洞察密度 / 长文实质 vs 产品页·发布稿·摘要。高/中/低 + 一句话理由
- **翻译质量**：完整逐译 / 压缩摘要 / 首轮粗稿；通顺度、术语到位度。精品/合格/需返工 + 一句话理由
- **与知识库契合度**：补薄弱环节还是重复（对照 references/articles.md 与 expand/ 已有条目）
- **一句话定性 + 建议去向**：working/ 正式收录 / articles.md 观察项一行 / tools/（待实测）/ 淘汰

## 汇总

最后输出一个「候选 × 定性 × 去向」markdown 表格：

| 篇名 | 原文价值 | 翻译质量 | 契合度 | 定性 | 建议去向 |

## 约束

- 基于实际内容，紧凑中文，结构化输出
- 只做评审与建议，不修改任何文件
