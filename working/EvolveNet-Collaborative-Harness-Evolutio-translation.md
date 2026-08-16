---
created: 2026-08-17
updated: 2026-08-17
title: EvolveNet：面向智能体自我改进的协作式 Harness 进化
sourceUrl: https://arxiv.org/abs/2608.04968
sourceAuthor: Jun Nie、Yonggang Zhang、Qianshu Cai、Yiu-ming Cheung、Xinmei Tian、Bo Han
translatedAt: 2026-08-17
sources: [references/articles.md 待处理队列]
tags: [AI Agent, Harness 工程, 联邦学习, 程序聚合, 自进化智能体, 智能体协作, type/翻译]
---

# EvolveNet：面向智能体自我改进的协作式 Harness 进化

> arXiv:2608.04968（cs.LG，2026-08-05 提交）| 代码：[github.com/junnie00/EvolveNet](https://github.com/junnie00/EvolveNet)
> 作者：Jun Nie、Yonggang Zhang、Qianshu Cai、Yiu-ming Cheung、Xinmei Tian、Bo Han（中国科学技术大学 / 香港科技大学 / 香港浸会大学）

## 摘要

LLM 智能体的能力不仅取决于其模型，还取决于 harness——即构造上下文、调用工具、校验结果并从失败中恢复的可执行程序。近期工作表明，进化 harness 无需更新模型权重就能带来持久的改进。然而，既有方法都假设所有执行经验可以汇总给单一优化器，让它沿一条串行轨迹进化一个 harness。真实的智能体生态违背了这一假设：用户、组织与环境产生的经验流相互隔离、无法汇总，因此最值得学习的经验恰恰是无法直接集中化的那部分。我们提出 EvolveNet——一种把经验提取下放到数据端的协作式 harness 进化范式。一个共享 harness 被广播到多个数据本地（data-local）的智能体部署，各自在自己的负载上演化它；只有由此产生的程序适配被组合进更新后的共享 harness 并重新分发，于是每个参与智能体都能继承其他智能体发现的运维经验。通过把聚合边界从原始负载转移到学到的适配，EvolveNet 既保持了负载的本地性，又允许多条进化搜索并发进行、降低串行深度。由于独立修改过的程序无法像模型参数那样求平均、组合时可能冲突，EvolveNet 引入了作用域类型化（scope-typed）、证据引导（evidence-guided）的程序聚合。在覆盖 text-to-SQL、数据科学编码、竞赛编程、软件工程与智能体工作流的五类场景中，EvolveNet 在全部五处都改进了共享 harness，且异构负载下增益最大；消融实验把改进归因于不同智能体适配的组合，而非对它们的挑选。

## 1 引言

LLM 智能体并非只由模型定义。其行为还关键地取决于周围的 harness：构造上下文、调用模型与工具、校验中间结果，并决定系统如何响应失败的可执行程序（[6](#bib.bib6)；[14](#bib.bib14)；[28](#bib.bib28)；[18](#bib.bib18)）。两个基于同一冻结模型构建的智能体，可能仅仅因为 harness 实现了不同的推理流程、工具使用策略与恢复机制，就表现出截然不同的能力。这一观察推动了一条日益壮大的研究线：改进模型周围的程序，包括提示词优化、工作流搜索，以及对智能体源代码的直接进化（[31](#bib.bib31)；[4](#bib.bib4)；[7](#bib.bib7)；[29](#bib.bib29)）。更新近的研究把 harness 本身当作适配的持久状态，表明智能体可以在不改动底层模型权重的情况下获得持久的行为改进（[6](#bib.bib6)；[14](#bib.bib14)；[28](#bib.bib28)；[18](#bib.bib18)）。

然而，既有的 harness 进化方法大体沿袭集中式范式：负载、执行轨迹与行为反馈必须先交给单一优化器，由它从中提取有用经验，并沿一条大体串行的轨迹进化一个 harness。当所有经验都集中可访问时，这种范式是自然的；但它把分布式经验的利用与负载的集中化耦合在一起。而且随着负载不断加入，这些负载的适配仍须通过同一个进化程序去探索，既限制了搜索的广度，也限制了 harness 进化的串行效率。

真实的智能体部署天然分布在用户、组织、数据库、代码仓库与工具环境之间。这提示我们颠倒经验提取与聚合的顺序：与其先把含有有用经验的负载汇总起来再集中学习，不如让每个部署先把它的本地执行与失败翻译成一个改进后的 harness，然后再聚合由此产生的程序适配。换句话说，跨越系统边界的对象从「承载经验的负载」变成了「从经验中学到的可执行表示」。

这一转变创造了智能体自我进化的不同范式。本地负载可以留在原地，多个部署则并发探索不同的进化轨迹；它们的发现随后累积进一个共享 harness 并重新分发，使每个客户端从其他客户端发现的适配出发开始下一轮。并行的本地进化并不会减少搜索的总量，但会降低其串行深度：客户端阶段由最慢的并发分支决定，而不是由所有本地搜索之和决定。

我们提出 **EvolveNet** 来实现这一范式。EvolveNet 每轮从一个共同的共享 harness 出发，把它广播给多个数据本地客户端，让它们在各自本地负载上独立进化。每个客户端由此把本地运维经验提取进一个专家程序（specialist program）。服务端随后把返回的适配整合进更新后的共享 harness 并重新分发，作为下一轮的共享起点。因此，EvolveNet 用「先本地进化、再聚合」的循环取代了传统的「先聚合数据、再进化」流水线，把分布式本地搜索变成单个可执行智能体系统中的累积进步。

关键障碍是聚合，而且它并非联邦优化所解决的那类问题：被组合的对象既不是参数向量，也不是带有预定义组合规则的模块集合，而是互相作用的可执行程序——其语义只有在运行时才显现。在参数空间聚合中，本地学到的信息编码为向量，可以通过加权平均等算术运算组合。harness 适配是源代码级修改：它们没有有意义的算术平均，且单独有益的编辑在组合后可能变得冗余、矛盾或无效。一个客户端可能加强某条校验规则，而另一个客户端把它删掉；两个客户端可能出于不同的本地原因改动同一条控制路径；一条本地有用的提示词编辑可能损害其他地方的行为。因此，协作式 harness 进化依赖的不只是通信，而是判定哪些适配可迁移、本地特化应如何保留，以及它们的组合能否保住既有能力。

EvolveNet 通过证据引导、作用域类型化的程序聚合应对这一挑战。所有客户端都从同一个广播 harness 出发，使服务端能够基于它们相对同一共同基线的程序增量（program delta）进行推理。每个增量都附带实测的行为变化，使服务端既能整合互补的机制，又能区分「全局可迁移行为」与「应保持领域条件化的适配」。候选合并体在被确定为下一轮共享 harness 之前，会先经过行为验证。客户端被鼓励在自己的负载切片上特化，使并行搜索产出互补而非冗余的适配。

因此，每一轮形成一个双向适配循环：本地专家与共享 harness 相互塑造——每个专家都从当前共享程序进化而来，而下一个共享程序则由这些专家发现的适配组合而成。这里的协作以产物为媒介，而非交互式的：客户端在一轮之内既不通信也不协调；一方发现的经验只能通过重新分发的 harness 传递给其他方。

评估聚合算子需要把它自身的贡献与本地 harness 进化固有的随机性和路径依赖分开。因此我们引入配对评估协议：让相互竞争的聚合规则作用于同一份本地进化客户端程序的快照，从而把「由聚合造成的差异」与「各规则收到的客户端群体差异」分开。

在覆盖 text-to-SQL、数据科学编码、竞赛编程、软件工程与智能体工作流的五类场景中，EvolveNet 在全部五处都改进了共享 harness，并把多条本地进化轨迹变成任何单一客户端都未曾产生的行为。我们的贡献如下：

- 我们提出**协作式 harness 进化**——一种把经验提取从集中式优化器下放到数据本地智能体部署、并聚合由此产生的可执行适配（而非产生它们的负载）的范式。这使分布式经验能在一个共享 harness 中累积，同时本地进化搜索并发进行（第 [4](#S4) 节）。
- 我们指出**程序聚合是该范式的核心技术挑战**，并开发了一个证据引导、作用域类型化的聚合算子：整合相对共同基线的 harness 增量，把可迁移机制提升为全局行为，并在条件化作用域下保留领域专属适配（第 [4.3](#S4.SS3) 节）。
- 我们建立了一套把「聚合质量」与「本地进化的随机性」分开的评估协议，并应用于五类场景。不同客户端发现的互补适配累积进一个共享 harness，异构负载下增益最大；同时并行本地进化降低了搜索的串行深度，每轮只需一次服务端聚合会话（第 [6.2](#S6.SS2)–[6.8](#S6.SS8) 节）。

## 2 相关工作

##### 围绕冻结模型优化程序。

大量工作通过优化模型周围的结构（而非权重）来改进 LLM 系统。提示词优化通过迭代精修、进化搜索或把 LLM 本身当作优化器来搜索指令（[31](#bib.bib31)；[4](#bib.bib4)；[23](#bib.bib23)；[5](#bib.bib5)）；DSPy 优化多阶段流水线（[12](#bib.bib12)）；自动化智能体设计则在工具使用工作流与控制结构上搜索（[7](#bib.bib7)；[30](#bib.bib30)）。一条紧密相关的研究线把可执行程序本身当作改进对象——STOP 递归改进生成代码的程序（[27](#bib.bib27)），FunSearch 让语言模型与程序评估结对（[20](#bib.bib20)），Darwin Gödel Machine 探索开放式自我修改（[29](#bib.bib29)），MOSS 重写智能体自身的源代码（[1](#bib.bib1)）；而最近期的工作把智能体的 harness 当作适配的持久状态，优化组织模型调用、工具、反馈与恢复的控制程序（[6](#bib.bib6)；[14](#bib.bib14)；[28](#bib.bib28)；[18](#bib.bib18)）。这些方法通常实例化为对集中可访问经验的单一优化过程，产出一条进化轨迹。它们研究**一个**智能体如何改进；EvolveNet 研究**许多**智能体发现的改进如何累积进一个共享的进化产物。EvolveNet 追问的是：当经验被切分到多个部署、无法集中化时，会发生什么改变。

##### 通过共享产物协作改进。

一条研究线让分布式智能体通过交换学到的产物（而非产生它们的数据）来协作。FederatedSkill 共享语义技能差异（skill diff），由服务端折叠进共享技能库（[24](#bib.bib24)）；Fed-SE 跨环境聚合参数高效适配器更新（[2](#bib.bib2)）；Federation over Text 把客户端的推理轨迹蒸馏成共享文本洞察库（[25](#bib.bib25)）。它们都继承了去中心化模型训练的「广播–优化–聚合–重分发」节奏，从 FedAvg（[17](#bib.bib17)）到应对不稳定与统计异质性的方法（[16](#bib.bib16)；[11](#bib.bib11)；[19](#bib.bib19)）。EvolveNet 与这些系统共享高层通信模式，但它优化的对象以及该对象引发的聚合问题属于不同种类。上述方法都假设客户端更新可以表达在一个预定义聚合空间里——权重张量、适配器、技能列表、文本洞察集合——其中「组合」是先验定义良好的。而这里的聚合空间本身就是一门编程语言：两个贡献能否组合，是关于执行的事实，而非表示的性质。EvolveNet 流通的是可执行控制程序本身，目标是单一的作用域条件化共享产物，而不是独立补丁、洞察或适配器权重的库。这改变了聚合的含义：技能补丁靠插入组合，洞察靠拼接组合，而程序编辑通过控制流、提示词、工具调用与运行时状态相互作用，因此服务端不能依赖求平均、数值距离或任何基于梯度的「一致性」概念，而必须对程序行为进行推理。

推理时还有另一种协作：智能体交换消息、辩论或委派子任务来回答单个查询（[3](#bib.bib3)；[21](#bib.bib21)）。EvolveNet 的协作跨适配轮进行：它的客户端在一轮之内独立进化、从不交换消息，它们的贡献只在一个持续累积并重分发的共享 harness 中相遇。

##### 模型合并。

模型合并在不重训于数据并集的前提下，把相对共同基线独立获得的能力整合起来。Task Arithmetic 把微调模型表示为参数位移再组合（[8](#bib.bib8)）；TIES-Merging 通过移除弱更新、解决符号冲突来降低干扰（[22](#bib.bib22)）；DARE 在合并前对增量做稀疏化与重缩放（[26](#bib.bib26)）。EvolveNet 与它们共享「相对共享基线组合能力、同时管理干扰」的目标，但聚合空间有本质不同：神经检查点允许逐坐标算术，而源代码编辑没有内在的幅度、方向或逐元素对应关系，语法上有效的编辑也可能以无法仅从编辑本身推断的方式相互作用。因此 EvolveNet 用执行派生的行为证据来引导整合并验证整合，目标不仅是挑选完整的客户端程序，而是保留并组合分散在它们之中的可迁移适配。

## 3 预备知识

##### Harness。

设 $M$ 为冻结的 LLM。harness $h$ 是一个可执行程序：给定输入 $x$，它可以任意次调用 $M$、执行工具、检查结果，并返回答案 $h(x)$。harness 空间 $\mathcal{H}$ 是满足两个不变量的程序空间（第 [5](#S5) 节）：模型永不被改动，且推理时永不去读金标准标签。

我们的本地进化循环实例化了 TTHE（[18](#bib.bib18)）的轨迹驱动 harness 进化：一个 LLM 提议器读取执行轨迹并编辑 harness 源代码。

##### 分布式设定。

我们考虑 $K$ 个「数据本地」的智能体部署：每个部署运行在其负载产生之处，进化也发生在这里而非中心站点。在协议中我们称它们为**客户端**。客户端 $k$ 持有一份无法与其他客户端合并的工作负载 $D_{k}$。客户端 $k$ 可以在 $D_{k}$ 上执行 harness、观察轨迹，并在自己的数据上给结果打分。原始负载与执行记录留在本地；跨越边界的是程序文本、它相对共同基线的增量，以及逐项的行为判定。

##### 目标。

我们寻求一个共享 harness $h^{\star}$，使目标负载 $\mathcal{P}_{\mathrm{target}}$ 上的期望准确率最大；进化期间只能使用客户端的本地进化与服务端的聚合。进化过程中只能访问客户端混合分布；目标分布可能还包含任何客户端都不持有的相关领域——我们的一个评估领域正是如此。

**图 1：** 左：传统 harness 进化是串行的。一个优化器按顺序消费输入批次，每个 harness 必须产出后才能探索下一个，因此 $T$ 阶段搜索的串行深度为 $T$，只沿一条轨迹。右：EvolveNet 把共享 harness $h^{(t)}$ 广播给 $K$ 个客户端，它们并行地在各自持有的负载上把它进化成专家 $h_{k}^{(t)}$。服务端聚合返回的程序（而非它们背后的负载）：当支持某机制的证据跨域时全局采纳，否则把它条件化在主域上；只有当结果通过逐项验收测试时才提交为 $h^{(t+1)}$（第 [4.4](#S4.SS4) 节）。虚线边闭合了循环：被提交的 harness 会被重新分发，因此每个客户端下一轮进化的起点是「整个协作学到的内容」，而非它自己上一轮的程序。

## 4 方法：EvolveNet

设 $M$ 为冻结语言模型，harness $h\in\mathcal{H}$ 为组织对 $M$ 的调用、调用工具、构造上下文、校验中间结果并处理失败的可执行程序。我们考虑 $K$ 个客户端，其中客户端 $k$ 持有一份来自部署领域 $d_{k}$ 的本地负载 $D_{k}^{\mathrm{tr}}$。原始负载保留在各自客户端。我们的目标是构造一个单一共享 harness，累积跨这些领域发现的有用适配：

```
h^{\star}=\arg\max_{h\in\mathcal{H}}\mathbb{E}_{z\sim\mathcal{P}_{\mathrm{target}}}\left[s(h;z)\right],
```
（式 1）

其中 $\mathcal{P}_{\mathrm{target}}$ 是共享 harness 必须服务的部署分布，$s$ 是任务专属的评估函数。进化期间 EvolveNet 只能访问客户端混合分布 $\mathcal{P}_{\mathrm{client}}=\sum_{k=1}^{K}\pi_{k}\mathcal{P}_{k}$，其中 $\mathcal{P}_{k}$ 是客户端 $k$ 的部署分布、$\pi_{k}$ 是它的混合权重；$\mathcal{P}_{\mathrm{client}}$ 可能只覆盖 $\mathcal{P}_{\mathrm{target}}$ 的一部分，我们的评估就包含一个任何客户端都不持有的领域（表 [2](#S6.T2)）。模型 $M$ 全程保持不变；所有适配都发生在 harness 中。

### 4.1 从集中式进化到协作式 harness 进化

传统 harness 进化遵循「先聚合负载、再进化」的范式：负载、执行轨迹与行为反馈先交给集中式优化器，它从中提取有用经验，并沿一条单一进化轨迹更新一个 harness。概念上即：

```
\underbrace{\operatorname{Pool}\left(D_{1}^{\mathrm{tr}},\ldots,D_{K}^{\mathrm{tr}}\right)\;\longrightarrow\;\operatorname{Evolve}}_{\text{centralized harness evolution}}.
```
（式 2）

这种设计把经验提取与负载集中化耦合在一起，还把全部适配压力压在一个进化程序上：更多负载可以扩大可用经验，但它们的适配仍须通过同一个中央搜索过程发现。

EvolveNet 把进化与聚合都分布化。每个客户端从同一个广播 harness 出发，独立运行本地进化算子；只有相对共同基线的程序增量被返回给服务端聚合：

```
\underbrace{\operatorname{Evolve}_{1:K}\left(h^{(t)},D_{1:K}^{\mathrm{tr}}\right)\;\longrightarrow\;\operatorname{Aggregate}\left(\Delta_{1:K}^{(t)}\right)}_{\text{collaborative harness evolution}}.
```
（式 3）

在第 $t$ 轮，所有客户端收到同一个共享 harness $h^{(t)}$。客户端 $k$ 应用本地进化算子 $\mathcal{E}$ 得到：

```
h_{k}^{(t)}=\mathcal{E}\left(h^{(t)},D_{k}^{\mathrm{tr}}\right).
```
（式 4）

本地提议器被鼓励特化到领域 $d_{k}$ 中反复出现的结构与失败模式，而不是复刻一个所有客户端都已可用的通用方案。广播 harness 始终保留在本地候选池中。因此，若 $S_{k}$ 表示客户端侧的选择分数，则有：

```
S_{k}\!\left(h_{k}^{(t)}\right)\geq S_{k}\!\left(h^{(t)}\right),
```
（式 5）

精度到客户端评估器的分辨率为止。本地特化由此产出候选能力，且不强迫客户端返回一个在自己的负载上明显劣于共享起点的程序。

服务端把返回的适配整合进候选共享 harness：

```
\widetilde{h}^{(t+1)}=\mathcal{A}\left(h^{(t)},h_{1}^{(t)},\ldots,h_{K}^{(t)}\right),
```
（式 6）

经过行为验证后，把它作为下一轮的起点重新分发。这就产生了周而复始的「特化 → 聚合 → 重分发」循环。本地发现的适配因此不是客户端的终态产物：一旦整合进共享 harness，它们就构成下一轮所有客户端进化的初始状态。这正是本地专家与共享 harness 共同进化的含义——每个专家从当前共享程序进化而来，而下一个共享程序由这些专家产生的适配组装而成。客户端在一轮之内不直接交互；它们的耦合通过跨轮的共享可执行产物发生。

这一范式转变也改变了搜索的串行结构。设 $C_{k}^{(t)}$ 为客户端 $k$ 第 $t$ 轮本地搜索的延迟，$C_{\mathcal{A}}^{(t)}$ 与 $C_{\mathrm{val}}^{(t)}$ 为聚合与验证延迟。串行执行同样的 $K$ 次本地搜索需要
$C_{\mathrm{serial}}^{(t)}=\sum_{k}C_{k}^{(t)}+C_{\mathcal{A}}^{(t)}+C_{\mathrm{val}}^{(t)}$，
而 EvolveNet 的并行客户端阶段的串行深度为：

```
C_{\mathrm{EvolveNet}}^{(t)}=\max_{k}C_{k}^{(t)}+C_{\mathcal{A}}^{(t)}+C_{\mathrm{val}}^{(t)}.
```
（式 7）

EvolveNet 并不消除本地搜索的计算成本；它让多条进化轨迹以「由最慢客户端决定、而非由它们之和决定」的串行深度并行可用。

### 4.2 程序聚合的挑战

上述范式依赖一个在参数空间聚合中没有直接对应物的聚合操作。模型更新位于公共向量空间，可以通过逐坐标算术组合（如权重平均，[17](#bib.bib17)）。源代码程序则不能。两个 Python harness 之间不存在有意义的平均值，独立有用的修改放在同一个可执行系统中未必还有用。

程序聚合必须应对三个相互耦合的困难。第一，**归因**（attribution）：返回的程序可能包含多个相互作用的编辑，服务端必须判断哪些行为变化与该客户端变体相关。第二，**干扰**（interference）：两个适配可能冗余、可能以不兼容的方式改动同一条控制路径，也可能编码对部署领域的不同假设。第三，**回退**（regression）：语法有效且单独成功的编辑，组合后仍可能破坏共享 harness 中已有的能力。

EvolveNet 通过四个相互关联的原则应对：所有客户端对照同一共同程序基线；源代码级变更附带实测行为证据；候选机制在组合前被赋予显式部署作用域；组合后的程序在取代当前共享 harness 之前先经过行为评估。

### 4.3 证据引导、作用域类型化的程序聚合

##### 共同基线程序增量。

因为每个客户端都从同一个 $h^{(t)}$ 出发，它的贡献可以表示为：

```
\Delta_{k}^{(t)}=\operatorname{diff}\left(h^{(t)},h_{k}^{(t)}\right).
```
（式 8）

服务端编辑 $h^{(t)}$ 的逐字节副本，而不是从 $K$ 份完整文件合成新程序。这种共同基线表示有两个用途：它使客户端贡献直接可比（每个增量都表达相对同一行为状态改变了什么），并限制了「拼接整个客户端程序」造成的失控产物增长。

聚合器把每个增量分解为候选**机制**（mechanism）。机制是语义连贯的适配，实现某个可识别行为——例如执行重试规则、模式探针、输出格式约束或仓库专属修复流程。机制不必与某一块语法 diff 精确对应：几处邻近的编辑可能共同实现一个行为。

##### 行为证据。

源代码本身不能揭示客户端修改是否有用。因此，客户端 $k$ 在选择本地程序时，会把自己的负载上 $h_{k}^{(t)}$ 与广播 harness 进行比较，并报告由此产生的行为变化。设 $v_{i}(h)\in\{0,1\}$ 为任务评估器对条目 $i$ 的判定。我们定义：

```
\displaystyle F_{k}^{(t)} \displaystyle=\left\{i\in D_{k}^{\mathrm{tr}}:v_{i}\!\left(h^{(t)}\right)=0,\,v_{i}\!\left(h_{k}^{(t)}\right)=1\right\},
```
（式 9）

```
\displaystyle B_{k}^{(t)} \displaystyle=\left\{i\in D_{k}^{\mathrm{tr}}:v_{i}\!\left(h^{(t)}\right)=1,\,v_{i}\!\left(h_{k}^{(t)}\right)=0\right\},
```
（式 10）

并把 $e_{k}^{(t)}=(F_{k}^{(t)},B_{k}^{(t)})$ 附到相应程序增量上。证据记录了相对共同基线「新获得了哪些能力、丢失了哪些能力」。它本身并不建立从每个条目到特定代码行的因果映射；而是用可观测行为约束聚合器对增量的解释。聚合算子现在可以更精确地写成：

```
\widetilde{h}^{(t+1)}=\mathcal{A}\left(h^{(t)},\left\{\left(\Delta_{k}^{(t)},e_{k}^{(t)}\right)\right\}_{k=1}^{K}\right).
```
（式 11）

##### 采纳问题。

聚合不是自由形式的改写。把 $K$ 个增量分解后得到候选集 $\mathcal{M}=\{m_{1},\dots,m_{n}\}$，每个 $m_{j}$ 携带其来源客户端的证据。一次**采纳**（adoption）是一个二元组 $(S,\tau)$：要并入的子集 $S\subseteq\mathcal{M}$ 及其成员的作用域指派 $\tau$，二者共同决定一个组合程序 $h(S,\tau)$。记 $\mathrm{Fix}(S,\tau)$ 与 $\mathrm{Brk}(S,\tau)$ 为服务端验证切片 $D^{\mathrm{val}}$ 中由 $h(S,\tau)$ 相对 $h^{(t)}$ 新解出与新失败的条目，服务端求解：

```
\max_{S\subseteq\mathcal{M},\;\tau}\;\left|\mathrm{Fix}(S,\tau)\right|\quad\text{subject to}\quad\left|\mathrm{Brk}(S,\tau)\right|\leq\left|\mathrm{Fix}(S,\tau)\right|.
```
（式 12）

这就是程序空间中的聚合问题，而且无法用搜索求解：目标与约束都要靠**执行** $h(S,\tau)$ 定义，因此 $2^{|\mathcal{M}|}$ 个子集及其作用域指派每一种都耗费一整轮评估；机制又相互影响，目标对 $S$ 既不满足可加性也不单调。EvolveNet 因此把式 [12](#S4.E12) 拆成「提议步骤」与「精确可行性检查」。作用域类型化聚合器（第 [4.3](#S4.SS3) 节）通过推理附带证据在单次遍历中提出一个 $(S,\tau)$，而非枚举；验收门控（第 [4.4](#S4.SS4) 节）随后评估实现出来的程序并精确执行约束，提案失败即拒绝。聚合器提供的是「采纳**哪些**机制、它们应作用于**哪里**」的启发式；门控提供的是「被采纳的提案确实满足式 [12](#S4.E12)」的保证。

##### 作用域类型化组合。

核心决策不是简单地接受或拒绝一个机制，而是该机制应作用于**哪里**。组合之前，每个候选机制 $m$ 都获得一个作用域：

```
\tau(m)\in\left\{\textsc{global}\right\}\cup\left\{\textsc{home}(d_{k})\right\}_{k=1}^{K}.
```
（式 13）

记 $\mathrm{ev}(m)$ 为归功于 $m$ 的条目，指派遵循唯一规则：

```
\tau(m)=\begin{cases}\textsc{global}&\text{if }\mathrm{ev}(m)\text{ meets two or more domains, or }m\text{ addresses a domain-independent failure mode,}\\
\textsc{home}(d_{k})&\text{if }\mathrm{ev}(m)\subseteq D_{k}^{\mathrm{tr}}\text{ for exactly one }k,\\
\bot\ \text{(reject)}&\text{if }\mathrm{ev}(m)\text{ is a single item.}\end{cases}
```
（式 14）

领域无关的失败模式是指证据原则上就无法本地化的那类——输出畸形、执行失败、普遍适用的恢复流程。全局机制以「应用于每个输入的单一实现」进入；主域 $d_{k}$ 机制以条件化方式进入，只有当 harness 观察到当前输入属于 $d_{k}$ 时才激活；最后一种情况剔除的是编码单个问题怪癖、而非某类反复问题的适配。

这一区分改变了程序冲突的结构。假设两个客户端以不兼容的方式修改同一行为，但各自修改的证据都局限于不同领域。参数空间聚合器要么平均这两个更新，要么二选一。EvolveNet 可以在不相交的领域条件下同时保留两个适配，于是许多表面冲突变成「条件化组合」而非「赢家通吃」。

这一性质并非无条件成立；它的要求可以精确陈述。设 $\kappa(x)$ 为 harness 对输入 $x$ 观察到的分派键。

**命题 1（作用域隔离）。** 设 $m$ 以作用域 $\textsc{home}(d)$ 被采纳，且其贡献的每条语句只在测试 $\kappa(x)=d$ 的守卫下可达。若 $m$ 不写入该守卫之外会被读取的任何状态、也不改动该守卫之外应用的任何提示词文本，那么对每个满足 $\kappa(x)\neq d$ 的输入 $x$，都有 $h(S\cup\{m\},\tau)(x)=h(S,\tau)(x)$。

**命题 2（不相交作用域下的冲突）。** 设 $m_{i}$ 与 $m_{j}$ 以作用域 $\textsc{home}(d_{i})$、$\textsc{home}(d_{j})$ 满足命题 1 的假设，且 $d_{i}\neq d_{j}$。那么无论 $m_{i}$ 与 $m_{j}$ 对同一行为做什么，$h(S\cup\{m_{i},m_{j}\},\tau)$ 在领域 $d_{i}$ 的每个输入上都与 $h(S\cup\{m_{i}\},\tau)$ 一致，在领域 $d_{j}$ 的每个输入上都与 $h(S\cup\{m_{j}\},\tau)$ 一致。

两者都来自同一个观察：在上述假设下，主域作用域机制的语句在其领域之外不可达，且该执行路径上读取的任何对象都未被改动，因此两个程序诱导出相同轨迹。命题 [2](#Thmproposition2) 正是上面冲突处理方式的依据：两个以相反方向改动同一行为的客户端，只要证据落在不同领域，就根本无须仲裁——因为每一方在另一方生效之处都不可达。参数空间聚合器没有对应操作——逐坐标组合无法让一个更新「条件化于将来要问它的那个输入」。

这两个命题的价值在于把所需的隔离假设显式化，而非证明本身。它们精确陈述了「领域条件化要按构造限制干扰，实现必须遵守什么」，也是聚合器把主域材料作为守卫扩展引入、而不是作为对共享提示词结构的编辑引入的原因。当假设失败——机制越过守卫触碰共享状态——隔离不成立，此时式 [12](#S4.E12) 的约束会检测到它。涉及真正共享行为的冲突，或通过公共状态相互作用的机制，仍需聚合器二选一。对以主域作用域采纳的机制，服务端倾向于保留客户端经过验证的实现而非改写它，因为源代码级重写可能去掉产生实测增益的那个行为。

##### 采纳流程。

式 [12](#S4.E12) 分五步逼近。(i) 把每个 $h_{k}^{(t)}$ 与 $h^{(t)}$ 做 diff，隔离客户端 $k$ 添加了什么。(ii) 阅读该增量附带的执行轨迹。(iii) 把编辑归组为机制，并把 $F_{k}^{(t)}$ 中归功于它的条目附上。(iv) 按式 [14](#S4.E14) 对每个机制分类。(v) 组合：每个全局机制一份实现；每个主域 $d$ 机制原样复制进以 $d$ 守卫的分支；不相交主域且冲突的机制同时保留——只有全局冲突才按分级证据仲裁。

步骤 (i)–(iii) 是机械性的。步骤 (iv) 与 (v) 由 LLM 合并器按上述标准结合附带证据执行，因为判定「一个机制的证据可否本地化、如何放置而不扰动基线」需要读程序而不是打分。这一划分使算子可测试：步骤 (iv) 是第 [6.4](#S6.SS4) 节聚合变体唯一改动的地方，因此它们的差异可完全归因于分类规则；而步骤 (v) 的输出在提交之前会对照式 [12](#S4.E12) 精确核验。

##### 保留共享基线。

共享 harness 不是可丢弃的源文本。它代表前几轮累积的行为状态，因此在聚合期间充当一组承重不变量。这对提示词规则尤其重要：与条件化代码路径不同，一条既有提示词指令可能影响每个输入。改写或「合并」这样一条规则，可能引入与所采纳机制无关的全系统变化。因此，聚合器就地修改广播 harness，保留既有提示词规则，尽可能把新机制作为局部化扩展整合。实现还约束了相对基线 harness 的增长；确切预算设置在实验配置中给出。这些限制并不能让组合零风险，但减少了单次合并改变的无辜行为数量。

### 4.4 行为提交与回滚

程序组合可能引入无法仅从源码 diff 可靠判定的回退。EvolveNet 因此把候选共享 harness 的**构造**与对它的**提交**分开。设 $D^{\mathrm{val}}$ 为与产生候选所用的客户端负载、以及最终测试集都不相交的验证切片。相对上一个共享 harness $h^{(t)}$，定义：

```
\displaystyle F_{\mathrm{val}} \displaystyle=\left\{i\in D^{\mathrm{val}}:v_{i}\!\left(h^{(t)}\right)=0,\,v_{i}\!\left(\widetilde{h}^{(t+1)}\right)=1\right\},
```
（式 15）

```
\displaystyle B_{\mathrm{val}} \displaystyle=\left\{i\in D^{\mathrm{val}}:v_{i}\!\left(h^{(t)}\right)=1,\,v_{i}\!\left(\widetilde{h}^{(t+1)}\right)=0\right\}.
```
（式 16）

候选被提交当且仅当：

```
\left|F_{\mathrm{val}}\right|\geq\left|B_{\mathrm{val}}\right|.
```
（式 17）

门控逐项比较行为转移，而不是相减聚合分数。两个相近 harness 之间大多数条目不变；聚焦于翻转的条目，使决策取决于合并引入的行为差异。

当候选未通过测试，聚合器会收到观测到的回退，并被允许修订一次。若修订后的候选仍失败，本轮回滚到 $h^{(t)}$。回滚始终指向上一轮共享 harness，而非表现最好的客户端，从而维持「每轮都从一个共享程序状态出发」的不变量。门控在式 [17](#S4.E17) 的标准下保护已提交的验证轨迹；它不保证在未见测试分布上改进。它的作用更窄：防止「实测回退多于实测增益」的聚合成为所有后续本地搜索的共享起点。由于该测试只消费逐项判定，它也可以在不集中验证条目的情况下计算：把切片分给各客户端，每个返回两个整数，服务端求和，即可复现相同的接受/拒绝决策。修订步骤则不同——它向聚合器展示哪些条目回退了——因此「两整数」变体支持门控但不支持修订。

### 4.5 完整 EvolveNet 流程

**算法 1：EvolveNet——一个通信轮**

```
1:  输入：共享 harness h^{(t)}；客户端负载 D_{1:K}^{tr}；验证切片 D^{val}；本地搜索预算 (E,G)
2:  对 k=1 到 K 并行执行：
3:      h_k^{(t)} ← LocalEvolve(h^{(t)}, D_k^{tr}, E, G)
4:      Δ_k^{(t)} ← diff(h^{(t)}, h_k^{(t)})
5:      e_k^{(t)} ← BehaviorChanges(h_k^{(t)}, h^{(t)}; D_k^{tr})
6:  结束 for
7:  h̃^{(t+1)} ← ScopeAggregate(h^{(t)}, {(Δ_k^{(t)}, e_k^{(t)})}_{k=1}^K)
8:  (F_val, B_val) ← Compare(h̃^{(t+1)}, h^{(t)}; D^{val})
9:  如果 |B_val| > |F_val| 则：
10:     h̃^{(t+1)} ← ReviseAggregate(h^{(t)}, {(Δ_k^{(t)}, e_k^{(t)})}_{k=1}^K, B_val)
11:     重新计算 (F_val, B_val)
12:  结束 if
13:  h^{(t+1)} ← h̃^{(t+1)}（若 |F_val| ≥ |B_val|），否则 h^{(t)}
14:  返回 h^{(t+1)}
```

算法 [1](#alg1) 陈述了一轮。服务端把 $h^{(t)}$ 广播给全部 $K$ 个客户端。每个客户端在本地负载上独立进化它，返回专家 harness $h_{k}^{(t)}$、其共同基线增量及其行为证据。服务端把增量分解为候选机制，为每个机制指派全局或主域作用域，并把它们组合成 $\widetilde{h}^{(t+1)}$。候选与 $h^{(t)}$ 在 $D^{\mathrm{val}}$ 上比较，只有通过式 [17](#S4.E17) 才被提交；否则修订一次，若仍失败则丢弃。

## 5 实验设置

我们在五类场景上评估 EvolveNet，它们都有自然的智能体特化轴；协议中每个特化单元就是一个数据本地客户端。客户端在 BIRD text-to-SQL 上是数据库（[15](#bib.bib15)）、在 DS-1000 上是库（[13](#bib.bib13)）、在 SWE-bench Verified 上是代码仓库（[10](#bib.bib10)）、在 ClawEval 上是任务族（基于 OpenClaw 智能体与模拟企业服务的智能体工作流任务）、在 LiveCodeBench 上是难度带（[9](#bib.bib9)）——后者作为更小的稳健性检查，因为其单一平台题库无法做五路分片。可访问客户端混合分布 $\mathcal{P}_{\mathrm{client}}$ 中的权重 $\pi_{k}$ 均匀，每个客户端的提议器被赋予一个搜索角色——保守修复、独立探索或对抗审计——按客户端索引分配，使并发分支不会塌缩到同一个编辑上；附录 [C](#A3) 逐字复现了专家指令与聚合器的采纳规则。除 LiveCodeBench（$K{=}3$）外一律用 $K{=}5$ 个客户端，全程 $T{=}3$ 轮，每轮一次本地生成、每个提议器一个分支（算法 [1](#alg1) 中 $E{=}G{=}1$）。留出集规模：BIRD 150、DS-1000 200、SWE-bench 40、ClawEval 与 LiveCodeBench 各 30；划分固定 seed 0，且每个条目在使用前都通过了我们环境中的金标准检查（附录 [A](#A1)）。附录 [B](#A2) 给出各客户端分片与划分规模。

冻结求解器全程为 deepseek-v4-flash，同一模型驱动客户端提议器与服务端聚合器；第 [6.7](#S6.SS7) 节用不同模型栈重跑了流水线。只有 harness 被适配：静态审计器拒绝任何改动模型、端点或凭据、或在推理时读取金标准答案的候选。标签只在两处进入循环——客户端在各自分片上选择候选，服务端在其验证切片上门控合并——测试集在共享 harness 冻结之后才评估。BIRD 是开发基准，聚合算子、门控与循环设计都在其上选定；算子随后冻结，其余四类场景各端到端跑一次。DS-1000 事先被指定为主确认基准，因为它的客户端持有最不相交的负载。求解器回复按完整请求缓存，每个子进程运行在固定 hash seed 下，因此两个 harness 之间的分数差反映行为差异而非采样噪声（附录 [D](#A4)）。

## 6 结果

### 6.1 一次运行能波动多少？

下面每个比较都以此测量为校准，因此先建立它。我们有同一 BIRD 第 0 轮协议的三个独立执行（相同分片、相同专家指令、相同预算；仅采样不同）。客户端级验证分数在这些运行间波动 2–4 个条目：同一混合分片客户端在两次运行中验证切片上得分 66% 与 69%，formula_1 专家 62% 与 66%，toxicology 专家 62% 与 65%；整个客户端在「返回进化程序」与「原样返回广播」之间摆动。同一规则产出的端到端最终留出分数波动相当（例如 select-best 最终结果在两次独立运行中为 66.7% 与 69.3%）。

这一散布设定了随后所有比较的分辨率。几个条目的差异落在噪声带内，因此 harness 不能按总分排名。对每对实现出来的 harness，我们因此报告配对逐项结果，而非依赖聚合分数差：证据单位是某个具体问题上的行为翻转，而不是总和的变化。

同样的散布也区分了验证切片能扮演的两种角色。作为门控它可靠：接受或拒绝取决于哪些条目翻转，而翻转在噪声之上可见。作为排名信号它不可靠——在 DS-1000 上验证总分最高的客户端，在留出数据上比一个验证分更低的合并 harness 差九个点（第 [6.3](#S6.SS3) 节）。EvolveNet 只把切片用于逐项决策，绝不用于宣布赢家。

### 6.2 主结果

表 [1](#S6.T1) 报告了 $T$ 轮 EvolveNet 之后共享 harness 的留出准确率，对照每个客户端起步所用的未进化 harness。

**表 1：** 共享 harness 进化前后（$T$ 轮 EvolveNet 后）的留出准确率（%）——本地提取、以程序适配形式聚合的经验，是否转化为共同起点程序中的累积改进。ClawEval 按连续标度评分，其列报告平均任务分数。

|  | BIRD | DS-1000 | LCB | SWE-V | ClawEval |
| --- | --- | --- | --- | --- | --- |
| 未进化 harness | 57.3 | 55.5 | 33.3 | 37.5 | 65.8 |
| EvolveNet | 70.7 | 68.5 | 66.7 | 57.5 | 74.1 |

协作进化在每个场景都改进了共享 harness：BIRD +13.4、DS-1000 +13.0、LiveCodeBench +33.4、SWE-bench +20.0、ClawEval +8.3 个点。每项改进在该基准留出集上的配对检验下显著——二值结果用精确 McNemar 检验，ClawEval 的连续法官分数用 Wilcoxon 符号秩检验——$p$ 分别为 5.4e-4（BIRD，胜 26 / 负 6）、6.2e-6（DS-1000，胜 30 / 负 4）、2.0e-3（LiveCodeBench，胜 10 / 负 0）、0.021（SWE-bench，胜 9 / 负 1）、0.022（ClawEval，更好 18 / 更差 7）；五项在 Holm 校正后全部保持显著。EvolveNet 在全部五类场景还优于「保留最强单客户端」（附录 [E](#A5)），差距随客户端负载差异增大而扩大——从 BIRD 的 1.4 个点（其十一个数据库共享同一任务形态）到 LiveCodeBench 的 23.4 个点。

轨迹的两个性质值得一提。增益不是一步到位的（图 [3](#S6.F3)）：在 DS-1000 上合并程序从一轮后的 60.0% 升到三轮后的 68.5%，一轮合并破坏的条目由下一轮救回；在 LiveCodeBench 与 SWE-bench 上，最后一轮在留出数据上比其前身再增加 16.7 与 17.5 个点。增益也不限于客户端训练过的库：在 DS-1000 上合并 harness 在每个库上都优于未进化 harness（表 [2](#S6.T2)），包括一个没有客户端训练过的库。本节其余部分追问：聚合算子对这些数字贡献了什么（第 [6.4](#S6.SS4) 节）、客户端发现的适配是否真的被保留（第 [6.5](#S6.SS5) 节）、合并后的程序里到底有什么（第 [6.9](#S6.SS9) 节）。

**表 2：** DS-1000 按库的留出准确率（%）。*Delegation*、*GLOBAL-only* 与 *EvolveNet* 都基于同一份最终轮客户端快照构建；*select-best* 是端到端基线流程，服务端直接提升验证得分最高的客户端而不聚合。*Delegation* 保留全部 $K$ 个客户端程序，把每个条目分派给其库的拥有者；*GLOBAL-only* 是禁止领域条件化的 EvolveNet 聚合器（第 [6.4](#S6.SS4) 节）。五个库有对应客户端；Pytorch 只出现在验证与测试中，因此不存在它的专家。加粗为 EvolveNet 列。

| 库 | n | 未进化 | Select-best | Delegation | GLOBAL-only | EvolveNet |
| --- | --- | --- | --- | --- | --- | --- |
| Pandas | 63 | 57.1 | 65.1 | 74.6 | 73.0 | 73.0 |
| Numpy | 47 | 51.1 | 55.3 | 55.3 | 61.7 | 61.7 |
| Matplotlib | 30 | 76.7 | 63.3 | 60.0 | 80.0 | 83.3 |
| Sklearn | 24 | 45.8 | 54.2 | 62.5 | 45.8 | 58.3 |
| Scipy | 21 | 42.9 | 57.1 | 57.1 | 61.9 | 61.9 |
| 无客户端训练过的库 |  |  |  |  |  |  |
| Pytorch | 15 | 53.3 | 53.3 | 66.7 | 66.7 | 66.7 |
| 全部 | 200 | 55.5 | 59.5 | 64.0 | 66.5 | 68.5 |

**图 2：** 各基准验证切片上逐轮提交的共享 harness（$t{=}0$ 为未进化 harness）。门控使已提交轨迹非降——被拒绝的合并让曲线持平而非下降——前提是切片固定且评分确定性（附录 [D](#A4)）。分数为切片最大值的百分比；ClawEval 为同一轴上的平均法官分数。

**图 3：** BIRD 准确率对照「EvolveNet 一轮相对串行执行同样本地搜索快多少」，计入不可并行的聚合与门控步骤；仅客户端阶段即可并行提速 1.9–5.4 倍（第 [6.8](#S6.SS8) 节）。切分固定负载买到墙钟时间而不损失精度：每个多客户端配置都达到或高于 $K{=}1$。$K{=}7$ 处的下滑是分片规模效应：把混合分片按数据库拆分后，其三个子客户端各只剩 6–8 个条目，候选会对它们过拟合。

### 6.3 验证分数不能给程序排名——所以门控只做门控

服务端的验证切片对门控与选择必不可少，但不能用它下结论。在 DS-1000 上，select-best 客户端验证得分 69% 但测试 59.5%；合并 harness 验证 63% 但测试 68.5%。按验证排名会把真实次序颠倒——与第 [6.1](#S6.SS1) 节的方差测量一致。因此 EvolveNet 只用验证做逐项接受/拒绝决策（这很稳健：比较的是行为翻转而非总分），论文中所有结论都来自带配对显著性检验的留出测试集。

### 6.4 这是聚合，还是伪装的按域路由？

作用域类型化合并包含领域条件化材料，这引出一个替代解释：EvolveNet 只是保留 $K$ 个专家并按领域分派，并没有发生真正的组合。我们在 DS-1000（客户端持有最不相交负载的场景）上检验它：在**同一份**最终轮客户端快照上重放各替代聚合器（表 [3](#S6.T3)）。最重要的对照是 *select-best*——它完全不做聚合，只保留服务端验证切片上得分最高的客户端；如果程序组合是不必要的，这就是显然该做的事。

**表 3：** 算子两半各自是否挣到了位置？*Delegation*、*GLOBAL-only* 与 *EvolveNet* 基于同一份 DS-1000 客户端 harness 快照、在同一留出集上评估，因此它们之间的差异可归因于聚合规则本身；*select-best* 是端到端基线流程——服务端提升最强客户端而非聚合。*Delegation* 完全不组合：保留全部 $K$ 个客户端程序，把每个条目分派给它所在库的拥有者。*GLOBAL-only* 是禁止领域条件化的 EvolveNet——聚合器只能凭跨库证据提升机制。

| 聚合规则 | 组合 | 领域门控 | 留出（%） |
| --- | --- | --- | --- |
| 未进化 harness | — | — | 55.5 |
| Select-best 客户端（无聚合） | — | — | 59.5 |
| Delegation（保留程序，分派） | 否 | 是 | 64.0 |
| GLOBAL-only 合并 | 是 | 否 | 66.5 |
| EvolveNet（作用域类型化合并） | 是 | 是 | 68.5 |

「只是路由」的解释不成立。把各客户端机制组合进一个程序，胜过把它们分开分派（68.5% vs 64.0%，胜 15 / 负 6）；更说明问题的是，一个**被禁止**写任何领域条件的聚合器已经达到 66.5%，高于 delegation。因此 EvolveNet 的增益主要来自「提升为全局共享行为的机制」，领域条件化在其上再贡献 2.0 个点，而不是增益的承载者。单调排序与「两个组件都有贡献」一致。

### 6.5 经验会跨智能体累积吗？

协作式 harness 进化的核心承诺是：一个智能体发现的适配通过重新分发的共享 harness 对其他智能体可用。聚合准确率并不能确立这种转移发生，因此我们直接测量组合。设每个客户端的**增益**为它相对当轮广播给它的共同 harness 新解出的留出条目，这样前几轮累积的能力不会被记到当前客户端头上。在 DS-1000 上，五个客户端的增益并集为 20 个条目——合并 harness 保留其中 18 个，保留率 90.0%。这 20 个条目中，9 个只有 Pandas 客户端解出、6 个只有 Sklearn、2 个只有 Matplotlib，因此保留不是客户端意见一致的产物：合并程序携带的能力恰好只存在于它的某个父程序里。还有 2 个条目被合并 harness 解出、却被任何单一客户端都解不出——即组合产生了任何单条轨迹都没达到的行为。

该基准上第二个观察指向同一结论。Pytorch 只出现在验证与测试中，任何分片都不含它、也不存在它的专家；未进化 harness 与 select-best 各解出它 15 个条目中的 8 个，EvolveNet 解出 10 个。产生这一差异的东西不是在 Pytorch 上学到的，这佐证了上面的机制层面解读：合并程序携带的部分行为是从它被发现的那个领域之外「提升」出来的。

### 6.6 EvolveNet 与集中式进化相比如何？

我们给集中式替代方案两个预算。在**等串行深度**下（$T{=}3$ 轮优化器、每轮一个提议器），对合并后 100 项负载做逐轮门控的集中式优化器在 BIRD 留出集上达到 68.7%；不逐轮选择地串联各代生成则彻底失败（最终候选在自家训练集上得分低于未进化 harness，被回滚）。在**等总预算**下——每轮五个并行提议器分支的集中式**种群**，与 EvolveNet 的十五次提议器会话精确对齐——它达到 67.3%：该种群在随后两轮从未超过第一轮的最佳分支。EvolveNet 在相同预算下达到 70.7%（配对条目上对种群基线胜 14 / 负 9）。在这个同质基准上差距在一个噪声带内，但机制差异在产物中可见：集中式优化器最强的机制帮了一个数据库族、却明显误导其他族，因此它的预算花在门控单个机制上；而协作客户端**并发**发展出五个特化机制族——在分解最要紧的 DS-1000 上，合并 harness 高出最强单客户端 9.0 个点（第 [6.4](#S6.SS4) 节）。对这个比较的解读需要谨慎。EvolveNet 与集中式种群有两处同时不同：搜索按分片分解，且每个分支被指示去特化。一个假设的、给定同样的五路划分、同样的专家指令、同样聚合器的集中式优化器，会精确执行 EvolveNet 的计算——数据本地性限制的是该计算**在哪里**运行，而不是它**是什么**。因此我们把这些数字读作：在等预算下，「分解的专家搜索 + 证据门控聚合」胜过「未分解的合并搜索」，且 EvolveNet 在不把任何负载移出客户端的情况下保住了这一收益——而这是集中式方法无须满足的约束。分布化负载是使分解必要且正当的原因；它本身不是增益来源。

### 6.7 这些结果依赖模型吗？

我们用完全不同的模型栈重跑了完整 BIRD 流水线——相同分片、专家指令、作用域类型化合并、门控与预算——把整个模型栈（求解器、提议器、合并器）从 deepseek-v4-flash 换成另一家供应商的推理模型 MiMo-V2.5。每个定性行为都复现：第 1 轮合并以大增益被接受，之后一次有害合并被门控拒绝并回滚，最终合并 harness 达到 72.7%，对照 select-best 72.0%、未进化 harness 62.7%（EvolveNet vs 未进化：胜 23 / 负 8，$p{=}0.011$；vs select-best：+0.7 个点，胜 10 / 负 9，方向与幅度和原栈在这个同质基准上一致）。EvolveNet 的定性行为——接受的增益、被门控拒绝的回退、领先两个基线的最终合并 harness——并非原模型栈特有。

### 6.8 通过并行轨迹扩展进化搜索

一轮 EvolveNet 的成本是 $K$ 次并行本地进化会话加一次合并器会话加一次门控测量。客户端阶段主导墙钟时间，且由于它们相互独立，相对串行进化同样程序集的加速比随客户端数量扩展——上限为 $K$，只被每轮收尾的掉队者拉低。把我们的运行中相同的客户端会话串行化，将分别耗时并行阶段的 1.93 倍（$K{=}2$）、3.96 倍（$K{=}5$）与 5.37 倍（$K{=}7$）；与理想 $K$ 的差距随分片变小、客户端运行时间变得不均而拉大——正是让图 [3](#S6.F3) 精度曲线下弯的同一分片规模效应。端到端计入聚合与门控，整个 $T{=}3$ 的 BIRD 运行在 $K{=}5$ 下耗时 6110 秒，对照逐轮集中式优化器 1693 秒、等预算集中式种群 3655 秒。因此协作并不会让固定预算在绝对墙钟时间上更便宜——它让**更大**的搜索在有限串行深度下可负担：$K{=}5$ 运行探索五条专家轨迹加一次聚合，墙钟约为单次逐轮集中式运行的三倍半，达到 70.7%，而集中式替代方案为 68.7% 与 67.3%（第 [6.6](#S6.SS6) 节）。聚合步骤每轮增加一次与 $K$ 无关的 LLM 会话；门控测量复用缓存的求解器调用，只增加数秒。跨网络传输的是几百行的程序——千字节级，载荷大小由 harness 决定而非模型。

这些测量刻画了 EvolveNet 的扩展维度。搜索随 $K$ 增长而轮数不增长：客户端阶段以最慢分支为上界，因此 $K$ 条并发轨迹的成本等于最长那条（比串行快 1.9–5.4 倍）。服务端排程也不随 $K$ 拉长：每轮一次合并器会话、一次缓存门控测量，无论聚合两个还是七个客户端——尽管合并器读取的增量越多、输入越大。每个客户端传输的是 harness 规模的载荷而非模型规模的更新，因此每客户端流量由程序大小决定，服务端总入站流量大致随 $K$ 线性增长。而且切分不用精度来支付：我们运行的每个多客户端配置都达到或高于单客户端基线（图 [3](#S6.F3)）。因此，新增一个部署就给共享 harness 增加一条搜索轨迹和一个经验领域，而不增加轮数。

### 6.9 聚合器实际做了什么

合并报告让算子变得具体。在 BIRD 上，服务端收到一个硬编码到某客户端数据库的数值锚定探针，把它**泛化**成一个在三个数据库上验证过的动态分类值探针；把第二个客户端的 SQL 方言自动修复**原样**采纳进第一个客户端更简单的重试结构；并**拒绝**了四条分片专属提示词规则，理由是它们各自破坏了哪些具体被评分的题目。在 DS-1000 上，第 2 轮合并把某个客户端的模式预分析门控到 Pandas——在服务端复现了集中式优化器被迫自己发现的那个库级门控——同时把带跨库证据的执行重试逻辑提升到全局作用域。这些报告中的每个采纳决定都引用了被评分的逐项判定或一条轨迹。

## 7 局限

##### 数据本地不等于隐私。

客户端分片永不离开客户端——本地进化、候选选择与逐项判定都在客户端计算，跨边界的是 harness 源代码、它相对广播基线的 diff 与布尔判定。这是本地性保证，不是隐私保证：程序编辑本身可能编码客户端信息（我们的定性分析显示一个探针硬编码了某客户端的 schema），量化这类泄漏需要威胁模型，我们留给未来工作。方法还假设服务端拥有带标签的验证数据且它对部署有代表性，这比参数空间聚合通常的要求更强。最后，门控主域机制所用的分派键必须推理时可观测；对数据库、库与仓库它可观测，而对 LiveCodeBench 检查它用的是基准难度元数据——这是该基准作为多客户端试验台的局限。

##### 产物增长。

当门控持续放行时，作用域类型化采纳会单调增加代码：三轮后 BIRD 共享 harness 从 14 行（未进化 harness）长到 253 行，DS-1000 从 17 行长到 409 行。当前门控对「准确率平局但增加行数」的合并没有惩罚。严格拒绝平局的门控不是答案——在我们的运行上重放它会在 DS-1000 上损失 14 项、LiveCodeBench 上损失 5 项（附录 [F](#A6)）——但在声称长期累积之前，需要大小或延迟感知的门控、机制退役机制，以及超出 $T{=}3$ 轮的测量。我们的观察覆盖 $T\leq 3$、$K\leq 7$。

##### 配对比较是反事实。

在一轮之内，我们给「每种聚合规则**本会**从某次运行的客户端快照产生的共享 harness」打分；我们不跑 $|\text{变体}|$ 次独立端到端运行。这是刻意的——它去除了本会主导结果的 $\sigma{\approx}3$ 客户端质量方差——但它意味着表 [3](#S6.T3) 各行共享同一客户端群体，且所涉轮次之外的偏离未被建模。

##### 每个聚合规则一个 seed。

表 [3](#S6.T3) 的聚合比较基于每个规则单个快照。它产生的排序由表 [2](#S6.T2) 的按库分解与第 [6.5](#S6.SS5) 节的机制层面保留分析佐证。

##### 标签使用。

标签通过本地训练分片（用于客户端侧候选选择）与独立验证切片（用于服务端侧验收门控）进入循环。因此该方法是**有监督的协作式适配**，而非既有 harness 进化工作的无标签测试时设定，其数字与该条线不可比。

##### 歧义的金标准。

在 40 项 hard 切片内部，审计标出 9 项金标准并非由题目与提示唯一确定的条目（例如题目问平均值而金标准枚举行）。我们为与既往工作可比而保留它们，但它们封顶了可达分数。正文所有 BIRD 数字都使用这 150 项留出集。

## 8 结论

既往 harness 进化研究一个智能体如何改进；本文研究许多智能体发现的改进如何累积进一个共享进化产物。我们提出 EvolveNet——一个协作式 harness 进化框架：数据本地智能体部署沿并行的专家轨迹进化广播 harness，服务端通过作用域类型化、证据门控的聚合把它们的编辑组合进一个共享程序。重新分发后，该程序让每个部署继承其他部署发现的经验。在五类评估场景中，合并 harness 都优于每个客户端起步的未进化程序；在每类场景中，它也优于保留最强单客户端。逐项验收门控让已提交轨迹在其测量标准上非降，且 BIRD 上 EvolveNet 避免了两个等预算集中式替代方案都出现的停滞与回滚。更广泛的教训是：协作式智能体改进期间共享的产物不必是参数向量——只要适配可组合、可行为验证，一个可执行程序就能把部署的运维经验带过组织边界。组合这样的程序是一个实用——但本质上非算术——的聚合问题。我们预期作用域类型化原则，以及「把每次采纳扎根于逐项行为证据」的纪律，能迁移到比本文研究更丰富的智能体生态。

## 附录要点摘译

- **附录 A（基准构建与金标准审计）**：每个训练/验证/测试条目使用前都通过基准专属的金标准检查。DS-1000 的 400 个初采问题中 39 个未通过（主要是 Matplotlib、Tensorflow、Pytorch 环境敏感问题），换为同库可过问题；SWE-bench Verified 的 80 个实例金标准补丁全部在 Docker 官方评测环境通过；LiveCodeBench 的 110 题全部携带非空测试套件。BIRD 金标准由 LLM 审计器逐项审查，默认「接受」、只拒绝三类明确缺陷（SQL 无法执行 / 提示与题目在具体值上矛盾 / 金标准静默丢弃或新增条件）；难度、大小写不匹配、`DISTINCT` 取舍不算拒绝理由。150 项留出集（40 hard + 110 representative）的审计在 2026-07-22 冻结，早于最早端到端运行（BIRD 2026-07-23）；审计器看不到任何 harness、生成 SQL 或系统分数。判据以「失败验证」校准：更严的早期版本误拒 60% 的人工审计切片且无判别力。作者声明未做独立人工审计。
- **附录 B（分片与划分）**：全部划分固定 seed 0、按构造不相交。BIRD：五客户端持 24/18/18/18/22 个训练条目（card_games、california_schools、formula_1、toxicology、混合分片），验证 100、测试 150，跨十一个数据库分层、其中四个无客户端专家。DS-1000：五客户端各 20 条（Pandas/Numpy/Matplotlib/Sklearn/Scipy），Pytorch 只出现在验证与测试；Tensorflow 未通过金标准检查被大库替换。SWE-bench：五客户端各 30 条（django/sphinx/sympy/astropy/pytest+pylint），测试再加 10 个无客户端训练过的仓库实例。LiveCodeBench：三客户端各 20 条按难度带。ClawEval：五客户端 8/8/4/4/6 条，验证 10、测试 30。$K$ 消融把 BIRD 分片重组为 $K{=}2$ 或把混合分片按数据库拆成 $K{=}7$。
- **附录 C（提示词）**：专家指令（节选）核心——「SPECIALIST MODE：你只服务一个客户端……目标是成为这片数据的专家，把反复出现的分片专属失败（表/列消歧、值格式、join 路径）编码为持久机制（不许硬编码单题答案；schema 级与切片级知识正是该捕获的）。服务端会把你与其他客户端的专长合并——你的 harness 知道得越多、越是他者不知道的，协作收益越大。」作用域采纳规则（节选）核心——「先给每个候选机制分 GLOBAL 还是 HOME 作用域：证据跨库或失败模式普适 → 全局采纳一个最佳实现；证据只来自某客户端主库 → 不要全局采纳，也不要因它在其他库上回退而拒绝——按条件采纳：harness 求解时拿到领域，把规则包成只在该客户端主域生效。主域规则按构造不可能在域外改变行为，只用它的域内证据评判。仍要拒绝单题 hack。冲突在作用域下消解：两个客户端反向改同一行为时，各自保留在主域内，而不是二选一。」变体只替换采纳块，脚手架、证据与预算一致。
- **附录 D（测量细节）**：两条工程措施让微小差异有意义。冻结求解器回复按完整请求缓存（提示词、系统消息、温度、采样数、重复索引），两个 harness 问同一问题得到同一答案。每个子进程固定 hash seed：不钉时，用 set 收集表名/列名的 harness 会因进程间迭代顺序不同改变提示词与缓存键，采样噪声复现——直接测量，钉 seed 前同一冻结 harness 三次相同评估得 16/17/17；钉后两次完整重复在 50/50 条目上产生字节级一致的 SQL。聚合规则另做配对比较：把每条规则应用到同一份客户端 harness 快照，报告各自本会产出的共享 harness，使差异可归因于规则本身。
- **附录 E（五类场景保留最强客户端）**：端到端对比（同协议、同留出集）：select-best 69.3/59.5/43.3/42.5/70.6 vs EvolveNet 70.7/68.5/66.7/57.5/74.1（BIRD/DS-1000/LCB/SWE-V/ClawEval）；配对胜/负 9/7、33/15、7/0、8/2、17/8；$p$ 值 0.80、0.013、0.016、0.11、0.080，五者 Fisher 合并 $p=0.0027$。差距随客户端负载差异增大：BIRD 最窄（十一个数据库共享任务形态、发现重叠），库/难度/仓库边界处最宽。
- **附录 F（门控规则重放）**：用严格改进规则（|修复|>|破坏|、平局拒绝）重放所有接受决策：BIRD 产物不变；DS-1000 与 LiveCodeBench 改变（68.5→61.5、66.7→50.0）。每个不同决策都偏向接受平局规则，分别 14 项与 5 项——接受「既不改进也不损害验证切片」的合并，能把其机制带进下一轮，其上的产物在留出数据上更强。任何重放都不改变任何显著性结论。

## 参考文献

1. Qianshu Cai, Yonggang Zhang, Xianzhang Jia, Huajiang Zheng, Wei Xue, Jun Song, Xinmei Tian, and Yike Guo. MOSS: Self-evolution through source-level rewriting in autonomous agent systems. *arXiv preprint arXiv:2605.22794*, 2026.
2. Xiang Chen, Yuling Shi, Qizhen Lan, Yuchao Qiu, Min Wang, Xiaodong Gu, and Yanfu Yan. Fed-SE: Federated self-evolution for privacy-constrained multi-environment LLM agents. *arXiv preprint arXiv:2512.08870*, 2025.
3. Yilun Du, Shuang Li, Antonio Torralba, Joshua B. Tenenbaum, and Igor Mordatch. Improving factuality and reasoning in language models through multiagent debate. In *International Conference on Machine Learning*, 2024.
4. Chrisantha Fernando, Dylan Banarse, Henryk Michalewski, Simon Osindero, and Tim Rocktäschel. Promptbreeder: Self-referential self-improvement via prompt evolution. *arXiv preprint arXiv:2309.16797*, 2023.
5. Qingyan Guo, Rui Wang, Junliang Guo, Bei Li, Kaitao Song, Xu Tan, Guoqing Liu, Jiang Bian, and Yujiu Yang. Connecting large language models with evolutionary algorithms yields powerful prompt optimizers. In *International Conference on Learning Representations (ICLR)*, 2024.
6. Yufei He, Juncheng Liu, Yue Liu, Yibo Li, Tri Cao, Zhiyuan Hu, Xinxing Xu, and Bryan Hooi. EvoTest: Evolutionary test-time learning for self-improving agentic systems. *arXiv preprint arXiv:2510.13220*, 2025.
7. Shengran Hu, Cong Lu, and Jeff Clune. Automated design of agentic systems. In *International Conference on Learning Representations (ICLR)*, 2025.
8. Gabriel Ilharco, Marco Tulio Ribeiro, Mitchell Wortsman, Suchin Gururangan, Ludwig Schmidt, Hannaneh Hajishirzi, and Ali Farhadi. Editing models with task arithmetic. In *International Conference on Learning Representations (ICLR)*, 2023.
9. Naman Jain, King Han, Alex Gu, Wen-Ding Li, Fanjia Yan, Tianjun Zhang, Sida Wang, Armando Solar-Lezama, Koushik Sen, and Ion Stoica. LiveCodeBench: Holistic and contamination free evaluation of large language models for code. In *International Conference on Learning Representations (ICLR)*, 2025.
10. Carlos E. Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, and Karthik Narasimhan. SWE-bench: Can language models resolve real-world GitHub issues? In *International Conference on Learning Representations (ICLR)*, 2024.
11. Sai Praneeth Karimireddy, Satyen Kale, Mehryar Mohri, Sashank J. Reddi, Sebastian U. Stich, and Ananda Theertha Suresh. SCAFFOLD: Stochastic controlled averaging for federated learning. In *International Conference on Machine Learning (ICML)*, 2020.
12. Omar Khattab, Arnav Singhvi, Paridhi Maheshwari, Zhiyuan Zhang, Keshav Santhanam, Sri Vardhamanan, Saiful Haq, Ashutosh Sharma, Thomas T. Joshi, Hanna Moazam, Heather Miller, Matei Zaharia, and Christopher Potts. DSPy: Compiling declarative language model calls into self-improving pipelines. In *International Conference on Learning Representations (ICLR)*, 2024.
13. Yuhang Lai, Chengxi Li, Yiming Wang, Tianyi Zhang, Ruiqi Zhong, Luke Zettlemoyer, Wen-tau Yih, Daniel Fried, Sida Wang, and Tao Yu. DS-1000: A natural and reliable benchmark for data science code generation. In *International Conference on Machine Learning (ICML)*, 2023.
14. Yoonho Lee, Roshen Nair, Qizheng Zhang, Kangwook Lee, Omar Khattab, and Chelsea Finn. Meta-Harness: End-to-end optimization of model harnesses. *arXiv preprint arXiv:2603.28052*, 2026.
15. Jinyang Li, Binyuan Hui, Ge Qu, Jiaxi Yang, Binhua Li, Bowen Li, Bailin Wang, Bowen Qin, Ruiying Geng, Nan Huo, et al. Can LLM already serve as a database interface? A big bench for large-scale database grounded text-to-SQLs. In *Advances in Neural Information Processing Systems (NeurIPS)*, 2023.
16. Tian Li, Anit Kumar Sahu, Manzil Zaheer, Maziar Sanjabi, Ameet Talwalkar, and Virginia Smith. Federated optimization in heterogeneous networks. In *Proceedings of Machine Learning and Systems (MLSys)*, 2020.
17. Brendan McMahan, Eider Moore, Daniel Ramage, Seth Hampson, and Blaise Agüera y Arcas. Communication-efficient learning of deep networks from decentralized data. In *International Conference on Artificial Intelligence and Statistics (AISTATS)*, 2017.
18. Jun Nie, Yonggang Zhang, Jun Song, Qianshu Cai, Dahai Yu, Yike Guo, Xinmei Tian, and Bo Han. TTHE: Test-time harness evolution. *arXiv preprint arXiv:2607.08124*, 2026.
19. Sashank J. Reddi, Zachary Charles, Manzil Zaheer, Zachary Garrett, Keith Rush, Jakub Konečný, Sanjiv Kumar, and H. Brendan McMahan. Adaptive federated optimization. In *International Conference on Learning Representations (ICLR)*, 2021.
20. Bernardino Romera-Paredes, Mohammadamin Barekatain, Alexander Novikov, Matej Balog, M. Pawan Kumar, Emilien Dupont, Francisco J. R. Ruiz, Jordan S. Ellenberg, Pengming Wang, Omar Fawzi, et al. Mathematical discoveries from program search with large language models. *Nature*, 2024.
21. Qingyun Wu, Gagan Bansal, Jieyu Zhang, Yiran Wu, Beibin Li, Erkang Zhu, Li Jiang, Xiaoyun Zhang, Shaokun Zhang, Jiale Liu, Ahmed Hassan Awadallah, Ryen W. White, Doug Burger, and Chi Wang. AutoGen: Enabling next-gen LLM applications via multi-agent conversation. *arXiv preprint arXiv:2308.08155*, 2023.
22. Prateek Yadav, Derek Tam, Leshem Choshen, Colin Raffel, and Mohit Bansal. TIES-merging: Resolving interference when merging models. In *Advances in Neural Information Processing Systems (NeurIPS)*, 2023.
23. Chengrun Yang, Xuezhi Wang, Yifeng Lu, Hanxiao Liu, Quoc V. Le, Denny Zhou, and Xinyun Chen. Large language models as optimizers. In *International Conference on Learning Representations (ICLR)*, 2024.
24. Jingbo Yang, Guanyu Yao, Yang Zhang, Ramana Rao Kompella, Gaowen Liu, and Shiyu Chang. FederatedSkill: Federated learning for agentic skill evolution. *arXiv preprint arXiv:2606.03143*, 2026.
25. Dixi Yao, Tahseen Rabbani, Manzil Zaheer, and Tian Li. Federation over Text: Insight sharing for multi-agent reasoning. *arXiv preprint arXiv:2604.16778*, 2026.
26. Le Yu, Bowen Yu, Haiyang Yu, Fei Huang, and Yongbin Li. Language models are super mario: Absorbing abilities from homologous models as a free lunch. In *International Conference on Machine Learning (ICML)*, 2024.
27. Eric Zelikman, Eliana Lorch, Lester Mackey, and Adam Tauman Kalai. Self-taught optimizer (STOP): Recursively self-improving code generation. *arXiv preprint arXiv:2310.02304*, 2023.
28. Hangfan Zhang, Shao Zhang, Kangcong Li, Chen Zhang, Yang Chen, Yiqun Zhang, Lei Bai, and Shuyue Hu. Self-Harness: Harnesses that improve themselves. *arXiv preprint arXiv:2606.09498*, 2026.
29. Jenny Zhang, Shengran Hu, Cong Lu, Robert Lange, and Jeff Clune. Darwin Gödel Machine: Open-ended evolution of self-improving agents. *arXiv preprint arXiv:2505.22954*, 2025a.
30. Jiayi Zhang, Jinyu Xiang, Zhaoyang Yu, Fengwei Teng, Xiong-Hui Chen, Jiaqi Chen, Mingchen Zhuge, Xin Cheng, Sirui Hong, Jinlin Wang, Bingnan Zheng, Bang Liu, Yuyu Luo, and Chenglin Wu. AFlow: Automating agentic workflow generation. In *International Conference on Learning Representations (ICLR)*, 2025b.
31. Yongchao Zhou, Andrei Ioan Muresanu, Ziwen Han, Keiran Paster, Silviu Pitis, Harris Chan, and Jimmy Ba. Large language models are human-level prompt engineers. In *International Conference on Learning Representations (ICLR)*, 2023.

> 参考文献保留英文不译；编号与正文 [N] 引用一致。
