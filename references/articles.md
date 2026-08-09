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
<!-- 当前：1 条待处理 -->
| Rust 2025 官方博客：Rust 1.85 版本说明（Move 语义 / Borrow Checker 演进） | https://blog.rust-lang.org/2025/02/20/Rust-1.85.0.html | dispatch-e2e | 2026-08-09 |
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

## 统计

- **正式收录：** 11 篇（编号 01-10、14）｜**已淘汰隔离：** 3 篇（编号 11-13，不计入收录数，仅防重复采集）

## 待补充

- [ ] 占位：外部新文章先查编号 01-14 确认未收，再由采集层写入「待处理」队列
