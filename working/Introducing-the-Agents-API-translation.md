---
created: 2026-10-03
updated: 2026-10-03
title: 推出 Agents API
sourceUrl: https://openai.com/index/introducing-the-agents-api/
sourceAuthor: OpenAI
translatedAt: 2026-10-03
sources: [references/articles.md 待处理队列]
tags: [Agents API, Codex harness, 云端智能体, Cloud Agents, 子智能体, Subagent, 多智能体, Multi-Agent, 上下文压缩, Compaction, 工具搜索, Tool Search, 程序化工具调用, Programmatic Tool Calling, MCP, 沙箱, Sandbox, OpenAI hosted sandbox, gpt-6-astra, 公测, Public Beta, type/翻译]
---

# 推出 Agents API

> [openai.com](https://openai.com/index/introducing-the-agents-api/)｜分类：Product / API
> 来源：OpenAI
> 发布：2026-09-10（队列日期 2026-09-12）
> 原文：https://openai.com/index/introducing-the-agents-api/

构建并运行由 Codex harness 驱动、由 OpenAI 全托管的云端智能体。

随着我们把 Codex 和 ChatGPT for Work 扩展到全球数百万用户，我们学到了要让长时运行（long-running）智能体在实践中真正好用需要什么。有用的智能体需要一个强大的 harness（智能体运行框架）：它能管理上下文、高效使用工具、协调子智能体（subagent）。它们还需要一套基础设施，让智能体能够可靠地连续运行数天，并提供可以操作文件、运行代码、保存中间结果的环境。

今天，我们推出公测版的 [Agents API](https://developers.openai.com/api/docs/guides/agents-api/overview)，把驱动 Codex 的同一套 harness 与基础设施，通过一个简单、灵活的 API 交到开发者手中。

## 客户如何评价 Agents API

> “借助 Agents API，我们的评估分数从 0.71 提升到 0.85。API 中的子智能体支持非常出色，大幅加快了我们的工作流。此前，在我们旧的架构中观察和编排子智能体相当繁琐，而新 API 让延迟降低了 4 倍。我们花了很长时间尝试优化这一点，而子智能体流程带来的是开箱即用的巨大提升。”
>
> Jack Weissenberger，Ciridae 首席技术官

> “改造现实世界的业务，意味着要把 AI 部署到各种形态的工作流中。Agents API 提供了 harness；环境、上下文和用户体验仍由我们自己掌控。借助我们的 AI 平台 Nexus，我们现在能在数小时内为从住宅服务到建筑等各行业搭建智能体。”
>
> Rasmus Wissmann，Long Lake 首席技术官

> “Agents API 让我们得以重新思考如何架构复杂、多步骤的工作流。过去我们编写提示链并自行管理一组工具调用，而现在我们可以直接在代码中使用智能体，就像 Codex 在你的笔记本电脑上工作一样。它已经帮我们解决了几个原本需要自建定制智能体基础设施才能解决的问题。”
>
> Cole Striler，WithCoverage 工程总监

> “把案件审查工作流迁移到 Agents API 之后，我们实现了单案成本下降 60%、延迟更低、token 效率显著提升，同时保持了原有性能。”
>
> Bhavyansh Sabharwal，SafetyKit 技术人员

> “在我们测试中最突出的一点，是 Agents API 处理突发型工作负载时有多么自然。我们可以把工作扇出到数百个智能体，异步运行它们，稍后再收集结果，而不必在峰值之间让基础设施空转。”
>
> Dmitry Khanukov，Dwelly 联合创始人兼首席技术官

> “赢得客户信任在金融服务中至关重要。OpenAI 的 Agents API 让我们能够构建更可靠的智能体，让客户放心地在生产环境中使用它们。通过把智能体 harness 与沙箱分离，我们把智能体的失败响应减少了 86%。”
>
> Serhii Shchoholiev，Hypha 首席工程师

> “Agents API 在一个真实、活跃的代码仓库中完成了实现、独立审查、修复以及真实浏览器验证。总体而言，该智能体的工程质量非常强。”
>
> Maks Operlejn，deepsense.ai 高级机器学习工程师

> “在 Nash，我们部署了数千个长时运行的 AI 智能体，它们管理着全球物流网络中数亿次配送。OpenAI 的 Agents API 提供了我们所需的持久会话与编排层，让智能体能在生产环境中持续运行，处理上下文、恢复和多步骤执行；而 Nash 提供把它们连接到物理世界的工具与执行环境。这使我们的智能体能够在可能跨越数小时甚至数天、复杂的工作流中推理、行动、恢复与协作。这些智能体是生产基础设施，为我们的合作伙伴运行着任务关键型的物流运营。”
>
> Aziz Alghunaim，Nash.ai 联合创始人兼首席技术官

## 用一次 API 调用构建云端智能体

借助 Agents API，你可以通过指定任务、模型、工具和环境，用一次 API 调用创建生产级智能体：

#### JavaScript

```javascript
import OpenAI from "openai";

const client = new OpenAI();

const session = await client.beta.agents.sessions.create({
  agent: {
    model: "gpt-6-astra",
    tools: [
      {
        type: "mcp",
        server_label: "observability",
        transport: {
          type: "http",
          server_url: "https://observability.example.com/mcp",
        },
      },
    ],
    multi_agent: { enabled: true, max_concurrent_subagents: 3 },
  },
  vault_ids: ["vault_YOUR_VAULT_ID"],
  environment: {
    type: "openai_hosted",
    capability_directories: ["/workspace/capabilities/skills"],
  },
  input:
    "Investigate service-api’s elevated 5xx rate over the last 30 minutes. " +
    "Delegate deployment, error, and dependency analysis to subagents. " +
    "Save findings, evidence, and recommended mitigation in /workspace/outputs.",
});
```

OpenAI 托管并维护 harness。你可以选择智能体的计算环境：OpenAI 托管的沙箱、你自己的基础设施，或者我们的沙箱伙伴之一。Agents API 为你提供坚实的基础，让你可以基于我们优化的智能体 harness 与基础设施来构建智能体，从而专注于那些让你的智能体与众不同的工具、知识和工作流。

*图：应用把任务发送给 Agents API 并接收事件与输出。Agents API 运行托管的 Codex harness，向沙箱发送工具调用并接收工具结果。应用掌控自托管算力。*

Agents API 为你的智能体提供与 Codex 背后相同的 harness 与基础设施。

## 选择你的智能体环境

不同的工作负载需要不同的计算、存储和部署选项。Agents API 允许你选择适合自己应用的沙箱。

我们正在[与生态伙伴合作](https://developers.openai.com/api/docs/guides/agents-api/environments/self-hosted#sandbox-providers)，包括 Blaxel、Cloudflare、Daytona、DigitalOcean、E2B、Modal、Oracle、Runloop 和 Vercel，为各类需求提供一流集成：

- 全托管环境，或部署在你自己的 VPC 内
- 特定的文件和密钥存储机制
- 不同的 CPU、GPU 和内存配置，具备与你公司工作流相匹配的性能、冷启动和成本画像

## OpenAI 托管沙箱

对于希望快速上手并高效扩展的开发者，我们还推出了 [OpenAI 托管沙箱](https://developers.openai.com/api/docs/guides/agents-api/environments/openai-hosted)。它复用了驱动 Codex 和 ChatGPT 的同一套沙箱基础设施。

OpenAI 负责提供并管理沙箱，为你的智能体提供一个安全、高性能的环境，用来运行代码、操作文件并产出制品（artifact）。这些沙箱可以灵活地用你的文件、包、skills 和插件进行配置，为智能体提供完成任务所需的一切。

## 基于持续演进的 Codex harness 构建

利用新的模型能力，往往意味着要重构你的 harness，从而占用本可用于改进应用的宝贵时间。Agents API 随每次模型发布提供对这些能力的版本化访问。我们随模型一道维护并持续改进 harness，帮助你的智能体在每次升级中都获得更好的性能。例如，harness 近期的改进包括：

### 让智能体在长会话中持续工作

为了支持模型连续工作数小时，我们构建了上下文管理能力，帮助智能体在更长的会话中携带相关信息。当会话接近其上下文上限时，Agents API 会[自动压缩](https://developers.openai.com/api/docs/guides/compaction)较早的上下文，保留智能体继续工作所需的信息。开发者可以构建跨越多个上下文窗口的工作流，而无需自己实现压缩逻辑。

### 帮助智能体高效使用更多工具

Agents API 帮助智能体找到正确的工具并高效使用它们。[工具搜索](https://developers.openai.com/api/docs/guides/tools-tool-search)会按需加载相关的工具定义，有助于在保持模型缓存的同时降低 token 用量与成本。工具可用之后，[程序化工具调用](https://developers.openai.com/api/docs/guides/tools-programmatic-tool-calling)让智能体可以并行运行调用、串联相关操作，并在代码中过滤或组合结果，从而能够处理海量数据，同时只把相关结果带回上下文。Agents API 支持 MCP、自定义函数，以及 web search 等内置工具。

#### JSON

```json
"agent": {
  "tools": [
    {
      "type": "mcp",
      "server_label": "openai_docs",
      "transport": {
        "type": "http",
        "server_url": "https://developers.openai.com/mcp"
      }
    },
  ]
}
```

### 让智能体通过子智能体并行处理工作

借助[多智能体支持](https://developers.openai.com/api/docs/guides/agents-api/multi-agent)，Agents API 可以把复杂任务拆分为相互独立的部分，并委派给并行工作的子智能体。每个子智能体维护自己的上下文，从而专注于自己的任务；主智能体则协调它们的工作并汇总结果。这可以加快受益于并行工作的研究、分析和编程任务，而无需你自己构建编排逻辑。

#### JSON

```json
"agent": {
  "model": "gpt-6-astra",
  "multi_agent": {
    "enabled": true,
    "max_concurrent_subagents": 3
  }
}
```

## 开源底座

Agents API 由开源的 Codex harness 驱动，让开发者可以了解协调模型调用、工具与上下文的核心逻辑。借助 Agents API，OpenAI 负责运营并维护这套 harness，而开发者可以检视并从其[公开代码库](https://github.com/openai/codex)中学习。

## 开始构建

Agents API 今日起以公测版向所有开发者开放。使用 Agents API 没有额外费用——你只需为智能体使用的 token 和工具付费，具体见我们的[定价页](https://developers.openai.com/api/docs/pricing)。

浏览 [Agents API 概览](https://developers.openai.com/api/docs/guides/agents-api/overview)了解更多，或按照[快速入门](https://developers.openai.com/api/docs/guides/agents-api/quickstart)开始使用，把 Codex 背后的 harness 引入你自己的智能体。

在公测期间，我们将根据你的反馈快速迭代，朝着正式可用（general availability）推进。请告诉我们哪些地方好用、你在哪里遇到阻力，以及你在生产环境中构建和运行智能体还需要什么。
