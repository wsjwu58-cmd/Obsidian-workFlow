评审完成。四篇候选的三件套（原文、译文、works-ready）已全部通读，并与 `references/articles.md`、`expand/` 既有条目对照。以下为评审结果。

---

### The new rules of context engineering for Claude 5 generation models

- **原文价值**：高 — Anthropic 工程师亲笔的方法论长文，核心洞察扎实（系统提示词删 80% 且评测无损）+ 六组「过去/现在」神话破除 + 系统提示词/CLAUDE.md/Skills/References 四类落地建议，非发布稿。
- **翻译质量**：精品 — 完整逐译，`渐进披露 / 制品 / 评分标准 / harness 执行框架` 等术语到位，通顺且保留了原文粗体强调结构。
- **与知识库契合度**：补薄弱环节 — 知识库有 Claude Code 源码解读与 `expand/thinking/MCP协议标准化的增量与边界.md`，但缺「上下文工程」方法论条目，而这恰是 Harness Engineering 主题的核心空白。
- **一句话定性 + 建议去向**：harness 上下文工程的方法论基准，译文可直接毕业 → `working/` 正式收录（译文作品），并在 `articles.md` 编号正文标记已收录、关联 wiki Claude Code 源码解读。

### One-shotting a Raccoon Heist game using Claude Fable 5

- **原文价值**：中 — 一手实操案例：单提示词 + 用 OpenAI key 补能力缺口、GitHub Pages 移动端预览循环、Playwright 自测截图、对「生成游戏不好玩」的诚实结论，都是真实信号；但属体验叙事，理论密度低。
- **翻译质量**：合格 — 完整逐译，代码块与截图说明保留，给 `gpt-image-2` 英文提示词补中文释义是加分处理；个别长句略平。
- **与知识库契合度**：边缘补白 — 知识库无 vibe coding / 游戏生成主题，与 KMP·Flutter·harness 主线弱相关，仅「agent 自测 + 移动端预览」工作流可借鉴。
- **一句话定性 + 建议去向**：agent 单次生成能力的实测样本，参考价值有限 → `articles.md` 观察项一行（防重复采集，标注「含可复用 agent 预览/自测工作流」），译文不收录。

### Six Agent Orchestration Patterns

- **原文价值**：中 — 六模式框架源自 Anthropic 既有分类（非原创），增量在 Vercel 生产视角：token 成本对照表、链式准确率复利（95%^10≈60%）、持久化/计费/沙箱平台行为；后半段是平台推广，但数据点可作参考。
- **翻译质量**：精品 — 完整逐译，六行选型表格结构完整保留，`编排器-工作器 / 评估器-优化器 / 过早扇出 / 失控评审循环` 等术语统一到位。
- **与知识库契合度**：补薄弱环节 — `expand/06-AI与LLM/Agent工具与平台/n8n.md`、`ECC.md` 讲平台与 harness，wiki 有 Claude Code 协调模式与 langgraph4j 笔记，但缺「模式选型决策框架 + token 成本量级」的浓缩参考，不重复。
- **一句话定性 + 建议去向**：六模式选型表是低成本高复用的参考作品（需标注框架出处为 Anthropic）→ `working/` 正式收录（译文作品），亦可作为 `articles.md` 编号正文「已收录」。

### Making production-ready agents the default: building Duolingo's agent platform

- **原文价值**：高 — 一方工程案例，实质内容足：`AgentDefinition` 注册表、Temporal `AgentWorkflow` 包装、定义与执行解耦、多运行时（含 OpenAI Agents SDK + MCP 工具调用转 activity）、确定性优先的评测 grader（`diff_assertions` / `no_op_consistency`），量化结果「数周 → 10 分钟」。
- **翻译质量**：合格 — 完整逐译，代码块保留，通顺度好；个别术语略直译（`生产化`、`包装器`），不影响理解。
- **与知识库契合度**：补薄弱环节 — 与 `expand/06-AI与LLM/Agent工具与平台/ECC.md`（harness 抽象）理念互补而非重复，评测 grader 设计与 `expand/thinking/MCP协议标准化的增量与边界.md` 的工具语义话题可互链。
- **一句话定性 + 建议去向**：生产级 agent 平台架构的一手参考，评测「检查产物而非文字」思路尤其值得沉淀 → `working/` 正式收录（译文作品），并建议在 `expand/thinking/` 提炼一条平台化抽象与评测优先的独立观点（可选）。

---

## 汇总

| 篇名 | 原文价值 | 翻译质量 | 契合度 | 定性 | 建议去向 |
| --- | --- | --- | --- | --- | --- |
| The new rules of context engineering for Claude 5 generation models | 高 | 精品 | 补薄弱环节（上下文工程方法论空白） | harness 上下文工程基准方法论 | `working/` 正式收录 |
| One-shotting a Raccoon Heist game using Claude Fable 5 | 中 | 合格 | 边缘补白（与主线弱相关） | agent 单次生成实测样本 | `articles.md` 观察项一行 |
| Six Agent Orchestration Patterns | 中 | 精品 | 补薄弱环节（模式选型 + 成本量级） | 选型参考框架（出处 Anthropic） | `working/` 正式收录 |
| Making production-ready agents the default: building Duolingo's agent platform | 高 | 合格 | 补薄弱环节（生产平台架构 + 评测） | 生产级 agent 平台工程案例 | `working/` 正式收录 |

评审仅输出结论，未修改任何文件；后续按建议落库时，记得在 `references/articles.md` 编号正文登记状态与归属（同一次提交同步 `expand/index.md` 等下游缓存）。

Reading prompt from stdin...
OpenAI Codex v0.147.0
--------
workdir: /root/note-worker
model: deepseek-v4-flash
provider: deepseek
approval: never
sandbox: workspace-write [workdir, /tmp, $TMPDIR] (network access enabled)
reasoning effort: none
reasoning summaries: none
session id: 019fe60b-f0f9-7492-9fbf-2567edbe1a1d
--------
user
---
created: 2026-08-09
updated: 2026-08-09
type: workflow
status: 待验证
product: null
source: curate-research 评审模板
---

# 候选自动评审

> 运行器：服务器 codex，由 curate.py 串行调用。对一批 3-4 篇候选统一打分。

## 任务

你是知识库的内容评审。知识库主题：AI Agent 开发 / 跨平台开发（KMP·Flutter）/ Harness Engineering / 通用技术。

读以下每篇候选的三件套，逐篇回答。候选位于 `candidates/20260809-180901/`：

- The new rules of context engineering for Claude 5 generation models | https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models
- One-shotting a Raccoon Heist game using Claude Fable 5 | https://simonwillison.net/2026/Aug/5/raccoon-heist/
- Six Agent Orchestration Patterns | https://vercel.com/i/agent-orchestration-patterns
- Making production-ready agents the default: building Duolingo's agent platform | https://blog.duolingo.com/production-ready-ai-agent-platform/

逐篇回答（每篇独立小节，标题为篇名）：

### 篇名
- **原文价值**：原创洞察密度 / 长文实质 vs 产品页·发布稿·摘要。高/中/低 + 一句话理由
- **翻译质量**：完整逐译 / 压缩摘要 / 首轮粗稿；通顺度、术语到位度。精品/合格/需返工 + 一句话理由
- **与知识库契合度**：补薄弱环节还是重复（对照 references/articles.md 与 expand/ 已有条目）
- **一句话定性 + 建议去向**：working/ 正式收录 / articles.md 观察项一行 / tools/（待实测）/ 淘汰

## 汇总

最后输出一个「候选 × 定性 × 去向」markdown 表格：

| 篇名 | 原文价值 | 翻译质量 | 契合度 | 定性 | 建议去向 |

## 约束

- 基于实际内容，紧凑中文，结构化输出
- 只做评审与建议，不修改任何文件

warning: Codex could not find bubblewrap on PATH. Install bubblewrap with your OS package manager. See the sandbox prerequisites: https://developers.openai.com/codex/concepts/sandboxing#prerequisites. Codex will use the bundled bubblewrap in the meantime.
warning: Model metadata for `deepseek-v4-flash` not found. Defaulting to fallback metadata; this can degrade performance and cause issues.
codex
我先浏览知识库结构和候选目录，再逐篇对照评审。
exec
/bin/bash -lc "cd /root/note-worker && ls -la && echo '---' && ls -la candidates/20260809-180901/ 2>/dev/null && echo '---' && ls references/ 2>/dev/null && echo '---' && ls expand/ 2>/dev/null | head -50" in /root/note-worker
 succeeded in 0ms:
total 104
drwxr-xr-x 19 root root  4096 Aug  9 18:22 .
dr-xr-x--- 14 root root  4096 Aug  9 17:46 ..
dr-xr-xr-x  2 root root    40 Aug  9 18:22 .agents
dr-xr-xr-x  2 root root    40 Aug  9 18:22 .codex
drwxr-xr-x  2 root root  4096 Aug  9 18:04 .firecrawl
drwxr-xr-x  8 root root  4096 Aug  9 18:09 .git
drwxr-xr-x  2 root root  4096 Aug  9 13:37 .githooks
drwxr-xr-x  3 root root  4096 Aug  9 13:37 .github
-rw-r--r--  1 root root   738 Aug  9 17:25 .gitignore
drwxr-xr-x  3 root root  4096 Aug  9 13:37 .obsidian
-rw-r--r--  1 root root  1066 Aug  9 13:37 LICENSE
-rw-r--r--  1 root root  9864 Aug  9 13:37 README.md
-rw-r--r--  1 root root 14623 Aug  9 13:37 agents.md
drwxr-xr-x  2 root root  4096 Aug  9 13:37 assets
drwxr-xr-x  3 root root  4096 Aug  9 18:09 candidates
drwxr-xr-x  3 root root  4096 Aug  9 17:25 docs
drwxr-xr-x  5 root root  4096 Aug  9 14:21 expand
drwxr-xr-x  3 root root  4096 Aug  9 17:25 prompts
drwxr-xr-x  2 root root  4096 Aug  9 18:11 references
drwxr-xr-x  3 root root  4096 Aug  9 18:03 scripts
drwxr-xr-x  2 root root  4096 Aug  9 13:37 templates
drwxr-xr-x 14 root root  4096 Aug  9 13:37 wiki
drwxr-xr-x  2 root root  4096 Aug  9 13:37 working
---
total 20
drwxr-xr-x 5 root root 4096 Aug  9 18:09 .
drwxr-xr-x 3 root root 4096 Aug  9 18:09 ..
drwxr-xr-x 2 root root 4096 Aug  9 18:20 sources
drwxr-xr-x 6 root root 4096 Aug  9 18:19 translations
drwxr-xr-x 2 root root 4096 Aug  9 18:22 works-ready
---
agents.md
articles.md
---
03-后端
06-AI与LLM
index.md
log.md
thinking
动态索引.md
知识图谱.md
知识库周报.md
自动化工作流功能与实现方案.md
自动化工作流设计.md

exec
/bin/bash -lc "cd /root/note-worker/candidates/20260809-180901 && find . -type f | sort && echo '---' && ls -la sources translations works-ready" in /root/note-worker
 succeeded in 0ms:
./sources/Making-production-ready-agents-the-defau-full.md
./sources/Making-production-ready-agents-the-defau.md
./sources/One-shotting-a-Raccoon-Heist-game-using-full.md
./sources/One-shotting-a-Raccoon-Heist-game-using.md
./sources/Six-Agent-Orchestration-Patterns-full.md
./sources/Six-Agent-Orchestration-Patterns.md
./sources/The-new-rules-of-context-engineering-for-full.md
./sources/The-new-rules-of-context-engineering-for.md
./translations/Making-production-ready-agents-the-defau/01-analysis.md
./translations/Making-production-ready-agents-the-defau/02-prompt.md
./translations/Making-production-ready-agents-the-defau/translation.md
./translations/One-shotting-a-Raccoon-Heist-game-using/01-analysis.md
./translations/One-shotting-a-Raccoon-Heist-game-using/02-prompt.md
./translations/One-shotting-a-Raccoon-Heist-game-using/translation.md
./translations/Six-Agent-Orchestration-Patterns/01-analysis.md
./translations/Six-Agent-Orchestration-Patterns/02-prompt.md
./translations/Six-Agent-Orchestration-Patterns/translation.md
./translations/The-new-rules-of-context-engineering-for/01-analysis.md
./translations/The-new-rules-of-context-engineering-for/02-prompt.md
./translations/The-new-rules-of-context-engineering-for/translation.md
./works-ready/Making-production-ready-agents-the-defau-translation.md
./works-ready/One-shotting-a-Raccoon-Heist-game-using-translation.md
./works-ready/Six-Agent-Orchestration-Patterns-translation.md
./works-ready/The-new-rules-of-context-engineering-for-translation.md
---
sources:
total 416
drwxr-xr-x 2 root root   4096 Aug  9 18:20 .
drwxr-xr-x 5 root root   4096 Aug  9 18:09 ..
-rw-r--r-- 1 root root  46716 Aug  9 18:20 Making-production-ready-agents-the-defau-full.md
-rw-r--r-- 1 root root  17440 Aug  9 18:20 Making-production-ready-agents-the-defau.md
-rw-r--r-- 1 root root  55153 Aug  9 18:13 One-shotting-a-Raccoon-Heist-game-using-full.md
-rw-r--r-- 1 root root  22012 Aug  9 18:13 One-shotting-a-Raccoon-Heist-game-using.md
-rw-r--r-- 1 root root 114296 Aug  9 18:18 Six-Agent-Orchestration-Patterns-full.md
-rw-r--r-- 1 root root  20237 Aug  9 18:17 Six-Agent-Orchestration-Patterns.md
-rw-r--r-- 1 root root 112623 Aug  9 18:10 The-new-rules-of-context-engineering-for-full.md
-rw-r--r-- 1 root root  15871 Aug  9 18:10 The-new-rules-of-context-engineering-for.md

translations:
total 24
drwxr-xr-x 6 root root 4096 Aug  9 18:19 .
drwxr-xr-x 5 root root 4096 Aug  9 18:09 ..
drwxr-xr-x 2 root root 4096 Aug  9 18:22 Making-production-ready-agents-the-defau
drwxr-xr-x 2 root root 4096 Aug  9 18:16 One-shotting-a-Raccoon-Heist-game-using
drwxr-xr-x 2 root root 4096 Aug  9 18:19 Six-Agent-Orchestration-Patterns
drwxr-xr-x 2 root root 4096 Aug  9 18:11 The-new-rules-of-context-engineering-for

works-ready:
total 76
drwxr-xr-x 2 root root  4096 Aug  9 18:22 .
drwxr-xr-x 5 root root  4096 Aug  9 18:09 ..
-rw-r--r-- 1 root root 12596 Aug  9 18:22 Making-production-ready-agents-the-defau-translation.md
-rw-r--r-- 1 root root 18631 Aug  9 18:15 One-shotting-a-Raccoon-Heist-game-using-translation.md
-rw-r--r-- 1 root root 16711 Aug  9 18:19 Six-Agent-Orchestration-Patterns-translation.md
-rw-r--r-- 1 root root 10573 Aug  9 18:11 The-new-rules-of-context-engineering-for-translation.md

exec
/bin/bash -lc 'cd /root/note-worker && cat references/articles.md' in /root/note-worker
 succeeded in 0ms:
# 文章索引

> **本文件是文章索引与计数的最佳事实来源（single source of truth）。**
>
> **计数规则（machine-checkable）：**
> 一篇文章 = 一个 `### N. {标题}` 形式的编号小节，且不属于本文末尾的「已淘汰 / 待补充」段落。
> 占位条目（"待处理 / 待补充"）**不写在编号正文里**，而是统一进本文末尾的「待处理队列」，避免污染计数。
> 全局连续编号（不按来源重置），最大编号 = 文章总数。
>
> **状态字段（流程机器码）：** `待处理`（采集到站，未加工） / `已收录`（判定有值，已归入某模块） / `已淘汰`（判定不值，保留 URL 防重复采集）。
> **归属字段：** 加工结果所在的模块路径（`expand/…` thinking / `working/…` 作品 / `prompts/…` 提示词），是「分到哪一模块」的落点记录。
>
> **下游引用都是本文的冗余缓存：** 根 `AGENTS.md`、`expand/index.md`、`.github/workflows/research.yml` 的去重清单、`references/AGENTS.md` 的概览表。
> 新增/更新文章时，必须**同一次提交**更新本文 + 相关下游缓存。

## 待处理（采集队列，计入编号正文前的暂存区）

> 由 `collect.yml` / 服务器 codex 采集写入。**人工 review 后移入编号正文**（`已收录`/`已淘汰`）。

<!-- pending:start -->
<!-- 采集自动化维护，按 `| 标题 | 链接 | 来源 | 日期 |` 追加一行；处理完移入编号正文 -->
<!-- 当前：7 条待处理 -->
| The new rules of context engineering for Claude 5 generation models | https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models | research | 2026-08-09 | 🔄评审中 candidates/20260809-180901/
| One-shotting a Raccoon Heist game using Claude Fable 5 | https://simonwillison.net/2026/Aug/5/raccoon-heist/ | research | 2026-08-09 | 🔄评审中 candidates/20260809-180901/
| Six Agent Orchestration Patterns | https://vercel.com/i/agent-orchestration-patterns | research | 2026-08-09 | 🔄评审中 candidates/20260809-180901/
| Making production-ready agents the default: building Duolingo's agent platform | https://blog.duolingo.com/production-ready-ai-agent-platform/ | research | 2026-08-09 | 🔄评审中 candidates/20260809-180901/
| Meta launches Muse Code for complex software work with persistent AI agents | https://www.infoworld.com/article/4206084/meta-launches-muse-code-for-complex-software-work-with-persistent-ai-agents.html | research | 2026-08-09 |
| Harness-R1: Learning to Edit Executable Runtime Harnesses from Agent Failure Trajectories | https://arxiv.org/abs/2608.02276 | research | 2026-08-09 |
| EvolveNet: Collaborative Harness Evolution for Agent Self-Improvement | https://arxiv.org/abs/2608.04968 | research | 2026-08-09 |
| The Shape of Things to Come, Part 1: The Continuous Thunderdome | https://yegge.ai/essays/the-shape-of-things-to-come/ | research | 2026-08-09 |
| Claude Code v2.1.224 — self-hosted environments | https://github.com/anthropics/claude-code/releases/tag/v2.1.224 | research | 2026-08-09 |
| I Gave Claude Code an AGENTS.md Contract and Stopped Babysitting It | https://dev.to/daymondhyper/i-gave-claude-code-an-agentsmd-contract-and-stopped-babysitting-it-53m | research | 2026-08-09 |
<!-- pending:end -->

## 已收录（编号正文）

### 01. arxiv — When Does On-Policy Interaction Help?

