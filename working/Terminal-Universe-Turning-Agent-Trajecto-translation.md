---
created: 2026-10-03
updated: 2026-10-03
title: Terminal-Universe：把智能体轨迹转化为可扩展的终端环境
sourceUrl: http://arxiv.org/abs/2609.04148v1
sourceAuthor: Jie Wu、Zhenru Zhang、Beichen Zhang 等（Qwen Team, Alibaba Group / 清华大学）
translatedAt: 2026-10-03
sources: [references/articles.md 待处理队列]
tags: [Agent 轨迹, 终端环境, 环境重建, 任务合成, 跨工作区, 多轮交互, SFT, Qwen, 代码智能体, type/翻译]
---

# Terminal-Universe：把智能体轨迹转化为可扩展的终端环境

> [arxiv.org/abs](http://arxiv.org/abs/2609.04148v1)｜分类：cs.AI（人工智能）/ cs.CL
> 作者：Jie Wu、Zhenru Zhang、Beichen Zhang、Xuwu Wang、Yuhui Su、Mouxiang Chen、Peng Wang、Zhihai Wang、Que Shen、Hao Zhou、An Yang、Fei Huang、Yujiu Yang、Dayiheng Liu（Qwen Team, Alibaba Group 与清华大学；Zhenru Zhang 为项目负责人，Yujiu Yang、Dayiheng Liu 为通讯作者）
> 提交：2026-09-03（arXiv v1）｜许可：arXiv.org perpetual non-exclusive license
> 原文：http://arxiv.org/abs/2609.04148v1｜DOI：https://doi.org/10.48550/arXiv.2609.04148

## 摘要

随着基于终端的代码智能体（terminal-based code agents）日益普及，相应的智能体轨迹（agent trajectories）已大规模积累，而真实、可执行的环境却依然稀缺。然而，环境恰恰是智能体后训练（post-training）真正需要的：每个环境都可以被反复查询成许多可验证的任务，并提供执行反馈；而一条轨迹只是一份冻结的单次示范。与其从零开始生成环境，我们观察到：现有轨迹中的工具执行历史暴露了它所运行环境的结构与内容，因此可以从轨迹本身重建那些环境。于是，我们提出 **Terminal-Universe**，一个把每条轨迹转化为可复用环境、并对其探索以合成新任务与持续交互的框架。具体而言，Terminal-Universe 重放轨迹中记录的文件操作，把每个文件还原到智能体修改它之前的状态，得到一个部分工作区（partial workspace）；随后由一个补全智能体（completion agent）补齐缺失的文件与依赖。在这个恢复出的工作区上，我们既重建原始意图任务，也合成全新的任务。此外，我们还沿两条互补的轴扩展任务：广度与深度。在广度上，我们挖掘相关环境之间的有向依赖关系，合成横跨多个代码库（codebase）的跨工作区查询，正如开发者在真实开发中经常做的那样。在深度上，我们借助一个用户智能体（user agent）把初始的单轮查询扩展为多轮会话，以捕获迭代式的用户反馈与需求精化。应用于公开的终端智能体轨迹后，Terminal-Universe 产出 **37.3k** 个任务充分（task-sufficient）的环境。在该语料上对 Qwen3.5-27B 进行监督微调（SFT），使 Terminal-Bench 2.1 的单轮成绩提升 **11.9** 分，使 EvoCode-Bench v2 的多轮 MT@4 成绩提升 **13.8** 分。

## 1 引言

随着基于终端的代码智能体日益普及，它们产生的轨迹已大规模积累，而真实、可执行的环境却依然稀缺。这个缺口之所以重要，是因为轨迹与环境的价值并不对等。一条轨迹是一份单一的、固定的记录：它的质量受限于产生它的策略模型的响应，而且我们无法检验它对代码库所做的改动是否真的正确。环境则没有这些限制，因为同一个任务可以被更强的模型重新求解，结果可以被我们自己的测试验证，更难的题目也可以被放在同一个工作区上。因此对于后训练来说，环境才是值得扩展的资源。

专家编写（expert-authored）的基准展示了好的环境长什么样。例如，Terminal-Bench（Merrill et al., 2026）为每个任务都配了一个自定义容器、一条指令和一个可执行验证器（verifier）。这种可靠性来自人工投入，而人工投入同样限制了能构建多少任务；有效的后训练所需的环境数量远超人工策划所能提供。因此，在训练规模上提供真实、可验证的环境，正是我们要解决的挑战。

现有工作以三种方式扩展可执行环境。基于仓库（repository-based）的方法从真实仓库的 git 历史构建任务（Pan et al., 2024；Jain et al., 2025）：对于过去被修复过的某个 bug，他们用 git 把仓库回滚到修复前的状态以构成环境，把原始 bug 报告作为任务，并复用随修复一起到来的测试来检验解答。扰动（perturbation）方法取一个能通过测试的仓库，注入一个 bug 使某些测试失败，然后要求智能体修复它（Yang et al., 2025；Lin et al., 2026）。少数仓库可以由此产生许多任务，但每个任务都是修复类任务，任务范围受源仓库和可注入 bug 类型的限制。任务条件合成（task-conditioned synthesis）则根据类别或组合轴（Gandhi et al., 2026；Ivison et al., 2026）、技能分类（Hua et al., 2026）或技能图（Fan et al., 2026）从零开始同时生成任务及其环境。这些方法对覆盖面和任务—环境对齐提供了控制，但环境并不与任何真实项目绑定，因此其真实性完全取决于生成器，而生成器往往产出小而整洁的工作区，而非真实代码。

在这些路线中，环境构建要么从一个既有环境出发，要么与一个从零新生成的任务相耦合。而轨迹作为对其所运行环境的观测，却大体上仍未作为资源被充分探索。一条轨迹内部记录的工具调用，已经暴露了它所运行环境的内容与结构。例如，工具 Read 展示文件内容，Write 和 Edit 展示工作区如何变化。这已足以重建原始工作区的一份可执行副本。因此，我们提出 Terminal-Universe（图 1），一个把每条轨迹转化为可复用环境、并对其探索以合成新任务与持续交互的框架。

图 1：Terminal-Universe 总览。轨迹与环境是同一段情节的两个视图，因此既有工作是从环境 rollout 出轨迹，而我们反转这一映射、从轨迹恢复环境（左）。重建分两阶段进行：确定性重放（deterministic replay）之后是智能体补全（agentic completion）（中）。每个恢复出的环境随后会被重查询（re-query）：在单个工作区内、跨多个相互依赖的工作区、或跨多轮用户交互（右）。图 2 详述了每种机制。

具体而言，为基于轨迹构建环境（§3.1），我们首先重放记录的文件操作，把每个文件恢复到智能体改动它之前的状态，并搁置智能体自身的改动、让工作区以未求解（unsolved）的状态开始，从而得到一个部分工作区。随后，智能体补全补齐缺失的项目上下文。每个恢复出的环境都被重查询成新的任务与交互，其规模沿广度与深度两轴扩展（§3.2）。广度扩展超越了大多数任务合成所假设的单仓库设定。我们识别相关环境之间的依赖关系，构建横跨多个代码库的跨工作区任务——它们要难得多，例如阅读一份参考实现、把一个功能从一个项目迁移到另一个项目，或连接两个组件。深度扩展把单轮任务变成多轮任务。在智能体完成一个初始查询后，一个用户智能体随着工作区演变提出有据可依的追问——用新需求扩展它，或者在某一轮失败时，基于出错的地方要求修复。我们验证每一轮，并把结果作为自然的、用户可见的反馈回传给智能体。每条新任务都配有一个由容器内智能体编写的验证器，我们只保留那些测试全部通过的轨迹（§4）。

在公开可用的终端智能体轨迹上，这条流水线产出 37.3k 个任务充分的环境。在这些环境之上，我们生成新的查询，并用 Qwen3.7-Max 作为教师（teacher）为每个任务 rollout 出一条解答轨迹。在所得数据上训练 Qwen3.5-27B，验证了本方法的有效性：它把单轮基准 Terminal-Bench 2.1 提升 11.9 分，把多轮基准 EvoCode-Bench v2 MT@4 提升 13.8 分（§5）。大量消融实验证实每个组件都有贡献，其中最值得注意的是：在重建环境中重解任务，远优于模仿原始轨迹。

综上，我们做出以下贡献：

- **环境重建。** 我们把记录下来的智能体轨迹重新诠释为可复用可执行环境的来源，并通过"确定性重放 + 智能体补全"重建每个环境——既不需要原始仓库，也不必从零构建。
- **重查询方法。** 我们通过新任务生成来放大每个重建环境的效用。除了朴素的单工作区、单轮任务外，我们贡献了经由跨工作区任务合成的广度扩展，以及经由多轮用户查询的深度扩展。每条任务都配有一个由智能体编写的验证器，且只保留通过的轨迹。
- **实证验证。** 在所得语料上微调 Qwen3.5-27B，相比同一基座模型把 Terminal-Bench 2.1 提升 11.9 分、把 EvoCode-Bench v2 MT@4 提升 13.8 分。消融实验证实每个组件都有贡献，尤其是：在重建环境中重解任务，远优于模仿原始轨迹。

表 1：代表性环境与训练数据构建方法的对比。Strategy 概述构建环境或训练任务所用的主要机制；Env. 统计可复用的源仓库/工作区或独立构建的环境数；Tasks 给出报告的任务数或训练实例数；Verif. 表示可执行的任务验证器；Multi-Round 表示扩展的多轮查询；Cross-WS 表示跨工作区合成。

| 方法 | 策略 | 环境数 | 任务数 | 验证器 | 多轮 | 跨工作区 |
| --- | --- | --- | --- | --- | --- | --- |
| Endless Term.（Gandhi et al., 2026） | 任务条件 | 3,255 | 3,255 | ✓ | ✗ | ✗ |
| TMax（Ivison et al., 2026） | 组合采样 | 14.6k | 14.6k | ✓ | ✗ | ✗ |
| CLI-Gym（Lin et al., 2026） | 环境扰动 | 29 | 1,655 | ✓ | ✗ | ✗ |
| CLI-Universe（Hua et al., 2026） | 分类引导 | 6k | 6k | ✓ | ✗ | ✗ |
| SkillSynth（Fan et al., 2026） | 技能图引导 | 3,560 | 3,560 | ✓ | ✗ | ✗ |
| OpenThinker-Agent（Raoof et al., 2026） | 多源策展 | – | 100k | ✓ | ✗ | ✗ |
| RST（Li et al., 2026b） | 递归演化 | 37.5k | 37.5k | ✓ | ✗ | ✗ |
| CalibForge（Meng et al., 2026） | 对抗校准 | 5,431 | 5,431 | ✓ | ✗ | ✗ |
| **Terminal-Universe（本文）** | **轨迹重建** | **37.3k** | **32.0k** | ✓ | ✓ | ✓ |

## 2 相关工作

**终端智能体的环境扩容。** 现有方法通过三条主要路线来扩展可执行工作区：从真实开发历史中恢复仓库状态、修改可用的工作区、或从生成的规格构建任务专用环境。SWE-Gym（Pan et al., 2024）与 R2E-Gym（Jain et al., 2025）从与历史 issue 或 commit 相关联的仓库版本构建环境。SWE-smith（Yang et al., 2025）与 CLI-Gym（Lin et al., 2026）从可用仓库或 CLI 工作区出发，向其中引入 bug 或故障。SETA（Shen et al., 2026b）则通过合成与自适应环境演化，为强化学习扩展可验证的终端环境。另有一类工作联合生成终端任务及其容器化执行环境，我们在下文讨论它们的任务构建策略。Terminal-Universe 则以记录下来的智能体轨迹为起点：它重放每条轨迹中记录的文件操作，并用智能体补全恢复缺失的项目上下文，产出可复用的可执行工作区。

**终端任务合成。** 现有方法要么从抽象先验、要么从具体可执行环境推导任务。自顶向下的流水线从类别或种子生成任务—环境对（Gandhi et al., 2026；Pi et al., 2026；Zhu et al., 2026），而更结构化的变体围绕能力分类法、组合轴或技能图组织生成（Hua et al., 2026；Ivison et al., 2026；Fan et al., 2026）。另有方法利用智能体技能、可执行元任务或求解器反馈来多样化并校准生成的任务（Cheng et al., 2026；Pan et al., 2026；Meng et al., 2026）。

**环境接地（environment-grounded）** 的方法则从可运行的代码与项目上下文推导任务。它们扰动健康环境、挖掘仓库文档、把任务接地到真实 issue，或在共享环境中联合实现指令、解答与验证器（Lin et al., 2026；Wu et al., 2026a；Yang et al., 2026；Shi et al., 2026）。RST 通过加长解答、重新对齐任务/验证器/环境来递归扩展已验证的种子（Li et al., 2026b）。Terminal-Universe 以过往智能体轨迹为起点：它先重建轨迹的工作区，再在这些工作区内部或之间生成新任务。

**交互式与多轮智能体。** 超越孤立的单轮提示，近期基准把智能体交互建模为动态的多轮对话。InterCode 通过容器化 shell 中的执行反馈形式化交互式编码（Yang et al., 2023）。SWE-INTERACT（Raghavendra et al., 2026）用模拟用户逐步揭示需求并提供有针对性的修改，而 SWE-Together（Wu et al., 2026b）通过一个状态条件用户模拟器重放真实的用户—智能体会话，在被评测智能体推进的过程中提供反馈。ICAE-Bench（Peng et al., 2026b）用自动化用户智能体评估从不完整产品需求出发的交互式项目构建。在持久工作区中，EvoCode-Bench v2（Shen et al., 2026a）跨一系列连续开发请求评估智能体。Terminal-Universe 通过深度扩展拥抱这一交互设定，把重建的工作区扩展成捕获迭代用户反馈与需求精化的多轮会话。

表 1 把 Terminal-Universe 与代表性方法做了对比。与既有工作不同，它从记录的轨迹构建其环境，并沿广度（跨工作区合成）与深度（多轮查询）两轴扩展任务。

## 3 Terminal-Universe

图 2 详述了跨环境重建、四种重查询变体与验证的各项机制。以下各小节分别描述环境重建（§3.1）、重查询（§3.2）与验证（§3.3）。

### 3.1 环境重建

依据轨迹 τ 中记录的文件与命令操作，我们恢复出一个可执行工作区 Ê，用以近似 τ 被产生时的环境 E。这种恢复本质上是有损的，因为未被访问的文件、隐式的系统依赖以及外部网络资源都没有留下直接痕迹。因此我们分三阶段重建：确定性重放恢复 τ 直接暴露的文件状态，智能体补全提供它省略的潜在上下文，环境过滤则只保留对其恢复任务 q 而言充分的工作区。

**阶段 1：确定性重放。** 重放按时间顺序处理 τ 中的 read、write、edit 操作，为每个被访问的路径恢复轨迹中可见的最早与最新文件内容。重建出的初始工作区 E₀ 收集每个既有文件在其最早被观测到的版本——即智能体第一次改动它之前；由智能体创建的文件被排除在外，智能体的文件改动被单独记录下来以供后续验证。由于轨迹只暴露智能体触碰过的路径，且当轨迹只展示文件的一部分或终端输出被截断时文件内容可能不完整，E₀ 仍然只是一个部分工作区。

**阶段 2：智能体补全。** 给定部分工作区 E₀ 与恢复出的任务 q，一个补全智能体创建缺失的文件、补全不完整的文件，并恢复使 q 可解所需的依赖——但不能把 q 实现出来。我们把所得补全工作区记为 Ê。我们对所有重放出的工作区都应用这一阶段，其对工作区复杂度的影响在 §4 中详述。

图 2：Terminal-Universe 框架。一条记录的轨迹被重放并补全为一个可执行工作区，只有当它对自身任务充分时才会被保留（左）。恢复出的工作区支撑四种重查询：Intent Recovery（意图恢复）、在单个工作区上探索并提出新任务候选的 Single-WS 合成、经由工作区画像与关系挖掘的 Cross-WS 合成，以及把初始查询扩展为迭代会话的 Multi-Round 延续。

**阶段 3：环境过滤。** 一个补全后的工作区，只有当它暴露出足够的项目上下文来支撑其任务时才有用。一个智能体裁判（agentic judge）用只读的 shell 与文件工具检查每个 Ê，并以恢复出的任务 q 为条件，根据其源代码、配置、数据与结构是否为一名有能力的智能体提供了足够的工作上下文，把该工作区标为充分或不充分（§B.3）。只有充分的工作区才会被保留下来用于下游任务生成；各阶段充分率与最终计数在 §4 中报告。

每个重建出的工作区都运行在一个标准化、可联网的 `ubuntu:24.04` 容器中。与仓库专用镜像相比，这一设计降低了成本、简化了部署，代价是按既有工作报告，求解率（resolve rate）会有适度下降（Zeng et al., 2026）。

### 3.2 重查询

重建产出可执行环境，而重查询则决定这些环境潜在能力空间被利用得有多充分。我们引入四种互补的重查询机制，全篇称为 Intent Recovery、Single-WS、Cross-WS 与 Multi-Round。Intent Recovery 重建源任务，Single-WS 在单个工作区内合成新任务，Cross-WS 通过连接相关工作区提供广度，Multi-Round 通过把初始查询扩展为交互式会话来提供深度。

**意图恢复（Intent Recovery）。** 把一条或多条源用户请求归并为一条自足任务。

我们把每条源轨迹规范化为用户请求、智能体动作与文件改动按时间排列的流。对于单轮轨迹，唯一的实质性用户请求直接定义了任务。对于多轮轨迹，第一个实质性用户请求确立任务主题，后续请求在澄清、约束或扩展同一任务时被并入；无关的任务转向被排除。我们用智能体动作与文件证据来解释请求，但只保留用户明确陈述的需求（§C.1）。

**单工作区合成（Single-workspace synthesis）。** 从单个重建工作区推导新查询。

一个离线生成器检查每个工作区，在接地性（groundedness）、结构多样性与可验证性约束下合成 5 条自足候选任务。我们为每个环境随机选择 1 条有效候选用于 rollout 与验证。

**广度扩展。** 在单条查询中连接相关工作区。

**跨工作区合成（Cross-workspace synthesis）。** 为合成横跨多个代码库的任务，我们跨恢复环境发现**有向**依赖关系。一个智能体首先为每个工作区做技术领域与已实现能力的画像。随后我们通过 TF-IDF 最近邻检索召回候选对，并用一个 LLM 裁判识别有向依赖边——即目标工作区缺失了某个已在参考工作区中实现的能力。

我们为每个配对恰好分配一个任务。每个跨工作区任务把一个可写的目标工作区与一个只读的参考工作区配对，后者挂载在另一独立路径上。任务生成器确认这一功能缺口真实存在，并指定目标中可观测的行为来弥合该缺口，且这些行为可通过确定性的本地命令验证。查询只提供这些目标行为与参考工作区的挂载路径，而不提供其内部细节，从而让参考工作区成为一项真实的依赖。因此求解者必须自行导航、内化并适配该参考实现。

**深度扩展。** 通过用户智能体的追问，把已解决的终端任务加以扩展。

**多轮用户查询（Multi-round user queries）。** 从一条初始终端查询开始，我们跨多轮编码保留工作区，并在初始响应之后引入一个用户智能体。延续过程采用两个协同机制来确保多轮轨迹连贯而真实：

1. **演化的任务规格。** 用户智能体维护一个显式的需求追踪器，记录 active、satisfied 与 updated 的需求。在每次追问之前，它通过新增、修改或替换约束来更新该追踪器，随着工作区演变保持上下文的连贯。
2. **轮级验证与反馈。** 在每一轮扩展中，用户智能体提交更新后的规格，促使一个自动验证器在编码智能体行动之前编写轮级验收测试。收到智能体的响应后，测试运行器同时评估新标准与仍在生效的回归检查。求解智能体与测试脚本及 traceback 严格隔离；用户智能体解释结构化的测试结果，并把任何失败转化为自然的、用户可观察的抱怨。中间失败被保留在对话历史中，为错误诊断与恢复提供真实的监督。

图 3：多轮会话中的通过/失败模式。

跨各轮，用户智能体的请求分为三种交互风格：(i) **功能扩展（feature extension）**，在某轮验证成功后引入新的有据可依的需求；(ii) **功能修订（feature revision）**，由测试失败触发，要求基于观测到的行为修复 bug；(iii) **功能冲突（feature conflict）**，修改或覆盖先前的规格以反映变化的用户意图。每种请求的风格自然地由该轮结果与会话上下文决定，其分布按观测结果报告（§E.3、表 17）。会话最多持续 6 轮追问，或直到发出终止哨兵。

图 3 报告了 §3.3 轮级筛选之后延续数据的通过/失败模式：保留的 3,079 条记录平均 4.51 轮，其中 69.6% 包含一次会话随后修复的失败，从而保留了恢复（recovery）监督。

### 3.3 验证与过滤

**智能体验证器构建。** 每条 Single-WS 或 Cross-WS 任务都配有一个可执行验证器，由一名专门的智能体在目标容器内编写。验证器智能体以任务规格与工作区文件为条件，通过迭代式本地执行打磨出一套自足的 pytest 测试套件，严格评估提示词中规定的公开接口与预期行为（附录 D）。

**解答 rollout。** 候选解答在任务容器内使用教师模型[^teacher]在 Claude Code 脚手架（Anthropic, 2026）中 rollout。rollout 以温度 1.0、top-p=0.95 解码，在 256k token 的上下文窗口上交错思考（interleaved thinking），单轮响应上限为 65,536 token，在 176k token 时触发主动摘要，最多 500 个智能体轮次，墙钟超时 4 小时。任务环境提供容器化网络访问以下载缺失依赖（§3.1）。

[^teacher]: 本工作中所有由模型驱动的组件都以 Qwen3.7-Max（xhigh effort）作为教师模型。

**验证与数据选择。** 对 Single-WS 与 Cross-WS，编写好的测试套件在 rollout 结束后的最终工作区状态上运行，只有当所有测试通过时轨迹才被接收。Multi-Round 则在轮级筛选：我们从终止的会话中裁掉连续失败轮次的尾部后缀，只保留至少包含两个已验证通过轮的会话。在成功恢复之前的中间失败被保留，为错误诊断与恢复提供监督。被接收的轨迹被格式化为多轮 SFT 示范，并针对评测基准进行严格去污染（§5）。

## 4 规模化数据构建

### 4.1 种子选择

我们从多样化的终端式 CLI 与软件工程语料中采集原始智能体轨迹。如果一条执行轨迹在末尾观测到的工作区状态包含至少 5 个文件与 100 行，它就作为可用种子被保留。为防止数据泄漏，我们严格过滤掉所有源自 Terminal-Bench 的语料。完整的来源分解与选择统计详见附录 A。

### 4.2 重建统计

从源轨迹池出发，重建流水线产出 **68,263** 个重建环境。如图 4 所示，重放出的终端工作区初始只含很少文件，因为原始 rollout 期间生成的解答文件被搁置在外。智能体补全显著丰富了这些环境，把平均文件数从 **2.9** 提升到 **22.4**。虽然 SWE 种子起始于更丰富的仓库状态，补全同样扩展了它们的上下文广度（完整复杂度分布见表 13）。

图 4：智能体补全前后的平均工作区大小。

在污染过滤与仓库级去重之后，我们对存活的、已补全的环境应用阶段 3 的充分性裁判（§3.1）。

表 2：恢复意图下的工作区充分性。

| 池 | 环境数 | 充分率（%）重放后 | 充分率（%）补全后 |
| --- | --- | --- | --- |
| Terminal | 38,294 | 40.2 | 93.5 |
| SWE | 1,900 | 20.1 | 77.1 |

如表 2 所示，仅确定性重放对 Terminal 工作区产生的充分率为 40.2%、对 SWE 工作区为 20.1%。智能体补全显著提升覆盖率，分别达到 93.5% 与 77.1%——这是在仓库级去重之后，对 38,294 个被评估的终端环境与 1,900 个 SWE 仓库（每个仅取一份代表性重建）统计的。总体上，任务接地的评估识别出 **37,273** 个完全充分、适合下游任务生成的环境（附录 A）。

图 5 展示了重建终端池的多样性：Python 是占主导的主要语言（84.7%），此外还有 C++ 与 C；数据处理、DevOps 与安全类工作负载合计占技术领域的 80% 以上。

图 5：重建终端工作区的语言与领域组成。

### 4.3 SFT 语料组成

这些任务充分的环境构成我们四种重查询变体的基础：Intent Recovery 重建原始任务，Single-WS 产出仓库内的新任务，Cross-WS 发现跨仓库的依赖挑战，Multi-Round 把初始查询扩展为迭代会话。在终端池上，经验证器过滤的 Single-WS、Cross-WS 与 Multi-Round 合成产出 **31,977** 条 SFT 示范（25,386 条 Single-WS、3,512 条 Cross-WS、3,079 条 Multi-Round 轨迹），合计约 **1.42B** 训练 token。中位交互统计见附录 F。

## 5 实验

### 5.1 设置

**训练。** 我们在 Terminal-Universe 数据上以 SFT 微调 Qwen3.5-27B，训练 2 个 epoch。我们使用恒定的学习率 7×10⁻⁶、全局批大小 256、序列长度 256k token。训练前，我们针对 Terminal-Bench 任务运行 13-gram 污染检查，并从四种重查询变体中排除源自 Terminal-Bench 的源数据集。

**单轮评测（Terminal-Bench 2.0 与 2.1）。** 我们用 Claude Code（版本 2.1.126）与 Terminus2（Merrill et al., 2026）并在 XML 解析器下评测 Terminal-Bench。评测沿用解答 rollout 的解码与执行配置（§3.3）：温度 1.0、top-p=0.95、交错思考、256k 上下文窗口、65,536 token 单轮上限、176k token 触发主动摘要、最多 500 个智能体轮次、4 小时墙钟超时。对于 Claude Code，交互式与网络检索工具（WebFetch、WebSearch、AskUserQuestion、EnterPlanMode、ExitPlanMode）被禁用。每个容器以 12 个 CPU 核与 32 GiB 内存运行。报告分数为 6 次独立运行的平均通过率。Terminal-Bench 2.0 与 2.1 的差异记录在该基准的更新中（https://github.com/harbor-framework/terminal-bench-2/pull/53）。

**多轮评测（EvoCode-Bench v2）。** 我们在 EvoCode-Bench v2（https://unipat.ai/benchmarks/EvoCode-Bench；Shen et al., 2026a）上评测深度扩展，它包含 26 个编码任务与 227 轮（每个任务 5–15 条请求）。工作区与会话持续存在，累积验证器同时检查当前需求与仍在生效的先前需求。我们的 Qwen3.5-27B checkpoint 使用 Terminus2-XML、温度 1.0、交错思考、256k token 上下文、每轮上限 65,536 token、176k token 触发主动摘要、每个请求轮最多 500 个智能体轮次、每个有状态任务总墙钟上限 10 小时。每个任务在 4 次独立运行中评测。MT@4 使用 fail-stop 计分：一次运行只在其首次失败之前连续通过的轮次上得分，而某个任务—轮只要有任何一次运行成功到达就计分。分数先在每个任务内对得分轮次取平均，再跨任务取平均。Case score 先在任务内对验证器用例通过率取平均，再跨任务与运行取平均，以衡量部分进展。

### 5.2 主要结果

表 3 报告单轮与多轮性能。在 Full Mixture（经验证器过滤的 Single-WS、Cross-WS 与 Multi-Round 轨迹，32.0k 条记录）上微调 Qwen3.5-27B，在 Terminus2-XML 下于 Terminal-Bench 2.0 达到 **52.8%**、于 Terminal-Bench 2.1 达到 **58.1%**（分别比基座 **+11.2** 与 **+11.9**）。在 Claude Code 下，于 Terminal-Bench 2.1 达到 **58.2%**（比基座 +10.4）。

表 3：Terminal-Bench 与 EvoCode-Bench v2 结果（%）。Terminal-Bench 各列为 Avg. Pass@1。绿色加粗标记任务合成方法中的最佳分数，蓝色下划线标记次佳。∗ 标记我们按附录 G 配置在已发布模型上测得的分数；其他分数取自相应报告。

| 模型 | 基座模型 | 数据量 | TB 脚手架 | TB2.0 | TB2.1 | MT@4 | Case Score |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **基座与教师模型** | | | | | | | |
| Qwen3.5-27B | – | – | Terminus2 | 41.6 | 46.2 | 6.3∗ | 67.8∗ |
| Qwen3.7-Max | – | – | Terminus2 | 69.7 | 74.5 | 39.8∗ | 83.4∗ |
| **终端任务合成方法** | | | | | | | |
| TerminalTraj-32B（Wu et al., 2026a） | Qwen2.5-Coder-32B | 50.7k | Terminus2 | 22.0 | 28.5∗ | 0.0∗ | 15.9∗ |
| TermiGen-32B（Zhu et al., 2026） | Qwen2.5-Coder-32B | 3.3k | BashAgent | 19.3 | 21.3∗ | 0.0∗ | 12.2∗ |
| LiberCoder-235B（Lin et al., 2026） | Qwen3-235B-A22B | 48.3k | OpenHands | 31.0 | – | – | – |
| Nemotron-Terminal-32B（Pi et al., 2026） | Qwen3-32B | 490k | Terminus2 | 27.4 | 27.9∗ | 0.0∗ | 13.7∗ |
| SkillSynth-32B（Fan et al., 2026） | Qwen3-32B | 10.7k | Terminus2 | 29.6 | – | – | – |
| Terminal-World-32B（Cheng et al., 2026） | Qwen3-32B | 5.7k | Terminus2 | 31.5 | – | – | – |
| Terminal-Lego-32B（Yang et al., 2026） | Qwen3-32B | 15.3k | Terminus2 | 24.3 | – | – | – |
| CLI-Universe-32B（Hua et al., 2026） | Qwen3-32B | 6k | Terminus2 | 33.4 | – | – | – |
| TMax-27B（Ivison et al., 2026） | Qwen3.6-27B | 14.6k | Vanillux2Agent | 42.7 | 44.9 | 17.1∗ | 72.5∗ |
| OpenThinker-Agent-32B（Raoof et al., 2026） | Qwen3-32B | 100k | Terminus2 | 26.2 | 30.7∗ | 0.0∗ | 19.7∗ |
| Meta-Task-32B（Pan et al., 2026） | Qwen3-32B | 3.2k | Terminus2 | 31.8 | – | – | – |
| RST-27B（Li et al., 2026b） | Qwen3.5-27B | 37.5k | Terminus2 | 49.4 | – | – | – |
| CalibForge-35B-A3B（Meng et al., 2026） | Qwen3.5-35B-A3B | 5.4k | CalibForge-Eval | 47.6 | – | – | – |
| FACET-Terminal-27B（Shi et al., 2026） | Qwen3.5-27B | 1.2k | Terminus2 | – | 47.6 | – | – |
| **Terminal-Universe-27B** | Qwen3.5-27B | 32.0k | Terminus2 | **52.8** | **58.1** | **20.1** | **76.1** |

在 EvoCode-Bench v2 上，Full Mixture 把 MT@4 从 6.3 提升到 **20.1**、把 Case score 从 67.8 提升到 **76.1**，表明 Full Mixture 训练同样提升了在带累积需求的持久任务上的表现。

## 6 分析与消融研究

我们的方法包含多个设计选择，本节逐一分离每个选择的贡献。我们问：(1) 重建环境并重解它，是否真的优于在原始轨迹上训练（§6.1）？(2) 智能体补全是否重要，还是确定性重放就够了（§6.2）？(3) 验证器过滤是否值得它丢弃的那些数据（§6.3）？(4) 固定预算应当如何在各重查询轴之间分配——广度（§6.4）、深度（§6.5），以及更多环境 vs 更多查询（§6.6）？最后我们检验该流水线是否能迁移到终端工作区之外（§6.7）。

### 6.1 任务重解

本消融问的是：是否根本需要重建——重解一个恢复出的任务，是否优于仅仅模仿原始轨迹？表 4 在 Terminal-Bench 2.1 上对比两者。为保持对比干净，Intent Recovery 未经验证器过滤，因此验证器选择在此不起作用。

表 4：源轨迹 SFT 与 Intent Recovery 在 Terminal-Bench 2.1 上的对比（%）。

| 变体 | 数据量 | Claude Code | Terminus2-XML | 均值 |
| --- | --- | --- | --- | --- |
| Qwen3.5-27B | - | 47.8±2.0 | 46.2±3.9 | 47.0 |
| 源轨迹 | 35.8k | 33.0±3.9 | 40.3±2.1 | 36.7 |
| Intent Recovery | 35.8k | **51.3±3.1** | **52.9±1.4** | **52.1** |

**重解优于源轨迹 SFT。** 源轨迹与 Intent Recovery 在 SFT 中使用相同的 Qwen3.5 对话模板与工具调用 schema。源轨迹 SFT 保留了原始智能体的行为，而 Intent Recovery 用一个更强的教师在重建工作区中重解恢复出的任务。源轨迹 SFT 均值为 36.7，而 Intent Recovery 为 52.1，说明在一致的教师策略下重新生成示范能提供更有效的监督。

### 6.2 智能体补全的影响

本消融问的是：智能体补全是否值它的成本，还是仅靠确定性重放就够了。我们通过只用重放（不做补全）重建环境并在 Intent Recovery 语料上训练，来隔离重建的第二阶段。仅重放变体在确定性重放重建出的 35,809 条源实例上训练，补全变体则是相同体量的正式 Intent Recovery 语料。二者共享恢复出的查询与教师配置，仅在环境重建模式上不同。

表 5：智能体补全对 Intent Recovery 的影响。

| 变体 | 记录数 | Terminus2-XML |
| --- | --- | --- |
| Qwen3.5-27B | – | 46.2±3.9 |
| 仅重放 | 35.8k | 48.7±3.5 |
| 重放 + 智能体补全 | 35.8k | **52.9±1.4** |

**智能体补全有帮助。** 在训练体量相近的情况下，在补全环境上训练比在仅重放环境上训练高出 4.2 分（52.9 对 48.7），且跨运行更稳定（±1.4 对 ±3.5）。这与表 2 的充分性结果一致：仅重放会让大多数终端工作区任务不充分，而补全恢复了重解所依赖的执行上下文。

**仅重放监督仍优于基座模型。** 仅重放变体仍比基座模型提升 2.5 分（46.2 到 48.7）。检视其 rollout 可以发现，当面对一个不完整工作区时，教师往往先修复缺失文件或环境设置，然后才着手任务。这些轨迹仍然有用，但其中一部分监督把注意力放在了修复工作区，而非求解恢复出的任务。

### 6.3 验证器过滤的作用

本消融问的是：丢弃未通过验证器的轨迹，是否值得它移除的那些数据。对每种合称方法，我们对比在全部教师轨迹上训练与仅在同一批已启动任务池中通过验证器的子集上训练。

表 6：验证器过滤对 Single-WS 与 Cross-WS 的影响。

| 变体 | 记录数 | Terminus2-XML |
| --- | --- | --- |
| Single-WS 无验证器 | 35.1k | 56.0±3.3 |
| Single-WS 有验证器 | 25.4k | **56.4±2.6** |
| Cross-WS 无验证器 | 7.1k | 53.2±2.1 |
| Cross-WS 有验证器 | 3.5k | **55.4±2.7** |

**验证器过滤对更难的任务更重要。** 对每种合成方法，我们对比全部教师轨迹与同一已启动任务池中通过验证器的子集。在 Single-WS 数据上，通过验证器的子集表现与全语料相近（56.4 对 56.0），但记录数更少。在 Cross-WS 数据上，保留未通过验证器的轨迹会降到 53.2，而通过验证器的子集用不到一半的数据达到 55.4。这一效果在多轮合成中同样可见：去掉轮级验证器监督会拉低两项 EvoCode-Bench 指标（表 9）。

### 6.4 广度扩展

本消融问的是：跨工作区任务是否在单工作区合成之外增加了监督。表 7 用 Single-WS 基线评估 Cross-WS。Cross-WS 单独在 Terminus2-XML 下达到 55.4，而把它加到 Single-WS 上则把性能从 56.4 提升到 **58.4**。

表 7：Single-WS、Cross-WS 及其混合在 Terminal-Bench 2.1 上的结果（%）。

| 变体 | 数据量 | Terminus2-XML |
| --- | --- | --- |
| Qwen3.5-27B | – | 46.2±3.9 |
| Single-WS | 25.4k | 56.4±2.6 |
| Cross-WS | 3.5k | 55.4±2.7 |
| Single-WS + Cross-WS | 28.9k | **58.4±2.1** |

表 8：Single-WS 与 Cross-WS 合成的轨迹与难度画像。

| 变体 | Turns 中位 | Turns 均值 | 工具调用 中位 | 工具调用 均值 | Tokens/记录 中位 | Tokens/记录 均值 | 教师 pass@1 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Single-WS | 14 | 15.1 | 20 | 21.2 | 30.4k | 32.9k | 72.3% |
| Cross-WS | 23 | 25.3 | 38 | 39.7 | 46.5k | 51.9k | 49.2% |

表 8 在同一教师下对比两种合成变体。跨工作区任务产出显著更长、更复杂的轨迹：中位数为 1.6× 的助手轮次、1.9× 的工具调用、1.5× 的每记录 token。它们对教师也更难：pass@1 从单工作区任务的 72.3% 降到 49.2%。把需求接地到第二个代码库，迫使智能体在编辑前阅读并调和两个仓库，这拉长了轨迹、提高了任务难度，而不仅仅是增加了数据体量。

图 6：在 Terminus2-XML 下把 Cross-WS 数据加入 Single-WS 训练后，各类别 Terminal-Bench 2.1 通过率的变化。单任务类别被省略。

**Cross-WS 如何扩展广度。** Single-WS 通过从每个恢复出的环境合成一个新任务，提供工作区内的基线。Cross-WS 超越这一设定：它要求在一个可写工作区中做出改动，而该改动以来自一个相关只读工作区的证据为依据。这暴露出单工作区任务中不存在的"领域—操作"组合，并要求智能体跨代码库调和信息。

**跨工作区数据在哪里有帮助。** 混合单工作区与跨工作区记录在 Terminus2-XML 下达到 58.4，优于单工作区基线（56.4）。图 6 按任务类别拆解了这一对比。软件工程是最大的类别（26 个任务），从 46.9 提升到 49.1；更大的增益出现在模型训练（+15.0）与调试（+10.0）。有三个类别下降 2.1 到 2.5 分，这一范围落在至多 8 个任务的类别运行间波动之内。最大类别的增益连同总体提升共同表明：跨工作区数据在单工作区合成之外增加了有用的监督。

### 6.5 多轮深度扩展

本消融问的是：多轮延续数据是否提升在持久的、累积型任务上的表现，以及生成期间的轮级验证是否重要。我们在 EvoCode-Bench v2 上评测。

**多轮数据提升深度。** 把 Multi-Round 数据加入 Single-WS，把 MT@4 从 18.4 提升到 **21.0**、把 Case score 从 71.9 提升到 **76.9**。更高的 MT@4 表明模型在首次失败前能完成更长的请求序列，而 Case score 的增益表明它在整个会话中通过了更大比例的验证器用例。

**轮级验证导向有效的延续。** 在匹配的 Single-WS + Multi-Round 对比中，去掉轮级验证器反馈使 MT@4 下降 2.2 分、Case score 下降 3.7 分。检视所得轨迹可以发现，在缺少"哪里仍然不对"的接地信号时，延续变得不那么有方向，产出的多轮轨迹更长但质量更低。

表 9：Multi-Round 合成与轮级验证对 EvoCode-Bench v2 的影响（%）。

| 变体 | 数据量 | MT@4 分数 | Case score |
| --- | --- | --- | --- |
| Single-WS | 25.4k | 18.4 | 71.9±3.5 |
| Single-WS + Multi-Round | 28.5k | 21.0 | **76.9±1.4** |
| Single-WS + Multi-Round（无轮级验证器） | 28.5k | 18.8 | 73.2±2.6 |

### 6.6 扩展轴消融

本消融问的是：固定的数据预算最好花在哪里。从一个共同的 Single-WS 基池出发——17,558 个环境，每个有一条查询与一条教师解（17.6k 记录）——我们一次沿一个轴把语料翻倍：追加第二组环境、为每个环境追加第二条查询、或为每条查询追加第二条教师解。三种变体都达到约 35k 记录的匹配预算，并在 §5 的设置下于 Terminal-Bench 2.1 上训练与评测，因此任何差异反映的是预算如何分配，而非预算大小。

表 10：Single-WS 合成的数据扩展消融。从共同基池出发，通过追加环境、每环境查询数或每查询解数把语料翻倍。

| 变体 | 环境数 | 查询/环境 | 解/查询 | 记录数 | Terminus2-XML |
| --- | --- | --- | --- | --- | --- |
| 基池 | 17,558 | 1 | 1 | 17.6k | 53.2±4.1 |
| 环境扩展 | 35,116 | 1 | 1 | 35.1k | **56.0±3.3** |
| 查询扩展 | 17,558 | 2 | 1 | 35.1k | 53.8±3.3 |
| 解扩展 | 17,558 | 1 | 2 | 35.1k | 53.9±2.4 |

在这一匹配预算下，环境扩展带来最大的变动，从 53.2 到 56.0，而追加查询或解几乎不改变分数（53.8 与 53.9）。这一模式符合直觉：每个新环境贡献一个不同的可执行上下文，因而贡献新的监督；而同一工作区上的第二条查询或解，大多只是在重复模型已经见过的东西。这也与我们将重点放在重建更多环境的动机相一致。

### 6.7 跨域泛化

本消融检验该流水线是否能超越它赖以构建的终端领域而有所帮助。我们把 Intent Recovery 应用于来自软件工程（SWE）工作区而非终端工作区的轨迹，然后在 §5 的设置下微调与评测，衡量在 Terminal-Bench 2.1 上的迁移。我们只使用 Intent Recovery，作为最简单的重查询变体，以保持测试干净。

表 11：在 SWE 意图恢复轨迹上训练后 Terminal-Bench 2.1 通过率（%）。

| 变体 | 数据量 | Claude Code | Terminus2-XML | 均值 |
| --- | --- | --- | --- | --- |
| Qwen3.5-27B | - | 47.8±2.0 | 46.2±3.9 | 47.0 |
| Intent Recovery | 10.3k | **50.6±0.9** | **49.4±1.6** | **50.0** |

在我们评估的 1,900 个 SWE 仓库中，有 1,464 个被判定为任务充分。由于一个仓库可能贡献多个源任务，这些仓库产出约 10.3k 条 Intent Recovery 训练轨迹。在它们上面训练把 Terminal-Bench 均值从 47.0 提升到 **50.0**，且两个脚手架同向变动（Claude Code 47.8→50.6，Terminus2-XML 46.2→49.4），因此这一增益并不依附于单一评测设置。这说明从 SWE 工作区合成的轨迹所提供的监督，对终端智能体行为同样有用，而不仅对其自身来源分布有用。此处我们测试的是 SWE→终端方向；反向留待未来工作。

## 7 讨论与局限

**随更丰富的源轨迹扩展。** 虽然 Terminal-Universe 在公开轨迹语料上展现出强有效性，但我们在更高质量轨迹上的经验观察揭示：源轨迹的复杂度与在重建环境上合成出的 rollout 的复杂度之间存在正相关。具有更丰富操作动态的轨迹（例如多文件操作与长工具调用链）暴露出更广的工作区状态，这反过来支撑更多样、更苛刻的合成任务。环境复杂度也可以通过聚合来提高：当多个会话在同一工作区上操作时，把它们一起重放，会将每个会话暴露的状态合并为一份重建结果，产出比任何单条轨迹所能恢复的都更复杂的环境。综合这些观察，该框架会随着智能体能力进步、复杂轨迹越来越易得而自然地扩展。

**局限。** Terminal-Universe 也有若干局限。第一，我们对所有工作区使用标准的 Ubuntu 24.04 容器，而不是像 SWE-Factory（Guo et al., 2026）或 RepoLaunch（Li et al., 2026a）那样通过自动化流水线构建量身定制的、仓库专用环境。因此，需要专门系统依赖或复杂编译步骤的边缘情况可能表现出降低的保真度。第二，我们重建工作区的领域、语言与工具链分布，从根本上受限于所采集源轨迹的覆盖范围。扩展到这些分布之外仍是重要的未来方向。第三，单一教师同时生成任务、解答与验证器。因此它的能力盲区可能限制任务覆盖，而它在解答中犯的错误也可能被它自己的测试漏掉。未来工作可以使用多个教师，并用一个独立模型来做验证器构建。

## 8 结论

在本工作中，我们提出 Terminal-Universe，一个基于轨迹的环境与任务合成框架，把记录下来的智能体轨迹从固定的示范重新诠释为可恢复、可复用的执行环境。通过确定性重放与智能体补全的两阶段过程，Terminal-Universe 恢复潜在的（latent）工作区状态，在每个环境内合成新任务，并把它们跨工作区扩展以获得广度、跨轮次扩展以获得深度。实证评测表明：重解恢复出的任务优于在源轨迹上做 SFT；而经验证器筛选的 Single-WS、Cross-WS 与 Multi-Round 轨迹同时提升了单轮与多轮终端智能体表现。总体而言，我们的发现表明，记录下来的轨迹可以被有效地重新利用为交互式执行环境，为在无需从零构建环境的前提下合成有据可依的智能体训练数据，提供了一种可扩展的范式。

## 致谢

我们感谢 Ye Li 对基于 CPU 的重放框架所做的贡献，该框架支撑了高效的大规模环境重建。

## 附录 A 数据来源与选择

表 12 汇总了每个纳入来源在重建前后的情况。一条轨迹能否被重建，取决于它暴露出的文件证据：多文件编辑痕迹揭示了足够的项目上下文以供重建，而命令繁重的 CLI 痕迹往往暴露的文件内容很少。我们排除源自 Terminal-Bench 的语料，以及以只读操作或不受支持的动作格式为主的来源。

**SWE 去重与去污染。** 公开 SWE 语料常包含同一任务的多条 rollout 或多种格式。我们在每个来源内按仓库、基线 commit 与问题陈述去重，选取重放暴露工作区内容最多的那条轨迹。随后我们移除来自 SWE-bench Verified 仓库的实例（Jimenez et al., 2024），以及无法关联到源轨迹的记录。表 12 给出各来源的最终计数。

表 12：源语料与重建环境。Trajectories 列统计从每个语料抽取的源轨迹数。

| 源语料 | 池 | 许可 | 轨迹数 | 环境数 |
| --- | --- | --- | --- | --- |
| SWE-rebench（Badertdinov et al., 2025） | SWE | CC-BY-4.0 | 67,074 | 6,118 |
| SWE-smith（Yang et al., 2025） | SWE | MIT | 95,851 | 8,476 |
| CoderForge（Ariyak et al., 2026） | SWE | Apache-2.0 | 32,964 | 3,978 |
| SWE-Gym（Pan et al., 2024） | SWE | MIT | 4,152 | 929 |
| LFM2-Terminal（gyung, 2026） | Terminal | CC-BY-4.0 | 139,841 | 46,037 |
| LiteCoder-Terminal（Peng et al., 2026a） | Terminal | MIT | 19,711 | 2,725 |
| **合计** | | | **359,593** | **68,263** |

表 13：智能体补全前后的工作区复杂度。单元格报告 中位/均值。

| | Terminal 池 重放（E₀） | Terminal 池 补全（Ê） | SWE 池 重放（E₀） | SWE 池 补全（Ê） |
| --- | --- | --- | --- | --- |
| 每工作区文件数 | 2 / 2.9 | 13 / 22.4 | 5 / 5.6 | 21 / 37.9 |
| 文本行数（全部文件） | 60 / 90 | 539 / 5,761 | 537 / 595 | 1,854 / 6,622 |
| 代码行数（源文件） | 0 / 43 | 316 / 503 | 421 / 487 | 1,643 / 6,302 |

## 附录 F SFT 数据集统计

表 19 汇总了最终的终端 SFT 语料，turns、工具调用与 token 报告为每条记录的中位数。Multi-Round 记录显著更长，因为它们用追问式用户请求扩展了一个已完成的会话。

表 19：长度过滤后最终 SFT 语料统计。

| 数据集 | 记录数 | Turns | 工具调用 | Tokens |
| --- | --- | --- | --- | --- |
| Intent Recovery | 35,809 | 12 | 17 | 36.1k |
| Single-WS | 25,386 | 14 | 20 | 30.4k |
| Cross-WS | 3,512 | 23 | 38 | 46.5k |
| Multi-Round | 3,079 | 92 | 102 | 126.1k |

## 参考文献

- Anthropic (2026). Claude Code overview. https://code.claude.com/docs/en/overview
- Ariyak, A., Zhang, J., Wang, J., Zhu, S., Bianchi, F., Srivastava, S., Panda, A., Bharti, S., Xu, C., Heo, J., Wu, X. S., Zhou, J., Liang, P., Song, L., Zhang, C., Athiwaratkun, B., Zhou, Z., Wu, Q. (2026). CoderForge-Preview: SOTA open dataset for training efficient agents. Together AI Blog. https://www.together.ai/blog/coderforge-preview
- Badertdinov, I., Golubev, A., Nekrashevich, M., Shevtsov, A., Karasik, S., Andriushchenko, A., Trofimova, M., Litvintseva, D., Yangel, B. (2025). SWE-rebench: an automated pipeline for task collection and decontaminated evaluation of software engineering agents. arXiv:2505.20411. https://arxiv.org/abs/2505.20411
- Cheng, Z., Wang, H., Liu, Z., Wang, X., Zhu, X., Guo, Y., Lin, W., Pan, J. Z., Wang, Y. (2026). Terminal-World: scaling terminal-agent environments via agent skills. arXiv:2605.20876. https://arxiv.org/abs/2605.20876
- Fan, Z., Yu, T., Cai, Y., Guan, J., Yang, Y., Hu, D., Zhou, J., Wu, X., Han, Z., Zhang, F., Wang, L. (2026). Toward scalable terminal task synthesis via skill graphs. arXiv:2604.25727. https://arxiv.org/abs/2604.25727
- Gandhi, K., Garg, S., Goodman, N. D., Papailiopoulos, D. (2026). Endless terminals: scaling RL environments for terminal agents. arXiv:2601.16443. https://arxiv.org/abs/2601.16443
- Guo, L., Wang, Y., Li, C., Tao, W., Yang, P., Chen, J., Song, H., Tang, D., Zheng, Z. (2026). SWE-Factory: your automated factory for issue resolution training data and evaluation benchmarks. arXiv:2506.10954. https://arxiv.org/abs/2506.10954
- gyung (2026). LFM2-Terminal-SFT-Processed. Hugging Face dataset. https://huggingface.co/datasets/gyung/LFM2-Terminal-SFT-Processed
- Hua, et al. (2026). CLI-Universe: taxonomy-guided terminal task synthesis.
- Ivison, H., et al. (2026). TMax: combinatorial sampling for terminal agent training.
- Jain, et al. (2025). R2E-Gym: repository-level environment construction.
- Jimenez, C. E., Yang, J., Wettig, A., Yao, S., Pei, K., Press, O., Narasimhan, K. (2024). SWE-bench: can language models resolve real-world GitHub issues? arXiv:2310.06770. https://arxiv.org/abs/2310.06770
- Li, et al. (2026a). RepoLaunch: automated repository environment construction.
- Li, et al. (2026b). RST: recursive expansion of verified terminal task seeds.
- Lin, et al. (2026). LiberCoder / CLI-Gym. arXiv:2605.29559. https://arxiv.org/abs/2605.29559
- Meng, et al. (2026). CalibForge: adversarial calibration for terminal agents.
- Merrill, M. A., et al. (2026). Terminal-Bench: a benchmark for terminal agents.
- Pan, J., et al. (2024). SWE-Gym: training software engineering agents. arXiv:2412.21139. https://arxiv.org/abs/2412.21139
- Pan, et al. (2026). Meta-Task terminal synthesis.
- Peng, et al. (2026a). LiteCoder-Terminal. arXiv:2504.21798. https://arxiv.org/abs/2504.21798
- Peng, et al. (2026b). ICAE-Bench: interactive project construction evaluation.
- Pi, et al. (2026). Nemotron-Terminal: terminal agent data synthesis.
- Raghavendra, et al. (2026). SWE-INTERACT: simulated-user interactive software engineering.
- Raoof, et al. (2026). OpenThinker-Agent: open terminal agent training data.
- Shen, et al. (2026a). EvoCode-Bench v2: persistent-workspace sequential development evaluation. https://unipat.ai/benchmarks/EvoCode-Bench
- Shen, et al. (2026b). SETA: scaling verifiable terminal environments for reinforcement learning.
- Shi, et al. (2026). FACET-Terminal: terminal task synthesis.
- Wu, et al. (2026a). TerminalTraj: terminal trajectory synthesis.
- Wu, et al. (2026b). SWE-Together: state-conditional user simulation for agent evaluation.
- Yang, et al. (2023). InterCode: interactive code generation via execution feedback.
- Yang, et al. (2025). SWE-smith: scaling data for software engineering agents. arXiv:2504.21798
- Yang, et al. (2026). Terminal-Lego: compositional terminal task construction.
- Zeng, et al. (2026). On container images for executable agent environments.
- Zhu, et al. (2026). TermiGen: task-environment co-generation for terminal agents.
