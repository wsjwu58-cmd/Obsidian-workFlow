---
created: 2026-10-03
updated: 2026-10-03
title: 面向 AI 智能体的自然语言交互协议与标准
sourceUrl: http://arxiv.org/abs/2609.04135v1
sourceAuthor: Luyi Xing、Rasit Onur Topaloglu、Ranjan Sinha、Abhay Ratnaparkhi、Samuel Ndichu、Christopher Nguyen、Anindita Das、Tom Sheffler、Mohamed Rahouti、Zichuan Li、Xiaojing Liao、Sanjay Aiyagari
translatedAt: 2026-10-03
sources: [references/articles.md 待处理队列]
tags: [NLIP, 自然语言交互协议, AI智能体, 智能体互操作, 应用层协议, ECMA-430, Ecma International, 语义消息信封, 传输绑定, MCP, A2A, 智能体安全, 提示注入, 混淆代理, 语义漂移, Agent协议, 标准化, type/翻译]
---

# 面向 AI 智能体的自然语言交互协议与标准

> [arxiv.org/abs](http://arxiv.org/abs/2609.04135v1)｜分类：cs.AI（人工智能）
> 作者：Luyi Xing、Rasit Onur Topaloglu、Ranjan Sinha、Abhay Ratnaparkhi、Samuel Ndichu、Christopher Nguyen、Anindita Das、Tom Sheffler、Mohamed Rahouti、Zichuan Li、Xiaojing Liao、Sanjay Aiyagari
> 机构：伊利诺伊大学厄巴纳-香槟分校（UIUC）、Marist University、IBM、eBay、日本 NICT、Aitomatic, Inc.、Lenovo、Fordham University、Red Hat
> 提交：2026-09-03（arXiv v1）｜备注：Accepted by ACM AI Summit 2026
> 原文：http://arxiv.org/abs/2609.04135v1｜DOI：https://doi.org/10.48550/arXiv.2609.04135

## 摘要

AI 智能体正越来越多地在各类组织中被开发和部署，其所用的智能体开发框架、AI 模型、工具接口、协议和执行环境各不相同。要实现它们潜在的社会与商业价值，这些智能体必须能够通过一种共同的通信协议进行互操作。自然语言交互协议（Natural Language Interaction Protocol, NLIP）由来自多家公司和高校的研究者与从业者共同开发，并已由 Ecma International 标准化；它通过为 AI 智能体交互定义一种基于标准的应用层协议来满足这一需求。NLIP 提供了一种轻量的语义消息信封（semantic message envelope），可以承载在 HTTP/HTTPS、WebSocket 和 AMQP 等既有传输之上，同时允许 NLIP 感知的智能体与网关在客户端、智能体、本地上下文存储、本体、工具、企业服务以及异构的底层协议之间进行适配。本文介绍了 NLIP 的动机与设计理由、其消息模型与传输绑定、面向安全的设计考量、参考实现、代表性应用、采用信号，以及它与 MCP、A2A 等新兴智能体协议之间的关系。

## 1 引言

基于 AI 的软件系统（即智能体）正开始被部署到广泛的工业应用中。要充分发挥其潜力，提供不同功能、由不同组织运营的智能体必须通过一种共同的通信协议进行互操作。出于这一需求，一群学术界与工业界的研究者合作开发了**自然语言交互协议（Natural Language Interaction Protocol, NLIP）**。NLIP 于 2025 年 12 月由 Ecma International 第 56 技术委员会（Technical Committee 56, TC56）正式标准化为 ECMA-430，并配套了相关的传输绑定与安全剖面（security-profile）规范 [17–19, 21, 22]。除 Ecma International 之外，推动该标准的工作还得到了 Enterprise Neurosystem Group（enterpriseneurosystem.org）与 AI Alliance（thealliance.ai）的支持，这两个开源组织致力于促进更广泛的 AI 社区之间的协作。本文介绍 NLIP 协议、其关键设计创新、安全考量、参考实现、采用信号、代表性应用，以及与相关协议的关系。

NLIP 并不取代现有的智能体框架、工具协议或企业服务，而是定义了一个标准化的交互层，它独立于智能体内部所用技术、逻辑与 AI 模型。NLIP 是一种应用层协议：它标准化智能体交互语义与消息信封，同时直接复用现有的底层传输协议，包括 HTTP/HTTPS、WebSocket 和 AMQP。NLIP 感知的智能体与网关向用户客户端及其他智能体暴露一个共同接口，而其内部继续使用各自的原生框架、LLM API、工具协议与企业服务。如图 1 所示，轻量的 NLIP 适配器使异构智能体无需修改其内部推理或执行逻辑，就能通过一种共同协议进行通信。这一架构将 NLIP 定位为异构智能体生态中基于标准的互操作层，使独立开发的智能体能够相互通信，同时保住各组织在框架、工具与企业基础设施上的既有投资。

下文安排如下：§2 描述 NLIP 的起源，包括该想法何时被提出并开始开发；§3 描述 NLIP 的核心设计创新；§4 概述 NLIP 协议设计，包括其消息模型与传输绑定；§5 讨论面向智能体通信的安全设计；§6 给出参考实现、开发框架采用情况与代表性应用；§7 将 NLIP 置于更广泛的智能体协议版图中，并报告与 A2A 的实证比较（§7.1）；§8 作结。附录提供关于 NLIP 起源与标准化历史的更多细节。

**图 1：NLIP 作为一种应用层互操作层，通过标准化的 NLIP 消息连接用户客户端、智能体、工具、LLM 与外部智能体。**

## 2 NLIP 的起源

NLIP 于 2024 年 6 月作为 Enterprise NeuroSystem Group（ENG）内部的一个技术工作组起步。ENG 是一个由 30 多家公司和高校参与的开源联盟，其目标是促成建立全球 AI 网络所需的技术。该工作组的初始成员包括来自特拉华大学、布法罗大学、密歇根大学、SRI International、IBM 和 Red Hat 的研究者。该小组后来进一步扩展，纳入了来自 Cisco、Fordham University、宾夕法尼亚州立大学和印第安纳大学伯明顿分校的研究者。2024 年 10 月，协议初版被定义，并做出了将该规范转为正式标准的决定。Ecma International 是定义 JavaScript 等多种应用层技术的组织，被认为最贴合应用层协议设计的需求，该小组遂于 2024 年 12 月被正式吸纳为 ECMA 内部的一个技术工作组。ServiceNow 和 Hitachi 也加入了这项工作，并支持在 ECMA 内组建该小组。2025 年初，ENG 成为 AI Alliance 的正式成员；AI Alliance 是一个由多家公司和高校组成的联盟，致力于推动开源 AI 技术与治理。该联盟决定将该工作组纳入其活动范畴，并为其提供 GitHub 空间等资源，以便小组继续开展活动。随后，来自其他若干组织的研究者也加入了这项工作，包括来自 Qualcomm、日本国家信息通信技术研究所（NICT）、伊利诺伊大学厄巴纳-香槟分校（UIUC）、Marist University、芝加哥州立大学、纽约市立大学、Microsoft 和 Palo Alto Networks 的研究者。

Ecma 要求以组织名义正式成为会员才能参与，而 ENG 则允许任何组织的任何技术人员公开参与。正式加入 Ecma TC56 以定义官方标准的成员包括 IBM、Hitachi、Red Hat、ServiceNow、普渡大学、印第安纳大学伯明顿分校、布法罗大学、Fordham University、芝加哥州立大学、Marist University 和纽约市立大学。其他组织的研究者仅作为 ENG 工作组的一部分、以技术顾问身份做出贡献。ENG 小组每周会面讨论技术问题并实现原型，而 Ecma 标准团队每月会面以将标准正式化。这种双轨并行的方式使我们既能快速取得技术进展，又能朝着正式标准化阶段稳步推进。

ENG 的工作也让小组得以通过若干概念验证（proof-of-concept）原型探索 NLIP 的设计，这些原型在 NLIP 解释性报告中有所描述，并在本文后文加以概述 [20]。

## 3 NLIP 的设计创新

传统的应用层协议通常会定义通信双方之间交换的固定结构，例如 JSON 消息、Web 表单或 XML 文档。当客户端与服务器共享一个稳定的数据模型时，这种做法效果良好；但在异构的智能体生态中，它就会变得脆弱——在这些生态里，智能体、工具、模型、本体与任务表示可能各自独立演进。除非对模式（schema）、版本与兼容性规则加以精心管理，否则一个端点内部表示的哪怕是适度改动，也可能中断通信。这种紧耦合是分布式服务环境中 API 管理复杂性的一个根本来源，对于必须跨组织、跨框架、跨应用领域互操作的 AI 智能体系统而言，其局限尤为突出。

NLIP 采取了不同的方法，它将客户端与服务器之间的内部结构表示解耦。它不在网络上规定一套刚性结构，而是用**自然语言**来承载客户端与服务器需要交换的信息语义。客户端与服务器各自都可以使用内部的 AI 模型，将自然语言翻译为其内部表示。这使得客户端与服务器在需要时可以各自维持不同的内部表示 [21]。由于现代 AI 模型在结构化与非结构化信息之间的翻译上日益高效，NLIP 得以定义一个更灵活、更易维护的应用层协议。这一根本差异如图 2 所示。

在实践中，这一翻译可以由 NLIP 感知的智能体或网关完成。这些端点构成了自适应层：它们接收 NLIP 消息，将其接地（ground）到本地上下文中，并翻译为接收系统所使用的内部表示、工具、API、本体或协议。由于 NLIP 依赖语义翻译而非刚性的共享模式，当领域特定含义跨越协议边界时，实现方应防范语义漂移（semantic drift），包括上下文丢失或误读。NLIP 感知的智能体与网关可以通过将 NLIP 消息接地到结构化子消息、message-type 提示、label、provenance、本体或实体引用，以及适当的本地校验规则来缓解这一问题。从这个意义上说，NLIP 并不取代模式、本体或领域模型；它提供的是一个语义信封，让这些东西能够在异构系统之间被引用、中介与保留。

当客户端与服务器需要交换文本之外的其他模态（例如视频或音频）时，可以遵循类似的范式。NLIP 提供一种信封协议，用来描述所交换内容的类型——文本、音频、视频或其他模态——并让端点将其翻译为自己的内部表示。

**图 2：NLIP 的独特设计。**（左：传统协议要求 A = P = B；右：NLIP 中 A ≠ B，以纯文本 P 在两端之间进行翻译。）

**图 3：NLIP 消息的结构。**

## 4 NLIP 设计概述

**消息模型。** 为了在通信的双方之间实现多模态、灵活的交互，NLIP 以 JSON 对象的形式交换消息 [21]。消息主要由五个字段组成，其中三个为必填、两个为可选。三个必填字段包括：content 字段，承载实际交换的信息；format 字段，描述内容的格式；以及 subformat 字段，定义对 format 字段的进一步细化。举例来说，所交换的内容可能是一般文本，format 会将其指定为 text，而 subformat 会指定内容的语言，例如 English。可选字段包括 message-type 指定，以及一个 submessage（子消息）数组。message-type 字段可以包含一个应用特定的字符串，帮助对端解析内容；而 submessage 字段则允许在同一条消息中承载若干其他内容。其结构如图 3 所示。

submessage 数组中的每一项都包含 format、subformat 和 content 这三个必填字段，以及一个可选的 label 字段。label 与 message-type 一样，可以作为提示，让通信双方定义自己的约定以快速处理内容。举例来说，label 字段可以指明某条标识位置信息的子消息，是某次行程的接载地点（pick-up location）还是送达地点（drop-off location）。

NLIP 信封刻意保持轻量：它只标准化交互边界，而不规定每个端点的内部本体、推理方法、模型或执行框架。这使得 NLIP 感知的智能体可以承载自然语言意图、结构化上下文、provenance、约束条件以及对领域实体的引用，同时保留本地实现的选择自由。

format 字段可以标识所交换的内容是自然文本，并由 subformat 标识语言。这预期是信息交换的主导模式。format 字段的其他取值包括：将内容标识为 token，并由 subformat 标识它是关联令牌（correlation token，用于让通信流中多条相关消息彼此关联）还是认证令牌（authentication token，用于对通信双方进行认证）；标识内容为结构化文本，并由 subformat 标识它是 XML、JSON、HTML 还是其他；标识内容为二进制数据，并由 subformat 标识它是某种特定编码的音频、某种特定编码的视频数据、传感器数据等；将内容标记为位置（location），并由 subformat 标识该位置是文字描述还是经纬度描述；以及一种通用格式（generic format），允许对端处理任意信息。

**传输绑定。** 作为一种应用层协议，NLIP 不定义新的网络传输。相反，它定义了一个轻量的消息信封与交互语义，可以承载在既有的传输协议之上。当前的 NLIP 标准定义了基于 HTTP/HTTPS [18]、WebSocket [19] 和 AMQP [17] 的官方绑定。这一设计让 NLIP 端点能够复用广泛部署的传输基础设施，同时为客户端、智能体与网关提供一种共同的语义交互层。

## 5 面向智能体通信的安全设计

**安全剖面。** NLIP 为不同保障需求的部署定义了安全剖面（security profiles）[22]。然而，AI 智能体通信引入了超出传统传输安全的风险，包括提示注入（prompt injection）、间接提示注入（indirect prompt injection）、不安全的工具调用、敏感数据泄露，以及跨智能体链路的溯源丢失 [3, 34, 42]。NLIP 定义了三类应由基于 NLIP 的系统支持的安全剖面 [22]。这些剖面从基础安全要求，一直覆盖到更严格的、面向企业的要求，后者旨在最大限度地降低基于 NLIP 的部署中常见的安全风险。严格的安全剖面是为满足企业级智能体的需求而设计的，而这些需求在常见可用的标准或技术出版物中往往未被涉及。

**面向 AI 与智能体安全的统一控制点。** 除了定义安全剖面之外，NLIP 标准化的通信层还为跨异构智能体生态的安全执行提供了天然基础。由于用户客户端与智能体之间、以及智能体彼此之间的所有通信都通过标准化的 NLIP 消息承载，校验、授权、溯源追踪、策略执行、审计与安全监控就都可以在通信层一致地施加，而不是分散在各智能体框架或应用中各自为政。这为同时缓解两类漏洞提供了共同基础：一类是 AI 驱动的漏洞——如提示注入、间接提示注入、思维链泄露、语义操纵与隐私侵害 [3, 26, 29, 34, 41–43]；另一类是系统级漏洞——如会话劫持、混淆代理（confused-deputy）与令牌透传攻击、未认证的推理洪水、内存注入攻击以及静态数据暴露 [2, 14–16, 27, 35–37, 44]。通过在智能体通信上提供一个统一的执行点（图 1），NLIP 能够在独立开发的智能体框架之间实现一致的保护，同时保持互操作性。

## 6 实现与示例应用

NLIP 的灵活性与易用性已在参与组织的若干概念验证实现中得到探索。这些示例体现出一种共同的架构模式：NLIP 感知的智能体充当标准化 NLIP 交互层与异构底层系统之间的自适应接口，后者包括工具协议、企业 API、知识库、领域本体、工业标准以及厂商特定的服务。其中若干用例已在描述 NLIP 动机的技术报告 [20] 中有所阐述，包括：将 NLIP 用作问答服务、用作跨多个智能体进行联邦的代理、用作某个使用 MCP 调用工具的服务之前的网关 [20, 30]、用作基于语音的客服智能体，以及用作混合云环境中的服务集成器（具体是将 Active Directory 与 ServiceNow 系统集成）。在这一模式中，NLIP 并不取代 MCP。相反，NLIP 感知的智能体或网关向客户端暴露标准的 NLIP 接口，而内部使用 MCP 来调用工具与服务。MCP 仍是工具/服务协议，而 NLIP 为智能体与客户端提供交互信封。

### 6.1 NLIP 的参考实现

NLIP 协议配有开源的参考实现与软件开发工具包（Software Development Kit, SDK），包括 `nlip_sdk`、`nlip_client` 和 `nlip_server` [32]。这些库共同实现了 NLIP 协议的核心，包括消息结构、传输绑定、序列化以及客户端/服务器通信原语。这些 SDK 有意独立于智能体内部的应用逻辑与开发框架，使现有智能体与应用无需修改其内部执行模型就能采用 NLIP。这种分离让开发者可以专注于应用逻辑，同时依赖可复用、符合标准的实现来处理智能体通信，从而促进跨异构 AI 智能体生态的互操作。

### 6.2 向智能体开发框架的扩展与采用信号

NLIP 的框架无关架构使现有智能体系统能够通过轻量适配器暴露标准化的 NLIP 接口，而无需改变其内部推理、规划或工具调用逻辑。因此，使用不同框架开发的智能体可以通过一种共同协议与用户客户端及其他 NLIP 兼容智能体通信。

这种可扩展性已在 2026 年 4 月 NLIP 集成进 AG2 [1] 智能体开发框架时得到展示 [5, 6]。AG2 报告的月下载量超过一百万（2026 年 3 月为 1,087,122 次），日下载量超过 57,000 次、峰值超过 68,000 次，被工业界与研究界广泛应用于多样化的应用领域。随着 AG2 增加对 NLIP 的支持，这些部署为 NLIP 作为大规模智能体系统标准化交互层日益增长的足迹提供了早期证据。

### 6.3 NLIP 应用示例

**电信设备的自愈。** IBM 在 2025 年电信管理论坛（Telecommunications Management Forum, TMF）[40] 上展示了一个商业用例，其中一组智能 AI 智能体可以自动诊断设备故障的根因，并在适用策略允许的前提下自动重启或重新配置故障设备。与设备的通信采用 TMF 规定的标准进行，基于 NLIP 的 AI 智能体调用这些标准来监控和重新配置设备。该系统由两个智能体组成，它们利用 IBM Granite Mixture of Expert 模型来诊断并修复问题：一个负责识别根因（Event Agent），另一个负责确定应遵循的操作，以便通过 TMF Forum API 向客户告知任何问题。两个智能体之间使用 NLIP 相互通信。

在系统准备演示的过程中，人们发现了 NLIP 的一个有用特性。为了演示这些智能体的运行，需要一个演示控制台。通常的演示控制台需要支持一个特殊接口，以便从这次演示涉及的各个系统中获取演示信息；而 NLIP 提供了一个便捷的接口，可以把演示控制台架设在正在开发的系统之上。现有组件（即事件收集器）需要特殊接口来展示它正在执行什么，而基于 NLIP 的智能体无需任何额外的协议支持就能被演示。

**多模态 NLIP 智能体。** 在该用例 [20] 中，三个专用智能体——语音转文本智能体（Speech to Text Agent）、频道推荐智能体（Channel Recommender Agent）和搜索智能体（Search Agent）——使用 NLIP 协作，实时满足客户的语音支持请求。每个智能体在端到端交互流水线中扮演不同角色，展示了如何通过标准化通信与可互操作 API 来组合模块化 AI 组件。语音音频使用语音转文本模型被转写为文本。基于从客户请求中提取的关键词，系统识别出相关的 Reddit 频道。随后，一个专用搜索智能体查询这些频道，检索最新且相关的帖子，并实时将其返回给客户。

这段转写内容随后由频道推荐智能体处理，后者可能使用一个 LLM，从而具备上下文理解与意图抽取能力。此外，搜索智能体集成了 MCP 与 Reddit 的搜索 API，以检索相关的实时信息。这是 NLIP 用于面向客户端与智能体一侧的语义交互、而 MCP 用于内部访问工具与 API 的一个例子。该用例展示了多智能体系统如何跨外部知识源动态支持客户查询。

## 7 NLIP 与相关协议

NLIP 属于更广泛的智能体通信工作家族，从早期的智能体通信语言——如知识查询与操作语言（Knowledge Query and Manipulation Language, KQML）[23] 与智能物理代理基金会智能体通信语言（Foundation for Intelligent Physical Agents Agent Communication Language, FIPA ACL）[24, 25]——一直到近期的模型上下文协议（Model Context Protocol, MCP）[30]、Agent2Agent（A2A）[10]、智能体通信协议（Agent Communication Protocol, ACP）[7] 和智能体网络协议（Agent Network Protocol, ANP）[13] 等协议。AG-UI 则额外聚焦于智能体与用户之间的交互，提供一种基于事件的协议，用于将智能体与面向用户的应用连接起来 [4]。其他新兴工作则针对智能体生态的相邻部分，包括基于媒体 over QUIC 传输（Media over QUIC Transport, MoQ）的低延迟智能体传输提案，以及面向信任的协议——如用于智能体身份、授权与证明的智能体信任协议（Agent Trust Protocol, ATP）[28, 31, 33]。NLIP 项目的公开材料在 2024 年即可获得 [32]，随后在 2025 年 3 月于 AAAI '25 开源 AI 主流应用研讨会（AAAI '25 Workshop on Open-Source AI for Mainstream Use）上发表了综述论文 [11]。

最好将 NLIP 理解为一种中立的、应用层的语义交互协议，它对现有的智能体、工具与企业协议起补充而非替代作用。在模式 A（Mode A）中，NLIP 感知的智能体或网关向客户端及对等智能体暴露面向 NLIP 的接口，而在内部或面向底层服务时使用 MCP、A2A、ACP、企业 API 或工业协议等。在模式 B（Mode B）中，NLIP 感知的智能体在基于不同底层协议实现的智能体之间中介互操作。这使 NLIP 能够在碎片化的协议生态中充当语义协调层，同时保住各组织在工具协议、智能体框架与企业基础设施上的既有投资。与更狭窄的工具访问协议或智能体对智能体协议相比，NLIP 处理的是一个更宽泛的语义翻译边界，因此由 NLIP 感知的智能体进行显式接地（grounding）对于保留领域特定上下文尤为重要。

**与 Web 的类比。** 在智能体生态层面，NLIP 被设计为扮演一个类似于 Web 上 HTTP/HTTPS 的角色：一个共同的交互层，让独立实现的端点通过标准化消息相互通信。正如 Web 浏览器与服务器交换 HTTP/HTTPS 消息时并不关心其上承载的应用语义，AI 智能体也可以交换 NLIP 消息，而不管其内部框架、任务结构、工作流模式或执行环境如何。更高层的语义抽象——例如 A2A 的任务（task）与智能体卡片（agent card）——可以自然地承载在 NLIP 消息之中，正如 HTML 文档、REST API 或应用特定的数据格式通过 HTTP/HTTPS 传输。这种分层使 NLIP 适合作为一种通用的互操作基底，同时允许更专门的协议在其之上或旁边定义更高层的工作流语义。

### 7.1 NLIP 与 A2A 的实证比较

**设计目标。** 在高层次上，NLIP 与 A2A 都支持智能体对智能体的通信，但它们做出了不同的设计取舍。A2A 源自 Google，遵循一种任务导向的客户端-服务器模型，其中客户端智能体将工作委派给远程智能体 [12]。其协议模型包含预定义结构，例如任务（tasks）、包括 "input-required" 在内的任务状态（task states）[9]，以及字段固定的智能体卡片（agent cards）[8]。这些抽象支持结构化的任务委派，但也强加了一种特定的任务模型。相比之下，NLIP 不把任务、任务状态、工作流或委派关系硬编码进其核心消息模型；智能体通过 NLIP 消息自行定义交互语义，从而在异构系统之间支持任意对话、工作流与协调模式。

**性能开销。** A2A 更丰富的预定义结构可以支持治理密集型工作流，但可能在连接处理、消息交换、序列化与任务状态管理方面增加运行时开销。在一项受控比较中，使用同一个概念验证的三智能体客户支持工作流，在轻量协调阶段，NLIP 在两种硬件环境（16 GB 内存的 Apple M1 与 32 GB 内存的 Apple M2 Pro）上实现了比 A2A-SDK 低 8.4–9.6× 的延迟，而在第三台更快的机器（36 GB 内存的 Apple M3 Pro）上，这一差距收窄到约 4× [38, 39]。这些测量只界定了协议信封本身：LLM 推理在各智能体端点运行，不在本文所测的消息创建、连接与发送阶段之内。消息创建开销可忽略不计，A2A-SDK 连接的建立主导了这一差距。在启用连接缓存后，优势变得依硬件而定：NLIP 在一台机器上保持 2.75× 的领先，但在更快的一台机器上只有 1.27×。面对更优化的 Python-A2A，NLIP 在同一阶段保持了 4.1–4.3× 的优势 [38, 39]。这些结果表明，NLIP 可能非常适合频繁、轻量、延迟敏感的交互，而 A2A 式的任务抽象更适合长时间运行或治理密集型的工作流，并且可以承载在 NLIP 之上、与 NLIP 集成，或通过 NLIP 桥接。

## 8 结论

NLIP 是一个专门为现代 AI 智能体之间以自然语言为中心的交互而设计的正式标准，更广泛的采用正在出现。NLIP 更重要的意义在于：它标准化了交互的语义信封，而 NLIP 感知的智能体与网关则提供跨异构、领域特定智能体生态的自适应黏合。这使 NLIP 成为多协议、本体丰富且本地可控的 AI 部署的一个候选互操作层。

## 致谢

来自伊利诺伊大学厄巴纳-香槟分校（UIUC）的作者们部分受 NSF TI-2625398 资助。

## 参考文献

[1] [n. d.]. AG2 (formerly AutoGen). https://github.com/ag2ai/ag2.
[2] 2025. Model Context Protocol (MCP) Security Best Practices, Version 2025-11-25. https://modelcontextprotocol.io/specification/2025-11-25/basic/security_best_practices.
[3] Sahar Abdelnabi, Kai Greshake, Shailesh Mishra, Christoph Endres, Thorsten Holz, and Mario Fritz. 2023. Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection. In Proceedings of the 16th ACM Workshop on Artificial Intelligence and Security (AISec '23). ACM, 79–90. doi:10.1145/3605764.3623985
[4] AG-UI Protocol. 2026. AG-UI: The Agent-User Interaction Protocol. https://github.com/ag-ui-protocol/ag-ui. Accessed August 25, 2026.
[5] AG2 Contributors. 2026. Add Natural Language Interaction Protocol (NLIP) Support. GitHub Pull Request #2468. https://github.com/ag2ai/ag2/pull/2468
[6] AG2 Contributors. 2026. Enhancements to Natural Language Interaction Protocol (NLIP) Integration. GitHub Pull Request #3024. https://github.com/ag2ai/ag2/pull/3024
[7] Agent Communication Protocol Project. n.d.. Agent Communication Protocol (ACP) Documentation. https://agentcommunicationprotocol.dev/
[8] Agent2Agent Protocol Project. 2026. Agent Card. https://agent2agent.info/docs/concepts/agentcard/
[9] Agent2Agent Protocol Project. 2026. Task. https://agent2agent.info/docs/concepts/task/
[10] Agent2Agent Protocol Project. n.d.. Agent2Agent (A2A) Protocol Specification. https://a2a-protocol.org/latest/specification/
[11] Sanjay Aiyagari et al. 2025. An Overview of the Natural Language Interaction Protocol. In AAAI 2025 Workshop on Open-Source AI for Mainstream Use. https://www.eecis.udel.edu/~mlm/docs/2025-Aiyagari-AAAI-25-AnOverviewOfTheNaturalLanguageInteractionProtocol-Workshop.pdf
[12] Alan Blount, Frank Guan, and Nick Losier. 2026. How A2A Is Building a World of Collaborative Agents. Google Developers Blog. https://developers.googleblog.com/how-a2a-is-building-a-world-of-collaborative-agents/
[13] Gaowei Chang, Eidan Lin, Chengxuan Yuan, Rizhao Cai, Binbin Chen, Xuan Xie, and Yin Zhang. 2025. Agent Network Protocol Technical White Paper. arXiv preprint arXiv:2508.00007 (2025). doi:10.48550/arXiv.2508.00007
[14] Jay Chen, Royce Lu, and Palo Alto Networks Unit 42. 2025. When AI Agents Go Rogue: Agent Session Smuggling Attack in A2A Systems. https://unit42.paloaltonetworks.com/agent-session-smuggling-in-agent2agent-systems/.
[15] Zhaorun Chen, Zhen Xiang, Chaowei Xiao, Dawn Song, and Bo Li. 2024. Agentpoison: Red-teaming llm agents via poisoning memory or knowledge bases. Advances in Neural Information Processing Systems 37 (2024), 130185–130213.
[16] Jian Cui, Zichuan Li, Luyi Xing, and Xiaojing Liao. 2025. Safeguard-by-development: A privacy-enhanced development paradigm for multi-agent collaboration systems. arXiv preprint arXiv:2505.04799 (2025).
[17] Ecma International. 2025. Binding of the Natural Language Interaction Protocol (NLIP) over AMQP.
[18] Ecma International. 2025. Binding of the Natural Language Interaction Protocol (NLIP) over HTTP/HTTPS.
[19] Ecma International. 2025. Binding of the Natural Language Interaction Protocol (NLIP) over WebSocket.
[20] Ecma International. 2025. Explanatory Guide to the Natural Language Interaction Protocol (NLIP) (1 ed.). Report ECMA TR/113.
[21] Ecma International. 2025. Natural Language Interaction Protocol (NLIP).
[22] Ecma International. 2025. Security Profiles for Natural Language Interaction Protocol (NLIP).
[23] Tim Finin, Richard Fritzson, Donald P. McKay, and Robin McEntire. 1994. KQML as an Agent Communication Language. In Proceedings of the Third International Conference on Information and Knowledge Management (CIKM '94) (Gaithersburg, MD, USA). ACM, 456–463. doi:10.1145/191246.191322
[24] Foundation for Intelligent Physical Agents. 2002. FIPA ACL Message Structure Specification. http://www.fipa.org/specs/fipa00061/SC00061G.html
[25] Foundation for Intelligent Physical Agents. 2002. FIPA Communicative Act Library Specification. http://www.fipa.org/specs/fipa00037/SC00037J.html
[26] Tommaso Green, Martin Gubri, Haritz Puerto, Sangdoo Yun, and Seong Joon Oh. 2025. Leaky Thoughts: Large Reasoning Models Are Not Private Thinkers. In Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing (EMNLP).
[27] Abhinav Kumar, Jaechul Roh, Ali Naseh, Marzena Karpinska, Mohit Iyyer, Amir Houmansadr, and Eugene Bagdasarian. 2025. Overthink: Slowdown attacks on reasoning llms. arXiv preprint arXiv:2502.02542 (2025).
[28] D. Liu and S. Krishnan. 2026. Agent Protocol over MoQ. Internet-Draft draft-liu-agent-protocol-over-moq-00. IETF. https://www.ietf.org/archive/id/draft-liu-agent-protocol-over-moq-00.html
[29] Matthieu Meeus, Shubham Jain, Marek Rei, and Yves-Alexandre de Montjoye. 2024. Did the Neurons Read your Book? Document-level Membership Inference for Large Language Models. In Proceedings of the 33rd USENIX Security Symposium (USENIX Security 24).
[30] Model Context Protocol Contributors. 2025. Model Context Protocol Specification, version 2025-11-25. https://modelcontextprotocol.io/specification/2025-11-25
[31] S. Nandakumar and C. Jennings. 2026. MOQ Transport for Agent Protocols. Internet-Draft draft-nandakumar-ai-agent-moq-transport-00. IETF. https://www.ietf.org/archive/id/draft-nandakumar-ai-agent-moq-transport-00.html
[32] NLIP Project Contributors. 2024. NLIP Project Documents. https://github.com/nlip-project/documents
[33] OTT Cybersecurity LLC. 2026. Agent Trust Protocol (ATP). https://github.com/OTT-Cybersecurity-LLC/lyrie-ai/blob/main/packages/atp/README.md
[34] OWASP Foundation. 2025. OWASP Top 10 for Large Language Model Applications: LLM01:2025 Prompt Injection. https://genai.owasp.org/llm-top-10/
[35] OWASP GenAI Security Project. 2025. LLM10:2025 Unbounded Consumption. https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/.
[36] Ayush RoyChowdhury, Mulong Luo, Prateek Sahu, Sarbartha Banerjee, and Mohit Tiwari. 2024. Confusedpilot: Confused deputy risks in rag-based llms. arXiv preprint arXiv:2408.04870 (2024).
[37] Avital Shafran, Roei Schuster, and Vitaly Shmatikov. 2025. Machine Against the {RAG}: Jamming {Retrieval-Augmented} Generation with Blocker Documents. In 34th USENIX Security Symposium (USENIX Security 25). 3787–3806.
[38] Ranjan Sinha, Anindita Das, Ashika Anand Babu, and Hari Palleti. 2026. The Cost of a Hop: Benchmarking NLIP and A2A. (2026). Submitted to the IEEE International Conference on Big Data (IEEE BigData).
[39] Ranjan Sinha, Anindita Das, Ashika Anand Babu, and Hari Palleti. n.d.. Protocol-Level Efficiency in Agent Communication: An Empirical Comparison of NLIP and A2A. In 30th Annual CASIS Workshop.
[40] TM Forum. 2026. TM Forum. https://www.tmforum.org/
[41] Shouju Wang, Fenglin Yu, Xirui Liu, Xiaoting Qin, Jue Zhang, Qingwei Lin, Dongmei Zhang, and Saravan Rajmohan. 2025. Privacy in action: Towards realistic privacy mitigation and evaluation for llm-powered agents. arXiv preprint arXiv:2509.17488 (2025).
[42] Qiusi Zhan, Zhixiang Liang, Zifan Ying, and Daniel Kang. 2024. InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated Large Language Model Agents. In Findings of the Association for Computational Linguistics: ACL 2024 (Bangkok, Thailand). Association for Computational Linguistics, 10471–10506. doi:10.18653/v1/2024.findings-acl.624
[43] Muyang Zheng, Yuanzhi Yao, Changting Lin, Rui Wang, and Meng Han. 2025. MIST: Jailbreaking Black-box Large Language Models via Iterative Semantic Tuning. ArXiv abs/2506.16792 (2025).
[44] Wei Zou, Runpeng Geng, Binghui Wang, and Jinyuan Jia. 2025. {PoisonedRAG}: Knowledge corruption attacks to {Retrieval-Augmented} generation of large language models. In 34th USENIX Security Symposium (USENIX Security 25). 3827–3844.
