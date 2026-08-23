# S级核心亮点专项

> 面向新人的核心亮点详解 · 通俗语言 + 术语释义 + 阅读路线
>
> 📑 返回索引：[项目文档索引](项目文档索引.md)

## S级总览表格

| 排名 | 亮点标题 | 源码完整度 | 文档价值 | 系统定位 | 简述 |
|------|---------|-----------|---------|---------|------|
| S1 | V2 Session Core 准入/执行分离 | 高（core/session 全链路） | 极高 | 会话可靠性 | 先存后跑，崩溃不丢输入 |
| S2 | Context Epoch 上下文纪元 | 高（system-context + context-epoch） | 极高 | 上下文工程化 | 基线不变、增量更新、压缩重置 |
| S3 | SDK Contract IR 代码生成 | 高（httpapi-codegen + client） | 极高 | 平台化 | 一份协议契约生成多套客户端 |
| S4 | 嵌入式 Host（sdk-next） | 高（opencode.ts） | 高 | 平台化 | 进程内跑全套服务，零网络 |
| S5 | SessionRunner 单次流式 + 续跑 | 高（runner/llm.ts） | 高 | 会话编排 | 一轮一问，工具循环可续 |
| S6 | 工具输出有界化 | 高（truncate.ts + ToolOutputStore） | 高 | 上下文安全 | 大输出截断落盘，防上下文爆炸 |

---

## S1：V2 Session Core 准入/执行分离

### 1. 通俗概述

你发一句话，系统先把这句话**安全地记到硬盘上**，然后才开始让 AI 干活。这样就算中途程序崩溃，这句话也不会丢，重启后还能接着干。

### 2. 业务背景

编码助手的使用方是开发者，他们依赖"会话不丢失"。若崩溃即丢输入，续接（--continue）、分叉（--fork）等功能都会失效。这是整个产品可靠性的基石。

### 3. 术语通俗释义

| 术语 | 通俗解释 | 代码体现位置 |
|------|---------|-------------|
| Admitted Prompt | 已收下但还没给 AI 看的话 | `session_input` 表 |
| Prompt Promotion | 到点把收下的话正式递给 AI | `SessionInput.promoteNextQueued` |
| Session Drain | 一次"从收到话到答完话"的干活过程 | `session/execution.ts` |
| wake 合并 | 干活途中又来了新话，合并到当前这轮 | `session/run-coordinator.ts` |

### 4. 代码入口链路

`packages/opencode/src/cli/cmd/run.ts` → server handler → `SessionV2.prompt()` → `SessionInput.admit` → `SessionExecution.wake` → `SessionRunCoordinator` → `SessionRunner`

### 5. 核心文件清单

| 路径 | 作用 | 理解顺序 |
|------|------|---------|
| `packages/core/src/session.ts` | SessionV2 门面：查询/创建/消息 | 1 |
| `packages/core/src/session/input.ts` | 准入/提升/排队核心 | 2 |
| `packages/core/src/session/run-coordinator.ts` | 并发协调器 | 3 |
| `packages/core/src/session/execution.ts` | 执行调度 Service | 4 |
| `packages/core/src/session/runner/llm.ts` | 单轮执行编排 | 5 |

### 6. 主流程分步解析

1. 用户输入 → `admit` 写入 session_input（定 admitted_seq）
2. 发布 SessionEvent.PromptAdmitted
3. wake 调度 → 协调器判断是否已有活跃 drain
4. 安全边界处 promote 提升输入为模型可见消息
5. runner 执行 Provider Turn，完成输出投影

### 7. 方案取舍清单

- 多一次 DB 写入 vs 崩溃可恢复（选择后者）
- 进程本地协调 vs 集群化（当前选本地，集群为 TODO）
- 精确重试（Session+Prompt+delivery 全匹配）vs 宽松重试（防止误重放）

### 8. 新人阅读路线

先读 `input.ts` 的 admit/promote 概念 → 再读 `run-coordinator.ts` 理解并发 → 最后读 `runner/llm.ts` 看执行细节。

