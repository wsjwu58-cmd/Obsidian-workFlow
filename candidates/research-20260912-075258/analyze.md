已核对知识库现状（`references/articles.md` 29 篇正式收录、`expand/thinking/` 2 条、`expand/06-AI与LLM/` 9 条、上一批研究的 gaps_open 清单）与 `research.py` 三档分流逻辑。以下为完整分析。

## 1. 优先级排序

本批 10 条全部命中 Agent harness 主线，质量罕见地集中；跨平台方向连续第三轮零信号。排序如下（P0 最高）：

| 优先级 | 候选 | 与已收录/已跟踪内容的互补 | 对既有洞见的验证/挑战 | 对开放问题的回答 |
|---|---|---|---|---|
| P0 | [1] Google 行为评估 | 补 [22]/[23] 只测"任务侧、复合分"的空档；[19] 是"从失败轨迹改 harness"，本条给出"改完怎么知道没变差" | **验证** [23]「功能通过≠工程正确」并升级为"过程断言"；**挑战** [22] 式端到端跑分作为迭代信号的充分性 | **直接命中**上批 gaps_open 明确写着的「Harness 自身行为/覆盖率的度量工具」，且给可复现代码 |
| P0 | [2] OpenAI Agents API | 与 [16] Muse Code、观察项 Claude Managed Agents 构成托管平台三角；把 [07] n8n、[14] MCP 之上的"会话/沙箱/子代理"层补齐 | **验证** [06] ECC「harness 是工程化主战场」：官方把 harness + 基础设施显式两层化；**挑战** 多代理"独立上下文"是否等于隔离安全 | 回答「多智能体编排与成本」「harness 分层」，但把上下文/沙箱治理转嫁给平台 |
| P0 | [3] LangChain context modes | 直接续 [29] 上下文工程、[30] Headlong、观察项 Deep Agents；把「隔离 vs 复用」从经验变成 `isolated/fork` 两个 API 取值 | **补充并部分挑战** [25] AgentRoom「协调优于并发」：协调的代价来自重复上下文收集，fork 可消除 | 回答「上下文/compaction/记忆可复现实践」+「多智能体编排反模式（重复收集浪费）」 |
| P1 | [4] Dan Luu 验证技术实测 | 与 [23] SWE-Gate、[26] Code Review、[24] Committed AI Config 直接对话 | **强挑战**「多测多审就好」的隐含假设：给技术名字几乎无效；SMT 证错对象；TDD 跑输默认 | 回答「harness 行为正确性与覆盖率评估」——瓶颈在验证知识，而非模型 |
| P1 | [5] imec harness×model 成本 | 与 [22] FrontierHarness（17× 成本差）独立互证；补 [23] 只谈正确性、不谈成本经济学 | **验证**「harness 主要影响成本而非准确率」；量化 44–53% 收敛 + token 翻倍 | 回答「组件级归因」「中小团队成本数据」（部分） |
| P1 | [7] SoL-Pi | 与 [06]/[18]/[19] 同属 harness 自演化，但目标函数从正确率换成效率；补 [29] compaction 的"可复用机制" | **验证**「自动研究改 harness」范式可迁移到成本维度；**提示** 效率机制必须服务正确性（不早停/不跳过验证） | 回答「上下文/compaction 可复现实践」+ 成本数据 |
| P2 | [6] 掘金 8 Skill 全链路 | 把 [20] 单点契约扩为多角色、可追踪、可回写的团队工作流，与 [24]「提交式配置」实证印证 | **验证** [24]：配置形式有效；**补充** [26]：把"何时停下问人"写进契约 | 回答「中小团队落地案例」+「激活策略（human-summoned 决策点）」 |
| P2 | [10] Beyond Prompts | 为 [22]/[05] 的对比提供可复现统计协议；与 [18]/[19] 的"演化"互补为"选择" | **挑战** 单点 benchmark 选型：应以预算 B 下保守收益 `RelLift95(B)` 汇报 | 回答「组件级归因」的方法论口径（无开源实现） |
| P2 | [8] mini-harness | 把 [29] 上下文工程、[22]/[05] 评测讨论落到 ~1700 行可读代码 | **提供底座**：可对 [18][19][07] 的效率/演化结论做低成本复现 | 回答「可复现实践」；自报基准需存疑 |
| P3 | [9] HarnessME | 延伸 [20] AGENTS.md 与 [24]；用工具化缓解 [31] 的 context 特权提升 | **补充** [31]：关键路径人工闸门是一种（未验证的）缓解；填补"AGENTS.md 自动生成 + 防漂移"工具缺口 | 回答「激活策略（conditional/human-summoned）」；项目过新，仅作线索 |

