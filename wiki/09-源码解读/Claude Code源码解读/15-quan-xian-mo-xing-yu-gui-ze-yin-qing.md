# 15-quan-xian-mo-xing-yu-gui-ze-yin-qing
Claude Code 的权限模型是一套多层次、智能化的安全控制系统，通过 Allow/Ask/Deny 三级裁决机制、规则匹配引擎和权限模式切换，在保障用户安全的同时提供灵活的操作授权管理。本文档深入解析权限系统的架构设计与实现细节。

## 核心概念：三种权限行为

每一次工具调用，系统都会做出三种裁决之一。理解这三种行为是掌握整个权限模型的基础。

| 行为 | 含义 | 返回结构 | 典型场景 |
| --- | --- | --- | --- |
| **Allow** | 自动放行，用户无感知 | `{ behavior: 'allow', updatedInput, decisionReason }` | 读取项目内文件、执行安全命令 |
| **Ask** | 弹出确认对话框 | `{ behavior: 'ask', message, suggestions, metadata }` | 执行未知命令、修改敏感文件 |
| **Deny** | 直接拒绝执行 | `{ behavior: 'deny', message, decisionReason }` | 执行被禁止的命令、访问危险路径 |

这三种行为由 `PermissionResult` 类型定义，核心实现在 `src/utils/permissions/PermissionResult.ts` 中。决策理由 `decisionReason` 字段包含详细的拒绝/询问原因，包括规则匹配、Hook 拦截、沙箱覆盖等多种类型。

```typescript
// 权限决策的核心结构
type PermissionDecisionReason =
  | { type: 'rule'; rule: PermissionRule }           // 规则匹配
  | { type: 'hook'; hookName: string; reason?: string }  // Hook拦截
  | { type: 'classifier'; classifier: string; reason: string }  // 分类器决策
  | { type: 'sandboxOverride' }                     // 沙箱覆盖
  | { type: 'safetyCheck'; reason: string }         // 安全检查
  | { type: 'mode'; mode: PermissionMode }          // 权限模式
```