---

## S2：Context Epoch 上下文纪元

### 1. 通俗概述

AI 能"记住"的内容有个上限。系统把每次给 AI 的完整背景知识打包成一个**"快照纪元"**：纪元内背景不变，变化只发"小纸条"（增量更新）；背景太大时压缩一次、开新纪元。

### 2. 业务背景

长会话中，模型上下文会越积越多（环境信息、日期、项目指令、Skill 列表…）。若无纪元管理，每次变更都要重发全部背景，既慢又费 token；压缩时机也无法对齐。

### 3. 术语通俗释义

| 术语 | 通俗解释 | 代码体现位置 |
|------|---------|-------------|
| Baseline System Context | 纪元开始时给 AI 的完整背景 | `session_context_epoch.baseline` |
| Context Snapshot | 记录每个背景源的"上次状态" | `system-context/index.ts` Snapshot |
| Mid-Conversation Message | 背景变化时发的"小纸条" | `SystemContext.reconcile` |
| Safe Boundary | 只在这个安全时刻才看背景变没变 | runner 调度点 |

### 4. 核心文件清单

| 路径 | 作用 | 理解顺序 |
|------|------|---------|
| `packages/core/src/system-context/index.ts` | Source 定义 + initialize/reconcile/replace | 1 |
| `packages/core/src/system-context/registry.ts` | 注册与并发组合 | 2 |
| `packages/core/src/session/context-epoch.ts` | 纪元持久化与推进 | 3 |
| `packages/core/src/system-context/builtins.ts` | 内置源（env/date） | 4 |

### 5. 设计思路

选择"不可变基线 + 增量更新 + 惰性采样"组合：基线不可变保证模型看到的前缀稳定（利于 Provider 缓存）；更新只发差异减少 token；惰性采样避免并发变更撕裂视图。

### 6. 方案取舍清单

- 跨进程复用基线（省 token）vs 每次全新渲染（简单）
- 增量更新（省 token）vs 全量替换（简单直接）
- Unavailable 时保留旧状态（稳）vs 直接移除（简单）

### 7. 新人阅读路线

先读 `system-context/index.ts` 的 Source 接口 → 读 `context-epoch.ts` 的 initialize/reset → 最后看 builtins 体会真实 Source 长什么样。

---

## S3：SDK Contract IR 代码生成

### 1. 通俗概述

后端定义一份"接口说明书"（HttpApi），工具自动把它编译成"中间表示"，再自动生成两套客户端代码（传统 Promise 版、函数式 Effect 版）。改接口只改一处，客户端自动跟着变。

### 2. 业务背景

多端（TUI/Web/Desktop/嵌入式）都要调用同一套后端接口。手写客户端必然漂移；一份契约生成多端客户端是平台化的关键。

### 3. 术语通俗释义

| 术语 | 通俗解释 | 代码体现位置 |
|------|---------|-------------|
| HttpApi | 接口说明书 | `packages/protocol/src/api.ts` |
| SDK Contract IR | 编译后的中间表示 | `packages/client/src/contract.ts` |
| Emitter | 把中间表示翻译成具体语言的生成器 | `generated/`、`generated-effect/` |
| ClientError | 基础设施错误（连不上、超时）的统一类型 | `generated/` 错误映射 |

### 4. 主流程

1. Server 定义 HttpApi（18 组端点）
2. 编译为 SDK Contract IR（保留类型投影 + 传输元数据）
3. httpapi-codegen 构建期生成两套代码
4. 根导出零 Effect（浏览器安全）；/effect 提供富投影（runtime 解码）

### 5. 方案取舍清单

- 生成代码（一致但体积大）vs 手写（灵活但易漂移）
- 双 emitter（两套语义）vs 单 emitter（简单）
- 生成代码禁止手改（强制）vs 允许局部覆盖（灵活）

### 6. 新人阅读路线

读 `contract.ts` 理解 IR 形状 → 看 `generated/` 中一个端点方法的实现 → 对比 `generated-effect/` 同一端点。

