---
created: 2026-10-03
updated: 2026-10-03
title: 通过人机交互实现高效的测试时适配
sourceUrl: http://arxiv.org/abs/2609.04141v1
sourceAuthor: Zora Zhiruo Wang、Apurva Gandhi、Rulin Shao 等 25 位（卡内基梅隆大学、华盛顿大学、Handshake AI、斯坦福大学、普林斯顿大学、加州大学圣地亚哥分校）
translatedAt: 2026-10-03
sources: [references/articles.md 待处理队列]
tags: [测试时适配, TAHI, 人机交互, 智能体适配, 上下文适配, 权重适配, DPO, LoRA, 评分细则, rubric, 个性化, 人类反馈, 数据可视化, 学术写作, 泛化, type/翻译]
---

# 通过人机交互实现高效的测试时适配

> [arxiv.org/abs](http://arxiv.org/abs/2609.04141v1)｜分类：cs.AI（人工智能）
> 作者：Zora Zhiruo Wang、Apurva Gandhi、Rulin Shao、Aspen Chen、Jonas Mueller、Zhiqi Liang、Jett Chen、Michael Ryan、Qianou Ma、Luxi He、Zhoujun Cheng、Andre He、Seungone Kim、Jiayi Geng、Mingqian Zheng、Weiwei Sun、Zheyuan Zhang、Xinran Zhao、Yike Wang、Abe Hou、Liwei Jiang、Pang Wei Koh、Diyi Yang、Graham Neubig、Daniel Fried
> 机构：卡内基梅隆大学、华盛顿大学、Handshake AI、斯坦福大学、普林斯顿大学、加州大学圣地亚哥分校｜通讯：zhiruow@cs.cmu.edu
> 提交：2026-09-03（arXiv v1）｜许可：CC BY-SA 4.0
> 原文：http://arxiv.org/abs/2609.04141v1｜DOI：https://doi.org/10.48550/arXiv.2609.04141

## 摘要

基于大语言模型（LLM）的智能体是在群体规模的数据上训练的，从而编码了横跨众多从业者的广泛能力。然而，它们产出的成果很少能达到专业人士用来为自己的声誉背书所需的个人标准。在成功标准异质且文档不足的真实、开放式任务上，个人专长恰恰存在于对平均水平的提升与偏离之中。在实践中，迭代式的人机交互会浮现出用户无法预先完整说明、却会在任务之间反复应用的标准。我们认为，这种跨会话的交互数据是一种丰富但未被充分利用的信号，可用于弥合与个人专长之间的差距。在本工作中，我们提出通过人机交互的测试时适配（test-time adaptation through human-agent interaction, TAHI），它把这些信号整合进智能体的上下文与权重，并通过一个持续演化的评分细则（rubric）模块，把每个用户的训练与评估标准固化下来。我们在写作与视觉创作这两个高价值领域，将智能体适配到 30 位个体、共计 600 个任务上。我们的智能体仅在数十个任务内就把单人任务成功率提升了 4.5–20.9%。同时，我们持续演化的评分细则模块充当一种可扩展的标注工具，所创建的评估细则相比单纯由语言模型或人类创建的细则能多捕捉 16.0–22.3% 的失败。虽然智能体是针对个体适配的，但我们表明这些个性化智能体还能带来最高 8.8% 的成功率提升，并且可以跨用户泛化。

## 1 引言

基于大语言模型（LLM）的智能体已迅速成熟为能力出众的通用型系统，在写作、软件工程 [Wang et al., 2025d] 以及越来越多职业任务 [Patwardhan et al., 2026] 上都能产出合理的成果。然而，这种通用能力在若干显著方面仍达不到专家标准：把回答压平为同质化 [Jiang et al., 2026]，或偏离用户原本的观点 [Abdulhai et al., 2026]，由此得到的结果很少能达到让专业人士无需进一步迭代编辑即可直接使用的门槛。

人类专长，尤其是历经多年领域经验积累下来的隐性实践与判断，只能被用于训练基础语言模型的群体规模文本语料部分地捕获 [Gobet, 1998]。一个模型必然会学到横跨众多从业者的广泛能力，但一位个体专业人士需要的，是能够提升并偏离群体平均水平的特定知识、判断与策略。这种张力在真实的开放式任务上只会更加尖锐——这类任务的成功标准多样且很少被完整记录 [Weidinger et al., 2025]，使得智能体能从已文档化的人类知识中学到的能力，与那些未被言说出的能力之间始终存在一道鸿沟。更复杂的是，专长本质上是个人化的，且可能在不同从业者之间相互冲突，从而形成一组很难由单个训练好的模型或默认的智能体框架同时满足的期望。要补上这最后一公里，就需要智能体在部署时、在运行中，即时地适配它们正在与之共事的个体 [Kojima et al., 2021; Hawkins et al., 2020]。此外，高效地做到这一点也很重要：要在用户的耐心被数十轮试错耗尽之前，用几次会话就收敛到用户偏好的工作方式 [Shaikh et al., 2025]。

然而，高效的测试时适配需要正确的学习信号。当智能体仅仅通过反思自己过去的尝试来改进时，在没有来自外部的新信号的情况下，进步会停滞 [Huang et al., 2024; Xu et al., 2024b]。往往需要许多轮人机交互，才能迭代到用户一开始无法完整说明的目标形态。这些信号中有许多会在任务会话之间反复出现 [Wang et al., 2025c]，但当前的智能体系统在与人类交互时大多未加以利用。恰恰是这种通过与智能体一同工作的过程积累起来的跨会话交互数据，为智能体提供了一种丰富却未被充分探索的学习信号。不同于一次性的纠正，我们设想的是一位人类导师与一个受训智能体在多轮任务会话中并肩工作，通过多个渠道持续提供手把手的建议。于是，挑战就在于如何收集这些交互流并把它们整合进智能体中。

为此，我们提出通过人机交互的测试时适配（TAHI）。在该框架中，人类交互信号以流式方式被处理：智能体基于先前的交互会话不断适配自身，以解决后续会话，逐步减少满足人类专家期望所需的交互量（图 2）。我们的智能体由一个可训练的骨干语言模型（Qwen3.6-35B）支撑，它以可编辑的上下文为条件，并配有一个提供多种人类交互渠道的界面（图 1）。值得注意的是，除了像现有框架那样使用人类文本反馈 [Song et al., 2026a]（我们的 Message 模块）之外，我们的界面还支持多种额外信号，包括计划调整（Plan）、验证规范（Rubrics）以及直接编辑以产出成果（Deliverables）；这使我们能够研究多样化人类信号的价值。

在收集人机交互数据的同时，TAHI 还为我们所评估的开放式任务支持测试时智能体适配与评分细则创建。其一，我们的智能体支持 (i) 上下文适配，通过归纳出事实性记忆与程序性技能，使用户能够方便地检查与修订智能体所学；(ii) 权重适配，通过在 LoRA 适配器 [Hu et al., 2022] 上使用直接偏好优化（Direct Preference Optimization, DPO）[Rafailov et al., 2023]，鼓励智能体生成人类引导的最终输出而非其初始输出，从而捕获更持久的行为变化，并避免上下文窗口过度膨胀。其二，我们嵌入了一个演化的验证器模块，它用 LLM 把人类活动固化为具体的评估标准，同时允许用户纠正任何看起来不准确之处。它充当一种可扩展的工具，用于标注可供智能体训练与评估的标准，并把用户从为开放式任务手写成功标准的负担中解放出来（§2）。

我们跨越两个 AI 广泛应用的领域——写作与视觉创作——将智能体分别适配到 30 位人类专家、共计 600 个任务上。在每个领域，我们收集 5 位人类与我们的智能体在三种情形下的交互数据：在线上下文适配、在线权重适配，以及离线（不适配）；每位人类总共完成 20 个任务。基于这些数据，我们发现：

- **智能体能有效且高效地适配到个体用户。** 在上下文适配与权重适配两种方式下，我们的智能体分别在单人任务成功率上取得 4.5–12.9% 与 4.5–20.9% 的显著提升，且仅用 20 个任务会话就高效完成。在额外的留出任务上，我们的上下文适配与权重适配智能体在与同一位人类绑定的评分细则上分别提升 3.2–6.6% 与 4.8–5.2%，表明具有很强的跨任务泛化能力（§3）。
- **我们演化的评分细则比单纯由 LLM 或人类创建的更全面。** LLM 生成的评分细则常常遗漏关键评估维度，而人类需要大量激励与训练才能避免同样的陷阱。相比之下，我们演化的评分细则在不完美的智能体解上能比由 LLM 乃至人类单独创建的评分细则多捕捉 16.0–22.3% 的失败（§4.1）。
- **我们分别适配的智能体在不同用户之间都能改进。** 我们的数据反映出，人类专长是共享的社区知识与个性化策略或偏好的组合。我们的智能体同时学到两者，在跨用户的共享与个人评分细则条目上分别取得 0.3–8.8% 与 6.2–19.6% 的提升（§4.2–§4.4）。

展望未来，我们设想这样一个未来：AI 智能体不是通用的，而是由它们所服务的个体塑造、并对这些个体负责的自适应工具。

## 2 通过人机交互实现高效的测试时适配

### 2.1 基础：人机交互

我们把该问题形式化为一次人机交互（human-agent interaction）[Cukurova, 2026]：给定由人类指定的任务，智能体采取动作来执行它，而人类在此过程中提供反馈与纠正。

**建模智能体与人类。** 我们定义参与任务会话的两方。首先是一个基于 LLM 的智能体 A，其策略为 πθA(·|c)，由语言模型 θ 参数化并以上下文 c 为条件。沿着两条在上下文中适配智能体的研究脉络，我们设计两个组件：(i) 存储事实性与偏好性知识的记忆（memory）[Xu et al., 2026]，以及 (ii) 存储程序性知识的技能（skills）[Wang et al., 2024; Anthropic, 2025]。由于我们的目标是让智能体适配人类，我们还显式地定义以策略 πH 行事的人类 H。

给定一个带有指令 q 的任务，双方都可以从各自的动作空间中采取动作，形成一条求解该任务的行动轨迹 τ=[(s0,o0,a0),(s1,o1,a1),⋯]。其中 si 表示共享的环境状态，oi 是行动方（智能体 A 或人类 H）的观测，ai 是被采取的动作。

对于智能体，我们采用同时适用于 GUI 与编码活动的通用动作空间。我们把编码智能体当作通用智能体，认为程序化动作涵盖了常见的计算机使用动作（如点击、滚动、输入），并且足以求解多样化的任务。

`𝒜^A = {message, file_create, file_edit, file_read, execute, plan}`

该动作空间赋予智能体以下能力：(1) 沟通（message）：通过消息呈现信息或请求澄清；(2) 文件操作（file_create、file_edit、file_read）：在环境中读取、创建或编辑文件；(3) 程序执行（execute）：执行程序脚本；以及 (4) 规划（plan）：创建并细化结构化的步骤分解，以及每一步的验证标准。

人类则在一个互补的动作空间内行动：

`𝒜^H = {message, file_edit, plan_edit, context_edit, verify, trigger}`

人类与智能体共享若干相似动作：(1) 沟通（message）：通过文本消息向智能体提供反馈或额外信息；(2) 文件操作（file_edit）：编辑智能体产出的成果；(3) 规划（plan_edit）：修改智能体提出的步骤分解与验证标准。同时，人类还被赋予更多用于监督和调整智能体的动作：(4) 验证（verify）：为验证标准提供通过/不通过信号；(5) 编辑智能体上下文（context_edit）：编辑记忆与技能文件中的文本内容；以及 (6) 智能体解精修（trigger）：标志人类活动结束，并触发智能体继续行动。

整个任务会话 τ 可被看作由智能体与人类交替进行的 J+1 个轮次，其中每个轮次本身是一条由一或多个动作组成、记为 τ*_* 的行动轨迹。形式化地，τ=[τ0H,τ0A,τ1H,τ1A,⋯,τJH,τJA]，其中 τ0H=[message(q)] 表示用户任务指令步骤，q 为指令文本。若用户不再跟进或采取进一步动作，我们即判定任务会话结束。如果 τJH 触发了又一轮智能体动作（即 τJH 的最后一个动作是 trigger），则 τJA 非空；否则 τJA=∅，表示用户在自己行动之后对解感到满意。

**为鼓励多样化人类信号而对智能体界面的改造。** 为了让人类用户能方便地表达多样化的信号、同时保持流畅的用户体验，我们在被广泛采用的开源 Agent Cowork（https://github.com/DevAgentForge/Open-Claude-Cowork）之上构建，并新增三个组件：

第一，初始任务规划（图 1，Plan）。我们要求智能体提出一个初始任务计划，显示在界面的 Plan 模块中，以便人类用户可以对其给出有针对性的反馈。具体来说，该规划动作把指令分解为多个步骤，每一步用一段文本描述 w^i 表示，并配有一个输出产物 f^i。针对每一步，我们设计了一个由 LM 支持的验证器模块，初始化一列自然语言验证标准 V^i={v_k^i}，用于判断 f^i 在多大程度上满足 w^i。我们允许用户通过调整界面中的 Plan、Files 与 Rubrics 模块来编辑步骤、文件与验证器。形式上，该动作可记为 a_{0,0}^A=plan(o_{0,0}^A)→{(w^i,f^i,V^i)}，其中 a_{0,0}^A 表示轨迹 τ0A=[(s_{0,0}^A,o_{0,0}^A,a_{0,0}^A),⋯] 中首个智能体轮次里采取的第一个动作。由于用户主要与最后一步产生的文件和验证器交互，为简洁起见，我们使用 f 与 V 表示最终的产物与评分细则。

第二，直接文件编辑（图 1，Deliverables）。现有界面大多要求所有人类反馈都通过消息（C. Message）口头表达，当期望的改动难以被人类准确言说时，这种方式就很受限。我们转而把主面板切换为展示智能体产出的成果（如写作文档、数据可视化），允许用户直接编辑它们。由于人类偏爱基于 UI 的交互，而智能体往往以程序化方式运作 [Wang et al., 2025d]，对于可视化成果（如 HTML 图表），我们的界面允许用户通过 UI 直接拖拽元素，这些操作会被转换为代码差异，供智能体观测 [Nilsson et al., 2026]。

第三，自动步骤验证（图 1，Rubrics）。智能体通过生成一条轨迹 τ^i 来产出产物 f^i，从而完成步骤目标 w^i。验证器模块依据标准 V^i 给 f^i 打分，产生一列二值通过/不通过评分，即 verify(f^i,v_k^i)→r_k^i∈{0,1}。评分结果会以红叉或绿勾的形式渲染在界面上供用户参考。如果用户不同意自动验证结果，可以通过执行 verify 动作来更改评分。它既是一种帮助用户检查中间任务成功情况的辅助工具，也为构建任务评估评分细则奠定了基础。

**任务会话的迭代本质。** 尤其是对于以产物为驱动的任务，人机交替采取行动往往会发生多轮，才能产出令用户满意的最终产物。为回应任务会话的这种迭代本质，我们可以把每一对人与智能体的轨迹 (τ_j^H,τ_j^A) 视为一个交互单元 u_j，它在前 j 轮迭代产出 f_0,⋯,f_{j−1} 的基础上产出输出产物 f_j。具体来说，在每个交互单元 u_j 之后，用户可以通过采取一序列构成 τ_{j+1}^H 的动作来开启另一轮迭代。一旦用户完成动作并触发，智能体将接收所有过往交互 u_{0:j} 以及最新的人类活动 τ_{j+1}^H，以采取动作 τ_{j+1}^A 并把自身的产物输出精修为 f_{j+}。

虽然自动验证模块会产出当前产物的质量度量 r_0，但初始评分细则 V_0 是由 LM 一次性创建的，可能无法捕获忠实地评估所需的全部标准。因此，我们让验证器模块能够演化：利用人类活动 τ_j^H 更新上一轮的评分标准 V_j，把用户潜在的意图与偏好言说为可评分的细则，从而得到更新后的细则 V_{j+1}。在理想情况下，最终演化的验证器 V_J 应捕获所有用户需求并充当全面的评估评分细则，所产生产物 f_j 的质量应随着任务迭代（即 j 增大）通过整合人类反馈而大致提升，因此 ∑_{v∈V_J} verify(f_{j′},v) ≥ ∑_{v∈V_J} verify(f_j,v), ∀j′>j。然而在实践中，我们观察到这一性质在 j 与 j′ 相距较远时成立，例如当 j=0、j′=J 时，这构成了一种更强的智能体学习信号。

### 2.2 测试时智能体适配范式

测试时智能体适配以流式方式运作：任务依次到来，每个完成的会话都为适配智能体提供新数据。与基于固定数据集的一次性适配不同，智能体会随着与人类共事经验的积累而持续更新。

形式化地说，自适应智能体逐一处理共 T 个任务：t=1,⋯,T。智能体以一个未适配的模型与空上下文初始化，记为 A^0，并在每个任务之后更新。具体而言，在人类与智能体 A^t 共同完成第 t 个任务会话之后，智能体 A^t 利用该会话数据把自己升级为 A^{t+1}（§2.3）。接着，人类与最新的智能体 A^{t+1} 进行第 t+1 个任务的交互。如图 2 所示，我们期望智能体的能力在求解这一连串任务的过程中大致提升。

为评估测试时自适应智能体在给定任务 t 上的单人成功率，我们采用智能体在第 0 个任务迭代 u_0^t 中完全独自产出的首个最终步骤产物 f_0^t，并依据最终评分细则 V_J^t 对它进行评估，报告所有验证器分数的平均成功率。值得注意的是，产出这一首个产物的智能体只接收了来自先前任务的监督信号，对于当前任务除了任务指令之外没有接触任何东西。

作为对这种在线测试时智能体适配的消融设置，我们还收集用户与不适配智能体在同样 K 个任务上交互的数据，记为离线数据。我们利用这些数据在后续实验章节中对人类交互信号与智能体整合策略进行干净的消融研究。

### 2.3 智能体适配方法

给定智能体策略 πθA(a|o,c)，其中有两个可适配组件：智能体上下文 c 与骨干语言模型权重 θ，我们分别称之为基于上下文的适配与基于权重的适配。

#### 2.3.1 基于上下文的适配

基于上下文的适配把所有人类活动 {τ_j^H} 转化为两个类别上的语言化文本信息：(1) 存储事实性与偏好性知识的智能体记忆 M，以及 (2) 承载程序性知识的智能体技能库 K。在第 t 次上下文适配时，两种归纳均由一个以记忆/技能特定指令为条件的 LM 驱动：

`induce_{LM_memory}({τ_j^H}, M^t) → M^{t+1}`，`induce_{LM_skill}({τ_j^H}, K^t) → K^{t+1}`　(1)

由此得到适配后的策略 πθA(a|o,[M^t;K^t]) → πθA(a|o,[M^{t+1};K^{t+1}])。记忆 M 捕获陈述性的、用户或领域特定的信息，例如"图标题应当加粗"或"用户偏好简洁措辞"。技能库 K 把多步工作流编码为可复用的程序性知识，例如"撰写论文摘要：1. 写一句引出动机的话，2. 介绍我们的方法，3. 陈述数值证据，……"。我们的归纳提示词见附录 E。

图 2：左：测试时智能体适配范式，用一个示例性的智能体能力度量来说明。右：上下文适配与权重适配的实现概览。

#### 2.3.2 基于权重的适配

基于权重的适配把人类活动整合进模型参数 θ。不同于受限于"能被表述为文本的内容"以及"模型对该内容的利用能力"的上下文适配，基于权重的方法有可能内化那些隐式且难以言说的额外模式，并直接训练模型产生不同的输出。

通过对多种训练算法的初步探索（附录 B），我们采用直接偏好优化（DPO）[Rafailov et al., 2023]，用第一次与最后一次迭代的轨迹 τ_0 与 τ_{0:J} 对比来构造偏好对，其中 τ_{0:j} 表示轨迹 [τ_0,τ_1,⋯,τ_j] 的拼接。为防止智能体依赖人类交互来达到正确的任务解，我们把 τ_{0:j} 整合为更短的一次性解 τ_j^{A*}：把多次中间文件编辑合并为一次带多个参数的编辑动作，并跳过观测性（如读取）与触发动作。这样，我们就是在训练智能体偏好一次成稿地生成最终高质量解，而不以中间人类动作为条件。实现这一点意味着智能体能够通过保持恰当的用户建模来一次性产出用户偏好的解，而不再依赖进一步的人类监督。具体地：

`L_DPO(θ) = −log σ( β( log(πθ(τ_J^{A*}|q_j)/π_ref(τ_J^{A*}|q_j)) − log(πθ(τ_j^{A*}|q_j)/π_ref(τ_j^{A*}|q_j)) ) ), j=0`　(2)

其中

`log πθ(τ|q) = ∑_l log πθ(a_l|q,a_{<l},s_{<l};c)`　(3)

a_l 表示智能体在第 l 步采取的动作，s_l 表示由此产生的环境状态。q_j 是到第 j 次迭代为止的用户查询，在我们的设置中，当 j=0 时它就是初始任务指令。σ 是 sigmoid 函数，β 是控制 πθ 能偏离 π_ref 多远的超参数。在实现中，我们把参考策略 π_ref 设为该任务会话训练之前的初始策略。尽管策略并不显式地以人类活动为条件，我们确实使用人类活动来构造监督轨迹 τ_j^{A*}。对每个任务会话，我们使用第一次与最后一次解构成的配对，因为它们在经验上表现最好。

在这种构造的配对上训练只能提供数量有限的训练数据点，因此我们还用训练时采样的智能体解来构造配对，从而扩充训练池。具体来说，我们把训练时采样得到的智能体解视为被拒轨迹，把对应收集到的任务会话中的最终解视为被选轨迹，从而构造出额外的 DPO 训练配对。关于不同配对构造策略的更详细比较见附录 B。

## 3 实验：使智能体适配人类专长

在本节中，我们首先介绍测试时智能体适配的实验设置（§3.1），然后借助多样化的人类交互信号，用上下文与权重两种更新方法展示其有效性（§3.2、§3.3）。我们进一步比较上下文适配与权重适配在效率（§3.4）与所学专长（§3.5）方面的差异，以提供更多洞见。

### 3.1 任务、设置与评估

**任务。** 我们为智能体已被相对广泛采用的两个场景构建任务，即 (i) 论文摘要写作：给定论文标题与引言部分，撰写摘要；以及 (ii) 数据可视化：给定数据说明与期望的可视化风格，创建一个 HTML 图表来实现该可视化。

我们关注的是这样一些领域：(i) 有一定数量的人类比普通 AI 智能体拥有更强的个性化专长，以及 (ii) 足够开放式，以反映现实世界中人类数字活动的复杂本质。对每个场景，我们使用 2025 年 NeurIPS、ICML、ICLR、*CL、EMNLP 与 CHI 会议中最佳与杰出论文，手工构建了 20 个任务，以保证内容质量与话题覆盖的多样性。除了报告测试时智能体在这 20 个任务上的单人成功率之外，我们还进一步测试智能体能把所学知识多好地泛化到未见任务。我们同样为写作与数据可视化两个场景各创建了另外 30 个留出任务，取自同一批会议在 2023 与 2024 年的最佳论文，覆盖与用于收集数据的 20 个测试任务不同的话题（附录 A）。

**设置。** 对每个任务场景（写作或数据可视化），我们招募 5 位人类参与者与上下文自适应智能体交互，另招募 5 位与权重自适应智能体交互。为进行消融研究，我们额外招募 5 位与不适配智能体（即离线设置）交互。每位人类在其被分配的场景内完成 20 个任务。总之，我们收集了 2 场景 × 15 用户 × 20 任务 = 600 个数据点。

对于论文摘要写作，我们招募了五所大学的二年级及以上 CS 博士生，他们在覆盖 ML、NLP 与 HCI 的学术写作方面具有经验。对于数据可视化，我们从 Handshake 人才网络（https://joinhandshake.com/）招募，每位参与者在医疗、商业分析、工程，或数学、心理学、生物学研究等专业背景中都具备丰富的数据分析经验。

我们把智能体初始化在空的上下文 c=∅ 上，骨干语言模型为 Qwen3.6-35B-A3B，托管并使用 tinker API（https://tinker-docs.thinkingmachines.ai/tinker/）训练。上下文归纳与演化验证器由 claude-sonnet-4-6 支持。我们也在初步实验中尝试了同期的开源模型，但它们无法产出所需质量的、可复用的记忆、技能与验证标准。

**评估。** 我们分两个方面测试每个测试时自适应智能体。在收集了交互数据的 20 个任务上，我们依据其最终演化评分细则 V_J^k 评估智能体在每个任务 k 上的初始解 f_0^k，并计算所有任务上的平均评分细则分数，以展示其在线适配能力。注意我们的智能体是针对个体用户 e 适配的。我们分别报告上下文组与权重组中所有用户的平均分数。为测试智能体改进能否跨任务泛化，我们还让最终适配后的智能体 A^K 在没有人类参与或进一步适配的情况下运行那 30 个留出任务，并同样取其产物进行评估。为评估一个智能体向其对应人类 e 适配得多好，我们需要为这些留出任务构建专门的评估评分细则 V_e，因为它们不像收集数据的 20 个测试时任务那样被同样地产出。具体来说，我们让 claude-sonnet-4-6 模型在给定任务指令的情况下为每个任务创建评分细则，并要求它涵盖 (i) 人类撰写的评分细则：我们请用户 e 撰写一份可普遍适用于其任务场景（即摘要写作、数据可视化）中所有任务的评分细则；以及 (ii) 从我们收集自该用户的 20 个任务中总结出的评分细则 {V_e^k}_{k=1}^{20}。对于总结性评分细则 (ii)，我们使用 claude-sonnet-4-6 提取在 20 个任务间共享的重要标准。我们确保生成的留出评分细则同时与人类撰写和总结的细则对齐，以保证它满足该特定用户的要求。

作为对比，我们运行基线，即一个未适配的智能体 A^0 独立地在相同的测试时与留出任务上单独行动，并用相同的评分细则评估其产物。

为对智能体在这批会话数据下可能适配到的任务性能上界有一个概念，我们还把产物的最后一个版本 f_J 当作来自人机交互的 oracle 结果。我们同样用最终评分细则 V_J 给它评分并报告任务平均分数。正如我们随后在表 1 中展示的，这一 oracle 分数往往达不到 100%，原因是智能体能力的限制或允许人类投入的努力不足以实现所有人类要求。

### 3.2 智能体能通过交互高效适配人类专长

| 适配方式 | 场景 | 测试时任务 |  |  | 留出任务 |  |
| --- | --- | --- | --- | --- | --- | --- |
| | | 基线 | 适配 | Oracle | 基线 | 适配 |
| 上下文 | 摘要写作 | 81.7 | 85.4* | 89.5*** | 90.2 | 93.5*** |
| 上下文 | 数据可视化 | 77.0 | 86.9*** | 95.0*** | 89.9 | 92.1* |
| 权重 | 摘要写作 | 82.8 | 86.5* | 91.1*** | 88.0 | 93.0*** |
| 权重 | 数据可视化 | 69.0 | 81.1*** | 93.8*** | 86.2 | 91.2** |

表 1：在论文摘要写作与数据可视化任务上，比较智能体的单人成功率（SR），分别使用上下文（上）与权重（下）的测试时在线适配。测试时任务报告智能体在收集数据的 20 个任务上的表现；留出任务报告智能体在同一类别 30 个留出任务上的表现。我们对适配与 oracle 方法相对基线做了显著性检验，具体为双侧配对 t 检验。值得注意的是，所有适配结果在统计上都显著优于基线，即 |t-statistic|>2.0。我们用 *、**、*** 表示 p<0.05、p<0.01、p<0.001 的结果。

如表 1 所示，两种适配方法都能在仅 20 个任务会话内显著提升智能体的单人任务求解表现。在收集了人机交互数据的任务（测试时任务）上，我们的上下文适配与权重适配智能体——在每个任务上评估时，智能体在该任务上尚未收到任何人类建议，仅使用此前任务累积的适配——把单人任务求解成功率在写作任务上相对提升 4.5% 与 4.5%，在数据可视化任务上分别提升 12.9% 与 20.9%。为证明在每种适配情形、每个任务这样相对较小的 100 个数据点池上取得了有效改进，我们对匹配的任务实例在基线与适配智能体之间做了配对 t 检验，以评估这些增益的统计显著性。值得注意的是，每个配对检验都达到显著（t>2.0），表明即便来自少量样本，适配也相当有效。

为进一步检验我们适配智能体的跨任务泛化能力，我们同样在数据收集与智能体适配期间未见的留出任务上评估基线与适配智能体。如表 1（留出任务）所示，上下文适配与权重适配智能体相对基线智能体在写作上分别显著提升 3.6% 与 5.7%，在数据可视化上分别提升 2.4% 与 5.8%。这种跨任务集的一致改进确认了适配泛化到了适配期间的特定任务之外。

对比两个任务领域，我们观察到数据可视化的增益大于写作，这可能是因为骨干语言模型的写作能力已通过预训练得到更充分的发展，留给适配去改进的空间更小。当迁移到同一领域内的留出任务时，写作的增益与其测试时表现相当，而在未见的数据可视化任务上增益明显缩小。这种不对称表明数据可视化任务是异质的，接触更多样化的任务很可能更有利于适配。

### 3.3 从超越反馈的人类交互信号中获益

图 3：人类在与智能体交互过程中的动作分布。comment（评论）在数据可视化任务中不受支持。

此前许多工作把人类反馈简化为发回给 LM 或智能体的文本消息 [Christiano et al., 2017]。然而人类自然地通过远为丰富的一整套活动来表达反馈，其中大部分作为智能体学习信号的来源仍未被探索。通过我们的界面，除文本消息动作外，专家还可以直接编辑文件、调整智能体计划、修订验证标准并留下行内评论；每一类都构成专长得以浮现的独特渠道。如图 3 所示，人类在与智能体交互的整个过程中都会动用这整套动作。

| 方法 | 写作 | 数据可视化 |
| --- | --- | --- |
| 基线 | 80.8 | 66.4 |
| 全部动作 | 84.9 | 75.6 |
| 仅消息动作 | 81.9 | 68.0 |

表 2：比较使用全部人类动作与仅使用消息动作的智能体适配。

为检验这些多样的人类动作是否充当有效的适配信号，我们比较使用 (i) 全部人类动作与 (ii) 仅消息动作的智能体适配结果。我们在收集到的离线数据上使用上下文适配进行这一比较，因为在在线情形下或权重适配方法下很难隔离非消息动作的效应。(i) 使用我们默认的上下文适配方法，而 (ii) 把上下文归纳的输入限制为仅消息动作。如表 2 所示，加入非消息动作在写作与数据可视化任务上分别带来 3.0% 与 7.6% 的额外增益，表明文本反馈之外的动作具有价值。

### 3.4 权重适配比上下文适配具有更高的推理时效率

除任务表现之外，权重适配在推理时还提供显著的效率优势。在输入端，权重适配智能体在写作与数据可视化任务上比其上下文适配对应物分别少用 62.6% 与 88.3% 的 token，显示出把专长编码进模型权重而非不断增长的上下文所带来的直接好处。

这种效率增益也延伸到输出端。相对于来自人类与未适配基线智能体的任务会话，权重适配智能体在写作与数据可视化任务上分别少产出 9.1% 与 4.4% 的输出 token，同时取得更好的结果。相比之下，上下文适配智能体朝相反方向移动，在同样的任务上产出长 20.1% 与 6.1% 的回复，表明上下文适配继承了它所依条件上下文的某些冗长性。在图 4 中，我们通过分析不同动作类型的动作内容长度来探究更深层的原因，发现上下文适配智能体相对基线智能体和权重适配智能体分别产出长 143–176% 与 69.9–95.7% 的消息，而在其他任务执行动作上几乎没有差异。

图 4：按动作类型比较上下文适配与权重适配智能体相对未适配基线智能体的平均 token 数变化。正值表示动作内容比基线更长，负值表示更短。对于摘要写作（左）与数据可视化（右）任务，上下文适配智能体产出的消息分别比基线与权重适配智能体长 143% 与 176%。

### 3.5 智能体从人类身上学到了什么，又没学到什么

我们分析适配智能体相对基线与 oracle 的通过/未通过评分细则，以考察我们的智能体通过适配学到了什么、又没学到什么。具体来说，我们比较由以下三者产出的测试时解：(i) 基线智能体，(ii) 我们适配的智能体，以及 (iii) 人机交互（即 oracle）。我们通过找出被适配智能体 (ii) 满足、却被基线 (i) 未满足的评分细则来衡量 Agent Gains（智能体增益），并通过找出被适配智能体 (ii) 未满足、却在 oracle 解 (iii) 中达成的评分细则来衡量 Gap to Oracle（与 oracle 的差距）。对写作与数据可视化任务，我们按主题对这些评分细则进行分类，这些主题即人类表达其专长之处（附录 C）。

对于写作任务，人类表达其专长最多的方面是话语的精确与压缩（19.6%）、表层形式与会议惯例（19.1%）以及情境特异性（17.6%），反映出专家经常纠正智能体朝向的、关于会议隐含惯例的实践知识，以及对精确、简洁写作的持续强调。

在各主题中，表层形式以及术语与命名最容易吸收，人类所表达专长的 70.4–73.7% 被成功整合，这可能是因为它们易于被明确指定、智能体也易于遵循。相比之下，情境特异性与问题框定更难以学习，仅 41.9–43.4% 的表达专长被捕获，表明这些类别需要更隐式、更具情境判断力的东西，在少量样例中更难迁移。比较两种适配方法，上下文与权重获得的知识大体可比，各主题比例相近，这与先前把不同功能分配给上下文与权重的工作 [Tiwari et al., 2026] 相反。

对于数据可视化，人类表达专长主要围绕标题、图例与标签上的文本注释（38.5%），以及颜色（15.5%）与空间清晰度（12.4%）等视觉方面。值得注意的是，人类在图中该突出什么以及如何突出（颜色与视觉编码）方面表现出特别的专长，两种适配方法与人类 oracle 之间都存在可观差距，分别有 60.1% 与 50.0% 的专长未被捕获。相反，面向实现方面的内容对智能体明显更容易整合：数据保真要求的 75.2% 与 HTML 规范要求的 94.4% 得到满足。

图 5：适配过程中智能体上下文与权重吸收的专长（Agent Gains）以及相对人类 oracle 仍存在的差距（Gap to Oracle），写作（上）与数据可视化（下）任务。各专长主题的详细描述见附录 C。

## 4 用可扩展的评分细则演化引出人类专长

在本节中，我们把焦点转向智能体套件中演化的验证器模块，展示它作为开放式任务可扩展评分细则标注工具的潜力（§4.1）。我们进一步把评分细则剖析为共享社区专长与个人策略及偏好的组合（§4.2），并表明我们适配的智能体同时学到了两者（§4.3）。

### 4.1 来自人机交互的评分细则比纯 LLM 和纯人类细则捕捉到更多失败

长期以来，超出数学与编程问题的任务都被当作"不可验证"的，原因在于难以标注一份既全面又足够准确、可用于评估的评分细则。如何恰当地评估这类开放式任务一直是个长期问题：近期工作大多收敛到 LLM-as-a-judge [Zheng et al., 2023]，依据由 LLM 或人类产出的评分细则打分。然而每种方法都有各自不同的短板。

一方面，LLM 创建的评分细则常常遗漏人类专家在意的方面，且容易带有自偏好，偏爱 LLM 产出的解而非人类评估者会偏好的解 [Deutsch et al., 2022; Shankar et al., 2024]。然而纯人类标注也并不更容易，因为人类判断在开放式任务上天然不一致，而产出高质量评分细则需要投入大量精力去指导、激励和监督标注者 [Xu et al., 2024a; Vidgen et al., 2026]。更糟的是，标注者通常被要求仅依据任务说明撰写评分细则，缺乏在实际执行中的根据，使他们容易遗漏只有在任务被执行后才会浮现的细节 [Xu et al., 2024a]。为此，我们设计的演化评分细则模块直接从人类与智能体的交互中捕获人类专长，同时通过基于 LLM 的自动评分细则生成来减轻人工标注负担、实现可扩展性。

图 6：纯 LLM 评分细则无法区分低质量的智能体解（左：写作，右：数据可视化），而我们的评分细则在写作上捕捉到与人类撰写细则相当、在数据可视化上甚至多得多被忽视的方面。

为从经验上证明这一点，我们收集两套基线评分细则用于比较：(i) 依据任务说明由 LLM 产出的评分细则，以及 (ii) 依据任务场景由人类撰写的评分细则。鉴于人力资源有限、无法为 100 个任务逐一标注评分细则，我们让人类标注一套可普遍适用于其被分配类别（即写作或数据可视化）中所有任务的评分细则。然后我们评估每套评分细则捕捉智能体单人解中失败的能力，即智能体在每个任务会话中、任何人类交互之前的初始、无协助尝试。由于这些单人解随后都在同一会话中经过许多轮人类迭代修改，我们以此作为它们是"不完美的、应当在一份真正全面的评分细则下得到相应低分"的证据。具体来说，我们在三套评分细则上评估智能体单人解，并在图 6 中展示其分数。

首先，依据纯 LLM 评分细则的分数在写作与数据可视化任务上分别平均饱和于 98.3% 与 88.7%。相比之下，我们演化的评分细则给出显著更低的平均分 82.3% 与 66.4%，表明它们捕捉到更多基线评分细则所遗漏的失败。与纯人类评分细则相比，我们演化的评分细则在写作任务上捕捉到相当比例的失败，但在数据可视化任务上多捕捉 17.9%。人工分析纯人类评分细则后，我们推测这一差距主要源于标注者动机与专长的差异，因为我们为写作任务聘请的是高年级 CS 博士生，而为数据可视化聘请的是一般人类工作者。因此，基于 LM 的评分细则演化在数据可视化上可能有更大空间超越人类基线，因为一般工作者可能受训更少、动机更弱，去标注评估评分细则。更多验证测试见附录 D。

### 4.2 评分细则同时捕捉共享的社区专长与个人专长

即使用同一个初始智能体、在同一组任务上交互，不同人类也会得到不同的解与不同的评分细则。这反映了我们研究的写作与数据可视化等开放式任务的一个基本属性：它们不承认单一、普适的正确性概念。事实上，取决于特定专家偏好什么，无数解都能很好地求解这类任务，即在其对应评估标准上取得高分。尽管存在这种人际差异，大多数学科仍然维持着被其从业者广泛认同的社区准则，形成一种相对正确性的概念。我们假设，通过我们界面演化出的评分细则同时捕获了这两个组成部分：(i) 共享的社区准则，例如让每一处书面主张都建立在具体数值证据之上；以及 (ii) 个人策略与偏好，例如一位专家偏好枚举、另一位则避免枚举。

为检验这一假设，我们取每位用户演化出的评分细则，对每一条标准检查它是否也被同一任务上其他用户的评分细则所覆盖。被超过 60% 的其他评分细则覆盖的标准被归类为共享准则；否则我们将其视为个性化的。在所有写作与数据可视化任务上，我们发现平均 67.9% 与 70.7% 的用户评分细则属于共享社区准则，其余反映个性化专长与偏好。图 7 展示了这些共享标准以及示例性的个性化标准。在两个任务中，我们都观察到用户强调不同方面。例如对于可视化，一些用户优先关注实现细节（如 Plotly CDN、CSS 样式），另一些则强调统计严谨性，如误差棒与显著性检验。

图 7：摘要写作（左）与数据可视化（右）任务上的共享与个性化评分细则。每个交叉点的数值表示：在该用户交互所得全部评分细则中，被归类为共享的比例。

### 4.3 智能体同时学习共享专长与个性化专长

| 方法 | 写作：ΔSR% |  | 数据可视化：ΔSR% |  |
| --- | --- | --- | --- | --- |
| | 共享 | 个人 | 共享 | 个人 |
| 上下文 | 0.3 | 6.2 | 6.1 | 19.6 |
| 权重 | 1.9 | 9.4 | 8.8 | 13.8 |

表 3：相对基线智能体，适配到个体专家的智能体在写作（左）与数据可视化（右）任务上，在个性化标准与共享社区标准上都有改进。

紧接着的一个自然问题是：通过这种高效适配，智能体只学到个人专长，还是也在更广泛意义上改进社区共识标准？对每个适配到特定专家的智能体，我们分别测量它在共享与个性化标准上的成功率，并把两者都与基线智能体的成功率比较。如表 3 所示，除在个性化标准上的显著增益外，智能体在这两个任务的共享标准上还提升最高达 8.8%，表明这种适配带来了基础能力上的真实增益，而不仅仅是个人契合。

### 4.4 探索：从个体适配中提炼社区专长

尽管每个智能体都朝特定用户适配，我们已经表明平均 69.3% 的用户专长反映了共享的社区准则。于是我们问：能否把分别适配的智能体整合起来，以广泛提升跨用户的表现？在本节中，我们在上下文与权重两条通道上探索把多个个性化智能体合并为单一联合智能体的初步策略，并展示有效合并这一开放挑战。

**上下文合并。** 我们用一个 LLM（claude-sonnet-4-6）把来自不同用户交互数据得到的上下文合并为一份单一的共享内容。然后我们把这份共享内容增补到基线智能体上，并在留出任务上评估。

**权重合并。** 我们探索了两种整合不同用户所得模型权重的方法。第一种 Weight-Train 把所有用户的数据汇集起来从头训练一个单一模型。第二种 Weight-Merge 通过直接合并分别训练好的权重来避免重训练，具体做法是平均 LoRA 适配器参数 [Wortsman et al., 2022] 并与基座模型结合用于直接推理。

| 方法 | 写作：ΔSR% |  |  | 数据可视化：ΔSR% |  |  |
| --- | --- | --- | --- | --- | --- | --- |
| | 共享 | 个人 | 总体 | 共享 | 个人 | 总体 |
| 上下文 | -4.4 | 1.3 | -2.7 | 2.9 | -0.5 | +1.1 |
| Weight-T | -4.7 | 3.5 | -2.3 | 3.6 | 2.7 | +3.3 |
| Weight-M | 0.0 | 3.2 | +1.0 | 3.6 | 1.8 | +3.1 |

表 4：探索把个性化智能体整合为单一智能体的不同方法。

我们全部使用离线场景收集的数据进行合并，因为在在线场景下用自适应智能体进行干净的 Weight-Train 实验很困难。如表 4 所示，所有合并方法在数据可视化任务上都比基线有改进，但在写作任务上增益更小。分解共享与个人评分细则后，我们发现在写作任务上所有合并方法都比基线更好地满足个人标准，但在保持共享标准上表现不一。而对于数据可视化任务，方差主要来自满足个人标准方面。这可能是因为基线智能体在写作上已经表现很强，留给可跨用户泛化的改进空间更小。数据可视化相对更开放，因而在分歧较大的人类专长上给模型带来压力，其有效整合仍是一个开放挑战 [Park et al., 2024; Chakraborty et al., 2024]。

另一个潜在因素是我们适配的离线性质：与智能体接收针对其当前状态的人类反馈的在线适配相比，离线适配使用的是可能过时的人类反馈，因而导致更小的增益 [Tang et al., 2024]。综合来看，这些发现凸显了把多样化个人专长有效带入单一智能体的挑战，并推动未来对专长整合的研究。

## 5 相关工作

**测试时智能体适配。** 由于训练数据与下游使用多样性之间持续存在差距，在测试时适配智能体以满足临时的下游需求已越来越流行 [Gao et al., 2026]。这类工作的很大一部分聚焦于适配智能体上下文。一方面，既有研究把程序性 [Wang et al., 2025c]、事实性 [Packer et al., 2023] 与偏好性知识 [Lin et al., 2025] 归纳进推理时增补的智能体记忆。另一方面，为进一步的质量保证与效率，人们设计出程序性技能以实现稳健的知识复用 [Wang et al., 2025b; Zheng et al., 2025; Xia et al., 2026]。基于上下文的适配之所以在这一领域占主导，很大程度上是因为它更易解释、更易实现，且仅凭少量任务会话就能带来可观察的改进。部分正因如此，更新智能体骨干语言模型权重的研究仍远未被充分探索，受限于可用数据有限以及实现与检查的难度 [Lin et al., 2025]。结果是，尽管上下文适配很简单，我们对它与基于权重的测试时训练在逐实例基础上的比较知之甚少。近期研究引入测试时训练（TTT，[Sun et al., 2020]）来实现这种在线模型权重更新，利用来自已实验任务的弱监督信号 [Yuksekgonul et al., 2026]，但仍需要大量训练才能有效。我们的工作挑战了"权重更新更差、且需要更多数据"这一预设，证明了它在骨干语言模型之外的智能体系统上的可行性。

**从人类信号中学习。** 有一长串工作使用人类二值偏好或自然语言反馈来训练 LM，以提升指令遵循能力 [Christiano et al., 2017; Chiang et al., 2024; Buening et al., 2026]。具体在智能体训练中 [Pomerleau, 1988]，许多研究聚焦于训练智能体模仿人类示范 [Ross et al., 2011; Wang et al., 2025a; Shaikh et al., 2025]。然而人类活动通常涉及 UI 层面的交互，这与基于 LM 的智能体偏爱的程序化方式差异极大 [Wang et al., 2025d]，使得原始的人类示范并不适合智能体学习。为解决这种不匹配，一些工作改为让人类对智能体驱动的解提供反馈，并把该反馈转化为训练信号 [Wang et al., 2026b]。虽然有效，但这些方法通常需要大量数据，这在现实场景中往往不可行，同时忽视了人类活动中许多其他可行的行动信号。相比之下，我们的工作开发了一种高效的适配策略，仅在数十个任务会话内就有意义地提升智能体表现。

**在"不可验证"任务上评估智能体。** LM 智能体在软件工程任务上经历了第一波发展，在这些任务中，基于执行、单元测试式的验证器 [Chen et al., 2021] 已成为评估智能体表现的标准且稳健的方式 [Jimenez et al., 2024]。然而，当我们从这些易于验证的任务转向更具开放式性质的任务（如创意写作或视觉创作）时，会出现两大挑战。首先，我们需要找到替代的评估方式：人工评估往往不稳定且难以规模化 [Patwardhan et al., 2026]；一些研究尝试用 LM 直接产出分数 [Liu et al., 2023]，或更稳健地，依据一份评分细则提供一组二值判断 [Aggarwal et al., 2026; Shao et al., 2026]。构建高质量评分细则很困难，因为对开放式任务而言，"任务成功"的含义变得不清晰，存在无数"正确"的求解方式 [Jiang et al., 2026]。虽然大多数工作利用 LLM 或聘请人类标注者来构建评分细则，但我们的实验表明，由于 LM 的知识局限与人类缺乏任务执行中的根据，这些细则并不完整。为解决这一问题，我们提出一种 LLM 自动化、人在环路的评分细则演化策略，为模型训练与智能体评估两方面创建高质量评分细则。

**训练智能体化语言模型。** 与训练一个产出文本的 LM 不同，智能体化 LM 需要消费观测式输入（如序列化的网页内容或 UI 式视觉），并产出包含可执行动作与解释性思考的结构化回复。除了围绕问答或聊天式任务等低智能体化场景的大量工作 [Lin et al., 2025] 之外，近期研究探索了合成海量数据 [Song et al., 2026b] 以训练智能体用于常见用途（如软件工程 [Pan et al., 2025; Jain et al., 2025]）与网页导航任务 [Ou et al., 2024; Shen et al., 2025; Murty et al., 2024; Zhou et al., 2024]）的策略。另一些工作转向人类来源的数据，如记录下的人类计算机使用活动 [He et al., 2026; Wang et al., 2026a]，但仍指出最关键的要诀之一是为训练构建可扩展、高质量的数据。然而这在实践中并不总是可行，因为为特定下游应用准备大量数据可能在时间或成本上都很昂贵。这引出一个尚未被充分探索的问题：我们能否利用有限数量的样例有效地更新模型权重？在本工作中，我们直接处理这一问题并表明这是可能的。

## 6 结论

在本工作中，我们引入了一个自适应智能体框架，通过上下文与权重更新，利用人机交互数据进行测试时适配。在对 20 位人类专家的实验中，我们的智能体仅在 20 次交互内就有效地适配到个人任务成功。我们演化的验证器模块自动整合人类交互信号，为真实的开放式任务产出更全面的评估评分细则。适配后的智能体与演化后的评分细则都捕获了两个层次的专长：跨用户共享的社区专长，以及特定于某个用户的个人专长。

总体而言，我们的结果指向未来 AI 智能体的一条具体设计原则：持续从测试时交互中学习，并适配它们所服务的个体人类。我们希望这项工作能推动对更先进的测试时智能体适配技术的研究，以及对社区级与个人级专长的系统化文档与基准测试。

## 致谢

Zora 受 Google 博士奖学金资助。本工作部分受美国国家科学基金会（National Science Foundation）2543679 号资助支持。我们感谢 Tinker Research Grants 对权重测试时智能体适配实验的支持。我们感谢 CMU 语言技术研究所以及斯坦福 NLP 组的各位在整个项目中给予的有益讨论与反馈。

## 附录 A 数据采集

对于收集人机交互数据的 20 个任务，我们在表 5 中给出其会议与话题。在表 6 中，我们还列出了 30 个留出任务的来源，展示它们与上述 20 个任务的分布差异，以及它们作为我们泛化测试集的有效性。

| 会议 | 标题 |
| --- | --- |
| NeurIPS | Artificial Hivemind: The Open-Ended Homogeneity of Language Models (and Beyond) |
| NeurIPS | Gated Attention for Large Language Models: Non-linearity, Sparsity, and Attention-Sink-Free |
| NeurIPS | 1000 Layer Networks for Self-Supervised RL: Scaling Depth Can Enable New Goal-Reaching Capabilities |
| NeurIPS | On the Generalization Properties of Diffusion Models |
| ICLR | Safety Alignment Should Be Made More Than Just a Few Tokens Deep |
| ICLR | Learning Dynamics of LLM Finetuning |
| ICLR | AlphaEdit: Null-Space Constrained Knowledge Editing for Language Models |
| ICML | CollabLLM: From Passive Responders to Active Collaborators |
| ICML | Train for the Worst, Plan for the Best: Understanding Token Ordering in Masked Diffusions |
| ICML | Roll the dice & look before you leap: Going beyond the creative limits of next-token prediction |
| ICML | Conformal Prediction as Bayesian Quadrature |
| ICML | Score Matching With Missing Data |
| ICML | The Value of Prediction in Identifying the Worst-Off |
| ACL | INFINI-GRAM MINI: Exact n-gram Search at the Internet Scale with FM-Index |
| ACL | Mind the Value-Action Gap: Do LLMs Act in Alignment with Their Values? |
| ACL | LINGGYM: How Far Are LLMs from Thinking Like Field Linguists? |
| ACL | Generative or Discriminative? Revisiting Text Classification in the Era of Transformers |
| ACL | Measuring Chain of Thought Faithfulness by Unlearning Reasoning Steps |
| CHI | Synthetic Human Memories: AI-Edited Images and Videos Can Implant False Memories and Distort Recollection |
| CHI | Creative Writers' Attitudes on Writing as Training Data for Large Language Models |

表 5：我们收集人机交互数据的 20 个任务的标题与会议。

| 会议 | 标题 |
| --- | --- |
| ICLR | Transformers are Inherently Succinct |
| ICLR | LLMs Get Lost In Multi-Turn Conversation |
| CHI | Towards Fluent Interaction with Cyber-Physical Architecture |
| CHI | "I Don't Think RAI Applies to My Model" - Engaging Non-champions with Sticky Stories for Responsible AI Work |
| CHI | iTagPDF: Towards Finally Automating PDF Accessibility |
| NeurIPS | Visual Autoregressive Modeling: Scalable Image Generation via Next-Scale Prediction |
| NeurIPS | Not All Tokens Are What You Need for Pretraining |
| NeurIPS | The PRISM Alignment Dataset: What Participatory, Representative and Individualised Human Feedback Reveals About the Subjective and Multicultural Alignment of Large Language Models |
| ICLR | Generalization in Diffusion Models Arises from Geometry-Adaptive Harmonic Representations |
| ICLR | Never Train from Scratch: Fair Comparison of Long-Sequence Models Requires Data-Driven Priors |
| ICLR | Protein Discovery with Discrete Walk-Jump Sampling |
| ICML | Position: Considerations for Differentially Private Learning with Large-Scale Public Pretraining |
| ICML | Debating with More Persuasive LLMs Leads to More Truthful Answers |
| ICML | Genie: Generative Interactive Environments |
| ACL | Mission: Impossible Language Models |
| ACL | Why are Sensitive Functions Hard for Transformers? |
| ACL | Aya Model: An Instruction Finetuned Open-Access Multilingual Language Model |
| ACL | How Johnny Can Persuade LLMs to Jailbreak Them |
| EMNLP | Pretraining Data Detection for Large Language Models: A Divergence-based Calibration Method |
| EMNLP | An Image Speaks a Thousand Words, but Can Everyone Listen? On Image Transcreation for Cultural Relevance |
| EMNLP | Toward Robust Speech Representation Learning for Thousands of Languages |
| EMNLP | KidLM: Advancing Language Models for Children |
| CHI | Constrained Highlighting in a Document Reader can Improve Reading Comprehension |
| NeurIPS | Scaling Data-Constrained Language Models |
| NeurIPS | Direct Preference Optimization: Your Language Model is Secretly a Reward Model |
| ICLR | Emergence of Maps in the Memories of Blind Navigation Agents |
| ICLR | Universal Few-shot Learning of Dense Prediction Tasks with Visual Token Matching |
| ACL | Do Androids Laugh at Electric Sheep? Humor "Understanding" Benchmarks from The New Yorker Caption Contest |
| ACL | Marked Personas: Using Natural Language Prompts to Measure Stereotypes in Language Models |
| ACL | Weaker Than You Think: A Critical Look at Weakly Supervised Learning |

表 6：我们用于测试智能体泛化能力的留出任务标题与会议。

## 附录 B 对基于权重的适配方法的探索

我们对权重适配方法做了广泛探索，并选择 DPO 作为主实验采用的方法（§2.3）。

### B.1 备选算法

除 DPO 外，我们还实验了同策略蒸馏（on-policy distillation, OPD）与 REINFORCE 训练，公式如下。

**同策略蒸馏（OPD）。** 对当前智能体策略 πθ 施加来自教师策略 π_teacher 的 token 级 KL 散度目标。我们采用同策略自蒸馏（on-policy self-distillation, OPSD）[Zhao et al., 2026]。其学习损失可表示为：

`L_OPD(θ) = −∑_l ∑_{t∈a_{j,l}} π_teacher(a_{j,l}|q,a_{j,<l},s_{j,<l}) log πθ(a_{j,l}|q,a_{j,<l},s_{j,<l})`
`= −∑_l ∑_{t∈a_{j,l}} πθ(a_{j,l}|q,a_{j,<l},s_{j,<l};{τ_j^{A},τ_j^{H}}_{j′=j}^{J}) log πθ(a_{j,l}|q,a_{j,<l},s_{j,<l})`　(4)

**REINFORCE。** 使用第 j+1 条智能体轨迹 τ_j^A 的标量奖励 r_j=∑({r_j})，可选地加上量化的人类活动（例如动作数量 r_j=|τ_j^H|），作为策略梯度信号来强化高奖励轨迹。其损失可表示为：

`L_REINFORCE(θ) = −(R_j − b) ∑_l log πθ(a_{j,l}|q_j,a_{j,<l},s_{j,<l})`　(5)

其中 b 是用于降低方差的基线奖励，我们把 b 实现为上一轮迭代的奖励 b=R_{j−1}。

**性能分析。** 在初步实验中，我们发现两种备选方法都不如 DPO。对于 REINFORCE，我们发现智能体很少探索到依据人类反馈演化出的评分细则而言高分的解，而是不断合成出卡在 1 分制中 0.3–0.4 成功率区间的解。我们推测，智能体在训练中接触专家风格解的机会有限。相比之下，OPD 的优势在于向教师策略提供特权信息以提示学生探索。然而至少在我们的数据高效场景下，我们发现直接训练智能体策略偏好生成 oracle 解（即 DPO）更有效。

### B.2 DPO 数据构造

对于 DPO 训练，我们比较了多种构造成对数据的策略。具体来说，我们实验了 (i) first-last：把第一次与最后一次解配对；(ii) enumerate：把所有可能的更早与更晚的解配对；(iii) min-gap-k：把相隔至少 k 步的更早与更晚解配对。我们最终采用 first-last，因为它在经验上表现最好。

## 附录 C 智能体适配过程中学到的人类专长

在表 7 与表 8 中，我们给出在写作与数据可视化任务中观察到的专长类别定义与示例。

| 类别 | 示例任务（说明） |
| --- | --- |
| 表层形式与会议惯例 | 机械性呈现规则，包括字数限制（150–250 词）、单段排版、去除章节标题、标点惯例（不用破折号）以及避免非正式语体。 |
| 主动语态与直接措辞 | 偏好第一人称主动句式（'we find'、'we show'、'we introduce'），而非被动语态；偏好直接陈述而非含糊表述；使用优先考虑目标读者清晰度的易懂术语。 |
| 术语与命名 | 处理缩写（首次出现时展开并附括号缩写）、一致的技术命名、术语定义或回避、领域术语的精确使用，以及消除歧义引用或未定义术语。 |
| 问题框定 | 涵盖摘要如何以研究问题或空白开篇，并建立动机与背景。 |
| 具体程度 | 对落地细节的要求，包括具体数字、数据集名称、模型规模、度量单位、样本量、领域或任务的具名示例、定量结果，以及具体实验参数，而非抽象描述。 |
| 贡献与发现的呈现 | 工作总结声称要交付或证明什么，包括把贡献列为独立要点、用具体支撑给出核心发现、明确突出关键洞见、陈述理论贡献，以及给出对该领域的影响或启示。 |
| 话语精确与压缩 | 结合紧凑、精确的措辞——禁止模糊限定词、含糊修饰语与无支撑的最高级——以及话语压缩：强制每句只讲一个观点、消除冗余与重复，并在不牺牲清晰度的前提下压缩废话。 |
| 逻辑流 | 区分不同类型的论断或比较，把不同观点拆到各自句子或从句中；保持从问题到方法到结果的逻辑推进，句子之间有显式过渡与叙事连贯。 |

表 7：写作任务中观察到的人类专长类别说明。

| 类别 | 示例任务（说明） |
| --- | --- |
| 交付与 HTML 规范 | 成果的机械性打包：有效的自包含 HTML、必需的库/CDN 标签、存在预期的画布或图表元素，以及可被浏览器无错渲染的输出。区别于"图表结构与几何"（后者涵盖图表是如何组成的）。 |
| 图表结构与几何 | 可视化本身的配方：图表类型、朝向、面板/系列/分组的数量与排布、标记形状与尺寸（柱、单元格、热力图）、分组布局与视口尺寸。区别于交付（文件/HTML 有效性）、坐标轴（数值尺度）与数据保真（数值是否正确）。 |
| 数据保真 | 编码值与指定数据完全匹配：单元格内容、柱高/柱长、误差棒范围、系列/行/列数量，以及正确定位的最优值标记。区别于颜色与视觉编码（值如何着色）与图表结构（布局配方）。 |
| 坐标轴、尺度与参考标记 | 图表的数值骨架：轴范围、刻度间隔与顺序、线性与对数尺度、网格线有无，以及指定位置的虚线/阈值参考线。区别于标题、图例与标签（轴标题/刻度文本措辞）与数据保真。 |
| 颜色与视觉编码 | 把值与分组映射到颜色及相关视觉通道：语义色映射（如绿色=期望）、色图与不透明度、系列/分组色系、高亮填充，以及与背景的对比度。区别于数据保真（值是否正确）与标题、图例与标签（解释颜色的图例文字）。 |
| 标题、图例与标签 | 文本与注释内容：图表/章节标题、轴与系列名称、图例内容与位置、缩写/命名惯例、题注、页眉，以及叠加标记与提示（显著性括号、星号/星标、箭头、虚线引导、悬停/工具提示）。区别于空间清晰度（文本/标记是否重叠或被裁切）与颜色（颜色映射本身，而非图例措辞）。 |
| 空间清晰度与不重叠 | 布局卫生，使元素保持可见且彼此区分：避免遮挡的标签放置、柱/误差棒/工具提示不被裁切、单元格边框、外边距/内边距与图例边界。区别于标题、图例与标签（文本/标记写了什么或有没有）与图表结构（面板/视口配方，而非重叠/裁切）。 |

表 8：数据可视化任务中观察到的人类专长类别说明。

## 附录 D 评分细则验证

除了有效捕捉不完美任务解中的失败（§4）之外，我们还表明我们的评分细则在揭示任务成功方面与其他解一样有效，进一步验证了我们演化评分细则的质量。

在图 8 中，我们用纯 LLM、纯人类与我们的评分细则评估 oracle 解，三者都能通过给出接近高分的分数来有效指示任务成功。结合图 6 的结果，这表明我们的评分细则之所以判定不完美智能体解失败，是因为解本身存在问题，而不是评估标准存在问题。

图 8：我们演化的评分细则在衡量任务成功方面与 LLM 及人类产出的评分细则一样有效。

## 附录 E LM 支持模块的提示词

**用于上下文自适应智能体的记忆归纳提示词。**

```
Merge new induction entries into the existing memory file and produce a refined, cross-session version.
You receive (i) the original memory file and (ii) new entries derived from a new session.
Merge (ii) into (i): keep durable prior preferences, add genuinely new ones, and lightly deduplicate.
Output line count should stay about the same as the original memory (i). Do not add excessive new entries.
Keep:
- Specific user preferences that apply to certain contexts
- Recurring styling or workflow habits (e.g. larger fonts, no gridlines, compact layout) across tasks
- General facts about how the user works
Remove or merge only when necessary:
- Nonsensical or contradictory entries
- Highly task-specific details unlikely to help elsewhere (e.g. a color for one named column/bar)
- Duplicate lines that say the same thing in different words.
- Make each line concise but do not over-compress away useful detail.
Output rules:
- One entry per line. Plain text only (NO markdown headers like # or ##).
- Prefix each line with "Fact:" or "Preference:".
- Do not include reasoning or a thinking process.
Reply with:
Title: <short topic name>
- Fact: <item>
- Preference: <item>
```

**用于上下文自适应智能体的技能归纳提示词。**

```
From the task and numbered log, describe the workflow the agent used: ordered steps, generalized (no long paths).
Your primary job is to capture what THIS session did—especially techniques, fixes, and steps visible in the Log. The existing skill file—if any—is background only.
When an existing skill file is provided:
- FIRST update the workflow using concrete steps from this session's Log (mandatory when the log is non-empty).
- Add or revise steps for anything new in this session (e.g. chart tweaks, file edits, verification, user-requested changes).
- Adopt the useful parts from original steps only when still accurate; merge duplicates.
- Do not return the existing skill unchanged if the log shows new agent work.
Output the full updated skill (not a diff). Generalize: no long paths, file paths, or raw code.
Reply with:
Title: <short task name>
1. <step>
2. <step>
...
If nothing fits: NONE
```

## 参考文献

[1] Abdulhai et al. (2026). M. Abdulhai, I. White, Y. Wan, I. Qureshi, J. Leibo, M. Kleiman-Weiner, and N. Jaques How llms distort our written language. arXiv preprint arXiv:2603.18161.
[2] Aggarwal et al. (2026). P. Aggarwal, G. Neubig, and S. Welleck Gym-anything: turn any software into an agent environment. arXiv preprint arXiv:2604.06126.
[3] Anthropic (2025). Anthropic Agent skills.
[4] Buening et al. (2026). T. K. Buening, J. Hübotter, B. Pásztor, I. Shenfeld, G. Ramponi, and A. Krause Aligning language models from user interactions. arXiv preprint arXiv:2603.12273.
[5] Chakraborty et al. (2024). S. Chakraborty, J. Qiu, H. Yuan, A. Koppel, D. Manocha, F. Huang, A. Bedi, and M. Wang MaxMin-RLHF: alignment with diverse human preferences. In Forty-first International Conference on Machine Learning,
[6] Chen et al. (2021). M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. D. O. Pinto, J. Kaplan, H. Edwards, Y. Burda, N. Joseph, G. Brockman, et al. Evaluating large language models trained on code. arXiv preprint arXiv:2107.03374.
[7] Chiang et al. (2024). W. Chiang, L. Zheng, Y. Sheng, A. N. Angelopoulos, T. Li, D. Li, H. Zhang, B. Zhu, M. Jordan, J. E. Gonzalez, et al. Chatbot arena: an open platform for evaluating llms by human preference. arXiv preprint arXiv:2403.04132.
[8] Christiano et al. (2017). P. F. Christiano, J. Leike, T. Brown, M. Martic, S. Legg, and D. Amodei Deep reinforcement learning from human preferences. Advances in neural information processing systems30.
[9] Cukurova (2026). M. Cukurova What do you mean by human-ai collaboration: prerequisite functions and the affordances needed to achieve it. arXiv preprint arXiv:2606.15509.
[10] Deutsch et al. (2022). D. Deutsch, R. Dror, and D. Roth On the limitations of reference-free evaluations of generated text. In Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing, pp. 10960–10977.
[11] Gao et al. (2026). H. Gao, J. Geng, W. Hua, M. Hu, X. Juan, H. Liu, S. Liu, J. Qiu, X. Qi, Q. Ren, Y. Wu, H. WANG, H. Xiao, Y. Zhou, S. Zhang, J. Zhang, J. Xiang, Y. Fang, Q. Zhao, D. Liu, C. Qian, Z. Wang, M. Hu, H. Wang, Q. Wu, H. Ji, and M. Wang A survey of self-evolving agents: what, when, how, and where to evolve on the path to artificial super intelligence. Transactions on Machine Learning Research.
[12] Gobet (1998). F. R. Gobet Expert memory: a comparison of four theories.. Cognition66 2, pp. 115–52.
[13] Hawkins et al. (2020). R. Hawkins, M. Kwon, D. Sadigh, and N. Goodman Continual adaptation for efficient machine communication. In Proceedings of the 24th Conference on Computational Natural Language Learning, R. Fernández and T. Linzen (Eds.), Online, pp. 408–419.
[14] He et al. (2026). Y. He, J. Jin, and P. Liu Efficient agent training for computer use. In The Fourteenth International Conference on Learning Representations,
[15] Hu et al. (2022). E. J. Hu, Y. Shen, P. Wallis, Z. Allen-Zhu, Y. Li, S. Wang, L. Wang, W. Chen, et al. Lora: low-rank adaptation of large language models.. Iclr1 (2), pp. 3.
[16] Huang et al. (2024). J. Huang, X. Chen, S. Mishra, H. S. Zheng, A. Yu, X. Song, and D. Zhou Large language models cannot self-correct reasoning yet. In International conference on learning representations, Vol. 2024, pp. 32808–32824.
[17] Jain et al. (2025). N. Jain, J. Singh, M. Shetty, T. Zhang, L. Zheng, K. Sen, and I. Stoica R2E-gym: procedural environment generation and hybrid verifiers for scaling open-weights SWE agents. In Second Conference on Language Modeling,
[18] Jiang et al. (2026). L. Jiang, Y. Chai, M. Li, M. Liu, R. Fok, N. Dziri, Y. Tsvetkov, M. Sap, and Y. Choi Artificial hivemind: the open-ended homogeneity of language models (and beyond). In The Thirty-ninth Annual Conference on Neural Information Processing Systems Datasets and Benchmarks Track,
[19] Jimenez et al. (2024). C. E. Jimenez, J. Yang, A. Wettig, S. Yao, K. Pei, O. Press, and K. Narasimhan Swe-bench: can language models resolve real-world github issues?. In International Conference on Learning Representations, Vol. 2024, pp. 54107–54157.
[20] Kojima et al. (2021). N. Kojima, A. Suhr, and Y. Artzi Continual learning for grounded instruction generation by observing human following behavior. Transactions of the Association for Computational Linguistics9, pp. 1303–1319.
[21] Lin et al. (2025). J. Lin, L. Zettlemoyer, G. Ghosh, W. Yih, A. Markosyan, V. Berges, and B. Oğuz Continual learning via sparse memory finetuning. arXiv preprint arXiv:2510.15103.
[22] Liu et al. (2023). Y. Liu, D. Iter, Y. Xu, S. Wang, R. Xu, and C. Zhu G-eval: NLG evaluation using gpt-4 with better human alignment. In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, Singapore, pp. 2511–2522.
[23] Murty et al. (2024). S. Murty, C. Manning, P. Shaw, M. Joshi, and K. Lee Bagel: bootstrapping agents by guiding exploration with language. arXiv preprint arXiv:2403.08140.
[24] Nilsson et al. (2026). E. Nilsson, I. Huang, and R. Lu Direct agents with visual prompts in design mode.
[25] Ou et al. (2024). T. Ou, F. F. Xu, A. Madaan, J. Liu, R. Lo, A. Sridhar, S. Sengupta, D. Roth, G. Neubig, and S. Zhou Synatra: turning indirect knowledge into direct demonstrations for digital agents at scale. In The Thirty-eighth Annual Conference on Neural Information Processing Systems,
[26] Packer et al. (2023). C. Packer, S. Wooders, K. Lin, V. Fang, S. G. Patil, I. Stoica, and J. E. Gonzalez Memgpt: towards llms as operating systems. arXiv preprint arXiv:2310.08560.
[27] Pan et al. (2025). J. Pan, X. Wang, G. Neubig, N. Jaitly, H. Ji, A. Suhr, and Y. Zhang Training software engineering agents and verifiers with SWE-gym. In Forty-second International Conference on Machine Learning,
[28] Park et al. (2024). C. Park, M. Liu, D. Kong, K. Zhang, and A. E. Ozdaglar RLHF from heterogeneous feedback via personalization and preference aggregation. In ICML 2024 Workshop on Theoretical Foundations of Foundation Models,
[29] Patwardhan et al. (2026). T. Patwardhan, R. Dias, E. Proehl, G. Kim, M. Wang, O. Watkins, S. Fishman, M. Aljubeh, P. Thacker, L. Fauconnet, et al. Gdpval: evaluating ai model performance on real-world economically valuable tasks. In International Conference on Learning Representations, Vol. 2026, pp. 24005–24040.
[30] Pomerleau (1988). D. A. Pomerleau ALVINN: an autonomous land vehicle in a neural network. In Proceedings of the 2nd International Conference on Neural Information Processing Systems, NIPS’88, Cambridge, MA, USA, pp. 305–313.
[31] Rafailov et al. (2023). R. Rafailov, A. Sharma, E. Mitchell, C. D. Manning, S. Ermon, and C. Finn Direct preference optimization: your language model is secretly a reward model. Advances in neural information processing systems36, pp. 53728–53741.
[32] Ross et al. (2011). S. Ross, G. Gordon, and D. Bagnell A reduction of imitation learning and structured prediction to no-regret online learning. In Proceedings of the fourteenth international conference on artificial intelligence and statistics, pp. 627–635.
[33] Shaikh et al. (2025). O. Shaikh, M. Lam, J. Hejna, Y. Shao, H. Cho, M. Bernstein, and D. Yang Aligning language models with demonstrated feedback. In International Conference on Learning Representations, Vol. 2025, pp. 20498–20525.
[34] Shankar et al. (2024). S. Shankar, J. Zamfirescu-Pereira, B. Hartmann, A. Parameswaran, and I. Arawjo Who validates the validators? aligning llm-assisted evaluation of llm outputs with human preferences. In Proceedings of the 37th Annual ACM Symposium on User Interface Software and Technology, pp. 1–14.
[35] Shao et al. (2026). Y. Shao, Z. Z. Wang, N. Ahuja, Y. Wang, B. Liu, and D. Yang CollabSkill: evaluating human-agent collaboration on real-world tasks. arXiv preprint arXiv:2606.09833.
[36] Shen et al. (2025). J. Shen, H. Bai, L. Zhang, Y. Zhou, A. Setlur, S. Tong, D. Caples, N. Jiang, T. Zhang, A. Talwalkar, et al. Thinking vs. doing: agents that reason by scaling test-time interaction. arXiv preprint arXiv:2506.07976.
[37] Song et al. (2026a)Y. Song, L. Chen, F. Tajwar, R. Munos, D. Pathak, D. Bagnell, A. Singh, and A. ZanetteExpanding the capabilities of reinforcement learning via text feedback. In The 1st Workshop on Scaling Post-training for LLMs,
[38] Song et al. (2026b)Y. Song, K. Ramaneti, Z. Sheikh, Z. Chen, B. Gou, T. Xie, Y. Xu, D. Zhang, A. Gandhi, F. Yang, J. Liu, T. Ou, Z. Yuan, F. F. Xu, S. Zhou, X. Wang, X. Yue, T. Yu, H. Sun, Y. Su, and G. NeubigAgent data protocol: unifying datasets for diverse, effective fine-tuning of LLM agents. In The Fourteenth International Conference on Learning Representations,
[39] Sun et al. (2020). Y. Sun, X. Wang, Z. Liu, J. Miller, A. Efros, and M. Hardt Test-time training with self-supervision for generalization under distribution shifts. In International conference on machine learning, pp. 9229–9248.
[40] Tang et al. (2024). Y. Tang, D. Z. Guo, Z. Zheng, D. Calandriello, Y. Cao, E. Tarassov, R. Munos, B. Á. Pires, M. Valko, Y. Cheng, et al. Understanding the performance gap between online and offline alignment algorithms. arXiv preprint arXiv:2405.08448.
[41] Tiwari et al. (2026). R. Tiwari, K. Sareen, L. A. Agrawal, J. E. Gonzalez, M. Zaharia, K. Keutzer, I. S. Dhillon, R. Agarwal, and D. Khatri Learning, fast and slow: towards llms that adapt continually. arXiv preprint arXiv:2605.12484.
[42] Vidgen et al. (2026). B. Vidgen, A. Mann, A. Fennelly, J. W. Stanly, L. Rothman, M. Burstein, J. Benchek, D. Ostrofsky, A. Ravichandran, D. Sur, et al. APEX-agents. arXiv preprint arXiv:2601.14242.
[43] Wang et al. (2024). G. Wang, Y. Xie, Y. Jiang, A. Mandlekar, C. Xiao, Y. Zhu, L. Fan, and A. Anandkumar Voyager: an open-ended embodied agent with large language models. Transactions on Machine Learning Research.
[44] Wang et al. (2025a)X. Wang, B. Wang, D. Lu, J. Yang, T. Xie, J. Wang, J. Deng, X. Guo, Y. Xu, C. H. Wu, et al. Opencua: open foundations for computer-use agents. arXiv preprint arXiv:2508.09123.
[45] Wang et al. (2026a)X. Wang, B. Wang, D. Lu, J. Yang, T. Xie, J. Wang, J. Deng, X. Guo, Y. Xu, C. Wu, et al. Opencua: open foundations for computer-use agents. Advances in Neural Information Processing Systems38, pp. 139756–139806.
[46] Wang et al. (2026b)Y. Wang, X. Chen, X. Jin, M. Wang, and L. YangOpenclaw-rl: train any agent simply by talking. arXiv preprint arXiv:2603.10165.
[47] Wang et al. (2025b)Z. Z. Wang, A. Gandhi, G. Neubig, and D. FriedInducing programmatic skills for agentic tasks. In Second Conference on Language Modeling,
[48] Wang et al. (2025c)Z. Z. Wang, J. Mao, D. Fried, and G. NeubigAgent workflow memory. In Forty-second International Conference on Machine Learning,
[49] Wang et al. (2025d)Z. Z. Wang, Y. Shao, O. Shaikh, D. Fried, G. Neubig, and D. YangHow do ai agents do human work? comparing ai and human workflows across diverse occupations. ArXivabs/2510.22780.
[50] Weidinger et al. (2025). L. Weidinger, I. D. Raji, H. Wallach, M. Mitchell, A. Wang, O. Salaudeen, R. Bommasani, D. Ganguli, S. Koyejo, and W. Isaac Toward an evaluation science for generative ai systems. arXiv preprint arXiv:2503.05336.
[51] Wortsman et al. (2022). M. Wortsman, G. Ilharco, S. Y. Gadre, R. Roelofs, R. Gontijo-Lopes, A. S. Morcos, H. Namkoong, A. Farhadi, Y. Carmon, S. Kornblith, et al. Model soups: averaging weights of multiple fine-tuned models improves accuracy without increasing inference time. In International conference on machine learning, pp. 23965–23998.
[52] Xia et al. (2026). P. Xia, J. Chen, H. Wang, J. Liu, K. Zeng, Y. Wang, S. Han, Y. Zhou, X. Zhao, H. Chen, et al. Skillrl: evolving agents via recursive skill-augmented reinforcement learning. arXiv preprint arXiv:2602.08234.
[53] Xu et al. (2024a)F. F. Xu, Y. Song, B. Li, Y. Tang, K. Jain, M. Bao, Z. Z. Wang, X. Zhou, Z. Guo, M. Cao, et al. Theagentcompany: benchmarking llm agents on consequential real world tasks. arXiv preprint arXiv:2412.14161.
[54] Xu et al. (2024b)W. Xu, G. Zhu, X. Zhao, L. Pan, L. Li, and W. WangPride and prejudice: llm amplifies self-bias in self-refinement. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 15474–15492.
[55] Xu et al. (2026). W. Xu, Z. Liang, K. Mei, H. Gao, J. Tan, and Y. Zhang A-mem: agentic memory for llm agents. Advances in Neural Information Processing Systems38, pp. 17577–17604.
[56] Yuksekgonul et al. (2026). M. Yuksekgonul, D. Koceja, X. Li, F. Bianchi, J. Mc Caleb, X. Wang, J. Kautz, Y. Choi, J. Zou, C. Guestrin, et al. Learning to discover at test time. arXiv preprint arXiv:2601.16175.
[57] Zhao et al. (2026). S. Zhao, Z. Xie, M. Liu, J. Huang, G. Pang, F. Chen, and A. Grover Self-distilled reasoner: on-policy self-distillation for large language models. In ICLR 2026 Workshop on Lifelong Agents: Learning, Aligning, Evolving,
[58] Zheng et al. (2025). B. Zheng, M. Y. Fatemi, X. Jin, Z. Z. Wang, A. Gandhi, Y. Song, Y. Gu, J. Srinivasa, G. Liu, G. Neubig, et al. Skillweaver: web agents can self-improve by discovering and honing skills. arXiv preprint arXiv:2504.07079.
[59] Zheng et al. (2023). L. Zheng, W. Chiang, Y. Sheng, S. Zhuang, Z. Wu, Y. Zhuang, Z. Lin, Z. Li, D. Li, E. Xing, et al. Judging llm-as-a-judge with mt-bench and chatbot arena. Advances in neural information processing systems36, pp. 46595–46623.
[60] Zhou et al. (2024). Y. Zhou, A. Zanette, J. Pan, S. Levine, and A. Kumar Archer: training language model agents via hierarchical multi-turn rl. arXiv preprint arXiv:2402.19446.
