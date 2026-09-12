---
created: 2026-09-12
updated: 2026-09-12
type: translation-draft
status: 过程稿
sources:
  - title: langchain-ai/langchain - The agent engineering platform.
    url: https://github.com/langchain-ai/langchain
    source: github
    date: 2026-09-06
tags: [LangChain, Agent, LLM, LangGraph, Deep Agents, LangSmith, 框架, 翻译]
---

# langchain-ai/langchain —— Agent 工程平台

> 开源仓库：`langchain-ai/langchain`（主语言 Python；截至 2026-09-12 约 146.1k stars / 24.4k forks；MIT 许可证）
> 原文：https://github.com/langchain-ai/langchain

<div align="center">
  <a href="https://docs.langchain.com/oss/python/langchain/overview">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset=".github/images/logo-dark.svg">
      <source media="(prefers-color-scheme: light)" srcset=".github/images/logo-light.svg">
      <img alt="LangChain Logo" src=".github/images/logo-dark.svg" width="50%">
    </picture>
  </a>
</div>

<div align="center">
  <h3>Agent 工程平台。</h3>
</div>

<div align="center">
  <a href="https://opensource.org/licenses/MIT" target="_blank"><img src="https://img.shields.io/pypi/l/langchain" alt="PyPI - License"></a>
  <a href="https://pypistats.org/packages/langchain" target="_blank"><img src="https://img.shields.io/pepy/dt/langchain" alt="PyPI - Downloads"></a>
  <a href="https://pypi.org/project/langchain/#history" target="_blank"><img src="https://img.shields.io/pypi/v/langchain?label=%20" alt="Version"></a>
  <a href="https://x.com/langchain_oss" target="_blank"><img src="https://img.shields.io/twitter/url/https/twitter.com/langchain_oss.svg?style=social&label=Follow%20%40LangChain" alt="Twitter / X"></a>
</div>

<br>

LangChain 是一个用于构建 Agent 与 LLM 应用的框架。它帮助你链式组合可互操作的组件与第三方集成，从而简化 AI 应用开发——同时在底层技术不断演进的过程中，让你的技术决策始终面向未来。

> [!TIP]
> 刚刚起步？看看 **[Deep Agents](http://docs.langchain.com/oss/python/deepagents/)**——一个构建在 LangChain 之上的更高层封装，它内置了规划、子 Agent、文件系统使用等常见使用模式所需的 Agent 能力。

## 快速开始

```bash
uv add langchain
```

```python
from langchain.chat_models import init_chat_model

model = init_chat_model("openai:gpt-5.5")
result = model.invoke("Hello, world!")
```

如果你需要更高级的定制或 Agent 编排，看看 [LangGraph](https://github.com/langchain-ai/langgraph)——我们用于构建可控 Agent 工作流的框架。

如需等价的 JS/TS 库，看看 [LangChain.js](https://github.com/langchain-ai/langchainjs)。

> [!TIP]
> 如需开发、调试与部署 AI Agent 和 LLM 应用，见 [LangSmith](https://docs.langchain.com/langsmith/home)。

## LangChain 生态

LangChain 框架可以独立使用，同时也能与任何 LangChain 产品无缝集成，为开发者提供构建 LLM 应用的全套工具。

- **[Deep Agents](http://docs.langchain.com/oss/python/deepagents/)** —— 构建能够规划、使用子 Agent 并借助文件系统处理复杂任务的 Agent
- **[LangGraph](https://docs.langchain.com/oss/python/langgraph/overview)** —— 用我们的底层 Agent 编排框架，构建能够可靠处理复杂任务的 Agent
- **[Integrations](https://docs.langchain.com/oss/python/integrations/providers/overview)** —— 对话与嵌入模型、工具与工具包等
- **[LangSmith](https://www.langchain.com/langsmith)** —— 面向 LLM 应用的 Agent 评估、可观测性与调试
- **[LangSmith Deployment](https://docs.langchain.com/langsmith/deployments)** —— 用专为长时间运行、有状态工作流打造的平台来部署并扩展 Agent

## 为什么使用 LangChain？

LangChain 通过一套面向模型、嵌入、向量存储等的标准接口，帮助开发者构建由 LLM 驱动的应用。

- **实时数据增强** —— 轻松把 LLM 连接到各类数据源以及外部/内部系统，借助 LangChain 庞大的集成库，覆盖模型提供商、工具、向量存储、检索器等
- **模型互操作性** —— 随着工程团队通过实验为应用需求寻找最佳选择，可以随意替换模型。当前沿技术不断演进时，LangChain 的抽象让你快速适应、不丢节奏
- **快速原型开发** —— 借助 LangChain 模块化、基于组件的架构，快速构建并迭代 LLM 应用。无需从零重建即可测试不同方案与工作流，加速开发周期
- **生产就绪特性** —— 通过 LangSmith 等集成所内置的监控、评估与调试支持，部署可靠应用。用久经考验的模式与最佳实践，自信地扩展规模
- **活跃的社区与生态** —— 利用丰富的集成、模板与社区贡献组件生态。依托活跃的开源社区持续改进，紧跟最新 AI 进展
- **灵活的抽象层级** —— 在你需要的抽象层级上工作——从用于快速起步的高层链（chains），到用于精细控制的底层组件。LangChain 随应用复杂度的增长而成长

---

## 资源

- [文档](https://docs.langchain.com/oss/python/langchain/overview) —— 概念总览与指南
- [LangChain 生态总览](https://docs.langchain.com/oss/python/concepts/products) —— LangChain、LangGraph 与 Deep Agents 如何协同
- [API 参考](https://reference.langchain.com/python) —— 所有公开类、函数与类型的完整参考
- [Discussions](https://forum.langchain.com/c/oss-product-help-lc-and-lg/langchain/14) —— 用于技术问题、想法与反馈的社区论坛
- [LangChain Academy](https://academy.langchain.com/) —— 由 LangChain 团队制作的、关于 LangChain 库与产品的全面免费课程
- [贡献指南](https://docs.langchain.com/oss/python/contributing/overview) —— 如何贡献，以及如何找到适合新手的问题
- [行为准则](https://github.com/langchain-ai/langchain/?tab=coc-ov-file) —— 社区准则与标准
