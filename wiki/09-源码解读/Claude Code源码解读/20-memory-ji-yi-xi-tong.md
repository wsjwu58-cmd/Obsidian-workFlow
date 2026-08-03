# 20-memory-ji-yi-xi-tong
Claude Code 的记忆系统是一个**分层架构**，通过文件持久化存储实现跨对话上下文保持。系统包含三个核心组件：项目记忆（memdir）、会话记忆（Session Memory）和后台记忆提取（extractMemories），它们协同工作让 AI 能够"记住"用户偏好、项目上下文和长期知识。

## 系统架构概览

```
flowchart TB
    subgraph "User Layer 用户层"
        U[用户消息]
    end
    
    subgraph "Memory System 记忆系统"
        subgraph "Project Memory 项目记忆"
            M[memdir.ts]
            MT[memoryTypes.ts]
            MS[memoryScan.ts]
            FR[findRelevantMemories.ts]
        end
        
        subgraph "Session Memory 会话记忆"
            SM[sessionMemory.ts]
            SU[sessionMemoryUtils.ts]
            SP[prompts.ts]
        end
        
        subgraph "Extract Memories 记忆提取"
            EM[extractMemories.ts]
            EP[extractMemories/prompts.ts]
        end
        
        subgraph "Team Memory 团队记忆"
            TM[teamMemorySync]
            TP[teamMemPaths.ts]
        end
    end
    
    subgraph "Storage Layer 存储层"
        FS[(文件系统)]
        API[(API Server)]
    end
    
    U --> M
    U --> SM
    M --> MT
    M --> MS
    M --> FR
    SM --> SU
    SM --> SP
    EM --> EP
    EM --> MS
    TM --> TP
    M --> FS
    SM --> FS
    EM --> FS
    TM --> API
    TM --> FS
```

记忆系统的数据流遵循以下原则：`MEMORY.md` 作为每次对话的入口索引被完整加载，而具体的记忆内容文件通过 Sonnet 侧查询智能召回。`MEMORY.md` 本身仅包含索引指针，不存储实际记忆内容。

## 核心存储架构

源码路径：`src/memdir/paths.ts`、`src/memdir/memdir.ts`

### 目录布局与路径解析

```
~/.claude/projects/<sanitized-git-root>/memory/
├── MEMORY.md                    ← 入口索引（每次对话加载）
├── user_role.md                 ← 用户记忆
├── feedback_testing.md          ← 反馈记忆
├── project_mobile_release.md    ← 项目记忆
├── reference_linear_ingest.md   ← 参考记忆
├── private/                     ← 私有记忆目录（TEAMMEM模式）
│   ├── MEMORY.md
│   └── ...
└── team/                        ← 团队记忆目录（TEAMMEM模式）
    ├── MEMORY.md
    └── ...
```

路径解析遵循优先级链：`CLAUDE_COWORK_MEMORY_PATH_OVERRIDE` 环境变量（SDK 覆盖）→ `autoMemoryDirectory` 设置（仅限 policySettings/localSettings/userSettings，**故意排除** projectSettings 防止安全风险）→ 默认路径。

关键安全约束：`validateMemoryPath()` 拒绝相对路径、Windows 驱动器根、UNC 网络路径和包含空字节的路径。`~/` 展开也有限制，防止 `~/.ssh` 等敏感目录被意外匹配。

### MEMORY.md 索引机制

`src/memdir/memdir.ts:35-38`

```typescript
export const ENTRYPOINT_NAME = 'MEMORY.md'
export const MAX_ENTRYPOINT_LINES = 200
export const MAX_ENTRYPOINT_BYTES = 25_000
```

索引采用**双重上限保护**：200 行 AND 25KB。超过任一限制都会被 `truncateEntrypointContent()` 截断并追加警告。这种设计针对两种失败模式：p97 的索引文件用 200 行就能覆盖（行数限制），但 p100 观测到 197KB/200 行的异常条目（字节限制兜底）。

索引格式简洁：每条记忆一行，150 字符以内。`MEMORY.md` 本身**没有 frontmatter**，它只是一个链接列表。

## 四类型分类法

源码路径：`src/memdir/memoryTypes.ts`

