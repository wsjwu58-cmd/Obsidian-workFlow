---
created: 2026-10-03
updated: 2026-10-03
title: 为 harness 做工程：可靠编程智能体的一条实用模式
sourceUrl: https://www.thoughtworks.com/en-gb/insights/blog/architecture/engineering-the-harness-a-practical-pattern-for-reliable-coding-agents
sourceAuthor: Jaya Simha Reddy Nandyala、Prabina Pani，Thoughtworks
translatedAt: 2026-10-03
sources: [references/articles.md 待处理队列]
tags: [Harness 工程, Harness Engineering, AI Coding Agent, Guides, Sensors, 选择性人工闸门, Human-in-the-loop, 影响半径, Blast Radius, 多仓库, Microservices, 渐进式披露, 最小权限, 结构化接收, RED-GREEN-REFACTOR, 验收测试, type/翻译]
---

# 为 harness 做工程：可靠编程智能体的一条实用模式

> [thoughtworks.com](https://www.thoughtworks.com/en-gb/insights/blog/architecture/engineering-the-harness-a-practical-pattern-for-reliable-coding-agents)｜分类：Generative AI / Evolutionary architecture
> 作者：Jaya Simha Reddy Nandyala、Prabina Pani
> 发布：2026-09-29｜队列日期：2026-10-03
> 原文：https://www.thoughtworks.com/en-gb/insights/blog/architecture/engineering-the-harness-a-practical-pattern-for-reliable-coding-agents

随着大语言模型（LLM）在推理与代码生成能力上的持续进步，开发团队正发现一个令人费解的悖论：一个 AI 编程智能体可以写出局部优雅、编译干净、通过基础语法检查的代码，却对整个系统而言是错的。

一旦不加约束，智能体就会针对它手头可用的局部上下文做优化。一个被要求重构数据模型的智能体，可能会在它当前正在编辑的服务里重命名某个字段，却完全不知道有两个下游微服务正消费这个确切的字段。改动在局部是正确的，在系统层面却是破坏性的。

原始模型智能与可靠软件交付之间这条长期存在的鸿沟，主要不是模型质量问题。模型缺的是系统级可见性、架构护栏与自动化反馈机制。我们可以把这个关系表达为：

### _Agent = Model + Harness_

模型提供推理能力，而 [harness engineering](https://www.thoughtworks.com/en-us/insights/blog/generative-ai/what-is-harness-engineering) 提供结构化环境、工具约束、上下文边界与反馈回路，把原始智能转化为安全、可靠、可审计的交付系统。

## 一套实用的 harness 有两层（以及选择性人工闸门）

为同时防止 AI 无约束的漂移与人工评审疲劳，生产级 harness 依赖两层互补的强制机制，中间由有针对性的决策闸门隔开：

**1. 引导（Guides，行动前引导）：** 在智能体行动或写代码之前就约束并引导它的机制。

**2. 传感器（Sensors，行动后验证）：** 在智能体行动之后检查并验证其产出的自动化反馈回路。

**3. 选择性人工闸门（selective human gates）：** 部署在引导与传感器之间的战略检查点，在这些点上需要人工判断或对影响半径（blast radius）的签核。

通过把行动前引导与行动后验证清晰分开，团队可以避开两个常见陷阱：任由智能体毫无约束地自由发挥，或者逼着人类对每一次琐碎的工具调用都签字放行。

## 引导（Guides）：在智能体行动前施加约束

引导划定了智能体被允许在其中探索、规划与写代码的参数范围。有效的引导依赖四个核心模式：

### 作用域化指令与渐进式披露

把单体式的指令文件加载进每一个会话，会迅速填满上下文窗口，造成“注意力稀释（attention dilution）”与上下文腐化（context rot）。相反，指令应按文件路径或领域树来划定作用域（例如只在触碰 schema 文件时才加载数据库规则）。借助渐进式披露（progressive disclosure）——即按需遍历文档树，而不是预先加载所有内容——智能体能把高注意力保持在相关的团队约定上。

### 最小权限工具

依赖提示词文本来请求智能体不要执行未授权操作（例如推送代码或编辑配置），本质上是脆弱的。最小权限工具（least-privilege tools）把行为引导转化为结构性强制。举例来说，一个问答或代码验证智能体只配备只读工具，它实际上根本不存在写文件的能力。

### 用显式默认值取代猜测

当智能体在结构化接收（structured intake）过程中遇到可选输入（比如一份可选的技术规格说明）时，它应当避免做出未言明的假设。harness 强制一种“先询问再决定（ask before deciding）”的协议。如果开发者选择跳过某个可选步骤，harness 可以显式记录这一决定。默认值是可见、可检查的；猜测则是隐藏且危险的。

### 仅对高影响半径决策做确认

为了在不牺牲安全的前提下保持高速度，人工确认闸门只保留给不可逆或高影响半径的选择，例如多仓库范围变更、schema 迁移或公共 API 修改。风险更低的决策则采用合理的默认值继续推进。

## 传感器（Sensors）：在智能体行动后验证

即使是最好的引导，也无法捕获每一个逻辑边界情况或运行时错误。传感器在智能体行动之后运作，提供自动化的计算反馈来验证产出。

### 自动化验证

[**传感器（Sensors）**](https://www.thoughtworks.com/en-us/insights/blog/generative-ai/exploring-ai-coding-sensors) 把单元测试、linter、静态类型检查器与架构规则等标准软件工程检查包装进智能体回路。当智能体完成一轮实现后，传感器会自动运行来评估正确性，而不是依赖智能体的自我评估。

### 静默成功、失败详尽

传感器遵循“静默成功、失败详尽（silent success, verbose failure）”规则：

- **检查通过时：** 传感器只产生最小输出，以节省宝贵的上下文 token 与人类注意力。

- **检查失败时：** 传感器生成详尽、可操作的反馈（堆栈跟踪、linter 报错位置、失败测试的 diff），把错误直接回灌进智能体回路，让它无需人工介入即可自我修正。

### 把规则从文字（prose）升级为可执行强制

如果团队发现自己因为智能体无视某条约定，而反复往提示词文件里添加文字规则（prose rules），那么这条规则就应升级为机械化的传感器（一条自定义 linter 规则、一次类型检查或一个架构测试）。文字是起点；在规则能被可靠编码的地方，机械化强制是更强的选项。

## 这套模式如何跨仓库运作

为说明共享 harness 能带来什么帮助，考虑一个包含三个微服务的系统：

- billing-service（拥有共享的 discount_rate 字段）
- checkout-service（消费 discount_rate）
- invoicing-service（消费 discount_rate）

在这个简化的示例里，依赖关系是已知且对 harness 可访问的，借此可以说明这套模式如何运作。

### 无约束的仓库级执行

当智能体在 billing-service 内执行、且没有多仓库 harness 时，一个重构请求会让智能体只在 billing-service 里把 discount_rate 重命名为 promotional_discount。智能体报告成功，因为它的本地测试通过了。然而 checkout-service 与 invoicing-service 会静默地失去同步，破坏生产工作流。

### 共享 harness 执行

当同一个请求经由一个包裹全部三个仓库的共享 harness 处理时：

1. **影响分析（Impact analysis）：** 智能体扫描共享工作区内的依赖图，识别出修改 billing-service 会影响到 checkout-service 与 invoicing-service。

2. **多仓库确认闸门（Multi-repo confirmation gate）：** 识别出多仓库的影响半径后，harness 暂停执行，并向开发者展示一个阻塞式确认闸门。

3. **协同更新（Coordinated update）：** 在人工批准后，智能体跨全部三个仓库更新契约与实现，并运行多服务测试套件来验证这次协同改动。

## 完整的交付回路

把引导、传感器与选择性人工闸门组合起来的一种方式，是走一条端到端的 6 阶段交付流水线：

1. ANALYZE（分析）：结构化接收收集 Jira 工单与技术上下文，对缺失输入强制使用显式默认值。

2. BLUEPRINT（蓝图）：[**架构智能体（architecture agent）**](https://www.thoughtworks.com/en-in/insights/blog/agile-engineering-practices/supervisory-engineering-orchestrating-software-middle-loop) 设计跨仓库的文件计划。一旦检测到多服务影响半径，它就暂停在多仓库确认闸门处等待人工签核。

3. RED（红）：测试智能体编写与需求对应的、会失败的验收测试。

4. GREEN（绿）：实现智能体编写最小代码，直到所有 RED 测试通过。

5. REFACTOR（重构）：在保持测试套件通过的前提下，打磨代码结构并遵守团队约定。

6. REVIEW（评审）：[**自动化评审智能体（automated review agent）**](https://www.thoughtworks.com/en-us/insights/blog/testing/code-review-dead-long-live-code-review) 对照验收标准检查测试覆盖。

在这条流水线内，人类反馈与自动化反馈承担不同的职责：

- [**人类反馈回路（Human feedback loop）**](https://www.thoughtworks.com/en-us/insights/blog/generative-ai/cybernetics-human-on-the-loop)：保留给重大的、不可逆的决策（例如在 BLUEPRINT 阶段批准多仓库的架构范围）。

- **自动化反馈回路：** 处理可机械修正的失败。如果 REVIEW 阶段检测到某条未覆盖的验收标准，它不会打断人类。相反，它会自动把任务路由回 RED/GREEN，去补上缺失的测试与实现，并在开启拉取请求之前自动重新运行 REVIEW。

## 把 harness 本身当作软件来对待

harness 不是一套写一次就抛在脑后的静态配置文件或提示词片段。它必须用与生产软件同等的严谨度来管理：

- **版本控制与同行评审：** 把全部智能体定义、skills、规则与工作流存进版本控制。harness 的修改要通过带同行评审的拉取请求提交。

- **为每条规则挣得存在理由（Earn every rule）：** 抵制投机性的规则膨胀。harness 中的指令应当有明确目的，并可追溯到具体需求，例如过去的生产事故、开发者痛点、安全要求或既有的工程约束。没有挣得理由的规则只会增加噪声、稀释模型注意力并拉低产出质量。

- **持续重构：** 随着底层 LLM 能力的提升，重新审视现有 harness 规则。删减过时的约束，确保 harness 保持精简有效。这条纪律之所以重要，还因为 harness 本身会带来维护开销：每一条规则、每一个传感器、每一条工作流，都会成为团队必须持续维护的工程系统的一部分。

## 结语：有界自主与平衡控制

可靠的智能体软件开发不止于 prompt engineering。要求模型“小心一点”，与构建一个“违规会被阻止或被机械捕获”的环境，有着根本的区别。

关键差异不只是嘴上说“用个 harness”，而是精通如何在交付生命周期中划分职责。通过把 harness 当作有版本、可审计的软件来对待，开发团队就能利用 AI 能力来加速交付，同时保护系统完整性。

免责声明：本文陈述与观点仅代表作者本人，不一定反映 Thoughtworks 的立场。
