---
created: 2026-09-12
updated: 2026-09-12
title: farion1231/cc-switch —— 面向 Claude Code、Codex 等八大 AI 编程工具的跨平台一站式管理器
sourceUrl: https://github.com/farion1231/cc-switch
sourceAuthor: Jason Young（farion1231，CC Switch 官方 GitHub 仓库）
translatedAt: 2026-09-12
sources: [references/articles.md 待处理队列]
tags: [CC Switch, Claude Code, Codex, Tauri, Rust, Provider 管理, MCP, Skills, 桌面应用, type/翻译]
---

<div align="center">

# CC Switch

### Claude Code、Claude Desktop、Codex、Gemini CLI、Grok Build、OpenCode、OpenClaw 和 Hermes Agent 的全方位管理工具

[![Version](https://img.shields.io/github/v/release/farion1231/cc-switch?color=blue&label=version)](https://github.com/farion1231/cc-switch/releases)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/farion1231/cc-switch/releases)
[![Built with Tauri](https://img.shields.io/badge/built%20with-Tauri%202-orange.svg)](https://tauri.app/)
[![Downloads](https://img.shields.io/github/downloads/farion1231/cc-switch/total)](https://github.com/farion1231/cc-switch/releases/latest)

<a href="https://trendshift.io/repositories/15372" target="_blank"><img src="https://trendshift.io/api/badge/repositories/15372" alt="farion1231%2Fcc-switch | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>
<a href="https://www.star-history.com/#farion1231/cc-switch&Date"><picture><source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/badge?repo=farion1231/cc-switch&theme=dark" /><img alt="Star History Rank" src="https://api.star-history.com/badge?repo=farion1231/cc-switch" width="196" height="55" /></picture></a>

### 🌐 唯一官方网站：**[ccswitch.io](https://ccswitch.io)**

English | [中文](README_ZH.md) | [日本語](README_JA.md) | [Deutsch](README_DE.md) | [Changelog](CHANGELOG.md)

</div>

> 开源仓库：`farion1231/cc-switch`（主语言 Rust；截至 2026-09-12 约 132,370 stars / 9,129 forks / 2,663 open issues；MIT 许可证；最新版本 v3.20.3，2026-09-11 发布）
> 原文：https://github.com/farion1231/cc-switch · 唯一官方网站：https://ccswitch.io

## ❤️赞助商

> [想出现在这里？](mailto:farion1231@gmail.com)

<details open>
<summary>点击折叠</summary>

> 本节为原文赞助商广告（顶部 Kimi 广告位 + 32 行赞助商表格）的压缩摘译，完整英文原文见同批次抓取文件
> `sources/farion1231-cc-switch---A-cross-platform-full.md`。各家赞助商名称、可点击链接与关键促销信息均予保留。

[![Kimi K2.7 Code](https://gcdn.moonshot.cn/growth-cdn/sponsor/kimi-en.png)](https://platform.kimi.ai?track_id=track-20d65732f0aa45dcb1df9691a15610af&aff=cc-switch)

- **[Kimi（Moonshot AI）](https://platform.kimi.ai?track_id=track-20d65732f0aa45dcb1df9691a15610af&aff=cc-switch)**：Kimi K3 是 Moonshot AI 最强模型、全球首个开源 3T 级模型，2.8 万亿参数、原生视觉、100 万 token 上下文。新用户充值送 10% 赠额（上限 ¥1,000）；重度编程可考虑 [Kimi Code 订阅](https://www.kimi.com/code/?aff=cc-switch)。
- **[PackyCode](https://www.packyapi.ai/register?aff=cc-switch)**：可靠高效的 API 中转服务商，提供 Claude Code、Codex、Gemini 等中转服务。CC Switch 用户首充输入促销码 `cc-switch` 享 9 折。
- **[ZetaAPI](https://zetaapi.ai/go/u117)**：主打模型不掺水、保真不降智，价格低至官方 35%；企业级 SLA 稳定性，一个 API Key 调用多模型。首充输入促销码 `CC-SWITCH` 首充 9 折。
- **[APINEBULA](https://apinebula.ai/VjM74M)**：银河录像局旗下企业级 AI 聚合平台，集成 Claude、GPT、Gemini 等全能力模型，企业级高并发、正式合同与开票。首充输入促销码 `ccswitch` 享 9 折。
- **[AICodeMirror](https://www.aicodemirror.ai/register?invitecode=9915W3)**：Claude Code / Codex / Gemini CLI 官方高稳定中转，企业级并发、快速开票、7×24 技术支持。CC Switch 用户首充 8 折，企业客户最高 75 折。
- **[PatewayAI](https://pateway.ai/?ch=etzpm8&aff=WB6M6F67#/)**：面向重度 AI 开发者的 API 中转，100% 官方渠道的完整 Claude 系列与 Codex 系列，支持企业级并发与逐行可审计账单。注册送 $3 试用额度，充值低至 6 折。
- **[Fenno.ai](https://api.fenno.ai/register?redirect=/purchase?tab=subscription%26group=16&aff=P9MR3D3PLCNL)**：稳定高效的 API 中转，目前专注 Codex 中转，兼容 OpenAI 与 Anthropic 协议，支持 Codex、Claude Code、OpenCode 等工具。$1.99 试用套餐含 $50 额度（7 天），推荐最高返 20%。
- **[RunAPI](https://runapi.host/register?aff=iOKB)**：高性能 AI 模型 API 网关，一个 Key 接入 OpenAI、Claude、Gemini、DeepSeek、Grok 等 150+ 主流模型，价格低至官方 10%。首充 9 折。
- **[胜算云（Shengsuanyun）](https://www.shengsuanyun.com/?from=CH_4HHXMRYF)**：服务 AI Native Teams 的工业级 AI 任务并行执行平台，模型市场聚合 Claude、ChatGPT、Gemini 等，支持 BYOK 托管与按量计费（另有 [服务状态页](https://watch.shengsuanyun.com/status/shengsuanyun)）。新用户注册送 ¥10 额度，首充加赠 10%。
- **[AIGoCode](https://aigocode.app/invite/CC-SWITCH)**：集成 Claude Code、Codex 与最新 Gemini 模型的一站式平台，账号零封禁风险、无需 VPN。首充额外加赠 10% 额度。
- **[AICoding](https://aicoding.inc/i/CCSWITCH)**：全球 AI 模型 API 中转，Claude Code 低至原价 19%、GPT 低至 1%，支持企业级高并发、快速开票、7×24 技术支持。首充 9 折。
- **[SubRouter](https://subrouter.ai/register?aff=l3ri)**：面向 AI 服务经营者的市场中台与智能路由平台，商户可开店、发布套餐、管理用户/模型/定价，用户通过统一 API 获取可靠模型。
- **[APIKEY.FUN](https://apikey.fun/register?aff=CCSwitch)**：专业企业级 AI 中转平台，支持 Claude、OpenAI、Gemini 等主流模型，价格低至官方 7%。专属链接注册最高可永久享受充值 5% 优惠。
- **[9527CODE](https://9527.codes/register?aff=e5zI)**：企业级全能力 AI 中转平台，持续运营一年、99.9% 服务稳定性、7×24 人工技术支持。新用户可联系客服领取试用额度，推荐返现不设上限。
- **[ClaudeAPI](https://console.apito.ai/agent/register/pQBql2buaqiX3dDS)**：直接的 Claude API 接入，3 分钟连接 Claude Code 与 Agent 应用；基于 Anthropic 官方 API Key + AWS Bedrock 官方算力，保留 Tool Use、1M 上下文等官方能力。新用户可领取免费试用额度。
- **[code0.ai](https://code0.ai/agent/register/B2XHxGjGmRvqgznY)**：面向开发者的 AI 编程服务平台，支持 Claude Code、Codex、Gemini 等主流能力，帮助个人与团队稳定完成编码、调试、重构与自动化。CC Switch 用户可联系客服领取测试额度。
- **[TeamoRouter](https://teamorouter.cn/?utm_source=cc_switch&utm_medium=referral&utm_campaign=ai_directory)**：企业级 Agentic LLM 网关，无需订阅即可访问 Claude Code 等；Teamo Desktop 支持一键配置 Claude Code、Codex、Gemini CLI 等，无需管理 API Key 或手工配置网关。新用户首充 9 折。
- **[PPIO](https://ppio.com/activity/ccswitch)**：国内领先的独立 Agentic Cloud 服务商，一个 API Key 调用全模态模型；Fusion 混合模型以 Fable5 十分之一的价格达到其水平。注册并完成实名认证送 ¥10 代金券，邀请好友充值最高返 15%。
- **[new-api](https://www.newapi.ai/)**：来自 QuantumNous 的开源 AI 基础设施项目，统一 LLM 接入与分发。欢迎给 [new-api 仓库](https://github.com/QuantumNous/new-api) 点 Star 支持。
- **[ClaudeCN](https://claudecn.ai/register?aff=HEL9)**：由实体企业运营的企业级 AI 网关平台，提供 Claude、GPT、DeepSeek 等模型的高可用商业 API 接入，支持对公转账、签约合同与完整合规流程。
- **[Dola Seed（BytePlus / ModelArk）](https://www.byteplus.com/en/product/modelark?utm_campaign=hw&utm_content=ccswitch&utm_medium=devrel_tool_web&utm_source=OWO&utm_term=ccswitch)**：字节跳动自主研发、面向全球市场的全模态通用大模型 Dola Seed 2.0，支持多模态联合感知与端到端复杂任务交付，可通过 ModelArk 平台部署。注册每个模型送 50 万 tokens 免费推理额度。（[中国大陆开发者请点击这里](https://www.volcengine.com/activity/ai618?utm_campaign=hw&utm_content=hw&utm_medium=devrel_tool_web&utm_source=OWO&utm_term=ccswitch)）
- **[硅基流动（SiliconFlow）](https://cloud.siliconflow.cn/i/YflgU2Ve)**：高性能 AI 基础设施与模型 API 平台，一站式提供语言、语音、图像、视频模型。注册并完成实名认证送 ¥16 赠额；现已兼容 OpenClaw。
- **[A6API](https://a6api.com/register?aff=AqNr)**：一站式 AI 模型 API 聚合平台，覆盖 Claude、GPT、Gemini、Codex 等主流模型，多供应商可供货，通过统一接口快速接入、迁移成本低。新用户注册领免费试用额度。
- **[优云智算（Compshare）](https://www.compshare.cn/coding-plan?ytag=GPU_YY_YX_git_cc-switch)**：UCloud 旗下 AI 云平台，一个 Key 提供稳定的国内外模型 API，提供高性价比月付与按量方案，支持 Claude Code、Codex。注册送 ¥5 平台试用金。
- **[CCSub](https://www.ccsub.net/register?ref=Y6Z8DXEA)**：稳定实惠的 AI API 中转平台，Claude.ai 订阅的即插即用替代；一个 Key 访问 Claude Opus 4.8、Sonnet、Haiku、GPT、Gemini、DeepSeek，价格约为直连 API 成本的 30%，全球无需 VPN，兼容 Claude Code、Codex、Cursor、Cline、Continue、Windsurf 等。注册送 $5 额度。
- **[SSSAiCode](https://www.sssaicode.com/register?ref=DCP0SM)**：稳定可靠的 API 中转服务，专注提供稳定、可靠、实惠的 Claude 与 Codex 模型服务，当天快速开票。每次充值额外加赠 $10 额度。
- **[SoleAPI](https://soleapi.com/r/ccswitch)**：面向开发者与企业的 AI 模型网关，一个 Key 接入 Claude、GPT、Gemini 等 30+ 领先模型，原生兼容 OpenAI 与 Anthropic 协议；按延迟与上游健康实时路由，毫秒级自动故障转移，99.99% 可用性。注册领免费试用额度，推荐返现。
- **[米醋 API（Micu）](https://www.micuapi.ai/register?aff=aOYQ)**：全球 LLM 中转服务商，主打极致性价比与高稳定性，实体企业背书，支持快速官方开票。充值低至 ¥1 起、随时免手续费退款；充值输入促销码 `ccswitch` 享 9 折。
- **[Right Code](https://www.rightapi.ai/register?aff=CCSWITCH)**：为 Claude Code、Codex、Gemini 等提供稳定路由，支持按量与包月订阅；充值即可开票，企业与团队享一对一支持。每次充值额外获得相当于实付金额 5% 的按量额度。
- **[ETok.ai](https://etok.ai)**：一站式 AI 编程工具服务平台，提供专业的 Claude Code 套餐与技术社区服务，支持 Google Gemini 与 OpenAI Codex。
- **[Cubence](https://cubence.com/signup?code=CCSWITCH&source=ccs)**：可靠高效的 API 中转服务商，覆盖 Claude Code、Codex、Gemini 等，支持按量与包月。充值输入促销码 `CCSWITCH` 每次充值享 9 折。
- **[Crazyrouter](https://crazyrouter.com/register?aff=OZcm&ref=cc-switch)**：高性能 AI API 聚合平台，一个 Key 调用 Claude Code、Codex、Gemini CLI 等 300+ 模型，全部按官方价 55% 计费，支持自动故障转移、智能路由与不限并发。注册联系客服领 $2 免费额度，首充输入促销码 `CCSWITCH` 额外加赠 30%。
- **[DMXAPI](https://www.dmxapi.cn/register?aff=bUHu)**：为 200+ 企业用户提供全球大模型 API 服务，一个 Key 调用所有全球模型，支持即时开票、不限并发、低至 $0.15 起、7×24 技术支持；GPT/Claude/Gemini 全部 68 折（即 32% off），国产模型 5–8 折，Claude Code 专属模型 34 折（即 66% off）。

</details>

## 为什么选择 CC Switch？

现代 AI 编程依赖 Claude Code、Claude Desktop、Codex、Gemini CLI、Grok Build、OpenCode、OpenClaw 和 Hermes 等工具——但每个工具都有自己的配置格式。切换 API 供应商意味着手工编辑 JSON、TOML 或 `.env` 文件，而且没有统一的方式来跨多个工具管理 MCP 与 Skills。

**CC Switch** 让你用一个桌面应用管理所有受支持的 AI 工具。无需手工编辑配置文件，它提供可视化界面：一键导入供应商、即时切换，内置 50+ 供应商预设，统一管理 MCP 与 Skills，并支持系统托盘快速切换——所有数据都落在可靠的 SQLite 数据库中，配合原子写保护你的配置不被损坏。

- **一个应用，八个工具** —— 在单一界面中管理 Claude Code、Claude Desktop、Codex、Gemini CLI、Grok Build、OpenCode、OpenClaw 与 Hermes
- **不再手工编辑** —— 50+ 供应商预设，含 AWS Bedrock、NVIDIA NIM 与社区中转；选好即切
- **统一 MCP 与 Skills 管理** —— 一个面板管理 Claude、Codex、Gemini、Grok Build、OpenCode 与 Hermes 的 MCP 服务器和 Skills，支持双向同步
- **系统托盘快速切换** —— 直接从托盘菜单即时切换供应商，无需打开完整应用
- **云同步** —— 通过 Dropbox、OneDrive、iCloud 或 WebDAV 服务器跨设备同步供应商数据
- **跨平台** —— 基于 Tauri 2 构建的 Windows、macOS、Linux 原生桌面应用
- **内置实用工具** —— 包含首次启动登录确认、签名绕过、插件扩展同步等多种实用工具

## 界面预览

|                     主界面                      |                   添加供应商                   |
| :---------------------------------------------: | :--------------------------------------------: |
| ![Main Interface](assets/screenshots/main-en.png) | ![Add Provider](assets/screenshots/add-en.png) |

## 功能特性

[完整变更日志](CHANGELOG.md) | [发布说明](docs/release-notes/v3.16.1-en.md)

### 供应商管理

- **支持 8 个工具、50+ 预设** —— Claude Code、Claude Desktop、Codex、Gemini CLI、Grok Build、OpenCode、OpenClaw、Hermes；复制 Key 即可一键导入
- **通用供应商** —— 一份配置同步到 Claude Code、Codex 与 Gemini CLI
- 一键切换、系统托盘快速访问、拖拽排序、导入/导出

### 代理与故障转移

- **本地代理 + 热切换** —— 格式转换、自动故障转移、熔断、供应商健康监控与请求矫正
- **应用级接管** —— 独立代理 Claude、Codex、Gemini 或 Grok Build，粒度细到单个供应商

### MCP、Prompts 与 Skills

- **统一 MCP 面板** —— 管理 Claude、Codex、Gemini、Grok Build、OpenCode 与 Hermes 的 MCP 服务器，支持双向同步与 Deep Link 导入
- **Prompts** —— Markdown 编辑器，跨应用同步（CLAUDE.md / AGENTS.md / GEMINI.md）并带回填保护
- **Skills** —— 从 GitHub 仓库或 ZIP 文件一键安装，支持自定义仓库管理、符号链接与文件复制

### 用量与成本追踪

- **用量仪表盘** —— 通过趋势图追踪花费、请求数与 token，提供详细请求日志与按模型自定义定价

### 会话管理器与工作区

- 跨受支持的会话来源浏览、搜索并恢复对话历史
- **工作区编辑器**（OpenClaw）—— 编辑 agent 文件（AGENTS.md、SOUL.md 等），带 Markdown 预览

### 系统与平台

- **云同步** —— 自定义配置目录（Dropbox、OneDrive、iCloud、NAS）与 WebDAV 服务器同步
- **Deep Link**（`ccswitch://`）—— 通过 URL 导入供应商、MCP 服务器、Prompts 与 Skills
- 深色 / 浅色 / 跟随系统主题、自动启动、自动更新、原子写、自动备份、i18n（zh/zh-TW/en/ja）

## 常见问题

<details>
<summary><strong>CC Switch 支持哪些 AI 工具？</strong></summary>

CC Switch 支持八个工具：**Claude Code**、**Claude Desktop**、**Codex**、**Gemini CLI**、**Grok Build**、**OpenCode**、**OpenClaw** 与 **Hermes**。每个工具都有专属的供应商预设与配置管理。

</details>

<details>
<summary><strong>切换供应商后需要重启终端吗？</strong></summary>

对大多数工具来说需要——重启终端或 CLI 工具后变更才会生效。例外是 **Claude Code**，它目前支持供应商数据热切换，无需重启。

</details>

<details>
<summary><strong>切换供应商之后我的插件配置怎么不见了？</strong></summary>

CC Switch 提供「共享配置片段」功能，用于在供应商之间传递公共数据（API Key 与端点之外的内容）。进入「编辑供应商」→「共享配置面板」→ 点击「从当前供应商提取」即可保存所有公共数据。创建新供应商时勾选「写入共享配置」（默认开启），即可把插件数据带入新供应商。你的所有配置项都保留在首次启动应用时导入的默认供应商中。

</details>

<details>
<summary><strong>macOS 安装</strong></summary>

macOS 版 CC Switch 已由 Apple 代码签名并完成公证，可直接下载安装，无需额外步骤。推荐使用 `.dmg` 安装包。

</details>

<details>
<summary><strong>为什么总有一个正在激活中的供应商无法删除？</strong></summary>

CC Switch 遵循「最小侵入」设计原则——即使卸载了应用，你的 CLI 工具仍可正常工作。系统始终保留一份激活配置，因为删除全部配置会导致对应 CLI 工具不可用。如果你很少使用某个 CLI 工具，可以在设置中将其隐藏。要切回官方登录，见下一问。

</details>

<details>
<summary><strong>如何切换回官方登录？</strong></summary>

从预设列表中添加一个官方供应商。切换到它之后，走一遍登出/登录流程，随后即可在官方供应商与第三方供应商之间自由切换。Codex 支持在不同官方供应商之间切换，便于在多个 Plus 或 Team 账号之间切换。

</details>

<details>
<summary><strong>我的数据存储在哪里？</strong></summary>

- **数据库**：`~/.cc-switch/cc-switch.db`（SQLite——供应商、MCP、Prompts、Skills）
- **本地设置**：`~/.cc-switch/settings.json`（设备级 UI 偏好）
- **备份**：`~/.cc-switch/backups/`（自动轮转，保留最近 10 份）
- **Skills**：`~/.cc-switch/skills/`（默认以符号链接接入对应应用）
- **技能备份**：`~/.cc-switch/skill-backups/`（卸载前自动创建，保留最近 20 份）

</details>

<details>
<summary><strong>Linux（Wayland + NVIDIA）：点击无响应、缩放窗口时黑屏</strong></summary>

AppImage 强制使用 `GDK_BACKEND=x11`（XWayland）以规避历史上的原生 Wayland 崩溃。在较新的 Wayland + NVIDIA 环境下，这会导致网页内容区域无法点击（标题栏按钮仍可用），并在缩放时黑屏。可用这个 opt-in 逃生开关以切回原生 Wayland：

```bash
CC_SWITCH_GDK_BACKEND=wayland ./CC-Switch-*.AppImage
```

如果你从桌面图标启动，请把它加到 `.desktop` 文件的 `Exec=` 行（例如 `env CC_SWITCH_GDK_BACKEND=wayland /path/to/AppImage`），或在会话环境中设置。该变量是通用的：在点击无响应的平铺式 Wayland 合成器（sway/Hyprland）上，可改试 `CC_SWITCH_GDK_BACKEND=x11`。不设置则保持默认行为。

</details>

## 文档

关于每项功能的详细指南，请查看 **[用户手册](docs/user-manual/en/README.md)**——涵盖供应商管理、MCP/Prompts/Skills、代理与故障转移等。

## 快速开始

### 基本使用

1. **添加供应商**：点击「添加供应商」→ 选择预设或创建自定义配置
2. **切换供应商**：
   - 主界面：选择供应商 → 点击「启用」
   - 系统托盘：直接点击供应商名称（即时生效）
3. **生效**：重启终端或对应 CLI 工具以应用变更（Claude Code 无需重启）
4. **切回官方**：添加「官方登录」预设，重启 CLI 工具，然后按其登录/OAuth 流程操作

### MCP、Prompts、Skills 与会话

- **MCP**：点击「MCP」按钮 → 通过模板或自定义配置添加服务器 → 按应用切换同步
- **Prompts**：点击「Prompts」→ 用 Markdown 编辑器创建预设 → 激活后同步到实际文件
- **Skills**：点击「Skills」→ 浏览 GitHub 仓库 → 一键安装到支持的应用
- **会话**：点击「Sessions」→ 跨受支持的会话来源浏览、搜索并恢复对话历史

> **注意**：首次启动时，你可以手工将已有的 CLI 工具配置导入为默认供应商。

## 下载安装

### 系统要求

- **Windows**：Windows 10 及以上
- **macOS**：macOS 12（Monterey）及以上
- **Linux**：Ubuntu 22.04+ / Debian 11+ / Fedora 34+ 及其他主流发行版

### Windows 用户

从 [Releases](../../releases) 页面下载最新的 `CC-Switch-v{version}-Windows.msi` 安装包或 `CC-Switch-v{version}-Windows-Portable.zip` 便携版。

### macOS 用户

**方式一：通过 Homebrew 安装（推荐）**

```bash
brew install --cask cc-switch
```

更新：

```bash
brew upgrade --cask cc-switch
```

**方式二：手工下载**

从 [Releases](../../releases) 页面下载 `CC-Switch-v{version}-macOS.dmg`（推荐）或 `.zip`。

> **注意**：macOS 版 CC Switch 已由 Apple 代码签名并完成公证，可直接安装并打开。

### Arch Linux 用户

**通过 paru 安装（推荐）**

```bash
paru -S cc-switch-bin
```

### Linux 用户

从 [Releases](../../releases) 页面下载最新的 Linux 构建：

- `CC-Switch-v{version}-Linux.deb`（Debian/Ubuntu）
- `CC-Switch-v{version}-Linux.rpm`（Fedora/RHEL/openSUSE）
- `CC-Switch-v{version}-Linux.AppImage`（通用）

> **Flatpak**：官方发布未包含。你可以基于 `.deb` 自行构建——参见 [`flatpak/README.md`](flatpak/README.md)。

<details>
<summary><strong>架构总览</strong></summary>

### 设计原则

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React + TS)                    │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐    │
│  │ Components  │  │    Hooks     │  │  TanStack Query  │    │
│  │   (UI)      │──│ (Bus. Logic) │──│   (Cache/Sync)   │    │
│  └─────────────┘  └──────────────┘  └──────────────────┘    │
└────────────────────────┬────────────────────────────────────┘
                         │ Tauri IPC
┌────────────────────────▼────────────────────────────────────┐
│                  Backend (Tauri + Rust)                     │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐    │
│  │  Commands   │  │   Services   │  │  Models/Config   │    │
│  │ (API Layer) │──│ (Bus. Layer) │──│     (Data)       │    │
│  └─────────────┘  └──────────────┘  └──────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

**核心设计模式**

- **SSOT**（单一事实来源）：所有数据存储在 `~/.cc-switch/cc-switch.db`（SQLite）
- **双层存储**：可同步数据用 SQLite，设备级设置用 JSON
- **双向同步**：切换时写入实际文件，编辑激活供应商时从实际文件回填
- **原子写**：临时文件 + rename 模式，防止配置损坏
- **并发安全**：互斥锁保护数据库连接，避免竞态条件
- **分层架构**：清晰分离（Commands → Services → DAO → Database）

**关键组件**

- **ProviderService**：供应商增删改查、切换、回填、排序
- **McpService**：MCP 服务器管理、导入/导出、实际文件同步
- **ProxyService**：本地代理模式，支持热切换与格式转换
- **SessionManager**：跨受支持的会话来源浏览对话历史
- **ConfigService**：配置导入/导出、备份轮转
- **SpeedtestService**：API 端点延迟测量

</details>

<details>
<summary><strong>开发指南</strong></summary>

### 环境要求

- Node.js 18+
- pnpm 8+
- Rust 1.85+
- Tauri CLI 2.8+

### 开发命令

```bash
# 安装依赖
pnpm install

# 开发模式（热重载）
pnpm dev

# 类型检查
pnpm typecheck

# 代码格式化
pnpm format

# 检查代码格式
pnpm format:check

# 运行前端单元测试
pnpm test:unit

# 以监听模式运行测试（推荐开发时使用）
pnpm test:unit:watch

# 构建应用
pnpm build

# 构建调试版本
pnpm tauri build --debug
```

### Rust 后端开发

```bash
cd src-tauri

# 格式化 Rust 代码
cargo fmt

# 运行 clippy 检查
cargo clippy

# 运行后端测试
cargo test

# 运行特定测试
cargo test test_name

# 运行带 test-hooks feature 的测试
cargo test --features test-hooks
```

### 测试说明

**前端测试**：

- 使用 **vitest** 作为测试框架
- 使用 **MSW（Mock Service Worker）** 模拟 Tauri API 调用
- 使用 **@testing-library/react** 做组件测试

**运行测试**：

```bash
# 运行所有测试
pnpm test:unit

# 监听模式（自动重跑）
pnpm test:unit:watch

# 带覆盖率报告
pnpm test:unit --coverage
```

### 技术栈

**前端**：React 18 · TypeScript · Vite · TailwindCSS 3.4 · TanStack Query v5 · react-i18next · react-hook-form · zod · shadcn/ui · @dnd-kit

**后端**：Tauri 2.8 · Rust · serde · tokio · thiserror · tauri-plugin-updater/process/dialog/store/log

**测试**：vitest · MSW · @testing-library/react

</details>

<details>
<summary><strong>项目结构</strong></summary>

```
├── src/                        # 前端（React + TypeScript）
│   ├── components/
│   │   ├── providers/          # 供应商管理
│   │   ├── mcp/                # MCP 面板
│   │   ├── prompts/            # Prompts 管理
│   │   ├── skills/             # Skills 管理
│   │   ├── sessions/           # 会话管理器
│   │   ├── proxy/              # 代理模式面板
│   │   ├── openclaw/           # OpenClaw 配置面板
│   │   ├── settings/           # 设置（终端/备份/关于）
│   │   ├── deeplink/           # Deep Link 导入
│   │   ├── env/                # 环境变量管理
│   │   ├── universal/          # 跨应用配置
│   │   ├── usage/              # 用量统计
│   │   └── ui/                 # shadcn/ui 组件库
│   ├── hooks/                  # 自定义 hooks（业务逻辑）
│   ├── lib/
│   │   ├── api/                # Tauri API 封装（类型安全）
│   │   └── query/              # TanStack Query 配置
│   ├── i18n/                   # 国际化
│   │   └── locales/            # 翻译（zh/zh-TW/en/ja）
│   ├── config/                 # 预设（providers/mcp）
│   └── types/                  # TypeScript 类型定义
├── src-tauri/                  # 后端（Rust）
│   └── src/
│       ├── commands/           # Tauri 命令层（按领域划分）
│       ├── services/           # 业务逻辑层
│       ├── database/           # SQLite DAO 层
│       ├── proxy/              # 代理模块
│       ├── session_manager/    # 会话管理
│       ├── deeplink/           # Deep Link 处理
│       └── mcp/                # MCP 同步模块
├── tests/                      # 前端测试
└── assets/                     # 截图与合作伙伴资源
```

</details>

## 贡献

欢迎提交 issue 与建议！

提交 PR 前请确保：

- 通过类型检查：`pnpm typecheck`
- 通过格式检查：`pnpm format:check`
- 通过单元测试：`pnpm test:unit`

对于新功能，请先开 issue 讨论再提交 PR。与本项目不太契合的功能 PR 可能会被关闭。

## Star 历史

[![Star History Chart](https://api.star-history.com/svg?repos=farion1231/cc-switch&type=Date)](https://www.star-history.com/#farion1231/cc-switch&Date)

## 许可证

MIT © Jason Young
