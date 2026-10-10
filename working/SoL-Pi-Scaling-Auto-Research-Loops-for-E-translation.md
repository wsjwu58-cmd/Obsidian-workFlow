---
created: 2026-10-03
updated: 2026-10-03
title: SoL-Pi —— 为高效 Agent Harness 扩展自动研究循环
sourceUrl: https://github.com/NVlabs/SoL-Pi
sourceAuthor: NVIDIA（NVlabs · SIGIL）；Haozhe Liu、Tian Ye、Sensen Gao、Qihang Cao、Yitong Li、Mingchen Zhuge、Duomin Wang、Ruihua Zhang、Jiawang Bian、Lei Zhu、Ligeng Zhu、Enze Xie、Song Han 等
translatedAt: 2026-10-03
sources: [references/articles.md 待处理队列]
tags: [SoL-Pi, Pi, Agent Harness, Harness 工程, 自动研究循环, Auto-Research, RSI, 递归自我改进, Token 效率, 上下文压缩, ObservationPack, Action Fusion, Evidence-Preserving Reducer, Online Context Compact, EdgeBench, NVIDIA, type/翻译]
---

# SoL-Pi —— 为高效 Agent Harness 扩展自动研究循环

> 开源仓库：`NVlabs/SoL-Pi`（NVIDIA · SIGIL；主语言 TypeScript 94.9% / JavaScript 5.1%；截至 2026-10-03 约 3.3k stars / 259 forks / 9 contributors；MIT 许可证；暂无 release）
> 项目页：https://nvlabs.github.io/SoL-Pi/ ｜ 论文：https://arxiv.org/abs/2609.20519
> 原文：https://github.com/NVlabs/SoL-Pi

<p align="center">
  <img src="assets/sol-pi-hero.png" width="100%" alt="SoL-Pi: Scaling Auto-Research Loops for Efficient Agent Harnesses" />
</p>

## ⚡ SoL-Pi：为高效 Agent Harness 扩展自动研究循环

<p align="center">
  <a href="https://arxiv.org/abs/2609.20519"><img src="https://img.shields.io/badge/arXiv-2609.20519-B31B1B?logo=arxiv&logoColor=white" alt="arXiv: 2609.20519" /></a>
  <a href="#getting-started"><img src="https://img.shields.io/badge/Getting%20Started-Install-76B900" alt="Getting Started" /></a>
  <a href="https://github.com/NVlabs/SoL-Pi/blob/main/docs/configuration.md"><img src="https://img.shields.io/badge/Docs-Configuration-555555" alt="Configuration" /></a>
  <a href="https://nvlabs.github.io/SoL-Pi/"><img src="https://img.shields.io/badge/Blog-SoL--Pi-76B900" alt="SoL-Pi Blog" /></a>
  <a href="https://github.com/NVlabs/SoL-Pi/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="MIT License" /></a>
</p>