排序理由：P0 三条各自**直接填一个此前明确未闭合的缺口**，且两条是 Tier 1 一手；P1 三条提供**独立复现或反直觉证据**，用于校正既有结论；P2/P3 为落地与工具线索。

## 2. 缺口分析

**本批覆盖的缺口**

| 缺口 | 命中内容 |
|---|---|
| Agent harness 行为正确性与覆盖率评估 | [1] 行为评估断言中间步骤（上批 gaps_open 点名空缺）；[4] 30 条件 × ~80 次验证技术实测 |
| 上下文 / compaction / 记忆可复现实践 | [3] isolated/fork 两模式 + 配置；[7] Online Context Compact / Evidence-Preserving Reducer；[8] 教学型 compaction |
| 多智能体编排反模式与成本 | [3] isolated 重复收集上下文的 token/时间浪费；[2] 子代理独立上下文 + `max_concurrent_subagents` |
| Agent 评测：model/harness/环境组件级归因 | [5] 3 harness × 2 model × 64 任务；[10] 资源受限选择协议；[1] 过程级归因 |
| 中小团队 Agent 工程落地与成本数据 | [6] 企业 8-Skill 全链路 + 目录约定 + 反模式；[5][7] 成本数据 |
| Harness/控制激活策略 | [6]「模糊处停下等人」决策点；[9] Critical Gate Manager；[1] 行为断言作防回退闸门 |
| Agent 安全审计（部分） | [9] 关键路径人工闸门缓解 [31] 的上下文特权提升 |
| 跨模型可移植性（部分） | [10] optimizer-agnostic、不改模型只改 middleware；[5] 跨模型 token 对照 |

**仍未被触及的缺口**

- 跨模型可移植性与迁移指南：本批仍是"同模型换 harness"，没有 harness/模型迁移的实操路径。
- KMP / Compose Multiplatform 与 Flutter 架构选型、共享逻辑边界、工具链痛点（**连续三轮空窗**）。
- 跨平台 CI / 发布 / 性能基线（同上空窗）。
- Agent 安全审计完整面：缺轨迹违规检测、多智能体信息流、工具权限边界的系统研究，[9] 仅给工具级闸门。
- 多智能体权限隔离设计原语：[2] 的"独立上下文"是上下文隔离，不等于权限/凭据隔离，与 [31] 的攻击面存在缺口。
- 长时程/持续 agent 评测方法论：[2] 提供基础设施，但"跑数天怎么评"仍无基准。
- 生产环境组件级归因：[5] 触及 doom-loop、prefix caching 异常，但未展开环境/网关/仓库规模维度。
- 正确率–成本帕累托：[7] 以"不早停/不跳过验证"作约束，但未给出质量-成本联合基线。

## 3. 趋势信号

- **Harness 工程进入"护栏化/过程化"阶段**：[1] 用行为断言替代复合分，[4] 证明给技术名字无效、[23] 说明功能通过不够——三方合流为同一判断：**评估粒度必须下沉到中间步骤**，与既有 [22]/[23] 一致且更进一步。
- **上下文治理从"压缩"扩展到"继承策略"**：[3] 把上下文复用变成 API 取值，[7] 把 compaction 变成经济性触发——续 [29][30] 主线，多智能体 harness 开始有可复用的上下文原语。
- **Harness 自演化目标函数从正确率转向成本效率**：[7] 与 [06][18][19] 同路线但换目标，预示"自动研究"下一步会搜效率与证据保全机制。
- **托管 agent 平台成为主战场**：[2] 把 harness（上下文/工具/子代理）+ 基础设施（沙箱/长任务/持久化）产品化为 API，与 Muse Code、Claude Managed Agents 形成平台三角；平台化的同时，harness 内部细节被隐藏，**可归因性下降**。
- **"机制 > 指令"浮现为共识**：[4] 教程式技能无效、[1] 行为断言与 [9] 关键路径闸门有效、[6] 决策点写进契约——与 [24]「配置形式有效」一致，但对 [26]「多审多测」构成反例。
- **评测方法趋于统计协议化**：[10] `RelLift95(B)`、worst-condition lift，[5] 独立复现，[22] 受控矩阵——选型从单点跑分走向"带保守估计的协议 + 多源互证"。
- **冲突点**：[3] fork 继承主管上下文与 [31] context privilege escalation 存在张力（注入内容可能随 fork 传播）；[4] 的悲观结论与 [23] 的"双门控可提升验收"并不矛盾，但说明**约束必须机械化、可执行**。
- **跨平台连续第三轮零信号**：KMP/Flutter 需换定向信源（官方 changelog、JetBrains blog、Klibs.io），否则将持续失联。

