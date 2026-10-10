---
created: 2026-10-03
updated: 2026-10-03
title: Harness 工程解剖学：如何评估、迭代与守护 AI 编程智能体
sourceUrl: https://developers.googleblog.com/the-anatomy-of-harness-engineering-how-to-evaluate-iterate-and-guard-ai-coding-agents/
sourceAuthor: Taylor Mullen（Principal Engineer）、Christian Gunderman（Staff Software Engineer），Google
translatedAt: 2026-10-03
sources: [references/articles.md 待处理队列]
tags: [Harness 工程, Harness Engineering, 行为评估, Behavioral Evaluation, 智能体评估, AI Coding Agent, 端到端基准, Terminal-Bench, DeepSWE, Antigravity SDK, dogfooding, 回归防护, CI/CD, type/翻译]
---

# Harness 工程解剖学：如何评估、迭代与守护 AI 编程智能体

> [developers.googleblog.com](https://developers.googleblog.com/the-anatomy-of-harness-engineering-how-to-evaluate-iterate-and-guard-ai-coding-agents/)｜分类：AI / Cloud / How-To Guides
> 作者：Taylor Mullen（Principal Engineer）、Christian Gunderman（Staff Software Engineer）
> 发布：2026-09-09（页面标注 SEPT. 9, 2026）｜队列日期：2026-09-12
> 原文：https://developers.googleblog.com/the-anatomy-of-harness-engineering-how-to-evaluate-iterate-and-guard-ai-coding-agents/

开发者在初次接触面向智能体编程系统（agentic coding systems）的 harness 工程时，常常会掉进同一个陷阱：跑一遍 Terminal-Bench、DeepSWE 这类常见的端到端基准，看着综合分数浮动几个百分点，却完全说不清它为什么变。

端到端基准是评估模型表现、判断"哪些地方需要深入排查"的事实标准（de facto），但问题在于：这类排查的代价很高。

**行为评估（behavioral evaluation）往往能更好地衡量你的信心**——你期望的行为是否真的发生了，以及你究竟是在朝对的方向前进，还是在回归（regression）或换新模型时出现倒退。它可以充当你的迭代伙伴，帮助你理解某些改动为什么会（以这样或那样的方式）推动指标。

以下就是我们对行为评估的看法，包括那些帮助我们在模型不断演进时保持智能体系统可靠的做法。

## 范式转变：成绩单 vs. 行为路标

多数团队评估 AI 智能体的方式，就像评估一个参加考试的学生：扔给它一个庞大的代码库，限定时间，然后按通过或失败的测试数量来打分。

当分数掉下来时，到底是哪里出了问题？

- 是模型在模糊的提示（ambiguous prompt）上变得过度自信了吗？
- 是它提交前忘了验证测试套件吗？
- 是它编造了某个 CLI 参数（flag）吗？

端到端基准通常无法直接回答这些问题。

**行为评估**的作用就像改进智能体 harness 运行方式的集成测试（integration test）。当你拥有一套足够丰富的行为评估集，你就为智能体应当表现出的目标行为建立了一个基线，从而能够迭代改进提示词以达成该目标。

行为评估衡量的不是智能体是否完成了一整次多文件重构，而是一系列离散的、可观察的动作：

- 面对一个描写不充分的提示（underspecified prompt）时，智能体是提出澄清性问题，还是靠猜？
- 修改构建文件时，它会不会在宣布完成之前先跑一遍本地校验器？
- 生成文档时，它会不会提供规范的仓库链接（canonical repository links）？

## 何时该做评估：先自用（dogfooding）

与其在第一天就搭一套复杂的评估 harness，不如把这段时间用来跟随直觉、做实验。

从零开始构建智能体时，**你要先从开发者直觉和自用（dogfooding）出发**。在你造出一个能够自用其自身代码库、处理样板代码、编写自己的 Markdown 渲染器、并执行日常开发者任务的智能体之前，跑评估是没有意义的。

评估属于开发的第二阶段：**确保向前推进**，以及**防止回归**。

评估套件的主要目的，不是在智能体变好 2% 时庆祝一番；而是给你不可动摇的信心：一次新的提示词调整、工具 schema 变更或模型升级**并没有让智能体整体上变得更差**。

## 行为评估架构如何运作

一个稳健的 harness 评估框架，会把行为断言拆分成快速、确定性、单元测试风格、在本地运行的检查。

把关注点转向这些更小的、可观察的动作，你就拥有了一张可靠的安全网。你可以放心地迭代系统提示词或切换到另一个模型，因为一旦你不小心破坏了某项核心行为，你会立刻知道。

### 编写一个行为评估

行为评估断言的是中间执行步骤——比如特定的工具调用或文件修改——而不是最终字符串的相等性：

```python
import pytest
from google.antigravity import Agent, LocalAgentConfig, types

@pytest.mark.asyncio
async def test_agent_uses_web_search_for_live_weather():
  """Assert that the agent consults ground truth rather than guessing."""
  config = LocalAgentConfig()

  async with Agent(config) as agent:
    response = await agent.chat("What's the weather like in Mountain View, California?")
    tools = [call.name async for call in response.tool_calls]

  # Assert behavior, not output prose
  assert types.BuiltinTools.SEARCH_WEB in tools, (
      "Agent answered from memory without consulting live search."
  )
```

[该示例为 Antigravity SDK 编写，可查阅完整仓库。](https://github.com/google-antigravity/antigravity-sdk-python)

借着一套丰富的行为评估，你可以把提示词工程自动化。例如，你可以搭一个循环，让 LLM 自己调整系统提示词，反复迭代直到某个失败的测试终于通过，同时其余测试套件像 CI/CD 风格的护栏一样运作。这有助于确保这些改动不会破坏任何现有功能。

## 构建行为评估套件时要考虑什么

为了让这套流程从一开始就可复现，有几件事你可以做。我建议先从小处着手，用三步式行为测试循环：

1. **选定一种失败模式（failure mode）**：找出智能体最近犯的一个错误，比如在把任务标记为完成之前忘记跑单元测试。找到那个漏掉的、单一而明显的动作，把它设为目标。

2. **根据任务复杂度写出灵活的断言**：对于只有一个最优解的简单任务，构建严格的单轮断言，检查智能体是否到达了某个特定里程碑（例如验证它是否调用了测试运行器）。但对于更复杂的任务，模型可能走一条意料之外但完全正确的路径。这种情况下，不要强制固定的工具调用顺序，而应采用更模糊、基于结果的检查——比如 LLM-as-a-judge——来评估智能体所选步骤是否成功且安全地解决了问题。

3. **用批量评估来自动监控稳定性**：与其让单次评估运行阻塞 PR（单次运行会因 AI 模型的非确定性而充满噪声），不如自动化批量评估，拉取更大量的数据。持续跟踪聚合通过率，确保模型行为正朝着正确方向变化。依靠这种方向性信号，你就能灵活地调整提示词、安全地升级模型，而不必因为预期内的波动而叫停开发。

```shell
# Run local behavioral suite in under 5 seconds
pytest evals/behavioral/ -v
```

你的智能体并不需要一个更高的基准分数才能起步。它需要的是一个能让它保持诚实的评估 harness。

要构建一个稳定、有韧性的 harness，你必须停止把模型当作一个通过期末考试的"黑盒"，而开始把 harness 当作需要单元测试与集成测试的标准软件来对待。

## 结语

行为评估是 harness 工程的核心支柱之一，但它们并不能取代更大规模的端到端评估套件。二者实际上是互补的：宏观基准验证的是最终目的地，微观行为评估则是让你能够安全、快速迭代的伙伴。当两者都采用时，你在迭代时——无论是改提示词、开发新功能，还是部署全新模型——都会拥有更高的信心。

---

> 发布于：[AI](https://developers.googleblog.com/search/?technology_categories=AI)、[Cloud](https://developers.googleblog.com/search/?technology_categories=Cloud)、[How-To Guides](https://developers.googleblog.com/search/?content_type_categories=How-To+Guides)、[Learn](https://developers.googleblog.com/search/?content_type_categories=Learn)、[Explore](https://developers.googleblog.com/search/?content_type_categories=Explore)
