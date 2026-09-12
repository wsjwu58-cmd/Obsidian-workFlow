---
created: 2026-09-12
updated: 2026-09-12
type: prompt-draft
status: 过程稿
sources:
  - url: https://github.com/farion1231/cc-switch
tags: [CC Switch, 翻译, prompt, GitHub README]
---

# 02 本次翻译使用的提示词（过程稿）

> 本次翻译用如下提示词驱动。原文（英文 README）已抓取到
> `candidates/20260912-080217/sources/farion1231-cc-switch---A-cross-platform.md`
> （GitHub API `repos/farion1231/cc-switch/readme` raw 取得权威正文，仓库元数据取
> `repos/farion1231/cc-switch`，最新版本取 `releases/latest`；完整原始抓取另存同目录
> `farion1231-cc-switch---A-cross-platform-full.md`）。

## 提示词正文

```
你是一名资深技术译者（英→中），翻译 GitHub 开源仓库 farion1231/cc-switch 的主 README
（标题：The All-in-One Manager for Claude Code, Claude Desktop, Codex, Gemini CLI,
Grok Build, OpenCode, OpenClaw & Hermes Agent）。

## 输入
- 原文：candidates/20260912-080217/sources/farion1231-cc-switch---A-cross-platform.md
  （正文从 "# CC Switch" 开始；忽略文件头部的采集元信息块）。
- 官方简体中文版 README_ZH.md 可作为术语/专有名词对照，但译文必须以英文 README 为唯一来源，
  不得整段搬运中文版。
- 仓库元数据（2026-09-12）：stars 132,370 / forks 9,129 / open issues 2,663 /
  subscribers 250，主语言 Rust，许可证 MIT，仓库创建 2025-08-04，默认分支 main，
  最新 release v3.20.3（2026-09-11）。

## 输出要求
1. 完整逐译核心正文：官网标语、Why CC Switch?（含 7 条要点）、Screenshots 表格、
   Features 全部 6 组（Provider Management / Proxy & Failover / MCP, Prompts & Skills /
   Usage & Cost Tracking / Session Manager & Workspace / System & Platform）、
   FAQ 全部 8 条（含 Linux Wayland+NVIDIA 的 bash 代码块）、Documentation、Quick Start
   （Basic Usage + MCP/Prompts/Skills & Sessions）、Download & Installation
   （System Requirements 与 Windows/macOS/Arch Linux/Linux 全部命令）、
   Architecture Overview（Design Principles + Key Components）、Development Guide
   （Environment Requirements + 全部命令 + Testing Guide + Tech Stack）、
   Project Structure（保留 ASCII 目录树与 # 注释的翻译）、Contributing、
   Star History、License。
2. 顶部 <picture>/<div align="center"> logo、shields.io 徽章（Version / Platform /
   Built with Tauri / Downloads）、Trendshift 与 Star History badge 的 HTML 原样保留；
   语言导航行 "English | [中文](README_ZH.md) | [日本語](README_JA.md) | [Deutsch](README_DE.md) | [Changelog](CHANGELOG.md)"
   原样保留。
3. 赞助商区块（## ❤️Sponsor，32 行）：这是 affiliate 广告，逐字翻译无知识增量。
   压缩为一行式中文简介表格，但每个赞助商名称、可点击链接、关键促销码/折扣必须保留；
   在本节开头标注「本节为原文赞助商广告的压缩摘译，完整原文见 sources 抓取文件」。
4. 保留原文全部超链接（Markdown 写法沿用，链接文字译为中文）；
   代码、命令、路径、标识符原样保留：brew install --cask cc-switch、
   paru -S cc-switch-bin、pnpm dev / pnpm typecheck / pnpm format:check / pnpm test:unit、
   cargo fmt / cargo clippy / cargo test --features test-hooks、
   CC_SWITCH_GDK_BACKEND=wayland、ccswitch://、~/.cc-switch/cc-switch.db、AGENTS.md、SOUL.md、
   CLAUDE.md、GEMINI.md、TanStack Query、shadcn/ui、@dnd-kit、vitest、MSW、
   @testing-library/react、tauri-plugin-updater/process/dialog/store/log 等。
5. 术语表（必须一致）：
   - provider → 供应商
   - relay → 中转
   - failover → 故障转移
   - circuit breaker → 熔断
   - hot-switching → 热切换
   - request rectifier → 请求矫正
   - preset → 预设
   - shared config snippet → 共享配置片段
   - backfill → 回填
   - atomic writes → 原子写
   - SSOT (Single Source of Truth) → 单一事实来源
   - health monitoring → 健康监控
   - session manager → 会话管理器
   - workspace → 工作区
   - Deep Link → 深度链接（保留 ccswitch://）
   - Skills → Skills（技能，首现可注）
   - Claude Code / Claude Desktop / Codex / Gemini CLI / Grok Build / OpenCode /
     OpenClaw / Hermes Agent / Tauri / Rust / SQLite / MCP / WebDAV 保留原文
6. 数字与结论逐一比对原文，不得改动：8 个支持工具、50+ 供应商预设、
   Features 6 组、FAQ 8 条、备份保留 10 份、技能备份保留 20 份、
   i18n（zh/zh-TW/en/ja）、Node 18+ / pnpm 8+ / Rust 1.85+ / Tauri CLI 2.8+、
   最新版本 v3.20.3。
7. 中文表达通顺自然，术语到位；输出 Markdown，标题层级沿用原文；frontmatter（过程稿）：
   ---
   created: 2026-09-12
   updated: 2026-09-12
   type: translation-draft
   status: 过程稿
   sources:
     - title: farion1231/cc-switch - A cross-platform desktop All-in-One assistant for Claude Code, Codex, OpenCode, OpenClaw, Grok Build & Hermes Agent
       url: https://github.com/farion1231/cc-switch
       source: github
       date: 2026-09-06
   tags: [CC Switch, Claude Code, Codex, Tauri, Rust, Provider 管理, MCP, Skills, 桌面应用, 翻译]
   ---
```

## 执行备注

- 抓取方式：GitHub API `repos/farion1231/cc-switch/readme`（raw）取得权威正文；
  `repos/farion1231/cc-switch` 取 stars/forks/issues/license/language/created_at 等元数据；
  `releases/latest` 取版本 v3.20.3 与发布时间。
- 翻译策略：核心正文完整逐译 + 赞助商区块压缩摘译（保留链接与促销码）；
  「Why CC Switch?」「Features」「FAQ」等小节结构与英文版一致。
- 关键数字比对：stars 132,370 / forks 9,129 / open issues 2,663 / subscribers 250 已抽查与
  GitHub API 一致，属 2026-09-12 时点值；README 正文自身的可核验数字（8 工具 / 50+ 预设 /
  10 份备份 / 20 份技能备份 / i18n 四语 / v3.20.3）逐条回查原文。
- 该提示词本身不直接沉淀进 prompts/（curate 产出边界：不写 prompts/），
  留待评审通过、实测后再考虑复用。
