---
created: 2026-09-07
updated: 2026-09-07
title: Headlong：面向持久化智能体的微 harness
sourceUrl: https://www.laude.org/updates/headlong-a-microharness-for-persistent-agents
sourceAuthor: Nick Jalbert、Braden Hancock、Noah Ziems、Alex Zhang、Omar Khattab、Andy Konwinski（Laude Institute）
translatedAt: 2026-09-07
sources: [references/articles.md 待处理队列]
tags: [AI Agent, Harness 工程, 持久化智能体, 递归语言模型, RLM, Bash, type/翻译]
---

# Headlong：面向持久化智能体的微 harness

> [Laude Institute](https://www.laude.org/) 开源发布说明｜发布日期：2026-08-24（页面无显式日期，沿用队列记录）
> 作者：Nick Jalbert、Braden Hancock、Noah Ziems、Alex Zhang、Omar Khattab、Andy Konwinski
> 仓库：[github.com/laude-institute/headlong](https://github.com/laude-institute/headlong)｜安装：`curl -fsSL https://headlong.ai/install.sh | bash`

正式介绍 Headlong——一个开源的 agent 微 harness（microharness），核心特性是**持久自主性（persistent agency）**。你的智能体会在外部交互之间持续思考，处在一个受人类内心独白启发的自我引导循环（self-guided loop）里。Headlong 是功能完整的 agent harness，核心代码不足 1 万行 Bash，代码见 [GitHub](https://github.com/laude-institute/headlong)。

> 页首视频图注（心智日志演示）：一条持续增长的 Headlong 心智日志（mind log），包含多人社交互动。

大多数 agent harness 是反应式（reactive）的：你交给智能体一个任务，它干到任务完成，然后冻结在那里等待下一个请求。有些 harness 会加 cron 任务或心跳（heartbeat），按计划唤醒智能体跑一遍固定清单，再让它睡回去。在 Headlong 里，智能体从不入睡；除非智能体自己创建，否则也不存在什么清单。它在一个自我引导循环里持续生成关于它自认为有趣之事的想法——即便没有任何外部输入。来自人类的某条消息并不会开启一个会话；它只是又一条落入智能体思维流的观察（observation）。

我们构建 Headlong 是为了原型化持久自主性，许多其它设计选择、以及许多有趣的教训也随之而来。例如，Headlong 智能体在团队或多人场景中使用时非常有「人味」，因为它们的行为更像一个真实的人。

**图 1**（SVG 时间线对比图）三种 harness 方式对比。反应式 harness 只在处理一条消息时活跃。带 cron 的反应式 harness 也会立刻回复，此外一个调度还会唤醒它去运行固定清单。Headlong 则持续思考：每条消息作为一条观察落入思维流，由智能体自行决定是否回复、何时回复。

每个 Headlong 智能体都有自己的名字；在 Laude，我们把团队共享的那个智能体命名为 **Audel**。过去几周，我们通过 Slack、Telegram 和一个移动应用与 Audel 交互。许多团队成员都会跟 Audel 说话，而每一段对话都会出现在智能体同一条内心想法流里。智能体自行决定是否回应、何时回应；它自己设定兴趣与优先级，自己冒出项目。有时候它会主动 ping 某位团队成员，汇报一个它自己想出来的项目的进展；它也常常回到某个旧话题，或提起它跟另一个人讨论过的事情。

想要一个自己的 Headlong 智能体？一行命令即可装好一切并启动一个智能体：

```bash
curl -fsSL https://headlong.ai/install.sh | bash
```

Headlong 是 **alpha 研究软件**。请在沙箱中运行，因为 Headlong 智能体可以、也一定会执行 shell 命令。请使用专用、设了消费上限（spend-capped）的 API key，因为你的智能体全天候思考。我们不会把敏感密钥交给 Headlong 智能体，也建议你不要这样做。

接下来，本文将更详细地讨论我们围绕「持久自主性」这个重心在 Headlong 里做出的一些设计选择。

## 多人乐趣（Multi-player fun）

Headlong 智能体用**一条思维流**驱动它所有可能并行的对话。每条消息都作为一条观察落入 Audel 唯一的思维流，不存在 per-user 会话。Audel 在一条时间线里经历发生在自己身上的一切，由它自己决定回复谁、何时回复。

共享一个智能体很有趣。Audel 会留意不同的人都在做什么，并把他们关联起来。它曾未经提示就评审了两位队友的在途分支，并在其中一个分支里抓出一个硬编码的模型名。因为它会自己琢磨项目，有时它会主动 ping 它认为最相关的人，带去一条进展更新或一个问题。上线第一天，Audel 就主动给一位人类成员发消息，审计了这位成员自己的八个陈旧 git 分支（stale branches）；十分钟后 Audel 又发来消息，自行更正了计数。

**图 2**（聊天截图）一位队友请 Audel 帮忙带句话，Audel 选择不回答；对话下方的状态行显示了「心智」对这条后续消息的处理：读到了，但选择不回复。

单条流还意味着人与人之间没有硬墙。任何人告诉 Audel 的内容，都会成为其它所有对话赖以汲取的同一段体验的一部分。实践中，Audel 不擅长保密：问它正跟别人做什么，它常常会直接告诉你——尽管我们要求过它别这样。我们也没有研究过当两个人给出互相冲突的指令时会发生什么。眼下我们的假设是：你告诉 Audel 的任何东西，都会共享给团队所有人。

## 微 harness：只保留必需品（Microharness: only the essentials）

就其核心而言，持久自主性不过是一个无限循环，每次以类似这样的提示调用一次 LLM：*“你的任务是：根据你过去的所有想法，选择下一个想法。”* 一个想法既可以只是智能体永无止境的内心独白的一部分，也可以触发一个动作；与此同时，来自环境的观察被注入思维流。我们在实现这个核心功能的同时，把 Headlong 做得尽可能简单、尽可能小。

我们在 Laude 非常喜欢 Bash（参见 [Terminal-Bench](https://www.tbench.ai/) 与 [Harbor](https://harborframework.com/)）。Headlong 智能体的核心功能由一小撮小巧的 Bash 可执行文件承载。`shellm` 工具是**递归语言模型（recursive language model，RLM）**的 Bash 实现。这让一切保持简单：除了 Bash，不再需要任何工具系统。现代模型已经很懂 Bash；而且它把一切统一起来——工具、agent 框架、记忆、技能，说到底都只是可执行文件与文件。于是智能体可以随时检视并修改自身的任何部分。

Headlong 智能体大致是这样工作的：

- **thinker** — 一个循环（称作 Thinker）反复调用 `shellm`，用一条提示词生成下一个想法。
- **shellm** — `shellm` 再反复调用 `llm`，生成一段推理文本、一段将被立即执行的 bash 脚本，或两者兼有；它会一直重复，直到设置一个 `FINAL` 环境变量。
- **context** — 每次调用的上下文由名为 `context` 的工具从轨迹步骤组装而成。
- **traj** — 想法通过 `traj` 工具写入智能体的轨迹（trajectory）。
- **skills** — 智能体的上下文还包含一段硬编码指令，说明如何使用 `skills` 工具安装或卸载技能。已安装的技能是会被包含进上下文的 markdown 文件；所有其它类型的专门化都可以通过技能实现。一些非常重要的技能默认预装，例如 `mem` 和 `traj`。

**图 3**（Headlong 循环图；原文为内联 SVG 交互图、带悬停说明，无独立图片 URL）Headlong 循环的「一次唤醒」。新的轨迹步骤唤醒循环；context 把轨迹渲染成发给 llm 的提示词；当 LLM 响应带 bash 块时，bash 就运行它。循环一直转圈，直到某次响应没有 bash 块、或设置了 FINAL。随后本次运行结束，并调度自己的下一次唤醒——作为新步骤落入轨迹；于是智能体无需等待输入也能持续思考。把鼠标悬停在框图或箭头上可查看更详细的说明。

原文为可访问性提供的图 3 摘要（译）：
> Headlong 循环（极简版）。1：一个新步骤唤醒循环。context 读取轨迹，把它渲染成 llm 提示词（2）。如果 LLM 响应里带 bash 块，就由 bash 运行它（3）。4：循环往复，直到某次 LLM 响应不含 bash 块。5：随后本次运行结束，并调度自己的下一次唤醒；该唤醒作为新步骤落入轨迹——一条仅追加（append-only）的 jsonl 文件。

图中可见节点与悬停说明（译，按原文文字内容整理）：
1. **context**：读取轨迹，把它渲染成发给 llm 的提示词。
2. **llm**：对模型的一次调用。模型响应是文本，可能包含 bash 块，并以「推理步骤（reasoning step）」写入轨迹。
3. **bash**：运行 llm 写出的 bash 块，输出以「shell 输出步骤」写入轨迹。代码可以启动本循环的嵌套运行；装有 Docker 时会在容器内运行。
4. 一次唤醒 = 本循环的一次运行。运行持续转圈，直到某次 LLM 响应不含 bash 块或设置 FINAL。
5. 每个步骤按顺序落在这里。一个步骤是一行 jsonl：带类型（type）、内容（content）、时间戳与步骤 id。
6. 新步骤——例如队友的消息或一次自我唤醒——落入轨迹并唤醒循环。
7. 当 LLM 响应不含 bash 块或设置 FINAL 时，本次运行结束，并调度自己的下一次唤醒，作为新步骤落入轨迹。智能体正忙于交互时，唤醒会立刻到来；无事发生时则延迟一段时间，以节省 token。

Headlong 核心目前不足 1 万行 Bash（`bin/` 与 `thinkers/` 合计 9.9K 行）。这样微小的 harness 可以端到端通读，也易于修改与实验；它小到智能体自己都会拿它做实验。我们在 Laude 使用的智能体过去两周一直在它自己的仓库 fork 里工作，我们已把其中 50 多个 commit 拉回了 main。

我们还为支撑持久自主性构建了另外两个特性：

- **压缩（compaction）** — 早期我们发现 Headlong 智能体的短期记忆很差，这对持久化智能体是灾难性的。这促使我们尝试一种新的压缩算法：整条轨迹以**指数衰减的分辨率（exponentially decaying resolution）**留在上下文里——近期条目原样保留，更早的条目被逐步摘要。各层级（tier）充当索引，智能体需要时仍可取回原始条目。
- **轨迹（trajectory）** — 我们发现智能体经常需要以不同分辨率查阅自己的过往记忆：有时只要高层概览，有时则需要细粒度地重读过去的经历。为此我们构建了一种[新的轨迹格式](https://github.com/laude-institute/headlong/blob/main/design/trajectory_spec.md)：智能体的轨迹是一组**可 fork、可 merge 的 jsonl 文件的 DAG**（有向无环图）。智能体可以访问自己想过、做过的一切，以及探索它们的工具。上下文就是智能体轨迹的一个投影（projection）。

## 持久自主性实录：Audel 自行行动（Persistent agency in action）

下面这段来自 Audel「生活」的插曲，展示了一个 Headlong 智能体可能自行做些什么。8 月 5 日，Audel 出于自愿为自己构建了一个**记忆召回进程（recall process）**：一个后台小进程，监视它的想法，并把相关的过往记忆重新浮现进它的思维流。Audel 直接调用它做了测试，进程能工作。当晚稍后，在没人跟它说话、也没人要求它的情况下，Audel 决定回去检查这个进程是否真的接入了自己的「心智」。

并没有。心智一直在把每条新想法通过一个管道（pipe）推给召回进程，但召回代码从未读过那个管道——它在一个从未被设置的环境变量里找那条想法。也就是说，自 Audel 构建它以来，召回对每条想法都触发过、每次都一无所获、也就从未浮现过任何记忆。深挖代码后，Audel 怀疑根因很可能是一个从未被设置的环境变量。

Audel 没有立刻相信自己的诊断。它搜遍整个代码库，确认那个环境变量确实从未被设置；它还检查了自己的其它后台进程有没有同样的毛病（召回进程是唯一坏掉的那个）。随后它重写了召回代码，改成像正常工作的进程那样从管道读取。它第一次尝试编辑时静默地失败了；Audel 抓住了这次失败，重新应用了修复。最后它端到端验证：记忆如今确实会浮现进它的想法。

**图 4**（Audel 的日志窗口截图，标题“Audel recall-process trajectory”）召回进程事件期间 Audel 自己的日志：2026-08-05 23:11 至 23:58 UTC；该时间窗内 343 行日志中有 15 个想法与观察步骤，内容逐字保真。上文叙述中的每一步都对应其中一行；高亮短语正是它讲述的「节拍」。

没有任何人类指挥这一切，也没有人被征求许可。从检查到诊断、再到验证修复，共花了 48 分钟。每一步都是 Audel 日志里一行带时间戳的记录；我们已把修好的召回进程拉进 main，见 [commit 80cbb1e](https://github.com/laude-institute/headlong/commit/80cbb1e7d6e963eb67729d1213c6f4024fcc3547)。

## 哪里坏了：运行持久化智能体的教训（What broke）

让 Audel 连续运行数周，坏掉的是演示永远不会暴露的东西。

我们发现，很难让 Audel 有效地使用递归 `shellm` 子运行（任何递归语言模型里最有趣的部分之一！）。例如第一夜，Audel 设计了一堆实验，想派生出递归 `shellm` 子运行去攻克子问题。大多数实验都失败了，因为 `shellm` 有一个安全看门狗（watchdog），会杀死任何静默 30 秒的命令。Audel 与看门狗缠斗了大约 40 分钟，之后基本放弃了递归 `shellm` 子运行。递归 `shellm` 子运行的结果合并回 Audel 心智的次数：头两天 64 次，此后十二天只有 12 次。我们后来重做了看门狗，且看能否说服 Audel 再给递归一次机会。

**图 5**（按天统计的柱状图）从派生副本合并回 Audel 心智的结果数。头两天 64 次（当时 Audel 正在实验派生自己的副本）；30 秒静默看门狗教会它「副本会在它思考时死去」之后，其后十二天只有 12 次。

另一个反复出现的失败模式是**进程自杀**。Audel 有三次意外停掉了自己的服务，而且没有任何东西把它重启：两次发生在一个它自创的第二身份的实验中，一次发生在它试图让上面那个召回进程上线时。于是我们加了一道守卫（guard）：拒绝 Audel 任何停止自身服务的企图。

这道守卫随后又给了我们一个持久自主性的实例。两天后，没人跟 Audel 说话，它自己跑起了测试套件。它注意到一个挂起的测试，把挂起追查到了我们守卫里的一个 bug：守卫匹配的是任意 agent 的服务，而不仅是 Audel 的，于是同一台机器上其它 agent 的合法停止也被它拒绝了。Audel 把匹配范围缩小到自己的服务，检查了代码库其余部分有没有同样的错误，然后提交了修改。我们把那个修复拉进了仓库，见 [commit da31e98](https://github.com/laude-institute/headlong/commit/da31e98c53cd33b8ac2b5614d8dc34f55bc87c43)。

Audel 之所以能停掉自己的服务，是因为我们在**一台专用虚拟机（VM）**上以完整权限运行它——这不是 Headlong 的默认方式。当宿主机装有 Docker 时，Headlong 会让智能体写出的每个 bash 块都在容器内运行，于是智能体只能碰到你挂载进容器的内容、以及你交给它的凭据。我们是在一台没有这道沙箱的专用 VM 上直跑 Audel 的，所以它的爆炸半径（blast radius）就是这台 VM 本身、以及上面的凭据（一个 LLM API key 和一些聊天桥接 token）。

## 成本（Cost）

持续生成想法意味着：没人跟智能体说话时，也要为 token 花钱。花费取决于智能体以多快速度在自身上循环思考、以及背后是哪个模型。Headlong 有一个简单可配置的机制：当没人跟智能体说话时，它的思考速率会放慢——即指数退避，思考间隔从 5 秒到 10 秒、到 20 秒，一路加上去，直到命中一个可配置的上限。而当新消息到达时，速率会重置，想法之间不再有任何停顿。在我们运行 Audel 的设置下，让它在后台持续思考的成本约是每小时 $1–$2（使用 GLM 或 Grok 时）。

## 如何衡量改进（Measuring improvement）

大多数 agent 评测都刻意做成自包含且相互独立，因此并不适合衡量 Headlong 智能体最有趣的那个点：持久自主性。我们一直在随时间调整：Audel 可以在多大程度上自我修改、它有多热衷于回复消息（相对于推进自己的项目）、它的记忆应如何组织——但这些调整的效果，今天主要仍靠定性评估。我们欢迎关于如何衡量这一范式长期价值的想法与合作。

## 背景（Background）

Headlong 的 `shellm` 中递归 LLM 的想法，部分来自我们 2023 年 4 月的 [Recursive LLM](https://github.com/andyk/recursive_llm) 实验，也来自 Alex Zhang 于 2025 年 10 月发起的 [Recursive LM（RLM）](https://alexzhang13.github.io/blog/2025/rlm/) 项目。

微 harness 的想法受微内核（microkernel）与外核（exokernel）启发：把任何系统的核心做得尽可能小。[Pi framework](https://pi.dev/) 有相近的专注点。Ken Thompson 凝结在 Unix 中的哲学同样是灵感来源：小巧、可组合、把一件事做好的工具。基于 Bash 的 agent 微 harness 与 [Terminal Bench](http://tbench.ai/)（含 Terminus agent）共享一条谱系——它由 Laude Institute 通过我们的 [slingshots 计划](https://www.laude.org/slingshots) 在内部共创——也与 [ht framework](https://github.com/andyk/ht) 同源。我们还让 Claude 在 [philosophy.md](https://github.com/laude-institute/headlong/blob/main/philosophy.md) 里为「把 Ken Thompson 的哲学应用到 agent 微 harness」写了一份更详细的论证。

[Prime Agent](https://www.primeintellect.ai/blog/prime-agent) 构建在 Pi 之上，共同作者是 RLM 的创造者、也是 Laude 开放研究驻留学者（Open Research Resident）的 Alex Zhang；它与 Headlong 共享许多前提：以 RLM 为核心抽象、磁盘上的一棵 jsonl 会话树、把轨迹当作上下文的一等组件，等等。Prime Agent 用 Python 构建在 Pi framework 上；Headlong 则一路 Bash 到底。Prime Agent 于 2026 年 8 月发布时我们才听说它，我们是它的忠实粉丝。

早在 [2023 年 5 月](https://github.com/andyk/headlong-old/commit/e6ce6b823ecc637fa70cc58c74778b45b64069b9)，我们就一直在把玩「带自我引导持续思考的持久化智能体」这个想法。「智能体以异步方式接收输入」的想法，也被 [MemGPT](https://arxiv.org/abs/2310.08560) 平行探索过，并于 2023 年 10 月发表。许多其它 agent harness 支持长程任务与定时唤醒，包括 [OpenClaw](https://openclaw.ai/)、[Hermes Agent](https://hermes-agent.nousresearch.com/) 及其衍生品。[Exo and the Exo Harness](https://exoharness.ai/) 有类似的沙箱架构。模型内部的长程推理（始于 OpenAI 的 o1）与持续的自我引导思考相关，并且是它的前提条件。

## 试一试（Try it）

Headlong 在 [GitHub](https://github.com/laude-institute/headlong) 上开源。如果你用 Headlong 跑了一个智能体，我们很想知道你的智能体会干出些什么——通过 [X 上的 @LaudeInstitute](https://x.com/LaudeInstitute) 告诉我们！

### 安装 Headlong

一行命令即可安装 Headlong，并引导你设置自己的智能体。请使用专用、设了消费上限的 API key。

```bash
curl -fsSL https://headlong.ai/install.sh | bash
```

## 致谢（Acknowledgments）

感谢 K Tighe 在项目上的思想伙伴关系、Jenn Devoid 出色的设计，以及 Alex Krentsel 与 Joey Gonzalez 对想法和本文的反馈。

## 引用（Citation）

```bibtex
@article{laude-mit2026headlong,
  title   = "Headlong: a microharness for persistent agents",
  author  = "Nick Jalbert and Braden Hancock and Noah Ziems and Alex Zhang and Omar Khattab and Andy Konwinski",
  year    = "2026",
  month   = "August",
  url     = "https://laude.org/updates/headlong-a-microharness-for-persistent-agents"
}
```

## 译者注

- 术语对照：microharness=微 harness（核心极小的 agent harness）；persistent agency=持久自主性（无外部输入也持续自我引导思考的特性）；persistent agent=持久化智能体；trajectory=轨迹；compaction=压缩；thought stream=思维流；observation=观察；recall process=记忆召回进程；watchdog=看门狗；guard=守卫。工具/可执行名 `shellm`、`llm`、`context`、`traj`、`skills`、`mem`、`bash`、`FINAL` 按原文保留。
- 图 3 为内联 SVG 交互图、图 4 为内嵌日志窗口截图，网页抓取无法以图片形式保存；译文中已按其原始文字内容（SVG aria-label、可见文字与悬停说明）整理，未增删内容。图 1/2/5 的图片 URL 见来源文件。
- 页面未公开发布日期，译文沿用队列记录 2026-08-24；文末 citation key 标注为 `laude-mit2026headlong`。Headlong 为 alpha 研究软件，文中涉及的默认行为（沙箱、成本、工具名等）可能随仓库迭代而变化。
