---
created: 2026-10-03
updated: 2026-10-03
title: AutoCompact：学习长程编程智能体中何时压缩上下文
sourceUrl: https://arxiv.org/abs/2610.02163
sourceAuthor: Xuan Zhang、Longtao Zheng、Cunxiao Du、Bo An、Xin Dong
translatedAt: 2026-10-03
sources: [references/articles.md 待处理队列]
tags: [上下文压缩, Context Compaction, 长程智能体, Long-Horizon Agents, 编程智能体, Coding Agents, AutoCompact, 上下文管理, 工作状态, 摘要自洽性, SFT, 强化学习, RL, GRPO, SWE-bench, SWE-PolyBench, type/翻译]
---

# AutoCompact：学习长程编程智能体中何时压缩上下文

> [arxiv.org/abs](https://arxiv.org/abs/2610.02163)｜分类：cs.CL（Computation and Language，计算与语言）
> 作者：Xuan Zhang†、Longtao Zheng、Cunxiao Du（Singapore Management University）、Bo An（Nanyang Technological University）、Xin Dong（Harvard University）；† 同等贡献
> 提交：2026-10-01（arXiv v1）｜许可：CC BY 4.0
> 原文：https://arxiv.org/abs/2610.02163｜PDF：https://arxiv.org/pdf/2610.02163

## 摘要

编码智能体通过代码查阅、搜索、编辑与测试的长轨迹来完成仓库级软件工程任务。随着任务推进，早期探索会逐渐失效，因此上下文管理不只是避免溢出：智能体必须决定何时压缩、要保留哪些工作状态，以及如何据此继续。我们提出 AutoCompact，训练编程智能体把这些决策纳入其策略。为收集训练数据，我们在编程任务上运行基础智能体，并用一个 judge（评审模型）审查其压缩决策、摘要以及压缩后的动作。有缺陷的输出会在环境中执行之前被替换为修正后的输出，使每条轨迹都从修正后的决策继续。我们用这些轨迹做监督微调（SFT），再通过以任务成功为奖励的强化学习（RL）联合优化编码与压缩。在 SWE-bench Verified 与 SWE-PolyBench Verified 上的实验表明，AutoCompact 相对基础模型的通过率分别绝对提升 9.2% 与 5.0%。该提升在所有评估的推理预算下都成立：在 256K 上下文窗口下从不溢出，在 16K 窗口下溢出会触发兜底压缩。

## 1 引言

大语言模型（LLM）智能体通过查阅代码、搜索仓库、编辑文件与运行测试，在仓库级软件工程任务上展现出很强的能力（Jimenez et al., 2024; Yang et al., 2024; Wang et al., 2025）。解决复杂问题往往需要考察多个候选原因，并在实现与验证之间反复迭代，因此轨迹会不断累积代码片段、工具输出与中间发现。随着智能体从任务的一个阶段进入下一个阶段，其中大量信息——例如探索性假设、失败尝试与冗长的工具输出——会变得陈旧（stale）。保留完整轨迹于是用过期细节填满上下文，而下一阶段其实只需要一份紧凑的**工作状态（working state）**：目前得出的结论、相关代码与工作区状态，以及剩余动作。因此，有效的上下文管理要求智能体决定*何时*压缩、*在工作状态中保留什么*信息，以及*如何*据此继续执行。

现有方法只解决了这一问题的一部分。长度触发式方法（length-triggered）如 CompactionRL（Li et al., 2026b）只在剩余上下文预算低于固定阈值时才压缩，这把压缩与上下文长度而非任务进度绑定在一起：陈旧的探索会一直累积到触发阈值，而压缩随后可能发生在一个尚未解决的阶段中途，而此时其证据仍然需要。主动式方法（proactive）则让智能体自己决定何时压缩，要么通过推理时的 rubric（Li et al., 2026a），要么通过在离线插入压缩调用后的轨迹上微调（Liu et al., 2026）。然而，决定何时压缩并不足够：工作状态可能遗漏或错误表述关键信息；即便它准确，智能体也可能不遵循它，重新翻出已完成的探索或忽略预期的下一步动作。这两类主动式方法都没有解决这些失效：rubric 不提供任何训练信号，离线插入则在每次插入调用后保留原始动作。

我们提出 AutoCompact，训练编程智能体把何时压缩、保留什么以及如何继续，作为其策略的一部分。为收集训练数据，我们在训练任务上运行基础智能体，并用 judge 审查其压缩决策、它写出的摘要以及压缩后的动作。judge 会在环境中执行之前，把有缺陷的输出替换为修正后的输出，使每条轨迹都从修正后的决策继续，并展示出压缩后应如何行动。我们用这些轨迹做监督微调（SFT），然后应用基于结果的强化学习（RL），仅以二值化的任务成功作为奖励信号，联合优化编码与压缩。

我们在 SWE-bench Verified（Jimenez et al., 2024; OpenAI, 2024）与 SWE-PolyBench Verified（Rashid et al., 2025）上评估 AutoCompact，分别取得 39.6% 与 24.5% 的通过率，相对基础模型提升 9.2% 与 5.0%。我们进一步在 SWE-bench Verified 上考察两种互补上下文机制下的成本效率：一种 256K 设置，其中没有轨迹触及强制压缩阈值；以及一种受限的 16K 设置，其中所有方法共享同一个长度触发的兜底机制。训练后的策略在所有评估预算（每任务 $0.10 至 $4.00）下均稳定提升性能，而基于结果的 RL 相对 SFT 进一步带来增益，在低预算下尤为明显。把同一个训练后的检查点在执行与不执行压缩两种情况下比较，进一步表明压缩在紧张的推理预算下尤其有益，印证了它对高效任务完成的贡献。

图 1：长度触发式压缩与 AutoCompact 的对比。在长度触发式压缩下，智能体在 bug 被定位之后仍持续累积上下文，例如反复进行带长输出的搜索，直到触及上下文上限才做摘要。AutoCompact 让模型自行决定 (1) 何时压缩、(2) 保留什么——把有用的发现改写成一份工作状态摘要，同时丢弃陈旧的探索，以及 (3) 如何据此继续。

## 2 方法

AutoCompact 为编程智能体配备一个 `compact()` 动作（§2.1），并分两阶段训练策略。我们首先收集带 judge 引导修正的同策略（on-policy）轨迹，修正对象是压缩时机、生成的工作状态以及紧随压缩之后的动作（§2.2）。这些修正后的轨迹为 SFT 提供训练数据。然后我们应用基于结果的 RL，以最终任务成功为奖励联合优化编码与压缩（§2.3）。

### 2.1 主动上下文压缩

图 2：judge 引导的同策略数据收集。每一步，judge 只依据当前执行历史审查策略的提议。有用的探索被保留，而修正针对三件事：(1) 何时压缩，例如在 bug 已被定位后把一次搜索替换为 `compact()`；(2) 保留什么，例如修复一个遗漏了目标文件的摘要；(3) 如何继续，例如把一次重复搜索重定向到摘要中计划好的编辑。环境执行修正后的输出，由此得到的轨迹用于监督 SFT；训练后的智能体不需要 judge。

我们为智能体增加一个可在执行过程中主动调用的 `compact()` 动作。除此之外，智能体照常运行：查阅文件、编辑代码、运行测试。当它判断当前阶段已被充分解决、累积的历史可以被摘要时，就可以在触及上下文上限之前调用 `compact()`。例如，智能体可以在定位到问题根因之后、进入实现之前进行压缩。

压缩会用一份由模型生成的工作状态摘要替换此前的交互历史，该摘要以 `# Auto Context Summary` 为标题，同时保持原始任务不变。摘要旨在保留已确立的发现、相关的代码与工作区状态，以及剩余动作，同时省略先前探索中不必要的细节。智能体随后从压缩后的上下文继续执行，如图 1 所示。

该机制让压缩成为模型的一项决策，而不再只是对上下文窗口压力的被动响应。因此它的有效性取决于三种行为：选择合适的压缩点、构造准确的工作状态，以及可靠地从该状态继续。接下来我们描述如何通过 judge 引导的同策略数据收集来监督这三种行为。

### 2.2 Judge 引导的数据收集与 SFT

仅靠提示无法诱发主动压缩。在我们的初步实验中，即便在智能体提示词中明确写入压缩规则，基础模型也很少在触及上下文上限之前调用 `compact()`。主动压缩引入了一种基础策略中并不常见的行为：模型必须打断一条本来有效的执行轨迹，并在任何上下文长度约束迫使它这么做之前替换已累积的上下文。因此，我们用在线 judge 修正来收集训练轨迹，并用于 SFT。这些修正提供了基础策略自身很少产生的压缩及其后续执行的示范。judge 只在数据收集阶段使用；训练后的智能体在推理时不需要 judge。

为收集这类示范，我们在软件工程任务上展开（roll out）基础策略，并在执行推进的过程中用 judge 审查每一个提议的动作。judge 只接收当前步骤可用的轨迹历史，并按照预先定义的标注协议判断所提议的动作是否令人满意；该协议规定了合适的压缩点、压缩后工作状态中应保留的信息，以及压缩后的行为应如何继续。图 2 给出了这一在线纠正数据收集过程的概览，并针对下一段描述的三种修正各给出一个具体例子。

我们监督与压缩主要失效模式相对应的三类决策。**触发修正（trigger correction）**检查当前点是否适合压缩：当当前阶段已被充分解决时智能体应当压缩，但当中间证据仍然需要时应继续探索。**工作状态修正（working-state correction）**检查生成的 `# Auto Context Summary` 是否准确保留了后续执行所需的信息，包括相关结论、代码与工作区状态，以及剩余动作。**继续修正（continuation correction）**检查压缩后的第一批动作是否遵循了所得的工作状态，而不是重新翻出已完成的探索或忽略预期的下一步——例如重新运行一次其结果已经记录在工作状态摘要中的搜索。

修正会在执行之前生效，因此每一次修正都会塑造轨迹的其余部分。当 judge 判定某个输出不令人满意时，它会写出一个修正输出，环境用该修正输出来替代原始输出执行；策略随后从这段修正后的历史生成后续动作。这与事后标注不同——在事后标注中，修正不会影响后续状态。

最后，我们用标准的下一 token 预测目标在修正后的轨迹上微调基础策略。由此得到的策略 AutoCompact-SFT 既学习普通的编码行为，也学习上文引入的三种压缩行为：选择合适的压缩点、构造可执行的工作状态，以及在此之后可靠地继续执行。SFT 为主动压缩提供了行为初始化，但它优化的是被局部修正的决策，而不是这些决策对任务完成的最终影响。我们随后用基于结果的 RL 进一步优化策略，直接以任务成功为目标。

### 2.3 面向任务求解与压缩的联合 RL

从 SFT 检查点出发，我们用端到端多轮 RL（Xue et al., 2026）在 SWE-Gym（Pan et al., 2025）上继续训练智能体，采用组相对策略优化（GRPO）（Shao et al., 2024）与一套完全异步的 RL 系统。每条 rollout 根据最终 patch 是否通过任务测试获得一个二值结果奖励。在每个 rollout 组内，GRPO 把这些结果转化为相对优势（advantage），为一条轨迹中所有由模型生成的 token 提供共享的学习信号，包括常规编码动作、调用 `compact()` 的决策、生成的上文摘要以及压缩后的继续执行。

因此，压缩既不需要单独的辅助目标，也不需要压缩专用的奖励整形。相反，任务求解与上下文管理在最终任务奖励下被联合训练，使策略学会何时压缩有益、应保留哪些信息，以及此后应如何继续执行。

压缩还改变了轨迹被转换为训练序列的方式，因为每次调用 `compact()` 都会重写上下文。这样一来，含压缩的轨迹不再构成一条"每一模型轮次都扩展前文上下文"的单一序列。因此，我们在上下文前缀被重写处把每条轨迹切分为若干段（segment），使得在每一段内，每个模型轮次所条件化的前缀只增不减。一条轨迹的所有段共享该轨迹的优势，因此压缩决策、摘要与压缩后的动作即便落在不同段中，也接收到相同的基于结果的信号。策略损失在一个批次内对所有段按 token 级求平均，不使用 KL 惩罚，也不使用熵奖励，因此二值结果奖励是编码与压缩唯一的训练信号。

## 3 实验

我们的实验回答三个问题。第一，AutoCompact 相对全历史执行以及既有的长度触发式与主动式压缩方法，是否提升了任务成功率（§3.2）？第二，主动压缩、基于结果的 RL 以及压缩的执行本身，在不同推理预算与上下文设置下分别贡献了什么（§3.3）？第三，SFT 之后与 RL 之后产生的摘要有何不同（§3.4）？

### 3.1 实验设置

**模型与脚手架。** 我们在全部实验中使用 Qwen3-Coder-30B-A3B-Instruct（Yang et al., 2025a）作为基础模型，并在两个仓库级软件工程基准上评估所有模型变体：SWE-bench Verified（Jimenez et al., 2024; OpenAI, 2024）与 SWE-PolyBench Verified（Rashid et al., 2025）。所有变体使用相同的基于终端的 read-eval-print loop（REPL）脚手架（Lin and Liu, 2025; Du et al., 2025），并加装 §2.1 中描述的模型可调用的 `compact()` 动作。在监督数据收集期间，我们额外使用 GPT-5.5-Codex 作为在线修正的 judge；评测时移除 judge。

**训练。** 在 SFT 阶段，我们在 379 个 SWE-rebench 任务（Badertdinov et al., 2025）上展开基础模型，按照 §2.2 的流程收集了 1,052 条 judge 修正轨迹，其间过滤掉了格式错误的请求、摘要循环与偏离轨道的续写。在这些轨迹中，24% 监督压缩触发，53% 监督工作状态构造，23% 监督压缩后的继续执行。我们训练两个 epoch，学习率为 5×10⁻⁷，批大小为 8。从 AutoCompact-SFT 出发，我们进一步用 GRPO 在 SWE-Gym（Pan et al., 2025）上优化策略。对每个任务采样 8 条轨迹，并根据最终 patch 是否通过该任务专属测试套件赋予一个二值结果奖励。RL 使用 1×10⁻⁶ 的学习率与 64 的批大小，rollout 上限为 50 个环境步与 32K token。

**评测。** 我们报告在不设推理成本上限的完整智能体运行下 SWE-bench Verified 与 SWE-PolyBench Verified 的通过率。所有报告的定量评测结果均为三次运行的平均。为评估成本效率，我们额外在每任务 $0.10 至 $4.00 的六个推理预算下评估 SWE-bench Verified（图 3）。当一条 rollout 的累计推理成本达到指定预算时即被终止。我们依据 Qwen3-Coder-30B-A3B-Instruct 在阿里云百炼（Alibaba Cloud Model Studio）的官方定价（Alibaba Cloud, 2026）从 token 用量估算推理成本。为计入前缀缓存，我们把缓存 token 定价为标准输入 token 费率的 20%，遵循阿里云百炼的隐式缓存定价，而未缓存输入 token 与输出 token 则按其各自的标准费率计价。

表 1：不设推理成本上限的完整运行通过率，按压缩触发方式分组。所有方法共享同一基础模型与脚手架。在 Context 列中，256K 表示模型上下文窗口，† 表示 16K 强制压缩阈值。

| **方法** | **触发** | **优化** | **上下文** | **SWE-bench Verified (%)** | **SWE-PolyBench Verified (%)** |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |
| **Full-history baseline（全历史基线）** |
| Base | — | — | 256K | 30.4 | 19.5 |
| **Length-triggered compaction（长度触发式压缩）** |
| Fixed Compaction | Length | — | 16K† | 28.8 | 18.6 |
| CompactionRL（Li et al., 2026b） | Length | RL | 16K† | 32.7 | 19.8 |
| **Proactive compaction（主动式压缩）** |
| SelfCompact（Li et al., 2026a） | Rubric | — | 256K | 31.7 | 20.6 |
| SWE-Compressor（Liu et al., 2026） | Learned | SFT | 256K | 31.0 | 20.1 |
| AutoCompact-SFT | Learned | SFT | 256K | 32.2 | 21.7 |
| AutoCompact | Learned | SFT → RL | 256K | **39.6** | **24.5** |

**基线。** 我们把 AutoCompact 与若干上下文管理策略比较。Base 使用相同的基础模型与脚手架，但不具备学习到的主动压缩。Fixed Compaction 在剩余上下文预算低于预设阈值时触发压缩。SelfCompact（Li et al., 2026a）使用推理时的 rubric 来引导压缩决策，而 CompactionRL（Li et al., 2026b）在长度触发式压缩机制下联合训练任务执行与摘要生成。SWE-Compressor（Liu et al., 2026）通过对离线插入压缩调用后重建的轨迹做监督微调，学会调用一个上下文管理工具。对于这一 SFT 对比，我们从可比的 SWE-rebench 任务集中收集轨迹，并为 SWE-Compressor 与 AutoCompact-SFT 使用相近数量的训练轨迹。与这些基线不同，AutoCompact 在数据收集期间修正智能体自身的压缩决策与后续动作，直接监督智能体如何使用压缩后的状态。

### 3.2 主要结果

图 3：SWE-bench Verified 上通过率随推理预算的变化。(a) 256K 下 AutoCompact-SFT 对 Base，其中没有轨迹触及强制压缩阈值。(b) 256K 下 AutoCompact（RL 之后）对 AutoCompact-SFT。(c) 16K 下 AutoCompact 对 Base，二者共享强制压缩兜底。(d) 同一检查点在遵循摘要与忽略摘要两种情况下的对比。预算档位等距划分；增益表示每 500 道任务中额外解决的任务数。

如表 1 所示，AutoCompact 在两个基准上都取得最高的完整运行通过率，相对 Base 在 SWE-bench Verified 上提升 9.2%，在 SWE-PolyBench Verified 上提升 5.0%。

**长度触发式压缩增益有限。** Fixed Compaction 在两个基准上分别低于 Base 1.6% 与 0.9%，表明在这种受限上下文设置下存在性能代价。CompactionRL 通过 RL 相对 Fixed Compaction 提升 3.9% 与 1.2%。然而，它相对 Base 的增益仍然有限，与 AutoCompact 之间仍有很大差距。

**主动式压缩优于全历史执行。** 在 256K 设置下，所有被评估的主动方法——包括 SelfCompact、SWE-Compressor 以及两个 AutoCompact 变体——在两个基准上都优于 Base。SelfCompact 仅凭推理时引导就取得提升，而 SWE-Compressor 通过 SFT 学会了压缩工具的使用。这些结果表明，即便完整历史能装进上下文，主动式上下文管理也有帮助。

**在线 judge 引导的 SFT 与基于结果的 RL 都带来增益。** AutoCompact-SFT 在两个基准上分别比 SWE-Compressor 高 1.2% 与 1.6%。由于二者使用相同的基础模型、脚手架与可比的训练数据，这一对比表明在线 judge 引导的修正比离线插入到已完成轨迹中更有效。AutoCompact-SFT 学习的轨迹中，修正后的输出（包括压缩后的修正动作）确实被执行过；而 SWE-Compressor 把压缩调用插入到已完成轨迹里，并保留其原有的后续动作。基于结果的 RL 随后在两个基准上又相对 AutoCompact-SFT 把通过率分别提升 7.4% 与 2.8%。

### 3.3 进一步分析

**主动式压缩在上下文溢出之前就有帮助。** 我们首先在 256K 长上下文设置下比较 Base 与 AutoCompact-SFT。由于没有轨迹触及强制压缩阈值，这一比较检验的是：当完整交互历史能装进上下文窗口时，为主动压缩而做的监督训练是否仍能提升智能体性能。如图 3(a) 所示，AutoCompact-SFT 在所有评估的推理预算下通过率都高于 Base。这一结果表明，即便上下文窗口足够大，保留完整交互历史也不一定最优。在长轨迹中，过时的假设、失败的尝试与冗长的工具输出会不断累积，使模型偏离当前的工作状态。通过用一份精炼的工作状态替换陈旧的上下文，AutoCompact-SFT 在上下文成为瓶颈之前就提升了性能。

**基于结果的 RL 超越了监督模仿。** 在同样的 256K 协议下，我们比较 AutoCompact-SFT 与 AutoCompact。如图 3(b) 所示，AutoCompact 在所有推理预算下都持续优于 AutoCompact-SFT，且增益在低预算区间最大。这些结果表明，SFT 建立了基本的压缩行为，而基于结果的 RL 进一步改进了如何利用这一行为来最大化任务成功。由于低预算会提前截断 rollout，这些预算下更大的增益说明 RL 让智能体更具成本效率，而不仅仅是依赖更长的轨迹。

图 4：压缩行为，其中 (1)、(2)、(3) 分别标记何时压缩、保留什么与如何继续（图 1）。(a) 模型主动调用 `compact()` 的任务比例。(b) 遗漏相关任务或工作区状态的摘要比例。(c) 遗漏具体下一步动作的摘要比例。(b) 与 (c) 中越低越好。

**RL 无需压缩专用奖励即可改善压缩行为。** 图 4 比较了 RL 前后的压缩行为。Base 极少调用 `compact()`，而 AutoCompact-SFT 已在 44.3% 的任务上使用它，说明监督训练建立了基本行为。RL 把使用率扩展到 58.5% 的任务，同时降低了两种摘要遗漏：关键状态遗漏从 3.1% 降至 0.2%，下一步动作遗漏从 8.2% 降至 2.2%。这些统计是在全部 500 道 SWE-bench Verified 任务的轨迹上、用基于关键词的筛查计算得到的，并用随机人工抽查加以补充。这两个趋势互补：压缩被用于更多任务，同时却有更少的摘要被标记为缺失状态或下一步信息。这表明任务成功奖励鼓励智能体保留从压缩状态继续任务所需的信息。

**主动式压缩与长度触发兜底互补。** 我们在共享的 16K 强制压缩阈值下评估 Base 与 AutoCompact。这一设置代表一种受上下文约束的运行时：两套系统都用强制压缩作为兜底，而 AutoCompact 还可以在触及阈值之前主动调用 `compact()`。如图 3(c) 所示，AutoCompact 在所有评估的推理预算下通过率都高于 Base。这一结果表明，学习到的主动式上下文管理在与长度触发兜底一起部署时仍然有效，让智能体能够在压缩变为强制之前重组其上下文。它也说明，基于任务进度的压缩比仅基于上下文长度的压缩更有效。

**压缩本身对训练后智能体的增益有贡献。** AutoCompact 的增益可能同时反映了训练中学到的更好的智能体行为，以及推理时对压缩的使用。为评估后者的贡献，我们把正常执行与同一个训练后检查点的"忽略摘要"（Summary-ignored）变体比较。在该变体中，`compact()` 调用被跳过：不生成摘要，执行沿用既有历史继续。两种条件都保留全部已学参数，使我们能够检验执行压缩是否带来了超出这些参数所编码改进之外的收益。图 3(d) 显示正常执行取得更高的通过率，且在紧张的推理预算下优势最大。这表明所观察到的增益不能仅归因于训练中学到的更好的智能体行为：部分收益依赖于真正执行压缩。该优势在 $0.10 预算下为 19.9%，到 $4.00 时仍保持 1.9%，因此执行压缩在不降低最终性能的前提下提升了成本效率。

### 3.4 案例研究：SFT 与 RL 下的摘要自洽性

保留相关状态并给出下一步动作，本身并不足以让一份摘要可用。图 4 中的摘要内容指标对二者都做了检查，然而一份摘要可以在满足这些指标的同时，提出一个与其所记录状态不相容的下一步动作，从而违背我们所说的**摘要自洽性（summary self-consistency）**。图 5 通过同一个 SWE-bench Verified 任务上来自 AutoCompact-SFT 与 AutoCompact 的改写摘要，展示了这一差距。

图 5：SWE-bench Verified 任务 `django-13809` 上的摘要自洽性。这一质性例子对比了来自 AutoCompact-SFT 与 AutoCompact 的改写摘要及其最终评测结果。每份摘要都记录了一个状态并提出了一个下一步动作；两者之间的标记表示该动作是否与所记录的状态一致。

图 5 中的两份摘要恰恰在这一方面有所不同。AutoCompact-SFT 的摘要记录了一个未解决的语法错误，却仍提议不再做进一步动作就收尾：错误被保留在摘要里，却未能约束所提议的续写。相反，AutoCompact 的摘要报告参数与条件逻辑的修改已经完成，并提议在提交之前进行验证。这一下一步与所记录的实现状态一致。相应的 AutoCompact-SFT 运行在评测中因 `SyntaxError` 失败，而 AutoCompact 运行通过了测试并解决了任务。

这一对比凸显了摘要自洽性是超越信息覆盖度的一个摘要质量维度。这种差异可能源于训练目标：SFT 模仿示范摘要，这并不保证所记录的状态会约束下一步动作；而 RL 仅通过摘要之后那些动作的成功来奖励摘要。

## 4 相关工作

**编程智能体。** 仓库级编程研究通过脚手架设计与模型训练两条路径提升任务求解能力。脚手架设计方面的工作通过智能体-计算机接口、工具执行环境与结构化修复流程来组织仓库探索、代码编辑与验证（Yang et al., 2024; Wang et al., 2025; Xia et al., 2025）。模型训练方面的工作通过可执行任务环境、扩大的任务与轨迹数据集，以及监督或强化学习来提升编码与问题求解能力（Pan et al., 2025; Yang et al., 2025b; Wei et al., 2025）。AutoCompact 把二者结合为模型-脚手架协同设计（model-harness co-design）：脚手架暴露一个 `compact()` 动作，而模型学会把它与任务执行联合使用，而不是通过一个独立的压缩模块。

**记忆与上下文管理。** 长程智能体通过记忆层级（Packer et al., 2023）、原始观测的抽象（Zheng et al., 2024）、对累积观测与交互的摘要（Kang et al., 2026; Wu et al., 2025; Liu et al., 2026），或对子轨迹与选定历史片段的压缩（Sun et al., 2025; Ye et al., 2025; Gao et al., 2026）来管理不断增长的交互历史。这些工作主要设计保留的上下文如何表示。AutoCompact 采用一种简单的表示——一份工作状态摘要，与原始任务及近期轮次并列——并把重点放在何时压缩以及压缩后如何继续。

**学习上下文管理策略。** 基于 rubric 与指南的方法（Li et al., 2026a; Kang et al., 2026）通过指令引导压缩，而不是训练智能体自身的压缩行为。监督式方法从构造的轨迹中学习（Liu et al., 2026; Ye et al., 2025; Gao et al., 2026），例如把上下文管理动作插入已完成轨迹（Liu et al., 2026），这会保留每次插入之后的原始动作；或如并发工作 SWE-MeM（Gao et al., 2026）那样合成轨迹，其中由更强的模型决定何时压缩一段步骤并写出摘要，但不生成任务动作。RL 方法（Wu et al., 2025; Sun et al., 2025; Li et al., 2026b; Gao et al., 2026）通过奖励优化上下文管理——SWE-MeM 还额外使用步级掩码处理记忆管理失败——但不直接监督压缩之后的行为。与这些方法不同，AutoCompact 在数据收集期间修正智能体自身的压缩决策、摘要与后续动作，执行修正后的输出，并仅用基于结果的 RL 精化这一行为。

## 5 结论

AutoCompact 训练编程智能体把上下文管理作为任务执行的一部分。judge 修正的轨迹为压缩决策、摘要构造以及压缩后的动作提供监督，随后用基于结果的强化学习联合优化编码与压缩。在 SWE-bench Verified 与 SWE-PolyBench Verified 上的实验表明，任务成功率在所有评估的推理预算下均有提升；而忽略同一个训练模型的压缩调用会降低通过率，说明增益并非仅来自训练本身。这些发现凸显了不仅在压缩状态的构造上、也在智能体从这些状态出发的行为上进行训练的价值——而后者是既有方法未加监督的。

**局限与未来工作。** 受资源约束，RL 训练使用 32K token 的序列，短于评测所用的 256K 上下文窗口。尽管如此，在 256K 与 16K 两种设置下、所有评估预算上的增益都表明，这一训练设置已足以学到有用的主动压缩。更广泛地说，AutoCompact 是一种模型-脚手架协同设计：脚手架提供压缩机制，而模型学习何时调用它、保留什么以及此后如何继续。我们在单一脚手架内研究这种协同设计。当前广泛使用的智能体脚手架（如 Codex 与 Claude Code）会在上下文接近窗口上限时自动压缩，这正是 §1 讨论的长度触发式设计。我们的 16K 结果提示，把这类机制与学习到的主动压缩结合起来，可能进一步改进这些系统，我们将其留作未来工作。

### AI 使用声明

在本工作中，我们使用生成式 AI 工具进行语言编辑与训练用的轨迹修正。我们已审阅所有由 AI 辅助的工作，并对本工作的最终内容（包括借助生成式 AI 产出的文本、论断或产物）承担责任。

## 参考文献

- Alibaba Cloud (2026). Alibaba Cloud Model Studio: model inference pricing. https://www.alibabacloud.com/help/en/model-studio/model-pricing
- Badertdinov, I., Golubev, A., Nekrashevich, M., Shevtsov, A., Karasik, S., Andriushchenko, A., Trofimova, M., Litvintseva, D., and Yangel, B. (2025). SWE-rebench: an automated pipeline for task collection and decontaminated evaluation of software engineering agents. In Advances in Neural Information Processing Systems.
- Du, C., Wang, T., Dou, L., Li, S., Zhang, T., Liu, T., Chen, X., and Lin, M. (2025). On policy annotation: how minimal human edits unlock massive gains in LLM agents. Blog post. https://terminal-agent.github.io/blog/annotation/
- Gao, S., Zeng, W., Yu, Z., Wangni, J., Wang, C., Cai, K., He, S., and Lyu, M. R. (2026). SWE-MeM: learning adaptive memory management for long-horizon coding agents. arXiv preprint arXiv:2606.28434.
- Jimenez, C. E., Yang, J., Wettig, A., Yao, S., Pei, K., Press, O., and Narasimhan, K. (2024). SWE-bench: can language models resolve real-world GitHub issues? In International Conference on Learning Representations.
- Kang, M., Chen, W., Han, D., Inan, H. A., Wutschitz, L., Chen, Y., Sim, R., and Rajmohan, S. (2026). ACON: optimizing context compression for long-horizon LLM agents. In Proceedings of the 43rd International Conference on Machine Learning.
- Li, T., Zhang, J., Jurayj, W., Wang, X., Jin, C., Farajtabar, M., Nalisnick, E., and Khashabi, D. (2026a). Self-compacting language model agents. arXiv preprint arXiv:2606.23525.
- Li, Y., Hou, Z., Jing, Y., Tang, J., and Dong, Y. (2026b). CompactionRL: reinforcement learning with context compaction for long-horizon agents. arXiv preprint arXiv:2607.05378.
- Lin, M. and Liu, Z. (2025). Terminal: LLM's last tool. Blog post. https://terminal-agent.github.io/blog/tool/
- Liu, S., Jiang, B., Yang, J., Li, Y., Guo, J., Liu, X., and Dai, B. (2026). Context as a tool: context management for long-horizon SWE-agents. In Findings of the Association for Computational Linguistics: ACL 2026.
- OpenAI (2024). Introducing SWE-bench verified. https://openai.com/index/introducing-swe-bench-verified/
- Packer, C., Wooders, S., Lin, K., Fang, V., Patil, S. G., Stoica, I., and Gonzalez, J. E. (2023). MemGPT: towards LLMs as operating systems. arXiv preprint arXiv:2310.08560.
- Pan, J., Wang, X., Neubig, G., Jaitly, N., Ji, H., Suhr, A., and Zhang, Y. (2025). Training software engineering agents and verifiers with SWE-Gym. In Proceedings of the 42nd International Conference on Machine Learning.
- Rashid, M. S., Bock, C., Zhuang, Y., Buchholz, A., Esler, T., Valentin, S., Franceschi, L., Wistuba, M., Sivaprasad, P. T., Kim, W. J., et al. (2025). SWE-PolyBench: a multi-language benchmark for repository level evaluation of coding agents. arXiv preprint arXiv:2504.08703.
- Shao, Z., Wang, P., Zhu, Q., Xu, R., Song, J., Bi, X., Zhang, H., Zhang, M., Li, Y. K., Wu, Y., and Guo, D. (2024). DeepSeekMath: pushing the limits of mathematical reasoning in open language models. arXiv preprint arXiv:2402.03300.
- Sun, W., Lu, M., Ling, Z., Liu, K., Yao, X., Yang, Y., and Chen, J. (2025). Scaling long-horizon LLM agent via Context-Folding. arXiv preprint arXiv:2510.11967.
- Wang, X., Li, B., Song, Y., Xu, F. F., Tang, X., Zhuge, M., Pan, J., Song, Y., Li, B., Singh, J., et al. (2025). OpenHands: an open platform for AI software developers as generalist agents. In International Conference on Learning Representations.
- Wei, Y., Duchenne, O., Copet, J., Carbonneaux, Q., Zhang, L., Fried, D., Synnaeve, G., Singh, R., and Wang, S. I. (2025). SWE-RL: advancing LLM reasoning via reinforcement learning on open software evolution. In Advances in Neural Information Processing Systems.
- Wu, X., Li, K., Zhao, Y., Zhang, L., Ou, L., Yin, H., Zhang, Z., Yu, X., Zhang, D., Jiang, Y., et al. (2025). ReSum: unlocking long-horizon search intelligence via context summarization. arXiv preprint arXiv:2509.13313.
- Xia, C. S., Deng, Y., Dunn, S., and Zhang, L. (2025). Demystifying LLM-based software engineering agents. Proceedings of the ACM on Software Engineering 2 (FSE), pp. 801–824.
- Xue, Z., Zheng, L., Liu, Q., Li, Y., Zheng, X., Ma, Z., and An, B. (2026). SimpleTIR: end-to-end reinforcement learning for multi-turn tool-integrated reasoning. In International Conference on Learning Representations.
- Yang, A., Li, A., Yang, B., Zhang, B., Hui, B., Zheng, B., Yu, B., Gao, C., Huang, C., Lv, C., et al. (2025a). Qwen3 technical report. arXiv preprint arXiv:2505.09388.
- Yang, J., Jimenez, C. E., Wettig, A., Lieret, K., Yao, S., Narasimhan, K., and Press, O. (2024). SWE-agent: agent-computer interfaces enable automated software engineering. In Advances in Neural Information Processing Systems.
- Yang, J., Lieret, K., Jimenez, C. E., Wettig, A., Khandpur, K., Zhang, Y., Hui, B., Press, O., Schmidt, L., and Yang, D. (2025b). SWE-smith: scaling data for software engineering agents. In Advances in Neural Information Processing Systems.
- Ye, R., Zhang, Z., Li, K., Yin, H., Tao, Z., Zhao, Y., Su, L., Zhang, L., Qiao, Z., Wang, X., et al. (2025). AgentFold: long-horizon web agents with proactive context management. arXiv preprint arXiv:2510.24699.
- Zheng, L., Wang, R., Wang, X., and An, B. (2024). Synapse: trajectory-as-exemplar prompting with memory for computer control. In International Conference on Learning Representations.
