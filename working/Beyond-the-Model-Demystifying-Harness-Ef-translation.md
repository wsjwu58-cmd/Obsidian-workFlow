---
created: 2026-10-03
updated: 2026-10-03
title: 超越模型：揭开软件工程智能体中 Harness 效应的面纱
sourceUrl: https://arxiv.org/abs/2609.32459
sourceAuthor: Haichuan Hu、Quanjun Zhang、Shengcheng Yu、Zhifei Chen、Tianyu Luo、Chunrong Fang、Zhenyu Chen、Liang Xiao
translatedAt: 2026-10-03
sources: [references/articles.md 待处理队列]
tags: [Agent Harness, Harness 工程, 软件工程智能体, SE Agent, SWE-bench Pro, ProgramBench, GitTaskBench, mini-SWE-agent, OpenCode, NanoHarness, 工具注册表, 上下文压缩, 显式规划, 子智能体, 惰性技能, Qwen, DeepSeek, 代码生成, type/翻译]
---

# 超越模型：揭开软件工程智能体中 Harness 效应的面纱

> [arxiv.org/abs/2609.32459](https://arxiv.org/abs/2609.32459)｜分类：cs.SE（软件工程）
> 作者：Haichuan Hu、Quanjun Zhang、Shengcheng Yu、Zhifei Chen、Tianyu Luo、Chunrong Fang、Zhenyu Chen、Liang Xiao
> 单位：1 南京理工大学（Nanjing University of Science and Technology）、2 慕尼黑工业大学（Technical University of Munich）、3 南京大学（Nanjing University）
> 联系：huhaichuan2024@gmail.com、quanjunzhang@njust.edu.cn、shengcheng.yu@tum.de、chenzhifei@njust.edu.cn、Ty_L191025@outlook.com、fangchunrong@nju.edu.cn、zychen@nju.edu.cn、xiaoliang@mail.njust.edu.cn
> 提交：2026-09-26（arXiv v1）｜许可：CC BY 4.0
> DOI：https://doi.org/10.48550/arXiv.2609.32459
> 关键词：大语言模型、Agent Harness、软件工程、代码生成、编码智能体

## 摘要

基于大语言模型（Large Language Model, LLM）的智能体正越来越多地用于软件工程（software engineering, SE）任务，但其性能并非仅由基座模型（base model）决定。智能体 harness（agent harness）在很大程度上塑造了 SE 智能体与代码仓库交互、执行动作以及验证解决方案的方式。然而，harness 设计所扮演的角色仍未被充分理解，尤其是在不同模型、任务与 harness 组件之间。本文对 SE 智能体中的 harness 效应开展了一项系统性的实证研究。我们首先在三个基准——SWE-bench Pro、ProgramBench 与 GitTaskBench——上，用来自两个主流开放权重（open-weight）模型家族 Qwen 与 DeepSeek 的十个模型，评测了两个具有代表性的 harness：mini-SWE-agent 与 OpenCode。随后，我们构建了 NanoHarness——一个构建于 mini-SWE-agent 之上的轻量级模块化 harness，并用它分析五个具有代表性的 harness 组件：工具注册表（tool registry）、上下文压缩（context compression）、显式规划（explicit planning）、子智能体（subagents）与惰性技能（lazy skills）。

实验结果表明，harness 的有效性同时取决于模型能力与任务类型。随着模型能力提升，复杂 harness 在 SWE 风格的问题修复上带来的边际收益递减，但在更复杂、更开放的仓库级任务上，却能让更强的模型受益。ProgramBench 上的组件级分析进一步表明，结构化工具使用与任务专属子智能体带来了最稳定的提升，而上下文压缩与通用子智能体则可能损害仓库生成性能。当所有组件组合在一起时，NanoHarness 在 Qwen3.7-Max 与 DeepSeek-V4-Pro 上分别比 mini-SWE-agent 提升 7.37 与 6.21 个百分点，收复了产品级 harness 的大部分增益。这些发现凸显出：harness 设计是 SE 智能体性能的一等（first-class）因素，并为构建更有效、更高效的编码智能体提供了洞见。

**关键词：** 大语言模型、Agent Harness、软件工程、代码生成、编码智能体

## 1 引言

基于大语言模型（LLM）的智能体正越来越多地被用于解决软件工程（SE）任务，例如问题修复（issue resolution）[11][56][64]、代码修改 [14][16][22] 与测试生成 [29][47]。尽管大量进展由更强的基础模型（如 GPT [42][1]、Claude [4]、Gemini [43]、DeepSeek [26]、Qwen [54]）驱动，但编码智能体的性能同样高度依赖于围绕模型、位于模型之外的基础设施，包括上下文检索 [34][62]、工具使用 [12][63]、执行环境 [51]、补丁生成 [40][21] 与验证 [13][65]。这套基础设施通常被称为智能体 harness [30][68]。

Figure 1：在 SWE-bench Verified 上比较「固定模型」与「固定 harness」两种设置。结果采集自排行榜。

SWE-bench Verified 排行榜 [20] 上公开报告的结果表明，harness 设计的影响可能与模型选择相当。如图 1 所示，在固定模型的情况下，表现最好与最差的 harness 之间差距达到 **19.4 个百分点**，接近固定 harness 时 Claude 各模型之间 **22.8 个百分点**的差距。Epoch AI [9] 也指出，harness 与模型选择同样重要，一个设计良好的 harness 可以带来大约 **20%** 的性能提升。这些现象促使我们开展一项受控分析：究竟是哪些 harness 设计选择带来了这些增益，以及它们能否跨模型、跨任务迁移。

尽管影响如此显著，既有 SE 研究尚未把 harness 设计单独作为系统研究的对象。近期工作 [45][23][7][60][48] 针对特定软件工程场景提出了能力越来越强的编码智能体。这些智能体必然会做出具体的 harness 层面选择，例如如何检索仓库上下文、如何暴露工具、如何规划编辑、如何运行测试以及如何选择最终补丁。然而，这些选择通常是作为端到端智能体系统的一部分被评测，而不是作为可分离的设计组件被分析。因此，我们仍不清楚哪些 harness 组件驱动了改进、它们如何相互作用，以及它们的效应如何依赖基座模型与任务类型。

为弥合这一差距，我们对 SE 智能体中的 harness 开展了一项实证研究。我们的研究聚焦于两条互补的视角：(1) 模型、harness 与任务如何共同塑造智能体性能；(2) harness 组件如何对通用 SE 任务的性能做出贡献。

就第一条视角而言，我们在三个覆盖 SE 生命周期大部的代表性 SE 任务上评测智能体：SWE-bench Pro [11] 上的问题修复、ProgramBench [57] 上的仓库级代码生成，以及 GitTaskBench [31] 上的以仓库为中心的真实任务求解。我们在两种对比鲜明的 harness 配置下研究这些任务：mini-SWE-agent [56]，一个具备基础命令行交互能力的轻量级 harness；以及 OpenCode [2]，一个设计更复杂的产品级 harness。我们把这些 harness 与两个模型家族 Qwen [54] 和 DeepSeek [26] 配对，每个家族选取五个代表性模型。总体而言，这一设计产生了 **60 种实验配置（3 任务 × 2 harness × 10 模型）**，使我们能够系统性地分析模型、harness 与任务如何共同塑造智能体性能。

就第二条视角而言，我们参照商业 harness 的设计（如 Claude Code [3] 与 Codex [33]）识别出现代 harness 架构的五个核心组件，并以最小形式实现每个组件。从 mini-SWE-agent 出发，我们以积木式（building-block）方式向既有 harness 增量加入这些即插即用组件，构建出一个受控的 harness 变体 NanoHarness，用于组件级分析。以 ProgramBench 作为试验台，我们既评测每个组件的单独效应，也评测整合全部组件后的组合效应。此外，我们采集并分析 NanoHarness 及其各变体的性能与执行行为，并进一步开展轨迹级分析。

实验结果表明，harness 设计显著塑造了 SE 智能体的性能，但其效应既不均匀也不单调。首先，harness 在不同任务范式下扮演不同角色。在 SWE 风格的问题修复中，工作流相对固定、编辑往往局部化，复杂 harness 主要补偿较弱的模型，其边际收益随模型能力提升而下降。相反，在较新、更开放的仓库级任务（如 ProgramBench 与 GitTaskBench）上，复杂 harness 更像能力放大器：只有足够强的模型才能可靠地利用额外的流程复杂度。

其次，我们的组件与轨迹分析表明，harness 的增益较少来自增加脚手架或消耗更多 token，更多来自规训（regulate）智能体在仓库中探索与行动的方式。结构化工具使用与任务专属子智能体提供了最稳定的提升，而上下文压缩与通用子智能体则可能损害仓库生成性能。NanoHarness 在 Qwen3.7-Max 与 DeepSeek-V4-Pro 上分别比 mini-SWE-agent 提升 7.37 与 6.21 个百分点，并仅以受控的 prompt 增长就缩小了与产品级 harness 的大部分差距。这些结果说明，有效的 harness 之所以改进 SE 智能体，是把原始探索转化为结构化、与任务对齐的交互，而不是单靠提升模型能力。

本文做出以下贡献：

(1) **大规模实证研究。** 我们在三个具有代表性的基准上开展系统性实证研究，使用来自 Qwen 与 DeepSeek 的 10 个不同 LLM，prompt 侧 token 用量超过 10B（Qwen）与 20B（DeepSeek）。

(2) **组件级拆解。** 我们把现代 SE 智能体 harness 拆解为若干代表性组件，并构建 NanoHarness——一个轻量级模块化 harness，从而支持受控的组件级分析。

(3) **行为洞见。** 我们揭示 harness 机制如何影响性能与执行行为，表明有效的 harness 主要通过促成结构化工具使用与更受规训的探索来提升 SE 智能体性能，而不是单靠模型改进。

## 2 预备知识

本节简要介绍现代 harness 设计的架构与主要组件。

### 2.1 架构

如图 2 所示，我们给出一个现代智能体 harness 的通用架构。harness 围绕模型进行组织，我们将其拆解为 **12 个模块** [30][68]。蓝色高亮模块是本工作的关注重点，因为它们代表了 harness 的基础能力，并直接影响智能体性能。灰色模块包括环境、权限、日志、可观测性、知识源与评测等支撑组件。尽管这些模块也是完整智能体系统中不可或缺的部分，但它们通常扮演更偏工程化的角色，或在不同 harness 之间充当外部约束。因此我们不再详细讨论其内部机制。接下来我们介绍 harness 的五个核心模块。

![参见图注](https://arxiv.org/html/2609.32459v1/arch.png) Figure 2：现代智能体 harness 的通用架构。

### 2.2 组件

#### 2.2.1 工具

工具暴露诸如文件查看、编辑、搜索、shell 执行与测试等外部动作。工具的接口决定了模型能观测到怎样的仓库状态，以及它能以多安全的方式对该状态采取行动。

#### 2.2.2 上下文与记忆

上下文与记忆决定在智能体循环期间，哪些任务信息、观测结果、代码片段、输出与中间推理保持可用。有效的管理会在保留有用状态的同时，限制无关或冗余的历史。

#### 2.2.3 规划

规划帮助智能体分解任务、跟踪中间目标并决定后续动作。harness 可以通过显式计划、迭代式重规划或轻量级动作选择来实现这一点。

#### 2.2.4 子智能体

子智能体把任务的某些部分委派给专门的角色或执行流，例如定位、实现或验证。这可以改善任务分解，但也会增加协调与通信开销。

#### 2.2.5 技能

技能编码可复用的高层工作流，例如调试、验证或从失败尝试中恢复。当某个流程与当前任务相关时，技能可减少重复决策。

## 3 关于 SE 智能体 Harness 的研究

### 3.1 总体研究设计

**概览。** 图 3 给出了我们对 SE 智能体 harness 的实证研究概览。该研究分为两个互补的部分。第一，我们通过在不同能力水平的模型上，跨软件开发生命周期的一系列 SE 任务，用轻量级与产品级两类 harness 进行评测，来考察模型、harness 与任务的联合效应。第二，我们通过向一个最小基线 harness 逐步加入核心 harness 机制（包括工具注册表、上下文压缩、显式规划、子智能体与惰性技能），开展组件级分析。这一设计使我们不仅能够研究 harness 如何与模型能力和任务特征交互，还能研究单个组件及其组合如何影响智能体的性能、行为与效率。

![参见图注](https://arxiv.org/html/2609.32459v1/harness_analysis.png) Figure 3：我们的智能体 harness 研究概览：(1) 模型–harness–任务的联合效应；(2) 组件级 harness 分析。

**研究 1：度量模型、harness 与任务的联合效应。** SE 研究主要沿三条方向展开：改进面向编码的模型、设计智能体 harness，以及构建 SE 任务与基准。面向模型的研究 [39][59][55] 通过代码预训练、微调、强化学习或推理时优化来训练模型。面向 harness 的研究 [52][8][49] 改进智能体使用仓库、工具、测试与执行环境的方式。面向任务与基准的研究 [38][46] 设计贴近真实的 SE 任务与评测协议。然而，这些方向通常各自独立推进，模型、harness 与任务的联合效应仍未被充分探索。

为考察这些联合效应，我们围绕这三个因素设计第一项研究。对于模型，我们从同一模型家族中选取多个能力从弱到强的模型，使性能差异能够反映模型规模与能力的变化，同时减少模型血缘（model lineage）带来的差异。对于 harness，我们比较一个轻量级基础 harness 与一个更复杂的产品级 harness，从而度量周围的智能体工作流在多大程度上改变了 SE 任务性能。对于任务，我们选择覆盖软件开发生命周期不同阶段的基准，包括需求分析 [10]、架构设计 [66]、编码 [19]、测试 [29] 与验证 [13]。通过把这些因素组合成一个统一的三维实验矩阵，我们在每个任务上用每个 harness 评测每个模型，从而比较它们的单独效应并分析它们在基于 LLM 的 SE 智能体中如何交互。

**研究 2：组件级 harness 分析。** 第二项研究聚焦智能体 harness 的内部设计。如 §2 所述，现代 SE 智能体 harness 可拆解为 12 个组件。为研究代表性组件背后的机制，我们在 mini-SWE-agent 之上实现了一个模块化 harness，称为 NanoHarness，其中每种机制都可以独立启用或禁用。具体而言，我们实例化了五种代表性机制：工具注册表、上下文压缩、显式规划、子智能体与惰性技能。这种模块化设计使我们能够单独以及组合地评测它们对 SE 任务的影响，从而分析不同的 harness 机制如何在模型选择之外对长时程（long-horizon）性能做出贡献。

**工具注册表（Tool Registry）。** 我们把 mini-SWE-agent 的 Bash 交互模式扩展为一个工具层，通过统一的注册表与原生工具调用机制实现。我们引入四个面向文件系统的工具：read_file、write_file、edit_file 与 glob。read_file 提供有界的文件查看，write_file 负责创建或覆盖文件，edit_file 施加局部文本修改，glob 支持基于模式的文件发现。

**上下文压缩（Context Compression）。** 我们实现了一个上下文压缩模块，用于在有限上下文窗口下进行长时程执行。过大的工具输出会被持久化到工作区，prompt 中只保留路径与简短预览。当历史变得过长时，该模块会执行消息剪裁（message snipping）与观测压缩（observation compaction），同时保留近期结果与高价值输出。如果上下文仍超过限制，则触发基于 LLM 的摘要以保留必要信息。压缩也可以被手动调用，或在出现上下文窗口错误后触发，并保留日志以便审计。

**显式规划（Explicit Planning）。** 规划模块为智能体加入了一种 TodoWrite 风格的轻量级规划机制。启用后，智能体可以调用 todo_write 维护一份简短的任务清单，其中最多一项可被标记为 in_progress。每次更新都会替换完整的 todo 列表，并由 TodoManager 校验条目格式、状态取值、列表长度与规划一致性。当前计划会被渲染回 prompt，并保存到轨迹元数据中。为避免计划过期，当计划在数轮内未被更新时，智能体会注入提醒。

**通用 / 任务专属子智能体（General/Task-Specific Subagents）。** 子智能体模块按需提供专家能力，同时把任务控制、预算管理与最终提交留给父智能体。每个子智能体在共享工作区中以全新历史运行，通过 SubagentRunner 使用受限的工具白名单，并通过 finish_subagent 返回结构化报告。嵌套委派被禁用，轨迹会被记录以便审计与成本分析。

(1) **通用 SE 子智能体。** 第一种类型由按软件开发生命周期组织的软件工程子智能体构成，包括 requirement_analysis、architecture_design、code_generation、test_generation 与 defect_repair。每个子智能体被分配适当的工具集，并返回结构化产物供父智能体整合。

(2) **任务专属子智能体。** 第二种类型由用于行为分析、差分测试与提交审查的专用配置构成。这些子智能体支持有针对性的探索、验证与最终检查。

**惰性技能（Lazy Skills）。** 技能模块把流程性知识当作惰性加载、可调用的资源，从而降低 prompt 开销。启用后，prompt 中只包含一份紧凑的技能目录，智能体可在需要时调用 load_skill(name) 获取详细指引。SkillLoader 依据所配置 SKILL.md 文件中的元数据构建这份目录。已加载的技能以结构化包装返回，支持实现、调试、测试、模糊测试与最终审查。可用技能定义于表 1。

Table 1：惰性加载技能概览。

| 技能 | 用途 |
| --- | --- |
| Terminal Workflow | 指导基于终端的任务求解，从探索到验证与提交。 |
| Minimal Implementation | 鼓励小而聚焦的实现与快速验证。 |
| Build Diagnostics | 帮助诊断构建、可执行文件、工具链与依赖问题。 |
| Test Triage | 分析失败的测试、日志、退出码与接口不匹配。 |
| CLI Fuzzing | 生成有界的边界用例测试并比较 CLI 行为。 |
| Submission Review | 检查构建可复现性、可执行文件正确性与仓库整洁度。 |

### 3.2 研究问题

基于我们的研究目标，我们提出以下三个研究问题。

**RQ1：模型、harness 与任务之间存在怎样的关系？**

- RQ1.1：harness 性能如何随模型能力伸缩？
- RQ1.2：harness 在不同 SE 任务之间有何差异？

**RQ2：harness 组件如何影响 SE 智能体？**

- RQ2.1：每个组件的单独效应是什么？
- RQ2.2：所有组件的组合效应是什么？

**RQ3：harness 机制如何影响智能体的执行行为与效率？**

- RQ3.1：harness 机制如何改变智能体的工具使用、上下文使用与 token 使用？
- RQ3.2：harness 机制如何影响长时程 SE 任务中的常见失败模式？

## 4 实验设置

### 4.1 任务与数据集

我们在三个互补的 SE 基准上评测 harness（表 2）：ProgramBench [57]、SWE-bench Pro [11] 与 GitTaskBench [31]。这些数据集覆盖 SE 生命周期的关键阶段，包括需求理解、架构设计、代码生成、测试与验证，因而适合评估复杂、长时程 SE 任务下的 harness 有效性。具体而言，ProgramBench 面向仓库级代码生成，SWE-bench Pro 聚焦真实世界的问题修复，GitTaskBench 评测以仓库为中心的任务求解。

Table 2：实验中使用的数据集概览。

| 数据集 | 任务 | 语言 | 规模 |
| --- | --- | --- | --- |
| ProgramBench [57] | 仓库生成 | Rust、Go、C/C++、Java、Haskell | 200 |
| SWE-bench Pro [11] | 问题修复 | Python、JS/TS、Go | 731 |
| GitTaskBench [31] | 仓库任务求解 | Python | 54 |

### 4.2 Harness 选择

我们选取 mini-SWE-agent [56] 与 OpenCode [2] 作为两个具有代表性的 harness。mini-SWE-agent 充当最小 harness 设置，提供以命令行为中心的简洁基础智能体工作流，代表一个模型外部支持有限的轻量级 harness。相比之下，OpenCode 代表一个产品级 harness，其设计更复杂，并集成了多个面向仓库交互、工具使用、上下文处理与任务执行的组件。这种对比使我们能够研究 harness 设计复杂度如何在不同模型与 SE 任务上影响性能。

### 4.3 模型选择

我们聚焦开放权重模型家族，以支持可复现的评测，并在能力水平不同但血缘相近的模型之间做受控比较。因此，我们没有使用闭源权重模型（如 GPT、Claude），而是选取两个广泛使用的开放权重模型家族 Qwen [6][54] 与 DeepSeek [26]，每个家族挑选五个模型。我们依据 Coding Index [5] 提供的官方分数对模型按能力排序（图 4）。这一选择与排序给出了各模型编码能力的概览，并便于在强、弱模型之间进行比较。此处的 DeepSeek-R1 指原始的 DeepSeek-R1 发布版，而非后续的 DeepSeek-R1-0528 更新；DeepSeek-V3 指 DeepSeek-V3-0324。所有模型均在非思考模式（non-thinking mode）下评测。

Figure 4：基于 Coding Index 的模型编码能力排名。

### 4.4 实现

我们在所有实验中采用统一的执行协议。对于模型推理，我们把所有模型的 temperature 设为 0.0 以降低随机性。对于 SWE-bench Pro 与 GitTaskBench，我们遵循原始评测设置，把每个任务限制为 250 个智能体步（agent steps）。对于 ProgramBench，我们把步数上限从原始的 1,000 步降到 300 步以降低评测成本。每个任务还受 **6 小时墙钟限制**与**每次命令执行 3 分钟超时**的约束。

为控制 RQ1 的评测成本，我们对较大的基准使用随机子集：RQ1.1 使用 SWE-bench Pro 中随机采样的 300 个实例，RQ1.2 使用 ProgramBench 中随机采样的 70 个实例。我们在所有配对的模型–harness 配置中使用相同的采样实例。RQ1.2 使用 GitTaskBench 全部 54 个实例。RQ2 与 RQ3 中的组件级实验使用完整的 200 实例 ProgramBench 集合。

SWE-bench Pro 与 ProgramBench 在 Docker 容器中评测，而 GitTaskBench 在本地环境中评测。对于容器化任务，我们通过 `--network none` 禁用网络访问，为每个容器分配 20 个 CPU 与 60 GB 内存，设置 7 小时容器寿命，并禁用 SYS_PTRACE。对于 GitTaskBench，我们隔离工作目录并阻断工作区之外的操作。

对于 NanoHarness，我们把子智能体最大轮数设为 50，把规划模块限制为最多 10 个 todo 条目。上下文压缩以 350K-token 预算启用，压缩触发时保留最近 20 条消息。

## 5 结果与分析

### 5.1 RQ1：模型、harness 与任务之间的关系

#### 5.1.1 RQ1.1——harness 性能随模型能力的伸缩

为研究 harness 带来的增益如何随模型能力伸缩，我们首先分析 SWE-bench Verified [20] 排行榜中配对模型（matched-model）的结果。如表 3 所示，对较弱的模型而言，更先进的 harness 相对 mini-SWE-agent 提供更大的改进，而对较强的模型，这一差距变小。例如，OpenHands 的增益从 Claude 3.7 Sonnet 上的 +13.60 pp 降到 Claude 4 Sonnet 上的 +5.47 pp，SWE-agent 的增益在同一模型演进下从 +9.60 pp 降到 +4.07 pp。这表明 harness 复杂度可以显著改善较弱或中等水平的模型，但其边际收益可能随模型能力提升而被压缩。

Table 3：SWE-bench Verified 上相对 mini-SWE-agent 的配对模型 harness 改进。

| Harness | 模型（弱 → 强） | mini-SWE | 增益 |
| --- | --- | --- | --- |
| SWE-agent | Claude 3.7 Sonnet | 52.80 | +9.60 |
| SWE-agent | Claude 4 Sonnet | 64.93 | +4.07 |
| OpenHands | Claude 3.7 Sonnet | 52.80 | +13.60 |
| OpenHands | Claude 4 Sonnet | 64.93 | +5.47 |
| Tools | Claude 3.7 Sonnet | 52.80 | +10.40 |
| Tools | Claude 4 Sonnet | 64.93 | +7.47 |
| Tools | Claude 4 Opus | 67.60 | +5.60 |

我们在 SWE-bench Pro [11] 随机 300 实例样本上的受控实验进一步支持这一趋势，但也揭示出伸缩模式在不同模型家族之间有所差异。对于 Qwen 家族，效应相对平滑。随着模型能力从 Qwen3-Max 提升到 Qwen3.7-Max，mini-SWE-agent 与 OpenCode 都在改进，但二者之间的性能差距逐渐收窄。具体而言，OpenCode 的优势从 Qwen3-Max 上的约 6 pp 降到 Qwen3.7-Max 上的 2.67 pp，说明更强的 Qwen 模型对产品级 harness 所提供的额外脚手架依赖更少。

表 4 中的轨迹统计为这一解释提供了进一步证据。OpenCode 在 Qwen 各模型上的智能体步数保持相对稳定，而工具调用次数从 39.87 增加到 72.23。这表明更强的 Qwen 模型可以在相近的决策步数内，用 OpenCode 执行更密集的工具辅助探索。相比之下，mini-SWE-agent 被约束在每步大约一次工具调用，其步数与 token 用量随模型能力提升先增后减。这表明更强的 Qwen 模型在轻量级 harness 下逐渐变得更有选择性，聚焦于更少但更有用的交互。

Figure 5：SWE-bench Pro 上不同 harness 的 Qwen 模型伸缩对比（N=300）。

Table 4：Qwen 模型的平均样本级统计。

| Harness | 模型 | 步数 | 工具 | Prompt | Response |
| --- | --- | --- | --- | --- | --- |
| mini-SWE | Qwen3-Max | 31.12 | 30.02 | 369,443 | 5,110 |
| mini-SWE | Qwen3.5-Plus | 89.72 | 88.05 | 2,347,080 | 30,942 |
| mini-SWE | Qwen3.6-Plus | 57.81 | 56.10 | 1,573,644 | 66,793 |
| mini-SWE | Qwen3.6-Max | 54.15 | 52.47 | 1,379,883 | 27,237 |
| mini-SWE | Qwen3.7-Max | 43.58 | 42.36 | 770,319 | 18,732 |
| OpenCode | Qwen3-Max | 35.95 | 39.87 | 1,069,425 | 6,442 |
| OpenCode | Qwen3.5-Plus | 37.84 | 57.13 | 1,702,800 | 9,505 |
| OpenCode | Qwen3.6-Plus | 37.91 | 61.15 | 1,499,056 | 11,132 |
| OpenCode | Qwen3.6-Max | 36.49 | 64.87 | 1,395,815 | 11,283 |
| OpenCode | Qwen3.7-Max | 37.38 | 72.23 | 1,523,661 | 14,921 |

如图 6 所示，DeepSeek 呈现出不同的伸缩模式。与 Qwen 不同，harness 增益并未在整个模型序列上平滑下降。OpenCode 对 DeepSeek-R1 几乎带不来改进，对 DeepSeek-V3、DeepSeek-V3.1 等中间模型带来较大增益，随后在 DeepSeek-V4-Pro 上再次与 mini-SWE-agent 收敛，最终得分为 OpenCode 的 34.3% 与 mini-SWE-agent 的 33.7%。这种非单调模式暗示了一种阈值效应（threshold effect）：过弱的模型可能无法可靠地利用复杂 harness，而足够强的模型即便在轻量级 harness 下也能解决许多实例，从而降低了额外 harness 机制的边际收益。

表 5 进一步表明，OpenCode 对 DeepSeek 执行行为的改变比在 Qwen 上更激进。对于 DeepSeek-V3.1 与 DeepSeek-V3.2，OpenCode 相比 mini-SWE-agent 会导致显著更多的步数、工具调用与 prompt token，说明其探索更广、对产品级工作流的使用更重。然而对于 DeepSeek-V4-Pro，OpenCode 使用的步数少于 mini-SWE-agent，同时每步仍进行更多工具调用。这表明最强的 DeepSeek 模型能以更紧凑、工具更密集的方式与 OpenCode 交互，但其相对 mini-SWE-agent 的性能增益变得非常小。

Figure 6：SWE-bench Pro 上不同 harness 的 DeepSeek 模型伸缩对比（N=300）。

Table 5：DeepSeek 模型的平均样本级统计。

| Harness | 模型 | 步数 | 工具 | Prompt | Response |
| --- | --- | --- | --- | --- | --- |
| mini-SWE | DeepSeek-R1 | 17.71 | 15.97 | 127,552 | 31,280 |
| mini-SWE | DeepSeek-V3 | 15.90 | 14.69 | 104,289 | 1,886 |
| mini-SWE | DeepSeek-V3.1 | 58.66 | 56.66 | 1,000,415 | 6,905 |
| mini-SWE | DeepSeek-V3.2 | 79.99 | 72.23 | 1,687,660 | 13,665 |
| mini-SWE | DeepSeek-V4-Pro | 61.77 | 60.12 | 1,860,832 | 29,326 |
| OpenCode | DeepSeek-R1 | 8.98 | 7.85 | 146,731 | 20,787 |
| OpenCode | DeepSeek-V3 | 36.42 | 34.66 | 1,163,976 | 5,488 |
| OpenCode | DeepSeek-V3.1 | 74.91 | 74.08 | 2,874,875 | 10,661 |
| OpenCode | DeepSeek-V3.2 | 89.42 | 101.18 | 2,796,537 | 19,093 |
| OpenCode | DeepSeek-V4-Pro | 31.96 | 70.42 | 1,178,990 | 16,397 |

**对 RQ1.1 的回答：**

(1) 复杂 harness 的边际收益通常随模型能力提升而递减：在 SWE-bench Verified 上，相对 mini-SWE-agent 的配对模型增益从 +9.60/+13.60 pp 降到 +4.07/+5.47 pp；在 Qwen 的 SWE-bench Pro 实验中，OpenCode 与 mini-SWE 的差距从 6.00 pp 收窄到 2.67 pp。(2) 这种收敛在不同模型家族之间并不一致。Qwen 遵循平滑收窄的趋势，而 DeepSeek 呈非单调模式，OpenCode 对中间模型（如 DeepSeek-V3.1、DeepSeek-V3.2）帮助更大，并在 DeepSeek-V4-Pro 上几乎与 mini-SWE 收敛（34.3% vs. 33.7%）。

#### 5.1.2 RQ1.2——不同 SE 任务上的 harness 性能

为验证 RQ1.1 的发现是否普遍适用，在 RQ1.2 中我们选取 ProgramBench 与 GitTaskBench，并使用与 RQ1.1 相同的配置开展实验。我们从 ProgramBench 的 200 个实例中随机采样 70 个，包括 20 个 easy、21 个 medium 与 29 个 hard 实例，并使用 GitTaskBench 的全部 54 个实例。

Figure 7：ProgramBench 上不同 harness 的 Qwen 模型伸缩对比（N=70）。Figure 8：ProgramBench 上不同 harness 的 DeepSeek 模型伸缩对比（N=70）。

如图 7 与图 8 所示，我们发现在 ProgramBench 上，OpenCode 并未比 mini-SWE-agent 给较弱模型带来更大改进。只有最新的模型（如 Qwen3.7-Max 与 DeepSeek-V4-Pro）才能稳定利用这一复杂 harness 更有效地完成任务。在 GitTaskBench 上（图 9 与图 10），我们也观察到类似现象：Qwen3.6-Max 与 DeepSeek-V3.1 分别是各自模型家族中开始能够利用 OpenCode 这类复杂 harness 的转折点。

Figure 9：GitTaskBench 上不同 harness 的 Qwen 模型伸缩对比（N=54）。Figure 10：GitTaskBench 上不同 harness 的 DeepSeek 模型伸缩对比（N=54）。

上述结果表明，模型能力并非影响 harness 有效性的唯一因素；任务类型与难度也同样是重要因素。与 ProgramBench 和 GitTaskBench 相比，SWE-bench Pro 的工作流相对固定，代码修改通常只涉及少数文件中的函数。相比之下，ProgramBench 是从零开始的仓库生成任务，往往要求模型在覆盖细粒度功能的同时生成数万行代码。GitTaskBench 的难点在于任务灵活性：它涉及多个目标，要求模型独立理解任务目标、利用仓库信息并设计执行工作流。此外，考虑到近年来产业界对 SWE 式任务的关注日益增长，模型可能接受过任务专属训练，这会使它们在这类任务上天然更强，从而降低对 harness 的依赖。

**对 RQ1.2 的回答：** harness 的有效性不仅受模型能力影响，也受任务复杂度与任务类型影响。对于 SWE-bench Pro，其工作流相对固定、代码修改量小、任务长期受到持续关注，模型普遍展现出较强的适应性。随着模型能力提升，复杂 harness（如 OpenCode）带来的额外增益逐渐减弱。相反，对于 ProgramBench 与 GitTaskBench 这类较新、更复杂的 SE 任务，复杂 harness 能给更强的模型（如 Qwen3.7-Max 与 DeepSeek-V4-Pro）带来更大收益。

### 5.2 RQ2：组件级效应分析

在 RQ1 中，我们把 harness 当作一个整体，分析它在不同 SE 任务上的性能。尽管结果表明复杂 harness（如 OpenCode）相比基础 harness（如 mini-SWE-agent）能提升性能，但这些改进的来源仍不清楚。因此，在 RQ2 中，我们拆解并组合 harness 的代表性组件，构建出轻量且模块化的 NanoHarness。随后，我们在完整的 ProgramBench 集合上，使用两个先进 LLM——Qwen3.7-Max 与 DeepSeek-V4-Pro——对 NanoHarness 进行消融实验。

Figure 11：使用 Qwen3.7-Max 时不同 harness 组件对 ProgramBench 得分的影响。Figure 12：使用 DeepSeek-V4-Pro 时不同 harness 组件对 ProgramBench 得分的影响。

#### 5.2.1 RQ2.1——单独效应

图 11 与图 12 显示，不同 harness 组件对智能体性能的贡献并不均衡。在单个组件中，工具注册表与任务专属子智能体在两个模型上都带来最一致的改进。对于 Qwen3.7-Max，加入工具注册表使 ProgramBench 得分提升 4.57 个百分点，而任务专属子智能体带来最大的单组件增益 5.91 个百分点。对于 DeepSeek-V4-Pro，同样这两个组件也分别带来 3.54 与 4.46 个百分点的强增益。这些结果表明，结构化仓库操作与面向任务的委派对仓库生成任务尤其有用——在这类任务中，智能体必须查看文件、创建或修改多个模块，并反复验证实现行为。

规划与惰性技能也能提升性能，但其效应更温和且依赖模型。显式规划对 Qwen3.7-Max 与 DeepSeek-V4-Pro 都只带来小幅增益，说明轻量级任务清单有助于组织长时程执行，但仅靠规划不足以大幅改善仓库生成。惰性技能对 DeepSeek-V4-Pro 的收益大于对 Qwen3.7-Max，说明当模型能够有效判断何时、如何调用流程性指引时，这类指引更有帮助。

相反，上下文压缩与通用子智能体会同时降低两个模型的性能。上下文压缩使 Qwen3.7-Max 得分降低 4.86 个百分点、DeepSeek-V4-Pro 降低 3.85 个百分点，因为 ProgramBench 需要在长轨迹中保留详细需求、接口约束与实现状态。激进的压缩可能移除后续编码与调试仍然有用的信息。通用子智能体同样表现不佳，说明泛化的 SE 委派可能引入协调开销，或产生与仓库生成的细粒度需求并不直接对齐的产物。

**对 RQ2.1 的回答：** 单个 harness 组件具有异质效应。工具注册表与任务专属子智能体提供最稳定、最可观的增益，规划与惰性技能带来较小或依赖模型的改进，而上下文压缩与通用子智能体可能损害仓库生成任务上的性能。

#### 5.2.2 RQ2.2——组合效应

当所有组件组合在一起时，NanoHarness 在两个模型上都取得了各变体中的最佳性能。对于 Qwen3.7-Max，完整配置把得分从 42.88 提升到 50.25，相对 mini-SWE-agent 取得 7.37 个百分点的增益。对于 DeepSeek-V4-Pro，它把得分从 45.14 提升到 51.35，对应 6.21 个百分点的增益。这些改进大于任何单个组件，说明多种 harness 机制在被整合进统一工作流时能够相互补充。

然而，组合后的改进并非所有单个增益的简单相加。某些组件（如上下文压缩与通用子智能体）单独作用时为负效应，它们与更强组件的交互还可能引入额外开销。这说明 harness 组件并非彼此独立：它们的收益取决于它们在智能体循环中如何被协调。尽管如此，完整的 NanoHarness 配置仍持续改进两个模型，说明结构化工具、任务专属委派与流程性技能等正向组件在恰当组合时可以主导整体效应。

与产品级 harness 相比，NanoHarness 在保持轻量与模块化的同时也取得了有竞争力的性能。在 Qwen3.7-Max 上，NanoHarness 达到 50.25，把与 OpenCode（51.68）和 Claude Code（52.33）的差距分别缩小到 1.43 与 2.08 个百分点。在 DeepSeek-V4-Pro 上，NanoHarness 达到 51.35，同样接近 OpenCode（52.48）与 Claude Code（52.76），差距仅为 1.13 与 1.41 个百分点。这些结果表明，尽管产品级 harness 仍取得最佳得分，一个由代表性组件构成的轻量级模块化 harness 能够收复它们的大部分性能增益。这说明复杂 harness 的收益未必来自其完整的工程栈；相反，一小批经过精心选择与协调的组件就能贡献相当大一部分改进。

**对 RQ2.2 的回答：** 完整的 NanoHarness 配置在各变体中取得最强性能，在两个模型上都超过 mini-SWE-agent，并优于任何单个组件。尽管 NanoHarness 仍略微落后于 OpenCode 与 Claude Code 等产品级 harness，但它以轻量级模块化设计缩小了大部分差距，说明一小组代表性组件就能复现复杂 harness 的相当一部分收益。

Table 6：在 ProgramBench 上比较 NanoHarness 与其他产品级 harness。

| Harness | Qwen3.7-Max | DeepSeek-V4-Pro |
| --- | --- | --- |
| mini-SWE-agent | 42.88 | 45.14 |
| NanoHarness | 50.25 (+7.37%) | 51.35 (+6.21%) |
| OpenCode | 51.68 (+8.80%) | 52.48 (+7.34%) |
| ClaudeCode | 52.33 (+9.45%) | 52.76 (+7.62%) |

### 5.3 RQ3：harness 机制对智能体行为与效率的影响

在 RQ3 中，我们收集 RQ2 中每种配置的性能与成本统计，并进一步分析执行轨迹，以考察 harness 组件如何影响智能体行为。具体而言，RQ3.1 分析 NanoHarness 不同配置在智能体步数、工具调用与 token 使用上的差异，RQ3.2 度量探测（probing）行为的分布模式，并用案例研究说明失败模式的转变。

#### 5.3.1 RQ3.1——对工具使用、上下文使用与 token 使用的影响

表 7 展示了三种主要行为模式。第一，面向工具的机制增加了仓库交互：工具注册表小幅提高工具调用，而任务专属子智能体使 Qwen3.7-Max 的工具调用增加 115.76%、DeepSeek-V4-Pro 增加 73.10%。由于任务专属子智能体改进性能而通用子智能体不能，额外的工具使用似乎只有在指向任务时才有益。第二，上下文压缩降低成本却损害性能。它使两个模型的 prompt token 分别减少 54.29% 与 77.02%，但 RQ2 显示相应得分下降 4.86 与 3.85 个百分点，说明被压缩的历史可能丢失了后续仍需的需求或调试状态。第三，完整的 NanoHarness 配置在受控的 prompt 增长下改进性能：尽管工具调用增加 131.18% 与 83.58%，prompt token 增长却小得多（+16.37% 与 +7.26%），而得分相对 mini-SWE-agent 提升 7.37 与 6.21 个百分点。这说明组合 harness 的增益来自更结构化的交互，而非单纯花费更多 prompt 预算。

**对 RQ3.1 的回答：** harness 机制主要通过三种方式影响执行行为。工具与子智能体增加工具使用，上下文压缩降低成本但可能损害性能，而完整的 NanoHarness 配置通过更结构化的交互与受控的 prompt 增长来改进性能。

Table 7：在 ProgramBench 上，Qwen3.7-Max 与 DeepSeek-V4-Pro 在不同 harness 组件下的平均样本级统计。括号中的百分比表示相对同模型 mini-SWE 的相对变化。

| 模型 | 配置 | 步数 | 工具 | Prompt | Response |
| --- | --- | --- | --- | --- | --- |
| Qwen3.7-Max | mini-SWE | 104.13 | 104.14 | 3,978,148 | 46,763 |
| Qwen3.7-Max | + tools | 105.89 (+1.69%) | 120.87 (+16.06%) | 4,299,572 (+8.08%) | 44,366 (-5.13%) |
| Qwen3.7-Max | + planning | 102.19 (-1.86%) | 104.35 (+0.20%) | 4,817,378 (+21.10%) | 65,679 (+40.45%) |
| Qwen3.7-Max | + skills | 108.69 (+4.38%) | 109.20 (+4.86%) | 4,503,568 (+13.21%) | 47,913 (+2.46%) |
| Qwen3.7-Max | + context | 61.77 (-40.68%) | 62.06 (-40.41%) | 1,818,344 (-54.29%) | 26,577 (-43.17%) |
| Qwen3.7-Max | + specific subagents | 141.29 (+35.69%) | 224.69 (+115.76%) | 4,270,462 (+7.35%) | 72,240 (+54.48%) |
| Qwen3.7-Max | + general subagents | 99.06 (-4.87%) | 157.40 (+51.14%) | 4,372,546 (+9.91%) | 67,919 (+45.24%) |
| Qwen3.7-Max | + all (NanoHarness) | 133.68 (+28.38%) | 240.75 (+131.18%) | 4,629,172 (+16.37%) | 64,751 (+38.47%) |
| DeepSeek-V4-Pro | mini-SWE | 142.19 | 181.84 | 10,065,204 | 91,370 |
| DeepSeek-V4-Pro | + tools | 164.11 (+15.41%) | 204.20 (+12.29%) | 11,979,965 (+19.02%) | 86,982 (-4.80%) |
| DeepSeek-V4-Pro | + planning | 140.66 (-1.07%) | 184.27 (+1.33%) | 10,418,872 (+3.51%) | 91,832 (+0.51%) |
| DeepSeek-V4-Pro | + skills | 147.85 (+3.98%) | 179.22 (-1.44%) | 10,415,011 (+3.48%) | 90,942 (-0.47%) |
| DeepSeek-V4-Pro | + context | 54.17 (-61.91%) | 56.61 (-68.87%) | 2,312,701 (-77.02%) | 33,747 (-63.07%) |
| DeepSeek-V4-Pro | + specific subagents | 190.45 (+33.94%) | 314.77 (+73.10%) | 9,104,564 (-9.54%) | 118,453 (+29.64%) |
| DeepSeek-V4-Pro | + general subagents | 169.54 (+19.24%) | 332.14 (+82.65%) | 15,284,596 (+51.86%) | 145,124 (+58.83%) |
| DeepSeek-V4-Pro | + all (NanoHarness) | 203.53 (+43.14%) | 333.84 (+83.58%) | 10,795,507 (+7.26%) | 103,443 (+13.21%) |

#### 5.3.2 RQ3.2——对失败模式的影响

通过对 mini-SWE-agent 产生的失败与低分轨迹进行人工检查，我们按探测次数与验证行为对失败进行分类，发现模型在 ProgramBench 上主要表现出两种失败模式。(1) **过度探测（excessive probing）**：在探索早期阶段，智能体盲目地对参考二进制执行大量细粒度行为探测，却未能覆盖目标程序的核心功能。结果它耗尽预算，草草结束任务。(2) **探测不足（insufficient probing）**：智能体在仅少量探测（如 ≤20 次）后就假定自己已理解程序核心功能，在实现程序后又只用少量冒烟测试来验证解。如图 13 所示，我们比较了 Qwen3.7-Max 在不同 harness 配置下的探测次数分布。我们观察到，性能增益最大的组件（即任务专属子智能体）大幅降低了 mini-SWE-agent 出现过度探测或探测不足的倾向。在这些改进的基础上，NanoHarness 进一步结合了不同组件的优势。它不仅减少了极端探测行为，还学会使用更多探测来更全面地探索目标程序行为，使探测次数整体分布稳定右移。

![参见图注](https://arxiv.org/html/2609.32459v1/qwen_probe_distribution_dotplot_by_component.png) Figure 13：探测次数分布（Qwen3.7-Max）。

两个案例说明了 NanoHarness 如何缓解这些极端情况。对于过度探测，`jqlang__jq.b33a763` 展示了 NanoHarness 如何减少无产出的探索：mini-SWE-agent 发出了 133 次参考二进制探测，仅通过 1602/6491 个测试（24.68%），而 NanoHarness 把参考探测总数降到 43 次，并把结果提升到 4425/6491 个测试（68.17%）。对于探测不足，`lfos__calcurse.49180d5` 展示了相反方向的纠正：mini-SWE-agent 在实现前只做了 3 次参考探测，通过 1231/1994 个测试（61.74%），而 NanoHarness 把探索扩展到 45 次参考探测，并把得分提升到 1499/1994 个测试（75.18%）。这些例子说明，NanoHarness 并非简单地统一增加或减少探测；相反，它通过减少智能体卡住时的浪费性探测、并在智能体过早自信时增加行为覆盖，来规训探索。

**对 RQ3.2 的回答：** harness 机制通过规训探测行为来影响失败模式。在 ProgramBench 上，任务专属子智能体等有效组件同时减少过度的低价值探测与不足的浅层验证。通过组合这些组件，NanoHarness 促成更稳定的行为探索，帮助避免浪费性探测与过早实现。

## 6 相关工作

### 6.1 面向软件工程的 LLM 智能体

基于 LLM 的智能体已被广泛研究，用于代码生成 [27][69][18]、仓库级问题求解 [20][61]，以及 ChatDev [36] 与 MetaGPT [15] 等多角色软件开发工作流。其他工作通过规划、检索、调试与工具反馈来改进智能体式编码 [17][28][24]。在修复与问题解决方面，SWE-bench [20] 促成了 SWE-agent [56]、AutoCodeRover [67]、RepairAgent [7] 与 Agentless [53] 等系统，而更新的基准把评测扩展到更广的仓库级任务 [57][31]。

这些研究展示了智能体工作流的价值，但它们通常评测完整系统、基准或任务专属流水线。因此，模型、harness 与任务的效应往往相互纠缠。我们的工作与他们互补：把 harness 设计当作主要研究对象，并度量 harness 及其组件如何跨模型与任务影响 SE 智能体性能。

### 6.2 Agent Harness

近期研究强调，智能体性能不仅取决于基座模型，还取决于周围的 harness 或外部脚手架 [32][35][30][68][25]。ReAct [58]、ToolLLM [37]、Reflexion [41]、Voyager [44] 与 AutoGen [50] 等通用智能体框架表明，工具使用、记忆、规划、反思、技能与多智能体协调能够改进长时程问题求解。

在 SE 领域，harness 必须支持仓库导航、编辑、命令执行、测试与恢复。现有系统引入了诸如智能体–计算机接口（agent-computer interface）[56]、仓库搜索与故障定位 [67][7]，以及定位–修复–验证流水线 [53] 等机制。然而，这些机制通常作为完整智能体的一部分被评测。我们的工作把代表性 harness 组件隔离出来，在受控的模型与任务设置下分析它们的性能、行为与效率效应。

## 7 有效性威胁

**内部威胁。** 主要的内部威胁源于我们对 harness 组件的有限选择：我们研究了五个代表性组件，这可能遗漏其他相关机制。我们计划在未来的工作中把评测扩展到更多组件。第二个威胁来自模型家族的覆盖范围，因为我们只使用了 Qwen 与 DeepSeek。不过，这一点通过覆盖 10 个最具代表性的变体得到缓解，其 prompt 侧 token 总用量超过 10B（Qwen）与 20B（DeepSeek），估计成本超过 7,000 美元。

**外部威胁。** 主要的外部威胁源于我们的数据集选择。我们的主要实验在 ProgramBench 上进行，因此结论可能无法直接推广到其他数据集。尽管如此，ProgramBench 代表了近期一个具有挑战性的仓库级软件生成基准，覆盖从需求理解到制品生成的完整开发生命周期。因此，我们认为 ProgramBench 为评测所研究的 harness 提供了一个有意义且全面的试验台。

## 8 结论

本文把 harness 设计作为基于 LLM 的 SE 智能体的一等因素来研究。跨越三个基准，我们表明 harness 的增益取决于模型能力与任务类型。通过 NanoHarness，我们进一步识别出哪些组件重要：结构化工具与任务专属子智能体改进性能，而上下文压缩与通用子智能体可能有害。我们的轨迹分析表明，有效的 harness 会规训探索与工具使用，说明未来的 SE 智能体设计应同时考虑模型、harness、任务与执行行为。

## 参考文献

- [1] J. Achiam, S. Adler, S. Agarwal, L. Ahmad, I. Akkaya, F. L. Aleman, D. Almeida, J. Altenschmidt, S. Altman, S. Anadkat, et al. (2023). Gpt-4 technical report. arXiv preprint arXiv:2303.08774.
- [2] Anomaly (2026). OpenCode: the open source ai coding agent. https://github.com/anomalyco/opencode
- [3] Anthropic. Claude Code. https://docs.anthropic.com/en/docs/claude-code/overview
- [4] Anthropic (2024). The claude 3 model family: opus, sonnet, haiku. https://www-cdn.anthropic.com/de8ba9b01c9ab7cbabf5c33b80b7bbc618857627/Model_Card_Claude_3.pdf
- [5] Artificial Analysis (2026). Artificial Analysis Coding Index. https://artificialanalysis.ai/models/capabilities/coding
- [6] J. Bai, S. Bai, Y. Chu, Z. Cui, K. Dang, X. Deng, Y. Fan, W. Ge, Y. Han, F. Huang, et al. (2023). Qwen technical report. arXiv preprint arXiv:2309.16609.
- [7] I. Bouzenia, P. Devanbu, and M. Pradel (2025). Repairagent: an autonomous, llm-based agent for program repair. In 2025 IEEE/ACM 47th International Conference on Software Engineering (ICSE), pp. 2188–2200.
- [8] I. Bouzenia and M. Pradel (2024). You name it, i run it: an llm agent to execute tests of arbitrary projects. Proceedings of the ACM on Software Engineering2, pp. 1054 – 1076.
- [9] F. Brand and J. Denain (2025). What skills does swe-bench verified evaluate?.
- [10] S. T. Demirel and R. Das (2018). Software requirement analysis: research challenges and technical approaches. In 2018 6th International Symposium on Digital Forensic and Security (ISDFS), pp. 1–6.
- [11] X. Deng, J. Da, E. Pan, Y. Y. He, C. Ide, K. Garg, N. Lauffer, A. Park, N. Pasari, C. Rane, et al. (2025). Swe-bench pro: can ai agents solve long-horizon software engineering tasks?. arXiv preprint arXiv:2509.16941.
- [12] H. Ding, S. Tao, L. Pang, Z. Wei, J. Gao, B. Ding, H. Shen, and X. Cheng (2025). Toolcoder: a systematic code-empowered tool learning framework for large language models. In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 17876–17891.
- [13] Y. Dong, J. Ding, X. Jiang, G. Li, Z. Li, and Z. Jin (2025). Codescore: evaluating code generation by learning code execution. ACM Transactions on Software Engineering and Methodology34 (3), pp. 1–22.
- [14] L. Fan, J. Liu, Z. Liu, D. Lo, X. Xia, and S. Li (2025). Exploring the capabilities of llms for code-change-related tasks. ACM Transactions on Software Engineering and Methodology34 (6), pp. 1–36.
- [15] S. Hong, M. Zhuge, J. Chen, X. Zheng, Y. Cheng, J. Wang, C. Zhang, S. Yau, Z. Lin, L. Zhou, et al. (2024). MetaGPT: meta programming for a multi-agent collaborative framework. In International Conference on Learning Representations, Vol. 2024, pp. 23247–23275.
- [16] K. Huang, J. Zhang, X. Bao, X. Wang, and Y. Liu (2025). Comprehensive fine-tuning large language models of code for automated program repair. IEEE Transactions on Software Engineering51 (4), pp. 904–928.
- [17] M. A. Islam, M. E. Ali, and M. R. Parvez (2024). Mapcoder: multi-agent code generation for competitive problem solving. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 4912–4944.
- [18] N. Jain, A. Gu, W. Li, F. Yan, T. Zhang, S. Wang, A. Solar-Lezama, K. Sen, and I. Stoica (2025). Livecodebench: holistic and contamination free evaluation of large language models for code. In International Conference on Learning Representations, Vol. 2025, pp. 58791–58831.
- [19] J. Jiang, F. Wang, J. Shen, S. Kim, and S. Kim (2026). A survey on large language models for code generation. ACM Transactions on Software Engineering and Methodology35 (2), pp. 1–72.
- [20] C. E. Jimenez, J. Yang, A. Wettig, S. Yao, K. Pei, O. Press, and K. Narasimhan (2024). Swe-bench: can language models resolve real-world github issues?. In International Conference on Learning Representations, Vol. 2024, pp. 54107–54157.
- [21] Y. Kim, S. Shin, H. Kim, and J. Yoon (2025). Logs in, patches out: automated vulnerability repair via {tree-of-thought}{llm} analysis. In 34th USENIX Security Symposium (USENIX Security 25), pp. 4401–4419.
- [22] F. Li, J. Jiang, J. Sun, and H. Zhang (2025). Hybrid automated program repair by combining large language models and program analysis. ACM Transactions on Software Engineering and Methodology34 (7), pp. 1–28.
- [23] H. Li, Y. Shi, S. Lin, X. Gu, H. Lian, X. Wang, Y. Jia, T. Huang, and Q. Wang (2025). Swe-debate: competitive multi-agent debate for software issue resolution. arXiv preprint arXiv:2507.23348.
- [24] J. Li, G. Li, Y. Zhao, Y. Li, H. Liu, H. Zhu, L. Wang, K. Liu, Z. Fang, L. Wang, et al. (2024). Deveval: a manually-annotated code generation benchmark aligned with real-world code repositories. In Findings of the Association for Computational Linguistics: ACL 2024, pp. 3603–3614.
- [25] J. Lin, S. Liu, C. Pan, L. Lin, S. Dou, Z. Xi, X. Huang, H. Yan, Z. Han, T. Gui, et al. (2026). Agentic harness engineering: observability-driven automatic evolution of coding-agent harnesses. arXiv preprint arXiv:2604.25850.
- [26] A. Liu, B. Feng, B. Xue, B. Wang, B. Wu, C. Lu, C. Zhao, C. Deng, C. Zhang, C. Ruan, et al. (2024). Deepseek-v3 technical report. arXiv preprint arXiv:2412.19437.
- [27] J. Liu, C. S. Xia, Y. Wang, and L. Zhang (2023). Is your code generated by chatgpt really correct? rigorous evaluation of large language models for code generation. Advances in neural information processing systems36, pp. 21558–21572.
- [28] T. Liu, C. Xu, and J. McAuley (2024). Repobench: benchmarking repository-level code auto-completion systems. In International Conference on Learning Representations, Vol. 2024, pp. 47832–47850.
- [29] A. Lops, F. Narducci, A. Ragone, M. Trizio, and C. Bartolini (2025). A system for automated unit test generation using large language models and assessment of generated test suites. In 2025 IEEE International Conference on Software Testing, Verification and Validation Workshops (ICSTW), pp. 29–36.
- [30] Q. Meng, Y. Wang, L. Chen, Q. Wang, C. Lu, W. Wu, Y. Gao, Y. Wu, and Y. Hu (2026). Agent harness for large language model agents: a survey.
- [31] Z. Ni, H. Wang, S. Zhang, S. Lu, Z. He, Z. Tang, S. Hu, B. Li, C. Hu, B. Jiao, et al. (2026). Gittaskbench: a benchmark for code agents solving real-world tasks through code repository leveraging. In Proceedings of the AAAI Conference on Artificial Intelligence, Vol. 40, pp. 32564–32572.
- [32] X. Ning, K. Tieu, D. Fu, T. Wei, Z. Li, Y. Bei, J. Zou, M. Ai, Z. Liu, T. Li, et al. (2026). Code as agent harness. arXiv preprint arXiv:2605.18747.
- [33] OpenAI. Codex: AI Coding Partner from OpenAI. https://openai.com/codex/
- [34] S. Ouyang, W. Yu, K. Ma, Z. Xiao, Z. Zhang, M. Jia, J. Han, H. Zhang, and D. Yu (2025). Repograph: enhancing ai software engineering with repository-level code graph. In International Conference on Learning Representations, Vol. 2025, pp. 30098–30121.
- [35] L. Pan, L. Zou, S. Guo, J. Ni, and H. Zheng (2026). Natural-language agent harnesses. arXiv preprint arXiv:2603.25723.
- [36] C. Qian, W. Liu, H. Liu, N. Chen, Y. Dang, J. Li, C. Yang, W. Chen, Y. Su, X. Cong, et al. (2024). Chatdev: communicative agents for software development. In Proceedings of the 62nd annual meeting of the association for computational linguistics (volume 1: Long papers), pp. 15174–15186.
- [37] Y. Qin, S. Liang, Y. Ye, K. Zhu, L. Yan, Y. Lu, Y. Lin, X. Cong, X. Tang, B. Qian, et al. (2024). Toolllm: facilitating large language models to master 16000+ real-world apis. In International Conference on Learning Representations, Vol. 2024, pp. 9695–9717.
- [38] W. I. Shafin, M. N. Rafi, Z. Li, and T. Chen (2025). Evaluating software process models for multi-agent class-level code generation. ArXivabs/2511.09794.
- [39] Y. Shang, Q. Zhang, C. Fang, S. Gu, J. Zhou, and Z. Chen (2024). A large-scale empirical study on fine-tuning large language models for unit testing. Proceedings of the ACM on Software Engineering2, pp. 1678 – 1700.
- [40] M. Shao, Y. Ding, C. Gao, J. Wang, and G. Zhu (2026). Fix pattern-aware vulnerability patch generation via in-context learning. ACM Transactions on Software Engineering and Methodology.
- [41] N. Shinn, F. Cassano, A. Gopinath, K. Narasimhan, and S. Yao (2023). Reflexion: language agents with verbal reinforcement learning. Advances in neural information processing systems36, pp. 8634–8652.
- [42] A. Singh, A. Fry, A. Perelman, A. Tart, A. Ganesh, A. El-Kishky, A. McLaughlin, A. Low, A. Ostrow, A. Ananthram, et al. (2025). Openai gpt-5 system card. arXiv preprint arXiv:2601.03267.
- [43] G. Team, R. Anil, S. Borgeaud, J. Alayrac, J. Yu, R. Soricut, J. Schalkwyk, A. M. Dai, A. Hauth, K. Millican, et al. (2023). Gemini: a family of highly capable multimodal models. arXiv preprint arXiv:2312.11805.
- [44] G. Wang, Y. Xie, Y. Jiang, A. Mandlekar, C. Xiao, Y. Zhu, L. Fan, and A. Anandkumar (2023). Voyager: an open-ended embodied agent with large language models. arXiv preprint arXiv:2305.16291.
- [45] H. Wang, Z. Hou, Y. Wei, J. Tang, and Y. Dong (2025). Swe-dev: building software engineering agents with training and inference scaling. In Findings of the Association for Computational Linguistics: ACL 2025, pp. 3742–3761.
- [46] J. Wang, X. Xie, Q. Hu, S. Liu, J. Yu, J. Klong, and Y. Li (2025). Defects4C: benchmarking large language model repair capability with c/c++ bugs. 2025 40th IEEE/ACM International Conference on Automated Software Engineering (ASE), pp. 254–265.
- [47] W. Wang, C. Yang, Z. Wang, Y. Huang, Z. Chu, D. Song, L. Zhang, A. R. Chen, and L. Ma (2025). Testeval: benchmarking large language models for test case generation. In Findings of the Association for Computational Linguistics: NAACL 2025, pp. 3547–3562.
- [48] X. Wang, P. Gao, X. Meng, C. Peng, R. Hu, Y. Lin, and C. Gao (2025). Aegis: an agent-based framework for bug reproduction from issue descriptions. In Proceedings of the 33rd ACM International Conference on the Foundations of Software Engineering, pp. 331–342.
- [49] X. Wang, P. Gao, X. Meng, C. Peng, R. Hu, Y. Lin, and C. Gao (2025). AEGIS: an agent-based framework for bug reproduction from issue descriptions. Proceedings of the 33rd ACM International Conference on the Foundations of Software Engineering.
- [50] Q. Wu, G. Bansal, J. Zhang, Y. Wu, B. Li, E. Zhu, L. Jiang, X. Zhang, S. Zhang, J. Liu, et al. (2024). Autogen: enabling next-gen llm applications via multi-agent conversations. In First conference on language modeling,
- [51] Z. Xi, Y. Ding, W. Chen, B. Hong, H. Guo, J. Wang, X. Guo, D. Yang, C. Liao, W. He, et al. (2025). Agentgym: evaluating and training large language model-based agents across diverse environments. In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 27914–27961.
- [52] C. Xia, Y. Deng, S. Dunn, and L. Zhang (2024). Agentless: demystifying llm-based software engineering agents. ArXivabs/2407.01489.
- [53] C. S. Xia, Y. Deng, S. Dunn, and L. Zhang (2024). Agentless: demystifying llm-based software engineering agents. arXiv preprint arXiv:2407.01489.
- [54] A. Yang, A. Li, B. Yang, B. Zhang, B. Hui, B. Zheng, B. Yu, C. Gao, C. Huang, C. Lv, et al. (2025). Qwen3 technical report. arXiv preprint arXiv:2505.09388.
- [55] B. Yang, H. Tian, J. Ren, H. Zhang, J. Klein, T. F. Bissyandé, C. L. Goues, and S. Jin (2024). MORepair: teaching llms to repair code via multi-objective fine-tuning. ACM Transactions on Software Engineering and Methodology35, pp. 1 – 38.
- [56] J. Yang, C. Jimenez, A. Wettig, K. Lieret, S. Yao, K. Narasimhan, and O. Press (2024). Swe-agent: agent-computer interfaces enable automated software engineering. Advances in Neural Information Processing Systems37, pp. 50528–50652.
- [57] J. Yang, K. Lieret, J. Ma, P. Thakkar, D. Pedchenko, S. Sootla, E. McMilin, P. Yin, R. Hou, G. Synnaeve, et al. (2026). ProgramBench: can language models rebuild programs from scratch?. arXiv preprint arXiv:2605.03546.
- [58] S. Yao, J. Zhao, D. Yu, N. Du, I. Shafran, K. Narasimhan, and Y. Cao (2022). React: synergizing reasoning and acting in language models. arXiv preprint arXiv:2210.03629.
- [59] L. Yu, Z. Huang, H. Yuan, S. Cheng, L. Yang, F. Zhang, C. Shen, J. Ma, J. Zhang, J. Lu, and C. Zuo (2025). Smart-llama-dpo: reinforced large language model for explainable smart contract vulnerability detection. Proceedings of the ACM on Software Engineering2, pp. 182 – 205.
- [60] Z. Yu, Z. Guo, Y. Wu, J. Yu, M. Xu, D. Mu, Y. Chen, and X. Xing (2025). {patchagent}: A practical program repair agent mimicking human expertise. In 34th USENIX Security Symposium (USENIX Security 25), pp. 4381–4400.
- [61] D. Zan, Z. Huang, W. Liu, H. Chen, S. Xin, L. Zhang, Q. Liu, L. Aoyan, L. Chen, X. Zhong, et al. (2026). Multi-swe-bench: a multilingual benchmark for issue resolving. Advances in Neural Information Processing Systems38.
- [62] F. Zhang, B. Chen, Y. Zhang, J. Keung, J. Liu, D. Zan, Y. Mao, J. Lou, and W. Chen (2023). Repocoder: repository-level code completion through iterative retrieval and generation. In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, pp. 2471–2484.
- [63] K. Zhang, J. Li, G. Li, X. Shi, and Z. Jin (2024). Codeagent: enhancing code generation with tool-integrated agent systems for real-world repo-level coding challenges. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 13643–13658.
- [64] Q. Zhang, C. Gao, Y. Han, Y. Shang, C. Fang, Z. Chen, and L. Xiao (2026). SGAgent: suggestion-guided llm-based multi-agent framework for repository-level software repair. ArXivabs/2602.23647.
- [65] Q. Zhang, Y. Shang, H. Hu, C. Fang, Z. Chen, and L. Xiao (2026). ComPass: contrastive learning for automated patch correctness assessment in program repair. Empirical Software Engineering31 (6), pp. 157.
- [66] Y. Zhang, R. Li, P. Liang, W. Sun, and Y. Liu (2025). Knowledge-based multi-agent framework for automated software architecture design. In Proceedings of the 33rd ACM International Conference on the Foundations of Software Engineering, pp. 530–534.
- [67] Y. Zhang, H. Ruan, Z. Fan, and A. Roychoudhury (2024). Autocoderover: autonomous program improvement. In Proceedings of the 33rd ACM SIGSOFT International Symposium on Software Testing and Analysis, pp. 1592–1604.
- [68] C. Zhou, H. Chai, W. Chen, Z. Guo, R. Shan, Y. Song, T. Xu, Y. Yang, A. Yu, W. Zhang, et al. (2026). Externalization in llm agents: a unified review of memory, skills, protocols and harness engineering. arXiv preprint arXiv:2604.08224.
- [69] T. Y. Zhuo, M. C. Vu, J. Chim, H. Hu, W. Yu, R. Widyasari, I. N. B. Yusuf, H. Zhan, J. He, I. Paul, et al. (2025). Bigcodebench: benchmarking code generation with diverse function calls and complex instructions. In International Conference on Learning Representations, Vol. 2025, pp. 66602–66656.