记忆被约束为**封闭的四类型系统**，每种类型有明确的语义边界和保存时机：

| 类型 | 作用域 | 存储内容 | 典型触发场景 |
| --- | --- | --- | --- |
| **user** | 始终私有 | 用户角色、技术背景、偏好 | "我是数据科学家"、"写了十年 Go" |
| **feedback** | 默认私有，例外时团队 | 用户对 AI 行为的纠正和确认 | "别 mock 数据库"、"对，就是这样" |
| **project** | 强烈推荐团队 | 非代码可推导的项目上下文 | "合并冻结周四开始"、"合规驱动 auth 重写" |
| **reference** | 通常团队 | 外部系统指针 | "pipeline bugs 在 Linear INGEST" |

### 反馈类型的双通道捕获

`feedback` 类型的保存指令特别强调：**既要从失败中记录，也要从成功中记录**。如果只保存纠正，AI 会避免过去错误但会逐渐偏离已被用户验证的方法。确认比纠正更难捕捉，但同等重要——它防止 AI 行为随时间漂移。

### 记忆的严格排除规则

系统明确禁止保存**可从当前项目状态推导的信息**：

*   代码模式、架构、文件路径——可实时读取
*   Git 历史、最近变更——`git log`/`git blame` 更权威
*   调试方案或修复配方——代码和 commit message 已有
*   CLAUDE.md 中已记录的内容
*   临时状态和当前对话上下文

这些排除规则即使在用户明确要求保存时也适用。如果用户要求保存本周 PR 列表，系统会引导用户提取其中**出乎意料或非显而易见**的部分。

## 智能召回机制

源码路径：`src/memdir/findRelevantMemories.ts`、`src/memdir/memoryScan.ts`

### 召回流程

```
sequenceDiagram
    participant U as 用户消息
    participant FR as findRelevantMemories
    participant MS as scanMemoryFiles
    participant SQ as selectRelevantMemories
    participant S as Sonnet侧查询
    
    U->>FR: findRelevantMemories(query, memoryDir)
    FR->>MS: scanMemoryFiles() — 扫描所有.md文件
    MS-->>FR: MemoryHeader[] (filename, description, type)
    FR->>SQ: selectRelevantMemories(query, headers)
    SQ->>S: sideQuery() — 轻量Sonnet调用
    S-->>SQ: selected_memories: string[]
    SQ-->>FR: string[]
    FR-->>U: RelevantMemory[] (path, mtimeMs)
```

核心是 `selectRelevantMemories()` 函数，它通过 `sideQuery()` 调用轻量级 Sonnet 模型（非主模型）进行相关性筛选：

```typescript
// findRelevantMemories.ts:98-121
const result = await sideQuery({
  model: getDefaultSonnetModel(),  // 用 Sonnet 做筛选
  system: SELECT_MEMORIES_SYSTEM_PROMPT,
  messages: [{
    role: 'user',
    content: `Query: ${query}\n\nAvailable memories:\n${manifest}${toolsSection}`
  }],
  max_tokens: 256,
  output_format: { type: 'json_schema', schema: { ... } },
})
```

### 近期工具去噪

当 AI 正在使用某工具时，召回该工具的使用文档是噪音（对话中已有工作上下文）。`recentTools` 参数让召回系统跳过这些记忆，但**保留**关于这些工具的警告、陷阱或已知问题——这正是使用时最关键的信息。

### 已展示去重

`alreadySurfaced` 参数过滤之前轮次已展示过的文件路径，让 Sonnet 的 5 槽预算花在新的候选上。

## 会话记忆（Session Memory）

源码路径：`src/services/SessionMemory/sessionMemory.ts`

会话记忆自动维护一个 Markdown 文件，记录当前对话的关键信息。它通过**forked 子 agent** 在后台周期性提取，不打断主对话流程。

### 触发阈值

会话记忆的提取遵循三个阈值条件：

| 阈值类型 | 默认值 | 说明 |
| --- | --- | --- |
| `minimumMessageTokensToInit` | 10,000 | 初始化最小上下文 tokens |
| `minimumTokensBetweenUpdate` | 5,000 | 两次更新间最小上下文增长 |
| `toolCallsBetweenUpdates` | 3 | 两次更新间最小工具调用数 |

