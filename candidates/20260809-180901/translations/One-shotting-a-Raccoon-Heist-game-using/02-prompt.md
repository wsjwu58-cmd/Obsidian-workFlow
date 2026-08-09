---
created: 2026-08-09
updated: 2026-08-09
type: prompt-draft
status: 过程稿
sources:
  - url: https://simonwillison.net/2026/Aug/5/raccoon-heist/
tags: [AI Agent, Claude, vibe coding, 游戏开发, 翻译, prompt]
---

# 02 本次翻译使用的提示词（过程稿）

> 本次翻译用如下提示词驱动。原文已抓取到
> `candidates/20260809-180901/sources/One-shotting-a-Raccoon-Heist-game-using.md`
> （firecrawl markdown 主内容），全文 HTML 存于同名 `-full.md`。

## 提示词正文

```
你是一名资深技术译者（英→中），翻译 Simon Willison 的博客文章
《One-shotting a Raccoon Heist game using Claude Fable 5》。

## 输入
- 原文：candidates/20260809-180901/sources/One-shotting-a-Raccoon-Heist-game-using.md
  （正文从 "# One-shotting a Raccoon Heist game using Claude Fable 5" 到
  "Posted 5th August 2026" 为止；忽略站点导航、More recent articles、
  Monthly briefing、页脚等噪音；视频元素无法提取，标注可到原文页面查看。）

## 输出要求
1. 完整逐译正文全部段落、引用块与更新段，不压缩、不删节；代码块
   （makeDog 函数、Playwright 测试片段）原样保留不译。
2. 保留原文全部超链接（Markdown 链接写法原样保留，链接文字翻译成中文）；
   图片保留原地址，alt 文本翻译成中文。
3. 术语表（必须一致）：
   - one-shotting → 一次做出（单条提示完成）
   - vibe coding → 氛围编码（首现注 vibe coding）
   - cul-de-sac → 尽端路
   - key art → 主视觉
   - texture atlas → 纹理图集
   - smoke-test → 冒烟测试
   - low-poly → 低多边形
   - DPR → 设备像素比（首现注 DPR）
   - Claude Fable 5 / Claude Code for web / Three.js / Playwright / WebAudio /
     gpt-image-2 / localStorage / GitHub Pages 等专名保留原文
4. 原文中的英文提示词引用块（Fable 5 提示词、gpt-image-2 提示词）给出中文译文；
   gpt-image-2 那段在引用块后附中文括号说明。代码注释不译。
5. 中文表达通顺自然，术语到位；关键数字（2022-08-05→2026-08-05 四周年、
   7 commits、12/17 单位、6 秒 FRENZY、120 分、DPR-1、2×、2026-08-07 更新）
   与原文逐一比对，不得改动。
6. 输出 Markdown，标题层级沿用原文；frontmatter：
   ---
   created: 2026-08-09
   updated: 2026-08-09
   title: 用 Claude Fable 5 一次做出《Raccoon Heist》游戏
   sourceUrl: https://simonwillison.net/2026/Aug/5/raccoon-heist/
   sourceAuthor: Simon Willison
   translatedAt: 2026-08-09
   sources: [references/articles.md 待处理队列]
   tags: [AI Agent, Claude, vibe coding, 游戏开发, 提示词工程, type/翻译]
   ---
```

## 执行备注

- 抓取方式：`firecrawl scrape -f markdown --only-main-content`（22KB）；
  全文 HTML 用 `-f html --only-main-content` 抓取（55KB）备用核对。
- 代码块处理：makeDog / Playwright 两段代码从源文件脚本抽取拼接，与原文逐字节比对一致，
  消除手工转写误差。
- 翻译策略：术语优先 + 完整逐译；长引用（Fable 5 完工声明四段）逐段对应翻译；
  图片 alt 文本同步译中。
- 关键数字比对：四周年（2022-08-05 → 2026-08-05）、7 commits、12/17 单位、
  6 秒 FRENZY、120 分、DPR-1、2× 渲染、2026-08-07 更新日期均与原文抽查一致。
- 该提示词本身不直接沉淀进 prompts/（curate 产出边界：不写 prompts/），
  留待评审通过、实测后再考虑复用。
