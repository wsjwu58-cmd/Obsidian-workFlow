---
created: 2026-10-03
updated: 2026-10-03
title: 让生产就绪的智能体成为默认：构建 Duolingo 的智能体平台
sourceUrl: https://blog.duolingo.com/production-ready-ai-agent-platform/
sourceAuthor: Guadalupe Aliseda-Canton（Duolingo 博客）
translatedAt: 2026-10-03
sources: [references/articles.md 待处理队列]
tags: [Duolingo, 智能体平台, Agent Platform, 生产就绪, Production-Ready, Temporal, 持久化工作流, Durable Workflow, MCP, OpenAI Agents SDK, Claude Agents SDK, Codex CLI, LLM Gateway, 智能体评测, Agent Eval, LLM-as-judge, 可观测性, 编排, type/翻译]
---

# 让生产就绪的智能体成为默认：构建 Duolingo 的智能体平台

> [blog.duolingo.com](https://blog.duolingo.com/production-ready-ai-agent-platform/)｜分类：工程
> 作者：Guadalupe Aliseda-Canton
> 发布：2026-08-04（队列日期 2026-08-09）
> 原文：https://blog.duolingo.com/production-ready-ai-agent-platform/

## TL;DR

在 Duolingo，各团队曾反复重建围绕 AI 智能体的同一套基础设施。我们的解法是打造一个共享平台：开发者只需定义一次智能体，平台负责执行、可观测、编排与评估。由此，各团队可以更轻松、更快速地大规模构建、复用并改进智能体。

* * *

## 每个团队都在重建同一套基础设施

AI 智能体在本地很容易构建和原型验证。你写一个提示词，让模型访问它需要的工具和文件，运行它，然后反复迭代提示词，直到对输出满意为止。

难的部分从这里才开始。

一旦你想把它跑在云上，工作重心就从"写提示词"转向"上生产"。每个有用的智能体都需要一大圈令人意外的周边基础设施：搭建 MCP server、准备凭据、克隆仓库、加载项目上下文。

在 Duolingo，这成了真正的痛点，因为我们在每个需要智能体的项目里都把这套基础设施重造一遍。一个团队为某个系统搭的基础设施，很难被另一个做不同系统或平台的团队复用，于是团队不断从零重建同一套底座。

还有一个分发问题。智能体做好之后，我们常常希望它在不同地方都能用。这要求智能体可以在很多界面上被调用，比如 Slack、内网站点、CLI，或另一个 Temporal 工作流。没有共享的执行层，你就得在这些系统里各自重建一遍智能体。

最后，我们希望给所有智能体都配上真正达到生产就绪所需的编排、评估与可观测能力。

## 定义一个智能体

为了解决这些痛点，我们构建了一套系统，让开发者只需定义智能体该做什么（system prompt）、该有哪些工具（启用哪些 MCP）、该能访问什么（哪些仓库应被克隆到它的工作空间），就能轻松拉起一个智能体。其余一切都封装掉了。

智能体定义在注册表里，因此可以从不同入口复用。一个简化后的定义如下：

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

这给了我们一种一致的方式来描述：一个智能体是什么、归谁所有、用哪家 provider、需要哪些工具、输出结构应该是什么样。

然后我们有一个名为 `AgentWorkflow` 的 Temporal 工作流来处理其余的事。

`AgentWorkflow` 的目标不是它自己成为智能体；相反，它充当一个包装层，把共享的基础设施和搭建要求都封装掉。

在高层次上看，它做四件事：

1. 加载智能体的定义
2. 准备执行环境
3. 用 LLM provider SDK 运行该智能体
4. 返回智能体的输出

一旦智能体在注册表里定义好，从调用方视角触发它就很简单。只需用智能体名称和用户提示词作为输入来触发工作流即可。

```python
AgentWorkflow(
    agent_name="incident_summary",
    prompt="Summarize the investigation findings for this incident.",
)
```

## 为什么选 Temporal？

Temporal 是一个持久化工作流引擎。它持久化状态、安全重试、并跨系统协调长时间运行的工作。

这与智能体非常契合，因为智能体可能：

- 运行好几分钟
- 调用外部工具
- 等待人工输入
- 以需要重试或调试的方式失败

与其把一次智能体运行当成一次性进程，我们可以把它当作一个工作流。工作流持有持久状态与编排；活动（activity）处理副作用——比如准备工作空间、克隆仓库、保存结果——而查询（query）在工作流运行期间暴露状态。

我们此前围绕 Temporal 已经建了足够多的基础设施，可以从任意入口触发工作流；由于智能体是在工作流里运行的，我们天然就支持从任何地方运行智能体。想了解更多，可以听资深软件工程师 Zhihao Wang 在[这里](https://temporal.io/resources/case-studies/duolingo-temporal-nexus?ref=blog.duolingo.com)的分享。

## 把定义与执行解耦

在构建这个平台之前，提示词、模型、SDK、工具链和执行环境全都紧耦合在一起。

`AgentWorkflow` 改变了这一点。我们可以通过定义智能体做什么、需要哪些工具、返回什么来创建智能体。工作流则管理该智能体如何运行的一切。

这种区分对于构建一个可扩展的智能体平台至关重要。一旦执行与行为彼此独立，我们就能独立演进运行时、模型、工具链和评估，而无需改动调用方使用的接口。

正是这种分离，让平台的下一次迭代成为可能：对 OpenAI Agents SDK 的支持。

### 一个新的运行时

`AgentWorkflow` 已经支持若干运行时，包括 Claude Agents SDK 和 Codex CLI。新增对另一个运行时的支持，无需改变智能体的定义或调用方式；它只是同一工作流抽象背后的另一种实现。

加入这个新运行时影响很大。OpenAI Agents SDK 显著改善了平台的操作特性，具体体现在两方面：

1. 借助 Temporal 的插件，MCP 工具调用变成 Temporal 活动。这让系统更持久，因为工具失败可以复用与其他工作流活动相同的重试策略、状态管理和失败处理。它也让系统更可观测，因为每次工具调用——包括输入、输出、失败和重试——都能在 Temporal UI 里看到。
2. OpenAI Agents SDK 还支持通过代理（proxy）路由请求。这使我们能用上内部的 LLM Gateway，它提供成本追踪、用量追踪和 provider 抽象。我们无需为每个模型 provider 单独做 SDK 集成，而是可以通过网关路由请求，并在一致的接口背后切换 provider。

## 评估智能体

一旦智能体可复用了，下一个挑战就是知道它们是在变好还是变差。

对于会改代码的智能体，这一点尤其重要。仅仅问智能体的输出听起来是否合理是不够的；我们需要知道它是否做出了正确的改动。

这就是我们构建智能体 eval 基础设施的原因。

智能体 eval 会让真实智能体去跑预先编写的场景。它们捕获智能体的输出、变更的文件和 git diff，然后对结果评分。

一个简化后的评估用例长这样：

```yaml
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

这让我们既能测试智能体的输出，也能测试它实际改动了什么。

### 评分如何工作

我们使用几种评分器。

`structured_output` 检查智能体结构化响应中的字段。

`diff_assertions` 检查真实的仓库 diff。它可以要求特定改动、拦截有风险的改动、限制变更文件数量，或把编辑限制在特定路径内。

`no_op_consistency` 检查报告的结果是否与仓库状态一致。如果输出表明无需改动但文件却变了，评估失败。如果输出表明做了修复但 diff 是空的，评估同样失败。

对于精确 diff 断言过于脆弱的情况，我们还支持一个可选的 LLM-as-judge。不过确定性评分器才是地基。LLM-as-judge 有用，但我们不希望唯一的信号是"一个模型去评判另一个模型的工作"。

要让智能体 eval 有用，它们需要检查产物，而不只是散文。

### 把评估当作工作流来跑

评估系统本身也跑在 Temporal 上。

套件工作流（suite workflow）加载评估用例，为每个用例和每次重复启动一个子工作流，聚合结果，渲染报告，并可选地把这次运行保存到 dashboard。

这让评估获得了与生产智能体运行相同的持久性。一个长时间运行的评估用例可以持续跑下去；失败的用例会被明确捕获；多次重复可以并行运行；结果可以被持久化并在之后复查。

这也让评估不再像本地脚本，而更像是平台的一部分。

## 从数周到几分钟

在这个平台之前，创建一个生产就绪的智能体是一个复杂的多步项目。团队得选 SDK、学它的细节、设置仓库克隆、配置 MCP server、接好凭据。取决于用例，这套搭建可能要花上好几周。

现在，创建一个智能体大约需要 10 分钟。开发者可以使用一个内网站点，选择 MCP、挑选模型、定义 system prompt，就能立即创建一个智能体。之后，他们可以从任何地方调用它，而无需操心底层细节。

这种提速只是影响的一部分。通过平台创建的每个智能体都会自动获得持久性、可观测、编排、评估和多入口调用。智能体也因此更有用，因为它们可以在创建它们的系统之外被使用。一旦定义好，它们就能被其他团队、其他工作流，最终被其他智能体使用。

目前，智能体驱动着修复 CI 失败、处理代码审查评论的工作流，也支撑着诸如我们面向发布经理的 Slack bot 这样的内部工具。这个 bot 使用组合在一起的专门智能体来调查崩溃、定位相关改动并汇总发现。

## 下一步是什么？

到目前为止，这套基础设施为运行和评估可复用的智能体提供了底座。

我们现在主要关注的是：

- 从工程师对智能体结果的反馈中自动生成 eval，以形成持续、低成本的改进闭环。
- 启用智能体编排。因为智能体以工作流形式运行，它们也可以被暴露为其他智能体的工具。这开启了更大的自主系统之门：智能体之间可以互相触发，而 Temporal 为整个系统管理持久性。

## 结论

好的抽象一直是开发者快速前进的方式。当一个复杂问题被解决一次并包进一个干净的接口，后来者就都继承了这份工作，并在无需额外开销的情况下写出更好的代码。

这个理念在今天比以往任何时候都更重要。AI 快速生成代码，但并不一定生成高质量代码。用 Claude Code 或 Codex 这类工具构建一个智能体是小事一桩，但这些工具不会自动考虑持久性、可观测或评估。放任不管的话，每一个新智能体都会变成它自己的基础设施问题。我们生成的代码越多，一个能保证质量的抽象就越有价值。

我们构建的平台就是这个抽象。它不只是加快创建速度；它改变了被创建出来的智能体的性质。通过把基础设施关切上移到平台里，每个新智能体都自动继承了它们，让开发者可以专注于行为，而不是持久性或可观测性。

"快速行动"通常被说成与"构建生产就绪系统"之间的权衡。这个平台消解了这种权衡：让开发者和 AI 快速行动的那些工具，同时也确保了他们构建的东西已经为生产做好准备。

如果你对打造能在公司范围内产生实际影响的、务实的生产级 AI 系统感兴趣，我们在招聘！

[在此查看我们的开放职位](https://careers.duolingo.com/?department=Engineering&utm_source=blog.duolingo.com&utm_medium=blog&utm_campaign=prodready_blog_080426#careers)
