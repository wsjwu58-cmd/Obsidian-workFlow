---
created: 2026-10-03
updated: 2026-10-03
title: 在多智能体 Harness 中组织上下文
sourceUrl: https://www.langchain.com/blog/organizing-context-in-a-multi-agent-harness
sourceAuthor: T. Bengre、C. Curme，LangChain
translatedAt: 2026-10-03
sources: [references/articles.md 待处理队列]
tags: [多智能体, Multi-Agent, Harness, Subagent, 上下文工程, Context Engineering, 上下文模式, Context Modes, 分叉, Fork, Deep Agents, deepagents, Prompt Caching, 上下文隔离, type/翻译]
---

# 在多智能体 Harness 中组织上下文

> [langchain.com](https://www.langchain.com/blog/organizing-context-in-a-multi-agent-harness)｜分类：Agent Architecture / Deep Agents / Open Source
> 作者：T. Bengre、C. Curme
> 发布：2026-09-08（页面标注 September 8, 2026）｜队列日期：2026-09-12｜阅读时长：6 min
> 原文：https://www.langchain.com/blog/organizing-context-in-a-multi-agent-harness

**TL;DR**

大多数 harness 都支持 [subagent](https://www.langchain.com/blog/choosing-the-right-multi-agent-architecture) 特性，用于从 supervisor 智能体派生出新任务。子智能体（subagent）支持[并行推理与上下文隔离](https://docs.langchain.com/oss/python/langchain/multi-agent)，让 supervisor 智能体能够在不污染上下文窗口的情况下委派工作。

supervisor 智能体负责指定任务，subagent 通常在一个全新的上下文窗口中完成任务。这会带来浪费：subagent 可能会重做 supervisor 已经做过的上下文收集操作，例如读取文件。

对于 subagent 能够从 supervisor 智能体的上下文中获益的场景，我们构建了[分叉子智能体（forked subagents）](https://docs.langchain.com/oss/python/deepagents/subagents#forked-subagents)。分叉子智能体继承 supervisor 的完整对话，而不是从零开始。由于复用 supervisor 的对话可以借助 prompt caching 并减少重复工作，分叉可能比隔离式子智能体更快、更便宜。

## 带子智能体的 Harness

把任务委派给 subagent，是智能体管理自身上下文的一种有效方式。subagent 提供[上下文隔离](https://docs.langchain.com/oss/python/langchain/multi-agent)，这样单个任务的细节就可以被挡在 supervisor 智能体的上下文窗口之外。如果你想了解更多，我们此前已经就不同的多智能体架构[写过不少内容](https://www.langchain.com/blog/choosing-the-right-multi-agent-architecture)！

[supervisor](https://docs.langchain.com/oss/python/deepagents/subagents) 是最具普适性的模式之一，大多数编程 harness 都已采用。在这种模式中，supervisor 维护一份计划，并把工作委派给专业化的 subagent。例如：

- Workers（工作者）：承接某个范围明确的实现。
- Reviewers（评审者）：对已完成的工作做出独立判断。

supervisor 智能体通常只从 subagent 那里接收任务的结果；它们的中间推理过程被挡在 supervisor 的上下文窗口之外。不过，subagent 应该从 supervisor 那里接收什么上下文，取决于该 subagent 的用途。

## 子智能体的上下文模式

为了便于规定这一点，我们在最新版 `deepagents` 中引入了上下文模式（context modes）。上下文模式规定 subagent 可以从 supervisor 接收哪些上下文。支持的取值为 `"isolated"` 和 `"fork"`。

### 隔离式子智能体（isolated）

这是 [Deep Agents](https://docs.langchain.com/oss/python/deepagents/overview) 中 subagent 的默认行为，也是此前的既有行为。subagent 以全新的上下文窗口启动，只接收 supervisor 指定的任务描述。

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6a9f9ebb18c02828b5e69194_image.png)

### 分叉式子智能体（fork）

设置 `"mode": "fork"` 后，supervisor 的当前状态会传播给 subagent，而不是让它从空状态启动。这实际上是当前线程的一次分叉续写——由 supervisor 写入一条附加指令——最终回卷（unwind）成一条供 supervisor 读取的单独工具结果。

具体来说：

- supervisor 智能体生成一次工具调用（tool call），用一段任务描述来唤起该 subagent。
- subagent 接收 supervisor 智能体的完整状态，包括对话历史。末尾的那次工具调用会被剔除，其任务描述被格式化为一条 user 消息，并附带一段固定的[前言（preamble）](https://github.com/langchain-ai/deepagents/blob/15454a85438146a59c804af3a525f96091c55fe8/libs/deepagents/deepagents/middleware/subagents.py#L357)来澄清它的角色。
- 当 subagent 完成时，supervisor 会收到它的最终消息，作为对最初那次工具调用的响应。

尽管分叉式子智能体被注入的上下文比隔离式子智能体更多，但设计上依然会尊重 prompt caching。在 subagent 需要详细上下文才能正确执行任务的场景中，分叉可以省去重复的工具调用与上下文收集。

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6a9f9f279199d5bb6100d84e_image.png)

## 如何选择上下文模式

上下文模式的正确选择，取决于 subagent 与工作的关系。一个有用的思考方式是用两种常见模式来划分：承接 supervisor 工作的 worker，以及独立评估该工作的 verifier。

#### **Worker Agent**：继续已在进行中的工作

worker 在 supervisor 已经收集完上下文或做出决定之后，执行其中一部分工作。例如，supervisor 可能排查了一个错误，追踪到某个具体函数，然后委派他人实现并测试修复。

让 worker 在隔离状态下启动，会迫使它重新发现证据。使用 `fork` 时，它会收到 supervisor 的历史，可以从调查中断的地方接着往下做。当某项工作需要完成、但 supervisor 并不一定关心为得出结论所经历的中间步骤时，就会这样调用。

```typescript

const fixerSubagent: SubAgent = {
  mode: "fork",
  name: "fixer",
  description:
    "Use when a problem has already been diagnosed and the remaining work is to implement and test the fix",
  systemPrompt: "...",
}
```

supervisor 可能会用一个类似这样的任务来调用它：

> 根据我们发现的超时问题更新重试逻辑，然后补一个回归测试

#### **Verifier Agent**：独立评估工作

verifier 会依据某些标准评审另一个智能体的工作——例如检查一个 diff 的正确性、向后兼容性与测试覆盖率。

在这种情况下，继承 supervisor 的推理可能适得其反。verifier 应当评估工作本身，而不是被 supervisor 的诊断或预期所锚定。`isolated` 模式会把任务与相关评审材料交给它，但不带上前面的对话。

```typescript

const reviewerSubagent: SubAgent = {
  mode: "isolated",
  name: "reviewer",
  description:
    "Use after an implementation is complete and needs an independent review",
  systemPrompt: "...",
}
```

supervisor 可能会这样调用它：

> 评审这个 diff 的完整性、向后兼容性与测试覆盖是否充分。

我们此前写过 [RubricMiddleware](https://www.langchain.com/blog/introducing-rubrics-for-deepagents)，那是使用独立验证器的另一个实例！

### 让子智能体专业化

除了工具和中间件之类的东西之外，上下文模式也是你可以用来让 subagent 针对某项任务进行专业化（specialize）的杠杆之一。以下是我们认为属于专业化的几个 subagent，以及它们与上下文模式的关系：

#### **Researcher Agent**：调查一个问题

researcher 调查一个问题，并向 supervisor 返回一份压缩后的答案。例如，supervisor 可能会把关于某个不熟悉的库、某个竞品，或某项技术决策历史的不同问题各自委派出去。

当问题可以独立成立时，researcher 并不需要 supervisor 的对话。使用 `isolated` 能让它的上下文聚焦在手头的问题上。当多个 researcher 并行运行时，这一点尤其有用：为每一个都做分叉会重复 supervisor 的历史，即便每个 researcher 只需要自己被分配的那个问题。

```typescript

const researcherSubagent: SubAgent = {
  mode: 'isolated',
  name: 'researcher',
  description:
    'Use to investigate a self-contained question and return a condensed, well-sourced answer',
  tools: [search_engine],
};
```

supervisor 可能会这样调用它：

> 判断 API 在 1.2 与 1.3 版本之间是否发生了变化，并链接到相关的 release notes。

我们可以给 subagent 赋予它自己的能力（比如一个 `search_engine` 工具），帮助它完成任务。

#### **Memory Agent**：从对话中保留信息

memory agent 会从一次交互中识别出稍后应当可用的信息——例如用户偏好、某项架构决策，或对话过程中确立的某个约束。

在这里，对话本身就是该智能体需要分析的材料。使用 `fork` 时，memory agent 会收到完整的交互内容，并能自行决定哪些值得保留，而无需 supervisor 在任务中重新陈述一遍。

```typescript

const memorizerSubagent: SubAgent = {
  mode: "fork",
  name: "memorizer",
  description:
    "Use when the conversation contains durable decisions, facts, or preferences worth saving to memory",
  permissions: [\
    {\
      operations: ["write"],\
      paths: ["/**"],\
      mode: "deny",\
    },\
    {\
      operations: ["read"],\
      paths: ["/AGENTS.md", "/docs/**"],\
      mode: "allow",\
    },\
  ],
};
```

supervisor 可能会这样调用它：

> 记住这次对话中确立的决策与偏好。

因为我们希望精确限制 memorizer 智能体能够编辑的内容，所以可以通过设定它工作期间可编辑文件的限制，来让这个 subagent 专业化。

### 试一试

`deepagents` 是我们在与数千个不同的团队合作交付智能体的过程中，把经验教训沉淀下来的一个框架。你可以安装它，试用 subagent 上下文模式（文档见[此处](https://docs.langchain.com/oss/python/deepagents/subagents#forked-subagents)）以及更多功能：

```bash

# Python
uv add deepagents
# Typescript
pnpm i deepagents
```

欢迎通过 GitHub [issues](https://github.com/langchain-ai/deepagents/issues)、[forum](https://forum.langchain.com/)，或在 X / LinkedIn 上告诉我们你的想法！
