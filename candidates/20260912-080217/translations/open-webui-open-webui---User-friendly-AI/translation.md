---
created: 2026-09-12
updated: 2026-09-12
type: translation-draft
status: 过程稿
sources:
  - title: open-webui/open-webui - User-friendly AI Interface (Supports Ollama, OpenAI API, ...)
    url: https://github.com/open-webui/open-webui
    source: github
    date: 2026-09-06
tags: [Open WebUI, 自托管, Ollama, OpenAI API, RAG, Agent, LLM 前端, 翻译]
---

# open-webui/open-webui —— 用户友好的 AI 界面（支持 Ollama、OpenAI API 等）

> 开源仓库：`open-webui/open-webui`（主语言 Python；截至 2026-09-12 约 151.7k stars / 22.2k forks）
> 原文：https://github.com/open-webui/open-webui

![GitHub stars](https://img.shields.io/github/stars/open-webui/open-webui?style=social)
![GitHub forks](https://img.shields.io/github/forks/open-webui/open-webui?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/open-webui/open-webui?style=social)
![GitHub repo size](https://img.shields.io/github/repo-size/open-webui/open-webui)
![GitHub language count](https://img.shields.io/github/languages/count/open-webui/open-webui)
![GitHub top language](https://img.shields.io/github/languages/top/open-webui/open-webui)
![GitHub last commit](https://img.shields.io/github/last-commit/open-webui/open-webui?color=red)
[![Discord](https://img.shields.io/badge/Discord-Open_WebUI-blue?logo=discord&logoColor=white)](https://discord.gg/5rJgQTnV4s)
[![](https://img.shields.io/static/v1?label=Sponsor&message=%E2%9D%A4&logo=GitHub&color=%23fe8e86)](https://github.com/sponsors/open-webui)

Open WebUI 是 **AI 之家（a home for AI）**，一个**[可扩展](https://docs.openwebui.com/features/extensibility/plugin/)**、**[功能丰富](https://docs.openwebui.com/features/)**、用户友好的**自托管** AI 平台，并被打造为可**[完全离线](https://openwebui.com/sovereign-ai)**运行。它支持 **Ollama** 与 **OpenAI 兼容 API**，为本地与云端模型提供一个强大、与提供商无关的界面。

对开源 AI 充满热情？[加入我们的团队 →](https://careers.openwebui.com/)

![Open WebUI Demo](./demo.png)

> [!TIP]  
> **正在寻找[企业版方案](https://docs.openwebui.com/enterprise)？** – **[立即与我们的销售团队联系！](https://docs.openwebui.com/enterprise)**

更多信息，请务必查看我们的 [Open WebUI 文档](https://docs.openwebui.com/)。

## Open WebUI 的核心功能 ⭐

- 🚀 **轻松安装**：通过 pip、uv、Docker 或 Kubernetes（kubectl、kustomize 或 helm）无缝安装，容器部署还提供带 `:ollama` 和 `:cuda` 标签的镜像。

- 🤝 **广泛的模型与 API 集成**：在本地 Ollama 模型之外，可接入任何 OpenAI 兼容 API。把 API URL 指向 **LMStudio、GroqCloud、Mistral、OpenRouter、vLLM 等**，即可自由混搭不同提供商。

- 🔐 **细粒度 RBAC 与用户组**：管理员可定义详细的角色、用户组与权限，让每个用户恰好获得其所需的访问权限。默认安全，并为不同用户组提供定制化体验。

- 🧩 **插件支持**：通过 **Filters**、**Actions**、**Pipes**、**Tools** 与 **Skills** 扩展 Open WebUI。通过 **MCP**、**MCPO** 与 **OpenAPI 工具服务器**接入外部服务。可构建自定义集成、速率限制、审批流、数据连接等。

- 🤖 **模型与 Agent**：用自定义指令、工具与知识封装任意基础模型，构建专用 Agent。支持动态变量、按用户/用户组的访问控制，并可通过 [Open WebUI 社区](https://openwebui.com/) 导入社区预设。

- 📝 **笔记**：为对话之外的内容提供专属工作区。用富文本编辑器起草，让 AI 改写选中文本，并把笔记附加到任意聊天以实现全上下文注入。

- 📢 **频道**：实时共享空间，让团队与 AI 模型在同一时间线上协作。可标注模型来起草或评审，支持话题串、表情回应、置顶与访问控制。

- 🧠 **持久记忆**：AI 能跨对话记住关于你的事实，把上下文从一次聊天延续到下一次。

- ✅ **实时工作流与消息流**：实时观看 AI 构建并逐项完成清单。在 AI 仍在回复时可排队消息，待其就绪后自动发送。

- 📅 **日历与 AI 日程安排**：内置个人与共享日历，支持月/周/日视图、重复事件、颜色标记、参与人与提醒。模型可通过原生函数调用，以对话方式管理你的日程。

- ⏱️ **自动化**：让提示词按周期性计划运行，运行记录呈现在日历上，每次完成的运行都会链接回它产生的聊天。

- 📱 **响应式设计与 PWA**：在桌面、笔记本与移动端提供无缝体验，并以渐进式 Web 应用（PWA）带来类原生手感，以及在 localhost 上的离线访问。

- ✒️🔢 **完整的 Markdown 与 LaTeX 支持**：全面的 Markdown 与 LaTeX 能力，让交互更丰富。

- 🎤📹 **免提语音/视频通话**：集成语音与视频通话，支持多家语音转文本提供商（Local Whisper、OpenAI、Deepgram、Azure）与文本转语音引擎（Azure、ElevenLabs、OpenAI、Transformers、WebAPI）。

- 💾 **持久化产物存储**：内置面向产物的键值存储 API，可支撑日志、追踪器、排行榜等协作工具，并区分个人与共享数据范围。

- 📚 **本地 RAG 集成**：检索增强生成（RAG）由 9 种向量数据库与多种内容抽取引擎（Tika、Docling、Document Intelligence、Mistral OCR、PaddleOCR-vl、外部加载器）支撑。支持带重排序的混合检索（BM25 + 向量）与全上下文模式。可用 `#` 命令把文档载入聊天，或从你的资料库中拉取。

- 🔍 **面向 RAG 的网页搜索**：通过数十家提供商搜索网络，包括 `SearXNG`、`Google PSE`、`Brave Search`、`Kagi`、`Mojeek`、`Tavily`、`Perplexity`、`Firecrawl`、`serpstack`、`serper`、`Serply`、`DuckDuckGo`、`SearchApi`、`SerpApi`、`Bing`、`Jina`、`Exa`、`Sougou`、`Azure AI Search` 与 `Ollama Cloud`，并将结果直接注入对话。

- 🌐 **网页浏览能力**：用 `#` 命令后接 URL 即可把网站拉入聊天，或在需要时让模型自行抓取。

- 🎨 **图像生成与编辑**：用多个引擎创建与编辑图像，包括 OpenAI DALL·E、Gemini、ComfyUI（本地）与 AUTOMATIC1111（本地），同时支持生成与基于提示词的编辑。

- ⚙️ **多模型对话**：同时与多个模型交互，并行发挥各自所长，以获得尽可能好的回答。

- 📊 **用量分析与模型评估**：管理员仪表盘可跟踪不同用户与模型的消息量、Token 消耗与成本。借助内置竞技场、A/B 测试与基于 ELO 的排行榜评估模型。

- 🗄️ **灵活的数据库与存储**：可选择 SQLite（支持可选加密）或 PostgreSQL，文件可存放于本地、S3、Google Cloud Storage 或 Azure Blob Storage。

- 🧬 **高级向量数据库支持**：可从 9 种向量数据库中选用：ChromaDB、PGVector、Qdrant、Milvus、Elasticsearch、OpenSearch、Pinecone、S3Vector 与 Oracle 23ai。

- 🪪 **企业级认证与用户开通**：完整的 LDAP / Active Directory 集成，通过可信标头与 OAuth 提供商实现 SSO，并针对 Okta、Azure AD、Google Workspace 等身份提供商支持 SCIM 2.0 自动开通。

- ☁️ **云原生文件集成**：原生支持 Google Drive 与 OneDrive/SharePoint 文件选择，从企业云存储无缝导入文档。

- 🔭 **生产级可观测性**：内置 OpenTelemetry 支持，覆盖追踪、指标与日志，可接入你现有的监控栈。

- ⚖️ **水平扩展**：由 Redis 支撑的会话管理与 WebSocket 支持，适合部署在负载均衡器之后的多 worker、多节点场景。

- 🌐🌍 **多语言支持**：借助 i18n 支持，用你偏好的语言使用 Open WebUI。我们正在积极寻找贡献者来扩展语言覆盖！

- 🌟 **持续更新**：我们持续通过定期更新、修复与新功能来改进 Open WebUI。

- 🛡️ **透明的安全流程**：安全报告会经过分诊、修复，并通过有文档记录的负责任披露流程以公开公告形式发布。参见我们的[安全策略](https://github.com/open-webui/open-webui/security)。

想进一步了解 Open WebUI 的功能？请查看我们的 [Open WebUI 文档](https://docs.openwebui.com/features)，获取全面概览！

## Open WebUI 生态 🌐

Open WebUI 是核心，四周环绕着配套应用与基础设施，它们扩展了你的 AI 能做什么、能触达哪里，以及你如何运行它：

- 💻 **Open WebUI Computer**（[open-webui/computer](https://github.com/open-webui/computer)）：一个独立的、移动优先的电脑与编码 Agent，运行在你自己的机器上。文件、终端与 git 都在一个浏览器标签页里，可从手机访问。可将其作为模型接入 Open WebUI，也可通过 Telegram、WhatsApp 等访问它。

- ⚡ **Open Terminal 与 Terminals（企业版）**（[open-webui/open-terminal](https://github.com/open-webui/open-terminal) 与 [open-webui/terminals](https://github.com/open-webui/terminals)）：一个自托管计算环境，可接入 Open WebUI，为 AI 提供在聊天中编写代码、运行、读取输出、修复错误并迭代的场所。Terminals 为每个用户提供隔离容器，具备独立凭据、资源限制与网络规则。在 Docker 或 Kubernetes 上自动管理生命周期。

- 🔄 **oikb**（[open-webui/oikb](https://github.com/open-webui/oikb)）：从 45+ 个数据源（GitHub、Confluence、ServiceNow、Salesforce、Jira、Slack、SharePoint、Notion 等）为你的知识库持续供给内容，让团队已在使用的工具保持同步。

- 🖥️ **原生桌面应用**（[open-webui/desktop](https://github.com/open-webui/desktop)）：在 macOS、Windows 与 Linux 上把 Open WebUI 作为原生应用运行。提供全系统 Spotlight 聊天栏、截图捕获、按键说话语音，以及通过内置 llama.cpp 引擎实现的可选完全本地推理。

想了解更多？请查看我们的 [Open WebUI 文档](https://docs.openwebui.com) 获取更多细节！

---

我们无比感谢赞助商的慷慨支持。他们的贡献帮助我们维护并改进项目，确保我们能持续为社区交付高质量的工作。谢谢！

## 如何安装 🚀

### 通过 Python pip 安装 🐍

可使用 Python 包安装器 pip 安装 Open WebUI。开始之前，请确保使用 **Python 3.11**，以避免兼容性问题。

1. **安装 Open WebUI**：
   打开终端并运行以下命令安装 Open WebUI：

   ```bash
   pip install open-webui
   ```

2. **运行 Open WebUI**：
   安装完成后，可执行以下命令启动 Open WebUI：

   ```bash
   open-webui serve
   ```

这将启动 Open WebUI 服务器，你可以通过 [http://localhost:8080](http://localhost:8080) 访问。

### 使用 Docker 快速开始 🐳

> [!NOTE]  
> 请注意，某些 Docker 环境可能需要额外配置。如果你遇到任何连接问题，我们的详细指南 [Open WebUI 文档](https://docs.openwebui.com/) 可为你提供帮助。

> [!WARNING]
> 使用 Docker 安装 Open WebUI 时，请务必在 Docker 命令中包含 `-v open-webui:/app/backend/data`。这一步至关重要，它能确保数据库被正确挂载，防止任何数据丢失。

> [!TIP]  
> 如果你希望使用内置 Ollama 或 CUDA 加速的 Open WebUI，我们建议使用带 `:cuda` 或 `:ollama` 标签的官方镜像。要启用 CUDA，你必须在 Linux/WSL 系统上安装 [Nvidia CUDA 容器工具包](https://docs.nvidia.com/dgx/nvidia-container-runtime-upgrade/)。

### 使用默认配置安装

- **如果 Ollama 就在你的电脑上**，使用此命令：

  ```bash
  docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
  ```

- **如果 Ollama 在另一台服务器上**，使用此命令：

  要连接另一台服务器上的 Ollama，请把 `OLLAMA_BASE_URL` 改为该服务器的 URL：

  ```bash
  docker run -d -p 3000:8080 -e OLLAMA_BASE_URL=https://example.com -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
  ```

- **要以 Nvidia GPU 支持运行 Open WebUI**，使用此命令：

  ```bash
  docker run -d -p 3000:8080 --gpus all --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:cuda
  ```

### 仅使用 OpenAI API 的安装方式

- **如果你只使用 OpenAI API**，使用此命令：

  ```bash
  docker run -d -p 3000:8080 -e OPENAI_API_KEY=your_secret_key -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
  ```

### 安装内置 Ollama 支持的 Open WebUI

这种安装方式使用一个将 Open WebUI 与 Ollama 打包在一起的单一容器镜像，只需一条命令即可完成简洁的搭建。请根据你的硬件情况选择相应的命令：

- **带 GPU 支持**：
  运行以下命令以利用 GPU 资源：

  ```bash
  docker run -d -p 3000:8080 --gpus=all -v ollama:/root/.ollama -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:ollama
  ```

- **仅 CPU**：
  如果不使用 GPU，请改用此命令：

  ```bash
  docker run -d -p 3000:8080 -v ollama:/root/.ollama -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:ollama
  ```

这两条命令都能轻松完成 Open WebUI 与 Ollama 的内置安装，让你迅速把一切运行起来。

安装完成后，你可以在 [http://localhost:3000](http://localhost:3000) 访问 Open WebUI。祝你使用愉快！😄

### 其他安装方式

我们提供多种安装替代方案，包括非 Docker 的原生安装方式、Docker Compose、Kustomize 与 Helm。请访问我们的 [Open WebUI 文档](https://docs.openwebui.com/getting-started/) 或加入我们的 [Discord 社区](https://discord.gg/5rJgQTnV4s) 获取完整指引。

### 故障排查

遇到连接问题？我们的 [Open WebUI 文档](https://docs.openwebui.com/troubleshooting/) 已经为你准备好了。如需更多帮助并加入我们活跃的社区，请访问 [Open WebUI Discord](https://discord.gg/5rJgQTnV4s)。

#### Open WebUI：服务器连接错误

如果你遇到连接问题，通常是因为 WebUI 的 Docker 容器无法在容器内部访问 127.0.0.1:11434（host.docker.internal:11434）上的 Ollama 服务器。可在 docker 命令中使用 `--network=host` 标志来解决。注意端口会从 3000 变为 8080，因此链接变为 `http://localhost:8080`。

**示例 Docker 命令**：

```bash
docker run -d --network=host -v open-webui:/app/backend/data -e OLLAMA_BASE_URL=http://127.0.0.1:11434 --name open-webui --restart always ghcr.io/open-webui/open-webui:main
```

### 保持 Docker 安装为最新

请查看我们 [Open WebUI 文档](https://docs.openwebui.com/getting-started/updating) 中的更新指南。

### 使用 dev 分支 🌙

> [!WARNING]
> `:dev` 分支包含最新的不稳定功能与变更。使用风险自负，它可能存在缺陷或未完成的功能。

如果你想尝试最新的前沿功能，并能接受偶发的不稳定，可以这样使用 `:dev` 标签：

```bash
docker run -d -p 3000:8080 -v open-webui:/app/backend/data --name open-webui --add-host=host.docker.internal:host-gateway --restart always ghcr.io/open-webui/open-webui:dev
```

### 离线模式

如果你在离线环境中运行 Open WebUI，可以将 `HF_HUB_OFFLINE` 环境变量设为 `1`，以阻止从互联网下载模型的尝试。

```bash
export HF_HUB_OFFLINE=1
```

## 下一步是什么？🌟

在 [Open WebUI 文档](https://docs.openwebui.com/roadmap/) 中查看我们路线图上的即将推出的功能。

## 许可证 📜

本项目包含多种许可证下的代码。当前代码库中的组件依据 Open WebUI License 授权，并附加保留 "Open WebUI" 品牌标识的额外要求；同时也包含依据各自原始许可证授权的历史贡献。有关许可证变更的详细记录以及各代码段所适用的条款，请参阅 [LICENSE_HISTORY](./LICENSE_HISTORY)。完整且最新的许可详情，请参见 [LICENSE](./LICENSE) 与 [LICENSE_HISTORY](./LICENSE_HISTORY) 文件。

## 支持 💬

如果你有任何问题、建议或需要帮助，请提交 issue，或加入我们的 [Open WebUI Discord 社区](https://discord.gg/5rJgQTnV4s) 与我们联系！🤝

## 安全 🛡️

如果你认为自己发现了安全漏洞，或发现不应公开披露的问题，请通过 GitHub 上的[负责任披露项目](https://github.com/open-webui/open-webui/security)以保密方式联系我们。我们只接受通过 GitHub 提交的报告，不接受任何其他平台。感谢你帮助 Open WebUI 保持安全！

## Star 历史

<a href="https://star-history.com/#open-webui/open-webui&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=open-webui/open-webui&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=open-webui/open-webui&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=open-webui/open-webui&type=Date" />
  </picture>
</a>

---

由 [Timothy Jaeryang Baek](https://github.com/tjbck) 创建 —— 让我们一起把 Open WebUI 做得更出色！💪
