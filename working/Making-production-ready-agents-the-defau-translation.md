---
created: 2026-08-09
updated: 2026-08-09
title: 让生产就绪的智能体成为默认：构建 Duolingo 的智能体平台
sourceUrl: https://blog.duolingo.com/production-ready-ai-agent-platform/
sourceAuthor: Guadalupe Aliseda-Canton（Duolingo 工程博客）
translatedAt: 2026-08-09
sources: [references/articles.md 待处理队列]
tags: [AI Agent, 智能体平台, 生产就绪, Temporal, MCP, 评测, type/翻译]
---

# 让生产就绪的智能体成为默认：构建 Duolingo 的智能体平台

看看我们如何让 AI 智能体在生产环境中易于构建、运行与改进。

2026 年 8 月 4 日，[Guadalupe Aliseda-Canton](https://blog.duolingo.com/author/guadalupe/)

## TL;DR

在 Duolingo，各团队一直在反复重建围绕 AI 智能体的同一套基础设施。我们的解决办法是创建一个共享平台：开发者只需定义一次智能体，平台负责执行、可观测性、编排与评测。结果是，团队可以更快、更轻松地在规模上构建、复用与改进智能体。

## 每个团队都在重建同一套基础设施

AI 智能体在本地很容易构建和做原型验证。你写一段提示词，给模型它需要的工具和文件权限，运行，然后反复调整提示词，直到对输出满意为止。

难的部分从这之后才开始。

一旦你想让它跑到云端，工作重心就从提示词转向「生产化」（productionizing）。每个真正有用的智能体都需要数量惊人的周边基础设施：配置 MCP 服务器、准备凭据、克隆仓库、加载项目上下文。

在 Duolingo，这正成为一个实实在在的痛点，因为我们正在每个需要智能体的项目里重建所有这些基础设施。一个团队为某个系统搭建的基础设施，很难被另一个团队在别的系统或平台上复用，于是各团队只能一遍遍从零重建相同的地基。

此外还有分发（distribution）问题。一个智能体做好之后，我们常常希望它在不同地方都可用。这要求智能体能在多种入口被调用，比如 Slack、内部站点、CLI 或另一个 Temporal 工作流。没有共享的执行层，你就得在这些系统里把智能体重建一遍。

最后，我们还想让所有智能体都具备真正「生产就绪」所需的编排、评测与可观测性。

## 定义智能体

为了解决这些痛点，我们构建了一个系统：开发者只需简单定义智能体「应该做什么」（系统提示词）、「应该有哪些工具」（启用哪些 MCP）、「应该能访问什么」（把哪些仓库克隆进它的工作区），其余一切都由系统抽象掉。

智能体定义在注册表（registry）里，可以从不同入口复用。一个简化版定义长这样：

```python
AgentDefinition(
    name="incident_summary",
    description="Summarize incident context from prior investigation steps.",
    owner="Incident Team",
    system_prompt="Use the provided evidence to write a concise summary.",
    model="gpt-5.5",
    mcp_servers=("github", "sentry"),
    output_type=IncidentSummaryOutput,
)
```

这给了我们一种一致的方式来描述：智能体是什么、归谁所有、用哪个模型提供商、需要哪些工具、输出结构应该是什么样。

然后我们有一个名为 `AgentWorkflow` 的 Temporal 工作流负责其余部分。

`AgentWorkflow` 的目标不是成为智能体本身，而是充当一个包装器（wrapper），把共享基础设施与配置需求抽象掉。

从宏观上看，它做四件事：

1. 加载智能体的定义
2. 准备执行环境
3. 用 LLM 提供商 SDK 运行智能体
4. 返回智能体的输出

一旦智能体定义在注册表中，从调用方的角度看，触发非常简单。他们只需把智能体名称和用户提示词作为输入触发工作流。

```python
AgentWorkflow(
    agent_name="incident_summary",
    prompt="Summarize the investigation findings for this incident.",
)
```

## 为什么选 Temporal？

Temporal 是一个持久化工作流引擎（durable workflow engine）。它持久化状态、安全地重试，并跨系统协调长期运行的工作。

这与智能体的特性非常契合，因为智能体可能：

- 运行需要好几分钟
- 调用外部工具
- 等待人工输入
- 以需要重试或调试的方式失败

与其把一次智能体运行当成一次性进程，我们可以把它当作一个工作流。工作流持有持久化状态并负责编排。Activity 处理副作用——比如准备工作区、克隆仓库或保存结果——而 Query 在工作流运行期间暴露状态。

我们也已经围绕 Temporal 建好了足够多的基础设施，可以从任何入口触发工作流；既然智能体是在工作流里运行的，我们也就天然支持从任何地方运行智能体。如果你好奇，可以听听 Staff Software Engineer Zhihao Wang 在[这里](https://temporal.io/resources/case-studies/duolingo-temporal-nexus?ref=blog.duolingo.com)的分享。

## 把定义与执行解耦

在构建这个平台之前，提示词、模型、SDK、工具链与执行环境都是紧耦合的。

AgentWorkflow 改变了这一点。我们可以通过定义智能体「做什么、需要什么工具、返回什么」来创建它，而工作流管理关于它如何运行的一切。

这种区分对构建一个能够规模化（scale）的智能体平台至关重要。一旦执行与行为相互独立，我们就可以独立演进运行时、模型、工具链与评测，而无需改变消费者使用的接口。

正是这种分离让平台的下一轮迭代成为可能：对 OpenAI Agents SDK 的支持。

### 新的运行时

AgentWorkflow 已经支持若干运行时，包括 Claude Agents SDK 与 Codex CLI。增加对另一个运行时的支持，并不需要改变智能体的定义或调用方式；它只是成为同一个工作流抽象背后的又一个实现。

加入这个新运行时影响很大。OpenAI Agents SDK 显著改善了平台的操作特性，具体体现在两个方面：

1. 借助 Temporal 插件，MCP 工具调用变成了 Temporal activity。这让系统更持久化（durable），因为工具失败可以复用与其他任何工作流 activity 相同的重试策略、状态管理与失败处理。它也让系统更可观测，因为每一次工具调用——包括输入、输出、失败与重试——都在 Temporal UI 中可见。
2. OpenAI Agents SDK 还支持通过代理（proxy）路由请求。这让我们能够使用内部 LLM 网关（LLM Gateway），提供成本追踪、用量追踪与提供商抽象。与其为每个模型提供商分别维护 SDK 集成，我们可以把请求路由到网关，在一个一致接口后面切换提供商。

## 评测智能体

智能体变得可复用之后，下一个挑战是知道它们是在变好还是变差。

这对会改动代码的智能体尤其重要。光问「智能体的输出听起来是否合理」是不够的；我们需要知道它是否做了正确的改动。

为此我们构建了智能体评测（agent eval）基础设施。

智能体评测让真实的智能体跑编写好的场景（authored scenarios）。在评分之前，它们会捕获智能体的输出、改动的文件与 git diff。

一个简化版的评测用例长这样：

```python
agent_name: fix_ci
cases:
  - id: missing_requests_import
    description: Fixes a deterministic NameError by importing requests.
    input:
      repo_fixture: fixtures/missing_requests_repo
      prompt_file: prompts/fix_ci_eval_prompt.md
    graders:
      - type: structured_output
        expect:
          no_op: false
      - type: diff_assertions
        include:
          - "import requests"
        exclude:
          - "pytest.mark.skip"
        max_changed_files: 1
      - type: no_op_consistency
```

这让我们既能测试智能体的输出，也能测试它实际改了什么。

### 评分如何工作

我们使用好几种评分器（grader）。

`structured_output` 检查智能体结构化响应中的字段。

`diff_assertions` 检查实际的仓库 diff。它可以要求特定改动、捕捉有风险的改动、限制改动文件的数量，或把编辑限制在特定路径内。

`no_op_consistency` 检查报告的结果是否与仓库状态一致。如果输出表明无需改动、但文件却变了，评测失败；如果输出表明做了修复、但 diff 是空的，评测同样失败。

对于精确 diff 断言过于脆弱（brittle）的用例，我们还支持可选的 LLM 作为裁判（LLM-as-judge）。不过，确定性评分器才是地基。LLM 作为裁判有用，但我们不希望唯一信号是一个模型评判另一个模型的成果。

要让智能体评测真正有用，它们必须检查产物（artifacts），而不仅仅是文字。

### 把评测跑成工作流

评测系统本身也跑在 Temporal 上。

套件工作流（suite workflow）加载评测用例，为每个用例与每次重复启动一个子工作流，汇总结果，渲染报告，并可选地把本次运行保存到仪表盘。

这让评测拥有与生产智能体运行相同的持久化特性。长时间运行的评测用例可以继续跑下去。失败的用例会被显式捕获。重复运行可以并行。结果可以持久化并留待后续审查。

这也让评测不再像本地脚本，而更像是平台的一部分。

## 从数周缩短到数分钟

在这个平台之前，创建一个生产就绪的智能体是一个复杂的多步骤项目。团队必须选择 SDK、学习它的各种细节、配置仓库克隆、搭建 MCP 服务器、接通凭据。视用例而定，这套搭建可能要花上好几周。

现在，创建一个智能体大约只需要 10 分钟。开发者可以用内部站点选择 MCP、挑选模型、定义系统提示词，立即创建一个智能体。之后他们就可以从任何地方调用它，而无需操心底层细节。

这种提速只是影响的一部分。通过平台创建的每个智能体，都自动获得持久化、可观测性、编排、评测与多入口调用能力。智能体也更有用，因为它们可以用在创建它们的系统之外。定义之后，其他团队、其他工作流、甚至将来的其他智能体都可以使用它们。

目前，智能体正在支撑这些工作流：修复 CI 失败、处理代码评审意见，以及支持像我们的发布经理 Slack 机器人这样的内部工具。这个机器人把多个专用智能体组合在一起：调查崩溃、定位相关改动并汇总发现。

## 接下来是什么？

到目前为止，这套基础设施为「运行与评测可复用智能体」提供了地基。

我们现在主要聚焦这几件事：

- 根据工程师对智能体结果的反馈，自动化评测用例的创建，实现一个持续、低成本的改进闭环。
- 实现智能体编排（agent orchestration）。由于智能体以工作流形式运行，它们也可以作为工具暴露给其他智能体。这为更大的自主系统打开了大门：智能体之间可以互相触发，而 Temporal 为整个系统管理持久化。

## 结语

好的抽象一直是开发者快速前进的方式。当一个复杂问题被解决一次、并包进一个干净的接口时，所有后来者都继承了这份工作，并在不增加额外开销的情况下写出更好的代码。

这个想法现在比以往任何时候都更重要。AI 生成代码很快，但不一定能生成高质量代码。用 Claude Code 或 Codex 这类工具做一个智能体很容易，但这些工具不会自动考虑持久化、可观测性或评测。如果放任不管，每个新智能体都会变成它自己的基础设施问题。我们生成的代码越多，能保证质量的抽象就越有价值。

我们构建的平台就是那个抽象。它不仅加快了创建速度，还改变了被创建出来的智能体的性质。通过把基础设施问题搬进平台，每个新智能体都自动继承了它们，让开发者专注于行为，而不是持久化或可观测性。

「快速前进」通常被描绘成与「构建生产就绪系统」之间的取舍。这个平台把这种取舍消解了：让开发者和 AI 快速前进的同一套工具，同时也确保他们构建的东西为生产就绪。

如果你对构建能影响全公司的、务实且生产级的 AI 系统感兴趣，我们正在招人！

[查看我们的开放职位](https://careers.duolingo.com/?department=Engineering&utm_source=blog.duolingo.com&utm_medium=blog&utm_campaign=prodready_blog_080426#careers)
