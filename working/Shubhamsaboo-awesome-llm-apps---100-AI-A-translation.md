---
created: 2026-09-12
updated: 2026-09-12
title: Shubhamsaboo/awesome-llm-apps —— 100+ AI 智能体、智能体技能与 RAG 应用（免费开源）
sourceUrl: https://github.com/Shubhamsaboo/awesome-llm-apps
sourceAuthor: Shubham Saboo（Shubhamsaboo / Unwind AI）
translatedAt: 2026-09-12
sources: [references/articles.md 待处理队列]
tags: [awesome-llm-apps, Agent, RAG, Agent Skills, MCP, 开源模板, type/翻译]
---

> 开源仓库：`Shubhamsaboo/awesome-llm-apps`（主语言 Python；截至 2026-09-12 约 137.2k stars / 20.2k forks；Apache-2.0）
> 原文：https://github.com/Shubhamsaboo/awesome-llm-apps

<p align="center">
  <a href="http://www.theunwindai.com">
    <img src="docs/banner/unwind_black.png" width="900px" alt="Unwind AI">
  </a>
</p>

<div align="center">

# Awesome LLM Apps

**100+ 开源 AI 智能体、智能体技能与 RAG 应用。手工构建、端到端测试、Apache-2.0。**

克隆它、发布它、卖掉它 —— 100% 免费开源

支持 Claude、Gemini、GPT、DeepSeek、Llama、Qwen 及其他开源模型。

