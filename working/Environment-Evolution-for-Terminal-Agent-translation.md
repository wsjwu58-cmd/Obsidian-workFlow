---
created: 2026-10-03
updated: 2026-10-03
title: Environment Evolution：面向终端智能体的环境演化
sourceUrl: http://arxiv.org/abs/2609.04128v1
sourceAuthor: Zhiyuan Fan、Tinghao Yu、Yuanjun Cai 等（Hunyuan Team, Tencent）
translatedAt: 2026-10-03
sources: [references/articles.md 待处理队列]
tags: [终端智能体, 环境演化, 环境扩展, 强化学习, 多轮学习, 多智能体 harness, GRPO, 长程任务, Qwen, type/翻译]
---

# Environment Evolution：面向终端智能体的环境演化

> [arxiv.org/abs](http://arxiv.org/abs/2609.04128v1)｜分类：cs.AI（人工智能）
> 作者：Zhiyuan Fan、Tinghao Yu、Yuanjun Cai、Jiang Zhou、Jiangtao Guan、Jincheng Liu、Yun Yang、Dingxin Hu、Zhuo Han、Xing Wu、Feng Zhang、Lilin Wang（Hunyuan Team, Tencent）
> 提交：2026-09-03（arXiv v1）｜许可：CC BY 4.0
> 原文：http://arxiv.org/abs/2609.04128v1｜DOI：https://doi.org/10.48550/arXiv.2609.04128

## 摘要

扩展可交互、可验证的环境，是训练终端智能体（terminal agents）的关键。随着前沿模型（frontier models）能力越来越强，从零合成（synthesized from scratch）的环境变得不再有挑战性，因而只能提供有限的学习信号。近期的协同演化（co-evolution）方法会根据 rollout 中暴露出的弱点，迭代地合成接近模型"可学习前沿"（learnable frontier）的环境。然而，这类方法依赖 on-policy rollout，限制了泛化能力，也限制了当模型变强时学习信号的持续供给。本文提出**环境演化（environment evolution）**：它以 off-policy 的方式逐步提高环境难度，并在训练过程中按"代"（generation）调度演化出的环境，从而持续提供学习信号。我们从多轮学习目标（multi-turn learning objective）中推导出三条影响环境难度的演化方向，并通过一个循环工程化（loop-engineered）的多智能体 harness 沿这些方向实现演化。使用 Hy4 preview、Claude Opus 5 与 GPT-5.6 Sol 进行的定量 rollout 实验表明，环境演化能稳定地产出更难的环境。我们通过简单的长程 RL 训练，在 Qwen3.6-27B 与 Qwen3.6-35B-A3B 上验证了其有效性，在 Terminal-Bench 2.1 上分别将性能提升 14.4 与 18.0 个百分点。

## 1 引言

强化学习环境正成为训练有能力智能体的下一个可扩展方向（Bellemare et al., 2013；Brockman et al., 2016）。随着工业级智能体 RL 算法趋于稳定、异步基础设施日益成熟（Fu et al., 2026；Cao et al., 2025；Tan et al., 2025），进一步扩展的重心正在向环境转移。对通用终端智能体而言，环境的难度与多样性因此成为决定智能体通过可验证反馈能学到什么的中心杠杆：自适应难度保持持续学习（continual learning）的潜力，而多样性支撑泛化能力（Dennis et al., 2021；Jiang et al., 2021；Parker-Holder et al., 2023；Garcin et al., 2024；Cobbe et al., 2020；Team et al., 2021；Merrill et al., 2026）。

近期工作专注于通过人工设计的流水线从零合成大规模终端环境，把多样资源（例如 GitHub 仓库、技能与网页）转化为可执行的终端环境，每个环境都配有相应的指令（做什么）与验证系统（如何评估完成）（Gandhi et al., 2026；Wu et al., 2026；Fan et al., 2026；Pi et al., 2026；Hua et al., 2026；Zhao et al., 2026；Yao et al., 2026）。然而，这些环境对当前前沿模型往往不够有挑战性，模型在反复 rollout 中能稳定地解决它们。当用于 RL 训练时，这类环境会被丢弃：它们无法提供区分更好与更差轨迹的有效学习信号，既浪费环境构建成本，又降低了保留下来的训练分布的多样性。

为了提供有用的学习信号，现有协同演化方法把模型训练与环境合成耦合起来：在种子环境（seed environments）上做 on-policy rollout 以暴露弱点，再据此引导合成"保持挑战性但仍可学习"的新环境（Zala et al., 2024；Hu et al., 2025；Guo et al., 2025；Sygkounas et al., 2026）。然而，由此得到的环境受 rollout 模型与初始环境分布约束，限制了泛化能力，也限制了当训练饱和、模型失败变得稀疏时持续提供学习信号的能力。

**图 1：环境扩展范式的对比。**（a）环境集成（environment ensemble）通过组合若干困难的原语环境（primitive environments）得到一个新环境。（b）智能体–环境协同演化（agent–environment co-evolution）在原始环境上 rollout 目标智能体，以填充弱点库（weakness bank），据此引导新环境的构建。（c）环境演化（本文提出的范式）：演化器（evolver）利用推导出的难度信号，沿谱系（lineage）产出相继的环境。

本文提出**环境演化**：它不依赖 rollout 模型，逐代提高环境难度，如图 1 所示。我们从多轮学习目标出发，推导出一个 off-policy 的环境难度公式，识别出**场景（scenario）新颖度**、**技能（skill）稀有度**与执行**长度（length）**是影响难度的三个因素。随后，我们用一个循环工程化的多智能体 harness 实现环境演化：沿这三条方向之一增量地修改已有环境，从而构建难度递增的谱系，同时围绕原始环境分布引入多样的变化。使用 Hy4 preview、Claude Opus 5 与 GPT-5.6 Sol 进行的基于 rollout 的难度估计表明，尽管这些环境是 off-policy 合成的，它们对不同模型都具有挑战性。在模型开发过程中，我们还发现：即使种子环境已被用于 SFT，演化出的环境仍能持续提供有挑战性的 RL 信号。在 Qwen3.6-27B 与 Qwen3.6-35B-A3B 上的实验表明，环境演化把 Terminal-Bench 2.1 的性能分别提升 14.4 与 18.0 个百分点。与智能体–环境协同演化相比，off-policy 的环境演化能提供更持久的学习信号，并获得更好的性能。总结而言，我们的贡献如下：

1. 我们从多轮学习目标推导出一个与模型无关（model-agnostic）的环境难度公式，说明环境演化是提高环境难度的一种更通用的方法。
2. 我们提出**环境演化**，并将其实现为一个循环工程化的多智能体 harness，增量地演化已有环境，构建经过验证、难度递增的谱系。
3. 我们通过 Qwen3.6-27B 与 Qwen3.6-35B-A3B 上的 200 步长程 RL 实验验证了该方法，证明它比协同演化与集成的基线提供更持久的学习信号，并在 Terminal-Bench 2.1 上分别提升 14.4 与 18.0 个百分点。

## 2 相关工作

#### 终端智能体

终端智能体通过命令行工具与计算系统交互（Chen et al., 2021；Yang et al., 2024；Merrill et al., 2026），从而获得开放式地探索与利用计算资源、并迭代地使用环境反馈完成长程任务的能力（Yao et al., 2023）。关于 harness 设计的一条研究路线，旨在增强智能体的规划、导航与探索能力，同时约束不良行为，重点在观测空间设计、上下文压缩与工具路由（Lee et al., 2026；Wang et al., 2025；Bui, 2026）。社区最近转向从零合成大规模终端环境以训练智能体（Gandhi et al., 2026；Wu et al., 2026；Fan et al., 2026；Pi et al., 2026；Hua et al., 2026；Zhao et al., 2026；Yao et al., 2026）。尽管这些开源环境数量充足、领域覆盖面广，但我们的大规模 rollout 与质量评估实验揭示：它们存在奖励信号质量低（例如任务指令与验证系统不匹配、环境损坏）（Bercovich, 2026）的问题，而且难度不足，难以为前沿模型提供有意义的学习信号。

#### 环境扩展

开放式强化学习需要持续不断地提供"可解但有挑战、且保留学习潜力"的环境（Wang et al., 2019；Dennis et al., 2021；Jiang et al., 2021；Parker-Holder et al., 2023）。Paired Open-Ended Trailblazer（POET）协同演化一个环境–智能体对种群，通过环境变异生成新挑战，并把智能体跨环境迁移以利用"垫脚石"（stepping stones）（Wang et al., 2019；Wang et al., 2020）。无监督环境设计（Unsupervised Environment Design, UED）把"从欠规定的环境参数自动构建与策展有效且可解的环境"形式化，涵盖基于遗憾（regret）的生成、优先回放（prioritized replay）与增量关卡编辑（Dennis et al., 2021；Jiang et al., 2021；Jiang et al., 2022；Parker-Holder et al., 2023）。近期工作开始把这些思想引入 LLM 智能体：通过反馈条件生成（feedback-conditioned generation）（Chen et al., 2026；Yang et al., 2026）、在线课程（online curricula）（Qi et al., 2025）以及智能体–环境协同演化（Guo et al., 2025；Liu et al., 2026），这些方法随智能体能力的提升自适应地调整环境分布，使环境始终接近其能力前沿。然而，它们需要一个指定的智能体通过 on-policy rollout 来估计环境难度，而且得到的环境同时与 rollout 智能体和初始环境分布相关。环境演化则不同：它独立于目标策略构建难度递增的谱系，并在训练中调度相继的代，以持续提供学习信号。

## 3 预备知识

我们不采用 on-policy 的方式来估计难度（例如 rollout 一个模型、用其通过率作为难度指标），而是需要一个从多轮学习目标推导出的、衡量环境自身难度的 off-policy 指标。由于模型在不同数据分布上训练，与某个模型 θ 绑定的难度估计实际上是"模型特定的弱点"，而不是环境难度。

我们首先把智能体–环境交互看作一个具有交错观测与动作的马尔可夫过程（Kaelbling et al., 1998）。令 h_t = (o_{≤t}, a_{<t})。于是 o_t ∼ O_E(·|s_t)，a_t ∼ π_θ(·|h_t, g)，s_{t+1} ∼ P_E(·|s_t, a_t)，并由此诱导出一条低层执行轨迹 ζ = (o_0, a_0, o_1, a_1, …, o_T)。

沿用层级化智能体执行的既有定义（Sutton et al., 1999），我们把高层的智能体执行轨迹视为场景与技能执行的交错：

ξ = (σ_0, κ_1, σ_1, …, κ_L, σ_L),

其中 σ_t 是第 t 步的高层场景，κ_t 是在该场景下施加的技能。

在模型 θ 下，高层轨迹的似然按它到达的场景与它施加的技能分解。取负对数似然即得到模型特定的难度：

D_θ(ξ) = −log p_θ(ξ | g)
= Σ_{t=1}^{L} [ −log p_θ(σ_{t−1} | g) − log p_θ(κ_t | σ_{t−1}, g) ]。

这个量有三个贡献来源。第一，L 是轨迹所需的、有意义的求解轮数。第二，−log p_θ(σ_{t−1} | g) 度量场景在该模型下的新颖度。第三，−log p_θ(κ_t | σ_{t−1}, g) 度量在该场景下施加所需技能的稀有度。后两项依赖于策略：它们取决于模型的训练数据分布与学到的策略。

为了得到一个与策略无关的难度度量，我们把依赖模型的概率替换为植根于广泛世界知识的参考分布 𝒯 下的概率：

D_𝒯(ξ) = Σ_{t=1}^{L} [ −log p_𝒯(σ_{t−1} | g) − log p_𝒯(κ_t | σ_{t−1}, g) ]。

这里 p_𝒯(σ | g) 度量某个场景在环境族（environment family）中的常见程度，而 p_𝒯(κ | σ, g) 度量所需技能在该场景下的常见程度。这把估计从"模型特定的弱点"转变为"与模型无关的环境难度"。特别地，一个深度研究智能体（deep-research agent）可以通过广泛的网络搜索来估计这两个分布，借助提供 g 与 ξ 的相对上下文，把它们锚定在世界知识上。

这同时给出了一条把环境难度与智能体弱点直接联系起来的途径。令 z_t = (σ_{t−1}, κ_t) 表示第 t 步的"场景–技能"需求，并定义每步难度

d_θ(z_t | g) = −log p_θ(σ_{t−1} | g) − log p_θ(κ_t | σ_{t−1}, g)， 及在 p_𝒯 下类似的 d_𝒯(z_t | g)。智能体弱点是在减去环境族难度之后仍然残留的"多余难度"：

δ_θ(z_t | g) = [ d_θ(z_t | g) − d_𝒯(z_t | g) ]_+，

其中 [x]_+ = max(x, 0)。等价地，

δ_θ(z_t | g) = [ log ( p_𝒯(σ_{t−1} | g) / p_θ(σ_{t−1} | g) ) + log ( p_𝒯(κ_t | σ_{t−1}, g) / p_θ(κ_t | σ_{t−1}, g) ) ]_+。

对完整的高层轨迹，

Δ_θ(ξ) = Σ_{t=1}^{L} [ d_θ(z_t | g) − d_𝒯(z_t | g) ]_+。

因此，弱点不是环境本身的难度；它是该轨迹中，相对于环境族而言对某个特定模型异常困难的那一部分。

这一区分澄清了智能体与环境 on-policy 协同演化的适用范围。这类方法从模型 θ 收集 rollout，识别模型的失败模式，并围绕这些失败生成新环境。若用 e_t^θ 表示第 t 步的失败，则由此诱导的信号主要是 Σ_{t=1}^{L} e_t^θ [ −log p_θ(κ_t | σ_{t−1}, g) ]。也就是说，智能体与环境的 on-policy 协同演化主要针对的是：在种子环境所包含、且被当前模型在 rollout 中到达的场景下，出现的技能选择错误。它既不显式控制所需的求解步数 L，也不系统性地提高 p_𝒯(σ | g) 下的场景新颖度。相比之下，环境演化直接在整个难度空间上操作：

( L, −log p_𝒯(σ | g), −log p_𝒯(κ | σ, g) )，

这表明环境演化是提供持续学习信号的一种更通用的范式。

## 4 方法

### 4.1 序列引导的环境演化

**图 2：用于环境演化的循环工程化多智能体 harness。** 它把每一代分解为两个带门控的反馈回路：（1）序列引导的计划精化（plan refinement），生成并修订一个演化计划，直到它通过基于评分细则（rubric）的审查；（2）以计划为条件的环境精化（environment refinement），演化并修复候选环境，直到它通过严格的可解性（solvability）与质量检查。

环境演化被实现为一个循环工程化的多智能体 harness，如图 2 所示。它以最近一次被接受的环境为输入，在场景与技能层面、由预期执行轨迹引导，通过增量修改产出下一代环境。

#### 回路 1：计划精化

Proposer（提议者）首先从环境 E 中抽取一条场景与技能交错的执行序列：

ξ_E = (σ_1, κ_1), …, (σ_L, κ_L)。  (1)

然后它根据当前代所选的演化方向更新该序列。对于**长度（length）**，它向序列中插入"场景–技能"对，沿预期执行轨迹引入额外的依赖关系。对于**场景（scenario）**，它替换一个场景而保留与之配对的技能；对于**技能（skill）**，它替换一个技能。计划由更新后序列与原始序列之间的差异生成，并由一个基于评分细则的审查者（reviewer）迭代审查，直到计划被接受，或当前演化方向失败。

#### 回路 2：环境精化

通过审查的计划随后被交给 Modifier（修改者），后者构造一个残差 ΔE 并将其施加到当前环境上。每个候选环境都必须通过三个并行运行的验证器：（i）Oracle 验证器检查参考解（reference solution）能在沙箱中成功执行；（ii）无效测试（Invalid-test）验证器确认空解或 no-op 解会失败，从而保证验证系统可靠；（iii）自适应通用评分细则验证器检查环境质量。在开发阶段，被接受的环境还要经过人在环（human-in-the-loop）审查。对于绕过基于评分细则检查的问题，我们将其转化为新的评分细则，补充给计划审查者与环境验证器，直到该回路能可靠地产出"未被人审发现任何问题"的环境。

#### 演化力度

为了控制相邻代之间的变异幅度，我们引入一个由提示词控制的变异参数，称为**演化力度（evolution effort）**，其精神类似于思考力度（thinking effort），设有低、高、极高（low、high、max）三档。如果说演化方向决定了执行哪一类序列级编辑，那么演化力度则控制该编辑的幅度。三档力度分别把编辑限制在一对 (σ_ℓ, κ_ℓ)、一段连续区间，或序列中不受限制的部分。第 5 节定量验证了这一设计的有效性。

在每一代，我们随机排列三个演化方向。如果计划审查者拒绝了一个计划，或当前方向的修复预算耗尽，我们就回退到下一个方向，从同一环境构造新的目标序列并重复该过程。只有当所有三个方向都失败时，该分支才终止。

### 4.2 演化谱系调度器

随着演化推进，越靠后的代越难。因此，从整条谱系中随机采样可能让策略暴露在它尚无法解决的环境上，产生全失败的 rollout 组，提供不了有效的学习信号。为此我们提出**演化谱系（Evolution-Lineage, EL）调度器**，它从最早的一代开始，按顺序调度各代的环境。令 E_{i,g,k} 表示谱系 i 中第 g 代的第 k 个环境，该代共有 N_{i,g} 个环境。在第 u 次更新时，调度器按如下方式更新活跃索引：

    (g_{u+1}, k_{u+1}) =
      (g_u, k_u)，            若 p̂_u(E_{i,g_u,k_u}) ≤ τ；
      (g_u, k_u + 1)，         若 p̂_u(E_{i,g_u,k_u}) > τ 且 k_u < N_{i,g_u}；
      (g_u + 1, 1)，           若 p̂_u(E_{i,g_u,k_u}) > τ 且 k_u = N_{i,g_u}。

其中 p̂_u(E) = (1/B) Σ_{b=1}^{B} r_{u,b}。  (2)

我们取 B = 8、τ = 6/8。一旦当前环境超过该阈值，调度器就移动到同代的下一环境。只有当当前代不再有环境剩余时，它才前进到下一代。

## 5 实验

### 5.1 实验设置

#### Harness

本文的评估与 RL 训练都使用 Claude Code harness（Anthropic, 2025）。它在各模型间固定工具协议，同时通过在单个 assistant 轮次内并行发起多个工具调用，提高执行效率。对于 RL 训练，harness 以 256K 上下文窗口运行，并在剩余可用上下文降到 16K 时自动压缩（auto compact）轨迹，为长程执行提供稳定的上下文管理。

#### 基准

Terminal-Bench 2.1 Verified（Merrill et al., 2026）是衡量终端智能体能力的主要留出（held-out）基准。它修复了 Terminal-Bench 2.0 中妨碍可复现评估、并会错误低估基准性能的不稳定问题。每个任务配置 32 个 CPU 核与 48 GB 内存，超时为 4 小时。采样使用 temperature 1.0、top-p 0.95、top-k 20，并在每个 assistant 轮次采用动态输出预算 256K − L_used，以避免因单轮过长导致的截断错误。我们报告五次运行的平均值。

#### 训练算法

我们使用 GRPO（Shao et al., 2024）进行智能体 RL 训练，采用部分 rollout（partial rollouts）、GPU 位置完全异步，以及取值为 5 的陈旧度上界（staleness bound），以减少 GPU 空泡时间。当 Claude Code harness 的自动压缩被触发时，其摘要会保留在完整轨迹中，并作为常规动作轮次参与多轮信用分配（multi-turn credit assignment）。我们训练 Qwen3.6-27B（一个 27B 参数的稠密模型）与 Qwen3.6-35B-A3B（一个总参数 35B、激活参数 3B 的混合专家模型）。两个 checkpoint 的原生上下文长度都是 262,144 token。对 MoE 模型，我们额外使用 R3（Ma et al., 2025）来稳定训练过程。

#### 监控指标

环境难度由 8 次独立 rollout 的通过率估计。我们还记录平均 assistant 轮数，作为长程执行的度量；assistant 轮数通常约占总轮数的一半。Rollout 使用 Claude Opus 5 与 GPT-5.6 Sol（xhigh 力度）以及 Hy4 preview（Tencent Hunyuan, 2026，high 力度），全部使用 1M 上下文窗口。环境变异（environment mutation）：对每一代，相对于种子环境的结构变化分别在指令、环境与验证系统上度量，其变异分别按 token、文件与测试单元层级度量。

#### 种子环境选择

我们从 Hugging Face 与 GitHub 收集了 47,678 个非基准终端环境，并通过严格的评分细则过滤（针对环境质量与可解性）保留了 127 个。每个候选环境必须包含一个通过验证器的可执行 Oracle 解，满足基于评分细则的质量检查（我们发现环境质量对成功的 RL 训练至关重要），并达到 Claude Opus 5 下的难度阈值：通过率至多 4/8、平均轮数至少 30。随后用 SkillSynth（Fan et al., 2026）补充新合成的环境，这些环境同样要经过质量与难度过滤。最后，跨领域均匀采样得到一个均衡、多样的 500 个环境的种子池。

### 5.2 演化力度

**图 3：在 low、high、max 三档演化力度下，经过 15 代演化的环境难度，分别由 Hy4 preview、Claude Opus 5 与 GPT-5.6 Sol 独立评估。**

从相同的种子环境出发，随机化的交叉模式（cross-mode）策略分别在 low、high、max 三档演化力度下独立构建 15 代谱系。我们统一设 15 代为上限，因为一旦某条谱系进入"零通过"区间，通过率就再也不能提供分辨率；超过该点后，额外演化的有效性无法从 rollout 结果中可靠地评估。

如图 3 所示，low 力度逐步延长长程执行，平均轮数随代际增加而上升，但其通过率上下波动，且始终高于零。由于 low 只修改一个局部对 (σ_ℓ, κ_ℓ)，相继的代可能反复编辑同一对，并部分回到更早的配置。相比之下，high 与 max 单调地把通过率降到零并提高平均轮数，其中 max 更早达到零，且产生的难度变化更大。

**图 4：在 low、high、max 三档演化力度下，G1–G15 各代的指令、环境与验证系统变异率。**

图 4 把代级变异率拆分为指令、环境与验证系统三个部分。在 high 与 max 下，指令变异率保持高位，两者在 95% 与 100% 之间波动并呈下降趋势，而环境与验证系统的变化则更具选择性。在"有效且稳定的演化"与"每一代的可控性"之间权衡，我们采用 high 作为默认演化力度。

### 5.3 演化方向

| 方向 | Δ 通过率 | Δ 平均轮数 | 指令 | 环境 | 验证系统 | 合计 |
| --- | --- | --- | --- | --- | --- | --- |
| **单步效果** | | | | | | |
| scenario | −4.7 pp | +13.5 | 99.8% | 59.6% | 53.8% | 71.1% |
| skill | −4.0 pp | +12.5 | 99.1% | 50.3% | 58.4% | 69.3% |
| length | −7.1 pp | +9.4 | 87.5% | 45.2% | 58.6% | 63.8% |
| **15 步平均效果** | | | | | | |
| scenario | −2.9 pp | +9.5 | 97.1% | 34.6% | 43.7% | 58.5% |
| skill | −2.7 pp | +10.6 | 96.5% | 27.8% | 45.8% | 56.7% |
| length | −4.8 pp | +7.4 | 85.5% | 34.3% | 48.9% | 56.2% |

**表 1：high 演化力度下演化方向效果的单步一致性。** 两个难度变化列由 Claude Opus 5（xhigh 思考力度）测量。第一个区块对同一批种子环境各施加一次方向；第二个区块对每个方向连续演化 15 步，并在 15 次代际转移上平均各指标。两个区块之间的一致性检验了每个方向是否能在更长的谱系上保持稳定、且方向特有的变化轮廓。难度变化按"后一代减前一代"计算，组件列报告代级变异率，合计为其未加权平均。

为了隔离演化方向的效果，我们固定 high 演化力度，把 scenario、skill 与 length 施加到同一批种子环境上。在每一代，我们同时测量通过率与平均轮数的变化，以及指令、环境与验证系统的变异。单步效果刻画每个方向带来的即时变化，而 15 步平均则在方向特定的谱系上对相邻转移取相同指标的平均，以检验该效果是否持续。

三个方向都一致地降低通过率并提高平均轮数。length 带来最大的通过率下降，而 scenario 与 skill 带来更大的平均轮数增长。scenario 产生最大的总体变异，而 length 在带来最强通过率下降的同时，总体变异最小。单步与 15 步结果之间的一致性表明，这些方向特有的轮廓能持续到单次编辑之外。因此在完整的演化过程中，各方向在每一代被随机排序，以多样化产出的谱系，并在当前方向失败时进行交叉模式回退。

### 5.4 RL 训练动态

在 RL 训练之前，每个基座模型会生成轨迹用于拒绝采样微调（rejection sampling fine-tuning, RFT）（Touvron et al., 2023）。只有通过验证系统且符合 Claude Code 协议的轨迹会被保留。过滤后的集合会针对轨迹多样性重新平衡，以提高策略熵，从而获得更好的 RL 训练。从由此得到的 RFT checkpoint（记为 step 0）出发，我们用 GRPO 对每个模型训练 200 步。

#### EL 调度器

EL 调度器按顺序推进每条环境谱系，只有当第 g 代在式（2）中达到通过率阈值后，才暴露第 g+1 代。图 5 在匹配 rollout 预算的条件下，把它与随机调度在前 50 个 RL 步上做了对比。通过避免过早暴露于策略尚无法解决的代，调度器更高效地利用 rollout 预算，并为 GRPO 提供更有信息量的学习信号——更多 rollout 组保持部分解决，从而保留非零的组内优势（within-group advantage）。在整个 200 步 RL 训练中，默认使用 EL 调度器。

**图 5：前 50 个训练步的早期训练动态。** 实线表示"部分解决"的 rollout 组比例（八次 rollout 中有一到七条成功轨迹）；虚线表示平均训练奖励。

#### 轮数与 Token

训练期间，调度器逐步接纳更难的环境，而这些环境往往需要更长的交互视野。如图 6 所示，这一推进伴随着每条轨迹的轮数与 token 数同时增加。每轮 token 数也在增加，说明策略为每次交互分配了更多的思考力度。

**图 6：Qwen3.6-27B（左）与 Qwen3.6-35B-A3B（右）在 200 个 RL 训练步上的轨迹长度；左右两个 y 轴分别报告每条轨迹的平均轮数与 token 数，注释标在第 200 步。** 每轮 token 数从约 951 增至 1,221（Qwen3.6-27B）、从 947 增至 1,103（Qwen3.6-35B-A3B）。

### 5.5 对比

为确保环境扩展各范式之间的公平对比，我们把 Claude Opus 5 固定为环境合成模型，并保持训练环境总数不变。

**图 7：Qwen3.6-27B（左）与 Qwen3.6-35B-A3B（右）在 200 个 RL 训练步上的 checkpoint 性能，每 10 步做一次离线评估；注释标出每种方法的峰值准确率及对应的训练步。** Step 0 表示用于在 RL 训练前提高策略熵的、经过 RFT 的共享 checkpoint。

#### 环境集成（Environment Ensemble）

首先在种子环境上评估目标智能体，选出它无法解决的环境。然后枚举所有二环境与三环境组合，把每个组合合并为一个更难的环境。该过程以树的方式递归应用，一层的输出成为下一层的输入。

#### 智能体–环境协同演化（Agent–Environment Co-Evolution）

目标智能体首先在种子环境上 rollout 生成轨迹。分析其失败轨迹以构建弱点库，从中采样组合来合成新的、更难的环境。智能体训练 50 个 RL 步后重复该过程。

#### 环境演化（Environment Evolution）

环境演化在每一代随机排序三种模式并遵循交叉模式回退，对每个种子环境产出经过验证的 15 代谱系，且无需目标智能体的 rollout。

图 7 报告了每 10 个 RL 步的离线 Terminal-Bench 2.1 评估。环境演化在 Qwen3.6-27B 与 Qwen3.6-35B-A3B 上分别达到 71.5% 与 64.9% 的峰值准确率，而协同演化为 62.9% 与 55.1%，集成为 60.0% 与 52.8%。

## 6 结论

本文提出**环境演化**，它为 RL 训练增量地合成难度递增的环境。建立在推导出的、off-policy 的环境难度公式之上，它是面向终端智能体扩展环境的一种更通用范式。在不同的模型上，尽管演化出的环境是 off-policy 合成的，它们的难度仍逐代稳定上升。把这些环境沿谱系调度后，对 Qwen3.6-27B 与 Qwen3.6-35B-A3B 的长程 RL 训练获得了持续有效的学习信号，并取得优于协同演化与集成基线的性能。未来工作将探索环境演化在 SWE 智能体与计算机使用智能体（Computer-Use Agents）上的潜力。

## 参考文献

- Anthropic (2025). Claude Code. https://code.claude.com/docs/en/overview
- Bellemare, M. G., Naddaf, Y., Veness, J., Bowling, M. (2013). The arcade learning environment: an evaluation platform for general agents. arXiv:1207.4708. https://arxiv.org/abs/1207.4708
- Bercovich, I. (2026). What makes a good terminal-agent benchmark task: a guideline for adversarial, difficult, and legible evaluation design. arXiv:2604.28093. https://arxiv.org/abs/2604.28093
- Brockman, G., Cheung, V., Pettersson, L., Schneider, J., Schulman, J., Tang, J., Zaremba, W. (2016). OpenAI gym. arXiv:1606.01540. https://arxiv.org/abs/1606.01540
- Bui, N. D. Q. (2026). Building effective AI coding agents for the terminal: scaffolding, harness, context engineering, and lessons learned. arXiv:2603.05344. https://arxiv.org/abs/2603.05344
- Cao, S., Li, D., Zhao, F., Yuan, S., Hegde, S. R., Chen, C., Ruan, C., Griggs, T., Liu, S., Tang, E., Liaw, R., Moritz, P., Zaharia, M., Gonzalez, J. E., Stoica, I. (2025). SkyRL-agent: efficient RL training for multi-turn LLM agent. arXiv:2511.16108. https://arxiv.org/abs/2511.16108
- Chen, M., Tworek, J., Jun, H., Yuan, Q., et al. (2021). Evaluating large language models trained on code. arXiv:2107.03374. https://arxiv.org/abs/2107.03374
- Chen, Z., Zhao, Z., Zhang, K., Liu, B., Qi, Q., Wu, Y., Kalluri, T., Cao, S., Xiong, Y., Tong, H., Yao, H., Li, H., Zhu, J., Li, X., Song, D., Li, B., Weston, J., Huynh, D. (2026). Scaling agent learning via experience synthesis. In The Fourteenth International Conference on Learning Representations (ICLR). https://openreview.net/forum?id=cf7qpBwttr
- Cobbe, K., Hesse, C., Hilton, J., Schulman, J. (2020). Leveraging procedural generation to benchmark reinforcement learning. arXiv:1912.01588. https://arxiv.org/abs/1912.01588
- Dennis, M., Jaques, N., Vinitsky, E., Bayen, A., Russell, S., Critch, A., Levine, S. (2021). Emergent complexity and zero-shot transfer via unsupervised environment design. arXiv:2012.02096. https://arxiv.org/abs/2012.02096
- Fan, Z., Yu, T., Cai, Y., Guan, J., Yang, Y., Hu, D., Zhou, J., Wu, X., Han, Z., Zhang, F., Wang, L. (2026). Toward scalable terminal task synthesis via skill graphs. arXiv:2604.25727. https://arxiv.org/abs/2604.25727
- Fu, W., Gao, J., Shen, X., Zhu, C., Mei, Z., He, C., Xu, S., Wei, G., Mei, J., Wang, J., Yang, T., Yuan, B., Wu, Y. (2026). AReaL: a large-scale asynchronous reinforcement learning system for language reasoning. arXiv:2505.24298. https://arxiv.org/abs/2505.24298
- Gandhi, K., Garg, S., Goodman, N. D., Papailiopoulos, D. (2026). Endless terminals: scaling RL environments for terminal agents. arXiv:2601.16443. https://arxiv.org/abs/2601.16443
- Garcin, S., Doran, J., Guo, S., Lucas, C. G., Albrecht, S. V. (2024). DRED: zero-shot transfer in reinforcement learning via data-regularised environment design. arXiv:2402.03479. https://arxiv.org/abs/2402.03479
- Guo, J., Yang, L., Chen, P., Xiao, Q., Wang, Y., Juan, X., Qiu, J., Shen, K., Wang, M. (2025). GenEnv: difficulty-aligned co-evolution between LLM agents and environment simulators. arXiv:2512.19682. https://arxiv.org/abs/2512.19682
- Hu, M., Zhao, P., Xu, C., Sun, Q., Lou, J., Lin, Q., Luo, P., Rajmohan, S. (2025). AgentGen: enhancing planning abilities for large language model based agent via environment and task generation. arXiv:2408.00764. https://arxiv.org/abs/2408.00764
- Hua, Z., Yao, Y., Xie, W., Zhao, Y., Liu, M., Qiu, R., Huang, Z., Wang, Z., Ji, Y., Ye, Y., Zhu, L., Lei, X., Li, H., Ma, Z., Wang, Z., Zhang, Z., Liu, J. (2026). CLI-Universe: towards verifiable task synthesis engine for terminal agents. arXiv:2606.22883. https://arxiv.org/abs/2606.22883
- Jiang, M., Dennis, M., Parker-Holder, J., Foerster, J., Grefenstette, E., Rocktäschel, T. (2022). Replay-guided adversarial environment design. arXiv:2110.02439. https://arxiv.org/abs/2110.02439
- Jiang, M., Grefenstette, E., Rocktäschel, T. (2021). Prioritized level replay. arXiv:2010.03934. https://arxiv.org/abs/2010.03934
- Kaelbling, L. P., Littman, M. L., Cassandra, A. R. (1998). Planning and acting in partially observable stochastic domains. Artificial Intelligence, 101(1–2), 99–134.
- Lee, Y., Nair, R., Zhang, Q., Lee, K., Khattab, O., Finn, C. (2026). Meta-harness: end-to-end optimization of model harnesses. arXiv:2603.28052. https://arxiv.org/abs/2603.28052
- Liu, B., Yu, S., Jiang, Y., Qu, A., Zhao, A., Liu, Z., Kim, J., Zhou, Z., Kim, S., Ren, T., Liu, M., Yu, H., Chen, Z., Shi, W., Liang, P. P., Zettlemoyer, L., Choi, Y., Jaques, N. (2026). SPADE: self-play in adaptive synthetic executable environments. arXiv:2608.19197. https://arxiv.org/abs/2608.19197
- Ma, W., Zhang, H., Zhao, L., Song, Y., Wang, Y., Sui, Z., Luo, F. (2025). Stabilizing MoE reinforcement learning by aligning training and inference routers. arXiv:2510.11370. https://arxiv.org/abs/2510.11370
- Merrill, M. A., Shaw, A. G., Carlini, N., Li, B., Raj, H., Bercovich, I., et al. (2026). Terminal-Bench: benchmarking agents on hard, realistic tasks in command line interfaces. arXiv:2601.11868. https://arxiv.org/abs/2601.11868
- Parker-Holder, J., Jiang, M., Dennis, M., Samvelyan, M., Foerster, J., Grefenstette, E., Rocktäschel, T. (2023). Evolving curricula with regret-based environment design. arXiv:2203.01302. https://arxiv.org/abs/2203.01302
- Pi, R., Lam, G., Shoeybi, M., Jannaty, P., Catanzaro, B., Ping, W. (2026). On data engineering for scaling LLM terminal capabilities. arXiv:2602.21193. https://arxiv.org/abs/2602.21193
- Qi, Z., Liu, X., Iong, I. L., Lai, H., Sun, X., Sun, J., Yang, X., Yang, Y., Yao, S., Xu, W., Tang, J., Dong, Y. (2025). WebRL: training LLM web agents via self-evolving online curriculum reinforcement learning. In The Thirteenth International Conference on Learning Representations (ICLR). https://proceedings.iclr.cc/paper_files/paper/2025/hash/c66e1fcc9691aae706250638f36f681b-Abstract-Conference.html
- Shao, Z., Wang, P., Zhu, Q., Xu, R., Song, J., Bi, X., Zhang, H., Zhang, M., Li, Y. K., Wu, Y., Guo, D. (2024). DeepSeekMath: pushing the limits of mathematical reasoning in open language models. arXiv:2402.03300. https://arxiv.org/abs/2402.03300
- Sutton, R. S., Precup, D., Singh, S. (1999). Between MDPs and semi-MDPs: a framework for temporal abstraction in reinforcement learning. Artificial Intelligence, 112(1–2), 181–211.
- Sygkounas, A., Hazra, R., Persson, A., Martires, P. Z. D., Loutfi, A. (2026). COvolve: adversarial co-evolution of large-language-model-generated policies and environments via two-player zero-sum game. arXiv:2603.28386. https://arxiv.org/abs/2603.28386
- Tan, Z., Abdullahi, M., Shi, T., Yuan, H., Xu, Z., Yu, C., Li, B., Zhao, B. (2025). EARL: efficient agentic reinforcement learning systems for large language models. arXiv:2510.05943. https://arxiv.org/abs/2510.05943
- Team, O. E. L., Stooke, A., Mahajan, A., Barros, C., Deck, C., Bauer, J., Sygnowski, J., Trebacz, M., Jaderberg, M., Mathieu, M., McAleese, N., Bradley-Schmieg, N., Wong, N., Porcel, N., Raileanu, R., Hughes-Fitt, S., Dalibard, V., Czarnecki, W. M. (2021). Open-ended learning leads to generally capable agents. arXiv:2107.12808. https://arxiv.org/abs/2107.12808
- Tencent Hunyuan (2026). Hy4 preview. https://hy.tencent.com/research/hy4-preview
- Touvron, H., et al. (2023). Llama 2: open foundation and fine-tuned chat models. arXiv:2307.09288. https://arxiv.org/abs/2307.09288
- Wang, R., Lehman, J., Clune, J., Stanley, K. O. (2019). Paired open-ended trailblazer (POET): endlessly generating increasingly complex and diverse learning environments and their solutions. arXiv:1901.01753. https://arxiv.org/abs/1901.01753
- Wang, R., Lehman, J., Rawal, A., Zhi, J., Li, Y., Clune, J., Stanley, K. O. (2020). Enhanced POET: open-ended reinforcement learning through unbounded invention of learning challenges and their solutions. arXiv:2003.08536. https://arxiv.org/abs/2003.08536
- Wang, X., Li, B., Song, Y., Xu, F. F., Tang, X., Zhuge, M., Pan, J., et al. (2025). OpenHands: an open platform for AI software developers as generalist agents. arXiv:2407.16741. https://arxiv.org/abs/2407.16741
- Wu, S., Li, Y., Song, Y., Zhang, W., Wang, Y., Batista-Navarro, R., Yang, X., Tang, M., Dai, B., Yang, J., Lin, C. (2026). Large-scale terminal agentic trajectory generation from dockerized environments. arXiv:2602.01244. https://arxiv.org/abs/2602.01244
- Yang, J., Jimenez, C. E., Wettig, A., Lieret, K., Yao, S., Narasimhan, K., Press, O. (2024). SWE-agent: agent-computer interfaces enable automated software engineering. arXiv:2405.15793. https://arxiv.org/abs/2405.15793
- Yang, S., Ma, Z., Huang, T., Hu, Y., Wang, Y., Chu, X. (2026). CoEvolve: training LLM agents via agent-data mutual evolution. In Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics, 23015–23036. https://aclanthology.org/2026.acl-long.1055/
- Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., Cao, Y. (2023). ReAct: synergizing reasoning and acting in language models. arXiv:2210.03629. https://arxiv.org/abs/2210.03629
- Yao, Y., Pang, B., Nguyen, X. P., Zhao, D., Joty, S., Yavuz, S. (2026). Learning generalizable behaviors for terminal agents. arXiv:2608.22631. https://arxiv.org/abs/2608.22631
- Zala, A., Cho, J., Lin, H., Yoon, J., Bansal, M. (2024). EnvGen: generating and adapting environments via LLMs for training embodied agents. arXiv:2403.12014. https://arxiv.org/abs/2403.12014
- Zhao, J., Lei, Z., Xi, Z., Zheng, R., Yan, H., Zhou, J., Chen, Q., He, L. (2026). NexForge: scaling agent capabilities through requirement-driven task synthesis for LLMs. arXiv:2607.14186. https://arxiv.org/abs/2607.14186

## 附录 A 版本说明

更多细节将在后续版本中提供。