- **标题：** When Does On-Policy Interaction Help? Representational Tradeoffs in Value-Based Imitation Learning
- **链接：** [arxiv.org/abs/2607.29617v1](http://arxiv.org/abs/2607.29617v1)
- **作者：** arxiv 论文 | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/06-AI与LLM/Agent研究与评测/在线策略交互与模仿学习.md`
- **核心：** 专家交互放宽模仿学习表征需求，提出 OVI 算法。
- **关联：** Agent 模仿学习；`references/raw/` 已删除，素材散点见 expand 条目 sources 字段

### 02. AgentHPOBench — LLM Agents as Sequential Hyperparameter Optimizers

- **标题：** AgentHPOBench: A Benchmark For Evaluating LLM Agents as Sequential Hyperparameter Optimizers
- **链接：** [arxiv.org/abs/2607.29626v1](http://arxiv.org/abs/2607.29626v1)
- **作者：** arxiv 论文 | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/06-AI与LLM/Agent研究与评测/AgentHPOBench.md`
- **核心：** 7 类 30 任务，评估 LLM Agent 作为顺序超参数优化器。
- **关联：** Agent 评测基准

### 03. ExtractBench — Schema-Guided Enterprise Document Extraction

- **标题：** ExtractBench: A Benchmark for Schema-Guided Enterprise Document Extraction
- **链接：** [arxiv.org/abs/2607.29677v1](http://arxiv.org/abs/2607.29677v1)
- **作者：** arxiv 论文 | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/06-AI与LLM/Agent研究与评测/ExtractBench.md`
- **核心：** 370 文档 / 4869 页，模式引导的企业文档提取基准。
- **关联：** RAG + 文档解析

### 04. DungeonBench — Rules-Rich Tactical Reasoning

- **标题：** DungeonBench: A Benchmark for Rules-Rich Tactical Reasoning in Dungeons & Dragons Combat
- **链接：** [arxiv.org/abs/2607.29577v1](http://arxiv.org/abs/2607.29577v1)
- **作者：** arxiv 论文 | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/06-AI与LLM/Agent研究与评测/DungeonBench.md`
- **核心：** D&D 规则密集型战术推理基准（遭遇战 + 一日冒险双轨道）。
- **关联：** Agent 推理评测

### 05. MOT-SR — Multi-Objective Scientific Equation Discovery

- **标题：** MOT-SR: Multi-Objective Tool-Augmented Scientific Equation Discovery with Large Language Models
- **链接：** [arxiv.org/abs/2607.29561v1](http://arxiv.org/abs/2607.29561v1)
- **作者：** arxiv 论文 | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/06-AI与LLM/Agent研究与评测/MOT-SR.md`
- **核心：** 多目标工具增强符号回归框架（双 LLM 模块 + 帕累托前沿）。
- **关联：** 科学发现 + 工具调用

### 06. ECC — agent harness 操作系统

- **标题：** affaan-m/ECC — The agent harness performance optimization system
- **链接：** [github.com/affaan-m/ECC](https://github.com/affaan-m/ECC)
- **作者：** github | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/06-AI与LLM/Agent工具与平台/ECC.md`
- **核心：** 面向编程代理的 harness 操作系统：技能 / 记忆 / 安全 / 跨 harness 编排。
- **关联：** Agent 工程化 / harness

### 07. n8n — AI 原生工作流自动化平台

- **标题：** n8n-io/n8n — Fair-code workflow automation platform with native AI capabilities
- **链接：** [github.com/n8n-io/n8n](https://github.com/n8n-io/n8n)
- **作者：** github | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/06-AI与LLM/Agent工具与平台/n8n.md`
- **核心：** 可视化画布 + 1500+ 集成，自托管或云上 AI 原生工作流。
- **关联：** Workflow / Agent 调度

### 08. MarkItDown — 文件/文档转 Markdown

- **标题：** microsoft/markitdown — Python tool for converting files to Markdown
- **链接：** [github.com/microsoft/markitdown](https://github.com/microsoft/markitdown)
- **作者：** github | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/06-AI与LLM/Agent工具与平台/MarkItDown.md`
- **核心：** 任意文件转 LLM 友好 Markdown（架构 / 插件 / Azure 集成 / 安全实践）。
- **关联：** 数据管线 / 文档解析

### 09. Hermes-Agent — the agent that grows with you

- **标题：** NousResearch/hermes-agent — The agent that grows with you
- **链接：** [github.com/NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)
- **作者：** github | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/06-AI与LLM/Agent工具与平台/Hermes-Agent.md`
- **核心：** 自我改进 AI 代理——闭环学习与跨会话记忆。
- **关联：** Agent 自我改进

### 10. JavaGuide — Java 面试 & 后端面试指南

- **标题：** Snailclimb/JavaGuide — Java 面试 & 后端通用面试指南
- **链接：** [github.com/Snailclimb/JavaGuide](https://github.com/Snailclimb/JavaGuide)
- **作者：** github | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/03-后端/java/JavaGuide.md`
- **核心：** 计算机基础 / 数据库 / 分布式 / 高并发 / 系统设计 / AI 应用开发。
- **关联：** 后端 / 求职面试

### 11. Bonsai: Janestreet's UI Library

- **标题：** Bonsai: Janestreet's UI Library
- **链接：** [github.com/janestreet/bonsai](https://github.com/janestreet/bonsai)
- **作者：** HN | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** 淘汰
- **核心：** UI 库一个（排除原因：非本知识库范围，无 AI/后端关联，仅留 URL 防重复采集）
- **关联：** —

### 12. Prevent cognitive debt by manually retyping LLM-generated code

- **标题：** Prevent cognitive debt by manually retyping LLM-generated code
- **链接：** [ankursethi.com](https://ankursethi.com/blog/prevent-cognitive-debt-by-manually-retyping-llm-generated-code/)
- **作者：** HN | **日期：** 2026-08-03
- **状态：** 已淘汰 | **归属：** —
- **核心：** 独立已学，判定无深度加工价值
- **关联：** —

### 13. Qwen3.8-Max: A New Bar for Coding and Cowork

- **标题：** Qwen3.8-Max: A New Bar for Coding and Cowork
- **链接：** [qwen.ai](https://qwen.ai/blog?id=qwen3.8)
- **作者：** HN | **日期：** 2026-08-03
- **状态：** 已淘汰 | **归属：** —
- **核心：** 官方营销博文，技术增量有限
- **关联：** —

### 14. MCP 官方文档：Model Context Protocol 介绍

- **标题：** MCP 官方文档：Model Context Protocol 介绍
- **链接：** [modelcontextprotocol.io/introduction](https://modelcontextprotocol.io/introduction)
- **作者：** MCP 官方文档（modelcontextprotocol.io） | **日期：** 2026-08-09
- **状态：** 已收录 | **归属：** `expand/thinking/MCP协议标准化的增量与边界.md`
- **核心：** 官方入门与架构——「AI 应用的 USB-C」定位、数据层/传输层双层、2026-07-28 版增量（MCP Apps / Agent Skills / Registry / server/discover）。思考：协议只标准化「连接信封」，工具语义仍靠 server 自治，M×N 适配成本转移而非消失。
- **关联：** MCP / Agent 工具生态；既有笔记 [[MCP协议与工具调用]]、Claude Code [[12-mcp-xie-yi-ji-cheng]]

### 15. Rust 2025 官方博客：Rust 1.85 版本说明（Move 语义 / Borrow Checker 演进）

- **标题：** Rust 2025 官方博客：Rust 1.85 版本说明（Move 语义 / Borrow Checker 演进）
- **链接：** [blog.rust-lang.org/2025/02/20/Rust-1.85.0.html](https://blog.rust-lang.org/2025/02/20/Rust-1.85.0.html)
- **作者：** The Rust Release Team（blog.rust-lang.org） | **日期：** 2025-02-20（采集 2026-08-09）
- **状态：** 已收录 | **归属：** `expand/thinking/Rust2024版次的语义收紧与异步闭合.md`
- **核心：** Rust 1.85.0 同步稳定 2024 Edition（官方口径「史上最大版次」）：RPIT 生命周期捕获规则、临时作用域/drop 顺序、match 擦除保留、unsafe extern/属性/static mut 收缩、set_var 转 unsafe、async closures（AsyncFn）稳定、元组 collect 扩展至 12 元。思考：采集器「Move 语义」标签失焦——真正主线是「版次语义收紧 + unsafe 显式化 + 异步借用补课」，edition 约三年一拍是 Rust 的语义债务清偿机制。
- **关联：** Rust / 版次 / 借用检查；对照 [[c++核心编程]]、思考层 [[MCP协议标准化的增量与边界]]

## 统计

- **正式收录：** 12 篇（编号 01-10、14、15）｜**已淘汰隔离：** 3 篇（编号 11-13，不计入收录数，仅防重复采集）

## 待补充

- [ ] 占位：外部新文章先查编号 01-15 确认未收，再由采集层写入「待处理」队列

exec
/bin/bash -lc 'cd /root/note-worker && find expand -type f | sort' in /root/note-worker
 succeeded in 0ms:
expand/03-后端/java/JavaGuide.md
expand/06-AI与LLM/Agent工具与平台/ECC.md
expand/06-AI与LLM/Agent工具与平台/Hermes-Agent.md
expand/06-AI与LLM/Agent工具与平台/MarkItDown.md
expand/06-AI与LLM/Agent工具与平台/n8n.md
expand/06-AI与LLM/Agent研究与评测/AgentHPOBench.md
expand/06-AI与LLM/Agent研究与评测/DungeonBench.md
expand/06-AI与LLM/Agent研究与评测/ExtractBench.md
expand/06-AI与LLM/Agent研究与评测/MOT-SR.md
expand/06-AI与LLM/Agent研究与评测/在线策略交互与模仿学习.md
expand/index.md
expand/log.md
expand/thinking/AGENTS.md
expand/thinking/MCP协议标准化的增量与边界.md
expand/thinking/Rust2024版次的语义收紧与异步闭合.md
expand/动态索引.md
expand/知识图谱.md
expand/知识库周报.md
expand/自动化工作流功能与实现方案.md
expand/自动化工作流设计.md

exec
/bin/bash -lc "cd /root/note-worker && sed -n '1,120p' references/articles.md" in /root/note-worker
 succeeded in 0ms:
# 文章索引

> **本文件是文章索引与计数的最佳事实来源（single source of truth）。**
>
> **计数规则（machine-checkable）：**
> 一篇文章 = 一个 `### N. {标题}` 形式的编号小节，且不属于本文末尾的「已淘汰 / 待补充」段落。
> 占位条目（"待处理 / 待补充"）**不写在编号正文里**，而是统一进本文末尾的「待处理队列」，避免污染计数。
> 全局连续编号（不按来源重置），最大编号 = 文章总数。
>
> **状态字段（流程机器码）：** `待处理`（采集到站，未加工） / `已收录`（判定有值，已归入某模块） / `已淘汰`（判定不值，保留 URL 防重复采集）。
> **归属字段：** 加工结果所在的模块路径（`expand/…` thinking / `working/…` 作品 / `prompts/…` 提示词），是「分到哪一模块」的落点记录。
>
> **下游引用都是本文的冗余缓存：** 根 `AGENTS.md`、`expand/index.md`、`.github/workflows/research.yml` 的去重清单、`references/AGENTS.md` 的概览表。
> 新增/更新文章时，必须**同一次提交**更新本文 + 相关下游缓存。

## 待处理（采集队列，计入编号正文前的暂存区）

> 由 `collect.yml` / 服务器 codex 采集写入。**人工 review 后移入编号正文**（`已收录`/`已淘汰`）。

<!-- pending:start -->
<!-- 采集自动化维护，按 `| 标题 | 链接 | 来源 | 日期 |` 追加一行；处理完移入编号正文 -->
<!-- 当前：7 条待处理 -->
| The new rules of context engineering for Claude 5 generation models | https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models | research | 2026-08-09 | 🔄评审中 candidates/20260809-180901/
| One-shotting a Raccoon Heist game using Claude Fable 5 | https://simonwillison.net/2026/Aug/5/raccoon-heist/ | research | 2026-08-09 | 🔄评审中 candidates/20260809-180901/
| Six Agent Orchestration Patterns | https://vercel.com/i/agent-orchestration-patterns | research | 2026-08-09 | 🔄评审中 candidates/20260809-180901/
| Making production-ready agents the default: building Duolingo's agent platform | https://blog.duolingo.com/production-ready-ai-agent-platform/ | research | 2026-08-09 | 🔄评审中 candidates/20260809-180901/
| Meta launches Muse Code for complex software work with persistent AI agents | https://www.infoworld.com/article/4206084/meta-launches-muse-code-for-complex-software-work-with-persistent-ai-agents.html | research | 2026-08-09 |
| Harness-R1: Learning to Edit Executable Runtime Harnesses from Agent Failure Trajectories | https://arxiv.org/abs/2608.02276 | research | 2026-08-09 |
| EvolveNet: Collaborative Harness Evolution for Agent Self-Improvement | https://arxiv.org/abs/2608.04968 | research | 2026-08-09 |
| The Shape of Things to Come, Part 1: The Continuous Thunderdome | https://yegge.ai/essays/the-shape-of-things-to-come/ | research | 2026-08-09 |
| Claude Code v2.1.224 — self-hosted environments | https://github.com/anthropics/claude-code/releases/tag/v2.1.224 | research | 2026-08-09 |
| I Gave Claude Code an AGENTS.md Contract and Stopped Babysitting It | https://dev.to/daymondhyper/i-gave-claude-code-an-agentsmd-contract-and-stopped-babysitting-it-53m | research | 2026-08-09 |
<!-- pending:end -->

## 已收录（编号正文）

### 01. arxiv — When Does On-Policy Interaction Help?

- **标题：** When Does On-Policy Interaction Help? Representational Tradeoffs in Value-Based Imitation Learning
- **链接：** [arxiv.org/abs/2607.29617v1](http://arxiv.org/abs/2607.29617v1)
- **作者：** arxiv 论文 | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/06-AI与LLM/Agent研究与评测/在线策略交互与模仿学习.md`
- **核心：** 专家交互放宽模仿学习表征需求，提出 OVI 算法。
- **关联：** Agent 模仿学习；`references/raw/` 已删除，素材散点见 expand 条目 sources 字段

### 02. AgentHPOBench — LLM Agents as Sequential Hyperparameter Optimizers

- **标题：** AgentHPOBench: A Benchmark For Evaluating LLM Agents as Sequential Hyperparameter Optimizers
- **链接：** [arxiv.org/abs/2607.29626v1](http://arxiv.org/abs/2607.29626v1)
- **作者：** arxiv 论文 | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/06-AI与LLM/Agent研究与评测/AgentHPOBench.md`
- **核心：** 7 类 30 任务，评估 LLM Agent 作为顺序超参数优化器。
- **关联：** Agent 评测基准

### 03. ExtractBench — Schema-Guided Enterprise Document Extraction

- **标题：** ExtractBench: A Benchmark for Schema-Guided Enterprise Document Extraction
- **链接：** [arxiv.org/abs/2607.29677v1](http://arxiv.org/abs/2607.29677v1)
- **作者：** arxiv 论文 | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/06-AI与LLM/Agent研究与评测/ExtractBench.md`
- **核心：** 370 文档 / 4869 页，模式引导的企业文档提取基准。
- **关联：** RAG + 文档解析

### 04. DungeonBench — Rules-Rich Tactical Reasoning

- **标题：** DungeonBench: A Benchmark for Rules-Rich Tactical Reasoning in Dungeons & Dragons Combat
- **链接：** [arxiv.org/abs/2607.29577v1](http://arxiv.org/abs/2607.29577v1)
- **作者：** arxiv 论文 | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/06-AI与LLM/Agent研究与评测/DungeonBench.md`
- **核心：** D&D 规则密集型战术推理基准（遭遇战 + 一日冒险双轨道）。
- **关联：** Agent 推理评测

### 05. MOT-SR — Multi-Objective Scientific Equation Discovery

- **标题：** MOT-SR: Multi-Objective Tool-Augmented Scientific Equation Discovery with Large Language Models
- **链接：** [arxiv.org/abs/2607.29561v1](http://arxiv.org/abs/2607.29561v1)
- **作者：** arxiv 论文 | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/06-AI与LLM/Agent研究与评测/MOT-SR.md`
- **核心：** 多目标工具增强符号回归框架（双 LLM 模块 + 帕累托前沿）。
- **关联：** 科学发现 + 工具调用

### 06. ECC — agent harness 操作系统

- **标题：** affaan-m/ECC — The agent harness performance optimization system
- **链接：** [github.com/affaan-m/ECC](https://github.com/affaan-m/ECC)
- **作者：** github | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/06-AI与LLM/Agent工具与平台/ECC.md`
- **核心：** 面向编程代理的 harness 操作系统：技能 / 记忆 / 安全 / 跨 harness 编排。
- **关联：** Agent 工程化 / harness

### 07. n8n — AI 原生工作流自动化平台

- **标题：** n8n-io/n8n — Fair-code workflow automation platform with native AI capabilities
- **链接：** [github.com/n8n-io/n8n](https://github.com/n8n-io/n8n)
- **作者：** github | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/06-AI与LLM/Agent工具与平台/n8n.md`
- **核心：** 可视化画布 + 1500+ 集成，自托管或云上 AI 原生工作流。
- **关联：** Workflow / Agent 调度

### 08. MarkItDown — 文件/文档转 Markdown

- **标题：** microsoft/markitdown — Python tool for converting files to Markdown
- **链接：** [github.com/microsoft/markitdown](https://github.com/microsoft/markitdown)
- **作者：** github | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/06-AI与LLM/Agent工具与平台/MarkItDown.md`
- **核心：** 任意文件转 LLM 友好 Markdown（架构 / 插件 / Azure 集成 / 安全实践）。
- **关联：** 数据管线 / 文档解析

### 09. Hermes-Agent — the agent that grows with you

- **标题：** NousResearch/hermes-agent — The agent that grows with you
- **链接：** [github.com/NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)
- **作者：** github | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/06-AI与LLM/Agent工具与平台/Hermes-Agent.md`
- **核心：** 自我改进 AI 代理——闭环学习与跨会话记忆。
- **关联：** Agent 自我改进

### 10. JavaGuide — Java 面试 & 后端面试指南

- **标题：** Snailclimb/JavaGuide — Java 面试 & 后端通用面试指南

exec
/bin/bash -lc 'cd /root/note-worker && wc -l candidates/20260809-180901/sources/*.md candidates/20260809-180901/works-ready/*.md candidates/20260809-180901/translations/*/translation.md' in /root/note-worker
 succeeded in 0ms:
   514 candidates/20260809-180901/sources/Making-production-ready-agents-the-defau-full.md
   252 candidates/20260809-180901/sources/Making-production-ready-agents-the-defau.md
   403 candidates/20260809-180901/sources/One-shotting-a-Raccoon-Heist-game-using-full.md
   281 candidates/20260809-180901/sources/One-shotting-a-Raccoon-Heist-game-using.md
     1 candidates/20260809-180901/sources/Six-Agent-Orchestration-Patterns-full.md
   153 candidates/20260809-180901/sources/Six-Agent-Orchestration-Patterns.md
    32 candidates/20260809-180901/sources/The-new-rules-of-context-engineering-for-full.md
   319 candidates/20260809-180901/sources/The-new-rules-of-context-engineering-for.md
   200 candidates/20260809-180901/works-ready/Making-production-ready-agents-the-defau-translation.md
   223 candidates/20260809-180901/works-ready/One-shotting-a-Raccoon-Heist-game-using-translation.md
   221 candidates/20260809-180901/works-ready/Six-Agent-Orchestration-Patterns-translation.md
   179 candidates/20260809-180901/works-ready/The-new-rules-of-context-engineering-for-translation.md
   200 candidates/20260809-180901/translations/Making-production-ready-agents-the-defau/translation.md
   223 candidates/20260809-180901/translations/One-shotting-a-Raccoon-Heist-game-using/translation.md
   221 candidates/20260809-180901/translations/Six-Agent-Orchestration-Patterns/translation.md
   179 candidates/20260809-180901/translations/The-new-rules-of-context-engineering-for/translation.md
  3601 total

exec
/bin/bash -lc 'cd /root/note-worker/candidates/20260809-180901 && head -100 sources/The-new-rules-of-context-engineering-for.md' in /root/note-worker
 succeeded in 0ms:
[Home page](https://claude.com/)

Explore here

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6903d222061abf091318fb82_423062049d4676b41d52b16068cbb5e21603190e-1000x1000.svg)

# ThenewrulesofcontextengineeringforClaude5generationmodels

We removed over 80% of Claude Code's system prompt for more advanced models. How to apply the lessons we learned to your own context engineering in Claude Code and with your own agents.

- Category







[Claude Code](https://claude.com/blog/category/claude-code)



[Agents](https://claude.com/blog/category/agents)

- Product







[Claude Code](https://claude.com/product/claude-code)



[Claude Enterprise](https://claude.com/solutions/enterprise)



[Claude Platform](https://claude.com/platform/api)

- Date



July 24, 2026

- Reading time





5



min

- Share

[Copy link](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models#)

https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models


I’ve written previously about how to best [prompt the newest generation of Claude 5 models](https://claude.com/blog/a-field-guide-to-claude-fable-finding-your-unknowns) and work with them iteratively to discover what you want to build.

But when you send a message to Claude, the prompt is only a small part of the context it gets. Much of your context is assembled from your system prompt, Skills, CLAUDE.md files, memory, and other sources. We call this [context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), and it makes a big impact on the results you generate when using Claude Code or in building your own agents.

Unlike a prompt, context is used generally across many requests, so it cannot be as specific.  How do you build these general prompts and guidance for Claude, especially when you don’t know what a user’s prompt might be?

This can be surprisingly difficult as Claude’s own capabilities evolve. Most recently, we noticed a large jump in the way we prompt the newest generation of Claude models. We removed over 80% of Claude Code’s system prompt for models like Claude Opus 5 and Claude Fable 5 with no measurable loss on our coding evaluations.

Here’s what we’ve learned about prompting this new class of models, and how you can utilize it to update your context engineering. We’ve put these best practices in \`claude doctor;\` use the command /doctor in Claude Code to rightsize your skills, and CLAUDE.md files.

## Unhobbling Claude

Overall, we found that we were overconstraining Claude Code, both through our system prompt and in our CLAUDE.md files and skills.

For example, when we read transcripts of our own internal usage of Claude Code, we see several conflicting messages in a single request like “leave documentation as appropriate,” or “DO NOT add comments” as our system prompt, skills, and user requests clash with each other.

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6a63620bedb2b7813b1071e2_afa90c36.png)

Generally, Claude can interpret the user’s intent to get to the right answer, but Claude must think more carefully about these overlapping and conflicting messages before deciding what to do.

And while these constraints were once needed to avoid worst case scenarios, we have since found we can delete many of them and let the model use surrounding context and judgement instead.

Additionally, Claude Code now has many more tools. Claude used to rely on CLAUDE.md as a source of memory, information, and guidance. Now we have memory, artifacts, and skills, which Claude can use to create new ways of loading and sharing context across sessions.

No items found.

[Prev](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models#) Prev

0/5

[Next](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models#) Next

Get Claude Code

exec
/bin/bash -lc "cd /root/note-worker/candidates/20260809-180901 && sed -n '100,320p' sources/The-new-rules-of-context-engineering-for.md" in /root/note-worker
 succeeded in 0ms:
Get Claude Code

curl -fsSL https://claude.ai/install.sh \| bash

Copy command to clipboard

irm https://claude.ai/install.ps1 \| iex

Copy command to clipboard

Or read the [documentation](https://code.claude.com/docs/en/overview)

Try Claude Code

[Try Claude Code](https://claude.ai/code) Try Claude Code

Developer docs

[Developer docs](https://code.claude.com/docs/en/overview) Developer docs

eBook

![](https://cdn.prod.website-files.com/6889473510b50328dbb70ae6/6889473610b50328dbb70b58_placeholder.svg)

![](https://cdn.prod.website-files.com/6889473510b50328dbb70ae6/6889473610b50328dbb70b58_placeholder.svg)![](https://cdn.prod.website-files.com/6889473510b50328dbb70ae6/6889473610b50328dbb70b58_placeholder.svg)

## Then and now

There were a number of previous context engineering best practices that had become myths. Including:.

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6a63620bedb2b7813b107213_3979f6a1.png)

### Then: Give Claude rules

### Now: Let Claude use judgement

When we first rolled out Claude Code, we needed to be sure that Claude avoided worst case scenarios, such as deleting files. This meant we would give particularly strong guidance that might not always be true, For example, in the system prompt we used to say:

_In code: default to writing no comments. Never write multi-paragraph docstrings or multi-line comment blocks — one short line max. Don't create planning, decision, or analysis documents unless the user asks for them — work from conversation context, not intermediate files._

But for a certain subset of prompts, this guidance would be wrong. In the case of documentation, the user may have their own preferences, or specific parts of very complex code might need multi-line comment blocks.

Still, without these guardrails for older models, the comments Claude wrote would be incorrect in many cases and we had to accept this tradeoff. But newer models have better judgement and can handle these decisions well without explicit rules.

In the new system prompt we say: _Write code that reads like the surrounding code: match its comment density, naming, and idiom._

### Then: Give Claude examples

### Now: Design interfaces

The number one rule for tool usage was to give Claude examples on how to use them. With our newest models, we’ve found that giving examples actually constrains them to a certain exploration space.

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6a63620bedb2b7813b107216_c4fdec0d.png)

Instead of using examples, think more about the design of your tools, scripts and files- what parameters does Claude have and how can they be more expressive?

For example, in the Todo tool example, just listing status as an enumeration between pending, in\_progress, and completed, hints to Claude about how to use it. The instruction on keeping one item in\_progress helps define our requested behavior.

### Then: Put it all upfront

### Now: Use progressive disclosure

Because Claude Code was focused on coding, our system prompt included detailed information on how to do code review and verification. These were not always needed, but when they were, it was crucial information.

Since then, Claude Code has gotten very competent at using progressive disclosure- loading the right context at the right times. For example, we moved verification and code review into their own skills that Claude Code could selectively call.

But progressive disclosure is not just for skills, we also use it for tools. Some of our tools are ‘deferred loading,’ which means the agent must search for their full definitions using ToolSearch before using them. This allows us to have more tools (such as our Task tools) that don’t take up context until they’re needed.

The same can be applied to your own CLAUDE.md and Skill.md files. A common myth is that you want to make these a central repository for every known practice that you _might_ run into, because Claude would not find it otherwise. Instead, [consider having a tree of files that can be loaded at the right time](https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code).

### Then: Repeat yourself

### Now: Simple tool descriptions

Earlier Claude models could sometimes need repeated instructions or be more likely to listen to instructions at the end of their context window than at the start. This meant our system prompt would sometimes have references to tools in the main system prompt as well as instructions in the tool description.

We found we could delete these repeat examples and put instructions on how to use tools in the tool descriptions rather than the system prompt.

### Then: Memory in CLAUDE.md files

### Now: Auto-memory

We used to encourage users to save things to Claude’s memory, by using the # hotkey to write to their [CLAUDE.md](http://claude.md/) automatically. Instead, Claude now automatically saves memories that are relevant to the work and to you.

### Then: Simple specs

### Now: Rich references

In plan mode, Claude Code has heavily relied on markdown files with plans. Storing these files as plans helped Claude refer to them when needed. Another similar best practice was to store specs in the codebase for Claude to refer to while working across longer projects.

But we’ve found that Claude can handle increasingly more complicated references. Instead of simple markdown files, Claude can reference HTML artifacts created by our new artifacts feature.

You may also give Claude references in the form of code. A spec may also be a detailed test suite, or a function in a different codebase that Claude might port.

Rubrics are another form of references. Rubrics allow Claude to try and verify your taste in a particular field (e.g. what does a good API design look like) by using [dynamic workflows](https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code) and spinning up verifier agents with those rubrics.

## Applying this to your context

Pulling this all together, what does this look like when you assemble your context?

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6a63620bedb2b7813b10721a_836a850d.png)

### System Prompt

A system prompt is heavily tied to the product context. It tells Claude what product it’s operating in and what it’s doing. For Claude Code, you will likely never modify this, but if you are building your own agent harness, this is where you should spend a lot of time.

### CLAUDE.md

Keep your CLAUDE.md lightweight and briefly describe what your repo is for, but spend most of the tokens on gotchas inside of the codebase. For example, you may organize your code to keep types in one monolithic file and nowhere else. Avoid stating ‘the obvious’ things Claude should know by looking at your file system or your repo.

Use progressive disclosure heavily, for example if you have several unique instructions on how to verify your work, create a verification skill and reference it from your CLAUDE.md.

### Skills

Think of skills as lightweight guides to let Claude find information when needed. Avoid making them overconstrained, except in highly important areas.

For long skills, try and use progressive disclosure as much as possible- divide it into many files and split them out.

It’s best when skills encode particular opinions, knowledge, or best practices that are particular to you, your team, or product.

### References

You can @ mention files to include them as references. References allow Claude to refer to in-depth information about the current plan.

This might be in specs files, mockups, or even entire codebases. Generally you should prefer files that are in code as it provides clear, high-fidelity instructions to Claude in a language it knows very well. For example, a HTML mockup of a design will generally produce better results than a description of the design or a screenshot.

## Try simplifying

Across your system prompt, skills, and CLAUDE.md files, you may need to simplify just like we did. We rolled out a new command called \`claude doctor,\` which will help you do this automatically as well. For more details on prompting more advanced models specifically, check out our [Fable field guide](https://claude.com/blog/a-field-guide-to-claude-fable-finding-your-unknowns).

_This article was written by Thariq Shihipar, member of technical staff, Anthropic._

FAQ

No items found.

## Related posts

Explore more product news and best practices for teams building with Claude.

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/690937bee860a953417a8eee_Object-CodeBrowserGlobe.svg)

Aug 7, 2026

### Auto mode is now the default in Claude Code for Pro, Max, and Team plans

Claude Code

[Auto mode is now the default in Claude Code for Pro, Max, and Team plans](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models#) Auto mode is now the default in Claude Code for Pro, Max, and Team plans

[Auto mode is now the default in Claude Code for Pro, Max, and Team plans](https://claude.com/blog/auto-mode-default-in-claude-code) Auto mode is now the default in Claude Code for Pro, Max, and Team plans

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6903d22b1ef956a6d81cfd9c_653e7474811cf768b6b0f628e253f98c60e2747e-1000x1000.svg)

Aug 7, 2026

### Running auto mode in production

Claude Code

[Running auto mode in production](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models#) Running auto mode in production

[Running auto mode in production](https://claude.com/blog/auto-mode-in-production) Running auto mode in production

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6903d223e0a787df988a824b_39db33950eb113e504a5b9fc56db490a64673e96-1000x1000.svg)

Aug 6, 2026

### Millennium and Anthropic are building a digital risk analyst with Claude

Enterprise AI

[Millennium and Anthropic are building a digital risk analyst with Claude](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models#) Millennium and Anthropic are building a digital risk analyst with Claude

[Millennium and Anthropic are building a digital risk analyst with Claude](https://claude.com/blog/millennium-and-anthropic-are-building-a-digital-risk-analyst-with-claude) Millennium and Anthropic are building a digital risk analyst with Claude

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6903d225e31f7aa22c1f28cb_46e4aa7ea208ed440d5bd9e9e3a0ee66bc336ff1-1000x1000.svg)

Jul 24, 2026

### Claude models explained: choosing the best model for your use case

Enterprise AI

[Claude models explained: choosing the best model for your use case](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models#) Claude models explained: choosing the best model for your use case

[Claude models explained: choosing the best model for your use case](https://claude.com/blog/claude-models-explained-choosing-the-best-model-for-your-use-case) Claude models explained: choosing the best model for your use case

## Transform how your organization operates with Claude

See pricing

[See pricing](https://claude.com/pricing#api) See pricing

Contact sales

[Contact sales](https://claude.com/contact-sales) Contact sales

Get the developer newsletter

Product updates, how-tos, community spotlights, and more. Delivered monthly to your inbox.

[Subscribe](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models#) Subscribe

Please provide your email address if you'd like to receive our monthly developer newsletter. You can unsubscribe at any time.

Thank you! You’re subscribed.

Sorry, there was a problem with your submission, please try again later.

Claude Code

Claude Enterprise

Claude Platform

Agents

Coding

×
exec
/bin/bash -lc "cd /root/note-worker/candidates/20260809-180901 && sed -n '140,220p' sources/The-new-rules-of-context-engineering-for.md" in /root/note-worker
 succeeded in 0ms:
But for a certain subset of prompts, this guidance would be wrong. In the case of documentation, the user may have their own preferences, or specific parts of very complex code might need multi-line comment blocks.

Still, without these guardrails for older models, the comments Claude wrote would be incorrect in many cases and we had to accept this tradeoff. But newer models have better judgement and can handle these decisions well without explicit rules.

In the new system prompt we say: _Write code that reads like the surrounding code: match its comment density, naming, and idiom._

### Then: Give Claude examples

### Now: Design interfaces

The number one rule for tool usage was to give Claude examples on how to use them. With our newest models, we’ve found that giving examples actually constrains them to a certain exploration space.

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6a63620bedb2b7813b107216_c4fdec0d.png)

Instead of using examples, think more about the design of your tools, scripts and files- what parameters does Claude have and how can they be more expressive?

For example, in the Todo tool example, just listing status as an enumeration between pending, in\_progress, and completed, hints to Claude about how to use it. The instruction on keeping one item in\_progress helps define our requested behavior.

### Then: Put it all upfront

### Now: Use progressive disclosure

Because Claude Code was focused on coding, our system prompt included detailed information on how to do code review and verification. These were not always needed, but when they were, it was crucial information.

Since then, Claude Code has gotten very competent at using progressive disclosure- loading the right context at the right times. For example, we moved verification and code review into their own skills that Claude Code could selectively call.

But progressive disclosure is not just for skills, we also use it for tools. Some of our tools are ‘deferred loading,’ which means the agent must search for their full definitions using ToolSearch before using them. This allows us to have more tools (such as our Task tools) that don’t take up context until they’re needed.

The same can be applied to your own CLAUDE.md and Skill.md files. A common myth is that you want to make these a central repository for every known practice that you _might_ run into, because Claude would not find it otherwise. Instead, [consider having a tree of files that can be loaded at the right time](https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code).

### Then: Repeat yourself

### Now: Simple tool descriptions

Earlier Claude models could sometimes need repeated instructions or be more likely to listen to instructions at the end of their context window than at the start. This meant our system prompt would sometimes have references to tools in the main system prompt as well as instructions in the tool description.

We found we could delete these repeat examples and put instructions on how to use tools in the tool descriptions rather than the system prompt.

### Then: Memory in CLAUDE.md files

### Now: Auto-memory

We used to encourage users to save things to Claude’s memory, by using the # hotkey to write to their [CLAUDE.md](http://claude.md/) automatically. Instead, Claude now automatically saves memories that are relevant to the work and to you.

### Then: Simple specs

### Now: Rich references

In plan mode, Claude Code has heavily relied on markdown files with plans. Storing these files as plans helped Claude refer to them when needed. Another similar best practice was to store specs in the codebase for Claude to refer to while working across longer projects.

But we’ve found that Claude can handle increasingly more complicated references. Instead of simple markdown files, Claude can reference HTML artifacts created by our new artifacts feature.

You may also give Claude references in the form of code. A spec may also be a detailed test suite, or a function in a different codebase that Claude might port.

Rubrics are another form of references. Rubrics allow Claude to try and verify your taste in a particular field (e.g. what does a good API design look like) by using [dynamic workflows](https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code) and spinning up verifier agents with those rubrics.

## Applying this to your context

Pulling this all together, what does this look like when you assemble your context?

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6a63620bedb2b7813b10721a_836a850d.png)

### System Prompt

A system prompt is heavily tied to the product context. It tells Claude what product it’s operating in and what it’s doing. For Claude Code, you will likely never modify this, but if you are building your own agent harness, this is where you should spend a lot of time.

### CLAUDE.md

Keep your CLAUDE.md lightweight and briefly describe what your repo is for, but spend most of the tokens on gotchas inside of the codebase. For example, you may organize your code to keep types in one monolithic file and nowhere else. Avoid stating ‘the obvious’ things Claude should know by looking at your file system or your repo.

Use progressive disclosure heavily, for example if you have several unique instructions on how to verify your work, create a verification skill and reference it from your CLAUDE.md.

### Skills

Think of skills as lightweight guides to let Claude find information when needed. Avoid making them overconstrained, except in highly important areas.

For long skills, try and use progressive disclosure as much as possible- divide it into many files and split them out.

It’s best when skills encode particular opinions, knowledge, or best practices that are particular to you, your team, or product.

### References

exec
/bin/bash -lc 'cd /root/note-worker/candidates/20260809-180901 && cat works-ready/The-new-rules-of-context-engineering-for-translation.md' in /root/note-worker
 succeeded in 0ms:
---
created: 2026-08-09
updated: 2026-08-09
title: Claude 5 世代模型的上下文工程新规则
sourceUrl: https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models
sourceAuthor: Thariq Shihipar（Anthropic）
translatedAt: 2026-08-09
sources: [references/articles.md 待处理队列]
tags: [Claude, 上下文工程, AI Agent, Harness, type/翻译]
---

# Claude 5 世代模型的上下文工程新规则

> 我们为更先进的模型删除了 Claude Code 系统提示词中 80% 以上的内容。如何把我们从中学到的经验，
> 应用到 Claude Code 与你自己构建的 agent 的上下文工程中。

我此前写过如何[给最新一代 Claude 5 模型写提示词](https://claude.com/blog/a-field-guide-to-claude-fable-finding-your-unknowns)、
如何与它们迭代式协作去发现你想构建的东西。

但当你向 Claude 发送一条消息时，提示词只是它拿到的上下文里很小的一部分。你的大部分上下文
是由系统提示词、Skills、CLAUDE.md 文件、记忆（memory）和其他来源组装起来的。我们把这称为
[上下文工程（context engineering）](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)，
它对你在 Claude Code 中生成的结果、或构建自己的 agent 时的效果，影响巨大。

与提示词不同，上下文会被大量请求通用性地使用，因此它无法那么具体。你要如何为 Claude 构建
这些通用提示词与引导，尤其是在你并不知道用户会问什么的情况下？

这件事出奇地难，因为 Claude 自身的能力也在不断演进。最近我们注意到，给最新一代 Claude 模型
写提示词的方式发生了巨大跃迁。**对于 Claude Opus 5 和 Claude Fable 5 这样的模型，
我们删除了 Claude Code 系统提示词中 80% 以上的内容，而编码评测没有任何可测量的损失。**

下面是我们对提示这一新类别模型学到的东西，以及你如何利用它来更新自己的上下文工程。
我们已把这些最佳实践放进了 `claude doctor;` —— 在 Claude Code 中使用 `/doctor` 命令，
即可自动调整你的 skills 与 CLAUDE.md 文件到合适规模。

## 解除 Claude 的束缚（Unhobbling Claude）

总的来说，我们发现我们过度约束了 Claude Code——既通过系统提示词，也通过我们的 CLAUDE.md 文件与 skills。

例如，在阅读我们内部使用 Claude Code 的转录记录时，我们看到单次请求中会出现多条互相冲突的
指令，比如「按需留下文档」（leave documentation as appropriate）和「禁止添加注释」（DO NOT add comments），
因为我们的系统提示词、skills 与用户请求在彼此打架。

一般来说，Claude 能够解读用户意图并得出正确答案，但在决定怎么做之前，Claude 必须更仔细地
思考这些重叠且冲突的信息。

这些约束曾经是避免最坏情况所必需的；但后来我们发现，其中很多约束都可以删掉，转而让模型
利用周围的上下文和它自己的判断力。

此外，Claude Code 现在拥有多得多的工具。Claude 曾经依赖 CLAUDE.md 作为记忆、信息和引导的来源；
现在我们有了记忆（memory）、制品（artifacts）和 skills，Claude 可以用它们创造在会话之间
加载与共享上下文的新方式。

## 过去与现在（Then and now）

不少过去的上下文工程最佳实践已经变成了「神话」，包括下面这些。

### 过去：给 Claude 规则

### 现在：让 Claude 运用判断力

当我们最初推出 Claude Code 时，需要确保 Claude 避开最坏情况（比如删除文件）。这意味着我们要给出
一些并不总是正确的特别强硬的引导。例如，我们的系统提示词里曾经写过：

> _在代码中：默认不写注释。绝不写多段 docstring 或多行注释块——最多一行短的。
> 除非用户要求，不要创建规划、决策或分析文档——基于对话上下文工作，而不是中间文件。_

但对于某一部分提示词，这条引导是错误的。以文档为例：用户可能有自己的偏好，或者非常复杂的
代码的某些特定部分确实需要多行注释块。

不过，没有这些护栏时，旧模型写的注释在很多情况下会出错，我们不得不接受这个权衡。
但新模型的判断力更好，即使没有显式规则，也能很好地处理这些决策。

在新的系统提示词里，我们说的是：_写出像周围代码一样可读的代码：匹配它的注释密度、命名和惯用法。_

### 过去：给 Claude 示例

### 现在：设计接口

工具使用的头号规则是给 Claude 提供使用示例。但对于我们的最新模型，我们发现**给示例实际上
会把它们约束在某个特定的探索空间里**。

与其堆示例，不如多思考你的工具、脚本和文件的设计——Claude 能拿到哪些参数？它们能否更有表现力？

例如在 Todo 工具的例子中，仅仅把状态列为 `pending`、`in_progress`、`completed` 这样的枚举，
就暗示了 Claude 该如何使用它；「始终只保留一个 in_progress 项」这条说明则帮助定义了我们期望的行为。

### 过去：把所有信息都前置

### 现在：使用渐进披露（progressive disclosure）

因为 Claude Code 聚焦于编码，我们的系统提示词里包含了关于如何做代码评审和验证的详细信息。
这些信息并非总用得上，但一旦需要，就是关键信息。

此后，Claude Code 已经非常擅长渐进披露——在正确的时间加载正确的上下文。例如，我们把验证和
代码评审移到了独立的 skills 里，由 Claude Code 按需选择性调用。

但渐进披露不只是用于 skills，我们也用于工具。我们的一些工具是「延迟加载」（deferred loading）的，
也就是说 agent 在使用它们之前，必须先通过 ToolSearch 搜索它们的完整定义。这样我们就能拥有更多
工具（比如我们的 Task 工具），它们在需要之前不占上下文。

同样的方法也可以应用到你自己的 CLAUDE.md 与 Skill.md 文件上。一个常见误区是：你想把它们变成
一个收纳所有「可能遇到」的已知实践的中央仓库，因为否则 Claude 就找不到。恰恰相反——
[考虑采用一棵可以在正确时间加载的文件树](https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code)。

### 过去：反复重复

### 现在：精简的工具描述

早期的 Claude 模型有时需要重复的指令，或者更可能听从上下文窗口末尾而不是开头的指令。这意味着
我们的系统提示词里有时既要在主提示词中引用工具，又要在工具描述里写指令。

我们发现可以删掉这些重复的示例，把如何使用工具的说明放到工具描述里，而不是系统提示词里。

### 过去：把记忆放进 CLAUDE.md 文件

### 现在：自动记忆（Auto-memory）

我们过去鼓励用户用 `#` 热键把内容写入 [CLAUDE.md](http://claude.md/) 来自动保存到 Claude 的记忆中。
现在，Claude 会自动保存与工作和你相关的记忆。

### 过去：简单的 spec

### 现在：丰富的引用（Rich references）

在计划模式（plan mode）下，Claude Code 一直重度依赖 Markdown 计划文件。把这些文件存成计划，
能帮助 Claude 在需要时引用它们。另一个类似的最佳实践是把 spec 存在代码库里，供 Claude 在
跨更长项目的过程中引用。

但我们发现 Claude 已经能处理越来越复杂的引用。除了简单的 Markdown 文件，Claude 还能引用由我们
新的 artifacts 功能创建的 HTML 制品。

你也可以以代码的形式给 Claude 引用。一份 spec 也可以是一套详细的测试套件，或是另一个代码库里
Claude 可能需要移植的函数。

评分标准（rubrics）是另一种引用形式。Rubrics 让 Claude 能够借助[动态工作流](https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code)
拉起带这些 rubrics 的验证 agent，尝试核验你在某个领域的品味（比如：好的 API 设计应该长什么样）。

## 应用到你的上下文

把这些串起来，当你组装自己的上下文时，应该是什么样？

### 系统提示词（System Prompt）

系统提示词与产品上下文紧密绑定：它告诉 Claude 自己运行在什么产品里、在做什么。对 Claude Code 而言，
你很可能永远不会修改它；但如果你在构建自己的 agent 执行框架（harness），这里是值得你投入大量时间的地方。

### CLAUDE.md

保持 CLAUDE.md 轻量：简要说明你的仓库是做什么的，但把大部分 token 花在代码库内部的坑（gotchas）上。
例如，你可能约定代码只把类型集中放在一个巨型文件里、别处不放。避免陈述那些 Claude 看看文件系统
或仓库就能知道的「显而易见」的事。

重度使用渐进披露：例如，如果你有几条关于如何验证工作的独特指令，就创建一个验证 skill，并从你的
CLAUDE.md 中引用它。

### Skills

把 skills 看作轻量指南，让 Claude 在需要时能找到信息。除非是极重要的领域，否则避免过度约束。

对于很长的 skill，尽量多用渐进披露——拆成多个文件，逐层展开。

最好的做法是让 skills 承载那些专属于你、你的团队或你的产品的观点、知识或最佳实践。

### 引用（References）

你可以用 `@` 提及文件，把它们作为引用包含进来。引用让 Claude 能参考当前计划的深度信息。

这些文件可以是 spec、原型稿（mockups），甚至整个代码库。一般来说，你应该优先选择代码形态的文件，
因为它能给 Claude 提供它非常熟悉的语言写成的、清晰且高保真的指令。例如，一份设计的 HTML 原型稿
通常比一段设计描述或一张截图产生更好的结果。

## 试着做减法

在你的系统提示词、skills 和 CLAUDE.md 文件中，你很可能也需要像我们一样做减法。我们还推出了
一个名为 `claude doctor` 的新命令，它也能自动帮你完成这件事。关于如何提示更先进的模型，
更多细节可以看我们的 [Fable 现场指南](https://claude.com/blog/a-field-guide-to-claude-fable-finding-your-unknowns)。

_本文作者：Thariq Shihipar，Anthropic 技术团队成员。_

exec
/bin/bash -lc "cd /root/note-worker/candidates/20260809-180901 && sed -n '80,140p' works-ready/The-new-rules-of-context-engineering-for-translation.md" in /root/note-worker
 succeeded in 0ms:
工具使用的头号规则是给 Claude 提供使用示例。但对于我们的最新模型，我们发现**给示例实际上
会把它们约束在某个特定的探索空间里**。

与其堆示例，不如多思考你的工具、脚本和文件的设计——Claude 能拿到哪些参数？它们能否更有表现力？

例如在 Todo 工具的例子中，仅仅把状态列为 `pending`、`in_progress`、`completed` 这样的枚举，
就暗示了 Claude 该如何使用它；「始终只保留一个 in_progress 项」这条说明则帮助定义了我们期望的行为。

### 过去：把所有信息都前置

### 现在：使用渐进披露（progressive disclosure）

因为 Claude Code 聚焦于编码，我们的系统提示词里包含了关于如何做代码评审和验证的详细信息。
这些信息并非总用得上，但一旦需要，就是关键信息。

此后，Claude Code 已经非常擅长渐进披露——在正确的时间加载正确的上下文。例如，我们把验证和
代码评审移到了独立的 skills 里，由 Claude Code 按需选择性调用。

但渐进披露不只是用于 skills，我们也用于工具。我们的一些工具是「延迟加载」（deferred loading）的，
也就是说 agent 在使用它们之前，必须先通过 ToolSearch 搜索它们的完整定义。这样我们就能拥有更多
工具（比如我们的 Task 工具），它们在需要之前不占上下文。

同样的方法也可以应用到你自己的 CLAUDE.md 与 Skill.md 文件上。一个常见误区是：你想把它们变成
一个收纳所有「可能遇到」的已知实践的中央仓库，因为否则 Claude 就找不到。恰恰相反——
[考虑采用一棵可以在正确时间加载的文件树](https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code)。

### 过去：反复重复

### 现在：精简的工具描述

早期的 Claude 模型有时需要重复的指令，或者更可能听从上下文窗口末尾而不是开头的指令。这意味着
我们的系统提示词里有时既要在主提示词中引用工具，又要在工具描述里写指令。

我们发现可以删掉这些重复的示例，把如何使用工具的说明放到工具描述里，而不是系统提示词里。

### 过去：把记忆放进 CLAUDE.md 文件

### 现在：自动记忆（Auto-memory）

我们过去鼓励用户用 `#` 热键把内容写入 [CLAUDE.md](http://claude.md/) 来自动保存到 Claude 的记忆中。
现在，Claude 会自动保存与工作和你相关的记忆。

### 过去：简单的 spec

### 现在：丰富的引用（Rich references）

在计划模式（plan mode）下，Claude Code 一直重度依赖 Markdown 计划文件。把这些文件存成计划，
能帮助 Claude 在需要时引用它们。另一个类似的最佳实践是把 spec 存在代码库里，供 Claude 在
跨更长项目的过程中引用。

但我们发现 Claude 已经能处理越来越复杂的引用。除了简单的 Markdown 文件，Claude 还能引用由我们
新的 artifacts 功能创建的 HTML 制品。

你也可以以代码的形式给 Claude 引用。一份 spec 也可以是一套详细的测试套件，或是另一个代码库里
Claude 可能需要移植的函数。

评分标准（rubrics）是另一种引用形式。Rubrics 让 Claude 能够借助[动态工作流](https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code)
拉起带这些 rubrics 的验证 agent，尝试核验你在某个领域的品味（比如：好的 API 设计应该长什么样）。

## 应用到你的上下文


codex
候选 1 已通读。继续读 Simon Willison 的 Raccoon Heist 原文与译文。
exec
/bin/bash -lc "cd /root/note-worker/candidates/20260809-180901 && sed -n '1,160p' sources/One-shotting-a-Raccoon-Heist-game-using.md" in /root/note-worker
 succeeded in 0ms:
# [Simon Willison’s Weblog](https://simonwillison.net/)

[Subscribe](https://simonwillison.net/about/#subscribe)

**Sponsored by:** Dynatrace — When agents enter the SDLC, observability becomes the enabler to move from code generation to scalable engineering. [Read the blog for a framework to get started](https://fandf.co/4fwyS92)

## One-shotting a Raccoon Heist game using Claude Fable 5

5th August 2026

Back in 2022 [I tweeted](https://twitter.com/simonw/status/1555626060384911360) screenshots of a game concept generated by GPT-3 and some concept “art” created using DALL-E. Today, on the fourth anniversary of that tweet, I decided to see if Claude Fable 5 (running in [Claude Code for web](https://code.claude.com/docs/en/claude-code-on-the-web)) could build the entire game from the content of that tweet. It did a pretty good job of it!

You can [play the game here](https://simonw.github.io/raccoon-heist/). Here’s [the GitHub repo](https://github.com/simonw/raccoon-heist/), and a short video demo:

Your browser does not support HTML5 video.


#### How I built this [\#](https://simonwillison.net/2026/Aug/5/raccoon-heist/\#how-i-built-this)

This is [the August 5th, 2022 tweet](https://twitter.com/simonw/status/1555626060384911360):

![Simon Willison @simonw - New hobby: prototyping video games in 60 seconds using a combination of GPT-3 and DALL-E Here's "Raccoon Heist". Two images - the first is a screenshot of the GPT-3 playground, prompt below. On the right is a very clearly DALL-E generated image of an almost-isometric 3D computer game, with two raccoons sneaking down a street past a futuristic looking building, looking like they want to steal something.](https://static.simonwillison.net/static/2026/raccoon-heist-tweet.webp)

My GPT-3 prompt back then was:

> `Write a detailed product description of a computer game where a team of raccoons go on heists.`

This was in the text completion days, where you asked GPT-3 to complete the rest of the text. It completed:

> In “Raccoon Heist”, you and your team of thieving raccoons are tasked with pulling off a series of daring heists. From robbing banks to stealing priceless art, no job is too big or too small for your furry crew. You’ll need to use your wits and your skills to avoid the police and make a clean getaway with the loot. With exciting gameplay and a charming cast of characters, “Raccoon Heist” is the perfect game for anyone looking for a light-hearted caper.

My prompt to DALL-E was short:

> `Screenshot from a video game where a team of raccoons go on a heist`

Today’s experiment: can I dump those screenshots into Fable 5 with a prompt telling it to write a game, then leave it to its own devices and get a working game at the end?

#### Setting Claude Code for web up to use GitHub Pages [\#](https://simonwillison.net/2026/Aug/5/raccoon-heist/\#setting-claude-code-for-web-up-to-use-github-pages)

A frustrating thing about Claude Code for web is that it can be hard to test what it’s working on while it’s still working.

I’ve been using GitHub Pages to work around that limitation, and found it to work really well.

Here’s my process:

1. Create a new repository for the project at [https://github.com/new](https://github.com/new)—this can be public or private, the trick works equally well for both.
2. Start a Claude Code for web session, in the Claude iPhone or Desktop apps or in the browser at [https://claude.ai/code](https://claude.ai/code)
3. Tell Claude what to work on, and encourage it to commit an `index.html` page as quickly as possible. This will create a branch with a name like `claude/3d-raccoon-heist-game-50n293`
4. Navigate to the Settings -> Pages area for the repository (`github.com/simonw/raccoon-heist/settings/pages` in my case), select “Deploy from a branch”, pick the branch name, and hit Save.

That’s all it takes! Within about 30 seconds of each push the latest content will be visible at `yourname.github.io/your-repo/`.

If you do this with a private repo, anyone who can guess the name of the repo will be able to view the published content. I don’t worry much about this myself.

#### The Fable 5 prompt [\#](https://simonwillison.net/2026/Aug/5/raccoon-heist/\#the-fable-5-prompt)

Here’s the prompt I gave Fable 5 (written in the notes app on my phone—this entire project was conducted on mobile). I accompanied it with the two images from the original tweet.

> `Build this 3D game, for the browser.`
>
> `This repo is configured to serve static files so make sure there is an index.html that loads everything else.`
>
> `Make sure it is mobile-friendly (touch controls, works well on small screens).`
>
> `You have an OpenAI API key and access to their image generation model APIs, use that for textures to use with your 3D models. Docs here: https://developers.openai.com/api/docs/guides/image-generation - use gpt-image-2`
>
> `Work independently - do not ask me to make any further design decisions. Make sure the game is fun, a little surprising, has good raccoon heist vibes, and is visually pleasing.`
>
> `Commit and push as often as possible so I can preview your work - start with an index.html that presents a title screen, then build from there.`
>
> `Append to a notes.md file as you work, including your changes to that as part of every commit.`

I didn’t make any technology choices. I assumed (correctly) that it would probably use [Three.js](https://threejs.org/) based on previous experiments.

Giving Claude access to an OpenAI key turns out to work really well for filling in gaps in its capabilities—in this case we needed some way to generate images to use as textures. Fable is very good at prompting image generators!

I said “Work independently—do not ask me to make any further design decisions” because I wanted to see if it could produce a full, working game without any further input from me.

I also said “Commit and push as often as possible so I can preview your work”. When you use Claude Code in the Claude iPhone app you give it a GitHub repository and it works in a branch. Telling it to “push as often as possible” means commits start landing in that branch straight away.

I like asking for `notes.md` as a bit of added flavor—here’s [that finished file](https://github.com/simonw/raccoon-heist/blob/main/notes.md), and the entry it made when it added the dog:

> New escalation: from night 3 the yards get a patrolling guard dog — a low-poly brown hound with a spiked red collar and a wagging tail. It wanders between random spots, and within 12 units it catches your scent and tracks you by smell (line of sight is irrelevant — it’s all nose, shown by a 👃 over its head and barking). It gives up if you open a 17-unit gap. Getting caught messages are now source-specific: guard / headlights / hound. Verified wander → track → caught with an automated test.

#### Reviewing the transcript [\#](https://simonwillison.net/2026/Aug/5/raccoon-heist/\#reviewing-the-transcript)

You can access [the Claude Code shared session](https://claude.ai/code/session_01NUBoCfnhGETcCDyEUPS8jp), and I also used my [claude-code-transcripts](https://github.com/simonw/claude-code-transcripts) tool to export my own HTML version which you [can find here](https://simonw.github.io/raccoon-heist/transcript/page-001.html).

Fable started with an index page, [vendored a copy](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T14-55-13-304Z) of Three.js, then wrote its own [gen\_textures.py script](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T14-55-49-064Z) ( [copy here](https://github.com/simonw/raccoon-heist/blob/main/gen_textures.py)).

It generated the textures and [spot-checked them](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T14-59-07-900Z) to make sure they looked OK. The [metal.jpg file](https://github.com/simonw/raccoon-heist/blob/main/textures/metal.jpg) it generated for the trash can looks like this, though I don’t think it was applied exactly right in the game itself:

![A game texture atlas of dark blue-grey riveted metal panels, showing a circular hatch with a handle in the top left, ribbed corrugated panels across the middle, a plain circular plate bottom left, and flat banded strips at top and bottom. No text visible.](https://raw.githubusercontent.com/simonw/raccoon-heist/refs/heads/main/textures/metal.jpg)

Then it built out the first basic version of the game, then [decided to](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-04-51-625Z) “smoke-test in the pre-installed Chromium” using Playwright. This meant it could take screenshots of its own work and [eyeball them](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-05-53-823Z). It did that for both desktop and mobile widths of the page, then noticed that [the raccoon was invisible](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-09-33-406Z) at mobile widths, so it [fixed that](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-14-39-180Z):

> The raccoon, dumpster hideout, and both crew raccoons are now perfectly visible on mobile. Committing this critical fix.

It decided to generate a title screen, which [it did](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-15-02-574Z) using this [gen\_title.py](https://github.com/simonw/raccoon-heist/blob/main/gen_title.py) script. Here’s the `gpt-image-2` prompt it used for that:

> `Video game key art, low-poly 3D render style, moody nighttime scene: a cute low-poly raccoon wearing a tiny black burglar mask sneaking on its hind legs carrying a glowing gold coin, next to a tipped-over metal trash can, suburban house with warm glowing windows in the background, deep blue night, full moon, fireflies, cinematic rim lighting, charming heist caper mood. No text, no words, no logos.`

And the resulting image (which Claude [thought was “gorgeous”](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-16-42-176Z))—though I note that when it’s shown on desktop it gets cropped to just the top third without the raccoon!

![Polygon raccoon holding a gold coin next to an overturned trash can, a house and the moon in the background.](https://static.simonwillison.net/static/2026/raccoon-heist-title.jpeg)

Then my favorite change: it [added the dog](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-23-00-850Z):

```
export function makeDog() {
  const g = new THREE.Group();
  const BROWN = 0x8a6440, DARK = 0x5e4128;
  const body = new THREE.Mesh(new THREE.SphereGeometry(0.42, 10, 8), M(BROWN));
  body.scale.set(0.9, 0.8, 1.5);
  body.position.y = 0.55;
  body.castShadow = true;
  g.add(body);
  const head = new THREE.Mesh(new THREE.SphereGeometry(0.3, 10, 8), M(BROWN));
  head.position.set(0, 0.85, 0.62);
  g.add(head);
  const snout = new THREE.Mesh(new THREE.SphereGeometry(0.16, 8, 6), M(DARK));
  snout.scale.set(0.9, 0.7, 1.3);
  snout.position.set(0, 0.76, 0.9);
  g.add(snout);
  const nose = new THREE.Mesh(new THREE.SphereGeometry(0.06, 6, 6), M(BLACK));
  nose.position.set(0, 0.78, 1.08);
  g.add(nose);
  for (const s of [-1, 1]) {
    const ear = new THREE.Mesh(new THREE.SphereGeometry(0.12, 6, 6), M(DARK));
    ear.scale.set(0.7, 1.3, 0.5);
    ear.position.set(0.2 * s, 1.08, 0.55);
    g.add(ear);
    const eye = new THREE.Mesh(new THREE.SphereGeometry(0.05, 6, 6), M(0x1a1a1a, { emissive: 0x331111 }));
    eye.position.set(0.13 * s, 0.92, 0.86);
    g.add(eye);
  }
  const tail = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.09, 0.5, 6), M(DARK));
  tail.position.set(0, 0.8, -0.62);
  tail.rotation.x = 0.8;
  g.add(tail);
  // spiked collar
  const collar = new THREE.Mesh(new THREE.TorusGeometry(0.22, 0.05, 6, 12), M(0xc0392b));
  collar.position.set(0, 0.78, 0.5);
  collar.rotation.x = Math.PI / 2.4;
  g.add(collar);
  const legGeo = new THREE.CylinderGeometry(0.07, 0.09, 0.34, 6);
  const legs = [];
  for (const [x, z] of [[-0.22, 0.35], [0.22, 0.35], [-0.22, -0.35], [0.22, -0.35]]) {
    const leg = new THREE.Mesh(legGeo, M(DARK));
    leg.position.set(x, 0.17, z);
    g.add(leg);
    legs.push(leg);
  }
  let phase = Math.random() * 10;
  return {
    group: g,
    animate(dt, speed) {
      phase += dt * (3 + speed * 10);
      const amp = Math.min(0.6, 0.1 + speed * 0.6);
      legs[0].rotation.x = Math.sin(phase) * amp;

exec
/bin/bash -lc "cd /root/note-worker/candidates/20260809-180901 && sed -n '60,200p' sources/One-shotting-a-Raccoon-Heist-game-using.md" in /root/note-worker
 succeeded in 0ms:
>
> `This repo is configured to serve static files so make sure there is an index.html that loads everything else.`
>
> `Make sure it is mobile-friendly (touch controls, works well on small screens).`
>
> `You have an OpenAI API key and access to their image generation model APIs, use that for textures to use with your 3D models. Docs here: https://developers.openai.com/api/docs/guides/image-generation - use gpt-image-2`
>
> `Work independently - do not ask me to make any further design decisions. Make sure the game is fun, a little surprising, has good raccoon heist vibes, and is visually pleasing.`
>
> `Commit and push as often as possible so I can preview your work - start with an index.html that presents a title screen, then build from there.`
>
> `Append to a notes.md file as you work, including your changes to that as part of every commit.`

I didn’t make any technology choices. I assumed (correctly) that it would probably use [Three.js](https://threejs.org/) based on previous experiments.

Giving Claude access to an OpenAI key turns out to work really well for filling in gaps in its capabilities—in this case we needed some way to generate images to use as textures. Fable is very good at prompting image generators!

I said “Work independently—do not ask me to make any further design decisions” because I wanted to see if it could produce a full, working game without any further input from me.

I also said “Commit and push as often as possible so I can preview your work”. When you use Claude Code in the Claude iPhone app you give it a GitHub repository and it works in a branch. Telling it to “push as often as possible” means commits start landing in that branch straight away.

I like asking for `notes.md` as a bit of added flavor—here’s [that finished file](https://github.com/simonw/raccoon-heist/blob/main/notes.md), and the entry it made when it added the dog:

> New escalation: from night 3 the yards get a patrolling guard dog — a low-poly brown hound with a spiked red collar and a wagging tail. It wanders between random spots, and within 12 units it catches your scent and tracks you by smell (line of sight is irrelevant — it’s all nose, shown by a 👃 over its head and barking). It gives up if you open a 17-unit gap. Getting caught messages are now source-specific: guard / headlights / hound. Verified wander → track → caught with an automated test.

#### Reviewing the transcript [\#](https://simonwillison.net/2026/Aug/5/raccoon-heist/\#reviewing-the-transcript)

You can access [the Claude Code shared session](https://claude.ai/code/session_01NUBoCfnhGETcCDyEUPS8jp), and I also used my [claude-code-transcripts](https://github.com/simonw/claude-code-transcripts) tool to export my own HTML version which you [can find here](https://simonw.github.io/raccoon-heist/transcript/page-001.html).

Fable started with an index page, [vendored a copy](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T14-55-13-304Z) of Three.js, then wrote its own [gen\_textures.py script](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T14-55-49-064Z) ( [copy here](https://github.com/simonw/raccoon-heist/blob/main/gen_textures.py)).

It generated the textures and [spot-checked them](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T14-59-07-900Z) to make sure they looked OK. The [metal.jpg file](https://github.com/simonw/raccoon-heist/blob/main/textures/metal.jpg) it generated for the trash can looks like this, though I don’t think it was applied exactly right in the game itself:

![A game texture atlas of dark blue-grey riveted metal panels, showing a circular hatch with a handle in the top left, ribbed corrugated panels across the middle, a plain circular plate bottom left, and flat banded strips at top and bottom. No text visible.](https://raw.githubusercontent.com/simonw/raccoon-heist/refs/heads/main/textures/metal.jpg)

Then it built out the first basic version of the game, then [decided to](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-04-51-625Z) “smoke-test in the pre-installed Chromium” using Playwright. This meant it could take screenshots of its own work and [eyeball them](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-05-53-823Z). It did that for both desktop and mobile widths of the page, then noticed that [the raccoon was invisible](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-09-33-406Z) at mobile widths, so it [fixed that](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-14-39-180Z):

> The raccoon, dumpster hideout, and both crew raccoons are now perfectly visible on mobile. Committing this critical fix.

It decided to generate a title screen, which [it did](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-15-02-574Z) using this [gen\_title.py](https://github.com/simonw/raccoon-heist/blob/main/gen_title.py) script. Here’s the `gpt-image-2` prompt it used for that:

> `Video game key art, low-poly 3D render style, moody nighttime scene: a cute low-poly raccoon wearing a tiny black burglar mask sneaking on its hind legs carrying a glowing gold coin, next to a tipped-over metal trash can, suburban house with warm glowing windows in the background, deep blue night, full moon, fireflies, cinematic rim lighting, charming heist caper mood. No text, no words, no logos.`

And the resulting image (which Claude [thought was “gorgeous”](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-16-42-176Z))—though I note that when it’s shown on desktop it gets cropped to just the top third without the raccoon!

![Polygon raccoon holding a gold coin next to an overturned trash can, a house and the moon in the background.](https://static.simonwillison.net/static/2026/raccoon-heist-title.jpeg)

Then my favorite change: it [added the dog](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-23-00-850Z):

```
export function makeDog() {
  const g = new THREE.Group();
  const BROWN = 0x8a6440, DARK = 0x5e4128;
  const body = new THREE.Mesh(new THREE.SphereGeometry(0.42, 10, 8), M(BROWN));
  body.scale.set(0.9, 0.8, 1.5);
  body.position.y = 0.55;
  body.castShadow = true;
  g.add(body);
  const head = new THREE.Mesh(new THREE.SphereGeometry(0.3, 10, 8), M(BROWN));
  head.position.set(0, 0.85, 0.62);
  g.add(head);
  const snout = new THREE.Mesh(new THREE.SphereGeometry(0.16, 8, 6), M(DARK));
  snout.scale.set(0.9, 0.7, 1.3);
  snout.position.set(0, 0.76, 0.9);
  g.add(snout);
  const nose = new THREE.Mesh(new THREE.SphereGeometry(0.06, 6, 6), M(BLACK));
  nose.position.set(0, 0.78, 1.08);
  g.add(nose);
  for (const s of [-1, 1]) {
    const ear = new THREE.Mesh(new THREE.SphereGeometry(0.12, 6, 6), M(DARK));
    ear.scale.set(0.7, 1.3, 0.5);
    ear.position.set(0.2 * s, 1.08, 0.55);
    g.add(ear);
    const eye = new THREE.Mesh(new THREE.SphereGeometry(0.05, 6, 6), M(0x1a1a1a, { emissive: 0x331111 }));
    eye.position.set(0.13 * s, 0.92, 0.86);
    g.add(eye);
  }
  const tail = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.09, 0.5, 6), M(DARK));
  tail.position.set(0, 0.8, -0.62);
  tail.rotation.x = 0.8;
  g.add(tail);
  // spiked collar
  const collar = new THREE.Mesh(new THREE.TorusGeometry(0.22, 0.05, 6, 12), M(0xc0392b));
  collar.position.set(0, 0.78, 0.5);
  collar.rotation.x = Math.PI / 2.4;
  g.add(collar);
  const legGeo = new THREE.CylinderGeometry(0.07, 0.09, 0.34, 6);
  const legs = [];
  for (const [x, z] of [[-0.22, 0.35], [0.22, 0.35], [-0.22, -0.35], [0.22, -0.35]]) {
    const leg = new THREE.Mesh(legGeo, M(DARK));
    leg.position.set(x, 0.17, z);
    g.add(leg);
    legs.push(leg);
  }
  let phase = Math.random() * 10;
  return {
    group: g,
    animate(dt, speed) {
      phase += dt * (3 + speed * 10);
      const amp = Math.min(0.6, 0.1 + speed * 0.6);
      legs[0].rotation.x = Math.sin(phase) * amp;
      legs[3].rotation.x = Math.sin(phase) * amp;
      legs[1].rotation.x = -Math.sin(phase) * amp;
      legs[2].rotation.x = -Math.sin(phase) * amp;
      tail.rotation.z = Math.sin(phase * 1.5) * 0.4;
      body.position.y = 0.55 + Math.abs(Math.sin(phase)) * 0.04 * (0.3 + speed);
    },
  };
}
```

And did a [round of testing on it](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-24-09-230Z) using Playwright, including [another screenshot](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-24-33-559Z).

```
  // walk near the dog
  await page.evaluate(() => { const d = window.__rh.dog; window.__rh.teleport(d.x + 6, d.z); });
  await page.waitForTimeout(2000);
  info = await page.evaluate(() => JSON.stringify({ dog: window.__rh.dog, state: window.__rh.state, player: window.__rh.debug().player }));
  console.log('after approach:', info);
  await page.waitForTimeout(3000);
  info = await page.evaluate(() => JSON.stringify({ dog: window.__rh.dog, state: window.__rh.state }));
  console.log('after chase:', info);
  await page.screenshot({ path: __dirname + '/shot-dog.png' });
```

![Screenshot of the game. Night 3, the raccoon is in the middle intersecting with the dog. A message reads Busted! The Guard shooed you off! The screen has a red tinge around the edges.](https://static.simonwillison.net/static/2026/shot-dog.png)

It made a few more tweaks, then [declared itself done](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-29-13-245Z):

> **Raccoon Heist is built, tested, and pushed** — 7 commits on `claude/3d-raccoon-heist-game-50n293`, all verified with automated Playwright playthroughs on desktop, portrait-phone, and landscape-phone viewports.
>
> **The game:** You’re a masked raccoon sneaking out of your crew’s dumpster hideout into a moonlit cul-de-sac. Grab coins, gems, rings, donuts, and fish (they visibly stack on your back and slow you down), then waddle home and bank them before dawn. Each night raises the goal and the heat: night 1 has one flashlight-sweeping guard, night 2 has two, night 3 adds a scent-tracking hound that ignores line-of-sight entirely. A police cruiser sweeps the street with headlights, homeowners randomly peek out of windows, a seagull periodically dive-bombs your unclaimed loot, pizza slices trigger a 6-second speed FRENZY, and a rare golden TV is worth 120 points if you can haul its weight home. Win ranks: TRASH PANDA ⭐ → CAT BURGLAR ⭐⭐ → MASTER OF DISGUISE ⭐⭐⭐, with your best run saved to localStorage.
>
> **How it’s built:** Vendored Three.js (no CDN), procedural low-poly characters, and a procedural WebAudio soundtrack (sneaky walking-bass jazz plus all sound effects — zero audio files). All seven ground/wall textures and the title-screen hero art were generated with gpt-image-2 and committed as static assets, so the deployed game makes no API calls. Mobile gets a dynamic touch joystick (appears wherever you touch) plus a DASH button; desktop uses WASD/arrows and Space.
>
> **Testing caught two real bugs worth mentioning:** the canvas rendered at 2× size on any real phone (a `cssText` assignment was wiping Three.js’s inline sizing — desktop DPR-1 tests masked it completely), and the win screen’s star-rating div inherited the title screen’s full-screen `.stars` CSS and silently swallowed every tap on the “next night” button. Both are fixed and regression-tested, along with pickup, banking, chase/caught, dawn, night progression, and lose/retry flows.
>
> `notes.md` has the full build log. The game is live on the branch — just serve the repo root and open `index.html`.

#### Is the game any good? [\#](https://simonwillison.net/2026/Aug/5/raccoon-heist/\#is-the-game-any-good-)


exec
/bin/bash -lc "cd /root/note-worker/candidates/20260809-180901 && sed -n '200,281p' sources/One-shotting-a-Raccoon-Heist-game-using.md" in /root/note-worker
 succeeded in 0ms:

It’s an impressive starting point, but it’s not a _good_ game.

You move your raccoon around a yard collecting items—donuts, fish, gold coins, jewels—while avoiding guards with flashlights and, in later levels, a dog. You have a limited carrying capacity, and once that’s full you need to drop stuff off at the dumpster. If you pick up a pizza slice you get a temporary speed boost.

There are no team mechanics at all—there are two other static raccoons next to the dumpster but they’re purely decoration.

It gets slightly more challenging as the levels progress—the dog introduced in level 3 is the most interesting new mechanic—but it’s very, very easy to beat. It’s also pretty boring—each night has a fixed duration and you can collect all of the items and then have nothing else to do while waiting for the dawn.

I was impressed by the implementation. It’s fully 3D, there are trash cans, the flashlight illumination cones are fun, and it has a reasonably coherent visual style. It works on mobile. The music (“a procedural WebAudio soundtrack (sneaky walking-bass jazz plus all sound effects — zero audio files)” according to Claude) is simple but feels about right.

As a finished game project, it’s mediocre. As a starting point from a single prompt I think it’s very impressive.

I’ve vibe coded up quite a few games now. They’ve all been deeply disappointing from a gameplay perspective—it turns out designing games that are _fun_ remains a uniquely human trait, and one which requires significantly more skill and experience than either Claude or I can bring to bear.

That said, I thoroughly recommend tinkering with game development projects as a way to explore the capabilities of agents. It’s a fun, low-risk way to try out new things. If you stick at it long enough you might even produce something that’s worth playing!

**Update 7th August 2026**: I posed the same prompt to OpenAI Codex Desktop running GPT-5.6 Sol Ultra and got a [significantly better result](https://simonwillison.net/2026/Aug/7/moonlight-mayhem/)—GPT-5.6 Sol picked up on the importance of the squad of raccoons going on a heist, and built a game where you must rescue your two crewmates in a museum and then stack on top of them to steal the Golden Sardine.

Posted [5th August 2026](https://simonwillison.net/2026/Aug/5/) at 7:42 pm · Follow me on [Mastodon](https://fedi.simonwillison.net/@simon), [Bluesky](https://bsky.app/profile/simonwillison.net), [Twitter](https://twitter.com/simonw) or [subscribe to my newsletter](https://simonwillison.net/about/#subscribe)

## More recent articles

- [Now we have a timeline of the OpenAI accidental attack against Hugging Face](https://simonwillison.net/2026/Aug/7/openai-timeline/) \- 7th August 2026
- [New release of LLM adds support for reasoning traces, OpenAI Responses, server-side tools, and smarter logging](https://simonwillison.net/2026/Aug/4/new-release-of-llm/) \- 4th August 2026

This is **One-shotting a Raccoon Heist game using Claude Fable 5** by Simon Willison, posted on [5th August 2026](https://simonwillison.net/2026/Aug/5/).

[game-design\\
21](https://simonwillison.net/tags/game-design/) [ai\\
2,176](https://simonwillison.net/tags/ai/) [prompt-engineering\\
196](https://simonwillison.net/tags/prompt-engineering/) [generative-ai\\
1,927](https://simonwillison.net/tags/generative-ai/) [llms\\
1,894](https://simonwillison.net/tags/llms/) [anthropic\\
325](https://simonwillison.net/tags/anthropic/) [claude\\
299](https://simonwillison.net/tags/claude/) [text-to-image\\
46](https://simonwillison.net/tags/text-to-image/) [vibe-coding\\
93](https://simonwillison.net/tags/vibe-coding/) [coding-agents\\
233](https://simonwillison.net/tags/coding-agents/) [claude-mythos-fable\\
34](https://simonwillison.net/tags/claude-mythos-fable/)

**Next:** [Now we have a timeline of the OpenAI accidental attack against Hugging Face](https://simonwillison.net/2026/Aug/7/openai-timeline/)

**Previous:** [New release of LLM adds support for reasoning traces, OpenAI Responses, server-side tools, and smarter logging](https://simonwillison.net/2026/Aug/4/new-release-of-llm/)

### Monthly briefing

Sponsor me for **$10/month** and get a curated email digest of the month's most important LLM developments.


Pay me to send you less!


[Sponsor & subscribe](https://github.com/sponsors/simonw/)

- [Disclosures](https://simonwillison.net/about/#disclosures)
- [Colophon](https://simonwillison.net/about/#about-site)
- ©
- [2002](https://simonwillison.net/2002/)
- [2003](https://simonwillison.net/2003/)
- [2004](https://simonwillison.net/2004/)
- [2005](https://simonwillison.net/2005/)
- [2006](https://simonwillison.net/2006/)
- [2007](https://simonwillison.net/2007/)
- [2008](https://simonwillison.net/2008/)
- [2009](https://simonwillison.net/2009/)
- [2010](https://simonwillison.net/2010/)
- [2011](https://simonwillison.net/2011/)
- [2012](https://simonwillison.net/2012/)
- [2013](https://simonwillison.net/2013/)
- [2014](https://simonwillison.net/2014/)
- [2015](https://simonwillison.net/2015/)
- [2016](https://simonwillison.net/2016/)
- [2017](https://simonwillison.net/2017/)
- [2018](https://simonwillison.net/2018/)
- [2019](https://simonwillison.net/2019/)
- [2020](https://simonwillison.net/2020/)
- [2021](https://simonwillison.net/2021/)
- [2022](https://simonwillison.net/2022/)
- [2023](https://simonwillison.net/2023/)
- [2024](https://simonwillison.net/2024/)
- [2025](https://simonwillison.net/2025/)

exec
/bin/bash -lc 'cd /root/note-worker/candidates/20260809-180901 && cat works-ready/One-shotting-a-Raccoon-Heist-game-using-translation.md' in /root/note-worker
 succeeded in 0ms:
---
created: 2026-08-09
updated: 2026-08-09
title: 用 Claude Fable 5 一次做出《Raccoon Heist》游戏
sourceUrl: https://simonwillison.net/2026/Aug/5/raccoon-heist/
sourceAuthor: Simon Willison
translatedAt: 2026-08-09
sources: [references/articles.md 待处理队列]
tags: [AI Agent, Claude, vibe coding, 游戏开发, 提示词工程, type/翻译]
---

# 用 Claude Fable 5 一次做出《Raccoon Heist》游戏

> 2022 年我用 GPT-3 生成了一个游戏概念、用 DALL-E 画了张概念「美术」；今天，在四周年之际，我让 Claude Fable 5 仅凭那条推文的内容做出一整款游戏。它干得相当不错！

2022 年，我在[一条推文](https://twitter.com/simonw/status/1555626060384911360)里贴出过 GPT-3 生成的游戏概念截图，以及用 DALL-E 创作的概念「美术」。今天，在这条推文四周年之际，我决定看看 Claude Fable 5（运行在 [Claude Code for web](https://code.claude.com/docs/en/claude-code-on-the-web) 中）能否仅凭那条推文的内容，把整款游戏做出来。结果它干得相当不错！

你可以[在这里试玩这款游戏](https://simonw.github.io/raccoon-heist/)。这是 [GitHub 仓库](https://github.com/simonw/raccoon-heist/)，还有一个短视频演示：

（视频演示：你的浏览器不支持 HTML5 video，可到原文页面查看）

### 我是怎么做的

这是 [2022 年 8 月 5 日那条推文](https://twitter.com/simonw/status/1555626060384911360)：

![Simon Willison @simonw - 新爱好：用 GPT-3 和 DALL-E 的组合在 60 秒内原型化视频游戏。这就是「Raccoon Heist」。两张图——左边是 GPT-3 playground 的截图，提示词见下。右边是一张明显由 DALL-E 生成的近乎等距视角的 3D 电脑游戏画面：两只浣熊正沿一条街道偷偷溜过，经过一栋未来主义风格的大楼，看起来想偷点东西。](https://static.simonwillison.net/static/2026/raccoon-heist-tweet.webp)

我当年给 GPT-3 的提示词是：

> `Write a detailed product description of a computer game where a team of raccoons go on heists.`

那是文本补全（text completion）的时代——你让 GPT-3 补全剩下的文本。它补全道：

> 在《Raccoon Heist》中，你和你的偷窃浣熊团队将执行一系列大胆的劫案。从抢银行到偷无价之宝的艺术品，对你的毛茸茸团队来说，没有办不到的事。你需要运用你的智慧与技能躲避警察，带着赃物全身而退。激动人心的玩法加上迷人的角色阵容，《Raccoon Heist》是任何想找一场轻松愉快冒险的人的不二之选。

我给 DALL-E 的提示词则非常简短：

> `Screenshot from a video game where a team of raccoons go on a heist`

今天的实验是：我能不能把这些截图丢给 Fable 5，附上一段让它写一款游戏的提示词，然后放手不管，最后拿到一款能玩的成品游戏？

### 为 GitHub Pages 配置 Claude Code for web

Claude Code for web 一个让人沮丧的地方是：它还在工作的时候，你很难实时预览它正在做的东西。

我一直在用 GitHub Pages 绕过这个限制，发现效果非常好。

我的流程是：

1. 在 [https://github.com/new](https://github.com/new) 为项目新建一个仓库——公开或私有都行，这个技巧对两者同样有效。
2. 打开一个 Claude Code for web 会话，在 Claude iPhone 应用、桌面应用或浏览器 [https://claude.ai/code](https://claude.ai/code) 里都行。
3. 告诉 Claude 要做什么，并鼓励它尽快提交一个 `index.html` 页面。这会创建一个类似 `claude/3d-raccoon-heist-game-50n293` 的分支。
4. 进入仓库的 Settings -> Pages 区域（我的情况是 `github.com/simonw/raccoon-heist/settings/pages`），选择「Deploy from a branch」，选中那个分支，点保存。

就这么简单！每次 push 后大约 30 秒，最新内容就会出现在 `yourname.github.io/your-repo/`。

如果你对私有仓库这么做，任何能猜到仓库名的人都能看到发布的内容。我自己不太担心这一点。

### 给 Fable 5 的提示词

下面是我给 Fable 5 的提示词（写在手机上的备忘录应用里——整个项目都是在手机上进行的）。我随提示词附上了原推文中的两张图片。

> 在浏览器里把这款 3D 游戏做出来。
>
> 这个仓库配置为托管静态文件，所以请确保有一个 index.html 加载其他所有内容。
>
> 确保它对移动端友好（触控操作，在小屏幕上表现良好）。
>
> 你有一个 OpenAI API key，可以访问他们的图像生成模型 API，用它们为你的 3D 模型生成贴图。文档在这里：https://developers.openai.com/api/docs/guides/image-generation - 使用 gpt-image-2
>
> 独立工作——不要让我做任何进一步的设计决定。确保游戏有趣、带点惊喜、有良好的浣熊劫案氛围，并且视觉上赏心悦目。
>
> 尽可能频繁地提交并推送，这样我就能预览你的进度——先从一个带标题画面的 index.html 开始，然后在此基础上继续构建。
>
> 边工作边把进展写进 notes.md 文件，并把对它的修改包含进每一次提交。

我没有做任何技术选型。我（正确地）猜它大概会用 [Three.js](https://threejs.org/)——基于以往的经验。

给 Claude 一个 OpenAI key 的效果出乎意料地好，正好补上它能力的缺口——这次我们需要某种生成图片来当贴图的方式。Fable 非常擅长给图像生成器写提示词！

我说「独立工作——不要让我做任何进一步的设计决定」，是因为我想看看它能否在不需要我任何进一步输入的情况下，产出一款完整可玩的游戏。

我还说了「尽可能频繁地提交并推送，这样我就能预览你的进度」。当你在 Claude iPhone 应用里使用 Claude Code 时，你会给它一个 GitHub 仓库，它在分支上工作。告诉它「尽可能频繁推送」，提交就会立刻开始落进那个分支。

我喜欢要一份 `notes.md` 作为一点额外风味——这是[那份最终文件](https://github.com/simonw/raccoon-heist/blob/main/notes.md)，以及它加入那条狗时写的记录：

> 新的升级：从第 3 夜起，院子里会有一只巡逻的护卫犬——一只低多边形棕色猎犬，戴着红色尖刺项圈，尾巴摇来摇去。它会在随机地点之间游荡，12 个单位内闻到你的气味就会追踪你（视线完全无关——全靠鼻子，头顶会显示 👃 并且会吠叫）。如果你拉开 17 个单位的距离，它就会放弃。被抓提示现在按来源区分：守卫 / 车灯 / 猎犬。已用自动化测试验证 游荡 → 追踪 → 被抓 的流程。

### 回顾对话记录

你可以访问 [Claude Code 共享会话](https://claude.ai/code/session_01NUBoCfnhGETcCDyEUPS8jp)，我还用我的 [claude-code-transcripts](https://github.com/simonw/claude-code-transcripts) 工具导出了一份我自己的 HTML 版本，[可以在这里找到](https://simonw.github.io/raccoon-heist/transcript/page-001.html)。

Fable 先做了一个 index 页面，[内置了一份](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T14-55-13-304Z) Three.js 副本，然后写了自己的 [gen_textures.py 脚本](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T14-55-49-064Z)（[副本在这里](https://github.com/simonw/raccoon-heist/blob/main/gen_textures.py)）。

它生成了贴图，并[抽查](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T14-59-07-900Z)确认效果没问题。它给垃圾桶生成的 [metal.jpg](https://github.com/simonw/raccoon-heist/blob/main/textures/metal.jpg) 长这样，不过我并不觉得它在游戏里被用对了地方：

![一张深蓝灰色铆接金属面板的游戏纹理图集：左上角是带把手的圆形舱门，中间是瓦楞波纹板，左下角是素面圆形板，顶部和底部是平坦的带状条。没有可见文字。](https://raw.githubusercontent.com/simonw/raccoon-heist/refs/heads/main/textures/metal.jpg)

然后它搭出了游戏的第一版，接着[决定](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-04-51-625Z)用 Playwright 在「预装的 Chromium」里做冒烟测试。这意味着它可以给自己的作品截图，然后[亲自过目](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-05-53-823Z)。它分别对桌面和移动宽度的页面做了这件事，然后注意到[移动宽度下浣熊不可见](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-09-33-406Z)，于是[修复了它](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-14-39-180Z)：

> 浣熊、垃圾箱藏身处和两个队友浣熊在移动端现在完全可见了。提交这个关键修复。

它决定做一个标题画面，用这个 [gen_title.py](https://github.com/simonw/raccoon-heist/blob/main/gen_title.py) 脚本[做了出来](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-15-02-574Z)。这是它给 `gpt-image-2` 用的提示词：

> `Video game key art, low-poly 3D render style, moody nighttime scene: a cute low-poly raccoon wearing a tiny black burglar mask sneaking on its hind legs carrying a glowing gold coin, next to a tipped-over metal trash can, suburban house with warm glowing windows in the background, deep blue night, full moon, fireflies, cinematic rim lighting, charming heist caper mood. No text, no words, no logos.`

（中文：游戏主视觉，低多边形 3D 渲染风格，阴郁的夜景：一只戴着小小黑色强盗面罩的可爱低多边形浣熊，用后腿蹑手蹑脚地走，叼着一枚发光的金币，旁边是一个被掀翻的金属垃圾桶，背景是亮着暖光窗户的郊区房屋，深蓝夜空、满月、萤火虫、电影感轮廓光，迷人的劫案片氛围。不要文字、不要单词、不要 logo。）

生成的图片（Claude [觉得它「美极了」](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-16-42-176Z)）——不过我注意到，它在桌面端显示时会被裁掉，只剩上面三分之一，浣熊都不见了！

![一只拿着金币的多边形浣熊，旁边是翻倒的垃圾桶，背景是房子和月亮。](https://static.simonwillison.net/static/2026/raccoon-heist-title.jpeg)

然后是我最喜欢的一处改动：它[加了一条狗](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-23-00-850Z)：

```
export function makeDog() {
  const g = new THREE.Group();
  const BROWN = 0x8a6440, DARK = 0x5e4128;
  const body = new THREE.Mesh(new THREE.SphereGeometry(0.42, 10, 8), M(BROWN));
  body.scale.set(0.9, 0.8, 1.5);
  body.position.y = 0.55;
  body.castShadow = true;
  g.add(body);
  const head = new THREE.Mesh(new THREE.SphereGeometry(0.3, 10, 8), M(BROWN));
  head.position.set(0, 0.85, 0.62);
  g.add(head);
  const snout = new THREE.Mesh(new THREE.SphereGeometry(0.16, 8, 6), M(DARK));
  snout.scale.set(0.9, 0.7, 1.3);
  snout.position.set(0, 0.76, 0.9);
  g.add(snout);
  const nose = new THREE.Mesh(new THREE.SphereGeometry(0.06, 6, 6), M(BLACK));
  nose.position.set(0, 0.78, 1.08);
  g.add(nose);
  for (const s of [-1, 1]) {
    const ear = new THREE.Mesh(new THREE.SphereGeometry(0.12, 6, 6), M(DARK));
    ear.scale.set(0.7, 1.3, 0.5);
    ear.position.set(0.2 * s, 1.08, 0.55);
    g.add(ear);
    const eye = new THREE.Mesh(new THREE.SphereGeometry(0.05, 6, 6), M(0x1a1a1a, { emissive: 0x331111 }));
    eye.position.set(0.13 * s, 0.92, 0.86);
    g.add(eye);
  }
  const tail = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.09, 0.5, 6), M(DARK));
  tail.position.set(0, 0.8, -0.62);
  tail.rotation.x = 0.8;
  g.add(tail);
  // spiked collar
  const collar = new THREE.Mesh(new THREE.TorusGeometry(0.22, 0.05, 6, 12), M(0xc0392b));
  collar.position.set(0, 0.78, 0.5);
  collar.rotation.x = Math.PI / 2.4;
  g.add(collar);
  const legGeo = new THREE.CylinderGeometry(0.07, 0.09, 0.34, 6);
  const legs = [];
  for (const [x, z] of [[-0.22, 0.35], [0.22, 0.35], [-0.22, -0.35], [0.22, -0.35]]) {
    const leg = new THREE.Mesh(legGeo, M(DARK));
    leg.position.set(x, 0.17, z);
    g.add(leg);
    legs.push(leg);
  }
  let phase = Math.random() * 10;
  return {
    group: g,
    animate(dt, speed) {
      phase += dt * (3 + speed * 10);
      const amp = Math.min(0.6, 0.1 + speed * 0.6);
      legs[0].rotation.x = Math.sin(phase) * amp;
      legs[3].rotation.x = Math.sin(phase) * amp;
      legs[1].rotation.x = -Math.sin(phase) * amp;
      legs[2].rotation.x = -Math.sin(phase) * amp;
      tail.rotation.z = Math.sin(phase * 1.5) * 0.4;
      body.position.y = 0.55 + Math.abs(Math.sin(phase)) * 0.04 * (0.3 + speed);
    },
  };
}
```

接着用 Playwright 对它做了一[轮测试](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-24-09-230Z)，包括[另一张截图](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-24-33-559Z)。

```
  // walk near the dog
  await page.evaluate(() => { const d = window.__rh.dog; window.__rh.teleport(d.x + 6, d.z); });
  await page.waitForTimeout(2000);
  info = await page.evaluate(() => JSON.stringify({ dog: window.__rh.dog, state: window.__rh.state, player: window.__rh.debug().player }));
  console.log('after approach:', info);
  await page.waitForTimeout(3000);
  info = await page.evaluate(() => JSON.stringify({ dog: window.__rh.dog, state: window.__rh.state }));
  console.log('after chase:', info);
  await page.screenshot({ path: __dirname + '/shot-dog.png' });
```

![游戏截图。第 3 夜，浣熊在画面中间和狗撞在一起。一条消息显示「Busted! The Guard shooed you off!（被抓了！守卫把你赶走了！）」屏幕边缘泛着红色。](https://static.simonwillison.net/static/2026/shot-dog.png)

它又做了几处微调，然后[宣布完工](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-29-13-245Z)：

> **Raccoon Heist 已构建、测试并推送** —— 分支 `claude/3d-raccoon-heist-game-50n293` 上 7 次提交，全部通过桌面、竖屏手机、横屏手机视口下的 Playwright 自动化通关验证。
>
> **游戏内容：** 你是一只戴着面罩的浣熊，从团队的垃圾箱藏身点溜出来，进入一条月光下的尽端路（cul-de-sac）。捡起金币、宝石、戒指、甜甜圈和鱼（它们会可见地叠在你的背上并拖慢你的速度），然后在黎明前蹒跚回家把它们存进仓库。每过一夜，目标和热度都会提高：第 1 夜有一个扫着手电筒的守卫，第 2 夜有两个，第 3 夜加了一条完全无视视线的嗅觉追踪猎犬。一辆警车用车灯扫过街道，房主会随机从窗户探出头来，海鸥会时不时俯冲轰炸你没收好的战利品，披萨片会触发 6 秒的速度狂热（FRENZY），还有一台稀有的金色电视，如果你能把它拖回家，就值 120 分。胜利段位：TRASH PANDA ⭐（垃圾熊猫）→ CAT BURGLAR ⭐⭐（入室窃贼）→ MASTER OF DISGUISE ⭐⭐⭐（伪装大师），最佳记录保存在 localStorage 里。
>
> **实现方式：** 内置 Three.js（无 CDN）、程序化生成的低多边形角色，以及一段程序化生成的 WebAudio 配乐（鬼祟的行走贝斯爵士乐加全部音效——零音频文件）。全部七张地面/墙壁贴图和标题画面主视觉都由 gpt-image-2 生成并作为静态资源提交，所以部署后的游戏不做任何 API 调用。移动端有动态触控摇杆（出现在你手指触碰的位置）外加 DASH 冲刺按钮；桌面端用 WASD/方向键和空格。
>
> **测试抓到了两个值得一提的真实 bug：** canvas 在任何真机上都会以 2 倍尺寸渲染（一个 `cssText` 赋值把 Three.js 的内联尺寸设置清掉了——桌面端 DPR-1 测试完全掩盖了这个问题）；胜利画面的星级评分 div 继承了标题画面的全屏 `.stars` CSS，悄悄吞掉了「下一夜」按钮的每次点击。两个都已修复并做了回归测试；拾取、存款、追逐/被抓、黎明、夜晚推进、失败/重试流程也都测过了。
>
> `notes.md` 里有完整的构建日志。游戏已经部署在该分支上——只需托管仓库根目录并打开 `index.html`。

### 这游戏好玩吗？

它是一个令人印象深刻的起点，但不是一款_好_游戏。

你操控浣熊在院子里移动、收集物品——甜甜圈、鱼、金币、宝石——同时躲避打着手电筒的守卫，后期关卡还要躲一条狗。你的携带容量有限，装满后得先去垃圾箱卸货。捡起一片披萨会获得临时加速。

完全没有团队机制——垃圾箱旁边有两只静止不动的浣熊，但它们纯粹是装饰。

随着关卡推进，难度会稍微上升——第 3 关引入的狗是最有意思的新机制——但这游戏非常、非常容易通关。它也挺无聊：每个夜晚时长固定，你可以把物品全捡完，然后只能干等着天亮。

我对实现本身印象深刻。它是完整的 3D，有垃圾桶，手电筒的光照锥很好玩，视觉风格也算自洽。它能在移动端运行。音乐（按 Claude 的说法是「程序化生成的 WebAudio 配乐（鬼祟的行走贝斯爵士乐加全部音效——零音频文件）」）很简单，但感觉刚刚好。

作为一款完成的游戏项目，它平庸。但作为从单条提示词出发的起点，我觉得它非常令人印象深刻。

我已经用氛围编码（vibe coding）做过不少游戏了。从玩法角度看，它们全都让人大失所望——事实证明，设计出_好玩_的游戏依然是人类独有的天赋，而且需要的技巧和经验，远比 Claude 或我能带来的多得多。

话虽如此，我强烈推荐把游戏开发小项目当作探索 agent 能力的方式。它好玩、低风险，适合尝试新东西。如果你坚持得够久，说不定还能做出点值得一玩的东西！

**2026 年 8 月 7 日更新：** 我把同样的提示词丢给了运行 GPT-5.6 Sol Ultra 的 OpenAI Codex Desktop，得到了[明显更好的结果](https://simonwillison.net/2026/Aug/7/moonlight-mayhem/)——GPT-5.6 Sol 抓住了「一队浣熊去干一票」的重点，做了一款你必须在一座博物馆里救出两位队友、然后叠罗汉偷走金沙丁鱼（Golden Sardine）的游戏。

codex
候选 2 已读完。接着读 Vercel 编排模式与 Duolingo 两篇。
exec
/bin/bash -lc "cd /root/note-worker/candidates/20260809-180901 && head -30 sources/Six-Agent-Orchestration-Patterns.md && echo '===TAIL===' && tail -40 sources/Six-Agent-Orchestration-Patterns.md" in /root/note-worker
 succeeded in 0ms:
[Skip to content](https://vercel.com/i/agent-orchestration-patterns#geist-skip-nav)

Once an AI feature grows past a single prompt, the decision becomes how to connect large language model (LLM) calls into a system that stays reliable under production load. The right orchestration pattern should match task decomposability, latency tolerance, token budget, and human-in-the-loop requirements. Start with the least complex pattern that solves the problem, then escalate only when the workload demands it. Six patterns map to those tradeoffs across reliability, cost, and coordination.

**Key takeaways:**

- Multi-agent systems can use up to 15× the token volume of standard chats, so task value has to justify the added complexity.

- Under equal compute budgets, single-agent loops match or exceed multi-agent accuracy on multi-hop reasoning tasks across Qwen3, DeepSeek-R1, and Gemini 2.5.

- Prompt chaining is the lowest-risk upgrade from a single LLM call, but chained accuracy compounds step by step.

- Orchestrator-worker is the pattern designed for cases where subtask count and nature are unknown at authoring time, which makes it the entry point for multi-agent work rather than the default.

- Vercel Workflows checkpoints each step and handles failure retries plus pauses for external events, so any of the six patterns can run durably.

- FLORA's creative agent fans a single session across more than 50 image models, with each step persisting and retrying on failure.


## [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#agent-orchestration-patterns-at-a-glance) Agent orchestration patterns at a glance

Start with the lowest-complexity pattern before adding agents. The six patterns form a complexity ladder. The premature fan-out anti-pattern appears when a team adds agents before the workload has independent subtasks, compounding cost and failure surface at the same time.

Multi-agent systems use approximately [15× more tokens](https://www.anthropic.com/engineering/multi-agent-research-system) than chat interactions, so task value has to justify the added agents. Pattern choice depends on the workload rather than the team's ambition.

The six patterns differ by fit, token cost, and failure conditions. Use this table as a planning range before choosing a pattern:

| Pattern | Best for | Token cost relative to single call | When to avoid |
| --- | --- | --- | --- |
| Single-agent loop | Tasks that fit one context window with tool access | Baseline | Independent subtasks that benefit from parallel exploration |
===TAIL===

- **Unified model routing:** AI Gateway handles automatic failover across the same routing layer, removing per-provider integration from application code.

- **Isolated code execution:** Vercel Sandbox runs worker and evaluator code in a Firecracker microVMs with bounded execution windows.

- **End-to-end observability:** [OpenTelemetry](https://ai-sdk.dev/docs/ai-sdk-core/telemetry) session correlation links traces across orchestrator and worker agents in one view.


Deploy a [new project](https://vercel.com/new) to start with a single-agent loop, or begin from [Vercel templates](https://vercel.com/templates) and escalate patterns only when the workload demands it. Keep the first version as small as the task allows, then add coordination when the workload proves the need.

## [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#frequently-asked-questions-about-agent-orchestration) Frequently asked questions about agent orchestration

### [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#what-is-the-difference-between-orchestrator-worker-and-hierarchical-multi-agent-patterns) What is the difference between orchestrator-worker and hierarchical multi-agent patterns?

A supervisor routes among a predefined roster of specialists and controls the communication flow. An orchestrator derives the subtasks themselves at runtime and delegates them to worker agents.

### [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#when-should-i-use-a-single-agent-loop-instead-of-multi-agent-orchestration) When should I use a single-agent loop instead of multi-agent orchestration?

Use a single-agent loop when the task fits one context window, when subtasks cannot be split to run in parallel, and when latency or token budgets are tight. Escalate only when a concrete capability gap makes multi-agent orchestration necessary.

### [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#how-does-token-cost-scale-across-agent-orchestration-patterns) How does token cost scale across agent orchestration patterns?

Token cost scales as you add model calls, workers, critique cycles, and separate context windows. Use the relative multipliers in the table as a planning range rather than treating any pattern as a fixed price.

### [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#what-makes-a-workflow-durable-in-an-agent-orchestration-context) What makes a workflow durable in an agent orchestration context?

Durable execution checkpoints state after each step, so a failure mid-chain resumes from the last successful step. Vercel Workflows implements durability with the `use workflow` directive, so a run can pause for a webhook or a human approval without holding compute and resume from the last checkpoint.

## More Build with AI articles

- [**How to choose an embedding model for production retrieval** \\
Embedding models set retrieval quality and lock your schema. Learn six selection criteria, four eval practices, and how to keep model swaps cheap.](https://vercel.com/i/embedding-model-selection-guide)
- [**5 AI agent guardrails that hold in production** \\
Learn five runtime guardrail patterns for AI agents: input validation, tool scoping, approval gates, loop limits, and output checks on Vercel.](https://vercel.com/i/five-ai-agent-guardrails-production)

* * *

## Ready to deploy?

[Start deploying](https://vercel.com/new) [Talk to an expert](https://vercel.com/contact/sales)

exec
/bin/bash -lc "cd /root/note-worker/candidates/20260809-180901 && sed -n '30,153p' sources/Six-Agent-Orchestration-Patterns.md" in /root/note-worker
 succeeded in 0ms:
| Single-agent loop | Tasks that fit one context window with tool access | Baseline | Independent subtasks that benefit from parallel exploration |
| Prompt chaining | Fixed subtasks known at authoring time | Moderate, fixed by chain length | Unknown subtask boundaries |
| Routing | Distinct input categories handled separately | Low to moderate | Inputs that need identical handling |
| Parallelization | Predefined independent subtasks | High, varies with fan-out | Sequential dependencies or shared context |
| Orchestrator-worker | Subtasks unpredictable until runtime | High, varies with worker count | Predictable subtasks |
| Evaluator-optimizer | Clear rubric plus measurable gains from iteration | Moderate, varies with critique cycles | Real-time responses or no rubric |

Those ranges are relative estimates anchored to measured agent and multi-agent token figures. The July 2026 AI Gateway Production Index puts Anthropic at [61% of AI Gateway spend](https://vercel.com/blog/ai-gateway-production-index-july-2026) on 32% of tokens, so the most consequential agentic work concentrates cost. Choosing among [agentic workflow patterns](https://vercel.com/i/what-are-agentic-workflows) comes before any infrastructure decision.

## [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#1.-start-agent-orchestration-with-a-single-agent-loop) 1\. Start agent orchestration with a single-agent loop

Under equal token budgets, [single-agent baselines](https://arxiv.org/html/2604.02460v1) match or exceed multi-agent accuracy on multi-hop reasoning, with reported multi-agent advantages better explained by unaccounted computation than by architecture.

The same constraint appears in production. The less complex architecture will get you far, while parallel writing still runs into coordination and context-sharing constraints. Escalation should follow a capability gap, such as context-window pressure or independent subtasks that can actually run in parallel.

A single-agent loop is an LLM that calls tools, receives results, adds them to context, and repeats until a stopping condition is met. In AI SDK 7, [`ToolLoopAgent`](https://ai-sdk.dev/docs/reference/ai-sdk-core/tool-loop-agent) runs this loop and stops after 20 steps by default through `stopWhen: stepCountIs(20)`. The `prepareStep` callback can adjust the model, tools, messages, and runtime context between steps. AI SDK 7 also adds typed `runtimeContext`, agent-level tool approvals, and total, per-step, per-chunk, and per-tool timeouts. State management problems, including repeated account numbers and re-run searches, push teams off this pattern. A `WorkflowAgent` turns the loop into separate invocations, so completed steps never re-run.

## [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#2.-use-prompt-chaining-for-fixed-agent-orchestration-steps) 2\. Use prompt chaining for fixed agent orchestration steps

Prompt chaining runs a fixed sequence of LLM calls where each call processes the previous output. Prompt chaining fits tasks with fixed decomposition. It trades latency for accuracy by narrowing each call's scope. Accuracy compounds across steps. At 95% per-step accuracy across ten steps, end-to-end accuracy is about 60%, and at 90% it is about 35%.

That compounding is why programmatic gates between steps are not optional. Gates can check schema validity, required fields, policy thresholds, or human approval before the next call inherits a bad intermediate result. Vercel's internal data agent d0 runs durable multi-step orchestration in production.

The AI SDK handles its model calls, while [Vercel Workflows](https://vercel.com/docs/workflows) adds retry and state recovery when Snowflake times out or a model call fails, and pauses a run that has to wait on a person or a webhook. Skip chaining when subtask boundaries are unknown at authoring time, or when independent subtasks could run at the same time.

## [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#3.-route-agent-orchestration-by-input-type) 3\. Route agent orchestration by input type

Routing adds an initial classification step, LLM-based or deterministic, that assigns each input to a specialized downstream handler. It separates concerns and works when distinct categories are better handled separately. Router accuracy sets a ceiling on the whole system, because a misclassified input sends the wrong work to a specialist handler.

Wherever the input space allows it, prefer deterministic classifiers (regex, keyword match, rule-based routing), since they remove one model failure surface entirely. Routing also needs a validation set that reflects production inputs, since a clean taxonomy on paper does not guarantee reliable classification at the boundary.

At the model level, [AI Gateway](https://vercel.com/docs/ai-gateway) routes across hundreds of models through a single endpoint. It handles automatic failover and load balancing, with per-provider fallback. Okara runs chief marketing officer (CMO) agents for [120,000+ businesses](https://vercel.com/customers/how-okara-runs-cmo-agents-for-120000-companies-on-vercel) on this layer, and with retry and fallback handling moved into the gateway it now processes 4 billion tokens daily. Skip routing when every input needs identical handling or classification accuracy can't be validated.

## [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#4.-run-parallel-agent-orchestration-for-independent-subtasks) 4\. Run parallel agent orchestration for independent subtasks

Parallelization runs independent subtasks simultaneously and aggregates their outputs programmatically. It uses predefined subtasks, while orchestrator-worker determines them at runtime. The pattern fits when subtasks can run at the same time for speed, or when multiple perspectives on one task raise confidence in the result. The aggregation step should be defined before fan-out starts, because inconsistent worker outputs can erase the latency benefit at merge time.

AI SDK represents a [subagent](https://ai-sdk.dev/docs/agents/subagents) as an agent invoked through a parent agent's tool. Each subagent receives its own context window and returns a focused result to the parent, which keeps context-heavy or parallel work out of the main agent's history. Subagents add latency and coordination cost, so use them only when context isolation or parallel execution provides a measurable benefit.

In wide fan-out, billing matters as much as code, since each concurrent invocation spends most of its life waiting on a model call. FLORA's creative agent fans out across more than 50 image models from one session. [Fluid compute](https://vercel.com/docs/fluid-compute) prices on active central processing unit (CPU), so waiting on a model call does not add to that meter. Skip parallelization when subtasks must build on one another in sequence or need one shared context.

## [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#5.-choose-orchestrator-worker-agent-orchestration-for-dynamic-decomposition) 5\. Choose orchestrator-worker agent orchestration for dynamic decomposition

In orchestrator-worker, a central LLM determines at runtime which subtasks a request needs, assigns them to worker agents, and synthesizes the results. With the AI SDK, each worker can be implemented as a subagent exposed to a parent `ToolLoopAgent` through a tool. The worker runs with an isolated context and returns a summarized result for synthesis. The fit is a complex task where the subtasks can't be predicted, like coding, where the number of files to change depends on the request. It is over-engineered for anything else. Each worker holds its own context window, which means coordination adds cost as well as capability.

General Intelligence's Cofounder gives founders a full team of agents covering engineering, marketing, search engine optimization (SEO), finance, sales, customer support, and operations, a shape consistent with orchestrator-worker. Its engineers ship [10 pull requests](https://vercel.com/customers/how-general-intelligence-used-agents-to-build-an-agent-platform-on-vercel) (PRs) and 70+ commits per engineer per day across 4,000+ preview branches, and 90% of site reliability engineering (SRE) work is automated. Worker code runs isolated in [Vercel Sandbox](https://vercel.com/docs/sandbox) microVMs with a separate filesystem and network. Skip the pattern when subtasks are predictable, or coordination overhead outweighs the value of dynamic decomposition.

## [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#6.-apply-evaluator-optimizer-agent-orchestration-when-quality-can-be-measured) 6\. Apply evaluator-optimizer agent orchestration when quality can be measured

Evaluator-optimizer pairs two LLM calls in a loop. One generates a response, the other evaluates it and provides feedback, and the cycle continues until a quality threshold or step ceiling is reached. The pattern needs a clear evaluation rubric and measurable gains from iterative refinement, so it earns its cost only when responses improve under critique.

Two signs make the fit stronger: responses improve when a human can articulate useful feedback, and the LLM can provide useful feedback itself. The runaway critique loop anti-pattern appears when ambiguous criteria keep requesting revisions without a measurable endpoint. Avoid the pattern when first-attempt quality already meets requirements, and enforce a hard revision ceiling in application code. For agent-based implementations, the AI SDK exposes `stopWhen` conditions and AI SDK 7 timeout budgets for bounding total and per-step execution.

[Vercel's Turborepo](https://vercel.com/solutions/turborepo) performance work is the human-in-the-loop version of that critique cycle. AI agents, Vercel Sandboxes, and human review over eight days produced up to a [96% speed improvement](https://vercel.com/blog/making-turborepo-ninety-six-percent-faster-with-agents-sandboxes-and-humans), and the same effort found that unattended state-of-the-art agents without context engineering fall short.

Vercel's Next.js agent evals found `AGENTS.md` outperformed skills on Next.js 16 APIs. Vercel Sandbox caps each isolated run at 45 minutes on Hobby and 24 hours on Pro and Enterprise, which bounds how long a critique loop can execute.

## [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#how-vercel-runs-agent-orchestration-patterns-in-production) How Vercel runs agent orchestration patterns in production

The six patterns are architecture decisions, but four platform behaviors remove failure modes that compound across them. In practice, they address the same runtime concerns across different shapes of work, including state recovery, model selection, fan-out cost, and isolated execution.

### [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#fluid-compute-reduces-active-cpu-cost-in-fan-out-steps) Fluid compute reduces active-CPU cost in fan-out steps

Parallelization and orchestrator-worker fan out into many concurrent invocations dominated by I/O wait. A team has to reject any billing model that charges for that wait, since it makes wide fan-out impractical. Fluid compute meters active CPU separately at a [$0.128/hour base rate](https://vercel.com/docs/functions/usage-and-pricing), with regional rates and other metered resources still applicable.

### [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#vercel-workflows-makes-each-pattern-durable) Vercel Workflows makes each pattern durable

Chaining, orchestrator-worker, and evaluator-optimizer all fail expensively when state disappears mid-run. The `use workflow` directive turns async TypeScript functions into durable workflows with checkpointing and retries. Runs can also pause and resume, so a failed run continues from the last good step. Workflow steps on Pro and Enterprise support execution durations up to 1,800 seconds.

### [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#ai-gateway-centralizes-model-routing-across-patterns) AI Gateway centralizes model routing across patterns

Routing and orchestrator-worker select models by task requirements and provider health, while cost constraints shape the fallback policy. Per-provider integration work slows product work. AI Gateway consolidates that into one unified endpoint with retries and load balancing, plus configurable fallbacks and zero markup on tokens. Provider integration lives in the gateway rather than application code, so teams can adopt newly available models without rebuilding each provider path.

### [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#vercel-sandbox-isolates-worker-and-evaluator-execution) Vercel Sandbox isolates worker and evaluator execution

Orchestrator-worker and evaluator-optimizer patterns run generated or untrusted code in coding-agent workloads. Coding agents need that isolation before they are safe to point at a real repository. Each Vercel Sandbox is a Firecracker microVM with its own filesystem and network, and `Sandbox.fork()` creates isolated branches from a shared snapshot. Each agent can also run as its own Linux user with a private home directory, while groups allow selected files to be shared between agents. When traces span orchestrators and workers, session correlation links them into a single connected view.

## [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#match-your-orchestration-pattern-to-your-workload,-then-ship) Match your orchestration pattern to your workload, then ship

Choosing a pattern whose token cost or operational complexity exceeds the task's value creates the main risk. Escalate for a concrete capability gap, such as a task that no longer fits one context window. Vercel supports all six patterns on a single infrastructure stack:

- **Durable orchestration:** Vercel Workflows checkpoints every step so no pattern restarts from zero on failure.

- **Active-CPU billing:** Fluid compute excludes model-call I/O wait from active-CPU metering, which makes fan-out patterns more practical while other metered resources still apply.

- **Unified model routing:** AI Gateway handles automatic failover across the same routing layer, removing per-provider integration from application code.

- **Isolated code execution:** Vercel Sandbox runs worker and evaluator code in a Firecracker microVMs with bounded execution windows.

- **End-to-end observability:** [OpenTelemetry](https://ai-sdk.dev/docs/ai-sdk-core/telemetry) session correlation links traces across orchestrator and worker agents in one view.


Deploy a [new project](https://vercel.com/new) to start with a single-agent loop, or begin from [Vercel templates](https://vercel.com/templates) and escalate patterns only when the workload demands it. Keep the first version as small as the task allows, then add coordination when the workload proves the need.

## [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#frequently-asked-questions-about-agent-orchestration) Frequently asked questions about agent orchestration

### [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#what-is-the-difference-between-orchestrator-worker-and-hierarchical-multi-agent-patterns) What is the difference between orchestrator-worker and hierarchical multi-agent patterns?

A supervisor routes among a predefined roster of specialists and controls the communication flow. An orchestrator derives the subtasks themselves at runtime and delegates them to worker agents.

### [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#when-should-i-use-a-single-agent-loop-instead-of-multi-agent-orchestration) When should I use a single-agent loop instead of multi-agent orchestration?

Use a single-agent loop when the task fits one context window, when subtasks cannot be split to run in parallel, and when latency or token budgets are tight. Escalate only when a concrete capability gap makes multi-agent orchestration necessary.

### [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#how-does-token-cost-scale-across-agent-orchestration-patterns) How does token cost scale across agent orchestration patterns?

Token cost scales as you add model calls, workers, critique cycles, and separate context windows. Use the relative multipliers in the table as a planning range rather than treating any pattern as a fixed price.

### [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#what-makes-a-workflow-durable-in-an-agent-orchestration-context) What makes a workflow durable in an agent orchestration context?

Durable execution checkpoints state after each step, so a failure mid-chain resumes from the last successful step. Vercel Workflows implements durability with the `use workflow` directive, so a run can pause for a webhook or a human approval without holding compute and resume from the last checkpoint.

## More Build with AI articles

- [**How to choose an embedding model for production retrieval** \\
Embedding models set retrieval quality and lock your schema. Learn six selection criteria, four eval practices, and how to keep model swaps cheap.](https://vercel.com/i/embedding-model-selection-guide)
- [**5 AI agent guardrails that hold in production** \\
Learn five runtime guardrail patterns for AI agents: input validation, tool scoping, approval gates, loop limits, and output checks on Vercel.](https://vercel.com/i/five-ai-agent-guardrails-production)

* * *

## Ready to deploy?

[Start deploying](https://vercel.com/new) [Talk to an expert](https://vercel.com/contact/sales)

exec
/bin/bash -lc "cd /root/note-worker/candidates/20260809-180901 && sed -n '60,120p' sources/Six-Agent-Orchestration-Patterns.md" in /root/note-worker
 succeeded in 0ms:

At the model level, [AI Gateway](https://vercel.com/docs/ai-gateway) routes across hundreds of models through a single endpoint. It handles automatic failover and load balancing, with per-provider fallback. Okara runs chief marketing officer (CMO) agents for [120,000+ businesses](https://vercel.com/customers/how-okara-runs-cmo-agents-for-120000-companies-on-vercel) on this layer, and with retry and fallback handling moved into the gateway it now processes 4 billion tokens daily. Skip routing when every input needs identical handling or classification accuracy can't be validated.

## [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#4.-run-parallel-agent-orchestration-for-independent-subtasks) 4\. Run parallel agent orchestration for independent subtasks

Parallelization runs independent subtasks simultaneously and aggregates their outputs programmatically. It uses predefined subtasks, while orchestrator-worker determines them at runtime. The pattern fits when subtasks can run at the same time for speed, or when multiple perspectives on one task raise confidence in the result. The aggregation step should be defined before fan-out starts, because inconsistent worker outputs can erase the latency benefit at merge time.

AI SDK represents a [subagent](https://ai-sdk.dev/docs/agents/subagents) as an agent invoked through a parent agent's tool. Each subagent receives its own context window and returns a focused result to the parent, which keeps context-heavy or parallel work out of the main agent's history. Subagents add latency and coordination cost, so use them only when context isolation or parallel execution provides a measurable benefit.

In wide fan-out, billing matters as much as code, since each concurrent invocation spends most of its life waiting on a model call. FLORA's creative agent fans out across more than 50 image models from one session. [Fluid compute](https://vercel.com/docs/fluid-compute) prices on active central processing unit (CPU), so waiting on a model call does not add to that meter. Skip parallelization when subtasks must build on one another in sequence or need one shared context.

## [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#5.-choose-orchestrator-worker-agent-orchestration-for-dynamic-decomposition) 5\. Choose orchestrator-worker agent orchestration for dynamic decomposition

In orchestrator-worker, a central LLM determines at runtime which subtasks a request needs, assigns them to worker agents, and synthesizes the results. With the AI SDK, each worker can be implemented as a subagent exposed to a parent `ToolLoopAgent` through a tool. The worker runs with an isolated context and returns a summarized result for synthesis. The fit is a complex task where the subtasks can't be predicted, like coding, where the number of files to change depends on the request. It is over-engineered for anything else. Each worker holds its own context window, which means coordination adds cost as well as capability.

General Intelligence's Cofounder gives founders a full team of agents covering engineering, marketing, search engine optimization (SEO), finance, sales, customer support, and operations, a shape consistent with orchestrator-worker. Its engineers ship [10 pull requests](https://vercel.com/customers/how-general-intelligence-used-agents-to-build-an-agent-platform-on-vercel) (PRs) and 70+ commits per engineer per day across 4,000+ preview branches, and 90% of site reliability engineering (SRE) work is automated. Worker code runs isolated in [Vercel Sandbox](https://vercel.com/docs/sandbox) microVMs with a separate filesystem and network. Skip the pattern when subtasks are predictable, or coordination overhead outweighs the value of dynamic decomposition.

## [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#6.-apply-evaluator-optimizer-agent-orchestration-when-quality-can-be-measured) 6\. Apply evaluator-optimizer agent orchestration when quality can be measured

Evaluator-optimizer pairs two LLM calls in a loop. One generates a response, the other evaluates it and provides feedback, and the cycle continues until a quality threshold or step ceiling is reached. The pattern needs a clear evaluation rubric and measurable gains from iterative refinement, so it earns its cost only when responses improve under critique.

Two signs make the fit stronger: responses improve when a human can articulate useful feedback, and the LLM can provide useful feedback itself. The runaway critique loop anti-pattern appears when ambiguous criteria keep requesting revisions without a measurable endpoint. Avoid the pattern when first-attempt quality already meets requirements, and enforce a hard revision ceiling in application code. For agent-based implementations, the AI SDK exposes `stopWhen` conditions and AI SDK 7 timeout budgets for bounding total and per-step execution.

[Vercel's Turborepo](https://vercel.com/solutions/turborepo) performance work is the human-in-the-loop version of that critique cycle. AI agents, Vercel Sandboxes, and human review over eight days produced up to a [96% speed improvement](https://vercel.com/blog/making-turborepo-ninety-six-percent-faster-with-agents-sandboxes-and-humans), and the same effort found that unattended state-of-the-art agents without context engineering fall short.

Vercel's Next.js agent evals found `AGENTS.md` outperformed skills on Next.js 16 APIs. Vercel Sandbox caps each isolated run at 45 minutes on Hobby and 24 hours on Pro and Enterprise, which bounds how long a critique loop can execute.

## [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#how-vercel-runs-agent-orchestration-patterns-in-production) How Vercel runs agent orchestration patterns in production

The six patterns are architecture decisions, but four platform behaviors remove failure modes that compound across them. In practice, they address the same runtime concerns across different shapes of work, including state recovery, model selection, fan-out cost, and isolated execution.

### [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#fluid-compute-reduces-active-cpu-cost-in-fan-out-steps) Fluid compute reduces active-CPU cost in fan-out steps

Parallelization and orchestrator-worker fan out into many concurrent invocations dominated by I/O wait. A team has to reject any billing model that charges for that wait, since it makes wide fan-out impractical. Fluid compute meters active CPU separately at a [$0.128/hour base rate](https://vercel.com/docs/functions/usage-and-pricing), with regional rates and other metered resources still applicable.

### [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#vercel-workflows-makes-each-pattern-durable) Vercel Workflows makes each pattern durable

Chaining, orchestrator-worker, and evaluator-optimizer all fail expensively when state disappears mid-run. The `use workflow` directive turns async TypeScript functions into durable workflows with checkpointing and retries. Runs can also pause and resume, so a failed run continues from the last good step. Workflow steps on Pro and Enterprise support execution durations up to 1,800 seconds.

### [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#ai-gateway-centralizes-model-routing-across-patterns) AI Gateway centralizes model routing across patterns

Routing and orchestrator-worker select models by task requirements and provider health, while cost constraints shape the fallback policy. Per-provider integration work slows product work. AI Gateway consolidates that into one unified endpoint with retries and load balancing, plus configurable fallbacks and zero markup on tokens. Provider integration lives in the gateway rather than application code, so teams can adopt newly available models without rebuilding each provider path.

### [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#vercel-sandbox-isolates-worker-and-evaluator-execution) Vercel Sandbox isolates worker and evaluator execution

Orchestrator-worker and evaluator-optimizer patterns run generated or untrusted code in coding-agent workloads. Coding agents need that isolation before they are safe to point at a real repository. Each Vercel Sandbox is a Firecracker microVM with its own filesystem and network, and `Sandbox.fork()` creates isolated branches from a shared snapshot. Each agent can also run as its own Linux user with a private home directory, while groups allow selected files to be shared between agents. When traces span orchestrators and workers, session correlation links them into a single connected view.

## [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#match-your-orchestration-pattern-to-your-workload,-then-ship) Match your orchestration pattern to your workload, then ship

Choosing a pattern whose token cost or operational complexity exceeds the task's value creates the main risk. Escalate for a concrete capability gap, such as a task that no longer fits one context window. Vercel supports all six patterns on a single infrastructure stack:

- **Durable orchestration:** Vercel Workflows checkpoints every step so no pattern restarts from zero on failure.

- **Active-CPU billing:** Fluid compute excludes model-call I/O wait from active-CPU metering, which makes fan-out patterns more practical while other metered resources still apply.

- **Unified model routing:** AI Gateway handles automatic failover across the same routing layer, removing per-provider integration from application code.

- **Isolated code execution:** Vercel Sandbox runs worker and evaluator code in a Firecracker microVMs with bounded execution windows.

- **End-to-end observability:** [OpenTelemetry](https://ai-sdk.dev/docs/ai-sdk-core/telemetry) session correlation links traces across orchestrator and worker agents in one view.


exec
/bin/bash -lc 'cd /root/note-worker/candidates/20260809-180901 && cat works-ready/Six-Agent-Orchestration-Patterns-translation.md' in /root/note-worker
 succeeded in 0ms:
---
created: 2026-08-09
updated: 2026-08-09
title: 六种智能体编排模式
sourceUrl: https://vercel.com/i/agent-orchestration-patterns
sourceAuthor: Vercel（官方平台指南）
translatedAt: 2026-08-09
sources: [references/articles.md 待处理队列]
tags: [AI Agent, 编排, Agent 架构, Vercel, AI SDK, type/翻译]
---

# 六种智能体编排模式

当一个 AI 功能成长到超过单条提示词之后，问题就变成了：如何把大语言模型（LLM）调用连接成一个
在生产负载下依然可靠的系统。合适的编排模式应当匹配任务的**可分解性（task decomposability）、
延迟容忍度、token 预算与人在回路（human-in-the-loop）要求**。先选能解决问题的最简单模式，
只有当工作负载确实需要时才升级。六种模式对应了可靠性、成本与协调之间的这些权衡。

**要点速览（Key takeaways）：**

- 多智能体系统的 token 用量最高可达普通聊天的 15 倍，因此任务价值必须配得上这份额外复杂度。
- 在相同计算预算下，单智能体循环在多跳推理任务上的准确率不输、甚至超过多智能体
  （Qwen3、DeepSeek-R1 与 Gemini 2.5 均验证）。
- 提示词链是从单次 LLM 调用升级的最低风险选项，但链式准确率会一步步复利折损。
- 编排器-工作器是为「子任务数量与性质在编写时未知」设计的模式，因此它是多智能体工作的
  **入口**而非默认选择。
- Vercel Workflows 会对每一步做检查点（checkpoint），并处理失败重试以及因外部事件而暂停，
  因此六种模式都能持久化运行。
- FLORA 的创意智能体把单个会话扇出到 50 多个图像模型，每一步都会持久化并在失败时重试。

## 智能体编排模式一览

在加智能体之前，先从最低复杂度的模式开始。六种模式构成一条复杂度阶梯。**过早扇出（premature fan-out）**
反模式出现在：团队在工作负载还没有独立子任务时就引入智能体，成本和故障面被同时放大。

多智能体系统使用的 token 大约是[聊天交互的 15 倍](https://www.anthropic.com/engineering/multi-agent-research-system)，
所以任务价值必须配得上这些新增的智能体。模式选择取决于工作负载，而不是团队的雄心。

六种模式在适用性、token 成本与失败条件上各不相同。选型前，可把这张表当作规划区间来用：

| 模式 | 最适合 | 相对单次调用的 token 成本 | 何时避免 |
| --- | --- | --- | --- |
| 单智能体循环 | 任务能装进一个带工具访问权限的上下文窗口 | 基线 | 存在可从并行探索中受益的独立子任务 |
| 提示词链 | 编写时已知的固定子任务 | 中等，由链长决定 | 子任务边界未知 |
| 路由 | 不同输入类别分开处理 | 低到中等 | 输入需要完全相同的处理 |
| 并行化 | 预定义的独立子任务 | 高，随扇出规模变化 | 存在顺序依赖或共享上下文 |
| 编排器-工作器 | 子任务直到运行时才可预测 | 高，随工作器数量变化 | 子任务可预测 |
| 评估器-优化器 | 有清晰评分标准且迭代有可衡量收益 | 中等，随评审循环次数变化 | 需要实时响应或没有评分标准 |

这些区间是锚定在实测的智能体与多智能体 token 数据上的相对估计。2026 年 7 月的
AI Gateway 生产指数（Production Index）显示，Anthropic 占[AI Gateway 支出的 61%](https://vercel.com/blog/ai-gateway-production-index-july-2026)、
却只占 token 量的 32%——也就是说，最重要的智能体工作集中了成本。在[智能体工作流模式](https://vercel.com/i/what-are-agentic-workflows)之间做选择，
先于任何基础设施决策。

## 1. 从单智能体循环开始智能体编排

在相同 token 预算下，[单智能体基线](https://arxiv.org/html/2604.02460v1)在多跳推理上的准确率不输、
甚至超过多智能体；那些被报道的多智能体优势，用未计量的计算量来解释，比用架构来解释更合理。

同样的约束也出现在生产中：越简单的架构走得越远，而并行写作仍会遇到协调与上下文共享的约束。
升级应当跟随**能力缺口**——比如上下文窗口压力，或者确实可以并行运行的独立子任务。

单智能体循环就是一个 LLM 反复调用工具、接收结果、把结果加进上下文，直到满足停止条件的循环。
在 AI SDK 7 中，[`ToolLoopAgent`](https://ai-sdk.dev/docs/reference/ai-sdk-core/tool-loop-agent) 运行这个循环，
默认通过 `stopWhen: stepCountIs(20)` 在 20 步后停止。`prepareStep` 回调可以在每一步之间调整模型、工具、
消息与运行时上下文。AI SDK 7 还新增了类型化的 `runtimeContext`、智能体级工具审批，以及总时长、
每步、每块（per-chunk）与每个工具的超时设置。状态管理问题——例如重复出现的账号、反复重跑搜索——
会把团队从这个模式逼走。`WorkflowAgent` 把循环拆成独立的调用，这样已完成的步骤永远不会重跑。

## 2. 固定步骤用提示词链（prompt chaining）

提示词链运行一组固定的 LLM 调用序列，每一步处理上一步的输出。它适合**固定分解**的任务，
通过收窄每一步的范围，用延迟换准确率。准确率会跨步骤复利：单步准确率 95% 时，十步之后
端到端准确率约为 **60%**；单步 90% 时约为 **35%**。

正是这种复利，让步骤之间的**程序化闸门（programmatic gates）不是可选项**。闸门可以校验 schema
合法性、必填字段、策略阈值，或在下一步继承坏掉的中间结果之前插入人工审批。Vercel 内部的数据
智能体 d0 就在生产环境跑持久化的多步编排。

它的模型调用由 AI SDK 处理，而 [Vercel Workflows](https://vercel.com/docs/workflows) 在 Snowflake
超时或模型调用失败时提供重试与状态恢复，并在需要等人或等 webhook 时暂停整个运行。
当子任务边界在编写时未知、或存在可以同时运行的独立子任务时，就不要用提示词链。

## 3. 按输入类型做路由（routing）

路由增加一个初始分类步骤（基于 LLM 或确定性规则），把每个输入分配给专门的下游处理器。
它实现了关注点分离，适合「不同类型最好分开处理」的场景。**路由器准确率是整套系统的天花板**，
因为一次误分类会把错误的工作送给专家处理器。

只要输入空间允许，就优先用确定性分类器（正则、关键词匹配、基于规则的转发）——它彻底移除了
一个模型故障面。路由还需要一个能反映生产输入的验证集，因为纸面上干净的分类体系并不能保证
边界处的分类可靠。

在模型层面，[AI Gateway](https://vercel.com/docs/ai-gateway) 通过单一端点路由数百个模型，
处理自动故障转移与负载均衡，并提供按提供商的回退。Okara 在这一层为[12 万多家企业](https://vercel.com/customers/how-okara-runs-cmo-agents-for-120000-companies-on-vercel)
运行首席营销官（CMO）智能体；把重试与回退搬进网关后，它现在每天处理 **40 亿 token**。
当每个输入都需要完全相同的处理、或分类准确率无法验证时，就不要用路由。

## 4. 独立子任务用并行化（parallelization）

并行化同时运行独立子任务，并用程序化方式聚合它们的输出。它使用**预定义**的子任务，
而编排器-工作器是在运行时确定子任务。适合的场景：子任务可以同时运行以换取速度，
或者同一任务的多个视角能提高结果可信度。**聚合步骤必须在扇出开始前定义好**，
因为不一致的工作器输出会在合并时抹掉延迟收益。

在 AI SDK 中，[子智能体（subagent）](https://ai-sdk.dev/docs/agents/subagents) 是通过父智能体的
工具被调用的智能体。每个子智能体拿到独立的上下文窗口，把聚焦的结果返回给父智能体，
这样上下文密集或并行的活儿就不会塞进主智能体的历史里。子智能体会增加延迟与协调成本，
所以只在上下文隔离或并行执行能带来可衡量收益时使用。

在大规模扇出中，**计费与代码同等重要**——每次并发调用的大部分生命周期都在等模型返回。
FLORA 的创意智能体从一个会话扇出到 50 多个图像模型。[Fluid compute](https://vercel.com/docs/fluid-compute)
按活动 CPU 计费，因此等待模型返回的时间不会计入计费表。当子任务必须按顺序互相依赖、
或需要共享同一上下文时，就不要用并行化。

## 5. 动态分解用编排器-工作器（orchestrator-worker）

在编排器-工作器中，中央 LLM 在运行时决定请求需要哪些子任务，把它们分配给工作器智能体，
再综合结果。在 AI SDK 里，每个工作器可以作为一个子智能体实现，通过工具暴露给父级
`ToolLoopAgent`。工作器在隔离的上下文中运行，返回综合所需的摘要结果。它的适用场景是
**子任务无法预测的复杂任务**——比如编码，要改几个文件取决于请求本身。对其他场景它就是过度设计。
每个工作器都有自己的上下文窗口，意味着协调既带来能力、也带来成本。

General Intelligence 的 Cofounder 给创始人提供了一支覆盖工程、市场、搜索引擎优化（SEO）、财务、
销售、客服与运营的完整智能体团队，形态与编排器-工作器一致。它的工程师每人每天提交
[10 个拉取请求（PR）](https://vercel.com/customers/how-general-intelligence-used-agents-to-build-an-agent-platform-on-vercel)
和 70+ 次提交，横跨 4,000+ 预览分支，90% 的站点可靠性工程（SRE）工作已自动化。
工作器代码隔离运行在 [Vercel Sandbox](https://vercel.com/docs/sandbox) 微虚拟机里，拥有独立的
文件系统与网络。当子任务可预测、或协调开销超过了动态分解的价值时，就不要用这个模式。

## 6. 质量可衡量时用评估器-优化器（evaluator-optimizer）

评估器-优化器把两个 LLM 调用配成一个循环：一个生成回答，另一个评估并给出反馈，
循环一直持续到达到质量阈值或步数上限。这个模式需要清晰的**评估评分标准**（rubric）和
可衡量的迭代改进收益，所以只有当回答真的能在评审下变好时，它的成本才值得。

两个信号会让它更适用：一是人类能说清有用反馈时回答确实变好，二是 LLM 自己也能给出有用反馈。
**失控评审循环（runaway critique loop）**反模式出现在：标准含糊不清，一直要求改稿却没有可衡量的终点。
当首次尝试的质量已经达标时就别用这个模式，并且要在应用代码里强制设置硬性改稿上限。
在基于智能体的实现中，AI SDK 暴露了 `stopWhen` 条件和 AI SDK 7 的超时预算，用来约束总执行时长
与每步执行时长。

[Vercel 的 Turborepo 性能改造](https://vercel.com/solutions/turborepo)是这个评审循环的人机协同版本：
AI 智能体、Vercel Sandbox 与人工评审在八天内带来了最高 [96% 的提速](https://vercel.com/blog/making-turborepo-ninety-six-percent-faster-with-agents-sandboxes-and-humans)，
同一项工作也发现：无人值守的最先进智能体，若不做上下文工程，就会达不到预期。

Vercel 的 Next.js 智能体评测发现，在 Next.js 16 API 上 `AGENTS.md` 优于 skills。
Vercel Sandbox 把每次隔离运行限制在 Hobby 计划的 45 分钟、Pro 与 Enterprise 计划的 24 小时，
这限定了评审循环最长能执行多久。

## Vercel 在生产中如何运行这些编排模式

六种模式是架构决策，但有四种平台行为能消除跨模式累积的故障模式。在实践中，它们针对的是
不同形态工作里的同一批运行时问题：状态恢复、模型选择、扇出成本与隔离执行。

### Fluid compute 降低扇出步骤的活动 CPU 成本

并行化与编排器-工作器会扇出大量以 I/O 等待为主的并发调用。团队必须拒绝任何按这种等待计费的
计费模型，否则大规模扇出就不可行。Fluid compute 单独计量活动 CPU，[基础费率 $0.128/小时](https://vercel.com/docs/functions/usage-and-pricing)，
区域费率与其他计量资源仍然适用。

### Vercel Workflows 让每种模式都持久化

链式、编排器-工作器与评估器-优化器在状态中途消失时都会失败得很昂贵。`use workflow` 指令把
异步 TypeScript 函数变成带检查点与重试的持久化工作流。运行还可以暂停与恢复，失败的运行会从
最后一个好步骤继续。Pro 与 Enterprise 计划的工作流步骤最长支持 1,800 秒的执行时长。

### AI Gateway 跨模式集中模型路由

路由与编排器-工作器会按任务要求与提供商健康状况选模型，而成本约束塑造回退策略。
逐个提供商的集成工作会拖慢产品开发。AI Gateway 把这些整合进一个统一端点，带重试与负载均衡，
外加可配置的回退与 token 零加价。提供商集成住在网关里而不是应用代码里，
因此团队可以接入新发布的模型，而无需重建每一条提供商路径。

### Vercel Sandbox 隔离工作器与评估器执行

编排器-工作器与评估器-优化器会在编码智能体工作负载中运行生成或不可信的代码。
编码智能体需要这种隔离，才能放心地指向真实仓库。每个 Vercel Sandbox 都是一个带独立文件系统
与网络的 Firecracker 微虚拟机，`Sandbox.fork()` 可以从共享快照创建隔离分支。
每个智能体还可以作为独立的 Linux 用户运行，拥有私有 home 目录；分组（groups）则允许在智能体之间
共享选定的文件。当追踪跨越编排器与工作器时，会话关联（session correlation）会把它们链接成
一个连通视图。

## 让编排模式匹配你的工作负载，然后交付

主要风险在于选了一个 token 成本或运维复杂度超过任务价值的模式。要为一个具体的能力缺口而升级，
比如任务不再装得进一个上下文窗口。Vercel 在单一基础设施栈上支持全部六种模式：

- **持久化编排：** Vercel Workflows 对每一步做检查点，任何模式失败时都不会从零重启。
- **活动 CPU 计费：** Fluid compute 把模型调用的 I/O 等待排除在活动 CPU 计量之外，
  让扇出模式更实际可用，其他计量资源仍然适用。
- **统一模型路由：** AI Gateway 在同一个路由层处理自动故障转移，把按提供商的集成从应用代码中移除。
- **隔离代码执行：** Vercel Sandbox 在带执行时限的 Firecracker 微虚拟机中运行工作器与评估器代码。
- **端到端可观测性：** [OpenTelemetry](https://ai-sdk.dev/docs/ai-sdk-core/telemetry) 会话关联把
  编排器与工作器智能体的追踪链接到一个视图里。

部署一个[新项目](https://vercel.com/new)从单智能体循环开始，或从 [Vercel 模板](https://vercel.com/templates)起步，
只在工作负载要求时才升级模式。让第一个版本尽量小，等工作负载证明需要时再引入协调。

## 关于智能体编排的常见问题

### 编排器-工作器与分层多智能体模式有什么区别？

监督者（supervisor）在预定义的专业名单之间路由，并控制通信流；编排器（orchestrator）则在运行时
推导出子任务本身，并委派给工作器智能体。

### 什么时候该用单智能体循环，而不是多智能体编排？

当任务能装进一个上下文窗口、子任务无法拆分并行、且延迟或 token 预算紧张时，用单智能体循环。
只有出现具体的能力缺口、让多智能体编排变得必要时，才升级。

### token 成本在各类编排模式之间如何缩放？

token 成本随模型调用、工作器、评审循环与独立上下文窗口的增加而上升。把表中的相对倍数当作
规划区间来用，不要把任何模式当成固定价格。

### 在智能体编排语境下，什么让工作流「持久化」？

持久化执行会在每一步之后对状态做检查点，因此链中段失败可以从最后一个成功的步骤恢复。
Vercel Workflows 用 `use workflow` 指令实现持久化，运行可以为了 webhook 或人工审批而暂停，
不占用计算资源，然后从最后一个检查点恢复。

exec
/bin/bash -lc "cd /root/note-worker/candidates/20260809-180901 && sed -n '1,120p' sources/Making-production-ready-agents-the-defau.md" in /root/note-worker
 succeeded in 0ms:
August 4, 2026

[Guadalupe Aliseda-Canton](https://blog.duolingo.com/author/guadalupe/)

# Making production-ready agents the default: building Duolingo’s agent platform

See how we made AI agents easy to build, run, and improve in production.

August 4, 2026

[Guadalupe Aliseda-Canton](https://blog.duolingo.com/author/guadalupe/)

![Lin on a motorcycle and Vikram on foot, traversing two Duolingo paths on cell phones.](https://storage.ghost.io/c/7a/33/7a33d0f4-927d-4fe8-a6bf-96131b5e76d4/content/images/2026/08/cover_Production-ready-agent-AI.png)

## TL;DR

At Duolingo, teams were repeatedly rebuilding the same infrastructure around AI agents. We solved this by creating a shared platform where developers define an agent once, while the platform handles execution, observability, orchestration, and evaluation. As a result, teams can build, reuse, and improve agents more easily and quickly at scale.

* * *

## Every team was rebuilding the same infrastructure

AI agents are easy to build and prototype locally. You write a prompt, give the model access to the tools and files it needs, run it, and then iterate with the prompt until you are happy with the output.

The hard part starts after that.

Once you want to run it in the cloud, the work shifts from prompting to productionizing. Every useful agent needs a surprising amount of surrounding infrastructure: setting up MCP servers, preparing credentials, cloning repositories, and loading project context.

At Duolingo, this was becoming a real pain point because we were recreating all of this infrastructure across every project that needed agents. The infrastructure one team built for one system couldn’t easily be reused by another team working on a different system or platform, so teams kept rebuilding the same foundation from scratch.

There was also a distribution problem. Once an agent had been made, we often wanted it to be available in different places. This requires the agent to be invokable across many surfaces like Slack, internal sites, a CLI, or another Temporal workflow. Without a shared execution layer, you would need to rebuild agents across those systems.

Lastly, we wanted to provide all agents with the orchestration, evaluation, and observability they need to truly be production-ready.

## Defining an agent

To address these pain points, we built a system that allows developers to easily spin up agents by simply defining what the agent should do (the system prompt), what tools it should have (which MCPs should be enabled), and what it should have access to (which repos should be cloned to its workspace). Everything else is abstracted away.

Agents are defined in a registry, making them reusable from different entry points. A simplified definition looks like this:

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

This gives us a consistent way to describe what an agent is, who owns it, which provider it uses, what tools it needs, and what the output structure should be.

We then have a Temporal workflow called `AgentWorkflow` that handles the rest.

The goal of `AgentWorkflow` is not to be the agent itself; instead, it serves as a wrapper that abstracts away the shared infrastructure and setup requirements.

At a high level, it does four things:

1. Loads an agent’s definition
2. Prepares the execution environment
3. Runs the agent using an LLM provider SDK
4. Returns the output of the agent

Once an agent is defined in the registry, triggering it is simple from the caller’s perspective. They only need to trigger the workflow with the agent name and user prompt as inputs.

```python
AgentWorkflow(
    agent_name="incident_summary",
    prompt="Summarize the investigation findings for this incident.",
)
```

## Why Temporal?

Temporal is a durable workflow engine. It persists state, retries safely, and coordinates long-running work across systems.

That maps really well to agents because they can:

- Take several minutes to run
- Call external tools
- Wait for human input
- Fail in ways that need retry or debugging

Instead of treating an agent run as a one-off process, we can treat it as a workflow. The workflow owns the durable state and orchestration. Activities handle side effects—like preparing a workspace, cloning a repo, or saving results—while queries expose status while the workflow is running.

We had also already built enough infrastructure around Temporal that we could trigger workflows from any entry point; since agents are run in a workflow, we already supported running agents from anywhere. You can hear more on that from Staff Software Engineer Zhihao Wang [here](https://temporal.io/resources/case-studies/duolingo-temporal-nexus?ref=blog.duolingo.com) if you’re curious.

## Decoupling definition from execution

Before building this platform, the prompt, the model, the SDK, the tooling, and the execution environment were all tightly coupled.

AgentWorkflow changed that. We can create an agent by defining what it does, what tools it needs, and what it returns. The workflow manages everything about how that agent runs.

This distinction is crucial for building an agent platform that can scale. Once execution becomes independent from behavior, we can evolve runtimes, models, tooling, and evaluation independently without changing the interface consumers use.

That separation is what made the next iteration of the platform possible: support for the OpenAI Agents SDK.

### A new runtime

AgentWorkflow already supported a few runtimes, including the Claude Agents SDK and Codex CLI. Adding support for another runtime did not require changing how agents were defined or invoked; it simply became another implementation behind the same workflow abstraction.

Adding this new runtime was very impactful. The OpenAI Agents SDK significantly improved the operational characteristics of the platform, specifically in two ways:

1. With Temporal’s plugin, MCP tool calls become Temporal activities. This makes the system more durable because tool failures can use the same retry policies, state management, and failure handling as any other workflow activity. It also makes the system more observable because every tool call—including inputs, outputs, failures, and retries—is visible in the Temporal UI.
2. The OpenAI Agents SDK also supports routing requests through a proxy. This allowed us to use our internal LLM Gateway, which provides cost tracking, usage tracking, and provider abstraction. Rather than supporting separate SDK integrations for each model provider, we can route requests through the gateway and switch providers behind a consistent interface.

## Evaluating agents

Once agents are reusable, the next challenge is knowing whether they are getting better or worse.

This is especially important for agents that change code. It is not enough to ask whether the agent’s output sounds reasonable; we need to know whether it made the right change.

That’s why we built agent eval infrastructure.

Agent evals run the real agent against authored scenarios. They capture the agent’s output, change files, and git diff before grading the result.

A simplified eval case looks like this:


exec
/bin/bash -lc "cd /root/note-worker/candidates/20260809-180901 && sed -n '120,252p' sources/Making-production-ready-agents-the-defau.md" in /root/note-worker
 succeeded in 0ms:

```python
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

This lets us test both the agent’s output and what it actually changes.

### How grading works

We use several types of graders.

`structured_output` checks fields in the agent’s structured response.

`diff_assertions` checks the actual repo diff. It can require specific changes, catch risky changes, limit the number of changed files, or restrict edits to certain paths.

`no_op_consistency` checks that the reported outcome matches the repo state. If the output indicates that no change was needed but files changed, the eval fails. If the output indicates that a fix was made but the diff is empty, the eval also fails.

For cases where exact diff assertions are too brittle, we also support an optional LLM-as-judge. However, deterministic graders are the foundation. The LLM-as-judge is useful, but we do not want our only signal to be one model judging another model’s work.

For agent evals to be useful, they need to inspect artifacts, not just prose.

### Running evals as workflows

The eval system itself also runs on Temporal.

The suite workflow loads eval cases, starts a child workflow for each case and repetition, aggregates results, renders a report, and optionally saves the run for a dashboard.

This gives evals the same durability properties as production agent runs. A long-running eval case can keep running. A failed case is captured explicitly. Repetitions can run in parallel. Results can be persisted and reviewed later.

This also makes evals feel less like a local script and more like part of the platform.

## From weeks to minutes

Before this platform, creating a production-ready agent was a complex multi-step project. Teams had to choose an SDK, learn its nuances, set up repository cloning, configure MCP servers, and wire up credentials. Depending on the use case, this setup could take several weeks.

Now, creating an agent takes about 10 minutes. A developer can use an internal site to select MCPs, choose a model, and define a system prompt to immediately create an agent. From there, they can invoke it from anywhere without worrying about underlying details.

That speedup is only part of the impact. Every agent created through the platform automatically gets durability, observability, orchestration, evaluation, and multi-entry-point invocation. Agents are also more useful because they can be used outside of the systems that created them. Once defined, they can be used by other teams, other workflows, and eventually other agents.

Agents currently power workflows that fix CI failures, address code review comments, and support internal tools like our Slack bot for release managers. This bot uses specialized agents composed together to investigate crashes, identify relevant changes, and summarize findings.

## What’s next?

So far, this infrastructure provides a foundation for running and evaluating reusable agents.

The main things we are focusing on now are:

- Automating eval creation from engineer feedback on agent results to enable a continuous, low-effort improvement loop.
- Enabling agent orchestration. Because agents run as workflows, they can also be exposed as tools for other agents. This opens the door to larger autonomous systems where agents can trigger one another while Temporal manages durability for the entire system.

## Conclusion

Good abstractions have always been how developers move fast. When a complex problem is solved once and wrapped in a clean interface, everyone who follows inherits that work and writes better code without additional overhead.

This idea is more important now than ever. AI generates code rapidly, but not necessarily high-quality code. It is trivial to have tools like Claude Code or Codex build an agent, but those tools do not automatically consider durability, observability, or evaluation. Left alone, every new agent becomes its own infrastructure problem. The more code we generate, the more valuable an abstraction that guarantees quality becomes.

The platform we built is that abstraction. It does more than speed up creation; it changes the nature of the agents created. By moving infrastructure concerns into the platform, every new agent inherits them automatically, allowing developers to focus on behavior rather than durability or observability.

Moving fast is usually framed as a tradeoff against building production-ready systems. This platform collapses that tradeoff: the same tools that allow developers and AI to move quickly also ensure what they build is ready for production.

If working on practical, production-grade AI systems that make a real impact across the company interests you, we’re hiring!

[SEE OUR OPEN ROLES HERE](https://careers.duolingo.com/?department=Engineering&utm_source=blog.duolingo.com&utm_medium=blog&utm_campaign=prodready_blog_080426#careers)

TAGS

[Life at Duolingo](https://blog.duolingo.com/tag/life-at-duolingo)

[Engineering](https://blog.duolingo.com/tag/engineering)

SHARE ARTICLE

[LinkedIn](https://www.linkedin.com/shareArticle?url=https://blog.duolingo.com/production-ready-ai-agent-platform/&title=Making%20production-ready%20agents%20the%20default%3A%20building%20Duolingo%E2%80%99s%20agent%20platform&summary=See%20how%20we%20made%20AI%20agents%20easy%20to%20build%2C%20run%2C%20and%20improve%20in%20production.&source=%5Bobject%20Object%5D "LinkedIn")[Facebook](https://www.facebook.com/sharer/sharer.php?u=https://blog.duolingo.com/production-ready-ai-agent-platform/ "Facebook")[Twitter](https://twitter.com/intent/tweet?url=https://blog.duolingo.com/production-ready-ai-agent-platform/&text=Making%20production-ready%20agents%20the%20default%3A%20building%20Duolingo%E2%80%99s%20agent%20platform&media=https%3A%2F%2Fstorage.ghost.io%2Fc%2F7a%2F33%2F7a33d0f4-927d-4fe8-a6bf-96131b5e76d4%2Fcontent%2Fimages%2F2026%2F08%2Fcover_Production-ready-agent-AI.png "Twitter")[Share on KakaoTalk](https://story.kakao.com/share?url=https://blog.duolingo.com/production-ready-ai-agent-platform/&title=Making%20production-ready%20agents%20the%20default%3A%20building%20Duolingo%E2%80%99s%20agent%20platform&media=https%3A%2F%2Fstorage.ghost.io%2Fc%2F7a%2F33%2F7a33d0f4-927d-4fe8-a6bf-96131b5e76d4%2Fcontent%2Fimages%2F2026%2F08%2Fcover_Production-ready-agent-AI.png "Share on KakaoTalk")[WhatsApp](whatsapp://send?text=Making%20production-ready%20agents%20the%20default%3A%20building%20Duolingo%E2%80%99s%20agent%20platform%20https://blog.duolingo.com/production-ready-ai-agent-platform/ "WhatsApp")[Email](mailto:?subject=Check%20out%20this%20post%20from%20Duolingo&body=Hi!%20I%20thought%20you%20might%20enjoy%20this%20post:%20Making%20production-ready%20agents%20the%20default:%20building%20Duolingo%E2%80%99s%20agent%20platform%0D%0A%0D%0Ahttps://blog.duolingo.com/production-ready-ai-agent-platform/ "Email")

### RELATED ARTICLES

[![](https://blog.duolingo.com/production-ready-ai-agent-platform/)](about:blank#)

[![](https://storage.ghost.io/c/7a/33/7a33d0f4-927d-4fe8-a6bf-96131b5e76d4/content/images/2026/06/cover_AI-iOS-unit-test-generation-pipeline.png)](https://blog.duolingo.com/ai-ios-unit-test-generation-pipeline/)

Jun 24[Kush Agrawal](https://blog.duolingo.com/author/kush/)

[**How we built an automated unit test generation pipeline for iOS**](https://blog.duolingo.com/ai-ios-unit-test-generation-pipeline/)

[![](https://storage.ghost.io/c/7a/33/7a33d0f4-927d-4fe8-a6bf-96131b5e76d4/content/images/2026/06/cover_How-a-simple-code-change-reduced-CPU-usage-by-97_.png)](https://blog.duolingo.com/reduce-cpu-usage-97-percent/)

Jun 22[Fabien Loudet](https://blog.duolingo.com/author/fabien/)

[**How a simple code change reduced CPU usage by 97%**](https://blog.duolingo.com/reduce-cpu-usage-97-percent/)

[![](https://storage.ghost.io/c/7a/33/7a33d0f4-927d-4fe8-a6bf-96131b5e76d4/content/images/2026/05/cover_How-I-Used-Duolingo-to-Find-My-Family-in-Poland.png)](https://blog.duolingo.com/learning-polish-family-reunion/)

Jun 1[David Sawicki](https://blog.duolingo.com/author/david-sawicki/)

[**How I used Duolingo to find my family in Poland**](https://blog.duolingo.com/learning-polish-family-reunion/)

### RELATED ARTICLES

[![](https://blog.duolingo.com/production-ready-ai-agent-platform/)](about:blank#)

[![](https://storage.ghost.io/c/7a/33/7a33d0f4-927d-4fe8-a6bf-96131b5e76d4/content/images/2026/06/cover_AI-iOS-unit-test-generation-pipeline.png)](https://blog.duolingo.com/ai-ios-unit-test-generation-pipeline/)

Jun 24[Kush Agrawal](https://blog.duolingo.com/author/kush/)

[**How we built an automated unit test generation pipeline for iOS**](https://blog.duolingo.com/ai-ios-unit-test-generation-pipeline/)

[![](https://storage.ghost.io/c/7a/33/7a33d0f4-927d-4fe8-a6bf-96131b5e76d4/content/images/2026/06/cover_How-a-simple-code-change-reduced-CPU-usage-by-97_.png)](https://blog.duolingo.com/reduce-cpu-usage-97-percent/)

Jun 22[Fabien Loudet](https://blog.duolingo.com/author/fabien/)

[**How a simple code change reduced CPU usage by 97%**](https://blog.duolingo.com/reduce-cpu-usage-97-percent/)

[![](https://storage.ghost.io/c/7a/33/7a33d0f4-927d-4fe8-a6bf-96131b5e76d4/content/images/2026/05/cover_How-I-Used-Duolingo-to-Find-My-Family-in-Poland.png)](https://blog.duolingo.com/learning-polish-family-reunion/)

Jun 1[David Sawicki](https://blog.duolingo.com/author/david-sawicki/)


exec
/bin/bash -lc 'cd /root/note-worker/candidates/20260809-180901 && cat works-ready/Making-production-ready-agents-the-defau-translation.md' in /root/note-worker
 succeeded in 0ms:
---
created: 2026-08-09
updated: 2026-08-09
title: 让生产就绪的智能体成为默认：构建 Duolingo 的智能体平台
sourceUrl: https://blog.duolingo.com/production-ready-ai-agent-platform/
sourceAuthor: Guadalupe Aliseda-Canton（Duolingo 工程博客）
translatedAt: 2026-08-09
sources: [references/articles.md 待处理队列]
tags: [AI Agent, 智能体平台, 生产就绪, Temporal, MCP, 评测, type/翻译]
---

# 让生产就绪的智能体成为默认：构建 Duolingo 的智能体平台

看看我们如何让 AI 智能体在生产环境中易于构建、运行与改进。

2026 年 8 月 4 日，[Guadalupe Aliseda-Canton](https://blog.duolingo.com/author/guadalupe/)

## TL;DR

在 Duolingo，各团队一直在反复重建围绕 AI 智能体的同一套基础设施。我们的解决办法是创建一个共享平台：开发者只需定义一次智能体，平台负责执行、可观测性、编排与评测。结果是，团队可以更快、更轻松地在规模上构建、复用与改进智能体。

## 每个团队都在重建同一套基础设施

AI 智能体在本地很容易构建和做原型验证。你写一段提示词，给模型它需要的工具和文件权限，运行，然后反复调整提示词，直到对输出满意为止。

难的部分从这之后才开始。

一旦你想让它跑到云端，工作重心就从提示词转向「生产化」（productionizing）。每个真正有用的智能体都需要数量惊人的周边基础设施：配置 MCP 服务器、准备凭据、克隆仓库、加载项目上下文。

在 Duolingo，这正成为一个实实在在的痛点，因为我们正在每个需要智能体的项目里重建所有这些基础设施。一个团队为某个系统搭建的基础设施，很难被另一个团队在别的系统或平台上复用，于是各团队只能一遍遍从零重建相同的地基。

此外还有分发（distribution）问题。一个智能体做好之后，我们常常希望它在不同地方都可用。这要求智能体能在多种入口被调用，比如 Slack、内部站点、CLI 或另一个 Temporal 工作流。没有共享的执行层，你就得在这些系统里把智能体重建一遍。

最后，我们还想让所有智能体都具备真正「生产就绪」所需的编排、评测与可观测性。

## 定义智能体

为了解决这些痛点，我们构建了一个系统：开发者只需简单定义智能体「应该做什么」（系统提示词）、「应该有哪些工具」（启用哪些 MCP）、「应该能访问什么」（把哪些仓库克隆进它的工作区），其余一切都由系统抽象掉。

智能体定义在注册表（registry）里，可以从不同入口复用。一个简化版定义长这样：

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

这给了我们一种一致的方式来描述：智能体是什么、归谁所有、用哪个模型提供商、需要哪些工具、输出结构应该是什么样。

然后我们有一个名为 `AgentWorkflow` 的 Temporal 工作流负责其余部分。

`AgentWorkflow` 的目标不是成为智能体本身，而是充当一个包装器（wrapper），把共享基础设施与配置需求抽象掉。

从宏观上看，它做四件事：

1. 加载智能体的定义
2. 准备执行环境
3. 用 LLM 提供商 SDK 运行智能体
4. 返回智能体的输出

一旦智能体定义在注册表中，从调用方的角度看，触发非常简单。他们只需把智能体名称和用户提示词作为输入触发工作流。

```python
AgentWorkflow(
    agent_name="incident_summary",
    prompt="Summarize the investigation findings for this incident.",
)
```

## 为什么选 Temporal？

Temporal 是一个持久化工作流引擎（durable workflow engine）。它持久化状态、安全地重试，并跨系统协调长期运行的工作。

这与智能体的特性非常契合，因为智能体可能：

- 运行需要好几分钟
- 调用外部工具
- 等待人工输入
- 以需要重试或调试的方式失败

与其把一次智能体运行当成一次性进程，我们可以把它当作一个工作流。工作流持有持久化状态并负责编排。Activity 处理副作用——比如准备工作区、克隆仓库或保存结果——而 Query 在工作流运行期间暴露状态。

我们也已经围绕 Temporal 建好了足够多的基础设施，可以从任何入口触发工作流；既然智能体是在工作流里运行的，我们也就天然支持从任何地方运行智能体。如果你好奇，可以听听 Staff Software Engineer Zhihao Wang 在[这里](https://temporal.io/resources/case-studies/duolingo-temporal-nexus?ref=blog.duolingo.com)的分享。

## 把定义与执行解耦

在构建这个平台之前，提示词、模型、SDK、工具链与执行环境都是紧耦合的。

AgentWorkflow 改变了这一点。我们可以通过定义智能体「做什么、需要什么工具、返回什么」来创建它，而工作流管理关于它如何运行的一切。

这种区分对构建一个能够规模化（scale）的智能体平台至关重要。一旦执行与行为相互独立，我们就可以独立演进运行时、模型、工具链与评测，而无需改变消费者使用的接口。

正是这种分离让平台的下一轮迭代成为可能：对 OpenAI Agents SDK 的支持。

### 新的运行时

AgentWorkflow 已经支持若干运行时，包括 Claude Agents SDK 与 Codex CLI。增加对另一个运行时的支持，并不需要改变智能体的定义或调用方式；它只是成为同一个工作流抽象背后的又一个实现。

加入这个新运行时影响很大。OpenAI Agents SDK 显著改善了平台的操作特性，具体体现在两个方面：

1. 借助 Temporal 插件，MCP 工具调用变成了 Temporal activity。这让系统更持久化（durable），因为工具失败可以复用与其他任何工作流 activity 相同的重试策略、状态管理与失败处理。它也让系统更可观测，因为每一次工具调用——包括输入、输出、失败与重试——都在 Temporal UI 中可见。
2. OpenAI Agents SDK 还支持通过代理（proxy）路由请求。这让我们能够使用内部 LLM 网关（LLM Gateway），提供成本追踪、用量追踪与提供商抽象。与其为每个模型提供商分别维护 SDK 集成，我们可以把请求路由到网关，在一个一致接口后面切换提供商。

## 评测智能体

智能体变得可复用之后，下一个挑战是知道它们是在变好还是变差。

这对会改动代码的智能体尤其重要。光问「智能体的输出听起来是否合理」是不够的；我们需要知道它是否做了正确的改动。

为此我们构建了智能体评测（agent eval）基础设施。

智能体评测让真实的智能体跑编写好的场景（authored scenarios）。在评分之前，它们会捕获智能体的输出、改动的文件与 git diff。

一个简化版的评测用例长这样：

```python
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

这让我们既能测试智能体的输出，也能测试它实际改了什么。

### 评分如何工作

我们使用好几种评分器（grader）。

`structured_output` 检查智能体结构化响应中的字段。

`diff_assertions` 检查实际的仓库 diff。它可以要求特定改动、捕捉有风险的改动、限制改动文件的数量，或把编辑限制在特定路径内。

`no_op_consistency` 检查报告的结果是否与仓库状态一致。如果输出表明无需改动、但文件却变了，评测失败；如果输出表明做了修复、但 diff 是空的，评测同样失败。

对于精确 diff 断言过于脆弱（brittle）的用例，我们还支持可选的 LLM 作为裁判（LLM-as-judge）。不过，确定性评分器才是地基。LLM 作为裁判有用，但我们不希望唯一信号是一个模型评判另一个模型的成果。

要让智能体评测真正有用，它们必须检查产物（artifacts），而不仅仅是文字。

### 把评测跑成工作流

评测系统本身也跑在 Temporal 上。

套件工作流（suite workflow）加载评测用例，为每个用例与每次重复启动一个子工作流，汇总结果，渲染报告，并可选地把本次运行保存到仪表盘。

这让评测拥有与生产智能体运行相同的持久化特性。长时间运行的评测用例可以继续跑下去。失败的用例会被显式捕获。重复运行可以并行。结果可以持久化并留待后续审查。

这也让评测不再像本地脚本，而更像是平台的一部分。

## 从数周缩短到数分钟

在这个平台之前，创建一个生产就绪的智能体是一个复杂的多步骤项目。团队必须选择 SDK、学习它的各种细节、配置仓库克隆、搭建 MCP 服务器、接通凭据。视用例而定，这套搭建可能要花上好几周。

现在，创建一个智能体大约只需要 10 分钟。开发者可以用内部站点选择 MCP、挑选模型、定义系统提示词，立即创建一个智能体。之后他们就可以从任何地方调用它，而无需操心底层细节。

这种提速只是影响的一部分。通过平台创建的每个智能体，都自动获得持久化、可观测性、编排、评测与多入口调用能力。智能体也更有用，因为它们可以用在创建它们的系统之外。定义之后，其他团队、其他工作流、甚至将来的其他智能体都可以使用它们。

目前，智能体正在支撑这些工作流：修复 CI 失败、处理代码评审意见，以及支持像我们的发布经理 Slack 机器人这样的内部工具。这个机器人把多个专用智能体组合在一起：调查崩溃、定位相关改动并汇总发现。

## 接下来是什么？

到目前为止，这套基础设施为「运行与评测可复用智能体」提供了地基。

我们现在主要聚焦这几件事：

- 根据工程师对智能体结果的反馈，自动化评测用例的创建，实现一个持续、低成本的改进闭环。
- 实现智能体编排（agent orchestration）。由于智能体以工作流形式运行，它们也可以作为工具暴露给其他智能体。这为更大的自主系统打开了大门：智能体之间可以互相触发，而 Temporal 为整个系统管理持久化。

## 结语

好的抽象一直是开发者快速前进的方式。当一个复杂问题被解决一次、并包进一个干净的接口时，所有后来者都继承了这份工作，并在不增加额外开销的情况下写出更好的代码。

这个想法现在比以往任何时候都更重要。AI 生成代码很快，但不一定能生成高质量代码。用 Claude Code 或 Codex 这类工具做一个智能体很容易，但这些工具不会自动考虑持久化、可观测性或评测。如果放任不管，每个新智能体都会变成它自己的基础设施问题。我们生成的代码越多，能保证质量的抽象就越有价值。

我们构建的平台就是那个抽象。它不仅加快了创建速度，还改变了被创建出来的智能体的性质。通过把基础设施问题搬进平台，每个新智能体都自动继承了它们，让开发者专注于行为，而不是持久化或可观测性。

「快速前进」通常被描绘成与「构建生产就绪系统」之间的取舍。这个平台把这种取舍消解了：让开发者和 AI 快速前进的同一套工具，同时也确保他们构建的东西为生产就绪。

如果你对构建能影响全公司的、务实且生产级的 AI 系统感兴趣，我们正在招人！

[查看我们的开放职位](https://careers.duolingo.com/?department=Engineering&utm_source=blog.duolingo.com&utm_medium=blog&utm_campaign=prodready_blog_080426#careers)

codex
四篇原文与译文都已通读。现在对照知识库既有条目，确认契合度与建议去向。
exec
/bin/bash -lc "cd /root/note-worker && ls working/ prompts/ && echo '---' && head -30 expand/06-AI与LLM/Agent工具与平台/ECC.md && echo '===THINKING===' && head -40 expand/thinking/MCP协议标准化的增量与边界.md" in /root/note-worker
 succeeded in 0ms:
prompts/:
AGENTS.md
curate-review.md
curate.md
deep-research-tracker.md
feedback
ingest.md
research-tracker.md
worker.md

working/:
AGENTS.md
---
---
created: 2026-08-04
updated: 2026-08-04
sources: [raw/github-2026-08-03-08c2bad9.md]
tags: [AI, Agent, 编程代理, 工具系统, type/工具, status/待验证, 启发]
---

# ECC

给编程代理装一套"操作系统"：技能、本能、记忆、安全一应俱全，Claude Code / Codex / Cursor 都能插上。

## 检索问题（Q&A）
- 编程代理除了模型还缺什么基础设施？→ 本条目：ECC 的技能 / 本能 / 记忆 / 安全分层
- Agent 工程化参考实现？→ ECC 的 npm 包 + GitHub App 架构

## 结构化提炼

### 核心论点
ECC 把编程代理的工程化需求（技能管理、持久记忆、安全防护、多运行时）沉淀为可插拔的"代理工具操作系统"，跨 Claude Code / Codex / Cursor 等前端使用。

### 逻辑骨架
- 问题：编程代理各自为战，缺少可复用的能力层
- 方案：Agent Harness 分层——技能（skills）、本能（instincts）、记忆（memory）、安全（AgentShield）
- 形态：npm 包（ecc-universal / ecc-agentshield）+ GitHub App + Pro 订阅（私有仓库协作）
- 运行时：Shell / TypeScript / Python / Go / Java / Perl / Markdown

### 关键概念（费曼式）
- Agent Harness：把"代理怎么干活"的公共部分（工具、记忆、权限）抽出来，像操作系统管硬件一样管能力
- 本能（instincts）：预设的行为倾向 / 检查点，让代理不用每次重新想"该不该这么干"

===THINKING===
---
created: 2026-08-09
updated: 2026-08-09
sources: [references/articles.md#14]
tags: [MCP, AI Agent, 协议标准化, type/想法]
---

# MCP 协议标准化的增量与边界

> 论点：官方文档把 MCP 比作「AI 应用的 USB-C」，这个类比在**接口/传输层**成立，在**语义层**不成立——协议标准化把集成成本从「每个模型 × 每个工具的协议适配」转移成了「每个 server 的语义适配与质量治理」，M×N 问题没有消失，只是换了战场。2026-07-28 版本文档的增量（MCP Apps / Agent Skills / Registry / `server/discover`）恰好说明：MCP 正在从「工具调用协议」长成「AI 应用平台层」。

## 一、官方文档说了什么（压缩）

MCP 是连接 AI 应用与外部系统（数据 / 工具 / 工作流）的开放标准，口号是「build once, integrate everywhere」，官方类比是「AI 应用的 USB-C」。

## 二、类比成立到哪一层

### 成立：接口层（传输 + 原语枚举）

- 架构文档把 MCP 拆成两层：**数据层**（JSON-RPC 2.0 消息、`server/discover` 能力发现、tools / resources / prompts 三个原语、通知与进度）与**传输层**（本地 stdio、远程 Streamable HTTP + OAuth）。
- 这两层才是「插头规格」：客户端生态（Claude、ChatGPT、VSCode、Cursor）只需实现一次连接逻辑，就能连上任何符合规范的 server——USB-C 类比真正的成立处是**接口一致 → 即插即用**。

### 不成立：语义层（每个 tool 仍是私有协议）

- USB-C 的语义（供电协商、DP / Thunderbolt 备选模式）由协议完整定义，插上就知道能干什么；MCP 只定义「信封」和三个粗粒度原语，**每个 tool 的输入输出 schema、错误语义、权限边界仍由各家 server 自治**。
- 后果：集成方（或 LLM 本身）依然要为每个 server 读文档、写调用示例、做 prompt 适配，还要防备「工具描述与实现不符」「长尾 server 质量参差」。M×N 从「协议适配」转为「语义适配 + 质量适配」，成本换了个名字，没消失。
- 更关键的不等式：**USB-C 插错设备最多不通电，MCP 接错权限可能泄露数据或触发副作用**。协议不解决信任问题——OAuth 2.1 授权、沙箱、审计仍是 host 的责任，官方只给 best practices 而非强制。

## 三、2026-07-28 版本文档的实质增量（相对知识库既有笔记）

知识库既有 [[MCP协议与工具调用]] 覆盖的是 2024–2025 经典视图（Client-Server、JSON-RPC、三原语）。本次官方文档可提取的新信号：

| 增量 | 含义 | 我的判断 |
|------|------|---------|
| `server/discover` 强制发现 | 版本 / 能力协商前置，请求自带 `_meta` 版本与能力 | 生态规模大到必须治理兼容性，走向「规范即契约」 |
| Sampling 原语废弃 | 服务器向用户采样被移除 | 收缩边界：server 只做「能力提供」，不做「用户交互」 |
| MCP Apps（扩展） | 可在 host 内渲染交互 UI 的应用 | 从「工具调用」扩展到「应用平台」，最值得注意的方向性变化 |
| Agent Skills over MCP | 技能经 MCP 分发的标准化工作组 | 与 Claude Code skills / ECC 技能体系同源，工程化赛道 |
| Registry + SEPs | 服务器注册表 + 规范增强提案流程 | 治理架构成型：谁来收录、怎么演进、如何淘汰 |
| 远程 server 一等公民 | Streamable HTTP + OAuth 2.1 教程 | 从本地 stdio 主场景走向企业远程部署 |

exec
/bin/bash -lc "cd /root/note-worker && cat prompts/curate-review.md | head -80 && echo '===INDEX===' && cat expand/index.md | head -60" in /root/note-worker
 succeeded in 0ms:
---
created: 2026-08-09
updated: 2026-08-09
type: workflow
status: 待验证
product: null
source: curate-research 评审模板
---

# 候选自动评审

> 运行器：服务器 codex，由 curate.py 串行调用。对一批 3-4 篇候选统一打分。

## 任务

你是知识库的内容评审。知识库主题：AI Agent 开发 / 跨平台开发（KMP·Flutter）/ Harness Engineering / 通用技术。

读以下每篇候选的三件套，逐篇回答。候选位于 `candidates/<batch>/`：

{ITEMS}

逐篇回答（每篇独立小节，标题为篇名）：

### 篇名
- **原文价值**：原创洞察密度 / 长文实质 vs 产品页·发布稿·摘要。高/中/低 + 一句话理由
- **翻译质量**：完整逐译 / 压缩摘要 / 首轮粗稿；通顺度、术语到位度。精品/合格/需返工 + 一句话理由
- **与知识库契合度**：补薄弱环节还是重复（对照 references/articles.md 与 expand/ 已有条目）
- **一句话定性 + 建议去向**：working/ 正式收录 / articles.md 观察项一行 / tools/（待实测）/ 淘汰

## 汇总

最后输出一个「候选 × 定性 × 去向」markdown 表格：

| 篇名 | 原文价值 | 翻译质量 | 契合度 | 定性 | 建议去向 |

## 约束

- 基于实际内容，紧凑中文，结构化输出
- 只做评审与建议，不修改任何文件
===INDEX===
---
created: 2026-08-03
updated: 2026-08-09
tags: [知识库, 索引]
---

# 内容总目录

> 知识库分类体系：`01-编程语言` → `02-前端` → `03-后端` → `04-数据库` → `05-数据结构与算法` → `06-AI与LLM` → `07-Linux与工具链` → `08-逆向与安全` → `09-源码解读` → `10-求职面试` → `11-生活杂项`
> 全库共 133 个 Markdown 文件（2026-08-09 更新：index 补入 opencode 项目解读 10 条 wiki 笔记；新增 expand/thinking/ 独立思考层；新增 [[Rust2024版次的语义收紧与异步闭合]]）。关系总览见 [[知识图谱]]。

## 知识库自动化

- [[自动化工作流设计]]：采集→过滤→加工→入库全自动管线设计文档（Agent 架构 / 平台接入 / LLM 质检 / Ingest 对接）
- [[自动化工作流功能与实现方案]]：GitHub Actions + Codex 混合自动化落地——功能需求清单、workflow 配置、实施路线图与运维指标
- [[动态索引]]：Dataview 按 frontmatter 动态生成的条目总览（F10，与 AI 维护的 index.md 互补）
- [[知识库周报]]：每周五自动生成的采集 / 加工 / 健康度周报（F08）

## thinking（独立思考，AI 主导）

> 2026-08 起 expand/ 承担 thinking 作用：文章/素材的独立观点、质疑、延伸统一收这里；存量概念/深度笔记仍在各分类目录。入链自查见 [[expand/thinking/AGENTS]]。

- [[MCP协议标准化的增量与边界]]：MCP 官方文档判值思考——USB-C 类比只到接口层，工具语义适配的 M×N 未消失；2026-07-28 版增量（MCP Apps / Agent Skills / Registry / server/discover）
- [[Rust2024版次的语义收紧与异步闭合]]：Rust 1.85 / 2024 版次判值思考——采集器「Move 语义」标签纠偏，真正主线是版次语义收紧（unsafe 显式化）+ async closures 异步借用补课

## 01-编程语言

- [[c++核心编程]]：C++ 内存分区、引用、函数与面向对象核心语法
- [[C++模板和STL]]：模板与 STL 容器/迭代器/算法库
- [[图结构的应用]]：图的基本结构与 BFS/DFS 搜索算法应用
- [[Dijkstra最短路算法]]：C++ 邻接矩阵 Dijkstra 最短路实现（图算法编程练习）
- [[python]]：Python 学习入口（⚠️ 空笔记，待补充）
- [[数据分析学习笔记]]：NumPy / Pandas / Matplotlib 数据分析实战
- [[01-编程语言/python/集合]]：Python 列表/元组/集合/字典四大数据结构对比

## 02-前端

- [[Day01]]：前端入门第一天——工具链与开发环境
- [[Day02]]：前端入门第二天——HTML 图片与常用标签
- [[Day03]]：前端入门第三天——CSS 与样式
- [[Day04]]：前端入门第四天——Bootstrap 与网格布局
- [[Day05]]：前端入门第五天——JavaScript 基础与练习
- [[Day06]]：前端入门第六天——正则表达式基础
- [[Layui表格和表单]]：Layui UI 框架表格与表单组件
- [[VUE]]：Vue 常用指令与渐进式框架核心概念

## 03-后端

- [[面向对象]]：Java 对象内存分配与 OOP 基础
- [[03-后端/java/集合]]：Java 集合框架（ArrayList 等）
- [[Stream]]：Java Stream 流式 API 与 Lambda
- [[java高级技术]]：Java 进阶特性
- [[javaweb]]：JavaWeb 开发（含 Vue 前端集成）
- [[案例]]：JavaWeb 综合案例
- [[Mybatis-plus]]：MyBatis-Plus 持久层框架
- [[mq]]：RabbitMQ 消息队列（异步调用/选型）
- [[redis]]：Redis 启动配置与常用命令
- [[redis分布式缓存]]：Redis 分布式缓存（⚠️ 空笔记，待补充）
- [[rocketmq]]：RocketMQ 发布-订阅消息模型
- [[judge0 API调用]]：Judge0 部署实战与 cgroup 兼容性排查

exec
/bin/bash -lc "cd /root/note-worker/candidates/20260809-180901 && diff works-ready/The-new-rules-of-context-engineering-for-translation.md translations/The-new-rules-of-context-engineering-for/translation.md && echo 'SAME-new-rules'; diff works-ready/One-shotting-a-Raccoon-Heist-game-using-translation.md translations/One-shotting-a-Raccoon-Heist-game-using/translation.md && echo 'SAME-raccoon'; diff works-ready/Six-Agent-Orchestration-Patterns-translation.md translations/Six-Agent-Orchestration-Patterns/translation.md && echo 'SAME-six'; diff works-ready/Making-production-ready-agents-the-defau-translation.md translations/Making-production-ready-agents-the-defau/translation.md && echo 'SAME-duolingo'" in /root/note-worker
 succeeded in 0ms:
SAME-new-rules
SAME-raccoon
SAME-six
SAME-duolingo

exec
/bin/bash -lc "cd /root/note-worker/candidates/20260809-180901 && head -25 translations/The-new-rules-of-context-engineering-for/01-analysis.md && echo '===DUOLINGO===' && head -25 translations/Making-production-ready-agents-the-defau/01-analysis.md" in /root/note-worker
 succeeded in 0ms:
---
created: 2026-08-09
updated: 2026-08-09
type: analysis
status: 待评审
sources:
  - title: The new rules of context engineering for Claude 5 generation models
    url: https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models
    source: research
    date: 2026-08-09
tags: [Claude, 上下文工程, AI Agent, Harness, 候选评审]
---

# 01 原文分析：The new rules of context engineering for Claude 5 generation models

## 原文信息

- **标题：** The new rules of context engineering for Claude 5 generation models
- **作者：** Thariq Shihipar（Anthropic technical staff）
- **发布：** 2026-07-24，claude.com/blog（分类：Claude Code / Agents）
- **篇幅：** 约 5 分钟阅读（正文约 1,900 英文词，抓取 Markdown 约 15KB）

## 原文价值评估（高 / 中 / 低）

**高。** 不是发布稿或产品页，而是 Anthropic 官方对新一代 Claude 模型（Opus 5 / Fable 5）
===DUOLINGO===
---
created: 2026-08-09
updated: 2026-08-09
type: analysis
status: 待评审
sources:
  - title: Making production-ready agents the default: building Duolingo's agent platform
    url: https://blog.duolingo.com/production-ready-ai-agent-platform/
    source: research
    date: 2026-08-09
tags: [AI Agent, 智能体平台, 生产就绪, Temporal, MCP, 评测, 候选评审]
---

# 01 原文分析：Making production-ready agents the default

## 原文信息

- **标题：** Making production-ready agents the default: building Duolingo's agent platform
- **作者：** Guadalupe Aliseda-Canton（Duolingo 工程博客，官方署名）
- **发布：** 2026-08-04（blog.duolingo.com；采集自 references/articles.md 待处理队列，日期 2026-08-09）
- **篇幅：** 正文约 2,000 英文词，抓取 Markdown 约 17KB（含 3 段 Python/YAML 代码块）；HTML 全文 47KB 存 `-full.md` 备用

## 原文价值评估（高 / 中 / 低）

**中高。** 一方工程博客，讲 Duolingo 如何把「生产就绪」从每个团队反复重建的负担，变成平台默认能力：

exec
/bin/bash -lc "cd /root/note-worker/candidates/20260809-180901 && sed -n '90,160p' works-ready/Six-Agent-Orchestration-Patterns-translation.md" in /root/note-worker
 succeeded in 0ms:
只要输入空间允许，就优先用确定性分类器（正则、关键词匹配、基于规则的转发）——它彻底移除了
一个模型故障面。路由还需要一个能反映生产输入的验证集，因为纸面上干净的分类体系并不能保证
边界处的分类可靠。

在模型层面，[AI Gateway](https://vercel.com/docs/ai-gateway) 通过单一端点路由数百个模型，
处理自动故障转移与负载均衡，并提供按提供商的回退。Okara 在这一层为[12 万多家企业](https://vercel.com/customers/how-okara-runs-cmo-agents-for-120000-companies-on-vercel)
运行首席营销官（CMO）智能体；把重试与回退搬进网关后，它现在每天处理 **40 亿 token**。
当每个输入都需要完全相同的处理、或分类准确率无法验证时，就不要用路由。

## 4. 独立子任务用并行化（parallelization）

并行化同时运行独立子任务，并用程序化方式聚合它们的输出。它使用**预定义**的子任务，
而编排器-工作器是在运行时确定子任务。适合的场景：子任务可以同时运行以换取速度，
或者同一任务的多个视角能提高结果可信度。**聚合步骤必须在扇出开始前定义好**，
因为不一致的工作器输出会在合并时抹掉延迟收益。

在 AI SDK 中，[子智能体（subagent）](https://ai-sdk.dev/docs/agents/subagents) 是通过父智能体的
工具被调用的智能体。每个子智能体拿到独立的上下文窗口，把聚焦的结果返回给父智能体，
这样上下文密集或并行的活儿就不会塞进主智能体的历史里。子智能体会增加延迟与协调成本，
所以只在上下文隔离或并行执行能带来可衡量收益时使用。

在大规模扇出中，**计费与代码同等重要**——每次并发调用的大部分生命周期都在等模型返回。
FLORA 的创意智能体从一个会话扇出到 50 多个图像模型。[Fluid compute](https://vercel.com/docs/fluid-compute)
按活动 CPU 计费，因此等待模型返回的时间不会计入计费表。当子任务必须按顺序互相依赖、
或需要共享同一上下文时，就不要用并行化。

## 5. 动态分解用编排器-工作器（orchestrator-worker）

在编排器-工作器中，中央 LLM 在运行时决定请求需要哪些子任务，把它们分配给工作器智能体，
再综合结果。在 AI SDK 里，每个工作器可以作为一个子智能体实现，通过工具暴露给父级
`ToolLoopAgent`。工作器在隔离的上下文中运行，返回综合所需的摘要结果。它的适用场景是
**子任务无法预测的复杂任务**——比如编码，要改几个文件取决于请求本身。对其他场景它就是过度设计。
每个工作器都有自己的上下文窗口，意味着协调既带来能力、也带来成本。

General Intelligence 的 Cofounder 给创始人提供了一支覆盖工程、市场、搜索引擎优化（SEO）、财务、
销售、客服与运营的完整智能体团队，形态与编排器-工作器一致。它的工程师每人每天提交
[10 个拉取请求（PR）](https://vercel.com/customers/how-general-intelligence-used-agents-to-build-an-agent-platform-on-vercel)
和 70+ 次提交，横跨 4,000+ 预览分支，90% 的站点可靠性工程（SRE）工作已自动化。
工作器代码隔离运行在 [Vercel Sandbox](https://vercel.com/docs/sandbox) 微虚拟机里，拥有独立的
文件系统与网络。当子任务可预测、或协调开销超过了动态分解的价值时，就不要用这个模式。

## 6. 质量可衡量时用评估器-优化器（evaluator-optimizer）

评估器-优化器把两个 LLM 调用配成一个循环：一个生成回答，另一个评估并给出反馈，
循环一直持续到达到质量阈值或步数上限。这个模式需要清晰的**评估评分标准**（rubric）和
可衡量的迭代改进收益，所以只有当回答真的能在评审下变好时，它的成本才值得。

两个信号会让它更适用：一是人类能说清有用反馈时回答确实变好，二是 LLM 自己也能给出有用反馈。
**失控评审循环（runaway critique loop）**反模式出现在：标准含糊不清，一直要求改稿却没有可衡量的终点。
当首次尝试的质量已经达标时就别用这个模式，并且要在应用代码里强制设置硬性改稿上限。
在基于智能体的实现中，AI SDK 暴露了 `stopWhen` 条件和 AI SDK 7 的超时预算，用来约束总执行时长
与每步执行时长。

[Vercel 的 Turborepo 性能改造](https://vercel.com/solutions/turborepo)是这个评审循环的人机协同版本：
AI 智能体、Vercel Sandbox 与人工评审在八天内带来了最高 [96% 的提速](https://vercel.com/blog/making-turborepo-ninety-six-percent-faster-with-agents-sandboxes-and-humans)，
同一项工作也发现：无人值守的最先进智能体，若不做上下文工程，就会达不到预期。

Vercel 的 Next.js 智能体评测发现，在 Next.js 16 API 上 `AGENTS.md` 优于 skills。
Vercel Sandbox 把每次隔离运行限制在 Hobby 计划的 45 分钟、Pro 与 Enterprise 计划的 24 小时，
这限定了评审循环最长能执行多久。

## Vercel 在生产中如何运行这些编排模式

六种模式是架构决策，但有四种平台行为能消除跨模式累积的故障模式。在实践中，它们针对的是
不同形态工作里的同一批运行时问题：状态恢复、模型选择、扇出成本与隔离执行。

### Fluid compute 降低扇出步骤的活动 CPU 成本

并行化与编排器-工作器会扇出大量以 I/O 等待为主的并发调用。团队必须拒绝任何按这种等待计费的
计费模型，否则大规模扇出就不可行。Fluid compute 单独计量活动 CPU，[基础费率 $0.128/小时](https://vercel.com/docs/functions/usage-and-pricing)，
区域费率与其他计量资源仍然适用。

exec
/bin/bash -lc "cd /root/note-worker/candidates/20260809-180901 && sed -n '75,140p' works-ready/Making-production-ready-agents-the-defau-translation.md" in /root/note-worker
 succeeded in 0ms:

## 为什么选 Temporal？

Temporal 是一个持久化工作流引擎（durable workflow engine）。它持久化状态、安全地重试，并跨系统协调长期运行的工作。

这与智能体的特性非常契合，因为智能体可能：

- 运行需要好几分钟
- 调用外部工具
- 等待人工输入
- 以需要重试或调试的方式失败

与其把一次智能体运行当成一次性进程，我们可以把它当作一个工作流。工作流持有持久化状态并负责编排。Activity 处理副作用——比如准备工作区、克隆仓库或保存结果——而 Query 在工作流运行期间暴露状态。

我们也已经围绕 Temporal 建好了足够多的基础设施，可以从任何入口触发工作流；既然智能体是在工作流里运行的，我们也就天然支持从任何地方运行智能体。如果你好奇，可以听听 Staff Software Engineer Zhihao Wang 在[这里](https://temporal.io/resources/case-studies/duolingo-temporal-nexus?ref=blog.duolingo.com)的分享。

## 把定义与执行解耦

在构建这个平台之前，提示词、模型、SDK、工具链与执行环境都是紧耦合的。

AgentWorkflow 改变了这一点。我们可以通过定义智能体「做什么、需要什么工具、返回什么」来创建它，而工作流管理关于它如何运行的一切。

这种区分对构建一个能够规模化（scale）的智能体平台至关重要。一旦执行与行为相互独立，我们就可以独立演进运行时、模型、工具链与评测，而无需改变消费者使用的接口。

正是这种分离让平台的下一轮迭代成为可能：对 OpenAI Agents SDK 的支持。

### 新的运行时

AgentWorkflow 已经支持若干运行时，包括 Claude Agents SDK 与 Codex CLI。增加对另一个运行时的支持，并不需要改变智能体的定义或调用方式；它只是成为同一个工作流抽象背后的又一个实现。

加入这个新运行时影响很大。OpenAI Agents SDK 显著改善了平台的操作特性，具体体现在两个方面：

1. 借助 Temporal 插件，MCP 工具调用变成了 Temporal activity。这让系统更持久化（durable），因为工具失败可以复用与其他任何工作流 activity 相同的重试策略、状态管理与失败处理。它也让系统更可观测，因为每一次工具调用——包括输入、输出、失败与重试——都在 Temporal UI 中可见。
2. OpenAI Agents SDK 还支持通过代理（proxy）路由请求。这让我们能够使用内部 LLM 网关（LLM Gateway），提供成本追踪、用量追踪与提供商抽象。与其为每个模型提供商分别维护 SDK 集成，我们可以把请求路由到网关，在一个一致接口后面切换提供商。

## 评测智能体

智能体变得可复用之后，下一个挑战是知道它们是在变好还是变差。

这对会改动代码的智能体尤其重要。光问「智能体的输出听起来是否合理」是不够的；我们需要知道它是否做了正确的改动。

为此我们构建了智能体评测（agent eval）基础设施。

智能体评测让真实的智能体跑编写好的场景（authored scenarios）。在评分之前，它们会捕获智能体的输出、改动的文件与 git diff。

一个简化版的评测用例长这样：

```python
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

exec
/bin/bash -lc "cd /root/note-worker && cat working/AGENTS.md && echo '===TEMPLATES===' && ls templates/ && head -40 templates/*.md 2>/dev/null | head -60" in /root/note-worker
 succeeded in 0ms:
# working/ — 作品输出（Phase 5）

可展示的成果：译文、工具、模板、教程。**作品应可独立理解，不依赖知识库其他上下文**——适合分享到博客/GitHub。

## 文件约定

- 每个作品一个文件或子目录：`{简述}.md`
- 译文沿用 `scripts/translator.py` 产出的 frontmatter 约定（title/sourceUrl/sourceAuthor/translatedAt…）
- 作品应是**完成态**：不是草稿（草稿放 `expand/` 相关分类）

## 与 expand 的关系

- `expand/` 是内部加工稿（concepts 层），`working/` 是最终对外输出
- 加工稿 → 打磨 → 移到 working/ 即"毕业"

## 已有作品 ｜（待建设）===TEMPLATES===
新条目模板.md
---
created: <% tp.date.now("YYYY-MM-DD") %>
updated: <% tp.date.now("YYYY-MM-DD") %>
sources: [来源]
tags: [内容标签, type/教程, status/待验证]
---

# <% tp.file.title %>

一句话概述这个概念。

## 详细说明

正文内容...

## 相关条目
- [[相关条目A]]
- [[相关条目B]]

exec
/bin/bash -lc "cd /root/note-worker/candidates/20260809-180901 && sed -n '120,190p' works-ready/One-shotting-a-Raccoon-Heist-game-using-translation.md" in /root/note-worker
 succeeded in 0ms:
  body.scale.set(0.9, 0.8, 1.5);
  body.position.y = 0.55;
  body.castShadow = true;
  g.add(body);
  const head = new THREE.Mesh(new THREE.SphereGeometry(0.3, 10, 8), M(BROWN));
  head.position.set(0, 0.85, 0.62);
  g.add(head);
  const snout = new THREE.Mesh(new THREE.SphereGeometry(0.16, 8, 6), M(DARK));
  snout.scale.set(0.9, 0.7, 1.3);
  snout.position.set(0, 0.76, 0.9);
  g.add(snout);
  const nose = new THREE.Mesh(new THREE.SphereGeometry(0.06, 6, 6), M(BLACK));
  nose.position.set(0, 0.78, 1.08);
  g.add(nose);
  for (const s of [-1, 1]) {
    const ear = new THREE.Mesh(new THREE.SphereGeometry(0.12, 6, 6), M(DARK));
    ear.scale.set(0.7, 1.3, 0.5);
    ear.position.set(0.2 * s, 1.08, 0.55);
    g.add(ear);
    const eye = new THREE.Mesh(new THREE.SphereGeometry(0.05, 6, 6), M(0x1a1a1a, { emissive: 0x331111 }));
    eye.position.set(0.13 * s, 0.92, 0.86);
    g.add(eye);
  }
  const tail = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.09, 0.5, 6), M(DARK));
  tail.position.set(0, 0.8, -0.62);
  tail.rotation.x = 0.8;
  g.add(tail);
  // spiked collar
  const collar = new THREE.Mesh(new THREE.TorusGeometry(0.22, 0.05, 6, 12), M(0xc0392b));
  collar.position.set(0, 0.78, 0.5);
  collar.rotation.x = Math.PI / 2.4;
  g.add(collar);
  const legGeo = new THREE.CylinderGeometry(0.07, 0.09, 0.34, 6);
  const legs = [];
  for (const [x, z] of [[-0.22, 0.35], [0.22, 0.35], [-0.22, -0.35], [0.22, -0.35]]) {
    const leg = new THREE.Mesh(legGeo, M(DARK));
    leg.position.set(x, 0.17, z);
    g.add(leg);
    legs.push(leg);
  }
  let phase = Math.random() * 10;
  return {
    group: g,
    animate(dt, speed) {
      phase += dt * (3 + speed * 10);
      const amp = Math.min(0.6, 0.1 + speed * 0.6);
      legs[0].rotation.x = Math.sin(phase) * amp;
      legs[3].rotation.x = Math.sin(phase) * amp;
      legs[1].rotation.x = -Math.sin(phase) * amp;
      legs[2].rotation.x = -Math.sin(phase) * amp;
      tail.rotation.z = Math.sin(phase * 1.5) * 0.4;
      body.position.y = 0.55 + Math.abs(Math.sin(phase)) * 0.04 * (0.3 + speed);
    },
  };
}
```

接着用 Playwright 对它做了一[轮测试](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-24-09-230Z)，包括[另一张截图](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-24-33-559Z)。

```
  // walk near the dog
  await page.evaluate(() => { const d = window.__rh.dog; window.__rh.teleport(d.x + 6, d.z); });
  await page.waitForTimeout(2000);
  info = await page.evaluate(() => JSON.stringify({ dog: window.__rh.dog, state: window.__rh.state, player: window.__rh.debug().player }));
  console.log('after approach:', info);
  await page.waitForTimeout(3000);
  info = await page.evaluate(() => JSON.stringify({ dog: window.__rh.dog, state: window.__rh.state }));
  console.log('after chase:', info);
  await page.screenshot({ path: __dirname + '/shot-dog.png' });
```


exec
/bin/bash -lc "cd /root/note-worker && rg -l -i \"编排|orchestrat|上下文工程|context engineering|harness\" wiki/ expand/ working/ --glob '*.md' | head -30 && echo '===AGENTS-md===' && rg -n \"工作区|working|expand|收录\" agents.md | head -20" in /root/note-worker
 succeeded in 0ms:
expand/index.md
expand/thinking/AGENTS.md
wiki/09-源码解读/juedge0解析文档/16-配置文件详解.md
expand/thinking/MCP协议标准化的增量与边界.md
wiki/09-源码解读/juedge0解析文档/5-系统架构设计.md
expand/06-AI与LLM/Agent工具与平台/n8n.md
expand/06-AI与LLM/Agent工具与平台/ECC.md
expand/知识图谱.md
wiki/09-源码解读/Claude Code源码解读/6-wu-ceng-jia-gou-she-ji.md
wiki/09-源码解读/Claude Code源码解读/2-kuai-su-kai-shi.md
wiki/09-源码解读/Claude Code源码解读/10-gong-ju-xi-tong-jia-gou.md
wiki/09-源码解读/Claude Code源码解读/1-xiang-mu-gai-lan.md
wiki/opencode项目解读/S级亮点专项.md
wiki/opencode项目解读/项目技术画像.md
wiki/09-源码解读/Claude Code源码解读/21-zi-ding-yi-agents.md
wiki/opencode项目解读/业务背景重建.md
wiki/09-源码解读/Claude Code源码解读/7-agentic-loop-he-xin-xun-huan.md
wiki/opencode项目解读/技术亮点评估.md
wiki/09-源码解读/Claude Code源码解读/11-nei-zhi-gong-ju-xiang-jie.md
wiki/opencode项目解读/能力缺口分析.md
wiki/opencode项目解读/业务流程梳理.md
wiki/opencode项目解读/系统架构总览.md
wiki/09-源码解读/Claude Code源码解读/19-agent-xie-diao-mo-shi.md
wiki/opencode项目解读/模块技术说明.md
wiki/opencode项目解读/项目文档索引.md
wiki/09-源码解读/Claude Code源码解读/13-computer-use-dian-nao-cao-kong.md
wiki/09-源码解读/Claude Code源码解读/9-hui-hua-zhuang-tai-guan-li.md
wiki/06-AI与LLM/langchain4jlanggraph4j 学习/langgraph4j-study-notes-02-advanced.md
wiki/06-AI与LLM/langchain4jlanggraph4j 学习/langgraph4j-study-notes-01-core.md
wiki/06-AI与LLM/AgentRag 学习/MCP协议与工具调用.md
===AGENTS-md===
5:你是个人知识库的管理助手。你的任务是阅读外部素材索引，将其加工为结构化、互相链接的知识条目，并按内容性质归入对应产出模块（expand/thinking、working/、prompts/）。
13:│   └── articles.md ← 文章收录权威索引（### N. 编号正文 + 待处理队列，harness 格式，状态/归属字段机器可读）
16:├── expand/        ← 第三层：AI 加工产物（thinking 思考主导 + 存量概念/深度笔记 + 索引与自动化文档）
22:├── working/       ← Phase 4：作品输出（译文/工具/模板，可独立理解）
24:├── prompts/       ← 有效提示词积累（只收录验证有效的；不属知识图谱，不参与一致性门禁）
53:Phase 2 expand/      ← AI 加工产物（概念/深度笔记 = concepts 层）
55:Phase 4 working/     ← 作品输出（译文/工具/模板）
58:读完一篇文章后的去处：判值 → `references/articles.md`（编号正文标记 已收录/已淘汰/归属）→ 有观点进 `expand/thinking/`；想输出 → `working/`；有有效提示词 → `prompts/`。
64:3. 检查 `expand/` 与 `wiki/` 中相关条目；**AI 生成/更新的条目一律写入 `expand/`**（`wiki/` 只读，绝不写入）——独立思考/观点统一写 `expand/thinking/`
65:4. 在 `expand/` 条目之间建立双向链接 `[[]]`，并更新相关条目的 `## 相关条目` 段；链接 `wiki/` 个人笔记为单向，回链由用户自行决定
66:5. 更新 `expand/index.md` 内容目录
67:6. 在 `expand/log.md` 中追加变更记录
68:7. 更新 `expand/知识图谱.md` 关系描述
88:1. 新增 `expand/` 条目**必须**同时更新 `expand/index.md`（计数 + 条目表），否则 K2/K5 拦截
91:4. `expand/` 必检文档中的 markdown 表格必须形状对齐（K6）
92:5. `references/articles.md` 编号条目的「状态：」必须 ∈ {待处理, 已收录, 已淘汰}；归属字段若指向 `expand/` 必须真实存在（K1）
118:### AI 生成条目：深度技术笔记模板（存量概念类，2026-08 起 expand 定位为 thinking）
120:> **当前默认：** expand/ 只承担 thinking（独立思考）作用。新摄入的外部素材默认进 `expand/thinking/`，
122:> 仅当素材确实需要（技术深度大于观点价值）且用户明确要求时使用，写入对应 `expand/01-xx` 分类目录。
201:4. `wiki/` 个人笔记只读：AI 只可读取用于链接，不修改、不追加内容；如个人笔记需要回链到 `expand/` 条目，由用户手动添加

codex
四篇素材与译文均已核对（译文与 works-ready 一致）。补看一眼 Raccoon 译文中段与六模式译文开头，确认无跳段。
exec
/bin/bash -lc "cd /root/note-worker/candidates/20260809-180901 && sed -n '75,115p' works-ready/One-shotting-a-Raccoon-Heist-game-using-translation.md" in /root/note-worker
 succeeded in 0ms:
> 边工作边把进展写进 notes.md 文件，并把对它的修改包含进每一次提交。

我没有做任何技术选型。我（正确地）猜它大概会用 [Three.js](https://threejs.org/)——基于以往的经验。

给 Claude 一个 OpenAI key 的效果出乎意料地好，正好补上它能力的缺口——这次我们需要某种生成图片来当贴图的方式。Fable 非常擅长给图像生成器写提示词！

我说「独立工作——不要让我做任何进一步的设计决定」，是因为我想看看它能否在不需要我任何进一步输入的情况下，产出一款完整可玩的游戏。

我还说了「尽可能频繁地提交并推送，这样我就能预览你的进度」。当你在 Claude iPhone 应用里使用 Claude Code 时，你会给它一个 GitHub 仓库，它在分支上工作。告诉它「尽可能频繁推送」，提交就会立刻开始落进那个分支。

我喜欢要一份 `notes.md` 作为一点额外风味——这是[那份最终文件](https://github.com/simonw/raccoon-heist/blob/main/notes.md)，以及它加入那条狗时写的记录：

> 新的升级：从第 3 夜起，院子里会有一只巡逻的护卫犬——一只低多边形棕色猎犬，戴着红色尖刺项圈，尾巴摇来摇去。它会在随机地点之间游荡，12 个单位内闻到你的气味就会追踪你（视线完全无关——全靠鼻子，头顶会显示 👃 并且会吠叫）。如果你拉开 17 个单位的距离，它就会放弃。被抓提示现在按来源区分：守卫 / 车灯 / 猎犬。已用自动化测试验证 游荡 → 追踪 → 被抓 的流程。

### 回顾对话记录

你可以访问 [Claude Code 共享会话](https://claude.ai/code/session_01NUBoCfnhGETcCDyEUPS8jp)，我还用我的 [claude-code-transcripts](https://github.com/simonw/claude-code-transcripts) 工具导出了一份我自己的 HTML 版本，[可以在这里找到](https://simonw.github.io/raccoon-heist/transcript/page-001.html)。

Fable 先做了一个 index 页面，[内置了一份](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T14-55-13-304Z) Three.js 副本，然后写了自己的 [gen_textures.py 脚本](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T14-55-49-064Z)（[副本在这里](https://github.com/simonw/raccoon-heist/blob/main/gen_textures.py)）。

它生成了贴图，并[抽查](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T14-59-07-900Z)确认效果没问题。它给垃圾桶生成的 [metal.jpg](https://github.com/simonw/raccoon-heist/blob/main/textures/metal.jpg) 长这样，不过我并不觉得它在游戏里被用对了地方：

![一张深蓝灰色铆接金属面板的游戏纹理图集：左上角是带把手的圆形舱门，中间是瓦楞波纹板，左下角是素面圆形板，顶部和底部是平坦的带状条。没有可见文字。](https://raw.githubusercontent.com/simonw/raccoon-heist/refs/heads/main/textures/metal.jpg)

然后它搭出了游戏的第一版，接着[决定](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-04-51-625Z)用 Playwright 在「预装的 Chromium」里做冒烟测试。这意味着它可以给自己的作品截图，然后[亲自过目](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-05-53-823Z)。它分别对桌面和移动宽度的页面做了这件事，然后注意到[移动宽度下浣熊不可见](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-09-33-406Z)，于是[修复了它](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-14-39-180Z)：

> 浣熊、垃圾箱藏身处和两个队友浣熊在移动端现在完全可见了。提交这个关键修复。

它决定做一个标题画面，用这个 [gen_title.py](https://github.com/simonw/raccoon-heist/blob/main/gen_title.py) 脚本[做了出来](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-15-02-574Z)。这是它给 `gpt-image-2` 用的提示词：

> `Video game key art, low-poly 3D render style, moody nighttime scene: a cute low-poly raccoon wearing a tiny black burglar mask sneaking on its hind legs carrying a glowing gold coin, next to a tipped-over metal trash can, suburban house with warm glowing windows in the background, deep blue night, full moon, fireflies, cinematic rim lighting, charming heist caper mood. No text, no words, no logos.`

（中文：游戏主视觉，低多边形 3D 渲染风格，阴郁的夜景：一只戴着小小黑色强盗面罩的可爱低多边形浣熊，用后腿蹑手蹑脚地走，叼着一枚发光的金币，旁边是一个被掀翻的金属垃圾桶，背景是亮着暖光窗户的郊区房屋，深蓝夜空、满月、萤火虫、电影感轮廓光，迷人的劫案片氛围。不要文字、不要单词、不要 logo。）

生成的图片（Claude [觉得它「美极了」](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-16-42-176Z)）——不过我注意到，它在桌面端显示时会被裁掉，只剩上面三分之一，浣熊都不见了！

![一只拿着金币的多边形浣熊，旁边是翻倒的垃圾桶，背景是房子和月亮。](https://static.simonwillison.net/static/2026/raccoon-heist-title.jpeg)

然后是我最喜欢的一处改动：它[加了一条狗](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-23-00-850Z)：

```

exec
/bin/bash -lc "cd /root/note-worker/candidates/20260809-180901 && sed -n '1,60p' works-ready/Six-Agent-Orchestration-Patterns-translation.md" in /root/note-worker
 succeeded in 0ms:
---
created: 2026-08-09
updated: 2026-08-09
title: 六种智能体编排模式
sourceUrl: https://vercel.com/i/agent-orchestration-patterns
sourceAuthor: Vercel（官方平台指南）
translatedAt: 2026-08-09
sources: [references/articles.md 待处理队列]
tags: [AI Agent, 编排, Agent 架构, Vercel, AI SDK, type/翻译]
---

# 六种智能体编排模式

当一个 AI 功能成长到超过单条提示词之后，问题就变成了：如何把大语言模型（LLM）调用连接成一个
在生产负载下依然可靠的系统。合适的编排模式应当匹配任务的**可分解性（task decomposability）、
延迟容忍度、token 预算与人在回路（human-in-the-loop）要求**。先选能解决问题的最简单模式，
只有当工作负载确实需要时才升级。六种模式对应了可靠性、成本与协调之间的这些权衡。

**要点速览（Key takeaways）：**

- 多智能体系统的 token 用量最高可达普通聊天的 15 倍，因此任务价值必须配得上这份额外复杂度。
- 在相同计算预算下，单智能体循环在多跳推理任务上的准确率不输、甚至超过多智能体
  （Qwen3、DeepSeek-R1 与 Gemini 2.5 均验证）。
- 提示词链是从单次 LLM 调用升级的最低风险选项，但链式准确率会一步步复利折损。
- 编排器-工作器是为「子任务数量与性质在编写时未知」设计的模式，因此它是多智能体工作的
  **入口**而非默认选择。
- Vercel Workflows 会对每一步做检查点（checkpoint），并处理失败重试以及因外部事件而暂停，
  因此六种模式都能持久化运行。
- FLORA 的创意智能体把单个会话扇出到 50 多个图像模型，每一步都会持久化并在失败时重试。

## 智能体编排模式一览

在加智能体之前，先从最低复杂度的模式开始。六种模式构成一条复杂度阶梯。**过早扇出（premature fan-out）**
反模式出现在：团队在工作负载还没有独立子任务时就引入智能体，成本和故障面被同时放大。

多智能体系统使用的 token 大约是[聊天交互的 15 倍](https://www.anthropic.com/engineering/multi-agent-research-system)，
所以任务价值必须配得上这些新增的智能体。模式选择取决于工作负载，而不是团队的雄心。

六种模式在适用性、token 成本与失败条件上各不相同。选型前，可把这张表当作规划区间来用：

| 模式 | 最适合 | 相对单次调用的 token 成本 | 何时避免 |
| --- | --- | --- | --- |
| 单智能体循环 | 任务能装进一个带工具访问权限的上下文窗口 | 基线 | 存在可从并行探索中受益的独立子任务 |
| 提示词链 | 编写时已知的固定子任务 | 中等，由链长决定 | 子任务边界未知 |
| 路由 | 不同输入类别分开处理 | 低到中等 | 输入需要完全相同的处理 |
| 并行化 | 预定义的独立子任务 | 高，随扇出规模变化 | 存在顺序依赖或共享上下文 |
| 编排器-工作器 | 子任务直到运行时才可预测 | 高，随工作器数量变化 | 子任务可预测 |
| 评估器-优化器 | 有清晰评分标准且迭代有可衡量收益 | 中等，随评审循环次数变化 | 需要实时响应或没有评分标准 |

这些区间是锚定在实测的智能体与多智能体 token 数据上的相对估计。2026 年 7 月的
AI Gateway 生产指数（Production Index）显示，Anthropic 占[AI Gateway 支出的 61%](https://vercel.com/blog/ai-gateway-production-index-july-2026)、
却只占 token 量的 32%——也就是说，最重要的智能体工作集中了成本。在[智能体工作流模式](https://vercel.com/i/what-are-agentic-workflows)之间做选择，
先于任何基础设施决策。

## 1. 从单智能体循环开始智能体编排

在相同 token 预算下，[单智能体基线](https://arxiv.org/html/2604.02460v1)在多跳推理上的准确率不输、
甚至超过多智能体；那些被报道的多智能体优势，用未计量的计算量来解释，比用架构来解释更合理。

同样的约束也出现在生产中：越简单的架构走得越远，而并行写作仍会遇到协调与上下文共享的约束。

codex
评审完成。四篇候选的三件套（原文、译文、works-ready）已全部通读，并与 `references/articles.md`、`expand/` 既有条目对照。以下为评审结果。

---

### The new rules of context engineering for Claude 5 generation models

- **原文价值**：高 — Anthropic 工程师亲笔的方法论长文，核心洞察扎实（系统提示词删 80% 且评测无损）+ 六组「过去/现在」神话破除 + 系统提示词/CLAUDE.md/Skills/References 四类落地建议，非发布稿。
- **翻译质量**：精品 — 完整逐译，`渐进披露 / 制品 / 评分标准 / harness 执行框架` 等术语到位，通顺且保留了原文粗体强调结构。
- **与知识库契合度**：补薄弱环节 — 知识库有 Claude Code 源码解读与 `expand/thinking/MCP协议标准化的增量与边界.md`，但缺「上下文工程」方法论条目，而这恰是 Harness Engineering 主题的核心空白。
- **一句话定性 + 建议去向**：harness 上下文工程的方法论基准，译文可直接毕业 → `working/` 正式收录（译文作品），并在 `articles.md` 编号正文标记已收录、关联 wiki Claude Code 源码解读。

### One-shotting a Raccoon Heist game using Claude Fable 5

- **原文价值**：中 — 一手实操案例：单提示词 + 用 OpenAI key 补能力缺口、GitHub Pages 移动端预览循环、Playwright 自测截图、对「生成游戏不好玩」的诚实结论，都是真实信号；但属体验叙事，理论密度低。
- **翻译质量**：合格 — 完整逐译，代码块与截图说明保留，给 `gpt-image-2` 英文提示词补中文释义是加分处理；个别长句略平。
- **与知识库契合度**：边缘补白 — 知识库无 vibe coding / 游戏生成主题，与 KMP·Flutter·harness 主线弱相关，仅「agent 自测 + 移动端预览」工作流可借鉴。
- **一句话定性 + 建议去向**：agent 单次生成能力的实测样本，参考价值有限 → `articles.md` 观察项一行（防重复采集，标注「含可复用 agent 预览/自测工作流」），译文不收录。

### Six Agent Orchestration Patterns

- **原文价值**：中 — 六模式框架源自 Anthropic 既有分类（非原创），增量在 Vercel 生产视角：token 成本对照表、链式准确率复利（95%^10≈60%）、持久化/计费/沙箱平台行为；后半段是平台推广，但数据点可作参考。
- **翻译质量**：精品 — 完整逐译，六行选型表格结构完整保留，`编排器-工作器 / 评估器-优化器 / 过早扇出 / 失控评审循环` 等术语统一到位。
- **与知识库契合度**：补薄弱环节 — `expand/06-AI与LLM/Agent工具与平台/n8n.md`、`ECC.md` 讲平台与 harness，wiki 有 Claude Code 协调模式与 langgraph4j 笔记，但缺「模式选型决策框架 + token 成本量级」的浓缩参考，不重复。
- **一句话定性 + 建议去向**：六模式选型表是低成本高复用的参考作品（需标注框架出处为 Anthropic）→ `working/` 正式收录（译文作品），亦可作为 `articles.md` 编号正文「已收录」。

### Making production-ready agents the default: building Duolingo's agent platform

- **原文价值**：高 — 一方工程案例，实质内容足：`AgentDefinition` 注册表、Temporal `AgentWorkflow` 包装、定义与执行解耦、多运行时（含 OpenAI Agents SDK + MCP 工具调用转 activity）、确定性优先的评测 grader（`diff_assertions` / `no_op_consistency`），量化结果「数周 → 10 分钟」。
- **翻译质量**：合格 — 完整逐译，代码块保留，通顺度好；个别术语略直译（`生产化`、`包装器`），不影响理解。
- **与知识库契合度**：补薄弱环节 — 与 `expand/06-AI与LLM/Agent工具与平台/ECC.md`（harness 抽象）理念互补而非重复，评测 grader 设计与 `expand/thinking/MCP协议标准化的增量与边界.md` 的工具语义话题可互链。
- **一句话定性 + 建议去向**：生产级 agent 平台架构的一手参考，评测「检查产物而非文字」思路尤其值得沉淀 → `working/` 正式收录（译文作品），并建议在 `expand/thinking/` 提炼一条平台化抽象与评测优先的独立观点（可选）。

---

## 汇总

| 篇名 | 原文价值 | 翻译质量 | 契合度 | 定性 | 建议去向 |
| --- | --- | --- | --- | --- | --- |
| The new rules of context engineering for Claude 5 generation models | 高 | 精品 | 补薄弱环节（上下文工程方法论空白） | harness 上下文工程基准方法论 | `working/` 正式收录 |
| One-shotting a Raccoon Heist game using Claude Fable 5 | 中 | 合格 | 边缘补白（与主线弱相关） | agent 单次生成实测样本 | `articles.md` 观察项一行 |
| Six Agent Orchestration Patterns | 中 | 精品 | 补薄弱环节（模式选型 + 成本量级） | 选型参考框架（出处 Anthropic） | `working/` 正式收录 |
| Making production-ready agents the default: building Duolingo's agent platform | 高 | 合格 | 补薄弱环节（生产平台架构 + 评测） | 生产级 agent 平台工程案例 | `working/` 正式收录 |

评审仅输出结论，未修改任何文件；后续按建议落库时，记得在 `references/articles.md` 编号正文登记状态与归属（同一次提交同步 `expand/index.md` 等下游缓存）。
tokens used
65,840
