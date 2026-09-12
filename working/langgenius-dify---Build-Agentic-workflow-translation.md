---
created: 2026-09-12
updated: 2026-09-12
title: langgenius/dify —— 在一个协作工作区里构建 Agentic 工作流与 RAG 管道
sourceUrl: https://github.com/langgenius/dify
sourceAuthor: LangGenius（Dify 官方 GitHub 仓库）
translatedAt: 2026-09-12
sources: [references/articles.md 待处理队列]
tags: [Dify, LLMOps, AI 工作流, RAG, Agent, 低代码, type/翻译]
---

# langgenius/dify —— 在一个协作工作区里构建 Agentic 工作流与 RAG 管道

> 开源仓库：`langgenius/dify`（主语言 TypeScript；截至 2026-09-12 约 155k stars / 24.5k forks）
> 原文：https://github.com/langgenius/dify

![cover-v5-optimized](./images/GitHub_README_if.png)

<p align="center">
  <a href="https://cloud.dify.ai">Dify 云服务</a> ·
  <a href="https://docs.dify.ai/getting-started/install-self-hosted">自托管</a> ·
  <a href="https://docs.dify.ai">文档</a> ·
  <a href="https://dify.ai/pricing">Dify 产品形态总览</a>
</p>

<p align="center">
    <a href="https://dify.ai" target="_blank">
        <img alt="Static Badge" src="https://img.shields.io/badge/Product-F04438"></a>
    <a href="https://dify.ai/pricing" target="_blank">
        <img alt="Static Badge" src="https://img.shields.io/badge/free-pricing?logo=free&color=%20%23155EEF&label=pricing&labelColor=%20%23528bff"></a>
    <a href="https://discord.gg/FngNHpbcY7" target="_blank">
        <img src="https://img.shields.io/discord/1082486657678311454?logo=discord&labelColor=%20%235462eb&logoColor=%20%23f5f5f5&color=%20%235462eb"
            alt="chat on Discord"></a>
    <a href="https://reddit.com/r/difyai" target="_blank">
        <img src="https://img.shields.io/reddit/subreddit-subscribers/difyai?style=plastic&logo=reddit&label=r%2Fdifyai&labelColor=white"
            alt="join Reddit"></a>
    <a href="https://twitter.com/intent/follow?screen_name=dify_ai" target="_blank">
        <img src="https://img.shields.io/twitter/follow/dify_ai?logo=X&color=%20%23f5f5f5"
            alt="follow on X(Twitter)"></a>
    <a href="https://www.linkedin.com/company/langgenius/" target="_blank">
        <img src="https://custom-icon-badges.demolab.com/badge/LinkedIn-0A66C2?logo=linkedin-white&logoColor=fff"
            alt="follow on LinkedIn"></a>
    <a href="https://hub.docker.com/u/langgenius" target="_blank">
        <img alt="Docker Pulls" src="https://img.shields.io/docker/pulls/langgenius/dify-web?labelColor=%20%23FDB062&color=%20%23f79009"></a>
    <a href="https://github.com/langgenius/dify/graphs/commit-activity" target="_blank">
        <img alt="Commits last month" src="https://img.shields.io/github/commit-activity/m/langgenius/dify?labelColor=%20%2332b583&color=%20%2312b76a"></a>
    <a href="https://github.com/langgenius/dify/" target="_blank">
        <img alt="Issues closed" src="https://img.shields.io/github/issues-search?query=repo%3Alanggenius%2Fdify%20is%3Aclosed&label=issues%20closed&labelColor=%20%237d89b0&color=%20%235d6b98"></a>
    <a href="https://github.com/langgenius/dify/discussions/" target="_blank">
        <img alt="Discussion posts" src="https://img.shields.io/github/discussions/langgenius/dify?labelColor=%20%239b8afb&color=%20%237a5af8"></a>
    <a href="https://insights.linuxfoundation.org/project/langgenius-dify" target="_blank">
        <img alt="LFX Health Score" src="https://insights.linuxfoundation.org/api/badge/health-score?project=langgenius-dify"></a>
    <a href="https://insights.linuxfoundation.org/project/langgenius-dify" target="_blank">
        <img alt="LFX Contributors" src="https://insights.linuxfoundation.org/api/badge/contributors?project=langgenius-dify"></a>
    <a href="https://insights.linuxfoundation.org/project/langgenius-dify" target="_blank">
        <img alt="LFX Active Contributors" src="https://insights.linuxfoundation.org/api/badge/active-contributors?project=langgenius-dify"></a>
</p>

