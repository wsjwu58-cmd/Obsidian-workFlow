# 3-huan-jing-yao-qiu-yu-an-zhuang
CCB (踩踩背) 是一个基于 Bun 运行时的交互式 AI 编程助手 CLI 工具。本文档详细介绍系统环境要求、多种安装方式、配置方法以及常见问题排查，帮助初学者快速搭建开发环境。

## 系统环境要求

### 运行时环境

CCB 基于 Bun 运行时构建，这是其核心运行环境要求。Bun 是一个高性能的 JavaScript/TypeScript 运行时，与 Node.js 兼容但速度更快。项目明确要求使用 Bun 的最新版本，以确保所有功能正常工作。

**最低版本要求：** Bun >= 1.3.11

Sources: [package.json](#root/662vkSWUepE4)

由于 Bun 版本更新频繁，旧版本可能导致各种奇怪的错误，因此在安装前强烈建议执行 `bun upgrade` 升级到最新版本。这是 README 中反复强调的重要前置步骤。

Sources: [README.md](#root/HrYoJ9KYtuBX)

### 操作系统支持

CCB 支持三大主流操作系统平台，并提供原生二进制适配：

*   **Windows**: 支持 x64 和 ARM64 架构
*   **macOS**: 支持 Apple Silicon (arm64) 和 Intel (x64) 架构
*   **Linux**: 支持 x64 和 ARM64 架构，包含 musl 和 glibc 两种链接方式

Sources: [scripts/download-ripgrep.ts](#root/qggKJdOmPjAb)

不同平台的 ripgrep 二进制文件会自动下载，无需手动配置。下载脚本会根据 `process.platform` 和 `process.arch` 自动选择正确的二进制版本。

Sources: [scripts/download-ripgrep.ts](#root/d12mYxKarWIS)

### 外部依赖

项目依赖几个关键的第三方工具和库：

1.  **ripgrep (rg)**: 高性能代码搜索工具，版本 15.0.1
    *   自动通过 GitHub Releases 下载
    *   支持国内镜像代理
    *   存放在 `src/utils/vendor/ripgrep/` 或 `dist/vendor/ripgrep/` 目录

Sources: [scripts/download-ripgrep.ts](#root/D8Pr8jmDxt9e)

1.  **TypeScript**: 类型系统支持，配置为 ESNext 目标 Sources: [tsconfig.json](#root/deoKkoa4NwOd)
2.  **React 19**: 用于构建 UI 组件，采用 React 19.2.4 版本 Sources: [package.json](#root/xAdxLVG629Qr)

### 原生模块依赖

CCB 使用了多个 N-API 原生模块，这些模块通过 Bun 的 FFI 机制或原生绑定实现高性能操作：

*   `audio-capture-napi`: 音频捕获功能
*   `color-diff-napi`: 颜色差异计算
*   `image-processor-napi`: 图像处理
*   `modifiers-napi`: 修饰符处理
*   `url-handler-napi`: URL 处理

Sources: [packages](#root/D8DdAXcTeoE3)

这些原生模块作为 workspace 包管理，在 `bun install` 时会自动处理其依赖关系。

Sources: [package.json](#root/cuErbeRY56ZW)

## 安装方式

### 标准安装流程

CCB 提供了简化的安装流程，适用于大多数开发场景。整个安装过程包含依赖安装、构建和启动三个核心步骤：

```
flowchart TD
    A[开始安装] --> B{检查 Bun 版本}
    B -->|版本 >= 1.3.11| C[bun install]
    B -->|版本过旧| B2[bun upgrade<br/>然后回到 C]
    C --> D[下载原生依赖]
    D --> E[自动下载 ripgrep]
    E --> F{网络环境检查}
    F -->|国外网络直接下载| G[完成安装]
    F -->|国内网络| H[设置镜像代理<br/>RIPGREP_DOWNLOAD_BASE]
    H --> G
    G --> I[bun run build<br/>可选，生产环境构建]
    I --> J[bun run dev<br/>启动开发模式]
```

**步骤 1: 安装依赖**

```
bun install
```

这个命令会：

*   安装所有 npm 包依赖
*   自动触发 postinstall 钩子
*   下载平台对应的 ripgrep 二进制文件
*   构建原生 N-API 模块

Sources: [package.json](#root/6xBf8AusCMAC)

**步骤 2:（可选）构建生产版本**

```
bun run build
```

构建系统采用 Bun 的 code splitting 功能，将代码分割为约 450 个 chunk 文件，输出到 `dist/` 目录。构建产物兼容 Bun 和 Node.js 两种运行时。

Sources: [build.ts](#root/zRqEagTJqYYL) [README.md](#root/KXLOG5J28Ad1)

**步骤 3: 启动开发模式**

```
bun run dev
```

开发模式会直接运行 TypeScript 源码，无需构建步骤。如果看到版本号 888，说明启动成功。

Sources: [README.md](#root/72gFAtE4Uzvz)

### 国内网络环境配置

针对国内 GitHub 访问较慢的问题，项目提供了镜像代理配置方案。通过设置环境变量，可以将 ripgrep 的下载重定向到国内镜像服务。

```
# 使用 ghproxy 镜像
export RIPGREP_DOWNLOAD_BASE="https://ghproxy.net/https://github.com/microsoft/ripgrep-prebuilt/releases/download/v15.0.1"

# 然后执行安装
bun install
```

Sources: [README.md](#root/2ZEIR9xsuO3L)

下载脚本内置了多种下载方式（PowerShell、curl、fetch），会根据平台和环境自动选择最合适的方案，并在 Windows 环境下提供回退机制以确保下载成功。

Sources: [scripts/download-ripgrep.ts](#root/RgD6ZEjL1kQt)

### Windows 快速启动

Windows 用户可以直接使用提供的 PowerShell 脚本快速启动：

```powershell
.\Run.ps1
```

该脚本会自动执行 `bun install` 并以 `--dangerously-skip-permissions` 模式启动开发环境，适用于快速验证和开发调试。

Sources: [Run.ps1](#root/kPITB6unczti)

## 功能配置

### Feature Flags 机制

CCB 采用环境变量驱动的 Feature Flags 系统来控制功能开关。所有功能通过 `FEATURE_<FLAG_NAME>=1` 格式的环境变量启用，这种设计允许用户灵活启用或禁用特定功能。

Sources: [build.ts](#root/qBdKai4cwPHI)

**常用 Feature Flags 示例：**

| Feature Flag | 说明 | 用途 |
| --- | --- | --- |
| `FEATURE_BUDDY=1` | 启用 Buddy 小宠物 | 陪伴式编程助手 |
| `FEATURE_FORK_SUBAGENT=1` | 启用子 Agent 分叉 | 并行任务处理 |
| `FEATURE_AUTO_MODE=1` | 启用自动模式 | 减少 API 调用确认 |
| `FEATURE_VOICE_MODE=1` | 启用语音模式 | 语音输入交互 |

**启用多个功能的示例：**

```
FEATURE_BUDDY=1 FEATURE_FORK_SUBAGENT=1 FEATURE_VOICE_MODE=1 bun run dev
```

Sources: [README.md](#root/UOCOtRbomTZM)

默认构建包含三个核心功能：`AGENT_TRIGGERS_REMOTE`、`CHICAGO_MCP`、`VOICE_MODE`，这些功能始终启用，无需额外配置。

Sources: [build.ts](#root/QEikGCOykUYv)

详细的 Feature 文档位于 `docs/features/` 目录，每个功能都有独立的说明文档，欢迎社区贡献。

Sources: [docs/features](#root/TDqJFoDAt3ho)

### API 平台配置

CCB 支持多种 API 提供商，不局限于 Anthropic 官方 API。用户可以通过 `/login` 命令或直接编辑配置文件对接第三方 API 兼容服务。

Sources: [README.md](#root/Eu4YxfJqGEVG)

**配置方式一：交互式登录**

在 REPL 模式下输入 `/login` 命令，选择 **Custom Platform** 模式：

| 字段 | 说明 | 示例 |
| --- | --- | --- |
| Base URL | API 服务地址 | `https://api.example.com/v1` |
| API Key | 认证密钥 | `sk-xxx` |
| Haiku Model | 快速模型 ID | `claude-haiku-4-5-20251001` |
| Sonnet Model | 均衡模型 ID | `claude-sonnet-4-6` |
| Opus Model | 高性能模型 ID | `claude-opus-4-6` |

使用 Tab/Shift+Tab 切换字段，Enter 确认并跳转到最后一个字段保存。

Sources: [README.md](#root/FKY67iPDyQOL)

**配置方式二：直接编辑配置文件**

配置文件路径：`~/.claude/settings.json`

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

Sources: [README.md](#root/dSDHM4EebEiv)

CCB 支持所有兼容 Anthropic Messages API 的服务，包括 OpenRouter、AWS Bedrock 代理等。

Sources: [README.md](#root/NBVA33pfZLca)

## 构建与部署

### 开发模式 vs 生产模式

CCB 提供两种运行模式，分别适用于不同的开发阶段：

| 模式 | 命令 | 特点 | 适用场景 |
| --- | --- | --- | --- |
| 开发模式 | `bun run dev` | 直接运行 TS 源码，支持热重载 | 日常开发调试 |
| 开发调试 | `bun run dev:inspect` | 启用 Inspector 调试端口 | VS Code 调试 |
| 生产模式 | `bun run build` | 代码分割打包，输出 JS 文件 | 生产部署 |

Sources: [package.json](#root/XsLEkQjVALuw)

### 构建输出说明

构建系统输出约 450 个 chunk 文件到 `dist/` 目录：

```
dist/
├── cli.js                 # 入口文件
├── download-ripgrep.js    # ripgrep 下载脚本
├── vendor/ripgrep/        # ripgrep 二进制文件
│   ├── x64-win32/rg.exe
│   └── arm64-win32/rg.exe
├── chunk-xxx.js          # 450+ 个分割后的模块
└── ...
```

Sources: [build.ts](#root/nG1K9qIjhvMn) [build.ts](#root/SSw2OUkKpYRw)

构建产物经过 Node.js 兼容性处理，可以在 Bun 和 Node.js 两种运行时下直接执行。这使得项目可以发布到私有 npm 仓库供其他项目使用。

Sources: [build.ts](#root/JA8eKyu9VIya)

### VS Code 调试配置

由于 REPL 模式需要真实终端环境，无法直接通过 VS Code launch 配置启动调试。推荐使用 attach 模式：

```
flowchart LR
    A[VS Code] -->|1. 配置 launch.json| B[启动调试会话]
    C[终端] -->|2. 运行 bun run dev:inspect| D[Inspector 服务<br/>localhost:9229]
    D -->|3. VS Code attach| E[断点调试]
    E -->|4. 步骤执行| F[查看变量<br/>调用堆栈]
```

**步骤：**

1.  在终端启动 inspector 服务：`bun run dev:inspect`
2.  配置 VS Code `launch.json`：

```json
{
  "type": "node",
  "request": "attach",
  "name": "Attach to Bun Inspector",
  "port": 9229,
  "restart": true,
  "localRoot": "${workspaceFolder}",
  "remoteRoot": "${workspaceFolder}"
}
```

1.  在 VS Code 中按 F5 启动调试会话

Sources: [README.md](#root/QF0YraU371K5)

### 健康度检查

项目提供了健康度检查脚本，用于评估代码质量：

```
bun run health
```

检查内容包括：

*   代码规模（文件数、代码行数）
*   Lint 问题数（Biome）
*   测试结果（Bun test）
*   冗余代码（Knip）
*   构建状态

Sources: [scripts/health-check.ts](#root/2wTC9Jmhgen4)

## 常见问题排查

### Bun 版本问题

**症状：** 各种奇怪的运行时错误、依赖安装失败

**解决方案：**

```
bun upgrade
```

确保 Bun 版本 >= 1.3.11。旧版本 Bun 存在已知的兼容性问题，会导致各种不可预测的错误。

Sources: [package.json](#root/662vkSWUepE4) [README.md](#root/HrYoJ9KYtuBX)

### ripgrep 下载失败

**症状：** postinstall 阶段报错，ripgrep 二进制未找到

**解决方案：**

```
# 方案 1: 使用国内镜像
export RIPGREP_DOWNLOAD_BASE="https://ghproxy.net/https://github.com/microsoft/ripgrep-prebuilt/releases/download/v15.0.1"

# 方案 2: 设置 HTTP 代理
export HTTPS_PROXY="http://proxy.example.com:8080"

# 方案 3: 手动下载并重新安装
bun run scripts/download-ripgrep.ts --force
```

下载脚本内置了 PowerShell、curl、fetch 三种下载方式，会自动选择最可靠的方案。在 Windows 环境下，即使 Bun fetch 失败，也会尝试通过 PowerShell 或 curl 下载。

Sources: [scripts/download-ripgrep.ts](#root/nVQEQH97csKU)

### 构建错误

**症状：** `bun run build` 失败，TypeScript 编译错误

**解决方案：**

```
# 1. 清理构建缓存
rm -rf dist/
rm -rf node_modules/.bun/

# 2. 重新安装依赖
bun install

# 3. 执行构建
bun run build
```

如果仍有错误，检查 TypeScript 配置和依赖版本兼容性。

Sources: [build.ts](#root/NfTcrfgpgoLI) [package.json](#root/B2mfjD8CqwfR)

### 权限问题（Windows）

**症状：** Windows 环境下脚本执行权限错误

**解决方案：**

使用项目提供的 PowerShell 脚本：

```powershell
# 以管理员身份运行 PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 或使用项目提供的 Run.ps1
.\Run.ps1
```

`Run.ps1` 使用 `--dangerously-skip-permissions` 标志启动，可以绕过部分权限检查。

Sources: [Run.ps1](#root/kPITB6unczti)

### Feature Flags 不生效

**症状：** 设置了环境变量，但功能未启用

**解决方案：**

确保环境变量格式正确，并使用大写的 `FEATURE_` 前缀：

```
# 错误格式
feature_buddy=1 bun run dev

# 正确格式
FEATURE_BUDDY=1 bun run dev
```

Feature Flags 在构建时会被写入代码，修改后需要重新构建（如果使用了 `bun run build`）。

Sources: [build.ts](#root/qBdKai4cwPHI)

## 下一步

完成环境安装和基本配置后，建议按照以下顺序阅读文档，深入了解 CCB 的架构和功能：

1.  **[登录与平台配置](4-deng-lu-yu-ping-tai-pei-zhi.md)** - 了解详细的 API 配置和认证流程
2.  **[Feature Flags 功能开关](5-feature-flags-gong-neng-kai-guan.md)** - 掌握所有功能的启用方式
3.  **[项目概览](1-xiang-mu-gai-lan.md)** - 理解项目的整体设计理念和目标
4.  **[五层架构设计](6-wu-ceng-jia-gou-she-ji.md)** - 深入理解系统的分层架构

如果安装过程中遇到未覆盖的问题，请查看项目的 [GitHub Issues](https://github.com/claude-code-best/claude-code/issues) 或加入 [Discord 群组](https://discord.gg/qZU6zS7Q) 获取社区支持。

## 相关条目
- [[2-kuai-su-kai-shi]]
- [[4-deng-lu-yu-ping-tai-pei-zhi]]