Sources: [PermissionResult.ts](#root/tBZBlZgIBi4J) Sources: [permissions.ts](#root/a7qsqOrPZozy)

## 五层规则来源架构

权限规则从五个来源汇聚，系统按照严格的优先级顺序进行处理。这种设计确保了灵活性的同时保持了安全边界。

```
flowchart TB
    subgraph Priority1["优先级 1: 会话层 session"]
        S["用户当前对话\nAlways allow"]
    end
    
    subgraph Priority2["优先级 2: CLI参数 cliArg"]
        C["--allow/--deny\n命令行参数"]
    end
    
    subgraph Priority3["优先级 3: 命令层 command"]
        CMD["Skill allowedTools\n白名单配置"]
    end
    
    subgraph Priority4["优先级 4: 项目配置 projectSettings"]
        P[".claude/settings.json\n团队共享规则"]
    end
    
    subgraph Priority5["优先级 5: 用户配置 userSettings"]
        U["~/.claude/settings.json\n跨项目通用规则"]
    end
    
    subgraph Priority6["优先级 6: 策略配置 policySettings"]
        POL["企业管理员下发\n不可覆盖策略"]
    end
    
    Decision{"最终裁决"}
    
    S --> Decision
    C --> Decision
    CMD --> Decision
    P --> Decision
    U --> Decision
    POL --> Decision
```

每个来源维护三个规则数组：`alwaysAllowRules[source]`、`alwaysAskRules[source]`、`alwaysDenyRules[source]`。值得注意的是，`policySettings` 是企业管理员下发的策略，用户无法覆盖，当启用 `allowManagedPermissionRulesOnly` 时，只有托管策略规则生效。

```typescript
// 规则来源常量定义
const PERMISSION_RULE_SOURCES = [
  ...SETTING_SOURCES,  // userSettings, projectSettings, localSettings, flagSettings, policySettings
  'cliArg',            // 命令行参数
  'command',           // Skill 工具白名单
  'session',          // 当前会话
] as const
```

Sources: [permissions.ts](#root/yYcCqy99nAHv) Sources: [permissionsLoader.ts](#root/rwBQ2WZ23YfB)

## 规则匹配引擎：三维度匹配机制

权限规则匹配引擎支持三种维度的精确控制，这种设计允许细粒度到命令级别的权限管理。

### 工具名匹配

工具名匹配用于整个工具类别的授权或拒绝。当规则没有 `ruleContent` 时，匹配整个工具。

```typescript
// 精确匹配示例
rule "Bash" → 匹配 BashTool 所有调用
rule "mcp__server1" → 匹配该 MCP Server 的所有工具
rule "mcp__server1__*" → 通配符匹配（同上效果）
```

MCP 工具使用 `getToolNameForPermissionCheck()` 获取标准化名称，支持带前缀（`mcp__server__tool`）和无前缀模式的匹配。

Sources: [permissions.ts](#root/9qK2HjHihJ9p)

### Bash 命令模式匹配

BashTool 通过 `preparePermissionMatcher()` 实现命令级别的细粒度控制，支持三种匹配模式：

| 模式类型 | 示例规则 | 匹配示例 | 优先级 |
| --- | --- | --- | --- |
| 精确匹配 | `git commit` | 精确等于 `git commit` | 最高 |
| 前缀匹配 (legacy) | `npm:*` | `npm install`, `npm test` | 中 |
| 通配符匹配 | `git *` | `git add`, `git push`, `git merge` | 最低 |

```typescript
// 通配符匹配支持转义
git \*          // 匹配字面量 "git *"
\\path          // 匹配字面量 "\path"
```

Sources: [shellRuleMatching.ts](#root/IDH9Ig5SYs5j)

### 文件路径匹配

文件工具（Read/Edit/Write）通过路径模式进行权限控制，支持 glob 模式。

```json
{"tool": "Edit", "ruleContent": "src/**"}  → 匹配 "src/utils/foo.ts"
{"tool": "Read", "ruleContent": "docs/**/*.md"}  → 匹配所有 Markdown 文档
```

Sources: [pathValidation.ts](#root/dQjwip1OMnBv) Sources: [filesystem.ts](#root/8xWWf7JYyZKk)

## 权限检查完整流程

每次工具调用的权限检查遵循严格的决策流程，从全局规则到工具特定检查层层递进。

```
flowchart TD
    Start["工具调用请求"] --> DenyCheck["1a. 全局拒绝检查"]
    DenyCheck --> |命中| Deny["返回 Deny"]
    DenyCheck --> |未命中| AllowCheck["1b. 全局允许检查"]
    AllowCheck --> |命中| Allow["返回 Allow"]
    AllowCheck --> |未命中| ToolCheck["2. 工具自身检查"]
    ToolCheck --> |返回 allow| Allow
    ToolCheck --> |返回 ask| HookCheck["3. Hook 系统检查"]
    ToolCheck --> |返回 deny| Deny
    HookCheck --> |hook deny| Deny
    HookCheck --> |hook allow| Allow
    HookCheck --> |无决定| AskRuleCheck["4. Ask 规则检查"]
    AskRuleCheck --> |命中| Ask["返回 Ask"]
    AskRuleCheck --> |未命中| ModeDefault["5. 权限模式默认行为"]
```

**第一步：全局规则检查（Blanket Check）**

系统首先检查工具名是否完全匹配任何全局 allow 或 deny 规则。如果命中 deny 规则，工具在 `getTools()` 阶段就被过滤掉，不会进入后续流程。

**第二步：工具自身检查**

每个工具实现自定义的 `checkPermissions()` 方法：

*   **BashTool**: readOnlyValidation → sandbox 判定 → AST 解析 → 模式匹配
*   **FileEditTool**: 路径白名单检查 → 危险文件检测
*   **SkillTool**: safe properties 白名单 + 精确/前缀匹配

**第三步：Hook 系统拦截**

`executePermissionRequestHooks()` 允许 PreToolUse hook 覆盖决策结果，实现自定义权限逻辑。

**第四步：Ask 规则匹配**

未在前几步做出决定的请求会检查 Ask 规则，命中则弹出确认对话框。

**第五步：权限模式默认行为**

根据当前权限模式决定默认行为，处理 `dontAsk` → `deny` 的转换。

Sources: [permissions.ts](#root/I4ZGS5ldoD17) Sources: [useCanUseTool.tsx](#root/Yi1lXRi4eZj0)

## 权限模式系统

Claude Code 支持多种权限模式，适应不同的使用场景和安全需求。

| 模式 | 值 | 适用场景 | 核心行为 |
| --- | --- | --- | --- |
| **Default** | `'default'` | 日常开发 | 敏感操作逐一确认 |
| **Plan Mode** | `'plan'` | 探索阶段 | 只读操作允许，写操作询问 |
| **Accept Edits** | `'acceptEdits'` | 信任项目 | 自动允许工作目录内的写操作 |
| **Dont Ask** | `'dontAsk'` | 受限环境 | 所有询问自动转为拒绝 |
| **Auto** | `'auto'` | 信任 AI | 通过分类器自动决策 |
| **Bypass** | `'bypassPermissions'` | 完全信任 | 所有操作自动放行（需显式标志） |

```typescript
// Plan Mode 切换逻辑
context.setAppState(prev => ({
  ...prev,
  toolPermissionContext: applyPermissionUpdate(
    prepareContextForPlanMode(prev.toolPermissionContext),
    { type: 'setMode', mode: 'plan', destination: 'session' },
  ),
}))
```

Sources: [PermissionMode.ts](#root/H5YxC73kcNjP)

## Denial Tracking：死循环防护机制

当 AI 被连续拒绝同一类操作时，系统需要防止陷入"反复请求被拒操作"的死循环。`denialTracking.ts` 实现了这一保护机制。

```typescript
const DENIAL_LIMITS = {
  maxConsecutive: 3,     // 同一工具连续拒绝上限
  maxTotal: 20,           // 会话内总拒绝上限
}
```

**工作流程**：

1.  每次拒绝操作调用 `recordDenial()` 增加计数
2.  `shouldFallbackToPrompting()` 检测是否达到限制
3.  达到限制时，系统向 AI 注入提示消息迫使其改变策略
4.  操作成功时调用 `recordSuccess()` 重置计数

```typescript
// 拒绝追踪状态更新
export function recordDenial(state: DenialTrackingState): DenialTrackingState {
  return {
    consecutiveDenials: state.consecutiveDenials + 1,
    totalDenials: state.totalDenials + 1,
  }
}

export function shouldFallbackToPrompting(state: DenialTrackingState): boolean {
  return (
    state.consecutiveDenials >= DENIAL_LIMITS.maxConsecutive ||
    state.totalDenials >= DENIAL_LIMITS.maxTotal
  )
}
```

Sources: [denialTracking.ts](#root/VBU4m8qq0Vem)

## 运行时规则更新

权限规则可以在运行时动态更新，无需重启会话。这种设计让用户可以在对话过程中灵活调整授权策略。

```typescript
type PermissionUpdate =
  | { type: 'addRules'; destination; rules; behavior }
  | { type: 'removeRules'; destination; rules; behavior }
  | { type: 'replaceRules'; destination; rules; behavior }
  | { type: 'setMode'; destination; mode }
  | { type: 'addDirectories'; destination; directories }
  | { type: 'removeDirectories'; destination; directories }
```

**更新流程**：

1.  用户在 Ask 对话框选择 "Always allow"
2.  系统调用 `persistPermissionUpdates()` 写入对应层级的 settings 文件
3.  内存中的 `toolPermissionContext` 同时更新
4.  规则持久化到 `~/.claude/settings.json`（用户级）或 `.claude/settings.json`（项目级）

```typescript
// 应用规则更新到上下文
export function applyPermissionUpdate(
  context: ToolPermissionContext,
  update: PermissionUpdate,
): ToolPermissionContext {
  switch (update.type) {
    case 'addRules': {
      const ruleStrings = update.rules.map(rule => 
        permissionRuleValueToString(rule)
      )
      const ruleKind = update.behavior === 'allow' 
        ? 'alwaysAllowRules' 
        : update.behavior === 'deny' 
          ? 'alwaysDenyRules' 
          : 'alwaysAskRules'
      
      return {
        ...context,
        [ruleKind]: {
          ...context[ruleKind],
          [update.destination]: [
            ...(context[ruleKind][update.destination] || []),
            ...ruleStrings,
          ],
        },
      }
    }
    // ... 其他更新类型
  }
}
```

Sources: [PermissionUpdate.ts](#root/Ss269BQud4cn)

## Auto Mode 智能分类器

在 Auto 模式下，系统使用 AI 分类器自动判断操作的安全性，避免频繁打扰用户。

```
flowchart LR
    subgraph Input["分类器输入"]
        T["工具调用"]
        C["对话上下文"]
        D["用户规则配置"]
    end
    
    Input --> Classifier["Claude 分类器 API"]
    
    Classifier --> |"allow"| AutoAllow["自动放行"]
    Classifier --> |"deny"| CheckLimits["检查拒绝限制"]
    Classifier --> |"ask"| FallbackPrompt["回退到询问"]
    
    CheckLimits --> |"未超限"| AutoDeny["自动拒绝"]
    CheckLimits --> |"已超限"| UserPrompt["用户确认"]
```

分类器接收以下信息进行决策：

*   当前工具调用详情
*   对话历史上下文
*   用户配置的 allow/deny 规则
*   环境变量和工作目录信息

```typescript
// 分类器决策结果处理
if (classifierResult.shouldBlock) {
  const newDenialState = recordDenial(denialState)
  persistDenialState(context, newDenialState)
  
  // 检查是否达到拒绝限制
  const denialLimitResult = handleDenialLimitExceeded(
    newDenialState,
    appState,
    classifierResult.reason,
    assistantMessage,
    tool,
    result,
    context,
  )
}
```

分类器失败时有两种策略：通过 `tengu_iron_gate_closed` feature flag 控制是"安全优先（fail closed）"还是"可用优先（fail open）"。

Sources: [yoloClassifier.ts](#root/HKBQcU2JzbhI) Sources: [permissions.ts](#root/6FLk6Qy1YZ2X)

## 危险模式识别

系统维护了一份危险命令/模式列表，防止通过宽泛的通配符规则绕过安全检查。

```typescript
// 跨平台代码执行入口点
const CROSS_PLATFORM_CODE_EXEC = [
  'python', 'python3', 'python2', 'node', 'deno', 'ruby', 'perl', 'php',
  'npx', 'bunx', 'npm run', 'yarn run', 'pnpm run', 'bun run',
  'bash', 'sh', 'ssh',
]

// Bash 危险模式（Ant 用户额外）
const DANGEROUS_BASH_PATTERNS = [
  ...CROSS_PLATFORM_CODE_EXEC,
  'zsh', 'fish', 'eval', 'exec', 'env', 'xargs', 'sudo',
  'fa run', 'coo', 'gh', 'gh api', 'curl', 'wget', 'git',
  'kubectl', 'aws', 'gcloud', 'gsutil',
]
```

这些模式用于在 Auto Mode 入口处检测并过滤过于宽泛的 allow 规则，防止通过 `Bash(python:*)` 这样的规则绕过分类器执行任意代码。

Sources: [dangerousPatterns.ts](#root/JFzYaRJK4XBh)

## 交互式权限处理

当权限检查返回 `ask` 时，系统通过 `handleInteractivePermission()` 处理用户交互流程。

```typescript
// 交互式权限处理核心流程
ctx.pushToQueue({
  assistantMessage: ctx.assistantMessage,
  tool: ctx.tool,
  description,
  input: displayInput,
  permissionResult: result,
  onUserInteraction() {
    // 用户开始交互，取消分类器自动批准
    userInteracted = true
    clearClassifierChecking(ctx.toolUseID)
  },
  onAllow(updatedInput, permissionUpdates, feedback) {
    // 用户批准 - 可选永久保存规则
    resolveOnce(ctx.handleUserAllow(
      updatedInput, 
      permissionUpdates, 
      feedback,
      permissionPromptStartTimeMs
    ))
  },
  onReject(feedback) {
    // 用户拒绝
    resolveOnce(ctx.cancelAndAbort())
  },
  recheckPermission() {
    // 重新检查权限（规则可能已更新）
  }
})
```

系统支持通过 Bridge 模式将权限请求转发到远程设备（如手机）进行审批。

Sources: [interactiveHandler.ts](#root/j5ZcZtMl4HEK) Sources: [PermissionContext.ts](#root/mPDwh0JMI11p)

## 文件系统安全检查

文件操作有额外的安全防护，防止修改危险文件或目录。

```typescript
// 危险文件列表
export const DANGEROUS_FILES = [
  '.gitconfig', '.gitmodules',
  '.bashrc', '.bash_profile', '.zshrc', '.zprofile', '.profile',
  '.ripgreprc', '.mcp.json', '.claude.json',
]

// 危险目录列表
export const DANGEROUS_DIRECTORIES = [
  '.git', '.vscode', '.idea', '.claude',
]
```

安全检查在允许写入前执行，确保：

1.  路径不包含路径遍历攻击 (`../`)
2.  不在 Windows 危险路径上
3.  不修改 Claude 配置文件
4.  不修改敏感文件
5.  符合沙箱写入规则

Sources: [filesystem.ts](#root/qYs5wQo8ReXw)

## 配置示例

### 命令行快速授权

```
# 允许所有 git 命令
claude --allow "Bash(git *)"

# 允许特定 MCP 服务器的所有工具
claude --allow "mcp__my-server__*"

# 禁止特定命令
claude --deny "Bash(sudo *)"
```

### Settings.json 配置

```json
{
  "permissions": {
    "allow": [
      "Bash(git *)",
      "Read(src/**)",
      "Edit",
      "mcp__github__*"
    ],
    "deny": [
      "Bash(sudo rm *)"
    ],
    "ask": [
      "Bash(curl *)",
      "Write(/etc/**)"
    ]
  }
}
```

## 架构总结

```
flowchart TB
    subgraph User["用户交互层"]
        CLI["命令行/UI"]
        Bridge["Bridge 远程审批"]
    end
    
    subgraph Engine["权限引擎"]
        Check["hasPermissionsToUseTool"]
        Classifier["Auto Mode 分类器"]
        Hooks["PermissionRequest Hooks"]
    end
    
    subgraph Rules["规则系统"]
        Global["全局规则匹配"]
        Tool["工具特定检查"]
        Path["路径验证"]
    end
    
    subgraph State["状态管理"]
        Context["ToolPermissionContext"]
        Tracking["Denial Tracking"]
        Modes["Permission Modes"]
    end
    
    CLI --> Check
    Bridge --> Check
    Check --> Classifier
    Check --> Hooks
    Classifier --> Global
    Hooks --> Global
    Global --> Tool
    Tool --> Path
    Path --> Modes
    Tracking --> Modes
```

权限模型通过分层设计实现了安全性与灵活性的平衡：全局规则提供快速的预筛选，工具特定检查确保细粒度控制，而 Auto Mode 分类器则在信任与安全之间取得最佳平衡。

## 相关文档

*   [Auto Mode 自动模式](16-auto-mode-zi-dong-mo-shi.md) - 了解如何配置 AI 自动决策
*   [沙箱安全机制](17-sha-xiang-an-quan-ji-zhi.md) - 了解沙箱隔离如何增强安全
*   [工具系统架构](10-gong-ju-xi-tong-jia-gou.md) - 了解各工具的权限检查实现

## 相关条目
- [[5-feature-flags-gong-neng-kai-guan]]
- [[17-sha-xiang-an-quan-ji-zhi]]
- [[21-zi-ding-yi-agents]]