<p align="center">
  <a href="./README.md"><img alt="README in English" src="https://img.shields.io/badge/English-d9d9d9"></a>
  <a href="./docs/zh-TW/README.md"><img alt="繁體中文文件" src="https://img.shields.io/badge/繁體中文-d9d9d9"></a>
  <a href="./docs/zh-CN/README.md"><img alt="简体中文文件" src="https://img.shields.io/badge/简体中文-d9d9d9"></a>
  <a href="./docs/ja-JP/README.md"><img alt="日本語のREADME" src="https://img.shields.io/badge/日本語-d9d9d9"></a>
  <a href="./docs/es-ES/README.md"><img alt="README en Español" src="https://img.shields.io/badge/Español-d9d9d9"></a>
  <a href="./docs/fr-FR/README.md"><img alt="README en Français" src="https://img.shields.io/badge/Français-d9d9d9"></a>
  <a href="./docs/tlh/README.md"><img alt="README tlhIngan Hol" src="https://img.shields.io/badge/Klingon-d9d9d9"></a>
  <a href="./docs/ko-KR/README.md"><img alt="README in Korean" src="https://img.shields.io/badge/한국어-d9d9d9"></a>
  <a href="./docs/ar-SA/README.md"><img alt="README بالعربية" src="https://img.shields.io/badge/العربية-d9d9d9"></a>
  <a href="./docs/tr-TR/README.md"><img alt="Türkçe README" src="https://img.shields.io/badge/Türkçe-d9d9d9"></a>
  <a href="./docs/vi-VN/README.md"><img alt="README Tiếng Việt" src="https://img.shields.io/badge/Ti%E1%BA%BFng%20Vi%E1%BB%87t-d9d9d9"></a>
  <a href="./docs/de-DE/README.md"><img alt="README in Deutsch" src="https://img.shields.io/badge/German-d9d9d9"></a>
  <a href="./docs/it-IT/README.md"><img alt="README in Italiano" src="https://img.shields.io/badge/Italiano-d9d9d9"></a>
  <a href="./docs/pt-BR/README.md"><img alt="README em Português do Brasil" src="https://img.shields.io/badge/Portugu%C3%AAs%20do%20Brasil-d9d9d9"></a>
  <a href="./docs/sl-SI/README.md"><img alt="README Slovenščina" src="https://img.shields.io/badge/Sloven%C5%A1%C4%8Dina-d9d9d9"></a>
  <a href="./docs/bn-BD/README.md"><img alt="README in বাংলা" src="https://img.shields.io/badge/বাংলা-d9d9d9"></a>
  <a href="./docs/hi-IN/README.md"><img alt="README in हिन्दी" src="https://img.shields.io/badge/Hindi-d9d9d9"></a>
</p>