## 4. 收录建议

| 候选 | verdict | lineage | 一句话理由 |
|---|---|---|---|
| [1] Anatomy of Harness Engineering | `translate` | `agent/eval` | Tier 1 一手方法 + 可复现代码，直接填「harness 行为/覆盖率度量」这一此前明确空缺，必全文留存 |
| [2] Introducing the Agents API | `translate` | `agent/platform` | Tier 1 官方把 harness + 基础设施两层与子代理原语定调，是托管平台三角的关键一手文本 |
| [3] Organizing Context in a Multi-Agent Harness | `translate` | `agent/context` | Tier 1 官方给出 isolated/fork 两个可落地取值的上下文模式抽象 + 配置，值得全篇留存 |
| [4] How well do agents use test/verification techniques? | `translate` | `agent/eval` | 罕见大规模预注册实验，结论反直觉且直接挑战 [23][24][26]，实验细节值得全篇保存 |
| [5] Does your harness matter more than your model? | `index` | `agent/eval` | 对 [22] 的独立复现 + 成本经济学量化，价值在数据与归因结论而非全文（与 [22] 处理一致） |
| [6] 企业级 AI Coding 的 Harness 工程实战：8 个 Skill | `translate` | `agent/harness` | 中文一线企业级多角色工作流，含目录约定与失败反模式，把 [20] 从单点契约扩展到团队闭环 |
| [7] SoL-Pi | `translate` | `agent/harness` | 有代码、公开博客与量化省钱数据的"自动研究改 harness 效率"新范式产物，续 [18][19] 主线 |
| [8] mini-harness | `index` | `agent/harness` | 约 1700 行覆盖 harness 全要素的可读实现，价值在可复现代码底座（索引 + 链接） |
| [9] HarnessME | `index` | `agent/harness` | AGENTS.md 自动生成 + 防漂移 + 关键路径闸门，直接回应激活策略与 [31] 的缓解工具线索，但项目过新 |
| [10] Beyond Prompts | `index` | `agent/eval` | 给出 harness 选择协议与保守收益指标 `RelLift95(B)`，方法价值高但无开源实现，索引即够 |

`translate + index` 合计 10 条（5 + 5），满足门槛；无 `observe`——每条都对上方缺口有直接增量，降级为 observe 会违反"直接命中缺口至少 index"的规则。