**[Unwind AI 上的分步教程](https://www.theunwindai.com)** · **[快速开始](#-run-one-now)** · **[浏览全部模板](#-browse-all-templates)**

<a href="https://trendshift.io/repositories/9876" target="_blank">
  <img src="https://trendshift.io/api/badge/repositories/9876" width="220" alt="Featured on Trendshift as the #1 repository of the day">
</a>

<br>

</div>

<table>
  <tr>
    <td width="33.3%" align="center">
      <a href="agent_skills/project-graveyard/"><img src="docs/gallery/project-graveyard.png" alt="Project Graveyard: an agent that autopsies your dead side projects"></a>
      <sub><b>Project Graveyard</b></sub>
    </td>
    <td width="33.3%" align="center">
      <a href="voice_ai_agents/insurance_claim_live_agent_team/"><img src="docs/gallery/insurance-claim-live-team.png" alt="Insurance Claim Live Agent Team: voice claims settled in real time"></a>
      <sub><b>Insurance Claim Live Agent Team</b></sub>
    </td>
    <td width="33.3%" align="center">
      <a href="advanced_ai_agents/single_agent_apps/ai_fraud_investigation_agent/"><img src="docs/gallery/ai-fraud-investigation.png" alt="AI Fraud Investigation Agent: public records, cross-examined"></a>
      <sub><b>AI Fraud Investigation Agent</b></sub>
    </td>
  </tr>
  <tr>
    <td align="center">
      <a href="agent_skills/self-improving-agent-skills/"><img src="docs/gallery/self-improving-agent-skills.png" alt="Self-Improving Agent Skills: skills that rewrite themselves against evals"></a>
      <sub><b>Self-Improving Agent Skills</b></sub>
    </td>
    <td align="center">
      <a href="advanced_ai_agents/multi_agent_apps/ai_home_renovation_agent"><img src="docs/gallery/ai-home-renovation.png" alt="AI Home Renovation Agent: photo in, photoreal redesign out"></a>
      <sub><b>AI Home Renovation Agent</b></sub>
    </td>
    <td align="center">
      <a href="always_on_agents/always_on_hn_briefing_agent/"><img src="docs/gallery/always-on-hn-briefing.png" alt="Always-on HN Briefing Agent: it reads Hacker News while you sleep"></a>
      <sub><b>Always-on HN Briefing Agent</b></sub>
    </td>
  </tr>
</table>

## 🚀 Run one now

给编码代理 10 秒钟装上一个新技能：

```bash
npx skills add https://github.com/Shubhamsaboo/awesome-llm-apps/tree/main/agent_skills/project-graveyard
```

然后问它：*"why do I never finish my side projects?"（我为什么总也完不成副业项目？）*

或者克隆并在 30 秒内运行任意智能体：

```bash
git clone https://github.com/Shubhamsaboo/awesome-llm-apps.git
cd awesome-llm-apps/starter_ai_agents/ai_travel_agent
pip install -r requirements.txt
streamlit run travel_agent.py
```

> 📬 每周都有新模板上线。[在 Unwind AI 订阅，直接送进你的收件箱](https://www.theunwindai.com)。

## 🙏 Thanks to our sponsors

<table align="center" cellpadding="16" cellspacing="12">
  <tr>
    <td align="center">
      <a href="https://devtoolsacademy.link/shubham" target="_blank" rel="noopener" title="Vorflux">
        <img src="docs/banner/sponsors/vorflux.png" alt="Vorflux" width="500">
      </a>
      <br>
      <a href="https://devtoolsacademy.link/shubham" target="_blank" rel="noopener" style="text-decoration: none; color: #333; font-weight: bold; font-size: 18px;">
        Vorflux
      </a>
    </td>
    <td align="center">
      <a href="https://sponsorunwindai.com/" title="Become a Sponsor">
        <img src="docs/banner/sponsor_awesome_llm_apps.png" alt="Become a Sponsor" width="500">
      </a>
      <br>
      <a href="https://sponsorunwindai.com/" style="text-decoration: none; color: #333; font-weight: bold; font-size: 18px;">
        Become a Sponsor
      </a>
    </td>
  </tr>
</table>

## 📂 Browse all templates

### 🧩 Agent Skills

*给你的编码代理装上新的能力。一条命令安装，用大白话使用。每个技能都附带真实代码，并通过安全 + 评测 CI 门禁。适配 Claude Code、Codex、Cursor 及其他编码代理。[浏览全部技能 →](agent_skills/)*

*   [⚰️ Project Graveyard](agent_skills/project-graveyard/) - 找出你放弃的每一个副业项目，说明它们各自为何死掉，并帮你完成那个值得回头再做的
*   [👁️ First Reader](agent_skills/first-reader/) - 模拟真实读者读你的稿子，报告他们在哪里失去兴趣、在哪里停下、读完后还记得什么，且一个字都不改你的原文
*   [🔭 Scope Creep Detector](agent_skills/scope-creep-detector/) - 检查一个 diff 是否超出了它声称的意图，并建议哪些该保留、拆分或给出理由
*   [🏺 Commit Archaeologist](agent_skills/commit-archaeologist/) - 从引入某文件或代码区域的提交、后续改动、共同变更与意图线索中，重建它为何存在
*   [🩺 Dependency Doctor](agent_skills/dependency-doctor/) - 检查依赖清单中的标准库钉子、过时的 backport、未锁定版本、重复约束与被撤回（yanked）的发布
*   [🧠 Advisor Orchestrator Worker](agent_skills/advisor-orchestrator-worker/) - 以 Claude Fable 5.1 为顾问、GPT-6 Astra 为编排者、Gemini 3.8 Flash 为执行者的元循环
*   [♾️ Self-Improving Agent Skills](agent_skills/self-improving-agent-skills/) - 使用 Gemini 与 ADK 自动优化智能体技能

### 🌱 Starter AI Agents

*只需一个 API key 就能运行的单文件智能体 —— 绝佳的起点。*

*   [🎙️ AI Blog to Podcast Agent](starter_ai_agents/ai_blog_to_podcast_agent/) - 把任意博客 URL 变成有旁白的播客单集
*   [❤️‍🩹 AI Breakup Recovery Agent](starter_ai_agents/ai_breakup_recovery_agent/) - 一支陪你走过分手后情绪漩涡的智能体团队
*   [📊 AI Data Analysis Agent](starter_ai_agents/ai_data_analysis_agent/) - 用自然语言向任意 CSV 或 Excel 文件提问
*   [🩻 AI Medical Imaging Agent](starter_ai_agents/ai_medical_imaging_agent/) - 用 Gemini 对 X 光片与扫描影像做诊断分析
*   [😂 AI Meme Generator Agent (Browser)](starter_ai_agents/ai_meme_generator_agent_browseruse/) - 通过驱动真实浏览器制作表情包，而非调用图像 API
*   [🎵 AI Music Generator Agent](starter_ai_agents/ai_music_generator_agent/) - 输入提示词，输出 MP3 音轨
*   [🛫 AI Travel Agent (Local & Cloud)](starter_ai_agents/ai_travel_agent/) - 个性化的逐日旅行行程
*   [💸 AI x402 Paying Agent](starter_ai_agents/ai_x402_paying_agent/) - 带钱包的智能体，按调用为其所需数据付费 —— 无需 API key
*   [✨ Gemini Multimodal Agent](starter_ai_agents/multimodal_ai_agent/) - 单个智能体同时完成视频分析与网页搜索
*   [🔄 Mixture of Agents](starter_ai_agents/mixture_of_agents/) - 多个 LLM 作答，由一个汇总出最佳回答
*   [📊 xAI Finance Agent](starter_ai_agents/xai_finance_agent/) - 由 Grok 驱动的实时股票分析
*   [🔍 OpenAI Research Agent](starter_ai_agents/openai_research_agent/) - 用 OpenAI Agents SDK 做多智能体主题研究
*   [🕸️ Web Scraping AI Agent](starter_ai_agents/web_scraping_ai_agent/) - 描述你要抽取的内容，智能体就去抓取

### 🚀 Advanced AI Agents

*带工具、记忆与多步推理的生产级风格智能体。*

*   [🏚️ 🍌 AI Home Renovation Agent with Nano Banana Pro](advanced_ai_agents/multi_agent_apps/ai_home_renovation_agent) - 输入你空间的照片，输出改造方案与照片级效果图
*   [🧠 DevPulse AI - Multi-Agent Signal Intelligence](advanced_ai_agents/multi_agent_apps/devpulse_ai/) - 聚合并为技术信号打分，生成每日情报摘要
*   [🔍 AI Deep Research Agent](advanced_ai_agents/single_agent_apps/ai_deep_research_agent/) - 用 OpenAI Agents SDK 与 Firecrawl 做全面网络研究
*   [📊 AI VC Due Diligence Agent Team](advanced_ai_agents/multi_agent_apps/agent_teams/ai_vc_due_diligence_agent_team) - 用 Gemini 3 做多智能体创业投资分析
*   [🔬 AI Research Planner & Executor (Google Interactions API)](advanced_ai_agents/single_agent_apps/research_agent_gemini_interaction_api) - 带状态化对话与自动生成信息图的多阶段研究
*   [🤝 AI Consultant Agent](advanced_ai_agents/single_agent_apps/ai_consultant_agent) - 结合实时网络研究的市场分析与战略建议
*   [🏗️ AI System Architect Agent](advanced_ai_agents/single_agent_apps/ai_system_architect_r1/) - 用 DeepSeek R1 推理加 Claude 做架构评审
*   [💰 AI Financial Coach Agent](advanced_ai_agents/multi_agent_apps/ai_financial_coach_agent/) - 个性化的预算、债务与储蓄分析
*   [🎬 AI Movie Production Agent](advanced_ai_agents/single_agent_apps/ai_movie_production_agent/) - 从一句话电影构思产出剧本草稿与选角想法
*   [📈 AI Investment Agent](advanced_ai_agents/single_agent_apps/ai_investment_agent/) - 基于 Yahoo Finance 数据的股票对比报告
*   [📡 Earnings Call Analyst Agent](advanced_ai_agents/single_agent_apps/earnings_call_analyst_agent/) - 把 YouTube 财报电话会变成与播放同步的分析师工作台
*   [🏋️‍♂️ AI Health & Fitness Agent](advanced_ai_agents/single_agent_apps/ai_health_fitness_agent/) - 依据你的目标定制饮食与训练计划
*   [🚀 AI Product Launch Intelligence Agent](advanced_ai_agents/multi_agent_apps/product_launch_intelligence_agent) - 关于竞品发布的上市情报
*   [🔍 AI Fraud Investigation Agent](advanced_ai_agents/single_agent_apps/ai_fraud_investigation_agent/) - 交叉比对公开记录，标记数据对不上的设施
*   [🗞️ AI Journalist Agent](advanced_ai_agents/single_agent_apps/ai_journalist_agent/) - 就任意主题做研究、写作与编辑
*   [🧠 AI Mental Wellbeing Agent](advanced_ai_agents/multi_agent_apps/ai_mental_wellbeing_agent/) - 协同工作的智能体团队，制定心理健康支持方案
*   [📑 AI Meeting Agent](advanced_ai_agents/single_agent_apps/ai_meeting_agent/) - 在你走进会议室前备好背景、行业洞察与战略简报
*   [🧬 AI Self-Evolving Agent](advanced_ai_agents/multi_agent_apps/ai_self_evolving_agent/) - 用 EvoAgentX 重写自身工作流的智能体
*   [👨🏻‍💼 AI Sales Intelligence Agent Team](advanced_ai_agents/multi_agent_apps/agent_teams/ai_sales_intelligence_agent_team) - 实时生成竞争性销售作战卡
*   [🎧 AI Social Media News and Podcast Agent](advanced_ai_agents/multi_agent_apps/ai_news_and_podcast_agents/) - 把你信任的信源整理成简报与生成的播客
*   [🌐 Openwork - Open Browser Automation Agent](https://github.com/accomplish-ai/coworker) <sub>↗ external</sub> - 操作真实浏览器的开源智能体
*   [🛡️ Trust-Gated Multi-Agent Research Team](advanced_ai_agents/multi_agent_apps/trust_gated_agent_team/) - 每个智能体都经过验证，每个动作都有哈希链审计轨迹

### 🛰️ Always-on Agents

*按计划或事件在后台运行的智能体：监控变化中的上下文、判断什么值得关注，并主动推送更新、产物或动作。*

*   [📰 Always-on Hacker News Briefing Agent](always_on_agents/always_on_hn_briefing_agent/) - 定时的侦察兵，把排序后的每日简报发到 Slack 或邮箱
*   [📡 Release Radar Agent](always_on_agents/release_radar_agent/) - 盯梢依赖发布，就破坏性变更、弃用、安全与主版本变更向你简报

### 🤝 Multi-agent Teams

*多个智能体协作，完成复杂的跨领域任务。*

*   [🧲 AI Competitor Intelligence Agent Team](advanced_ai_agents/multi_agent_apps/agent_teams/ai_competitor_intelligence_agent_team/) - 从竞品自家网站出发，产出结构化的竞品拆解
*   [💲 AI Finance Agent Team](advanced_ai_agents/multi_agent_apps/agent_teams/ai_finance_agent_team/) - 20 行 Python 搭出一个金融分析师团队
*   [🎨 AI Game Design Agent Team](advanced_ai_agents/multi_agent_apps/agent_teams/ai_game_design_agent_team/) - 由一群设计专家产出完整的游戏概念
*   [🧭 AG2 Adaptive Research Team](advanced_ai_agents/multi_agent_apps/agent_teams/ag2_adaptive_research_team/) - 基于 AG2 构建、带路由与回退的智能体团队协作
*   [👨‍⚖️ AI Legal Agent Team (Cloud & Local)](advanced_ai_agents/multi_agent_apps/agent_teams/ai_legal_agent_team/) - 由一整座法律团队完成研究、合同分析与策略
*   [💼 AI Recruitment Agent Team](advanced_ai_agents/multi_agent_apps/agent_teams/ai_recruitment_agent_team/) - 从简历筛选到面试安排，端到端完成
*   [🏠 AI Real Estate Agent Team](advanced_ai_agents/multi_agent_apps/agent_teams/ai_real_estate_agent_team) - 找房、市场分析与推荐
*   [👨‍💼 AI Services Agency (CrewAI)](advanced_ai_agents/multi_agent_apps/agent_teams/ai_services_agency/) - 一家为你的软件项目做需求界定与规划的数字代理公司
*   [👨‍🏫 AI Teaching Agent Team](advanced_ai_agents/multi_agent_apps/agent_teams/ai_teaching_agent_team/) - 一支为你搭建完整学习路径的智能体教师团队
*   [💻 Multimodal Coding Agent Team](advanced_ai_agents/multi_agent_apps/agent_teams/multimodal_coding_agent_team/) - 拍下编码问题的照片，拿到沙箱中验证过的解法
*   [✨ Multimodal Design Agent Team](advanced_ai_agents/multi_agent_apps/agent_teams/multimodal_design_agent_team/) - 由 Gemini 驱动的专家小组给出设计批评
*   [🎨 🍌 Multimodal UI/UX Feedback Agent Team](advanced_ai_agents/multi_agent_apps/agent_teams/multimodal_uiux_feedback_agent_team/) - 落地页反馈，外加自动生成的改进版本
*   [🌏 AI Travel Planner Agent Team](advanced_ai_agents/multi_agent_apps/agent_teams/ai_travel_planner_agent_team/) - 由一支团队精心打造的完整旅行行程

### 🗣️ Voice AI Agents

*使用实时语音 API 的「语音进、语音出」智能体。*

*   [🗣️ AI Audio Tour Agent](voice_ai_agents/ai_audio_tour_agent/) - 依据你的位置、兴趣与节奏生成自助语音导览
*   [📞 Customer Support Voice Agent](voice_ai_agents/customer_support_voice_agent/) - 以你自己的文档为依据的语音客服
*   [🛡️ Insurance Claim Live Agent Team](voice_ai_agents/insurance_claim_live_agent_team/) - 用 Gemini Live 做实时语音理赔受理
*   [🔊 Voice RAG Agent (OpenAI SDK)](voice_ai_agents/voice_rag_openaisdk/) - 向你的 PDF 提问，然后听答案
*   [🎙️ OpenSource Voice Dictation Agent (Wispr Flow clone)](https://github.com/akshayaggarwal99/jarvis-ai-assistant) <sub>↗ external</sub> - 你说话它就打字的地方开源听写工具

### 🖼️ Generative UI and Agentic Frontends

*渲染交互式 UI 组件（表单、卡片、图表、可编辑计划）而不只是文本的智能体。*

*   [🗂️ Generative UI Starter Project](generative_ui_agents/generative-ui-starter-project/) - 一个由对话驱动、你和智能体共同操作的看板
*   [🪙 AI Financial Coach Agent](generative_ui_agents/ai-financial-coach-agent/) - 预算、储蓄与债务计划渲染为交互式卡片
*   [📊 AI Dashboard Canvas Agent](generative_ui_agents/ai-dashboard-canvas-agent/) - 在对话中描述仪表盘，图表在实时画布上组装出来
*   [🛠️ AI MCP App Builder](generative_ui_agents/ai-mcp-app-builder/) - 描述一个 MCP 应用，拿回一个实时沙箱实例
*   [✈️ MCP Apps Generative UI Showcase](generative_ui_agents/mcp-apps-generative-ui-showcase/) - 渲染真实交互式 UI 的 MCP 应用，含航班搜索
*   [🎛️ AI Shadcn Component Generator](generative_ui_agents/ai-shadcn-component-generator/) - 聊着天就得到可用于生产的 shadcn 组件
*   [🔍 AI Deep Research Agent](generative_ui_agents/ai-deep-research-agent/) - 每一次工具调用都渲染为实时工作区卡片的研究

### 🎮 Autonomous Game-Playing Agents

*端到端玩游戏的智能体：推理、策略与行动。*

*   [🎮 AI 3D Pygame Agent](advanced_ai_agents/autonomous_game_playing_agent_apps/ai_3dpygame_r1/) - DeepSeek R1 编写 PyGame 代码，浏览器智能体实时运行
*   [♜ AI Chess Agent](advanced_ai_agents/autonomous_game_playing_agent_apps/ai_chess_agent/) - 白方智能体对阵黑方智能体，走子经过校验
*   [🎲 AI Tic-Tac-Toe Agent](advanced_ai_agents/autonomous_game_playing_agent_apps/ai_tic_tac_toe_agent/) - 两个不同的 LLM 一步步对弈

### ♾️ MCP AI Agents

*通过 Model Context Protocol（模型上下文协议）连接外部工具与数据的智能体。*

*   [♾️ Browser MCP Agent](mcp_ai_agents/browser_mcp_agent/) - 用自然语言经由 MCP 驱动真实浏览器
*   [🐙 GitHub MCP Agent](mcp_ai_agents/github_mcp_agent/) - 用大白话探索和分析任意仓库
*   [📑 Notion MCP Agent](mcp_ai_agents/notion_mcp_agent) - 从终端与你的 Notion 页面对话
*   [🌍 AI Travel Planner MCP Agent](mcp_ai_agents/ai_travel_planner_mcp_agent_team) - 基于 Airbnb 与 Google Maps 实时数据构建的行程
*   [🔀 Multi-MCP Agent Router](mcp_ai_agents/multi_mcp_agent_router/) - 专家智能体，各自接入自己的 MCP 服务器
*   [🔌 OpenAI Remote MCP Tool Bridge](mcp_ai_agents/openai_remote_mcp_bridge/) - 把 OpenAI 函数调用直接接到远程 MCP 服务器

### 📀 RAG (Retrieval Augmented Generation)

*检索管道，从简单链路到智能体式、多源检索。*

*   [🔥 Agentic RAG with Embedding Gemma](rag_tutorials/agentic_rag_embedding_gemma) - 用 EmbeddingGemma 与 Llama 3.2 构建完全本地的智能体式 RAG
*   [🧐 Agentic RAG with Reasoning](rag_tutorials/agentic_rag_with_reasoning/) - 观察智能体检索时的逐步推理过程
*   [📰 AI Blog Search (RAG)](rag_tutorials/ai_blog_search/) - 基于 LangGraph 的博客内容智能体式搜索
*   [🔍 Autonomous RAG](rag_tutorials/autonomous_rag/) - GPT-4o 从你的 PDF 作答，必要时回退到网络搜索
*   [🔄 Contextual AI RAG Agent](rag_tutorials/contextualai_rag_agent/) - 托管式 RAG：几分钟内从数据存储到有依据的对话
*   [🔄 Corrective RAG (CRAG)](rag_tutorials/corrective_rag/) - 会自我评分并在作答前重试的检索
*   [📎 Typed Agentic RAG with Pydantic AI](rag_tutorials/agentic_typed_rag_pydanticai/) - 带精确引用、经过校验的回答；证据不足时拒绝作答
*   [🐋 Deepseek Local RAG Agent](rag_tutorials/deepseek_local_rag_agent/) - 在你自己的文档上做本地 DeepSeek 推理
*   [🤔 Gemini Agentic RAG](rag_tutorials/gemini_agentic_rag/) - 用 Gemini Flash Thinking 做查询改写与网络回退
*   [👀 Hybrid Search RAG (Cloud)](rag_tutorials/hybrid_search_rag/) - 关键词加向量检索，为 Claude 提供上下文
*   [🔄 Llama 3.1 Local RAG](rag_tutorials/llama3.1_local_rag/) - 与任意网页对话，完全离线
*   [🖥️ Local Hybrid Search RAG](rag_tutorials/local_hybrid_search_rag/) - 混合检索，全部在你本机运行
*   [🧬 Multimodal Agentic RAG](rag_tutorials/multimodal_agentic_rag/) - 文本、PDF、图像、音频与视频，均带引用作答
*   [🦙 Local RAG Agent](rag_tutorials/local_rag_agent/) - Llama 3.2 加 Qdrant，无需 API key
*   [🧩 RAG-as-a-Service](rag_tutorials/rag-as-a-service/) - 不到 50 行代码的生产级 RAG 服务
*   [✨ RAG Agent with Cohere](rag_tutorials/rag_agent_cohere/) - Command R7B 检索，带回退网络搜索
*   [⛓️ Basic RAG Chain](rag_tutorials/rag_chain/) - 最小检索管道，应用于制药研究
*   [📠 RAG with Database Routing](rag_tutorials/rag_database_routing/) - 自动把每个问题路由到正确的数据库
*   [🖼️ Vision RAG](rag_tutorials/vision_rag/) - 用 Embed-4 就图像与 PDF 页面提问
*   [🩺 RAG Failure Diagnostics Clinic](rag_tutorials/rag_failure_diagnostics_clinic/) - 系统性地找出你的 RAG 管道为什么出错
*   [🕸️ Knowledge Graph RAG with Citations](rag_tutorials/knowledge_graph_rag_citations/) - 带可验证来源归因的多跳回答

### 💾 LLM Apps with Memory

*跨会话记住对话与用户状态的智能体与聊天机器人。*

*   [💾 AI ArXiv Agent with Memory](advanced_llm_apps/llm_apps_with_memory_tutorials/ai_arxiv_agent_memory/) - 记住你研究兴趣的论文搜索
*   [🛩️ AI Travel Agent with Memory](advanced_llm_apps/llm_apps_with_memory_tutorials/ai_travel_agent_memory/) - 记住你偏好的旅行助手
*   [💬 Llama3 Stateful Chat](advanced_llm_apps/llm_apps_with_memory_tutorials/llama3_stateful_chat/) - 与 Llama 3 进行跨会话持久化的对话
*   [📝 LLM App with Personalized Memory](advanced_llm_apps/llm_apps_with_memory_tutorials/llm_app_personalized_memory/) - 跨对话保持上下文的聊天机器人
*   [🗄️ Local ChatGPT Clone with Memory](advanced_llm_apps/llm_apps_with_memory_tutorials/local_chatgpt_with_memory/) - 完全本地，每个用户各有个人记忆
*   [🧠 Multi-LLM Application with Shared Memory](advanced_llm_apps/llm_apps_with_memory_tutorials/multi_llm_memory/) - 不同模型共享同一份对话记忆

### 💬 Chat with X

*把任意数据源变成聊天界面。*

*   [💬 Chat with GitHub (GPT & Llama3)](advanced_llm_apps/chat_with_X_tutorials/chat_with_github/) - 任意仓库，用 30 行 RAG 回答
*   [📨 Chat with Gmail](advanced_llm_apps/chat_with_X_tutorials/chat_with_gmail/) - 向你的收件箱提问
*   [📄 Chat with PDF (GPT & Llama3)](advanced_llm_apps/chat_with_X_tutorials/chat_with_pdf/) - 经典之作，30 行 Python
*   [📚 Chat with Research Papers (ArXiv) (GPT & Llama3)](advanced_llm_apps/chat_with_X_tutorials/chat_with_research_papers/) - 用 GPT-4o 以对话方式探索 arXiv
*   [📝 Chat with Substack](advanced_llm_apps/chat_with_X_tutorials/chat_with_substack/) - 与任意 newsletter 的存档对话
*   [📽️ Chat with YouTube Videos](advanced_llm_apps/chat_with_X_tutorials/chat_with_youtube_videos/) - 通过字幕向视频提问

### 🎯 LLM Optimization Tools

*在不损失质量的前提下，减少 token 用量、上下文长度与 API 成本。*

*   [🎯 Toonify Token Optimization](advanced_llm_apps/llm_optimization_tools/toonify_token_optimization/) - 用 TOON 格式把 LLM API 成本降低 30-60%
*   [🧠 Headroom Context Optimization](advanced_llm_apps/llm_optimization_tools/headroom_context_optimization/) - 把 LLM API 成本降低 50-90%

### 🔧 LLM Fine-tuning

*面向开源模型的端到端微调配方。*

*   [🦥 Gemma 3 Fine-tuning](advanced_llm_apps/llm_finetuning_tutorials/gemma3_finetuning/) - 用 Unsloth 做 4-bit LoRA，代码小而易读
*   [🦙 Llama 3.2 Fine-tuning](advanced_llm_apps/llm_finetuning_tutorials/llama3.2_finetuning/) - 30 行完成微调，Colab 上免费

### 🧑‍🏫 AI Agent Framework Crash Courses

*针对主流智能体框架的深度教程。*

*   [Google ADK Crash Course](ai_agent_framework_crash_course/google_adk_crash_course/) - 入门智能体、结构化输出、工具（内置、函数、第三方、MCP）、记忆、回调、插件与多智能体模式。模型无关。
*   [OpenAI Agents SDK Crash Course](ai_agent_framework_crash_course/openai_sdk_crash_course/) - 入门智能体、函数调用、结构化输出、工具、记忆、评测、handoffs、swarm 编排与路由逻辑。

---

<div align="center">

⭐ **[给仓库点 Star](https://github.com/Shubhamsaboo/awesome-llm-apps/stargazers)**，新模板上线时第一时间收到通知。

<sub>
<!-- Keep these links. Translations will automatically update with the README. -->
<a href="https://www.readme-i18n.com/Shubhamsaboo/awesome-llm-apps?lang=de">Deutsch</a> ·
<a href="https://www.readme-i18n.com/Shubhamsaboo/awesome-llm-apps?lang=es">Español</a> ·
<a href="https://www.readme-i18n.com/Shubhamsaboo/awesome-llm-apps?lang=fr">français</a> ·
<a href="https://www.readme-i18n.com/Shubhamsaboo/awesome-llm-apps?lang=ja">日本語</a> ·
<a href="https://www.readme-i18n.com/Shubhamsaboo/awesome-llm-apps?lang=ko">한국어</a> ·
<a href="https://www.readme-i18n.com/Shubhamsaboo/awesome-llm-apps?lang=pt">Português</a> ·
<a href="https://www.readme-i18n.com/Shubhamsaboo/awesome-llm-apps?lang=ru">Русский</a> ·
<a href="https://www.readme-i18n.com/Shubhamsaboo/awesome-llm-apps?lang=zh">中文</a>
</sub>

<sub>Apache-2.0 · 参见 <a href="LICENSE">LICENSE</a> · Fork it, ship it, sell it.</sub>

</div>