提取触发条件：**token 阈值必须满足** +（tool call 阈值满足 **或** 上一轮无工具调用）。无工具调用条件确保在自然对话间隙提取。

### 文件结构模板

会话记忆使用结构化模板：

```gfm
# Session Title
_5-10词描述性标题，信息密集_

# Current State
_当前活跃工作内容？未完成的待办？下一步？_

# Task specification
_用户要求构建什么？设计决策？_

# Files and Functions
_重要文件？它们包含什么？为什么相关？_

# Workflow
_常用 bash 命令及其顺序？如何解读输出？_

# Errors & Corrections
_遇到的错误及修复方法。用户纠正了什么？_

# Learnings
_什么效果好？什么不好？要避免什么？_

# Key results
_用户请求的具体输出（表格、答案等）_
```

### 与上下文压缩的集成

源码路径：`src/services/compact/sessionMemoryCompact.ts`

当上下文压缩发生时，`sessionMemoryCompact.ts` 负责**保留会话记忆中的关键信息**。它会识别哪些消息包含会话记忆内容，并在压缩边界处添加特殊标记，确保压缩后的消息序列仍然包含必要的会话记忆引用。

## 后台记忆提取（extractMemories）

源码路径：`src/services/extractMemories/extractMemories.ts`

后台记忆提取在**每个完整查询循环结束时**运行（当模型产生无工具调用的最终响应时），通过 `handleStopHooks` 触发。它使用 forked agent 模式——主对话的完美分叉，共享父级的 prompt cache。

### 与主 Agent 的协同

主 Agent 的 system prompt 始终有完整的保存指令。当主 Agent 自己写入了记忆时，后台 agent 会跳过那段范围（`hasMemoryWritesSince` 检查）。两者互斥：主 Agent 写则后台跳过，主 Agent 不写则后台捕获遗漏。

### 工具权限限制

后台 agent 的工具权限受到严格限制：

*   **允许**：Read/Grep/Glob（无限制）、只读 Bash 命令
*   **限制**：Edit/Write 仅限 `auto-memory` 目录内
*   **禁止**：Bash `rm`、目录外文件操作

```typescript
// extractMemories.ts:137-170
export function createAutoMemCanUseTool(memoryDir: string): CanUseToolFn {
  return async (tool: Tool, input: Record<string, unknown>) => {
    // 允许 Read/Grep/Glob 无限制
    if (tool.name === FILE_READ_TOOL_NAME || 
        tool.name === GREP_TOOL_NAME || 
        tool.name === GLOB_TOOL_NAME) {
      return { behavior: 'allow' }
    }
    // 允许只读 Bash
    if (tool.name === BASH_TOOL_NAME) {
      if (parsed.success && tool.isReadOnly(parsed.data)) {
        return { behavior: 'allow' }
      }
      return denyAutoMemTool(tool, ...)
    }
    // Edit/Write 仅限 memoryDir
    // ...
  }
}
```

## 团队记忆同步

源码路径：`src/services/teamMemorySync/index.ts`

团队记忆在 Git repo 范围内共享（通过 git remote hash 标识），所有认证组织成员可访问。

### API 契约

```
GET  /api/claude_code/team_memory?repo={owner/repo}           → TeamMemoryData（含 entryChecksums）
GET  /api/claude_code/team_memory?repo={owner/repo}&view=hashes → 仅 metadata + entryChecksums
PUT  /api/claude_code/team_memory?repo={owner/repo}           → 上传 entries（upsert 语义）
```

### 同步语义

*   **拉取**：服务器内容覆盖本地文件（服务器胜出）
*   **推送**：仅上传内容 hash 与 `serverChecksums` 不同的条目（增量上传）
*   **删除不传播**：删除本地文件不会从服务器移除，下次拉取会恢复

### 敏感信息防护

团队记忆同步包含**密钥扫描机制**（`secretScanner.ts`）。在上传前扫描记忆内容，拒绝包含潜在敏感信息（如 API 密钥、凭证模式）的文件。

## 记忆注入链路

源码路径：`src/memdir/memdir.ts` → `src/context.ts`

