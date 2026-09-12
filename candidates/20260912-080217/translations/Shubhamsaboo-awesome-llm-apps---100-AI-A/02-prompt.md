---
created: 2026-09-12
updated: 2026-09-12
type: prompt-draft
status: 过程稿
sources:
  - url: https://github.com/Shubhamsaboo/awesome-llm-apps
tags: [awesome-llm-apps, 翻译, prompt, GitHub README]
---

# 02 本次翻译使用的提示词（过程稿）

> 本次翻译用如下提示词驱动。原文（英文 README）已抓取到
> `candidates/20260912-080217/sources/Shubhamsaboo-awesome-llm-apps---100-AI-A.md`
> （GitHub API `repos/Shubhamsaboo/awesome-llm-apps/readme`，仓库元数据取自
> `repos/Shubhamsaboo/awesome-llm-apps`）。
> 仓库无官方简体中文 README，本译文以英文 `main` 分支原文为唯一依据。

## 提示词正文

```
你是一名资深技术译者（英→中），翻译 GitHub 开源仓库 Shubhamsaboo/awesome-llm-apps 的主 README
（标题：100+ AI Agents, Agent Skills and RAG Apps - Free and Open Source）。

## 输入
- 原文：candidates/20260912-080217/sources/Shubhamsaboo-awesome-llm-apps---100-AI-A.md
  （正文从首个 <p align="center"> banner 块到结尾 "Fork it, ship it, sell it." 为止；
  忽略文件头部的采集元信息块。）
- 仓库元数据（2026-09-12）：stars 137,242 / forks 20,194 / open issues 11 / watchers 1,286，
  主语言 Python，仓库创建 2024-04-29，homepage https://www.theunwindai.com，license Apache-2.0。

## 输出要求
1. 完整逐译正文全部标题、分类导语、117 条清单条目与底部区块，不压缩、不删节；
   HTML 区块（banner、画廊表格、赞助商表格、居中 div）与图片链接原样保留，
   仅翻译其中的可见文案（alt 文案、<sub><b> 标题等按需保留原文或意译）。
2. 保留原文全部超链接；分类清单里相对路径链接（如 agent_skills/project-graveyard/、
   starter_ai_agents/ai_travel_agent/）保持英文路径原样不译；外链（github.com 等）原样保留；
   `<sub>↗ external</sub>` 标记保留。
3. 代码块原样保留，不翻译：npx skills add ...、git clone ...、cd ...、pip install -r requirements.txt、
   streamlit run travel_agent.py。
4. 术语表（必须一致）：
   - Agent / AI Agent → 智能体（保留 Agent 亦可，正文统一用「智能体」）
   - Agent Skills → 智能体技能
   - RAG (Retrieval Augmented Generation) → 检索增强生成（RAG）
   - MCP (Model Context Protocol) → 模型上下文协议（MCP），MCP 保留英文缩写
   - Multi-agent Teams → 多智能体团队；Always-on Agents → 常驻智能体
   - Generative UI → 生成式 UI；Agentic Frontends → 智能体前端
   - Voice AI Agents → 语音智能体；Fine-tuning → 微调
   - Crash Course → 速成课；Memory → 记忆
   - eval → 评测；security gate → 安全门禁；CI gate → CI 门禁
   - 模型名与产品名保留英文：Claude、Gemini、GPT、DeepSeek、Llama、Qwen、OpenAI Agents SDK、
     Google ADK、CrewAI、AG2、EvoAgentX、Nano Banana Pro、Gemini Live、Qdrant、Unsloth、Streamlit
   - 技术名词保留：embedding、vector search、hybrid search、function calling、structured outputs、
     handoffs、swarm orchestration、sandbox、shadcn、arxiv、Notion、Slack
5. 数字与结论逐一比对原文，不得改动：100+ 条、「15 个分类、117 条条目」为译者统计的旁注，
   原文只写 "100+"；stars 137,242 / forks 20,194 / open issues 11 / watchers 1,286；
   创建时间 2024-04-29；Apache-2.0；条目描述中的具体数字（如 30 lines、20 lines、50 lines、
   30-60%、50-90%、4-bit LoRA）原样保留。
6. 中文表达通顺自然，术语到位；条目格式统一为 `- [emoji 名称](路径) — 中文描述`；
   输出 Markdown，标题层级沿用原文；frontmatter：
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
```

## 执行备注

- 抓取方式：GitHub API `repos/Shubhamsaboo/awesome-llm-apps/readme`（raw）取得权威正文；
  仓库元数据（stars / forks / issues / license / topics / created_at）取自
  `repos/Shubhamsaboo/awesome-llm-apps`。
- 翻译策略：术语优先 + 完整逐译；15 个分类标题与分类导语全译；
  117 条条目按原文顺序逐条翻译（不重排、不合并）；相对路径链接保持英文。
- 关键数字比对：15 个分类 / 117 条条目 /「100+」/ 137,242 stars / 20,194 forks /
  11 open issues / 1,286 watchers / Apache-2.0 / 创建 2024-04-29 已抽查一致；
  仓库热度数据以 2026-09-12 采集快照为准，属于时点值。
- 该提示词本身不直接沉淀进 prompts/（curate 产出边界：不写 prompts/），
  留待评审通过、实测后再考虑复用。