> [!NOTE]
> 本仓库包含 SoL-Pi 的开源版本，它是 [Pi](https://github.com/earendil-works/pi) 的一个独立扩展（standalone extension）。它不是 Pi 的官方发行版。

## 💡 TL;DR

**少花钱，但别让 agent 少干有用的活。**

SoL-Pi 是 Pi 的一个独立扩展，它打包了四个可复用的效率机制——这些机制是通过大规模自动研究循环（auto-research loops）发现的。它减少了重复的模型轮次、上下文重放、超大观测结果，以及不必要的长日志阅读，同时保留 agent 完成任务所需的工作与证据。

SoL-Pi 安装在一个未经修改的 Pi 发行版之上。每个机制都是 opt-in（显式开启）的，并默认关闭。

## 引言

长时运行的 coding agent 会不断累积重复工作。一次文件编辑之后，往往紧跟一条可预测的验证命令。大型工具结果在被首次使用很久之后仍会被反复重放。已完成的子任务依然留在活跃上下文中，而前沿模型可能花掉一整次请求去读一份日志，可其中真正影响下一步决策的只有几行。

SoL-Pi 源自我们自动研究工作中的一个更宽泛的问题：**在扩展 agent 循环之前，能不能先让 agent 把 harness 本身变得更高效？** 这项搜索聚焦于"受约束的效率"（constrained efficiency）：减少 token 流量、推理工作量与 agent 轮次，但不提前停止、不跳过验证、不隐藏证据。

这个独立发行版包含四个在这一过程中存活下来的机制。它们作用于 harness 的不同部位，并通过 Pi 的公开扩展 API 组合在一起。

## SoL-Pi 增加了什么

| 层面 | 机制 | 改变了什么 |
|---|---|---|
| 工具（Tools） | **Action Fusion** | 一次 edit 或 write 可以在同一个工具调用里顺带执行其后续验证命令。 |
| 观测（Observations） | **ObservationPack** | 反复出现的大型文本结果变成稳定句柄，可精确分页召回。 |
| 委派（Delegation） | **Evidence-Preserving Reducer** | 长诊断日志只在每条被保留的引用都与归档源文本一致时，才被压缩成紧凑凭据。 |
| 上下文（Context） | **Online Context Compact** | 已完成的计划步骤成为 Pi 原生压缩的候选触发点，并受经济性与窗口压力检查约束；成功压缩后，Pi 在新的轮次里继续该任务。 |

这些机制共享四条规则：

- **不改 Pi 源码。** SoL-Pi 只导入公开的 Pi API，不内置（vendor）Pi 源码树。
- **显式 opt-in。** 缺少配置时，所有机制均保持关闭。
- **保留证据。** 原始观测在本地仍然可用，且 Reducer 失败时会保持原始结果不变。
- **沿用 Pi 的运行时选择。** 认证、provider URL、主模型与 shell 行为仍由 Pi 掌控。

## 技术细节与核心洞见

阅读 [SoL-Pi 博客](https://nvlabs.github.io/SoL-Pi/)，可以深入了解 SoL-Pi 的技术细节、设计理由与核心洞见，包括自动研究如何导向这四个效率机制，以及它们各自如何工作。

## 论文

阅读我们的论文：[SoL-Pi: Recursively Scaling Auto-Research Loops for Efficient Agent Harness](https://arxiv.org/abs/2609.20519)。

## 快速开始

### 环境要求

- Node.js 22.19 或更高版本
- npm
- `@earendil-works/pi-coding-agent` 0.85.1

### 安装

安装经过测试的 Pi 版本：

```bash
npm install --global @earendil-works/pi-coding-agent@0.85.1
```

然后直接从 [NVlabs/SoL-Pi](https://github.com/NVlabs/SoL-Pi) 安装 SoL-Pi：

```bash
pi install git:github.com/NVlabs/SoL-Pi
```

如果只想为当前项目安装，使用项目本地作用域：

```bash
pi install git:github.com/NVlabs/SoL-Pi --local --approve
```

### 配置

SoL-Pi 只使用一份生效的配置。在官方 Pi 发行版下，它会按以下顺序查找 `sol-pi.json` 文件：

1. 当前项目中的 `.pi/sol-pi.json`——前提是该项目被信任且文件存在；
2. 否则使用 `~/.pi/agent/sol-pi.json`。

如果两个文件都不存在，SoL-Pi 使用内置默认值。项目级配置优先于用户级配置；两者不会被合并。

下面这份保守配置只开启两个本地机制——它们不产生额外的模型调用，也不会中断正在进行的运行：

```json
{
  "version": 1,
  "actionFusion": true,
  "observationPack": true,
  "evidencePreservingReducer": false,
  "onlineContextCompact": false,
  "cacheWriteReadRatio": 12.5
}
```

请在审阅过各机制的配置与安全影响之后，再开启其他机制。SoL-Pi 不使用专用的环境变量；功能开关、reducer 的 provider/model 路由，以及压缩比例都在 `sol-pi.json` 中配置。所有键的模板见 [sol-pi.example.json](https://github.com/NVlabs/SoL-Pi/blob/main/sol-pi.example.json)。

完整 schema 见[配置文档](https://github.com/NVlabs/SoL-Pi/blob/main/docs/configuration.md)。coding agent 与自动化环境应遵循规范的 [agent 安装与配置协议](https://github.com/NVlabs/SoL-Pi/blob/main/agents-install.md)，其中描述了一套"全部开启"的配置，并用 `scripts/check-sol-pi-config.mjs --require-all-enabled` 进行校验。

## 存储与安全

ObservationPack 与 Evidence-Preserving Reducer 把与会话相关的归档存放在：

```text
<session-directory>/sol-pi/<session-id>/
├── observation-pack/
└── evidence-preserving-reducer/
```

它们把符合条件的源材料归档到该目录。这些归档副本保留在本地，且不会在 Pi 会话结束时被自动删除。

使用 `pi --no-session` 或 `SessionManager.inMemory()` 时，Pi 不提供会话目录。此时 SoL-Pi 会在操作系统临时目录下创建一个名为 `sol-pi-<session-id>-<random>/` 的私有目录。ObservationPack 与 Evidence-Preserving Reducer 会在该扩展被加载的整个生命周期内共享这个目录。这些模式会禁用 Pi 的会话日志持久化；但 SoL-Pi 仍会写入归档文件以支持精确召回。会话或 worker 退出后，临时归档同样会被保留，以便调用方读取所引用的证据。它们最终的清理遵循宿主机的临时文件策略或调用方的清理逻辑，不保证能挺过系统清理，也不支持会话恢复。

Online Context Compact 把状态存放在 Pi 的会话日志中。成功压缩后，它会开启一个新轮次并自动继续当前任务。取消运行或退出 Pi 不会触发自动继续。

Evidence-Preserving Reducer 可能会使用由 Pi 管理的认证，把符合条件的诊断日志内容发送给它所配置的 reducer 模型。开启之前请先阅读 [SECURITY.md](https://github.com/NVlabs/SoL-Pi/blob/main/SECURITY.md)。对于必须留在本地的日志，请勿开启远程归约。

## 文档

| 文档 | 用途 |
| --- | --- |
| [Configuration](https://github.com/NVlabs/SoL-Pi/blob/main/docs/configuration.md) | 配置查找顺序、schema、默认值与信任行为 |
| [Compatibility](https://github.com/NVlabs/SoL-Pi/blob/main/docs/compatibility.md) | 受支持的 Pi API 与独立集成细节 |
| [Security](https://github.com/NVlabs/SoL-Pi/blob/main/SECURITY.md) | 本地存储、远程归约与敏感行为 |
| [Agent installation](https://github.com/NVlabs/SoL-Pi/blob/main/agents-install.md) | 可复现的安装与"全部开启"验证流程 |

## 开发

从 lockfile 安装并运行完整的源码检查：

```bash
npm ci --ignore-scripts
npm run check
npm audit --audit-level=high
node scripts/check-pi-compat.mjs
```

`npm run check` 覆盖 TypeScript、完整测试套件与包检查。开发依赖固定为 Pi 0.85.1；运行时 Pi 包仍然是 peer dependencies，因此由 Pi 自己负责它们的安装与升级。

## 项目状态

SoL-Pi 由 NVIDIA 开发并维护，是 Pi 的一个独立扩展。

我们欢迎经过测试、与 Pi 兼容、能提升 token 效率并降低 token 成本的扩展 PR。我们的团队会帮助对贡献进行基准测试，按固定的报告周期公布结果，并把被接受 PR 的作者列为 Contributors。详见 [CONTRIBUTING.md](https://github.com/NVlabs/SoL-Pi/blob/main/CONTRIBUTING.md)。

## 致谢

SoL-Pi 构建在 [Pi](https://github.com/earendil-works/pi) 提供的公开扩展接口之上。Pi 仍是一个独立的上游项目，未被内置（vendor）到本仓库中。

## 许可证

SoL-Pi 以 [MIT 许可证](https://github.com/NVlabs/SoL-Pi/blob/main/LICENSE)发布。

## Star 历史

<a href="https://www.star-history.com/?repos=NVlabs%2FSoL-Pi&type=date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/NVlabs/SoL-Pi/star-history/star-history-dark.svg" />
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/NVlabs/SoL-Pi/star-history/star-history-light.svg" />
    <img alt="SoL-Pi star history chart" src="https://raw.githubusercontent.com/NVlabs/SoL-Pi/star-history/star-history-light.svg" width="100%" />
  </picture>
</a>

---

# 研究与论文要点

> 以下内容译自项目博客页 [nvlabs.github.io/SoL-Pi](https://nvlabs.github.io/SoL-Pi/) 与论文 [arXiv:2609.20519](https://arxiv.org/abs/2609.20519)（15 页 / 8 图 / 4 表，2026-09-17 提交）。完整的英文原文已抓入 `sources/SoL-Pi-Scaling-Auto-Research-Loops-for-E-full.md`。

> **核心结论速览**

- 搜索规模：**152** 个提议方向 → **4** 个存活机制；约 **500** 个可执行环境（共 535 个：495 个仓库派生 + 40 个 verifier 驱动）、**超过 3,000** 次运行、**超过 60,000** 次 agent–环境交互。
- EdgeBench **51** 任务：记录 token 流量降低 **44.7–49.0%**，API 成本降低**约三分之一**，同时保留 Pi 约 **94%** 的平均得分。
- 折算节省：相对原生 Codex / Claude Code 每小时 **\$8.75–\$13.50**，相对 Pi 每小时 **\$4.36–\$5.71**。

## 研究动机

coding agent 的发展弧线又短又陡：从补全代码行，到跨仓库解决问题，再到根据反馈行动、甚至修改自己周围的工具。配合现代 harness，成千上万个 agent 已经可以连续协作一周而无需人工干预。这就引出一个基本问题：在一次长达数小时乃至数天的无人监督运行中，是每一个 token 都在把工作向前推进，还是冗余会随轨迹长度一起增长？

一旦 AI 能在复杂软件系统上工作，它也就可能作用于"生产 AI 的系统"本身——问题随之加深到递归自我改进（recursive self-improvement, RSI）。RSI 有可能加速通往更通用智能的进程；但 RSI 本身极其耗费 token：每一次尝试去产出更好的系统都要花 token，无论成功与否。那么在扩展 RSI 之前，是否应当先请 AI 让 AI 变得更高效？

为此，作者构建了一条可扩展的 RSI 流水线：agent 从公开数据和公开软件环境出发，为 harness rollout 构造可执行环境；另有 agent 观察模型在这些轨迹中如何探索，再把观察转化为自动研究循环，在效率目标下改进 harness。最终存活下来的机制被组合成 SoL-Pi——一个以 token 效率为核心的 agent harness。

作者同时指出，SoL-Pi 指向一种更宏观的 RSI 视角：它持久不变的价值或许不在于任何单一产物，而在于一个能够跨公开环境扩展、并发现可复用改进的**搜索过程**。

> **Pi** 是作为本研究基座的轻量、可扩展 coding-agent harness。**EdgeBench** 是一个由 51 个长时程可执行 agent 任务组成的套件；其任务、verifier 与反馈被保留用于最终留出评估。

## 方法：把 harness 改进当作开放式 RSI 问题

作者把 harness 改进视为一个开放式的 RSI 问题：在多种环境中搜索那些能够迁移到未见场景的改动。自动研究过程**分批**生成机制想法，把每个被选中的想法送入一条**独立循环**，并让通过验证的候选继续前进。

作者把 AI 主导的自动研究扩展到约 **150** 个提议方向与约 **500** 个可执行环境，涵盖 **超过 3,000** 次运行与 **超过 60,000** 次 agent–环境交互；这项搜索最终产出四个机制，合起来构成 SoL-Pi。

目标是**受约束的效率**（constrained efficiency）：在预先声明的"能力保持"判据约束下，搜索成本或 token 使用的降低。研究流程本身保持固定；存活下来的机制则界定下一轮研究的前沿。

- **想法池 fan-out**：外层把 152 个提议方向扇出为彼此独立的机制支线（lineage）。第一轮的 152 个方向先经 **Oracle Analysis**——一个在 rollout 之前、从既有轨迹中估计机会大小的阶段——筛选，然后再花费 rollout 预算。每条被选中的方向都对 harness 中"可避免的工作"给出一个具体主张，因此系统可以拒绝一条薄弱支线，而不必丢弃别处的进展。
- **六类提议家族**：按假设的**起点**分类（Context 24、Progress 26、Tools 26、Delegation 15、Prompt & policy 15、Improvement & evaluation 46），而非约束最终实现在哪里。例如 ObservationPack 起于 Context 家族（C23、C24），最终却成为观测边界上的机制。
- **每条支线内**：沿用 Karpathy 式的常规 autoresearch 实验循环——提出改动、实现、运行实验、读取结果，然后保留或丢弃并重复。针对 harness 研究，作者做了三处改造：
  1. **实现阶段是一个 Ralph Loop**：一个会持续迭代直到显式退出条件通过的实现循环；另有独立的 reviewer 检查实现及其行为契约，评审失败则把提议打回修订。
  2. **map-reduce 分析**处理多条探索轨迹：独立分析器各看一条轨迹，再由一个 reducer 在下一次机制提议之前合并它们的证据。
  3. **验证使用两个隔离的划分**：在训练集上开发与筛选候选；一旦冻结机制与验收规则，就在留出测试集上评估。留出轨迹永不进入后续分析，循环内也没有任何 agent 能看到留出结果。一次失败的留出评估会直接拒绝该冻结候选，且不会成为修复或新一轮搜索的反馈。

一条支线的阶段依次是：**轨迹 rollout → map-reduce 分析 → 提议 → 实现 → 评审 → 轨迹内验证 → 留出验证**（评审可打回实现；轨迹内验证可返回实现或重新 rollout）；想法之间并行、每条支线内部迭代。

### 可执行环境：两个家族，共 535 个

- **仓库派生环境（495 个）**：从 GitHub issue–PR 对挖掘带真值的轨迹。issue 指定任务，关联 PR 提供被接受的补丁与变更历史，二者共同构成真值轨迹。作者把仓库还原到修复前的提交，在离线镜像中安装依赖，并对 agent 隐藏 PR 与维护者的回归测试。只有当测试在 PR 前失败、在 PR 后通过时，才保留该环境——以此保证任务、轨迹与 verifier 一致。
- **verifier 驱动环境（40 个）**：先生成一个定义成功的可执行 verifier，再围绕它构造环境，供开放式探索使用，不提供参考轨迹；这些环境主要采用 Terminal-Bench 风格的 verifier。

为保证 EdgeBench 仍是有效的留出基准，作者**没有**使用 EdgeBench 的数据或 verifier 作为环境合成的来源或模板。EdgeBench 的任务与反馈始终位于 harness 搜索之外，只用于留出验证——这使得它的分数更能衡量对未见任务与 verifier 设计的泛化能力。

### 能力下限约束效率收益

搜索学到的是一个可复用的 harness 机制；决定候选存活的是**能力下限**（capability floor）。一个更便宜的候选如果靠提前停止、跳过必要的验证，或删掉完成任务所需的证据来省钱，就会被判失败。

每条循环都施加两道验收门：第一，每一项能力指标都必须落在预先声明的容差范围内；第二，至少有一项效率指标得到改善。在通过能力下限的候选中，循环保留非支配（nondominated）结果。由于这道门**一次只作用于一个机制**，它允许的微小损失会在机制组合时累积——最终组装出的 harness 保留了 Pi 约 94% 的平均得分。这道门真正要排除的，是"靠少干活省下来的"收益。

### 从编译式工作流到"一次性 skill 循环"

在数百个想法、数百轮研究迭代之间编排自动研究并不容易。作者的工作流经历了三种设计，区别在于**编排逻辑放在哪里**、**代码存活多久**、**规模化时最先坏在哪里**：

| 设计 | 优势 | 局限 |
|---|---|---|
| 01 编译式工作流 | 交接清晰 | 一旦编译就固定，超出固定图就脆弱 |
| 02 代码编排 | 运行时灵活 | 代码与测试不断累积 |
| 03 一次性 skill 循环 | 易于并行扩展 | 依赖一个可靠的模板 |

- **编译式工作流**：每个 agent 流用 YAML 描述并编译成可执行工作流，编排逻辑固定。显式图让协作与交接一目了然；但在规模上，固定图成为瓶颈——预编译的工作流覆盖不了所有边界情况，运行反复因人工修复而中断，操作者也无法重建数百个并发尝试的上下文。
- **代码编排**：由一个 lead agent 编写协调代码，在运行时打开会话、传递消息、组装工作流。这消除了固定图，但协调者成了瓶颈：为让每条循环互相兼容，长期存在且无界的代码库需要不断增加分支、测试与验证脚本；启动一次新实验可能需要对它做十小时以上的改动。
- **一次性 skill 循环**：作者维护一套最小、可复用的循环模板，每条循环都是一次性的，因此比固定图或不断膨胀的协调者都更易维护。

## 四个机制

自动研究产出了四个窄而聚焦的机制，分别对应工具、上下文管理、观测压缩与多 agent 委派。

### 01 工具 · Action Fusion（一次意图，一次轮次）

Action Fusion 把一次编辑与其后续命令保持在同一个本地序列里，从而去掉中间那一次模型决策。

基础 Pi 的 rollout 暴露出一个反复出现的序列：编辑文件之后，coding agent 常常会发出命令去测试、构建或运行这次改动。Action Fusion 把这个序列变成**一次工具调用**：harness 在本地应用编辑并执行命令，然后返回一个合并后的观测，不再需要额外一轮模型往返。

**这个工具是怎么造出来的（自动研究四阶段）：**

- **01 Oracle Analysis（搜索前）**：在 12.3% 的跨轮转换中测到"edit/write→command"的相邻候选；Bash 占观测到的后继动作的 85.1%。
- **02 基线构建**：把 Action Fusion 的执行在符合条件的调用中的 uptake 稳定到 87.7%、零无效调用，作为提示词搜索的可靠基线。
- **03 提示词优化（10 个搜索批次）**：去掉一个失败的提示词变体，再打磨提示词与 schema。选定 Iteration 10：**100% 触发率、87.0 的 task score**。
- **04 最终验证（2 次独立检查）**：确认发布行为后，机制才进入组合 harness。

在记录的 10 个批次里，触发率在 28.3% 到 100% 之间波动（非单调）。**全触发反事实**：若 149 个已观测的跨轮候选全部触发，模型轮次会从 1,386 降到 1,237（−10.8%），总 token 从 32.38M 降到 28.64M（−11.5%）。注意这是**由轨迹推演出的反事实，不是实测重跑**。

### 02 上下文 · Online Context Compact（在子任务边界压缩）

KV-cache 复用通常会把压缩推迟到运行的后期。Online Context Compact 换了一只时钟：它把任务分解为子任务，每当一个子任务完成就重新考虑压缩——但只在预期的未来节省足以偿还重写成本时才真正行动。

其做法是：agent 通过 `update_plan` 维护计划；在每个完成边界，harness 根据已完成步骤之间观测到的请求数与未完成步骤数，估计剩余模型请求，并用"按观测增长率填满当前上下文窗口所需的请求数"为这个估计封顶。成本门控把预计的输入节省，与重写 prompt 缓存的估计额外成本作比较；后续压缩还会计入尚未收回的重写成本，并要求更大的节省余量。当门控通过，或上下文用量接近窗口上限（且压缩确实能缩短上下文）时，harness 调用 Pi 原生的压缩。

### 03 观测 · ObservationPack（保留访问，去掉重复）

ObservationPack 用一个稳定句柄替换重复出现的完整输出，同时保留原件以支持分页召回。

在基础 Pi 中，一个大型文件或工具结果会在后续每一次请求里重新出现，既占上下文又占缓存。ObservationPack 改变了这个生命周期：它把载荷本地归档，在上下文里留下一个句柄和简短摘录，只在需要时精确召回对应页。

- **阈值**：超过 **10 KiB** 的结果会被本地归档，并在接下来**两次** provider 请求中仍全量发送；从第三次请求起，替换为稳定句柄、原始大小，以及由完整头尾行组成的短摘录。
- **选中过程**：从干净 Pi 重建占位机制（1 轮）→ 机制冻结（4 轮，把实现缩到 **315 行、2 个 hook**，并采用 fail-open 契约）→ TB40 权衡扫描（8 个配置，V2 是唯一落在质量门内的配置）→ EdgeBench 配对 A/B（11 任务 × 2 臂，在同一集群上并发）。
- **V2 配置**：**2,048 字节 head + 1,536 字节 tail + 投影前 2 次全量发送**。
- **配对结果**：provider 账单 **−23.58%**、单次响应成本 **−23.73%**、归一化得分 **+22.92%**；响应数量仅变化 **0.20%**，说明节省来自更便宜的响应，而非减少响应量。

### 04 委派 · Evidence-Preserving Reducer（把阅读委派出去，并验证证据）

Evidence-Preserving Reducer 只有在一条紧凑诊断凭据的证据能对着归档日志核查时，才接受它。

在构建与测试轨迹中，一份长日志往往只有几行会改变下一步决策。Evidence-Preserving Reducer 利用这个边界，把首次阅读委派给一个成本更低的 agent：它把产出的凭据绑定到归档日志，并在前沿 agent 看到它之前，逐条核验每一个被引用的片段。委派不再需要"信任一段流畅的摘要"。

- **处理范围**：只压缩不少于 **4 KiB** 的构建 / 测试日志，且限定于预定义命令集；文件读取与搜索结果绕过 reducer。
- **流程**：归档精确输出 → 请一个成本更低的模型（**GPT-5.6 Luna，high**）抽取关键证据为紧凑凭据 → 确定性 verifier 检查凭据的 schema、源哈希、退出状态、精确引用与大小 → 校验失败、怀疑凭据泄露，或凭据没有带来体积缩减时，回退到原始日志。
- **顺序**：Reducer 在 ObservationPack 投影模型上下文之前处理工具结果；ObservationPack 识别 reducer 的凭据标记并跳过这些结果，以保留已验证的证据。
- **职责边界**：辅助模型负责抽取证据；主 agent 仍负责诊断与行动选择。

四个机制作用于 agent 工作流的不同阶段：编辑代码时，Action Fusion 合并编辑与后续命令；环境返回输出时，Evidence-Preserving Reducer 从构建/测试日志抽取已验证证据，ObservationPack 避免重复全量发送大结果；agent 完成一个计划步骤时，Online Context Compact 判断压缩累积上下文是否省 token。它们处理的是互补的开销来源，因此作者对组合 harness 做端到端评估，以验证其联合效果。

## 实验结果

所有对比都在 **xhigh**（本评估中最高的推理努力档位）下运行每个模型后端。API 价格基准为 **2026-08-17**。

### EdgeBench（51 个任务）

在 EdgeBench 任务上，SoL-Pi 在两个模型后端上都保留了 Pi 约 **94%** 的平均得分；在 GPT-5.6 Sol 上，它还超过了该模型原生的 Codex harness。效率收益更大：相对 Pi，它少用 **45–49%** 的 token、成本低约**三分之一**；相对模型原生 harness，在 list-price API 成本口径下少用 **35–64%** 的 token、成本低 **50–54%**。

| Harness（GPT-5.6 Sol，搜索后端） | 总 token（B） | Token 成本（$） | 平均得分 | Token 效率（$/分） |
| --- | --- | --- | --- | --- |
| Codex | 3.0537 | 1,787 | 34.738 | 1.0086 |
| Pi | 2.1538 | 1,339 | 44.833 | 0.5855 |
| **SoL-Pi [Efficiency]** | **1.0990** | **894** | 42.003 | **0.4174** |
| SoL-Pi [Performance] | 2.0224 | 1,271 | **47.208** | 0.5280 |

| Harness（Opus 5，留出后端） | 总 token（B） | Token 成本（$） | 平均得分 | Token 效率（$/分） |
| --- | --- | --- | --- | --- |
| Claude Code | 2.0045 | 2,535 | 43.689 | 1.1377 |
| Pi | 2.3697 | 1,741 | 44.756 | 0.7625 |
| **SoL-Pi [Efficiency]** | **1.3101** | **1,158** | 42.224 | **0.5376** |
| SoL-Pi [Performance] | 2.1016 | 1,605 | **50.482** | 0.6235 |

- **SoL-Pi [Efficiency]** 组合全部四个机制；**SoL-Pi [Performance]** 对每个模型取得分最高的单机制（GPT-5.6 Sol 用 ObservationPack，Opus 5 用 Action Fusion）。
- **迁移**：SoL-Pi 用 GPT-5.6 Sol 开发，随后**不经进一步搜索或适配**直接应用到 Opus 5。在 Opus 5 上，它保留 Pi 平均得分的 **94.3%**，同时相对 Pi 的点估计把 token 流量降低 **44.7%**、API 成本降低 **33.5%**——这是向未见 LLM 后端迁移的初步证据。
- **缓存权衡**：以 GPT-5.6 Sol 为例，完整组合把 cache-read 流量从 2.1326 B 降到 1.0605 B token，cache-write 流量从 0.0141 B 升到 0.0316 B；尽管 cache-write 增加，总模型成本仍从 \$1,339 降到 \$894。每种单机制配置在两个后端下也都降低了"每分成本"，支持在评估时把**完整任务成本**与任务质量一并看，而不只是看缓存复用率。

### Terminal-Bench 4（63 个 CPU-only 任务）

在 63 个 Terminal-Bench 4 的 CPU-only 任务上：

| Harness | 解出任务数 | 总模型成本 | 每题成本 |
| --- | --- | --- | --- |
| Codex | 18 | — | — |
| Pi | 18 | \$286.45 | \$15.91 |
| **SoL-Pi** | 15 | **\$211.12** | **\$14.07** |

相对 Pi，SoL-Pi 把总模型成本降低 **26.3%**、把每题成本降低 **11.6%**——这说明效率收益并不局限于 EdgeBench。

### IMO 2026

在 IMO 2026 上（GPT-5.6 Sol，xhigh），要求每个解答都用 **Lean 4** 形式化并验证：SoL-Pi 在 6 道题中通过 3 道，总模型成本 **\$62.69**，每题通过成本 **\$20.90**，低于 Codex 的 \$22.89 与 Pi 的 \$25.32。

### 经由 SoL-Pi 的高效 Agent Swarm

一个高效的 harness 是否也能让**集体搜索**更经济？作者在 Anthropic 原始的 performance take-home（一个用模拟机器周期评分的 kernel 优化任务）上测试了 SoL-Pi。

设置：**1 个 GPT-5.6 Sol 协调者（运行在 Codex 中）指挥 20 个 GPT-5.6 Luna worker**，全部 xhigh；worker 分成 **5 组 × 4 个**，每组有独立工作区与本地证据板。对比中两组条件分别用 SoL-Pi 与 Pi 作为 worker harness，协调者都是 Codex agent。同组内可点对点传递笔记，协调者在组间转发紧凑发现；候选快照经冻结的官方验证，只有主 agent 接受的严格改进才会成为提交与得分记录并回灌给协调者。

三次独立的 2 小时试验（同一冻结起点，控制组顺序执行、单 agent 先跑）：

| 配置 | Cycles ↓ | 模型成本 ↓ |
| --- | --- | --- |
| 单 agent Sol | 1,333 | \$39.20 |
| Sol + 20 Pi worker | 1,366 | \$82.12 |
| **Sol + 20 SoL-Pi worker** | **1,127** | **\$60.11** |

SoL-Pi 组合同时把验证前沿推得更远、并把总成本压在单 agent 与 Pi swarm 之间——即"更低成本的已验证前沿"。

## 讨论

### EdgeBench 让长时程效率变得可测量

作者选择 EdgeBench，是因为它让 agent 在动辄数小时的轨迹上运行：在当时能找到的公开基准里，它是唯一一个稳定支持约 2–12 小时连续推理与工具使用的基准。常见的替代品——如 Terminal-Bench 2.1 与 SWE-bench——通常在一小时内结束。

更长的时程对测量 token 效率至关重要：在短任务上，上下文重放、大型工具输出、缓存写入与额外模型轮次几乎没有时间累积，单轮的小额节省会被启动成本与任务间差异淹没；而在数小时的运行中，同样的浪费来源会反复出现，使 harness 层面的效率差异更容易被测量。

### 广度能逃离局部搜索盆地

作者沿两条轴扩展自动研究：深度优先（DFS）保持一条支线存活、反复打磨其最新候选；广度优先（BFS）展开许多独立想法，再给每个有希望的支线一条自动研究循环去实现、测试、加固。

在运行中他们观察到一个定性规律：大约 **5 到 10 轮迭代**之后，即使是 xhigh 的 GPT-5.6 Sol 也可能卡在局部盆地中，对同一设计做越来越小的调整而不改变方向。广度优先表现不同：多数想法未通过验证，但增大起始想法的多样性，偶尔会暴露出一个不寻常的候选，让后续循环得以实现并加固它——这些跳跃产出了本项目中最有用的一些 harness 改动。转化率始终很低：**大约每 40 个起始想法只有 1 个通过验证**。是广度让这些稀有候选变得可被发现。

### 广度与隔离支撑泛化

作者认为有两个条件尤其重要：其一是通过广域搜索造出的多样化想法池；其二是稳健的验证——评估环境应当与搜索或训练**完全隔离**，并反映真实部署中的变化与失败模式。缺了这两者，自动研究可能只在某一个环境里提升了表现，却没有让系统在它之外也变好。

### 人设定先验、并检视存活者

当 AI 系统开始改进自己周围的机器时，人类在递归自我改进中的角色仍未定型。SoL-Pi 最好被理解为一个**混合式自动研究循环**：人类提供关于 harness 原则与机制的早期先验；在扩大想法池之前，人类过滤掉对本项目探索价值有限的方向（例如对基础 harness 超参数的搜索）。一旦某个想法进入自动研究循环，循环便在研究与验证过程中无人工干预地运行；当一个候选存活下来，人类回来理解 agent 发现的机制，并把它的代码重构成干净、可维护的实现。

全自主 RSI 是否终究是正确的终局，仍是一个开放问题：在一个开放式循环里，目标、证据或实现上的漂移可能在人类察觉之前复利式累积，后果也可能难以逆转。因此，人类判断与机器规模研究之间的关系需要持续研究——人应当在哪里提供先验、把住搜索预算、审阅被接受的改动、清理实现？又应当在哪里退后一步？

### 任务多样性或许能扩展 harness 质量

SoL-Pi 还运行了一个初步的闭环：agent 收集或合成任务、构造可执行环境、收集轨迹、验证候选，并更新自己的 harness。

作者把这一方向称为 **harness 预训练**（pretraining the harness）：在部署之前，让 harness 搜索面对一条不断扩张的自生成任务与环境流，并保留在这一分布上都能存活的机制。这条研究线仍处于早期；作者预期会出现一种类似模型 scaling law 的 **harness 扩展律**——随着算力与 rollout 环境多样性的增长，harness 应当变得更有能力、更稳健、更高效。

### 递归式高效改进（Recursive Efficient Improvement, REI）

效率本身也可能变成递归的：一个更高效的 harness 可以降低"用来构建其后继者"的自动研究成本。作者计划把 SoL-Pi 作为下一轮研究的起点 harness——更低的单次运行成本能让固定预算覆盖更多可执行环境、轨迹与研究想法。在这种视角下，效率既是 harness 研究的产出，也是扩展后续搜索的资源，因此一个更高效的 harness 可能帮助发现一个**更**高效的 harness。作者把这种可能性称为**递归式高效改进**（recursive efficient improvement），并明确将其定位为一项长期研究愿景，而非本研究已展示的复利效应。

## 作者

Haozhe Liu\*、Tian Ye\*、Sensen Gao†、Qihang Cao†、Yitong Li†、Mingchen Zhuge、Duomin Wang、Ruihua Zhang、Jiawang Bian、Lei Zhu、Ligeng Zhu、Enze Xie、Song Han\*（\* 同等贡献；† 核心贡献者）。

SoL-Pi · SIGIL
