---
created: 2026-09-12
updated: 2026-09-12
type: prompt-draft
status: 过程稿
sources:
  - url: https://github.com/open-webui/open-webui
tags: [Open WebUI, 翻译, prompt, GitHub README]
---

# 02 本次翻译使用的提示词（过程稿）

> 本次翻译用如下提示词驱动。原文（英文 README）已抓取到
> `candidates/20260912-080217/sources/open-webui-open-webui---User-friendly-AI.md`
> （GitHub API `repos/open-webui/open-webui/readme`，仓库元数据取自 `repos/open-webui/open-webui`）。
> README 无官方简体中文版，本译文以英文 `main` 分支原文为唯一依据。

## 提示词正文

```
你是一名资深技术译者（英→中），翻译 GitHub 开源仓库 open-webui/open-webui 的主 README
（标题：User-friendly AI Interface (Supports Ollama, OpenAI API, ...)）。

## 输入
- 原文：candidates/20260912-080217/sources/open-webui-open-webui---User-friendly-AI.md
  （正文从 "# Open WebUI 👋" 到 "Created by Timothy Jaeryang Baek ... Let's make Open WebUI
   even more amazing together! 💪" 为止；忽略文件头部的采集元信息块、shields.io 状态徽章、
   Sponsor 徽章、demo.png 演示图、Star History 图表等站点噪声。）
- 仓库元数据（2026-09-12）：stars 151,673 / forks 22,191 / open issues 305 / watchers 660，
  主语言 Python，仓库创建 2023-10-06，homepage https://openwebui.com，
  许可证为带品牌保留附加条款的自定义许可（GitHub 标记 NOASSERTION）。

## 输出要求
1. 完整逐译正文全部段落、小标题、列表、提示块与代码块，不压缩、不删节；
   徽章 / 图表 / 演示图等 HTML 与图片链接原样保留，不翻译其中的 alt 周边文案。
2. 保留原文全部超链接（Markdown 链接写法原样保留，链接文字翻译成中文）；
   代码与标识符原样保留：pip install open-webui、open-webui serve、
   docker run -d -p 3000:8080 ...、-v open-webui:/app/backend/data、
   --add-host=host.docker.internal:host-gateway、--network=host、
   ghcr.io/open-webui/open-webui:main / :cuda / :ollama / :dev、
   OLLAMA_BASE_URL、OPENAI_API_KEY、HF_HUB_OFFLINE=1、http://localhost:8080、
   http://localhost:3000、127.0.0.1:11434 / host.docker.internal:11434 等。
3. 术语表（必须一致）：
   - self-hosted → 自托管；extensible → 可扩展；feature-rich → 功能丰富
   - provider-agnostic → 与提供商无关
   - RBAC / User Groups → 基于角色的访问控制（RBAC） / 用户组
   - Plugin Support → 插件支持；Filters / Actions / Pipes / Tools / Skills 保留英文
   - MCP / MCPO / OpenAPI tool servers 保留英文
   - Persistent Memory → 持久记忆；Channels → 频道；Automations → 自动化
   - Live Workflow & Message Flow → 实时工作流与消息流
   - Artifact / Persistent Artifact Storage → 产物 / 持久化产物存储
   - RAG / hybrid search / reranking / full-context mode → 检索增强生成（RAG）/
     混合检索 / 重排序 / 全上下文模式
   - Observability → 可观测性；OpenTelemetry 保留英文
   - Horizontal Scalability → 水平扩展；Provisioning → 用户开通 / 预置
   - arena / ELO-based leaderboards → 竞技场 / 基于 ELO 的排行榜
   - Dev Branch → dev 分支；Branding → 品牌标识
4. 数字与结论逐一比对原文，不得改动：30 条核心功能、生态 4 个项目、
   9 种向量数据库（ChromaDB / PGVector / Qdrant / Milvus / Elasticsearch / OpenSearch /
   Pinecone / S3Vector / Oracle 23ai）、oikb 45+ 数据源、需要 Python 3.11、
   pip 启动默认 8080 端口、Docker 默认 3000 端口、SCIM 2.0、ELO。
5. 中文表达通顺自然，术语到位；输出 Markdown，标题层级沿用原文；frontmatter：
   ---
   created: 2026-09-12
   updated: 2026-09-12
   title: open-webui/open-webui —— 用户友好的 AI 界面（支持 Ollama、OpenAI API 等）
   sourceUrl: https://github.com/open-webui/open-webui
   sourceAuthor: Open WebUI 官方团队（open-webui GitHub 组织）
   translatedAt: 2026-09-12
   sources: [references/articles.md 待处理队列]
   tags: [Open WebUI, 自托管, Ollama, OpenAI API, RAG, Agent, LLM 前端, type/翻译]
   ---
```

## 执行备注

- 抓取方式：GitHub API `repos/open-webui/open-webui/readme`（raw）取得权威正文；
  仓库元数据（stars / forks / issues / license / topics / created_at）取自
  `repos/open-webui/open-webui`；`demo.png` 与 Star History 图表为相对/外链资源，译文只保留引用。
- 翻译策略：术语优先 + 完整逐译；保留原文 `> [!NOTE]` / `> [!WARNING]` / `> [!TIP]`
  提示块语法与 30 条功能列表的原始顺序（与英文版一致，不做重排）。
- 关键数字比对：30 条功能 / 4 个生态项目 / 9 种向量库 / 45+ 数据源 / Python 3.11 /
  8080 与 3000 端口 / 镜像标签 :main :cuda :ollama :dev / HF_HUB_OFFLINE=1 已抽查一致；
  仓库热度数据以 2026-09-12 采集快照为准，属于时点值。
- 该提示词本身不直接沉淀进 prompts/（curate 产出边界：不写 prompts/），
  留待评审通过、实测后再考虑复用。