Dify 是一个开源的 LLM 应用开发平台。其直观的界面把 AI 工作流、RAG 管道、Agent 能力、模型管理、可观测性功能（包括 [Opik](https://www.comet.com/docs/opik/integrations/dify)、[Langfuse](https://docs.langfuse.com) 和 [Arize Phoenix](https://docs.arize.com/phoenix)）等结合在一起，让你能快速从原型走向生产。以下是它的核心功能列表：

## 快速开始

> 安装 Dify 之前，请确认你的机器满足以下最低系统要求：
>
> - CPU >= 2 核
> - 内存 >= 4 GiB

<br/>

启动 Dify 服务器最简单的方式是使用 [Docker Compose](docker/docker-compose.yaml)。在用下面的命令运行 Dify 之前，请确认机器上已经安装 [Docker](https://docs.docker.com/get-docker/) 和 Docker Compose v2.24.0 或更高版本：

```bash
cd dify
cd docker
cp .env.example .env
docker compose up -d
```

运行完成后，可以在浏览器中访问 [http://localhost/install](http://localhost/install) 进入 Dify 控制台，并开始初始化流程。

#### 寻求帮助

如果搭建 Dify 时遇到问题，请参阅我们的[常见问题](https://docs.dify.ai/getting-started/install-self-hosted/faqs)。如果问题仍未解决，请联系[社区和我们](#社区与联系方式)。

> 如果你想为 Dify 贡献代码或做额外开发，请参阅我们的[源码部署指南](https://docs.dify.ai/getting-started/install-self-hosted/local-source-code)。

## 核心功能

**1. 工作流**：
在可视化画布上构建并测试强大的 AI 工作流，利用以下所有能力以及更多功能。

**2. 全面的模型支持**：
与来自数十家推理提供商和自托管解决方案的数百个专有/开源 LLM 无缝集成，覆盖 GPT、Mistral、Llama3 以及任何与 OpenAI API 兼容的模型。受支持模型提供商的完整列表见[此处](https://docs.dify.ai/getting-started/readme/model-providers)。

![providers-v5](https://github.com/langgenius/dify/assets/13230914/5a17bdbe-097a-4100-8363-40255b70f6e3)

**3. Prompt IDE**：
直观的界面，用于编写提示词、比较模型表现，并为基于聊天的应用添加文本转语音等额外功能。

**4. RAG 管道**：
广泛的 RAG 能力，覆盖从文档摄入到检索的完整流程，开箱即用地支持从 PDF、PPT 及其他常见文档格式中抽取文本。

**5. Agent 能力**：
你可以基于 LLM 函数调用（Function Calling）或 ReAct 定义 Agent，并为 Agent 添加预置或自定义工具。Dify 为 AI Agent 提供 50 多个内置工具，例如 Google Search、DALL·E、Stable Diffusion 和 WolframAlpha。

**6. LLMOps**：
随时间监控和分析应用日志与性能。你可以基于生产数据和标注持续改进提示词、数据集与模型。

**7. 后端即服务（Backend-as-a-Service）**：
Dify 的所有能力都配有对应的 API，因此你可以轻松地把 Dify 集成进自己的业务逻辑。

## 使用 Dify

- **云服务 <br/>**
  我们托管了 [Dify 云服务](https://dify.ai)，任何人都可以零配置试用。它提供自部署版本的全部能力，并在沙盒计划中赠送 200 次免费 GPT-4 调用。如果你在使用 Dify 云服务时遇到问题，请[联系我们的云服务支持团队](mailto:cloud@dify.ai?subject=%5BGitHub%5DDify%20Cloud%20Support)。

- **自托管 Dify 社区版<br/>**
  参照这份[入门指南](#快速开始)，快速在你的环境中跑起 Dify。
  更多参考和更深入的说明，请使用我们的[文档](https://docs.dify.ai)。

- **面向企业/组织的 Dify<br/>**
  我们提供额外的企业级功能。[发邮件给我们](mailto:business@dify.ai?subject=%5BGitHub%5DBusiness%20License%20Inquiry)讨论你的企业需求。<br/>

## 保持领先

在 GitHub 上 Star Dify，即可第一时间收到新版本通知。

<img width="1344" height="720" alt="star" src="https://github.com/user-attachments/assets/dcd086d1-af0f-471b-ae52-1ad2fa040595" />

## 高级设置

如需自定义配置、可观测性与部署选项，请参阅[高级设置](docs/ADVANCED_SETUP.md)。

## 贡献

Dify 欢迎各种形式的贡献：

- **代码**：阅读[贡献指南](CONTRIBUTING.md)，然后浏览[适合新手的问题](https://github.com/langgenius/dify/issues?q=is%3Aissue%20state%3Aopen%20label%3A%22good%20first%20issue%22)。
- **想法与反馈**：发起或加入 [GitHub Discussion](https://github.com/langgenius/dify/discussions)。
- **翻译**：参照[国际化指南](web/i18n-config/README.md)添加或更新语言。
- **社区**：分享你构建的应用、帮助其他用户，并帮助传播 Dify。

### 贡献者

<a href="https://github.com/langgenius/dify/graphs/contributors">
  <img alt="Dify contributors" src="https://contrib.rocks/image?repo=langgenius/dify" />
</a>

## 社区与联系方式

请选择最适合你问题的渠道：

- [GitHub Discussions](https://github.com/langgenius/dify/discussions)：获取帮助、分享反馈并提出想法。
- [GitHub Issues](https://github.com/langgenius/dify/issues)：报告可复现的缺陷并跟踪工程进展。提交前请先阅读[贡献指南](CONTRIBUTING.md)。
- [Discord](https://discord.gg/FngNHpbcY7)：实时交流、分享你的应用，并与其他 Dify 用户建立联系。
- [X](https://x.com/dify_ai)：关注 Dify，获取版本新闻与项目动态。

## Star 历史

<a href="https://star-history.dera.page/#langgenius/dify&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://star-history.dera.page/svg?repos=langgenius/dify&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://star-history.dera.page/svg?repos=langgenius/dify&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://star-history.dera.page/svg?repos=langgenius/dify&type=date&legend=top-left" />
 </picture>
</a>

## 安全披露

为保护你的隐私，请不要在 GitHub 上发布安全问题。请改为发送邮件至 security@dify.ai，我们的团队会给出详细答复。

## 许可证

本仓库基于 [Dify Open Source License](LICENSE) 授权，该许可证以 Apache 2.0 为基础，并附加了一些条件。
