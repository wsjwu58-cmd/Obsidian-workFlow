---
created: 2026-08-04
updated: 2026-08-04
sources: [raw/github-2026-08-03-7033561e.md]
tags: [AI, Agent, 记忆机制, 技能学习]
---

# Hermes-Agent

Nous Research 的自我改进型 AI 代理：内置学习循环，能从经验创建并改进技能、主动维护记忆、跨会话积累对用户的了解。

## 详细说明

Hermes Agent 的闭环学习是核心差异：复杂任务后自动创建技能，技能在使用中自我改进，FTS5 会话搜索结合 LLM 摘要实现跨会话回忆，并兼容 agentskills.io 开放技能标准。它支持 Telegram / Discord / Slack / WhatsApp / CLI 多端接入、内置 cron 定时自动化、子代理委派并行，可运行在 5 美元 VPS 或无服务器环境，模型可自由切换（Nous Portal / OpenRouter / OpenAI / 自建端点）。

## 相关条目
- [[Agent搭建]]
- [[多智能体与记忆机制]]
- [[22-skills-ji-neng-kai-fa]]
- [[ECC]]
- [[n8n]]