```json
{
  "analysis": {
    "priority": [
      "P0 [1] Google 行为评估：Tier 1 一手方法 + 可复现代码，直接命中原 gaps_open 的『harness 自身行为/覆盖率度量工具』空缺，把评估粒度从复合分下沉到中间步骤",
      "P0 [2] OpenAI Agents API：Tier 1 官方把 harness 与基础设施两层显式化并提供子代理原语，是托管 agent 平台竞争三角的关键定调文本",
      "P0 [3] LangChain context modes：Tier 1 官方把『上下文隔离 vs 复用』变成 isolated/fork 两个可落地 API 取值，直接补上下文治理与多智能体反模式缺口",
      "P1 [4] Dan Luu 预注册实验：30 种验证技术各约 80 次实测，反直觉地挑战『多测多审就好』，是校正既有评测假设的稀缺证据",
      "P1 [5] imec harness×model：独立复现 [22] 的『准确率收敛、成本翻倍』结论并给出成本经济学数据，直接服务选型与组件级归因",
      "P1 [7] SoL-Pi：有代码、博客与量化省钱数据的 harness 效率机制集合，续 [18][19] 自演化主线但换目标函数为成本",
      "P2 [6] 掘金 8 Skill：中文一线企业级多角色 harness 工作流，补中小团队落地与 human-summoned 决策点缺口",
      "P2 [10] Beyond Prompts：给出资源受限下的 harness 选择协议与保守收益指标 RelLift95(B)，统一评测口径",
      "P2 [8] mini-harness：覆盖 harness 全要素的可读最小实现，为复现既有 harness 研究提供低门槛底座",
      "P3 [9] HarnessME：AGENTS.md 自动生成 + 防漂移 + 关键路径闸门，作激活策略与 [31] 缓解的工具线索，但项目很新需观察"
    ],
    "gaps_covered": [
      "Agent harness 行为正确性与覆盖率评估：[1] 行为评估断言中间步骤并给可复现代码（原 gaps_open 点名空缺），[4] 30 条件×约 80 次的验证技术实测",
      "上下文/compaction/记忆可复现实践：[3] isolated/fork 上下文模式+配置，[7] Online Context Compact 与 Evidence-Preserving Reducer，[8] 教学型 compaction 实现",
      "多智能体编排反模式与成本：[3] isolated 重复收集上下文的 token/时间浪费，[2] 子代理独立上下文与 max_concurrent_subagents 原语",
      "Agent 评测组件级归因：[5] 3 harness×2 model×64 任务量化，[10] 资源受限选择协议，[1] 过程级归因",
      "中小团队 Agent 工程落地案例与成本数据：[6] 企业 8-Skill 全链路目录约定与反模式，[5][7] 成本与省钱数据",
      "Harness/控制激活策略：[6]『模糊处停下等人』决策点，[9] Critical Gate Manager 关键路径闸门，[1] 行为断言作防回退闸门",
      "Agent 安全审计（部分）：[9] 关键路径人工闸门可缓解 [31] 的上下文特权提升",
      "跨模型可移植性（部分）：[10] optimizer-agnostic 且不改模型只改 middleware，[5] 跨模型 token 对照"
    ],
    "gaps_open": [
      "跨模型可移植性与迁移指南：本批均为同模型换 harness，缺模型/harness 迁移实操路径",
      "KMP/Compose Multiplatform 与 Flutter 架构选型、共享逻辑边界、工具链痛点（连续三轮空窗）",
      "跨平台 CI/发布/性能基线（连续三轮空窗）",
      "Agent 安全审计完整面：缺轨迹违规检测、多智能体信息流、工具权限边界系统研究，[9] 仅工具级闸门",
      "多智能体权限隔离设计原语：[2] 的独立上下文是上下文隔离而非权限/凭据隔离",
      "长时程/持续 agent 评测方法论：[2] 给基础设施但无评判基准",
      "生产环境组件级归因：[5] 触及 doom-loop/prefix caching 异常但未展开环境/网关/仓库规模维度",
      "正确率-成本帕累托基线：[7] 以不早停/不跳过验证为约束，但未给质量-成本联合前沿"
    ],
    "trends": [
      "Harness 工程进入护栏化/过程化阶段：评估粒度从端到端复合分下沉到中间步骤行为断言，[1][4] 与既有 [22][23] 三方合流",
      "上下文治理从压缩扩展到继承策略：[3] 把隔离与复用变成 API 取值，[7] 把 compaction 变成经济性触发，延续 [29][30] 主线",
      "Harness 自演化目标函数从正确率转向成本效率：[7] 与 [06][18][19] 同路线但改搜效率与证据保全机制",
      "托管 agent 平台成为主战场：[2] 把 harness 与基础设施产品化为 API，与 Muse Code、Claude Managed Agents 形成平台三角，代价是 harness 内部可归因性下降",
      "机制大于指令成为共识：[4] 教程式技能无效，[1] 行为断言、[9] 关键路径闸门、[6] 契约化决策点有效，与 [24] 一致并对 [26] 构成反例",
      "评测方法趋于统计协议化：[10] RelLift95(B) 与 worst-condition lift，[5] 独立复现，[22] 受控矩阵，选型走向带保守估计的协议",
      "存在张力：[3] fork 继承上下文与 [31] 上下文特权提升攻击面冲突，注入内容可能随 fork 传播",
      "跨平台连续第三轮零信号：建议对 Kotlin/CMP/Flutter 官方 changelog、JetBrains blog、Klibs.io 定向补源"
    ]
  },
  "candidates": [
    {
      "title": "The Anatomy of Harness Engineering: How to Evaluate, Iterate, and Guard AI Coding Agents",
      "url": "https://developers.googleblog.com/the-anatomy-of-harness-engineering-how-to-evaluate-iterate-and-guard-ai-coding-agents/",
      "verdict": "translate",
      "lineage": "agent/eval",
      "reason": "Tier 1 一手方法论加可复现代码，用行为评估断言中间步骤，直接填补此前明确空缺的 harness 自身行为/覆盖率度量工具",
      "stars": 5
    },
    {
      "title": "Introducing the Agents API",
      "url": "https://openai.com/index/introducing-the-agents-api/",
      "verdict": "translate",
      "lineage": "agent/platform",
      "reason": "Tier 1 官方把 harness 与基础设施两层显式化并提供 multi_agent 原语，是托管 agent 平台竞争格局的关键定调文本",
      "stars": 5
    },
    {
      "title": "Organizing Context in a Multi-Agent Harness",
      "url": "https://www.langchain.com/blog/organizing-context-in-a-multi-agent-harness",
      "verdict": "translate",
      "lineage": "agent/context",
      "reason": "Tier 1 官方给出 isolated/fork 两个可落地取值的上下文模式抽象与 deepagents 配置，直接补上下文治理与多智能体成本缺口",
      "stars": 5
    },
    {
      "title": "How well do agents use test/verification techniques?",
      "url": "https://danluu.com/agentic-testing/",
      "verdict": "translate",
      "lineage": "agent/eval",
      "reason": "大规模预注册实验证明给验证技术名字几乎无效，反直觉地挑战多测多审假设，实验细节值得全篇留存",
      "stars": 5
    },
    {
      "title": "Does your harness matter more than your model?",
      "url": "https://aistack.imec-int.com/blog/harness-cost",
      "verdict": "index",
      "lineage": "agent/eval",
      "reason": "独立复现 FrontierHarness 的准确率收敛与成本翻倍结论并补 token 经济学，价值在数据与归因而非全文",
      "stars": 4
    },
    {
      "title": "企业级 AI Coding 的 Harness 工程实战：8 个 Skill 串起全链路",
      "url": "https://juejin.cn/post/7680079424891011124",
      "verdict": "translate",
      "lineage": "agent/harness",
      "reason": "中文一线企业级多角色 harness 工作流，含可复制目录约定、失败反模式与停下等人类闸门，把单点契约扩展为团队闭环",
      "stars": 4
    },
    {
      "title": "SoL-Pi: Scaling Auto-Research Loops for Efficient Agent Harnesses",
      "url": "https://github.com/NVlabs/SoL-Pi",
      "verdict": "translate",
      "lineage": "agent/harness",
      "reason": "有代码、公开博客与量化省钱数据的 harness 效率机制集合，是自动研究改 harness 范式在成本维度上的具体产物",
      "stars": 4
    },
    {
      "title": "mini-harness",
      "url": "https://github.com/mini-harness/mini-harness",
      "verdict": "index",
      "lineage": "agent/harness",
      "reason": "约 1700 行覆盖 agent loop/工具/压缩/重试/TUI 全要素的可读实现，价值在可复现代码底座而非全文翻译",
      "stars": 4
    },
    {
      "title": "HarnessME",
      "url": "https://github.com/Bonhollow/harnessme",
      "verdict": "index",
      "lineage": "agent/harness",
      "reason": "AGENTS.md 自动生成加防漂移与关键路径人工闸门，回应激活策略并缓解上下文特权提升，但项目很新仅作工具线索收录",
      "stars": 3
    },
    {
      "title": "Beyond Prompts: Measuring and Optimizing LLM Tool-Agent Harnesses",
      "url": "https://arxiv.org/abs/2609.05736",
      "verdict": "index",
      "lineage": "agent/eval",
      "reason": "提出资源受限下的 harness 选择协议与保守收益指标 RelLift95(B)，统一评测口径，方法论价值高但暂无开源实现",
      "stars": 4
    }
  ]
}
```