---
created: 2026-08-09
updated: 2026-08-09
type: prompt-draft
status: 过程稿
sources:
  - url: https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models
tags: [Claude, 上下文工程, 翻译, prompt]
---

# 02 本次翻译使用的提示词（过程稿）

> 本次翻译用如下提示词驱动。原文已抓取到
> `candidates/20260809-180901/sources/The-new-rules-of-context-engineering-for.md`
> （firecrawl markdown 主内容），全文 HTML 存于同名 `-full.md`。

## 提示词正文

```
你是一名资深技术译者（英→中），翻译 Anthropic 官方博客文章
《The new rules of context engineering for Claude 5 generation models》。

## 输入
- 原文：candidates/20260809-180901/sources/The-new-rules-of-context-engineering-for.md
  （正文从 "# Thenewrules..." 到 "written by Thariq Shihipar" 为止；
  忽略导航、Related posts、订阅等站点噪音。）

## 输出要求
1. 完整逐译正文全部段落与小标题，不压缩、不删节；导航/FAQ/Related posts 不译。
2. 保留原文全部超链接（Markdown 链接写法原样保留，链接文字翻译成中文）。
3. 术语表（必须一致）：
   - context engineering → 上下文工程
   - system prompt → 系统提示词
   - progressive disclosure → 渐进披露
   - deferred loading → 延迟加载
   - ToolSearch → ToolSearch（保留原文）
   - unhobbling → 解除束缚
   - rubrics → 评分标准
   - artifacts → 制品
   - harness → 执行框架（首现可注 harness）
   - CLAUDE.md / Skills / References / Auto-memory 等专名保留原文
4. 代码/命令（claude doctor、/doctor、# hotkey、curl 安装命令）原样保留。
5. 中文表达要通顺自然，术语到位；关键数字（80%、Opus 5、Fable 5、
   pending/in_progress/completed 枚举）与原文逐一比对，不得改动。
6. 输出 Markdown，标题层级沿用原文；frontmatter：
   ---
   created: 2026-08-09
   updated: 2026-08-09
   title: Claude 5 世代模型的上下文工程新规则
   sourceUrl: https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models
   sourceAuthor: Thariq Shihipar（Anthropic）
   translatedAt: 2026-08-09
   sources: [references/articles.md 待处理队列]
   tags: [Claude, 上下文工程, AI Agent, Harness, type/翻译]
   ---
```

## 执行备注

- 抓取方式：`firecrawl scrape -f markdown --only-main-content`（curl 直连被站点防护拦截）；
  全文 HTML 用 `-f html --only-main-content` 抓取（112KB）备用核对。
- 翻译策略：术语优先 + 完整逐译；「Then/Now」对照表保留为小标题对，
  加粗保留原文强调；引用的旧/新系统提示词原文用代码块/引用块呈现并附中文。
- 关键数字比对：80%+、Claude Opus 5 / Claude Fable 5、Todo 状态枚举三处已抽查一致。
- 该提示词本身不直接沉淀进 prompts/（curate 产出边界：不写 prompts/），
  留待评审通过、实测后再考虑复用。