`loadMemoryPrompt()` 是记忆注入的入口，每会话调用一次（通过 `systemPromptSection('memory', ...)` 缓存）：

```typescript
// memdir.ts:419-507
export async function loadMemoryPrompt(): Promise<string | null> {
  const skipIndex = getFeatureValue_CACHED_MAY_BE_STALE('tengu_moth_copse', false)
  
  // KAIROS 日志模式优先
  if (feature('KAIROS') && autoEnabled && getKairosActive()) {
    return buildAssistantDailyLogPrompt(skipIndex)
  }
  
  // TEAMMEM 组合模式
  if (feature('TEAMMEM') && teamMemPaths!.isTeamMemoryEnabled()) {
    return teamMemPrompts!.buildCombinedMemoryPrompt(extraGuidelines, skipIndex)
  }
  
  // 纯自动记忆
  if (autoEnabled) {
    return buildMemoryLines('auto memory', autoDir, extraGuidelines, skipIndex).join('\n')
  }
  
  return null
}
```

注入时机：`context.ts` 中 `getSystemContext()` 调用时，记忆 Prompt 作为 system prompt 的一个 section 被组装。`MEMORY.md` 的实际内容作为 **user context message** 注入（而非 system prompt），这样可以利用 Prompt Cache 的 prefix 共享。

## 记忆漂移防御

源码路径：`src/memdir/memoryTypes.ts`（`TRUSTING_RECALL_SECTION`）

记忆可能过期。系统设置专门的 "Before recommending from memory" section：

> A memory that names a specific function, file, or flag is a claim that it existed _when the memory was written_. It may have been renamed, removed, or never merged. Before recommending it:
> 
> *   If the memory names a file path: check the file exists.
> *   If the memory names a function or flag: grep for it.

这个 section 的标题经过 A/B 测试验证："Before recommending from memory"（行动导向）比 "Trusting what you recall"（抽象描述）效果好。

## CLI 命令

源码路径：`src/commands/memory/memory.tsx`

`/memory` 命令打开记忆文件选择器：

```typescript
// memory.tsx
export const call: LocalJSXCommandCall = async onDone => {
  clearMemoryFileCaches()
  await getMemoryFiles()
  return <MemoryCommand onDone={onDone} />
}
```

使用 `$EDITOR` 或 `$VISUAL` 环境变量配置的编辑器打开选中的记忆文件。

## 配置与 Feature Gates

| 功能 | Feature Flag | 配置项 |
| --- | --- | --- |
| 自动记忆 | `tengu_passport_quail` | `isExtractModeActive()` |
| Team Memory | `feature('TEAMMEM')` | `tengu_herring_clock` |
| KAIROS 日志 | `feature('KAIROS')` | `getKairosActive()` |
| 搜索历史上下文 | `tengu_coral_fern` | `buildSearchingPastContextSection()` |
| 跳过 MEMORY.md 索引 | `tengu_moth_copse` | `skipIndex` 参数 |
| 记忆形状遥测 | `feature('MEMORY_SHAPE_TELEMETRY')` | `logMemoryRecallShape()` |

## 关键设计原则

1.  **文件即存储**：无数据库、无向量存储，只有 Markdown 文件
2.  **封闭类型系统**：四种记忆类型覆盖所有不可推导的上下文
3.  **双重召回**：入口索引全量加载 + 智能筛选按需召回
4.  **主从协同**：主 Agent 和后台 Agent 互斥，不重复工作
5.  **增量同步**：团队记忆使用 SHA256 hash 比较实现增量上传
6.  **安全优先**：路径验证、敏感信息扫描、工具权限限制多层防护

## 相关文档

*   [系统提示组装](6-wu-ceng-jia-gou-she-ji.md) — 记忆如何融入 system prompt
*   [上下文压缩](7-agentic-loop-he-xin-xun-huan.md) — 与会话记忆的集成
*   [五层架构设计](6-wu-ceng-jia-gou-she-ji.md) — 记忆系统在整体架构中的位置

## 相关条目
- [[19-agent-xie-diao-mo-shi]]
- [[21-zi-ding-yi-agents]]
- [[多智能体与记忆机制]]
