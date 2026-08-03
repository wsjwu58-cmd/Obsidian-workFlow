# 22-skills-ji-neng-kai-fa
Claude Code 的 Skill 系统是 Prompt 即能力的架构哲学完美诠释——复杂任务的关键不在代码逻辑，而在 Prompt 质量本身。通过将领域专家知识封装为可复用的 Markdown 文件，Skill 让开发者可以创建从代码审查到 PR 创建的完整工作流，同时保持极低的实现成本。

## 核心概念：Tool 与 Skill 的本质差异

理解 Skill 的第一步是区分它与 Tool 的设计边界：

| 维度 | Tool | Skill |
| --- | --- | --- |
| **粒度** | 单个原子操作（读文件、执行命令） | 一套完整工作流（代码审查、创建 PR） |
| **触发方式** | AI 自主选择 | 用户 `/skill-name` 或 AI 通过 `SkillTool` 自动匹配 |
| **本质** | TypeScript 执行逻辑 | **Prompt + 权限配置**的声明式封装 |
| **注册位置** | `src/tools.ts` → `getTools()` | `src/commands.ts` → `getCommands()` |
| **执行器** | 各 Tool 的 `call()` 方法 | `SkillTool.call()` → 两条分支（inline / fork） |

Skill 的核心洞见在于：代码审查 Skill 不需要审查引擎，只需告诉 AI "审查什么、按什么顺序、输出什么格式"。Skill 把这种"经验"封装为可复用的 Markdown，将 AI 能力放大百倍。

