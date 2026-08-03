# 5-feature-flags-gong-neng-kai-guan
Claude Code 采用双层 Feature Flag 体系控制功能可见性：**构建时 Feature Flags** 通过 `bun:bundle` 编译器实现 Dead Code Elimination（死代码消除），**运行时 Feature Flags** 通过 GrowthBook SDK 实现用户级灰度发布。本页将详解这两层门控的机制、代码模式和实际应用。

## 双层门控架构

Claude Code 的 Feature Flags 系统由两个独立层次组成，它们在不同的生命周期阶段发挥作用：

```
flowchart TB
    subgraph Build["构建时层 feature()"]
        F1["88+ 构建时 Flags"]
        DCE["Dead Code Elimination<br/>编译时代码删除"]
    end
    
    subgraph Runtime["运行时层 GrowthBook"]
        F2["500+ 运行时 Flags<br/>tengu_* 前缀"]
        SDK["GrowthBook SDK"]
        Remote["远程服务器<br/>api.anthropic.com"]
    end
    
    Build -->|打包时求值| Runtime
    Runtime -->|按用户属性| User["用户可见功能"]
    
    style Build fill:#e1f5fe
    style Runtime fill:#fff3e0
    style User fill:#e8f5e9
```

| 维度 | 构建时 feature() | 运行时 GrowthBook |
| --- | --- | --- |
| **控制方式** | `bun:bundle` 编译时宏 | GrowthBook SDK 远程求值 |
| **决策时机** | 打包时（代码直接被删除） | 启动时 + 定期刷新 |
| **粒度** | 全有或全无 | 按用户/设备/组织定向 |
| **标记数量** | 88+ | 500+ |
| **逆向可见性** | 代码残留但永不执行 | 完整 SDK 代码可读 |

