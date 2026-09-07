---
created: 2026-09-07
updated: 2026-09-07
title: 面向编码智能体的上下文工程（从零构建编码智能体，第 4 课）
sourceUrl: https://www.decodingai.com/p/context-engineering-for-coding-agents
sourceAuthor: Paul Iusztin（Decoding AI Magazine）
translatedAt: 2026-09-07
sources: [references/articles.md 待处理队列]
tags: [AI Agent, 上下文工程, Harness 工程, 记忆, Skills, LSP, Compaction, 从零构建编码智能体, type/翻译]
---

# 面向编码智能体的上下文工程

> Decoding AI Magazine 公开课「Building a Coding Agent From Scratch」第 4 课｜发布于 2026-08-25
> 作者：[Paul Iusztin](https://substack.com/@pauliusztin)
> 课程仓库：[github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course)｜用 Python 从零构建编码智能体 **Decode**

> **让上下文窗口保持高信号的 4 个 harness 组件。**

**凡是用智能体包裹起来的 AI 应用，都是一个 harness！**

在 LangChain 的 Terminal-Bench 实验里，只更换 harness（模型不变），就让一个编码智能体从约第 30 名跃升进前 5：决定编码智能体好坏的，是 harness，不是模型。

在这门开源课程 **[Building a Coding Agent From Scratch](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course)** 中，你会用 Python 从零构建那个 harness：**Decode**——一个完整的编码智能体，它随着课程的推进，从一条裸露的智能体循环，长成一个并行运行在云端、由远程智能体组成的集群。

**为什么？** 你将能为自己的 AI 产品定制 harness（这正是那次榜单跃升背后的技能），也会真正理解 Claude Code 和 Codex 在底层到底做了什么，从而成为进阶用户。

**图 1**（课程演示 GIF，无文字说明；图片 URL 见来源文件）

**课程目录：**

1. [Building a Coding Agent From Scratch](https://www.decodingai.com/p/building-a-coding-agent-from-scratch-system-design)
2. [The Bare-Bones Coding Agent Loop](https://www.decodingai.com/p/the-coding-agent-loop)
3. [From a Raw Shell to a Sandboxed Coding Agent](https://www.decodingai.com/p/run-coding-agents-safely)
4. **Context Engineering for Coding Agents** **←** _**你在这里**_
5. [Subagents Are Context Engineering](https://www.decodingai.com/p/subagents-are-context-engineering)
6. Remote Headless Mode & Durability
7. AI Evals Foundations: Benchmarks, Regression and Online
8. AI Evals on Steroids via Replays

[查看完整开源课程](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course)

**图 2**（课程开篇题图，原文字：*你随身携带的东西，决定了你能走多远；手艺在于你留在工作台上的那些。*）——这句题词正是上下文工程的缩影：窗口里放什么、不放什么，是编码智能体质量的胜负手。

我曾痴迷于让 Claude Code 智能体 7×24 小时连轴转：回邮件、做饭、看电影的同时，事情也能被搞定。直到某次任务进行到一半，我的订阅额度在回合中间被耗尽——智能体正卡在一个功能做到一半的状态。听起来很熟悉？

向老板抱怨、买更大的订阅、换模型、或者换个 harness，都只是在治标。它们没有解决根本问题。你花了钱，窗口却依旧嘈杂，无论背后是哪个模型，输出质量都在下降。

真正的解法是更深入地理解 harness，以及它背后的上下文工程：改进规划，建立更强的技能（skills）与记忆（memory），并且知道什么时候该丢弃你的上下文。

到目前为止，课程聚焦在 harness 工程与构建沙箱化的智能体循环上。现在，终于轮到编码智能体的上下文工程了：记忆、技能、LSP 服务器与压缩（compaction）。

整个问题最终归结为：往上下文里放什么、不放什么、如何裁掉冗余，以及为智能体创造尽可能多的反馈回路——正如 Anthropic 所概括的，[找到尽可能小的一组高信号 token](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)。

学完这一课，你将理解并从零构建出：

- 智能体在会话之间应该携带什么。
- 技能如何做到「需要之前什么都不加载」。
- 整个系统里最便宜的反馈回路。
- 窗口如何在腐烂之前被裁剪。

## 一次会话的上下文生命周期（The context lifecycle of a session）

要看这 4 个组件如何协作，请看课程仓库里的 `demo-5-sandbox-feature-pr` 技能（`.decode/skills/demo-5-sandbox-feature-pr`）。我们在这个 demo 里编码了这样一个场景：**Decode** 通过拉起一个后台的沙箱会话，给 Decode 自己写一个新功能——宿主导航智能体（host agent）充当编排者，沙箱里的那个充当功能执行者。这个 demo 的最终产物，是一份包含新功能的 PR。

打开[仓库](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course)，运行 `decode`，输入 `/demo-5-sandbox-feature-pr` 并回车，剩下的交给 Decode 就好。

**图 3**（skill demo 截图）技能快照——Decode 派生出另一个 Decode 子智能体：

```
...

## 1. Launch decode against a sandboxed clone of the course repo

Launch the local Docker run (Docker must be running):

"""
SANDBOX_MODE=docker decode --repo git@github.com:decodingai-magazine/building-a-coding-agent-from-scratch-course.git
"""

...
```

会话启动时，系统提示词由四部分拼装而成：基础提示词、当前智能体的提示词、记忆文件（`AGENTS.md` ＋ `.decode/MEMORY.md`）、以及技能目录（每个技能一行）。Pydantic AI 会再追加每个工具的模式（schema）——这正是[第 2 课](https://www.decodingai.com/p/the-coding-agent-loop)那句「每个工具都要烧 token」的告诫。拼装好的提示词进入上下文，塑造模型下一步行为的概率分布。

随后运行开始填满窗口。调用技能会加载它的 `SKILL.md` 正文（渐进式披露的第 2 级）。规划模式会把仓库文件以 `read` 输出的形式倒进上下文。在构建循环中，每一次 `edit` 落盘，诊断信息增强器（Diagnostics Enricher）就免费追加一批类型错误，`bash` 则运行测试，直到绿色输出宣告完成。

_现在，站在上下文窗口的角度看，harness 内部发生了什么？_

如下面的图所示：我们一打开智能体，上下文窗口就被它的系统提示词、工具与技能描述、记忆文件填满；调用 `/demo-5-sandbox-feature-pr` 技能之后，窗口又会被工具输入/输出，以及包含具体指令的 `SKILL.md` 文件填满。

接下来，通过渐进式披露，智能体开始读取与该技能相关的文件和脚本。最终，它开始写新的 Python 文件、或编辑既有文件——这些文件经由我们的 `ty`（Language Server Protocol，LSP）服务器做静态语法检查。

**图 4**（示意图）编码智能体的上下文生命周期——同一会话的每一轮迭代往窗口里追加了什么。

在 Modal 自托管的 `Qwen3.6-35B` 上，窗口是 262,144 个 token。通常微压缩（microcompaction）在 60% 时触发，全量压缩（full compaction）在 80% 时触发。压缩之后，用量会回落到大约 5–10%，于是会话得以继续，而不是崩掉。

在下面的视频里，你可以看到 [Opik](https://www.comet.com/site/?utm_source=newsletter&utm_medium=partner&utm_campaign=paul&utm_content=coding_agent_course) 中 219 个 span 的链路追踪的一部分——它清晰地监控了 harness 与 LLM 调用的工具调用、token 计数与延迟。（原文为内嵌视频演示，无法在译文中内嵌。）

这个生命周期里的每个组件都有各自的机制：记忆、技能、LSP 服务器与压缩。我们逐一来看。

## 记忆：别再重复你的指令（Memory: Stop repeating your instructions）

在我早期的智能体运行中，智能体老是写 naive 的 datetime 对象而不是带时区的，类型注解也加得前后不一，害我不得不在一个又一个会话里重复输入同样的修正。解决办法是：把偏好一次性写进 `AGENTS.md`，让智能体在每一轮都读到它。

**图 5**（示意图）两份记忆文件——一份你手写，一份自己写自己：`AGENTS.md`（你手动定义的那份）对比 `.decode/MEMORY.md`（智能体从每个会话中自动提取的那份）。

`AGENTS.md` 注入的是项目上下文：业务逻辑、组件为什么存在、技术栈，以及围绕它的一系列流程（文档、部署、评审、测试）。代码才是事实来源（source of truth），所以要避免在文件里重复代码。放的是元数据与引用——那些智能体无需重度推理就能发现的信息。

把 `AGENTS.md` 控制在 300 行以内，并设一个约 600 行的护栏。每一行都应该针对一个你观察到的错误而写，好让智能体不再重犯——遵循 [Mitchell Hashimoto 的规则](https://mitchellh.com/writing/my-ai-adoption-journey)。

Decode 会递归地在项目的所有目录里查找 `AGENTS.md` 文件（从最靠近根目录的开始，因此最近的这份优先级最高），最后再追加上 `.decode/MEMORY.md`，给每一份都盖上 `# From <path>` 的溯源头，然后整体倒进系统提示词。

如果说 `AGENTS.md` 是你手动定义的，那 `.decode/MEMORY.md` 就是智能体自动从对话里提取出来的——复刻了 Claude Code 的自动记忆（auto-memory）。在每个会话结束时——无论是退出还是执行 `/clear`——都会用一次廉价的 LLM 调用，把会话压成一句平实的话，作为带日期的条目追加进去（`- 2026-06-26: …`），形成一份只追加（append-only）的日志。这个文件会长得很快，所以设有硬上限：200 行或 25,000 字节，超出时先丢最旧的行。

_摘录自 [src/decode/memory/extract.py](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/main/src/decode/memory/extract.py)：_

```
async def extract_on_exit(messages: list[ModelMessage], cwd: Path) -> None:
    summary = await summarize_session(messages, model_or_settings=settings)
    append_session_summary(cwd, summary, now=_utc_now())

    if settings.memory_compression_enabled:
        await compress_memory_file(cwd, model_or_settings=settings)
```

`summarize_session` 就是那唯一一次 LLM 调用——把对话蒸馏成一句话（如果不值得保存则返回 `None`）。`append_session_summary` 把这句话写进 `.decode/MEMORY.md` 并执行硬上限。

`compress_memory_file` 运行**记忆压缩（Memory Compression）**，就地重写文件：合并重复或已被取代的笔记，同时保留带日期的条目。

## 技能：能引用的就不加载（Skills: Never load what you can reference）

我的 Python 测试与 PR 约定以前直接住在记忆文件里，结果把每个会话的上下文都撑肥了。把它们移进技能之后，记忆文件里只剩几行引用，指明各自在什么时候该去访问哪个技能。

技能从两个方向防止上下文腐烂。在工具侧，前置的 schema 会白白烧掉预算：[Mario Zechner 实测发现，流行的 MCP 服务器在正式开始干活之前，就要消耗上下文窗口的 7–9%](https://mariozechner.at/posts/2025-11-30-pi-coding-agent/)。在记忆侧，把评审指南、工作流模板塞进 `AGENTS.md`，会污染每一轮对话。技能两头都解决：每个阶段特有的行为住进自己的技能，由目录里一行引用指向它，只有在该工作流阶段运行时才加载。

**图 6**（示意图）上下文窗口里看到的渐进式披露的三个层级——技能与其打包文件的 3 种加载层级。

技能遵循 [Agent Skills 标准](https://agentskills.io/home)。在 Decode 中，技能放在 `.decode/skills/` 下，也可以打开 TUI、输入 `/` 挑选。另有一个独立公开注册表 [skills.sh](https://www.skills.sh/)（`npx skills install <skill>`）：

```
my-skill/
├── SKILL.md          # Required: metadata + instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: documentation
├── assets/           # Optional: templates, resources
└── ...               # Any additional files or directories
```

**渐进式披露（progressive disclosure）** 在 **3 个层级**上运作。**第 1 级**：只有技能目录留在上下文里——每个技能一行 `名称 + 描述`。随着技能库变大，一个可选的护栏可以把目录限制在上下文窗口的约 1%。

**图 7**（示意图）第 1 级技能流水线——把描述汇总成目录、可选地上限封顶、再包进系统提示词：*把技能目录加载进系统提示词。*

Decode 还没有实现的一个常见策略是「仅限用户调用」（user-invocable-only）的技能：你把某个技能标记为仅可调用。这意味着可以从目录里去掉它的名称与描述，在用户显式调用之前，它占用的上下文为零。

**第 2 级**：通过 `skill` **调度工具**或 `/<skill-name>` 调用技能时，只加载它的 `SKILL.md` 正文，以及打包在技能里的其它文件。

_摘录自 [src/decode/tools/skills.py](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/main/src/decode/tools/skills.py)：_

```
async def skill(ctx: RunContext[AgentDeps], name: str) -> str:
    home = ctx.deps.harness_home or ctx.deps.cwd
    catalog = load_skills(home)
    found = catalog.get(name)

    return format_skill_payload(found, cwd=home)
```

**第 3 级**：在 `format_skill_payload` 内部，我们把技能的所有可用资源（文件、脚本、文档、assets）正确地格式化并暴露给智能体；如果智能体认为必要，就会通过它的 read 工具加载它们，或用 bash 工具执行其中的脚本。

这就是渐进式披露的核心思想。它其实主要是暴露一份打包文件的清单，带上精确的 cwd 相对路径，让智能体极其清楚该如何访问。关键在于：LLM 经过工具调用的充分训练，能对「该不该调用 read 或 bash 工具」做出正确决策。

_摘录自 [src/decode/skills/payload.py](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/main/src/decode/skills/payload.py)：_

```
def format_skill_payload(skill: SkillDef, *, cwd: Path) -> str:
    if skill.resource_dir is None:
        return f"{skill.body}\n\n{_OUTPUTS_TRAILER}"
    rel_dir = os.path.relpath(skill.resource_dir, cwd)
    files = _bundled_files(skill.resource_dir)

    listing = "\n".join(f"- {rel_dir}/{name}" for name in files)
    trailer = (
        f"Bundled files for this skill (all under `{rel_dir}/` — use these EXACT paths):\n"
        f"{listing}\n"
        "Read them with the `read` tool; run `scripts/` files with `bash`."
    )

    return f"{skill.body}\n\n{trailer}\n\n{_OUTPUTS_TRAILER}"
```

接下来，看看整个编码智能体里最便宜的那个反馈回路。

## LSP 服务器：用精确取代猜测（The LSP server: Replace guessing with precision）

在我多智能体的配置里，工程师智能体与测试智能体之间的每一轮，都会重跑一遍 linter、类型检查器、格式化器和测试套件。我的 Prefect 编排器集成测试光自己就要跑 15 分钟，所以我把它们拆开，加快反馈回路。

结论很明确：agent 化流程里最重要的事，是尽可能多地提供反馈回路。**LSP 服务器是把与代码相关的信号喂给智能体的最快方式。**

LSP 服务器是最被低估的组件之一，对编码 harness 尤其如此。它维护着整个代码库里符号的实时索引：变量、函数、类、定义、引用和类型错误。你的 IDE 已经为每种语言各跑了一个。你也需要为每种编程语言配一个。Decode 用 [Astral 的 ty](https://github.com/astral-sh/ty) 来支持 Python——一个用 Rust 写的极速类型检查器兼语言服务器，出自 uv 和 ruff 的同一个团队。

服务器通过 2 条通道把信号喂给智能体。

**图 8**（示意图）通向同一个 LSP 服务器的两种方式——要么智能体主动问，要么编辑操作替它问。两条 LSP 通道：1. 智能体按需查询 `lsp` 工具；2. 每一次 Python 编辑/写入都被动拉取诊断信息。

**通道 1** 是 `lsp` **工具**，处理主动查询，提供 4 个操作：`definition`（定位定义）、`references`（查找引用）、`hover`（悬停）、`diagnostics`（诊断）。一次调用就能返回精确的 `file:line:column` 答案，而不是做 3 次猜测性的文件读取。它是只读的，所以权限门（permission gate）会在所有模式下自动放行。

_摘录自 [src/decode/tools/lsp.py](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/main/src/decode/tools/lsp.py)：_

```
async def lsp(
    ctx: RunContext[AgentDeps],
    op: str,
    path: str,
    line: int | None = None,
    column: int | None = None,
) -> str:
    if op == "definition":
        return await _run_definition(ctx, path, line, column)
    if op == "references":
        return await _run_references(ctx, path, line, column)
    if op == "hover":
        return await _run_hover(ctx, path, line, column)

    return await _run_diagnostics(ctx, path)

async def _run_definition(ctx: RunContext[AgentDeps], path: str, line: int, column: int) -> str:
    result = await lsp_service.definition(ctx.deps.cwd, path, line, column)

    return _format_location(result)
```

服务器以后台进程的形式运行在每个项目根目录，通过 JSON-RPC（一种在标准输入/输出上进行的简单请求/响应协议）通信。Decode 的 `LspClient` 初始化会话、协商能力（capabilities）、发送请求：

_摘录自 [src/decode/services/lsp/service.py](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/main/src/decode/services/lsp/service.py)：_

```
from decode.services.lsp.client import LspClient

process = await asyncio.create_subprocess_exec(
    "ty", "server",
    stdin=PIPE, stdout=PIPE, cwd=root,
)
client = LspClient(process, root)
await client.initialize()
```

在 `demo-5` 会话里，智能体通过 JSON-RPC `textDocument/definition`，用 `lsp("definition", "src/decode/cli.py", <line>, <column>)` 解析出入口点。下一轮，模型就把它的编辑工具调用精准地指向那个位置，而不是先盲目地翻代码库。

**通道 2** 是**诊断信息增强器（Diagnostics Enricher）**，它在每次成功的 `.py` 写入或编辑之后被动运行，向工具结果追加一段「仅错误」的区块。它最多显示 10 条错误；文件干净或服务器不可用时保持沉默——这与 [OpenCode](https://github.com/anomalyco/opencode) 的模式一致。

`_enrich` 包装了文件修改工具的返回值，不需要额外的回合或工具。

_摘录自 [src/decode/tools/files.py](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/main/src/decode/tools/files.py)：_

```
def _enrich(base: str, cwd: Path, path: str) -> str:
    summary = _format_lsp_errors(lsp_service.diagnostics_on_edit(cwd, path))
    if summary is None:
        return base
    return f"{base}\n\n{summary}"

def _format_lsp_errors(diagnostics: list[Diagnostic] | None) -> str | None:
    ...
    errors = [d for d in diagnostics if d.severity == _LSP_ERROR_SEVERITY]
    shown = errors[:_LSP_DIAGNOSTICS_LIMIT]
    lines = [f"LSP diagnostics ({settings.lsp_server_command}) — fix these:"]
    ...
    return "\n".join(lines)
```

在 `demo-5` 会话里，当智能体更新 `src/decode/cli.py`、引入了一个未导入的引用时，文件能成功写入，但增强器会追加 `LSP diagnostics (ty) — fix these: ...`，带上错误详情。模型立刻看到这个反馈，并在运行任何测试之前，于下一次 `edit` 时修掉那个 import。

在下面的视频里，你可以在 [Opik](https://www.comet.com/site/?utm_source=newsletter&utm_medium=partner&utm_campaign=paul&utm_content=coding_agent_course) 中清楚地看到 LLM 如何输出 LSP 工具调用，以及它们在 harness 中如何被执行。（原文为内嵌视频演示，无法在译文中内嵌。）

记忆、技能与 LSP 共同决定了什么会进入窗口。现在来看看我们如何把它裁下去。

## 压缩：在窗口腐烂前清理（Compaction: Delete before the window rots）

回到 2025 年 11 月，当时我在为 agent 工程课程构建写作智能体：请求在 Gemini Pro 上大约 180,000 个输入 token 处开始劣化，单次请求耗时 >3 分钟，或者直接超时、断连。要知道，Gemini 纸面上能处理多达 1M 个输入 token。

一个塞满的窗口，远在撞上硬性 token 上限之前，就会让模型性能与可靠性双双劣化——[Anthropic 记录的退化曲线](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) 正是如此。所以你需要压缩：在尽量少丢失上下文的前提下，持续缩小你的上下文窗口。

压缩通过 3 种方式处理这个问题。最简单的是 `/clear`：先运行退出时的记忆写回（on-exit memory write-back），让关键经验持久化到 `.decode/MEMORY.md`，然后清空整个窗口。

**图 9**（示意图）三种压缩模式，以及每种模式在窗口里留下什么：`/clear` 只保留系统提示词；`/compaction` 把它重建为「摘要 + 尾部」；`/microcompaction` 则把旧工具输出就地替换成占位符。

第二种是**全量压缩（full compaction）**，在容量到 80% 时自动触发，也可以手动 `/compact`。一次 LLM 调用把对话总结进一个六段模板（目标 goal、约束与偏好 constraints & preferences、进展 progress、关键决策 key decisions、下一步 next steps、关键上下文 critical context），更旧的消息被丢弃。窗口变成 `[系统提示词] + [摘要] + [最近尾部]`——尾部保留最近约 20,000 个 token 的消息，并干净利落地切齐到一条**压缩边界（Compaction Boundary）**上，保证工具调用与它们的结果始终成对出现，这与 [Pi 的实现](https://github.com/earendil-works/pi) 一致。

两档压缩都用提供方上报的 token 窗口对照预留阈值（reserve threshold）来评估 `should_compact`（80% 全量压缩 → 剩余 20% 空余；60% 微压缩 → 剩余 40% 空余）：

_摘录自 [src/decode/context/compaction.py](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/main/src/decode/context/compaction.py)：_

```
def should_compact(usage: RunUsage, *, window: int, reserve: float, enabled: bool) -> bool:
    if not enabled:
        return False
    if usage.input_tokens <= 0:
        return False
    return usage.input_tokens >= reserve_threshold(window, reserve)
```

一切都在 `AgentTurnHandler` 的 `compact()` 方法里发生。`split_tail` 沿消息历史往回走、估算 token 数，定位压缩边界；`summarize_for_compaction` 生成摘要；`build_summary_message` 把摘要包成一条合成用户消息（synthetic user message）——它本身就是历史的一部分，下一次压缩会连它一起总结，于是连续的压缩可以免费合并；处理器在下一轮循环发送 `[summary_message, *tail]`。harness 持有它喂给模型的那个列表，所以**替换这个列表，就是压缩本身**：

_摘录自 [src/decode/agent/loop.py](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/main/src/decode/agent/loop.py)：_

```
class AgentTurnHandler:
    ...

    async def compact(self) -> CompactOutcome:
        split = split_tail(
            self.message_history, keep_recent_tokens=settings.compaction_keep_recent_tokens
        )
        skeleton = await summarize_for_compaction(
            self.message_history, model=self._compaction_model
        )

        before_tokens = self._last_input_tokens
        summary_message = build_summary_message(skeleton)
        tail = self.message_history[split:]

        self.message_history = [summary_message, *tail]

        return CompactOutcome.COMPACTED
```

第三种也是最后一种是**微压缩（microcompaction）**，在容量到 60% 时运行，全程不调用 LLM。它逐个检查 `ToolReturnPart`（承载工具输出的消息部件），把最近尾部之外的工具输出替换成一个占位符字符串。因为工具输出每一轮都会被消费掉，结论已经活在后续消息里；而工具输入仍留在消息中，必要时智能体可以重跑该工具，所以什么都不丢。这正是 [Anthropic 把「清除工具结果」称为最安全、最轻量的压缩手法](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) 的原因。

每一轮完成之后，处理器都用同一个数字对照两个阈值：先试全量压缩，再试 `microcompact`，通过同样的列表重赋值来替换 `message_history`。

_摘录自 [src/decode/context/compaction.py](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course/blob/main/src/decode/context/compaction.py)：_

```
_MICRO_PLACEHOLDER = "[tool output elided by microcompaction]"

def microcompact(
    messages: list[ModelMessage],
    *,
    keep_recent_tokens: int,
    placeholder: str = _MICRO_PLACEHOLDER,
) -> list[ModelMessage]:
    boundary = split_tail(messages, keep_recent_tokens=keep_recent_tokens)

    new_messages: list[ModelMessage] = []
    for index, message in enumerate(messages):
        if index >= boundary or not isinstance(message, ModelRequest):
            new_messages.append(message)
            continue

        new_parts = list(message.parts)
        changed = False
        for position, part in enumerate(message.parts):
            if not isinstance(part, ToolReturnPart | RetryPromptPart):
                continue
            new_parts[position] = dataclasses.replace(part, content=placeholder)

        new_messages.append(dataclasses.replace(message, parts=new_parts))

    return new_messages
```

把会话保存成 JSONL 文件时不做压缩：文件只是整段消息历史的一次简单快照。要保存压缩后的会话，你得在退出会话前先跑一次压缩；或者恢复会话、跑完压缩再退出。

**图 10**（截图）下图可以看到 `/compact` 命令如何把上下文窗口从 ◑57%（约 149,539 token）降到窗口的 8%。

## 下一步（Next steps）

本文没有触及其它组件，比如 MCP 客户端或 auto-mode 权限层。不过，这 4 个 harness 组件在你能用到的每一个编码 harness 里都无处不在——也许只有走极简路线的 Pi 是例外。

🧑‍💻 我们鼓励你 **clone 我们的[课程仓库](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course)**，打开终端，输入 **“decode”**，亲手试试这个编码智能体。

下一课，我们会补上 harness 拼图的最后一块：创建一份智能体目录（catalog），用来派发子智能体（subagent），让它们的工作永远不会污染你的窗口。

以下是**课程路线图**，一课一课看（[全部见 GitHub](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course#-course-outline)）：

1. [从零构建编码智能体](https://www.decodingai.com/p/building-a-coding-agent-from-scratch-system-design)（系统设计）
2. [极简编码智能体循环](https://www.decodingai.com/p/the-coding-agent-loop)
3. [从裸 Shell 到沙箱化编码智能体](https://www.decodingai.com/p/run-coding-agents-safely)
4. **面向编码智能体的上下文工程 ← 你在这里**
5. [子智能体即上下文工程](https://www.decodingai.com/p/subagents-are-context-engineering)
6. 远程无头模式与持久性（Remote Headless Mode & Durability）
7. AI 评测基础：基准、回归与在线评测（AI Evals Foundations: Benchmarks, Regression and Online）
8. 用回放给 AI 评测上强度（AI Evals on Steroids via Replays）

但我好奇的是：

> _**当编码智能体的窗口在任务中途被填满时，你今天实际会怎么做：**_`/clear`_** 丢掉线索，**_`/compact`_** 寄希望于摘要能扛住，还是就这么硬撑到它劣化？**_

点下面的按钮告诉我，每一条回复我都会读。

[发表评论](https://www.decodingai.com/p/context-engineering-for-coding-agents/comments)

## 译者注

- 术语对照：context engineering=上下文工程；coding agent=编码智能体；harness=保留英文（首现已注：包裹模型并驱动其执行的环境）；context window=上下文窗口；high-signal tokens=高信号 token；progressive disclosure=渐进式披露；skills catalog=技能目录；memory=记忆；auto-memory=自动记忆；LSP/language server=LSP/语言服务器；diagnostics=诊断信息；Diagnostics Enricher=诊断信息增强器；compaction=压缩（上下文压缩）；microcompaction=微压缩；Compaction Boundary=压缩边界；tail=尾部；placeholder=占位符；feedback loop=反馈回路；permission gate=权限门；synthetic user message=合成用户消息。工具/命令名（`decode`、`ty`、`Qwen3.6-35B`、`AGENTS.md`、`SKILL.md`、`.decode/MEMORY.md`、`/clear`、`/compact`、`/microcompaction`、`/demo-5-sandbox-feature-pr`）按原文保留。
- 全部代码块按原文保留（Python 示例、skill 目录树、demo 命令片段、`_format_lsp_errors` 中的 `...` 为原文真实截断）；代码内英文注释未译。
- 配图均为 Substack CDN 图片/GIF，无法在译文内嵌：译文按出现顺序整理为「图 N（图片性质）＋中文说明」，图片 URL 见来源文件 `sources/Context-Engineering-for-Coding-Agents-Bu.md`；两段内嵌视频（Opik 219 spans 链路追踪、LSP 工具调用执行演示）以文字说明标注。
- 翻译范围为正文（开篇导言 + Lesson 4 全课 + Next steps）；Substack 页面框架、订阅/分享按钮、赞助广告与评论区未译。