Sources: [docs/extensibility/skills.mdx](#root/UUmFwF5jsXQ9)

## 五大来源与完整加载链路

Skill 系统支持五种来源，每种都有其独特的加载策略和安全边界：

### 1\. 内置命令（Built-in Commands）

硬编码在 `src/commands.ts:258` 的 `COMMANDS` memoize 数组中，包含 70+ 条命令（`/commit`、`/review`、`/compact` 等）。这些是 TypeScript 模块而非 Markdown，但实现了相同的 `Command` 接口。

Sources: [src/commands.ts:258](#root/UrmxwDHwJtgd)

### 2\. Bundled Skills（编译时打包）

通过 `registerBundledSkill()`（`src/skills/bundledSkills.ts:53`）在模块初始化时注册。关键特性包括**延迟文件提取**——如果 Skill 声明了 `files`（参考文件），首次调用时才解压到临时目录，使用 `O_NOFOLLOW | O_EXCL` 防止符号链接攻击。

来源标记为 `source: 'bundled'`，在 Prompt 预算中享有**不可截断**的特权。

Sources: [src/skills/bundledSkills.ts:53](#root/jattjyfzkNJ5)

### 3\. 磁盘 Skills（`.claude/skills/`）

由 `loadSkillsFromSkillsDir()`（`src/skills/loadSkillsDir.ts:407`）加载，这是最重要的加载路径：

```
管理策略: $MANAGED_DIR/.claude/skills/     (policySettings)
用户全局: ~/.claude/skills/                 (userSettings)
项目级:   .claude/skills/                   (projectSettings, 向上遍历至 home)
附加目录: --add-dir 指定的路径下 .claude/skills/
```

**加载协议**：只识别 `skill-name/SKILL.md` 目录格式，不再支持单文件 `.md`。

Sources: [src/skills/loadSkillsDir.ts:407](#root/XwLERngr2O2r)

### 4\. MCP Skills（动态发现）

通过 `registerMCPSkillBuilders()` 注册构建器，MCP Server 的 prompt 被 `mcpSkillBuilders.ts` 转换为 `Command` 对象。标记为 `loadedFrom: 'mcp'`。

**安全边界**：MCP Skills 的 Prompt 内容**禁止执行内联 shell 命令**（`loadSkillsDir.ts:374` 的 `loadedFrom !== 'mcp'` 守卫），因为远程内容不可信。

Sources: [src/skills/mcpSkillBuilders.ts](#root/bBpwnTo7KvCC)

### 5\. Legacy Commands（`/commands/` 目录）

向后兼容的旧格式，由 `loadSkillsFromCommandsDir()`（第 566 行）加载。同时支持 `SKILL.md` 目录格式和单 `.md` 文件格式。

Sources: [src/skills/loadSkillsDir.ts:566](#root/YWtjlemQd6CR)

## Frontmatter 字段全景

一个 `SKILL.md` 的完整 frontmatter（`parseSkillFrontmatterFields`，第 185 行）定义了 Skill 的所有元数据：

```yaml
---
name: code-review                    # 显示名称（覆盖目录名）
description: 系统性代码审查           # 描述（或从 Markdown 首段提取）
when_to_use: "用户说审查代码、找 bug"  # AI 自动匹配依据
allowed-tools:                       # 工具白名单
  - Read
  - Grep
  - Glob
argument-hint: "<file-or-directory>" # 参数提示
arguments: [path]                    # 声明式参数名（用于 $ARGUMENTS 替换）
model: opus                          # 模型覆盖
effort: high                         # 努力级别
context: fork                        # 执行模式：inline（默认）| fork
agent: code-reviewer                 # 指定 Agent 定义文件
user-invocable: true                 # 用户是否可 /调用
disable-model-invocation: false      # 禁止 AI 自主调用
version: "1.0"                       # 版本号
paths:                               # 条件激活的文件路径模式
  - "src/**/*.ts"
hooks:                               # Hook 配置
  PreToolUse:
    - command: ["echo", "checking"]
shell: ["bash"]                      # Shell 执行环境
---
```

解析后有 17 个字段被提取，其中 `allowedTools`、`model`、`effort` 在执行时动态修改 `toolPermissionContext`。

Sources: [src/skills/loadSkillsDir.ts:185](#root/04LFQbVKf876)

## 两条执行路径：Inline vs Fork

SkillTool（`src/tools/SkillTool/SkillTool.ts:332`）在 `call()` 中根据 `command.context` 分流：

### Inline 模式（默认）

Skill 的 Prompt 内容被注入为 **UserMessage**，在主对话流中继续执行：

1.  `processPromptSlashCommand()` 处理参数替换（`$ARGUMENTS`）和 shell 命令展开（`` !`...` ``）
2.  `${CLAUDE_SKILL_DIR}` 被替换为 Skill 所在目录的绝对路径
3.  `${CLAUDE_SESSION_ID}` 被替换为当前会话 ID
4.  返回 `newMessages`（注入到对话流）+ `contextModifier`（修改权限上下文）

Sources: [src/tools/SkillTool/SkillTool.ts:332](#root/XnilKcpdRcyA)

### Fork 模式（`context: fork`）

Skill 在**独立子 Agent** 中执行（`executeForkedSkill`，第 122 行）：

1.  `prepareForkedCommandContext()` 构建隔离的 Agent 定义和 Prompt
2.  `runAgent()` 启动子 Agent 循环，拥有独立的 token 预算
3.  通过 `onProgress` 回调报告工具使用进度
4.  结果通过 `extractResultText()` 提取，子 Agent 的全部消息在提取后被释放

Fork 模式适用于需要强隔离的场景（如长时间运行的审查任务），避免污染主对话的上下文。

Sources: [src/tools/SkillTool/SkillTool.ts:122](#root/M5ZoImMEdkmA)

## 权限模型：Safe Properties 白名单

`checkPermissions()`（第 433 行）实现了一个四层权限检查：

```
1. Deny 规则匹配（支持精确匹配和 prefix:* 通配符）
   ↓ 未命中
2. 官方市场 Skill 自动放行（plugin + isOfficialMarketplaceName）
   ↓ 未命中
3. Allow 规则匹配
   ↓ 未命中
4. Safe Properties 白名单检查（skillHasOnlySafeProperties，第 911 行）
   ↓ 有非安全属性
5. Ask 用户确认（附带精确匹配和前缀匹配两条建议规则）
```

**Safe Properties**（`SAFE_SKILL_PROPERTIES`，第 876 行）是一个包含 28 个属性名的白名单。任何不在白名单中的**有意义的属性值**都会触发权限请求。这是**正向安全**设计——未来新增的属性默认需要权限。

Sources: [src/tools/SkillTool/SkillTool.ts:433](#root/PRtKmEqOKut5)

## Prompt 预算：1% 上下文窗口的截断策略

Skill 列表注入 System Prompt 时有严格的字符预算：

*   **预算计算**：`contextWindowTokens × 4 chars/token × 1%`（约 8000 字符）
*   **单条上限**：`MAX_LISTING_DESC_CHARS = 250` 字符（超出截断为 `…`）
*   **Bundled Skills 不可截断**：它们始终保留完整描述
*   **降级策略**：
    1.  尝试完整描述 → 超预算？
    2.  Bundled 保留完整，非 bundled 均分剩余预算 → 每条描述低于 20 字符？
    3.  非 bundled 仅保留名称

Sources: [src/tools/SkillTool/prompt.ts:1](#root/7Lf1YjkTID0r)

## 动态发现与条件激活

### 基于文件路径的动态发现

`discoverSkillDirsForPaths()`（`loadSkillsDir.ts:861`）在文件操作时触发：

1.  从被操作的文件路径开始，**向上遍历**至 CWD（不包含 CWD 本身）
2.  在每层查找 `.claude/skills/` 目录
3.  使用 `realpath` 去重，`git check-ignore` 过滤 gitignored 目录
4.  按路径深度排序（**深层优先**），更接近文件的 Skill 优先级更高

Sources: [src/skills/loadSkillsDir.ts:861](#root/U9HQQ2EqzbgW)

### 条件激活（paths frontmatter）

带有 `paths` 模式的 Skill 在加载时不会立即可用，而是存入 `conditionalSkills` Map。当被操作的文件路径匹配某个 Skill 的 paths 模式时（使用 `ignore` 库做 gitignore 风格匹配），该 Skill 才被**激活**。

这意味着一个只在 `*.test.ts` 上激活的测试 Skill，平时完全不可见，只有当 AI 读取或编辑测试文件时才会出现。

Sources: [src/skills/loadSkillsDir.ts:1000](#root/RxSn1QKrgPTs)

## 使用频率排名

`recordSkillUsage()`（`skillUsageTracking.ts`）使用指数衰减算法计算 Skill 排名分数：

```
score = usageCount × max(0.5^(daysSinceUse / 7), 0.1)
```

*   **7 天半衰期**：一周前的使用权重减半
*   **最低 0.1 保底**：避免老但高频使用的 Skill 完全沉底
*   **60 秒去抖**：同一 Skill 在 1 分钟内的多次调用只计一次

Sources: [src/utils/suggestions/skillUsageTracking.ts:1](#root/ehnORQOzjd0N)

## 远程技能加载（Experimental）

通过 `EXPERIMENTAL_SKILL_SEARCH` feature flag 控制，支持从远程（AKI/GCS/S3）加载 `_canonical_<slug>` 格式的 Skill：

1.  `validateInput()` 中 `stripCanonicalPrefix()` 拦截 canonical 名称
2.  `executeRemoteSkill()`（第 970 行）从远程 URL 加载 SKILL.md
3.  支持 `gs://`、`https://`、`s3://` 等 URL 协议
4.  内容经过 frontmatter 剥离、`${CLAUDE_SKILL_DIR}` 替换后直接注入

Sources: [src/tools/SkillTool/SkillTool.ts:970](#root/1D0XTkPuIkVq)

## SKILL.md 文件格式规范

Skill 开发者需要遵循的完整文件格式：

### 目录结构

```
skill-name/
└── SKILL.md          # 必须命名为 SKILL.md（大写）
```

### 最小有效示例

```gfm
# Code Review

审查代码库中的潜在问题。

## Usage

当用户说"审查代码"或"找 bug"时使用此技能。
```

### 完整 frontmatter 示例

```yaml
---
name: comprehensive-review
description: 全面的代码审查，包括性能、安全和可维护性
when_to_use: |
  用户要求审查 PR、代码变更或整个模块
  发现潜在的 bug 或性能问题
  代码审查作为日常开发流程的一部分
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
argument-hint: "<path-to-files>"
arguments: [path]
model: opus
effort: high
context: fork
agent: code-reviewer
user-invocable: true
version: "1.0"
paths:
  - "src/**/*.ts"
  - "src/**/*.tsx"
---
```

## 创建 Bundled Skill

Bundled Skill 是编译时打包到 CLI 中的 Skill，适合核心功能：

### 1\. 创建注册函数

在 `src/skills/bundled/` 下创建新文件：

```typescript
// src/skills/bundled/my-skill.ts
import { registerBundledSkill } from '../bundledSkills.js'

export function registerMySkill(): void {
  registerBundledSkill({
    name: 'my-skill',
    description: '描述信息',
    whenToUse: '用户说...时使用',
    allowedTools: ['Read', 'Grep'],
    argumentHint: '[参数]',
    async getPromptForCommand(args, context) {
      return [{ 
        type: 'text', 
        text: `# My Skill\n\n参数: ${args}\n\n## 指示...` 
      }]
    },
  })
}
```

### 2\. 注册到初始化

在 `src/skills/bundled/index.ts` 中导入并调用：

```typescript
import { registerMySkill } from './my-skill.js'

export function initBundledSkills(): void {
  // ... 其他注册
  registerMySkill()
}
```

Sources: [src/skills/bundled/index.ts](#root/p0bnv4z2VOM2)

## Skill 生命周期与缓存管理

### 缓存层级

Skill 系统使用多层缓存来平衡性能与新鲜度：

1.  **loadAllCommands** — 异步加载所有命令源（skills、plugins、workflows）
2.  **getCommands** — 过滤可用性（availability）和启用状态（isEnabled）
3.  **Skill Caches** — 磁盘 Skills、动态 Skills、条件激活 Skills

### 缓存失效触发器

`useSkillsChange` hook 管理缓存刷新：

1.  **Skill 文件变更（watcher）** — 完整缓存清除 + 磁盘重新扫描
2.  **GrowthBook 刷新** — 仅清除 memo，因为只有 `isEnabled()` 谓词可能改变

Sources: [src/hooks/useSkillsChange.ts](#root/0VlgCfmkR0bf)

## 架构总览图

```
flowchart TB
    subgraph Sources["Skill 来源"]
        BuiltIn["内置命令<br/>Built-in Commands"]
        Bundled["Bundled Skills<br/>编译时打包"]
        Disk["磁盘 Skills<br/>.claude/skills/"]
        MCP["MCP Skills<br/>动态发现"]
        Legacy["Legacy Commands<br/>/commands/ 目录"]
    end

    subgraph Load["加载层"]
        LoadAll["loadAllCommands()"]
        FilterAvail["meetsAvailabilityRequirement()"]
        FilterEnabled["isCommandEnabled()"]
    end

    subgraph Execute["执行层"]
        Inline["Inline 模式<br/>Prompt 注入主对话"]
        Fork["Fork 模式<br/>独立子 Agent"]
    end

    subgraph Permission["权限层"]
        Deny["Deny 规则"]
        Allow["Allow 规则"]
        SafeProps["Safe Properties 白名单"]
        Ask["用户确认"]
    end

    Sources --> LoadAll
    LoadAll --> FilterAvail
    FilterAvail --> FilterEnabled
    FilterEnabled --> Inline & Fork
    
    Deny -->|未命中| Allow
    Allow -->|未命中| SafeProps
    SafeProps -->|非安全属性| Ask
    
    Inline & Fork --> Permission
```

## 下一步探索

*   [Hooks 机制](23-hooks-ji-zhi.md) — 学习如何通过 Hooks 扩展 Skill 行为
*   [自定义 Agents](21-zi-ding-yi-agents.md) — 了解如何为 Fork 模式 Skill 定义专用 Agent
*   [MCP 协议集成](12-mcp-xie-yi-ji-cheng.md) — 深入 MCP Skills 的实现细节
*   [Permission Model 权限模型](15-quan-xian-mo-xing-yu-gui-ze-yin-qing.md) — 理解 Skill 权限检查的完整流程

## 相关条目
- [[21-zi-ding-yi-agents]]
- [[23-hooks-ji-zhi]]