Sources: [src/entrypoints/cli.tsx](#root/5YOEo6v1vPho), [src/services/analytics/growthbook.ts](#root/TrUzpRTe0LGv)

## 构建时 Feature Flags

### 机制原理

Claude Code 使用 Bun 打包器的 `bun:bundle` 模块提供编译时特性门控。在源码中的典型用法：

```typescript
// 源码中的用法
import { feature } from 'bun:bundle'

const SleepTool = feature('PROACTIVE') || feature('KAIROS')
  ? require('./tools/SleepTool/SleepTool.js').SleepTool
  : null
```

在 Anthropic 的内部构建中，`feature()` 在打包时被求值——返回 `true` 的代码会被保留，返回 `false` 的代码会被 **Dead Code Elimination (DCE)** 彻底移除。

在反编译版本中，这个函数被兜底为：

```typescript
// src/entrypoints/cli.tsx 第 3 行
const feature = (_name: string) => false;
```

这意味着所有 88+ 个 feature flag 后的代码在运行时永远不会执行，但代码本身完整保留，可以阅读和分析。

Sources: [src/entrypoints/cli.tsx](#root/5YOEo6v1vPho), [docs/internals/feature-flags.mdx](#root/k1MBERcLjRQm)

### Flags 分类全景

| 类别 | 数量 | 代表性 Flags |
| --- | --- | --- |
| **Agent / 自动化** | 15 | `KAIROS` · `PROACTIVE` · `COORDINATOR_MODE` · `FORK_SUBAGENT` |
| **基础设施** | 10 | `DAEMON` · `BRIDGE_MODE` · `DIRECT_CONNECT` · `SSH_REMOTE` |
| **安全 / 分类** | 6 | `TRANSCRIPT_CLASSIFIER` · `BASH_CLASSIFIER` · `TREE_SITTER_BASH` |
| **工具 / 能力** | 10 | `WEB_BROWSER_TOOL` · `VOICE_MODE` · `MCP_SKILLS` |
| **UI / 体验** | 8 | `MESSAGE_ACTIONS` · `QUICK_SEARCH` · `BUDDY` |
| **平台 / 实验** | 10+ | `ULTRAPLAN` · `ULTRATHINK` · `TORCH` · `PERFETTO_TRACING` |

Sources: [docs/internals/feature-flags.mdx](#root/VKdNP5P8OAGG)

### 典型代码模式

构建时 Feature Flags 在代码中有三种主要使用模式：

**模式一：条件加载工具**

```typescript
// src/tools.ts — 最常见的模式
const MonitorTool = feature('MONITOR_TOOL')
  ? require('./tools/MonitorTool/MonitorTool.js').MonitorTool
  : null
```

**模式二：条件注册命令**

```typescript
// src/entrypoints/cli.tsx — 注册子命令入口
if (feature('DAEMON') && args[0] === 'daemon') {
  const { daemonMain } = await import('../daemon/main.js');
  await daemonMain(args.slice(1));
  return;
}
```

**模式三：条件启用 API 特性**

```typescript
// src/constants/betas.ts — 控制发送给 API 的 beta header
export const AFK_MODE_BETA_HEADER = feature('TRANSCRIPT_CLASSIFIER')
  ? 'afk-mode-2026-01-31'
  : ''
```

**模式四：Ablation 基线实验**

```typescript
// src/entrypoints/cli.tsx — 科学对照实验
if (feature('ABLATION_BASELINE') && process.env.CLAUDE_CODE_ABLATION_BASELINE) {
  for (const k of [
    'CLAUDE_CODE_DISABLE_THINKING',
    'DISABLE_COMPACT',
    'CLAUDE_CODE_DISABLE_AUTO_MEMORY',
  ]) {
    process.env[k] ??= '1';
  }
}
```

Sources: [src/tools.ts](#root/Pr1VBzAwTBO3), [src/entrypoints/cli.tsx](#root/bXsxniKcjjs2), [src/constants/betas.ts](#root/c2X5EMVeu9JQ)

## 运行时 GrowthBook Flags

### 集成架构

GrowthBook 系统实现位于 `src/services/analytics/growthbook.ts`（1164 行），工作流程如下：

```
sequenceDiagram
    participant CLI as CLI 启动
    participant GB as GrowthBook SDK
    participant API as api.anthropic.com
    participant Cache as ~/.claude.json
    participant Code as 业务代码

    CLI->>GB: 初始化客户端
    GB->>API: 获取远程配置 (remoteEval)
    API-->>GB: 返回预计算的特征值
    GB->>Cache: 同步缓存到磁盘
    Code->>GB: 查询 tengu_xxx 标志
    GB-->>Code: 返回用户定向值
```

| 阶段 | 说明 |
| --- | --- |
| **启动时获取** | GrowthBook SDK 通过 `api.anthropic.com` 获取功能配置和实验分组规则 |
| **用户属性计算** | SDK 收集用户属性（订阅类型、组织 UUID、设备 ID 等） |
| **本地缓存** | 计算结果缓存到 `~/.claude.json` 的 `cachedGrowthBookFeatures` 字段 |
| **代码查询** | 业务代码通过 `tengu_*` 前缀的 flag 名查询功能状态 |

Sources: [src/services/analytics/growthbook.ts](#root/NMCuXAT4cv99), [docs/internals/growthbook-ab-testing.mdx](#root/u4evxCXWzxHr)

### Feature Key 命名规范

所有运行时 flag 都以 `tengu_` 为前缀——"Tengu"（天狗）是 Claude Code 的内部项目代号。flag 名采用**动物/植物/矿物 + 形容词**的命名约定，刻意保持不透明：

| Feature Key | 类型 | 代码默认值 | 用途 |
| --- | --- | --- | --- |
| `tengu_hive_evidence` | boolean | `false` | 任务证据系统 |
| `tengu_quartz_lantern` | boolean | `false` | 文件写入/编辑保护 |
| `tengu_auto_background_agents` | boolean | `false` | 自动后台 Agent |
| `tengu_amber_stoat` | boolean | `true` | 内置 Agents |
| `tengu_cobalt_harbor` | boolean | `false` | Bridge 模式 |
| `tengu_slate_thimble` | boolean | `false` | Slate Thimble |
| `tengu_terminal_panel` | boolean | `false` | 终端面板 |
| `tengu_scratch` | boolean | `false` | 草稿本功能 |
| `tengu_thinkback` | boolean | `false` | Thinkback 功能 |

Sources: [docs/internals/growthbook-adapter.mdx](#root/Lnp4okVwt820)

### 用户定向属性

GrowthBook 根据以下用户属性决定实验分组：

| 属性 | 类型 | 来源 | 用途 |
| --- | --- | --- | --- |
| `id` | string | 会话 ID | 按会话粒度分组 |
| `deviceID` | string | 持久化设备标识 | 跨会话一致性 |
| `organizationUUID` | string | API 认证信息 | 按组织灰度 |
| `accountUUID` | string | API 认证信息 | 按个人账户灰度 |
| `subscriptionType` | string | API 认证信息 | Free / Pro / Team 差异化 |
| `rateLimitTier` | string | API 认证信息 | 按速率限制层级 |
| `appVersion` | string | 版本号 | 按版本号灰度 |
| `github` | object | GitHub Actions 元数据 | CI 环境特殊处理 |

Sources: [src/services/analytics/growthbook.ts](#root/hr45kFSefaKA)

### 读取优先级链

每个 feature 的值按以下顺序解析：

```
1. CLAUDE_INTERNAL_FC_OVERRIDES 环境变量（JSON 对象覆盖）
   ↓ 未命中
2. growthBookOverrides 配置（仅 ant 构建）
   ↓ 未命中
3. 内存缓存（remoteEvalFeatureValues）
   ↓ 未命中
4. 磁盘缓存（~/.claude.json）
   ↓ 未命中
5. 代码中的 defaultValue 参数
```

Sources: [src/services/analytics/growthbook.ts](#root/hL0yDms8SjJM)

## 自定义 GrowthBook 服务器接入

### 环境变量配置

Claude Code 支持通过环境变量连接自定义 GrowthBook 服务器：

| 变量 | 必填 | 说明 |
| --- | --- | --- |
| `CLAUDE_GB_ADAPTER_URL` | 是 | GrowthBook API 地址，如 `https://gb.example.com/` |
| `CLAUDE_GB_ADAPTER_KEY` | 是 | GrowthBook SDK Client Key，如 `sdk-xxxxx` |

两个变量都设置时启用适配器模式，否则完全跳过 GrowthBook。

### 基本用法

```
# 使用自定义 GrowthBook 服务器
CLAUDE_GB_ADAPTER_URL=https://gb.example.com/ \
CLAUDE_GB_ADAPTER_KEY=sdk-abc123 \
bun run dev

# 不使用 GrowthBook（默认行为）
bun run dev
# 所有 getFeatureValue_CACHED_MAY_BE_STALE("xxx", defaultValue) 直接返回 defaultValue
```

### 缓存与刷新机制

| 机制 | Anthropic 员工 | 外部用户 |
| --- | --- | --- |
| **周期刷新** | 20 分钟 | 6 小时 |
| **初始化超时** | 5 秒 | 5 秒 |
| **磁盘持久化** | `~/.claude.json` 的 `cachedGrowthBookFeatures` | 同左 |
| **Auth 变更** | 登录/登出时自动销毁并重建 | 同左 |

Sources: [docs/internals/growthbook-adapter.mdx](#root/LVRLES3UZ8N1)

## Ant-Only 覆盖机制

Anthropic 员工拥有两种方式绕过 GrowthBook 的远程求值：

### 环境变量覆盖

```
# 仅在 USER_TYPE=ant 的构建中生效
CLAUDE_INTERNAL_FC_OVERRIDES='{"tengu_kairos": true}' claude
```

### Config 界面覆盖

在内部构建中，`/config` 命令的 Gates 标签页提供了图形化的 flag 管理界面。

Sources: [src/services/analytics/growthbook.ts](#root/vvUuuyKswBBC)

## 进阶阅读

| 文档 | 内容 |
| --- | --- |
| [三层门禁系统](6-wu-ceng-jia-gou-she-ji.md) | 功能可见性控制的全局架构 |
| [GrowthBook A/B 测试体系](#root/sUlfJF3xMJc9) | 运行时功能发布的完整机制 |
| [GrowthBook 适配器](#root/sOtx9n30WVKK) | 自定义 GrowthBook 服务器接入指南 |

## 相关条目
- [[4-deng-lu-yu-ping-tai-pei-zhi]]
- [[15-quan-xian-mo-xing-yu-gui-ze-yin-qing]]