---

## S4：嵌入式 Host（sdk-next）

### 1. 通俗概述

把"整个服务器"装进你的程序进程里跑，不占网络端口、不额外起进程，还能像用远程客户端一样调用它——这就是"嵌入式模式"。

### 2. 业务背景

CLI 的 attach 模式、桌面端 sidecar、测试环境都需要"不开网络也能完整使用 OpenCode"的能力。网络客户端与嵌入式共用同一契约，保证行为一致。

### 3. 核心文件清单

| 路径 | 作用 | 理解顺序 |
|------|------|---------|
| `packages/sdk-next/src/opencode.ts` | OpenCode.create 组装 | 1 |
| `packages/server/src/routes.ts` | createEmbeddedRoutes | 2 |
| `packages/client/src/contract.ts` | 共享契约 | 3 |

### 4. 主流程

1. OpenCode.create 在 Scope 内构建 Core（Layer.buildWithMemoMap）
2. createEmbeddedRoutes 生成 webHandler → 包装成 fetch
3. FetchHttpClient 注入 Client → 返回统一能力面
4. Scope.close() 释放数据库/注册/fiber

### 5. 方案取舍清单

- 内存 Router（零网络）vs 网络服务（可跨进程）
- Scope 生命周期（显式关闭）vs GC 兜底（不可靠）
- 共用 HttpApi（一致）vs 嵌入式专有 API（更高效但分叉）

---

## S5：SessionRunner 单次流式 + 续跑

### 1. 通俗概述

每轮对话，系统只对 AI 发**一次**请求。AI 想用工具？工具跑完，系统把结果再发一次请求续上。循环在"一次请求 + 若干次续跑"里完成，不会失控乱发。

### 2. 核心文件清单

| 路径 | 作用 | 理解顺序 |
|------|------|---------|
| `packages/core/src/session/runner/llm.ts` | 主编排：单次 stream + 工具结算 + 续跑 | 1 |
| `packages/core/src/session/runner/model.ts` | 模型解析 | 2 |
| `packages/core/src/session/runner/to-llm-message.ts` | 历史投影为模型消息 | 3 |

### 3. 设计思路

V1 的 SessionPrompt 是巨型单体循环（runLoop 约 1081 行），难以测试与扩展。V2 拆为"协调者 + 小协作件"，每个 Provider Turn 只调一次 llm.stream，工具结算在 FiberSet+Semaphore 下并行，Compaction 通过 TurnTransitionError 触发续跑。

### 4. 方案取舍清单

- 单次 stream（可控）vs 多次并发 stream（快但乱）
- 工具并行结算（快）vs 串行（简单）
- TurnTransitionError 续跑（灵活）vs 抛出重来（浪费）

---

## S6：工具输出有界化

### 1. 通俗概述

工具返回的内容如果太大（比如读完整个大文件），系统只把**开头和结尾**给 AI 看，完整的存到临时文件，并提示 AI 用搜索/读取工具按需取用。防止一次输出把上下文撑爆。

### 2. 核心文件清单

| 路径 | 作用 | 理解顺序 |
|------|------|---------|
| `packages/opencode/src/tool/truncate.ts` | 截断策略（2000 行 / 50KB） | 1 |
| `packages/core/src/tool-output-store` | 落盘管理（7 天保留） | 2 |
| `packages/core/src/tool/registry.ts` | 最终限长强制 | 3 |

### 3. 设计思路

"通用截断保留首尾 + 工具可自定义更有意义策略 + Registry 强制最终限制"三层。截断文件路径是全局唯一平铺目录，可被普通工具搜索读取。

### 4. 异常场景

- 结构化结果超限：保留原值给会话消费者，模型回放用有界 JSON 预览
- 落盘失败：记录"有损有界输出"（无路径），不改变工具成功语义
- 保留期后：文件可过期删除；有界输出本身是持久记录

---

*由 opencode-project-analyzer skill 生成*
