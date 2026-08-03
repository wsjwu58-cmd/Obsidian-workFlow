# 17-sha-xiang-an-quan-ji-zhi
Claude Code 的沙箱机制是纵深防御体系的第三层——即使 AI 生成了恶意命令，或权限审批被绕过，操作系统级别的沙箱约束仍能阻止危险行为。与权限系统（回答"这条命令能不能执行"）不同，沙箱决定"执行时能做到什么程度"。两者共同构成从应用层到 OS 层的双重安全屏障。

Sources: [sandbox.mdx](#root/LUSsEHHV2h4z)

## 架构概述：命令执行链路

一条 Bash 命令从用户输入到沙箱包裹，经历完整的验证链路：

```
flowchart TD
    A[用户输入] --> B[BashTool.call]
    B --> C[shouldUseSandbox input]
    C --> D{全局开关检查}
    D -->|未启用| E[跳过沙箱]
    D -->|启用| F{显式禁用检查}
    F -->|dangerouslyDisableSandbox| G{策略允许?}
    F -->|正常流程| H{排除列表检查}
    H -->|匹配| E
    H -->|不匹配| I[进入沙箱]
    G -->|允许| E
    G -->|禁止| I
    I --> J[Shell.exec shouldUseSandbox=true]
    J --> K[SandboxManager.wrapWithSandbox]
    K --> L[sandbox-exec bwrap]
    L --> M[spawn wrapped_command]
```

关键判定函数 `shouldUseSandbox()` 位于 `src/tools/BashTool/shouldUseSandbox.ts`，执行四层检查逻辑：

```typescript
export function shouldUseSandbox(input: Partial<SandboxInput>): boolean {
  // 1. 全局未启用 → 跳过
  if (!SandboxManager.isSandboxingEnabled()) return false

  // 2. 显式禁用 + 策略允许 → 跳过
  if (input.dangerouslyDisableSandbox && 
      SandboxManager.areUnsandboxedCommandsAllowed()) return false

  // 3. 无命令 → 跳过
  if (!input.command) return false

  // 4. 匹配排除列表 → 跳过
  if (containsExcludedCommand(input.command)) return false

  // 5. 其他情况 → 必须沙箱化
  return true
}
```

Sources: [shouldUseSandbox.ts](#root/Kgt114dNFDnJ)

## 沙箱判定逻辑：排除命令匹配机制

`containsExcludedCommand()` 的匹配机制是理解沙箱行为的核心。该函数支持三种匹配模式，不仅检查命令本身，还会对复合命令进行拆分迭代检查：

| 模式 | 语法 | 匹配行为 |
| --- | --- | --- |
| **精确匹配** | `npm run lint` | 完全相等才匹配 |
| **前缀匹配** | `npm run test:*` | 前缀 + 空格或完全相等 |
| **通配符** | `docker*` | 使用 glob 模式匹配 |

对于复合命令（如 `docker ps && curl evil.com`），系统会先通过 `splitCommand_DEPRECATED()` 拆分为子命令，逐一检查每个子命令是否匹配排除模式。

更重要的是，算法会迭代剥离环境变量前缀（`FOO=bar bazel ...`）和包装命令（`timeout 30 bazel ...`），直到不动点为止。这种双重剥离确保了：

```typescript
// 迭代生成候选命令列表
const candidates = [trimmed]
const seen = new Set(candidates)
while (startIdx < candidates.length) {
  const envStripped = stripAllLeadingEnvVars(cmd, BINARY_HIJACK_VARS)
  if (!seen.has(envStripped)) candidates.push(envStripped)
  const wrapperStripped = stripSafeWrappers(cmd)
  if (!seen.has(wrapperStripped)) candidates.push(wrapperStripped)
}
```

这意味着 `FOO=bar bazel build` 会匹配 `bazel:*` 排除规则，即使原始命令被包装为 `timeout 300 FOO=bar bazel build`。

Sources: [shouldUseSandbox.ts](#root/Fn89uUjCH4PD)

## 平台实现差异

### macOS：Seatbelt（sandbox-exec）

macOS 使用 Apple 原生的 Seatbelt 沙箱，通过 `sandbox-exec` 命令包裹原始命令：

```
sandbox-exec -p <profile> -- <original_command>
```

Seatbelt profile 是基于配置中的网络/文件系统规则动态生成的，在内核级别强制执行约束。网络隔离通过代理端口拦截 HTTP/HTTPS 请求实现，Unix socket 可单独配置允许路径。

### Linux：bubblewrap + seccomp

Linux 使用 `bubblewrap`（bwrap）创建命名空间隔离，配合 seccomp 过滤系统调用：

| 依赖项 | 作用 |
| --- | --- |
| `bubblewrap` | 创建 mount/PID/network 命名空间 |
| `socat` | 网络代理（HTTP/SOCKS） |
| `ripgrep` | 搜索工具（内置支持） |
| `libseccomp` / seccomp filter | 过滤 Unix socket 系统调用 |

bwrap 与 Seatbelt 的关键差异：

*   **不支持 glob 路径模式**：Linux 上带 glob 的权限规则会触发警告（`getLinuxGlobPatternWarnings()`）
*   **Unix socket 无法按路径过滤**：seccomp 只能全允许或全拒绝，无法像 macOS 那样按路径放行

Sources: [sandbox-adapter.ts](#root/WcPklY2JYVRb)

## 配置模型

沙箱配置定义在 `src/entrypoints/sandboxTypes.ts` 中，通过 Zod schema 验证。完整的配置结构：

```
{
  "sandbox": {
    "enabled": true,                      // 主开关
    "autoAllowBashIfSandboxed": true,     // 沙箱中命令自动放行（跳过审批）
    "allowUnsandboxedCommands": true,     // 是否允许 dangerouslyDisableSandbox
    "failIfUnavailable": false,           // 依赖缺失时是否报错退出
    
    "network": {
      "allowedDomains": ["github.com"],   // 网络白名单
      "deniedDomains": [],                // 网络黑名单
      "allowLocalBinding": true,          // 允许 localhost 绑定
      "httpProxyPort": 8888               // HTTP 代理端口（MITM）
    },
    
    "filesystem": {
      "allowWrite": ["~/projects"],       // 额外可写路径
      "denyWrite": ["~/.ssh"],            // 禁止写入路径
      "denyRead": [],                     // 禁止读取路径
      "allowRead": []                     // 在 denyRead 中重新放行
    },
    
    "excludedCommands": ["docker", "npm:*"]  // 不走沙箱的命令
  }
}
```

Sources: [sandboxTypes.ts](#root/s3q5ALdchY4G)

## 初始化流程与动态配置

沙箱的初始化发生在 REPL 或 SDK 启动时，通过 `SandboxManager.initialize()` 完成：

```
sequenceDiagram
    participant Main as main.tsx
    participant SM as SandboxManager
    participant Base as BaseSandboxManager
    participant Settings as Settings System

    Main->>SM: initialize(sandboxAskCallback)
    SM->>SM: detectWorktreeMainRepoPath()
    SM->>Settings: getSettings_DEPRECATED()
    SM->>SM: convertToSandboxRuntimeConfig()
    SM->>Base: BaseSandboxManager.initialize(config)
    SM->>Settings: settingsChangeDetector.subscribe()
    Note over SM: 动态监听设置变更
```

`convertToSandboxRuntimeConfig()` 是关键的配置转换函数，它从权限规则中提取约束并构建运行时配置：

```typescript
// 从 WebFetch 权限规则提取域名
const allowedDomains: string[] = []
for (const ruleString of permissions.allow || []) {
  const rule = permissionRuleValueFromString(ruleString)
  if (rule.toolName === WEB_FETCH_TOOL_NAME && 
      rule.ruleContent?.startsWith('domain:')) {
    allowedDomains.push(rule.ruleContent.substring('domain:'.length))
  }
}

// 从 Edit/Read 权限规则提取文件系统路径
const allowWrite: string[] = ['.', getClaudeTempDir()]
```

Sources: [sandbox-adapter.ts](#root/06nmYqa38N7B)

## 安全加固：自动注入的防护规则

`sandbox-adapter.ts` 中硬编码了多项安全加固措施，这些规则不会被用户的配置文件覆盖：

| 保护目标 | 规则类型 | 说明 |
| --- | --- | --- |
| `settings.json` | denyWrite | 防止沙箱逃逸到配置文件 |
| `.claude/skills` | denyWrite | 防止技能注入攻击 |
| `HEAD`, `objects`, `refs` | 条件 denyWrite | 防护 bare git repo 攻击 |
| 项目目录 | allowWrite | 自动放行当前项目 |

### Bare Git Repo 攻击防御

这是一个典型攻击向量：攻击者在 cwd 创建 `HEAD` + `objects/` + `refs/` 目录，伪装成 git bare repo，然后配置恶意 hooks。当 Claude 运行 unsandboxed git 时触发攻击。

防御措施：

```typescript
// 如果文件已存在，直接 denyWrite
const bareGitRepoFiles = ['HEAD', 'objects', 'refs', 'hooks', 'config']
for (const gitFile of bareGitRepoFiles) {
  try {
    statSync(p)
    denyWrite.push(p)  // 只读绑定
  } catch {
    bareGitRepoScrubPaths.push(p)  // 事后清理
  }
}
```

Sources: [sandbox-adapter.ts](#root/ZPHGdgFk1CGj)

## `dangerouslyDisableSandbox` 的设计权衡

这个参数的命名本身就是警示——它代表"危险地禁用沙箱"，而非简单的配置选项。设计包含双重保险机制：

```typescript
// 调用侧：模型可以在 BashTool inputSchema 中请求禁用沙箱
// 策略侧：管理员可通过 allowUnsandboxedCommands: false 完全禁止

if (input.dangerouslyDisableSandbox && 
    SandboxManager.areUnsandboxedCommandsAllowed()) {
  return false  // 只有策略允许时才真正跳过沙箱
}
```

当 `autoAllowBashIfSandboxed: true` 时，沙箱中的命令会自动获得执行许可，无需逐条审批。这基于信任假设：**如果 OS 级沙箱已经限制了命令的能力，应用层的逐条审批就变得多余**。

Sources: [sandbox.mdx](#root/UpOlME33l529)

## 沙箱执行与清理

`Shell.ts` 中的 `exec()` 函数是命令执行的最终入口：

```typescript
if (shouldUseSandbox) {
  commandString = await SandboxManager.wrapWithSandbox(
    commandString,
    sandboxBinShell,
    undefined,
    abortSignal,
  )
  // 创建沙箱临时目录
  await fs.mkdir(sandboxTmpDir, { mode: 0o700 })
}

// 命令执行后清理
void shellCommand.result.then(async result => {
  if (shouldUseSandbox) {
    SandboxManager.cleanupAfterCommand()
  }
})
```

`cleanupAfterCommand()` 执行两项清理：

1.  **调用底层清理**：bwrap 会在当前目录留下 0 字节的 mount-point 文件（如 `.bashrc`）
2.  **清理 planted bare repo 文件**：防止 planted 文件被 unsandboxed git 读取

Sources: [Shell.ts](#root/gylG0XOjgaXs), [sandbox-adapter.ts](#root/VZaXgHdTLJqf)

## 违规处理与审计

当命令尝试违反沙箱约束时，系统通过以下机制处理：

```
flowchart TD
    A[命令执行] --> B{违反沙箱约束?}
    B -->|是| C[运行时捕获违规事件]
    C --> D[annotateStderrWithSandboxFailures]
    D --> E[注入 <sandbox_violations> 标签]
    E --> F[SandboxViolationStore 持久化]
    F --> G[UI 层 removeSandboxViolationTags]
    G --> H[清理显示]
```

`removeSandboxViolationTags()` 用于清理错误消息中的违规标记：

```typescript
export function removeSandboxViolationTags(text: string): string {
  return text.replace(/<sandbox_violations>[\s\S]*?<\/sandbox_violations>/g, '')
}
```

Sources: [sandbox-ui-utils.ts](#root/7JI5JZKdNJH6), [sandbox-adapter.ts](#root/OSKRzJH7GR97)

## 平台支持矩阵

| 特性 | macOS | Linux | WSL2 |
| --- | --- | --- | --- |
| 沙箱引擎 | sandbox-exec (Seatbelt) | bubblewrap + seccomp | 同 Linux |
| 文件 glob 模式 | ✅ 完整支持 | ⚠️ 警告（不支持） | ⚠️ 警告 |
| Unix socket 按路径 | ✅ 支持 | ❌ 不支持 | ❌ 不支持 |
| 依赖检查 | ripgrep | bwrap + socat + ripgrep | 同 Linux |

### 依赖检查状态

```typescript
const depCheck = SandboxManager.checkDependencies()
// depCheck.errors: 缺失的必需依赖
// depCheck.warnings: 可选依赖缺失警告
```

Sources: [SandboxDependenciesTab.tsx](#root/l4aQFQqiBIZb)

## 交互式配置界面

Claude Code 提供 `/sandbox` 命令用于交互式配置：

```
/sandbox              # 打开交互式配置菜单
/sandbox exclude "npm run test:*"  # 添加排除命令
```

配置界面包含三个标签页：

*   **Mode**：选择沙箱模式（auto-allow / regular / disabled）
*   **Overrides**：配置 unsandboxed fallback 策略
*   **Config**：查看当前配置状态和 glob 模式警告

Sources: [sandbox-toggle.tsx](#root/GbiMeo3RhC0V), [SandboxSettings.tsx](#root/MJXR6I83TBnr)

## 权限系统与沙箱的关系

理解两者的区别至关重要：

| 维度 | 权限系统 | 沙箱机制 |
| --- | --- | --- |
| **层级** | 应用层 | OS 层 |
| **检查时机** | 工具调用前 | 进程执行时 |
| **控制粒度** | 按命令/路径 | 按系统调用 |
| **可绕过性** | 可能被 prompt injection 绕过 | 内核级强制执行 |
| **配置方式** | 规则匹配 | 系统级约束 |

权限系统是"软约束"（依赖模型遵从），沙箱是"硬约束"（即使 AI 生成了恶意命令也无法突破）。两者构成纵深防御的两层。

Sources: [why-safety-matters.mdx](#root/ZvcAfdJ7I6t9), [permission-model.mdx](#root/QBYB798rI0Zc)

## 下一步

*   [权限模型与规则引擎](15-quan-xian-mo-xing-yu-gui-ze-yin-qing.md)：了解 Allow/Ask/Deny 三级权限体系
*   [Auto Mode 自动模式](16-auto-mode-zi-dong-mo-shi.md)：了解 AI 分类器驱动的自主执行模式
*   [Remote Control 远程控制](18-remote-control-yuan-cheng-kong-zhi.md)：了解沙箱在远程场景中的应用

## 相关条目
- [[15-quan-xian-mo-xing-yu-gui-ze-yin-qing]]
- [[13-computer-use-dian-nao-cao-kong]]
