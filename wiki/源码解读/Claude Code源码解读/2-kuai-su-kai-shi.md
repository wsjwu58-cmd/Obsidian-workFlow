# 2-kuai-su-kai-shi
Claude Code (CCB) 是一个运行在终端中的 agentic coding system，它不是简单的聊天机器人——而是一个拥有完整 shell 访问权限、能够自主决策并执行工具链的 AI 编程助手。通过阅读本文档，你将在 5 分钟内完成环境搭建、配置认证并开始第一次对话。

Sources: [README.md](#root/C5RFhwbv9QOi), [docs/introduction/what-is-claude-code.mdx](#root/5Dg7mXbPSaxO)

## 系统架构概览

Claude Code 采用五层架构设计，从用户交互到基础设施层层递进。理解这个架构有助于你在后续开发中快速定位问题和扩展功能。

```
graph TB
    subgraph "交互层"
        A[REPL.tsx<br/>React/Ink TUI] --> B[用户输入处理]
    end
    
    subgraph "编排层"
        C[QueryEngine.ts<br/>会话状态管理] --> D[成本追踪]
        C --> E[Transcript 持久化]
    end
    
    subgraph "核心循环层"
        F[query.ts<br/>Agentic Loop] --> G[上下文预处理]
        F --> H[流式 API 调用]
        F --> I[工具执行]
        F --> J[终止/继续判定]
    end
    
    subgraph "工具层"
        K[tools.ts<br/>50+ 工具库] --> L[文件读写]
        K --> M[Bash 执行]
        K --> N[MCP 集成]
    end
    
    subgraph "通信层"
        O[claude.ts<br/>流式通信] --> P[Anthropic API]
        O --> Q[AWS Bedrock]
        O --> R[Vertex AI]
        O --> S[Azure]
    end
    
    A --> C
    C --> F
    F --> K
    K --> O
```

每层职责清晰、边界分明。交互层负责终端 UI 和用户输入，编排层管理会话状态和成本追踪，核心循环层实现 Agentic Loop 的单轮迭代，工具层提供 50+ 内置工具，通信层支持多种云服务提供商的流式 API 调用。

Sources: [docs/introduction/architecture-overview.mdx](#root/hfBWUsFGsCUu)

## 环境要求

Claude Code 依赖 Bun 运行时作为核心依赖，这是其高性能和快速启动的基础。务必使用最新版本的 Bun，旧版本会导致一系列奇怪的错误。

| 组件 | 最低版本 | 推荐版本 | 说明 |
| --- | --- | --- | --- |
| Bun | 1.2.0+ | 1.3.11+ | 必须最新版本，运行 `bun upgrade` 更新 |
| Node.js | 兼容 | 18+ | 构建产物支持 Node.js 运行 |
| Git | \- | 最新版 | 用于代码仓库操作 |
| 终端 | \- | \- | 支持 ANSI 转义序列的现代终端 |

**升级 Bun**：

```
bun upgrade
```

Sources: [README.md](#root/hQFkPEAIoKyZ), [package.json](#root/OPZ276YY6KTx)

## 安装步骤

安装过程分为依赖安装和构建产物生成两个阶段。国内用户如果网络环境较差，可以通过环境变量配置 GitHub 代理。

### 基础安装

```
# 1. 安装项目依赖
bun install

# 2. 国内网络优化（可选）
# 设置 ripgrep 下载源代理
DEFAULT_RELEASE_BASE=https://ghproxy.net/https://github.com/microsoft/ripgrep-prebuilt/releases/download/v15.0.1 bun install
```

### 构建与验证

```
# 开发模式运行（推荐首次使用）
bun run dev

# 构建生产版本
bun run build
```

构建采用 code splitting 多文件打包，产物输出到 `dist/` 目录，包含入口 `dist/cli.js` 和约 450 个 chunk 文件。构建出的版本同时支持 Bun 和 Node.js 启动，可以直接发布到私有源。

**验证安装成功**：运行 `bun run dev` 后看到版本号 `888` 或版本号信息即表示配置正确。

Sources: [README.md](#root/Nc8Cy3r0z0zM), [build.ts](#root/uiYrPI6WNyLs)

## 首次配置

首次运行 Claude Code 后，需要进行 API 认证配置。CCB 支持多种认证方式，包括 Anthropic 官方账号、自定义平台以及 OpenAI 兼容服务。

### /login 配置流程

在 REPL 中输入 `/login` 命令进入登录配置界面，选择 **Custom Platform** 即可对接第三方 API 兼容服务（无需 Anthropic 官方账号）。

**配置字段**：

| 字段 | 说明 | 示例 | 必填 |
| --- | --- | --- | --- |
| Base URL | API 服务地址 | `https://api.example.com/v1` | 是 |
| API Key | 认证密钥 | `sk-xxx` | 是 |
| Haiku Model | 快速模型 ID | `claude-haiku-4-5-20251001` | 否 |
| Sonnet Model | 均衡模型 ID | `claude-sonnet-4-6` | 否 |
| Opus Model | 高性能模型 ID | `claude-opus-4-6` | 否 |

**交互操作**：

*   **Tab / Shift+Tab**：在字段间切换
*   **Enter**：确认并跳到下一个字段
*   最后一个字段按 Enter：保存配置

配置保存到 `~/.claude/settings.json` 的 `env` 字段，保存后立即生效。

Sources: [src/commands/login/login.tsx](#root/QMzdvBwTdcbs)

### 手动配置文件

你也可以直接编辑 `~/.claude/settings.json` 文件进行配置：

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.example.com/v1",
    "ANTHROPIC_AUTH_TOKEN": "sk-xxx",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "claude-haiku-4-5-20251001",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "claude-sonnet-4-6",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "claude-opus-4-6"
  }
}
```

**支持的认证方式**：

*   Anthropic 官方 API
*   OpenRouter、AWS Bedrock 代理等兼容服务
*   OpenAI 协议兼容层（Ollama、DeepSeek、vLLM、One API 等）

Sources: [docs/plans/openai-compatibility.md](#root/gUFUpH1bC9sJ)

## 基本使用

完成配置后，你就可以开始与 Claude Code 交互了。Claude Code 的独特之处在于它不是简单的问答系统，而是一个能够自主执行工具链的 agentic system。

### 启动 Claude Code

```
# 开发模式启动
bun run dev

# 构建版本启动（需要先执行 bun run build）
node dist/cli.js

# 直接使用安装的命令
ccb
# 或
claude-code-best
```

### 第一次对话

在 REPL 提示符下，输入自然语言描述你的需求：

```
> 帮我查看当前目录结构
> 读取 package.json 文件
> 运行测试并修复报错
```

Claude Code 会自动执行以下步骤：

1.  理解你的需求
2.  选择合适的工具（如 `BashTool`、`FileReadTool`）
3.  执行工具调用
4.  将结果返回给你
5.  根据结果决定下一步操作

### 常用命令

| 命令 | 功能 | 说明 |
| --- | --- | --- |
| `/login` | 配置认证 | 设置 API 密钥和服务地址 |
| `/logout` | 退出登录 | 清除当前认证信息 |
| `/model` | 切换模型 | 在 Haiku/Sonnet/Opus 之间切换 |
| `/config` | 查看配置 | 显示当前配置信息 |
| `/help` | 帮助文档 | 显示所有可用命令 |
| `/exit` 或 `Ctrl+D` | 退出程序 | 关闭 Claude Code |

### 典型工作流示例

```
flowchart LR
    A[用户输入需求] --> B[QueryEngine 接收请求]
    B --> C[构建上下文]
    C --> D[调用 API 获取响应]
    D --> E{包含工具调用?}
    E -->|是| F[执行工具]
    E -->|否| G[直接返回结果]
    F --> H{需要后续操作?}
    H -->|是| C
    H -->|否| G
    G --> I[展示结果给用户]
```

**场景示例：修复 TypeScript 报错**

1.  输入：`bun run dev 有个 TypeScript 报错，帮我修一下`
2.  Claude Code 自动执行：
    *   `Bash("bun run dev 2>&1 | head -30")` 查看报错信息
    *   `Read("src/utils/foo.ts")` 读取源代码
    *   `Grep("interface Foo", "src/")` 搜索相关类型定义
    *   `FileEdit(old, new)` 修复代码
    *   `Bash("bun run dev 2>&1 | head -10")` 验证修复

Sources: [src/entrypoints/cli.tsx](#root/i2EzLOYQMrRZ), [src/main.tsx](#root/ES0g3Nyeb4qi)

## Feature Flags 功能开关

Claude Code 通过 Feature Flags 实现构建时特性门控，提供了 88+ 个功能开关。这些开关可以通过环境变量启用，允许你按需启用高级功能。

### 启用 Feature Flags

所有功能开关通过 `FEATURE_<FLAG_NAME>=1` 环境变量启用：

```
# 启用 Buddy AI 伴侣
FEATURE_BUDDY=1 bun run dev

# 启用多个功能
FEATURE_BUDDY=1 FEATURE_FORK_SUBAGENT=1 FEATURE_VOICE_MODE=1 bun run dev

# 在 package.json 脚本中设置
"scripts": {
  "dev:buddy": "FEATURE_BUDDY=1 bun run dev",
  "dev:full": "FEATURE_BUDDY=1 FEATURE_VOICE_MODE=1 FEATURE_PROACTIVE=1 bun run dev"
}
```

### 默认启用的 Feature Flags

开发模式默认启用的功能包括：

| Flag | 功能 | 说明 |
| --- | --- | --- |
| `BUDDY` | AI 伴侣 | 可爱的 AI 吉祥物，陪伴你编程 |
| `TRANSCRIPT_CLASSIFIER` | 对话分类 | 自动识别对话内容类型 |
| `BRIDGE_MODE` | 桥接模式 | 支持远程控制和多端同步 |
| `AGENT_TRIGGERS_REMOTE` | 远程触发 | 支持远程触发子任务 |
| `CHICAGO_MCP` | MCP 集成 | 支持 Model Context Protocol |
| `VOICE_MODE` | 语音模式 | 支持语音输入和交互 |

### Feature Flags 分类

Claude Code 的 88+ 个功能开关分为六大类别：

| 类别 | 数量 | 代表 Flag | 说明 |
| --- | --- | --- | --- |
| Agent/自动化 | 15 | `PROACTIVE`, `KAIROS`, `COORDINATOR_MODE` | 控制 AI 的自主能力边界 |
| 基础设施 | 10 | `DAEMON`, `BRIDGE_MODE`, `SSH_REMOTE` | 控制运行环境和连接方式 |
| 安全/分类 | 6 | `BASH_CLASSIFIER`, `TREE_SITTER_BASH` | 增强权限判断的智能性 |
| 工具/能力 | 10 | `WEB_BROWSER_TOOL`, `VOICE_MODE` | 新增的 AI 能力 |
| UI/体验 | 8 | `MESSAGE_ACTIONS`, `QUICK_SEARCH` | 界面和交互改进 |
| 平台/实验 | 10+ | `ULTRAPLAN`, `ULTRATHINK` | 实验性和平台级功能 |

Sources: [docs/internals/feature-flags.mdx](#root/j6pOYn7hEifa), [scripts/dev.ts](#root/iP96NVqvf20W)

## 项目结构预览

了解项目结构有助于你在后续开发中快速定位代码。Claude Code 采用 monorepo 结构，核心代码在 `src/` 目录下。

```
claude-code/
├── src/                          # 核心源码
│   ├── entrypoints/              # 入口文件
│   │   └── cli.tsx              # CLI 主入口
│   ├── screens/                  # UI 屏幕组件
│   │   └── REPL.tsx             # 主交互界面
│   ├── QueryEngine.ts            # 查询引擎（编排层）
│   ├── query.ts                  # Agentic Loop（核心循环）
│   ├── tools/                    # 工具实现
│   │   ├── BashTool/            # Bash 命令执行
│   │   ├── FileEditTool/        # 文件编辑
│   │   └── ...
│   ├── services/                 # 服务层
│   │   ├── api/                 # API 通信
│   │   ├── mcp/                 # MCP 协议
│   │   └── analytics/           # 分析和遥测
│   ├── commands/                 # 斜杠命令
│   │   ├── login/               # 登录配置
│   │   ├── model/               # 模型切换
│   │   └── ...
│   └── utils/                    # 工具函数
├── docs/                         # 文档目录
├── packages/                     # 子包
│   └── @ant/                     # Ant 生态工具
├── tests/                        # 测试文件
└── dist/                         # 构建产物
```

Sources: [README.md](#root/C5RFhwbv9QOi), [build.ts](#root/uiYrPI6WNyLs)

## 下一步

完成快速开始后，建议按照以下学习路径深入了解 Claude Code 的各项功能：

1.  **[环境要求与安装](3-huan-jing-yao-qiu-yu-an-zhuang.md)** - 详细的环境配置说明，包括特殊场景的处理方案
2.  **[登录与平台配置](4-deng-lu-yu-ping-tai-pei-zhi.md)** - 深入了解认证机制和多平台配置
3.  **[五层架构设计](6-wu-ceng-jia-gou-she-ji.md)** - 系统性地学习架构设计原理
4.  **[Agentic Loop 核心循环](7-agentic-loop-he-xin-xun-huan.md)** - 理解 AI 自主决策和工具调用机制
5.  **[工具系统架构](10-gong-ju-xi-tong-jia-gou.md)** - 学习如何使用和扩展工具系统

通过循序渐进的学习，你将全面掌握 Claude Code 的核心概念和高级用法，成为一名高效的 AI 辅助编程专家。

## 相关条目
- [[1-xiang-mu-gai-lan]]
- [[3-huan-jing-yao-qiu-yu-an-zhuang]]
