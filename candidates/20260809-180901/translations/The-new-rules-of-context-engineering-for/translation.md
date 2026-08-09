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

# Claude 5 世代模型的上下文工程新规则

> 我们为更先进的模型删除了 Claude Code 系统提示词中 80% 以上的内容。如何把我们从中学到的经验，
> 应用到 Claude Code 与你自己构建的 agent 的上下文工程中。

我此前写过如何[给最新一代 Claude 5 模型写提示词](https://claude.com/blog/a-field-guide-to-claude-fable-finding-your-unknowns)、
如何与它们迭代式协作去发现你想构建的东西。

但当你向 Claude 发送一条消息时，提示词只是它拿到的上下文里很小的一部分。你的大部分上下文
是由系统提示词、Skills、CLAUDE.md 文件、记忆（memory）和其他来源组装起来的。我们把这称为
[上下文工程（context engineering）](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)，
它对你在 Claude Code 中生成的结果、或构建自己的 agent 时的效果，影响巨大。

与提示词不同，上下文会被大量请求通用性地使用，因此它无法那么具体。你要如何为 Claude 构建
这些通用提示词与引导，尤其是在你并不知道用户会问什么的情况下？

这件事出奇地难，因为 Claude 自身的能力也在不断演进。最近我们注意到，给最新一代 Claude 模型
写提示词的方式发生了巨大跃迁。**对于 Claude Opus 5 和 Claude Fable 5 这样的模型，
我们删除了 Claude Code 系统提示词中 80% 以上的内容，而编码评测没有任何可测量的损失。**

下面是我们对提示这一新类别模型学到的东西，以及你如何利用它来更新自己的上下文工程。
我们已把这些最佳实践放进了 `claude doctor;` —— 在 Claude Code 中使用 `/doctor` 命令，
即可自动调整你的 skills 与 CLAUDE.md 文件到合适规模。

## 解除 Claude 的束缚（Unhobbling Claude）

总的来说，我们发现我们过度约束了 Claude Code——既通过系统提示词，也通过我们的 CLAUDE.md 文件与 skills。

例如，在阅读我们内部使用 Claude Code 的转录记录时，我们看到单次请求中会出现多条互相冲突的
指令，比如「按需留下文档」（leave documentation as appropriate）和「禁止添加注释」（DO NOT add comments），
因为我们的系统提示词、skills 与用户请求在彼此打架。

一般来说，Claude 能够解读用户意图并得出正确答案，但在决定怎么做之前，Claude 必须更仔细地
思考这些重叠且冲突的信息。

这些约束曾经是避免最坏情况所必需的；但后来我们发现，其中很多约束都可以删掉，转而让模型
利用周围的上下文和它自己的判断力。

此外，Claude Code 现在拥有多得多的工具。Claude 曾经依赖 CLAUDE.md 作为记忆、信息和引导的来源；
现在我们有了记忆（memory）、制品（artifacts）和 skills，Claude 可以用它们创造在会话之间
加载与共享上下文的新方式。

## 过去与现在（Then and now）

不少过去的上下文工程最佳实践已经变成了「神话」，包括下面这些。

### 过去：给 Claude 规则

### 现在：让 Claude 运用判断力

当我们最初推出 Claude Code 时，需要确保 Claude 避开最坏情况（比如删除文件）。这意味着我们要给出
一些并不总是正确的特别强硬的引导。例如，我们的系统提示词里曾经写过：

> _在代码中：默认不写注释。绝不写多段 docstring 或多行注释块——最多一行短的。
> 除非用户要求，不要创建规划、决策或分析文档——基于对话上下文工作，而不是中间文件。_

但对于某一部分提示词，这条引导是错误的。以文档为例：用户可能有自己的偏好，或者非常复杂的
代码的某些特定部分确实需要多行注释块。

不过，没有这些护栏时，旧模型写的注释在很多情况下会出错，我们不得不接受这个权衡。
但新模型的判断力更好，即使没有显式规则，也能很好地处理这些决策。

在新的系统提示词里，我们说的是：_写出像周围代码一样可读的代码：匹配它的注释密度、命名和惯用法。_

### 过去：给 Claude 示例

### 现在：设计接口

工具使用的头号规则是给 Claude 提供使用示例。但对于我们的最新模型，我们发现**给示例实际上
会把它们约束在某个特定的探索空间里**。

与其堆示例，不如多思考你的工具、脚本和文件的设计——Claude 能拿到哪些参数？它们能否更有表现力？

例如在 Todo 工具的例子中，仅仅把状态列为 `pending`、`in_progress`、`completed` 这样的枚举，
就暗示了 Claude 该如何使用它；「始终只保留一个 in_progress 项」这条说明则帮助定义了我们期望的行为。

### 过去：把所有信息都前置

### 现在：使用渐进披露（progressive disclosure）

因为 Claude Code 聚焦于编码，我们的系统提示词里包含了关于如何做代码评审和验证的详细信息。
这些信息并非总用得上，但一旦需要，就是关键信息。

此后，Claude Code 已经非常擅长渐进披露——在正确的时间加载正确的上下文。例如，我们把验证和
代码评审移到了独立的 skills 里，由 Claude Code 按需选择性调用。

但渐进披露不只是用于 skills，我们也用于工具。我们的一些工具是「延迟加载」（deferred loading）的，
也就是说 agent 在使用它们之前，必须先通过 ToolSearch 搜索它们的完整定义。这样我们就能拥有更多
工具（比如我们的 Task 工具），它们在需要之前不占上下文。

同样的方法也可以应用到你自己的 CLAUDE.md 与 Skill.md 文件上。一个常见误区是：你想把它们变成
一个收纳所有「可能遇到」的已知实践的中央仓库，因为否则 Claude 就找不到。恰恰相反——
[考虑采用一棵可以在正确时间加载的文件树](https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code)。

### 过去：反复重复

### 现在：精简的工具描述

早期的 Claude 模型有时需要重复的指令，或者更可能听从上下文窗口末尾而不是开头的指令。这意味着
我们的系统提示词里有时既要在主提示词中引用工具，又要在工具描述里写指令。

我们发现可以删掉这些重复的示例，把如何使用工具的说明放到工具描述里，而不是系统提示词里。

### 过去：把记忆放进 CLAUDE.md 文件

### 现在：自动记忆（Auto-memory）

我们过去鼓励用户用 `#` 热键把内容写入 [CLAUDE.md](http://claude.md/) 来自动保存到 Claude 的记忆中。
现在，Claude 会自动保存与工作和你相关的记忆。

### 过去：简单的 spec

### 现在：丰富的引用（Rich references）

在计划模式（plan mode）下，Claude Code 一直重度依赖 Markdown 计划文件。把这些文件存成计划，
能帮助 Claude 在需要时引用它们。另一个类似的最佳实践是把 spec 存在代码库里，供 Claude 在
跨更长项目的过程中引用。

但我们发现 Claude 已经能处理越来越复杂的引用。除了简单的 Markdown 文件，Claude 还能引用由我们
新的 artifacts 功能创建的 HTML 制品。

你也可以以代码的形式给 Claude 引用。一份 spec 也可以是一套详细的测试套件，或是另一个代码库里
Claude 可能需要移植的函数。

评分标准（rubrics）是另一种引用形式。Rubrics 让 Claude 能够借助[动态工作流](https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code)
拉起带这些 rubrics 的验证 agent，尝试核验你在某个领域的品味（比如：好的 API 设计应该长什么样）。

## 应用到你的上下文

把这些串起来，当你组装自己的上下文时，应该是什么样？

### 系统提示词（System Prompt）

系统提示词与产品上下文紧密绑定：它告诉 Claude 自己运行在什么产品里、在做什么。对 Claude Code 而言，
你很可能永远不会修改它；但如果你在构建自己的 agent 执行框架（harness），这里是值得你投入大量时间的地方。

### CLAUDE.md

保持 CLAUDE.md 轻量：简要说明你的仓库是做什么的，但把大部分 token 花在代码库内部的坑（gotchas）上。
例如，你可能约定代码只把类型集中放在一个巨型文件里、别处不放。避免陈述那些 Claude 看看文件系统
或仓库就能知道的「显而易见」的事。

重度使用渐进披露：例如，如果你有几条关于如何验证工作的独特指令，就创建一个验证 skill，并从你的
CLAUDE.md 中引用它。

### Skills

把 skills 看作轻量指南，让 Claude 在需要时能找到信息。除非是极重要的领域，否则避免过度约束。

对于很长的 skill，尽量多用渐进披露——拆成多个文件，逐层展开。

最好的做法是让 skills 承载那些专属于你、你的团队或你的产品的观点、知识或最佳实践。

### 引用（References）

你可以用 `@` 提及文件，把它们作为引用包含进来。引用让 Claude 能参考当前计划的深度信息。

这些文件可以是 spec、原型稿（mockups），甚至整个代码库。一般来说，你应该优先选择代码形态的文件，
因为它能给 Claude 提供它非常熟悉的语言写成的、清晰且高保真的指令。例如，一份设计的 HTML 原型稿
通常比一段设计描述或一张截图产生更好的结果。

## 试着做减法

在你的系统提示词、skills 和 CLAUDE.md 文件中，你很可能也需要像我们一样做减法。我们还推出了
一个名为 `claude doctor` 的新命令，它也能自动帮你完成这件事。关于如何提示更先进的模型，
更多细节可以看我们的 [Fable 现场指南](https://claude.com/blog/a-field-guide-to-claude-fable-finding-your-unknowns)。

_本文作者：Thariq Shihipar，Anthropic 技术团队成员。_
