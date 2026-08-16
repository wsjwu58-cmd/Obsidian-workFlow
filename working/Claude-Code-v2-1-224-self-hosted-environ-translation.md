---
created: 2026-08-17
updated: 2026-08-17
title: Claude Code v2.1.224 —— 自托管环境（self-hosted environments）
sourceUrl: https://github.com/anthropics/claude-code/releases/tag/v2.1.224
sourceAuthor: Anthropic（Claude Code 官方 GitHub release）
translatedAt: 2026-08-17
sources: [references/articles.md 待处理队列]
tags: [Claude Code, 发布说明, self-hosted, Remote Control, 沙箱安全, MCP, type/翻译]
---

# Claude Code v2.1.224 —— 自托管环境（self-hosted environments）

> GitHub release：`anthropics/claude-code` v2.1.224（2026-08-07 发布，正式版）
> 原文：https://github.com/anthropics/claude-code/releases/tag/v2.1.224

## 变更内容（What's changed）

- **新增** 自托管环境：`claude self-hosted-runner` 把你的机器或容器变成 Claude Code 网页端、移动端与桌面端会话可以运行的地方（Team 与 Enterprise 套餐）。
- **新增** `archive` 插件源：无需 git 或 npm，即可通过 HTTPS 从 zip 安装插件，可选用 SHA-256 固定校验。
- **新增** 移除不可用的粘贴内容会改变命令文本时，增加一个「取消-确认」步骤。
- **新增** Bedrock 环境变量 `ANTHROPIC_BEDROCK_REGION_PREFIX`：优先使用指定的跨区域推理配置，而非由 `AWS_REGION` 推导出的配置。
- **新增** `crossSessionInbound` 与 `dialogExpiry` 设置：发送给「以绕过权限模式运行」的会话的跨会话消息将被暂存、等待你的审批；发往其他会话的消息则自动投递。
- **新增** 沙箱凭据掩码选项：面向结构化 env 值的 `extract` 与 `onExtractNoMatch`、支持 JWT 感知掩码的 `decode: "jwt"` 与 `maskClaims`，以及用于 AWS SigV4 重签名的 `awsPairs`/`sigv4`；这些选项需要 `network.tlsTerminate`，且仅从 user、managed 或 `--settings` 来源的设置中生效。
- **新增** 跨会话 `SendMessage`：Claude Code 会话现在可以在你任意一台机器上互发消息，并用 `ListAgents` 发现彼此（macOS 与 Linux）。
- **修复** 超长（>200 字符）项目路径在共享的净化前缀下解析到另一项目的会话目录的问题；会话列表、重命名、fork、删除与 `/resume` 不再跨项目。
- **修复** `SendMessage` 在写入队友收件箱实际失败时仍报告「Message sent（消息已发送）」的问题；失败的投递现在会作为错误上报。
- **修复** 带尾斜杠的沙箱文件系统拒绝规则（如 `denyRead: "~/.aws/"`）在 Linux 与 macOS 上可被静默绕过的问题。
- **修复** 沙箱违规详情从不显示在 Bash 工具结果中的问题；现在 Claude 能看到哪个文件或网络访问被拒绝、以及拒绝原因。
- **修复** 回合中途连接的 MCP 工具被推迟参与工具搜索、且其名称未告知模型的问题。
- **修复** 同一插件安装在多个项目时插件安装记录被静默损坏的问题。
- **修复** 召回或恢复的粘贴内容偶尔附加错误数据、或在粘贴已过期、占位符编号冲突时静默丢失文本的问题。
- **修复** Wayland 上「选中即复制」有时无法写入剪贴板的问题；两次选择写入不再竞态。
- **修复** 长会话中反馈问卷的会话记录分享静默失败的问题；分享失败现在显示错误，而非成功消息。
- **修复** 远程控制自动启动在携带过期登录令牌冷启动时偶发「Remote credentials fetch failed（获取远程凭据失败）」的问题。
- **修复** `/clear` 等无输出命令之后，远程控制与 SDK 客户端显示空白「(no content)」消息的问题。
- **修复** 服务端会话过期后重建的远程控制会话把此前的本地对话历史上传进新会话的问题。
- **改进** 全屏模式：在反复上下文压缩之后，于回滚缓冲区中保留压缩前的完整历史，而不再只保留最近一段。
- **改进** 远程控制：连接的网页端与移动端现在能看到压缩进度与压缩后的边界，而非静默暂停；`/clear` 重置现在会传播到已连接的客户端。
- **改进** 远程控制：连接失败现在显示带详情与重连快捷键的持续失败指示，而不再只有 8 秒 toast。
- **移除** 每会话 200 个子代理的生成上限；长时间运行的会话不再拒绝新 agent（并发与深度限制仍然生效）。
- **变更** 托管设置：组织设置未变化时，重新登录或切换组织之后不再重复弹出审批提示。
- **变更** 反馈问卷的会话记录分享：经你同意后，现在还会上传最近一次请求的模型设置——系统提示词（包含你的 `CLAUDE.md` 指令）、工具定义与模型参数。秘密仍照旧脱敏；若分享内容过大，这些字段会被优先丢弃。
- **变更** Bash 工具描述：始终注明命令输出会展示给模型，而非可靠地展示给用户。
- **变更** 召回的粘贴占位符编号在接受进输入时会重新编号。
- **变更** 远程控制：上下文压缩或 `/resume` 之后创建新会话时，把过期的服务端会话归档，而非在列表中留下一个失效会话。
- **[VSCode] 修复** 连接失败后扩展仍把远程控制显示为「已连接」的问题。
- **修复** 用户关闭远程控制后，恢复会话仍会静默重连远程控制的问题（`--resume`、SDK 宿主与 VS Code 扩展）。
- **[VSCode] 修复** 显式启用时，会话不遵守 `remoteControlAtStartup` 的问题。

## 译注

- **self-hosted environments（自托管环境）**：本次版本的头条特性。`claude self-hosted-runner` 把用户自有机器/容器注册为运行场所，让 Claude Code 各端会话脱离 Anthropic 托管环境执行；限 Team / Enterprise 套餐。
- **`network.tlsTerminate`**：沙箱凭据掩码（`extract`/`decode: "jwt"`/`awsPairs`/`sigv4` 等）生效的前置条件——需要 TLS 终止才能看到待掩码的明文值。
- **compaction（上下文压缩）**：Claude Code 长会话把早期历史压缩为摘要的机制；本版让全屏模式在反复压缩后仍保留压缩前完整历史。
- **toast**：短暂出现的轻量通知；「8 秒 toast」按原文保留为时间量词。
- **subagent spawn cap（子代理生成上限）**：原每会话最多生成 200 个子代理，本版移除该上限，但并发与深度限制不变。
- **`dialogExpiry`**：控制跨会话消息在暂存等待审批后的投递/过期行为，不直译为「对话框过期」。
