---
created: 2026-10-03
updated: 2026-10-03
title: Claude 5 世代模型的上下文工程新法则
sourceUrl: https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models
sourceAuthor: Thariq Shihipar（Anthropic 技术团队成员）
translatedAt: 2026-10-03
sources: [references/articles.md 待处理队列]
tags: [Claude Code, 上下文工程, Context Engineering, 提示词工程, Skills, CLAUDE.md, 渐进式披露, 自动记忆, Harness 工程, type/翻译]
---

# Claude 5 世代模型的上下文工程新法则

> [claude.com/blog](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models)｜分类：Engineering
> 作者：Thariq Shihipar（Anthropic 技术团队成员）
> 发布：2026-07-24（页面标注）｜阅读时长：约 7 分钟
> 原文：https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models

我们为更先进的模型删掉了 Claude Code 超过 80% 的系统提示词。本文将讲述如何把我们学到的经验，应用到你在 Claude Code 及自建智能体中的上下文工程。

我此前写过如何最好地[提示最新一代 Claude 5 模型](https://claude.com/blog/a-field-guide-to-claude-fable-finding-your-unknowns)，并通过与它们迭代协作来发现你到底想构建什么。

但当你给 Claude 发送一条消息时，提示词只是它所获得上下文的一小部分。你的上下文有很大一部分是由系统提示词、Skills、CLAUDE.md 文件、记忆（memory）以及其他来源拼装而成的。我们称之为[上下文工程](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)，它对你在使用 Claude Code 或构建自研智能体时产出的结果有着巨大影响。

与提示词不同，上下文会在许多请求之间被通用地使用，因此它无法那么具体。你会如何为 Claude 构建这些通用的提示与指引——尤其当你不清楚用户的提示词会是什么样时？

随着 Claude 自身能力不断演进，这件事会难得惊人。最近我们就注意到，在提示最新一代 Claude 模型的方式上出现了一次大幅跃迁。对于 Claude Opus 5 和 Claude Fable 5 这类模型，我们删掉了 Claude Code 超过 80% 的系统提示词，而在我们的编码评测上没有任何可测量的损失。

以下就是我们对这一类新模型提示经验的心得，以及你该如何用它来更新自己的上下文工程。我们已经把这些最佳实践放进了 `claude doctor`；在 Claude Code 里用 `/doctor` 命令，就能自动给你的 Skills 和 CLAUDE.md 文件"瘦身"到合适规模。

## 给 Claude 松绑（UNHOBBLING CLAUDE）

总的来说，我们发现自己对 Claude Code 施加了过多的约束——无论是通过系统提示词，还是通过 CLAUDE.md 文件和 skills。

举个例子，当我们翻看自己内部使用 Claude Code 的会话记录时，会在同一个请求里看到好几条互相冲突的信息，比如"视情况保留文档"或"不要添加注释"，因为我们的系统提示词、skills 和用户请求彼此打架。

![一份拼装起来的上下文：系统提示词写着"视情况保留文档"，一个 skill 写着"不要添加注释"，用户请求则说"就让它像旧版那样跑起来就行"。](https://claude.dev/media/a0c1f3923f1e92004785e35257d3feed5081264767d0a99fa5eb397e2fb6f2e2.png)

一般而言，Claude 能够解读用户意图、得出正确答案，但在决定怎么做之前，它必须更仔细地权衡这些重叠且冲突的信息。

虽然这些约束曾经是避免最坏情况所必需的，但我们后来发现，可以删掉其中许多，转而让模型利用周边上下文和自己的判断力。

此外，Claude Code 现在的工具也多得多了。Claude 过去依赖 CLAUDE.md 作为记忆、信息和指引的来源。而现在我们有了记忆（memory）、artifacts 和 skills，Claude 可以用它们开辟出跨会话加载与共享上下文的新方式。

## 过去与现在（THEN AND NOW）

曾有不少旧的上下文工程最佳实践，如今已经变成了迷思（myth）。包括：

![六条旧规则被划掉，各自指向其替代项：给 Claude 规则 → 给 Claude 判断力；给 Claude 示例 → 设计接口；全部前置 → 渐进式披露；重复自己 → 简单的工具描述；把记忆放在 CLAUDE.md 文件里 → 自动记忆；简单的规格 → 丰富的引用。](https://claude.dev/media/aaa82d5934e084f1e509ac1679c26d0d2338d6c995c1c2f349fc12b8a0fd1a9c.png)

### 过去：给 Claude 规则
### 现在：让 Claude 使用判断力

当初刚推出 Claude Code 时，我们需要确保 Claude 避开最坏情况，比如删除文件。这意味着我们会给出一些特别强硬、但未必总是成立的指引。例如，我们曾在系统提示词里写道：

*在代码中：默认不写注释。绝不写多段 docstring 或多行注释块——最多一行短注释。除非用户要求，否则不要创建规划、决策或分析类文档——基于对话上下文工作，而不是中间文件。*

但对于某一类提示词，这条指引就是错的。以文档为例，用户可能有自己的偏好，或者极复杂代码的某些部分确实需要多行注释块。

不过，如果没有这些护栏，旧模型写出的注释在许多情况下都会不正确，我们不得不接受这种取舍。而更新的模型拥有更好的判断力，无需显式规则也能很好地处理这些决策。

在新系统提示词里，我们写的是：*写出读起来像周围代码的代码：匹配它的注释密度、命名和惯用法。*

### 过去：给 Claude 示例
### 现在：设计接口

工具使用曾经的第一法则是给 Claude 提供使用示例。而在我们最新的模型上，我们发现给示例反而会把它们限制在某个特定的探索空间内。

![改前：TodoWrite 工具描述约 9,100 个字符，满是"何时使用"的清单和完整示例。改后：一段简短描述"为当前会话创建并更新任务列表"，加上 pending、in_progress、completed 三个状态枚举，以及一条规则：同一时间只能有一个任务处于 in_progress。](https://claude.dev/media/8bb6f9365532bb8b19443ad00f230444087a452f776232d05045f1c6c63c3de8.png)

与其使用示例，不如多想想你的工具、脚本和文件该如何设计——Claude 手上有哪些参数，它们能否更具表达力？

例如在 Todo 工具这个例子里，只要把 status 列成 pending、in\_progress、completed 之间的枚举，就暗示了 Claude 该怎么用它。"同一时间只保留一个 in\_progress 项"这条指令，则帮助我们定义了想要的行为。

### 过去：全部前置
### 现在：渐进式披露

由于 Claude Code 专注于编码，我们的系统提示词里包含了关于如何做代码审查与验证的详细信息。这些信息并不总是需要，但一旦需要就至关重要。

此后，Claude Code 已经非常擅长使用渐进式披露（progressive disclosure）——在正确的时机加载正确的上下文。例如，我们把验证和代码审查移进了它们各自的 skills，让 Claude Code 能有选择地调用。

但渐进式披露不只用于 skills，我们也把它用于工具。我们有些工具是"延迟加载（deferred loading）"的，也就是说，智能体必须先通过 ToolSearch 搜索到它们的完整定义，然后才能使用。这让我们可以拥有更多工具（比如我们的 Task 系列工具），而这些工具在被需要之前不会占用上下文。

同样的做法也可以用到你自己的 CLAUDE.md 和 Skill.md 文件上。一个常见的迷思是：你想把它们做成一个中央仓库，收录你*可能*遇到的每一条已知实践，否则 Claude 就找不到它。相反，[不妨考虑维护一棵可按需在正确时机加载的文件树](https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code)。

### 过去：重复自己
### 现在：简单的工具描述

更早期的 Claude 模型有时需要重复的指令，并且更倾向于听信上下文窗口末尾的指令，而非开头的。这意味着我们的系统提示词有时会既在主系统提示词里引用某个工具，又在工具描述里给出指令。

我们发现可以删掉这些重复示例，把如何使用工具的指令放到工具描述里，而不是系统提示词里。

### 过去：把记忆放在 CLAUDE.md 文件里
### 现在：自动记忆

我们过去鼓励用户用 `#` 快捷键把内容自动写入他们的 `CLAUDE.md`，以此把东西存进 Claude 的记忆。而现在，Claude 会自动保存与工作、与你相关的记忆。

### 过去：简单的规格
### 现在：丰富的引用

在 plan mode 下，Claude Code 曾严重依赖带计划的 markdown 文件。把这些文件作为计划存起来，有助于 Claude 在需要时引用它们。另一个类似的最佳实践，是把规格（spec）存进代码库，供 Claude 在较长的项目里工作时参考。

但我们发现，Claude 能够处理越来越复杂的引用。与其使用简单的 markdown 文件，Claude 现在可以引用由我们新推出的 artifacts 功能所创建的 HTML artifact。

你也可以用代码的形式给 Claude 提供引用。一份规格也可以是一个详尽的测试套件，或者是另一个代码库里某个可能被 Claude 移植过来的函数。

评分量表（Rubrics）是另一种形式的引用。它让 Claude 得以借助[动态工作流（dynamic workflows）](https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code)，用这些 rubric 拉起验证智能体，来尝试核查你在某个领域里的品味（比如，好的 API 设计长什么样）。

## 把它应用到你的上下文上（APPLYING THIS TO YOUR CONTEXT）

把这些综合起来，当你拼装自己的上下文时，它会是什么样子？

![把上下文窗口画成一个栈：最上面是你的提示词，然后是引用，如 @ 提及的文件、规格、原型图、代码库和 artifacts；再往下是系统提示词、CLAUDE.md 文件、skills 和记忆。](https://claude.dev/media/6c6b396594b664244e31fe5ba0c37619accc4777be823e699906c7a641dfcc60.png)

### 系统提示词

系统提示词与产品上下文紧密绑定。它告诉 Claude 自己正运行在什么产品里、正在做什么。对 Claude Code 而言，你很可能永远不会修改它；但如果你在构建自己的智能体 harness，那么这里就是你应该花大量时间的地方。

### CLAUDE.md

让 CLAUDE.md 保持轻量，简要描述你的仓库是干什么的，但把大部分 token 花在代码库里的坑（gotcha）上。例如，你可能会把类型（type）集中放在一个单一的大文件里、别处不放。避免写那些 Claude 看一眼文件系统或仓库就"显而易见"的东西。

大量使用渐进式披露。例如，如果你有若干条独特的验证工作指令，就创建一个验证 skill，并在 CLAUDE.md 里引用它。

### Skills

把 skills 看作轻量的指引，让 Claude 在需要时找到信息。避免把它们约束得过紧——除非在极其重要的领域。

对于很长的 skills，尽量使用渐进式披露——把它拆成许多文件，分散开来。

当 skills 编码了那些你个人、你团队或你产品特有的观点、知识或最佳实践时，它才最有用。

### 引用（References）

你可以 @ 提及文件，把它们作为引用纳入。引用让 Claude 得以参考当前计划的深入信息。

这些引用可以是规格文件、原型图，甚至整个代码库。一般而言，你应当优先选代码形式的文件，因为它能以 Claude 非常熟悉的语言，给出清晰、高保真的指令。例如，一份设计的 HTML 原型，通常比一段设计描述或一张截图能带来更好的结果。

## 试着简化（TRY SIMPLIFYING）

横跨你的系统提示词、skills 和 CLAUDE.md 文件，你可能也需要像我们一样做简化。我们推出了一个新命令 `claude doctor`，它也能自动帮你完成这件事。想了解更深入地提示更先进模型的具体细节，请看我们的 [Fable 实战指南（field guide）](https://claude.com/blog/a-field-guide-to-claude-fable-finding-your-unknowns)。

*本文由 Anthropic 技术团队成员 Thariq Shihipar 撰写。*
