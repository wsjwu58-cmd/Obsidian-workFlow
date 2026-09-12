以下为过去两周（2026-08-29 至 2026-09-12）技术情报搜索结果，共 10 条（5 文章 / 1 工具 / 3 开源项目 / 1 论文），均经 Firecrawl 核实发布日期与正文细节。

---

#### [1]. The Anatomy of Harness Engineering: How to Evaluate, Iterate, and Guard AI Coding Agents

- **类型：** 文章
- **链接：** https://developers.googleblog.com/the-anatomy-of-harness-engineering-how-to-evaluate-iterate-and-guard-ai-coding-agents/
- **作者/组织：** Taylor Mullen（Principal Engineer）、Christian Gunderman（Staff Software Engineer）/ Google
- **日期：** 2026-09-09
- **信源层级：** Tier 1
- **推荐指数：** ⭐⭐⭐⭐⭐

**一句话摘要：** 主张用"行为评估"（behavioral evals）替代端到端基准，作为 harness 迭代与防回退的护栏。

**核心洞察（3-5 条）：**

1. 端到端基准（Terminal-Bench/DeepSWE）分数变动无法定位原因；行为评估断言中间步骤——面对模糊需求是否先提问、改构建文件前是否跑校验、工具调用是否正确——相当于 harness 的集成测试。
2. harness 开发分两阶段：先靠 dogfooding 与直觉 bootstrap，等 agent 能处理自身代码库后再引入 evals；评估的首要目的是"确认没有整体变差"，而非庆祝 +2%。
3. 行为断言应做成快速、确定性、可本地运行的 unit 级检查，从而在改 prompt、改工具 schema、换模型时立刻发现核心行为破坏。
4. 给出基于 Antigravity SDK 的可运行示例与开源仓库链接，方法可直接复现。

**与已知内容的关联：**

- 扩展 [22] FrontierHarness Eval（多 harness 成本对比）与 [19] Harness-R1（从失败轨迹改 harness）。
- 与 [23] SWE-Gate（"功能测试通过≠工程正确"）同向：都否定"只看复合分"。
- 填补"日常迭代中用什么信号当 harness 护栏"的方法论缺口。

**值得收录的理由 / 不值得的理由：**
Tier 1 一手工程方法 + 可复现代码，直击 harness 迭代缺反馈信号的核心痛点，必收。

---

#### [2]. Introducing the Agents API

- **类型：** 工具（托管 Agent 平台 / API）
- **链接：** https://openai.com/index/introducing-the-agents-api/
- **作者/组织：** OpenAI
- **日期：** 2026-09-10
- **信源层级：** Tier 1
- **推荐指数：** ⭐⭐⭐⭐⭐

**一句话摘要：** 把 Codex harness 变成托管服务：一次 API 调用跑云端长任务，含托管沙箱与子代理编排。

**核心洞察（3-5 条）：**

1. 长程 agent 需要两层同时具备：harness（上下文管理、工具、子代理协调）+ 基础设施（能连跑数天的环境、文件与代码执行、中间结果保存）。
2. 多代理原语化：`multi_agent.enabled` 与 `max_concurrent_subagents`，每个子代理持有独立上下文，主代理协调并汇总——直接回应"上下文隔离 vs 复用"。
3. 执行环境三选一：OpenAI 托管沙箱 / 自建基础设施 / 沙箱合作伙伴；托管沙箱复用 Codex 与 ChatGPT 的隔离底座，可按文件、包、skills、plugins 配置。
4. 声称基于开源 foundation 构建"持续演进的 Codex harness"，在模型/harness 迭代时保持 API 稳定。

**与已知内容的关联：**

- 与 [16] Meta Muse Code 及观察项中的 Claude Managed Agents / Auto mode 构成"托管 agent 平台"竞争三角。
- 把 [07] n8n、[14] MCP 之上缺失的"会话 / 沙箱 / 子代理"层补齐，是 Agent Infrastructure 主题的方向性事件。

**值得收录的理由 / 不值得的理由：**
形态上是产品发布，但含 harness 分层、沙箱架构、子代理上下文隔离等实质技术设定，属 Tier 1 平台定调，值得收录。

---

#### [3]. Organizing Context in a Multi-Agent Harness

- **类型：** 文章
- **链接：** https://www.langchain.com/blog/organizing-context-in-a-multi-agent-harness
- **作者/组织：** LangChain
- **日期：** 2026-09-08
- **信源层级：** Tier 1
- **推荐指数：** ⭐⭐⭐⭐⭐

**一句话摘要：** deepagents 新增 context modes（isolated/fork），让子代理按需继承主管上下文而非一律从零开始。

**核心洞察（3-5 条）：**

1. 默认 isolated 子代理上下文干净，但会重复主管已完成的上下文收集（如重复读文件），造成 token 与时间浪费。
2. fork 模式把主管当前状态（含对话历史）整体传给子代理，等价于当前线程的分叉延续，最终收敛为单条 tool result 返回主管。
3. 复用主管对话可吃到 prompt caching，通常更快更省；选 isolated 还是 fork 取决于子代理用途（worker/reviewer）。
4. 给出 supervisor + worker + reviewer 模式及 deepagents 的具体配置方式。

**与已知内容的关联：**

- 直接补充 [29] Context Engineering for Coding Agents 的 compaction 与渐进式披露。
- 是 [25] AgentRoom（并发多代理共享工作区）与观察项 Deep Agents 的上下文治理续篇，把"上下文隔离 vs 复用"从经验变成两个 API 取值。

**值得收录的理由 / 不值得的理由：**
Tier 1 官方给出可落地的上下文模式抽象，紧贴 multi-agent harness 设计，必收。

---

#### [4]. How well do agents use test/verification techniques?

- **类型：** 文章（预注册实验）
- **链接：** https://danluu.com/agentic-testing/
- **作者/组织：** Dan Luu
- **日期：** 2026-09-09（原文页无日期，据 HN 提交时间核实）
- **信源层级：** Tier 3（资深工程实践者，HN 188 分）
- **推荐指数：** ⭐⭐⭐⭐⭐

**一句话摘要：** 30 种测试/验证条件各约 80 次跑 Zstd 实现：几乎没有技术明显胜出，Default 反高于平均。

**核心洞察（3-5 条）：**

1. 只给"用 TDD / QuickCheck / Lean 4 / Kani…"这类名字，agent 基本不会真正用对：TDD 如预测般跑输；SMT 常被当草稿纸，证了错的对象仍写错代码。
2. 有效信号来自"把 agent 从默认行为拨开"的小 skill（作者 2 分钟写的），而非教程式技能；codex 推荐的高星 skill 表现不佳。
3. Fuzzing 只有在生成结构化随机输入时（160 次中 10 次）才真正找到 bug，多数只是灌随机字节走无效路径。
4. 失败多为 idiosyncretic，而非"某语言/某技术更适合 agent"；瓶颈可能是有效测试知识本身不普及。

**与已知内容的关联：**

- 强烈挑战 [23] SWE-Gate 与 [26] Maybe We Shouldn't Be Reviewing All This Code 的隐含假设（"多测多审就好"）。
- 与 [24] A Few Pages of Markdown 互补：后者说"配置形式"有效，本文说"指令内容本身不足"。

**值得收录的理由 / 不值得的理由：**
罕见的大规模预注册实验，直指 harness 反馈系统设计的核心（验证信号），结论反直觉，值得收录。

---

#### [5]. Does your harness matter more than your model?

- **类型：** 文章（第三方实测）
- **链接：** https://aistack.imec-int.com/blog/harness-cost
- **作者/组织：** Bohdan D., Ioana F., Michaël M., Baptist V., Wouter V.d.B. / imec aistack
- **日期：** 2026-09-01
- **信源层级：** Tier 2
- **推荐指数：** ⭐⭐⭐⭐

**一句话摘要：** 3 个 harness × 2 个模型跑 64 个 SWE-Bench Pro 任务：准确率几乎不变，但 token 账单可翻倍。

**核心洞察（3-5 条）：**

1. Codex / Claude Code / Pi 的解决率都落在 44–53%，差异仅 2–3 个任务；仅凭准确率选 harness 意义不大。
2. 差异在 token：同模型下 Claude Code 输入 token（445.8M / 480.2M）显著高于 Codex（330.5M / 192.1M），却未换来更多解决。
3. 每个已解决任务成本区间 $0.35–$0.70；输出 token 直接占用 GPU 时长，影响每小时吞吐。
4. doom-loop、prefix caching 错误等异常会显著推高账单，必须盯遥测。

**与已知内容的关联：**

- 与 [22] FrontierHarness Eval（9 harness cost-per-pass 17×）、观察项 Data-eng-bench 的"harness×模型双变量"一致，且提供独立复现。
- 补充 [23] SWE-Gate 只谈正确性、不谈成本经济学的缺口。

**值得收录的理由 / 不值得的理由：**
独立第三方实测，明确量化"harness 主要影响成本而非准确率"，可直接用于选型。

---

#### [6]. 企业级 AI Coding 的 Harness 工程实战：8 个 Skill 串起全链路

- **类型：** 文章
- **链接：** https://juejin.cn/post/7680079424891011124
- **作者/组织：** 乘风gg（掘金）
- **日期：** 2026-08-31
- **信源层级：** Tier 2（中文社区一线实践）
- **推荐指数：** ⭐⭐⭐⭐

**一句话摘要：** 把需求到 Bug 修复拆成 8 个 Skill，产出统一落在 `spec/changes/` 目录形成可追溯闭环。

**核心洞察（3-5 条）：**

1. 团队级真痛点不在编码，而在环节交接面：prompt 无 review、产出格式不一、变更范围不可见、经验随人走。
2. 8 个 Skill（product/api/ui/page/test/qa/review/bugfix）有固定依赖顺序，下游消费上游 md 产出，进度写入 `.spec.yaml`。
3. 三条共同设计：Skill 开头必须先读 `CLAUDE.md` 规范；在模糊处设"停下来等人"的决策点而非全自动；末尾维护"现象→原因→处理"的常见坑速查表并随交付回写。
4. `bugfix` 的硬约束"根因说不清不许动手"来自真实翻车；目录约定参考 OpenSpec 的 spec-driven 思路。

**与已知内容的关联：**

- 把 [20] "I Gave Claude Code an AGENTS.md Contract" 的单点契约扩展为多角色、可追踪、可回写的团队工作流。
- 与 [24] A Few Pages of Markdown 的"提交式 AI 配置"实证互相印证；填补中文社区团队级 harness 落地细节缺口。

**值得收录的理由 / 不值得的理由：**
真实企业项目、可复制目录结构与约束设计，非翻译转述，属中文原创一线经验。

---

#### [7]. SoL-Pi: Scaling Auto-Research Loops for Efficient Agent Harnesses

- **类型：** 开源项目（附研究博客）
- **链接：** https://github.com/NVlabs/SoL-Pi （博客：https://nvlabs.github.io/SoL-Pi/）
- **作者/组织：** NVIDIA Labs (NVlabs)
- **日期：** 2026-09-02
- **信源层级：** Tier 2
- **推荐指数：** ⭐⭐⭐⭐

**一句话摘要：** 用可扩展的自动研究循环搜出四个 harness 效率机制，作为 Pi 的可选扩展显著降低 token 成本。

**核心洞察（3-5 条）：**

1. 思路反转：先让 AI 把 harness 本身变高效，再谈扩大 RSI；搜索目标限定"不早停、不跳过验证、不隐藏证据"。
2. 四个机制：Action Fusion（编辑+校验合并为一次工具调用）、ObservationPack（大结果变成可精确分页召回的手柄）、Evidence-Preserving Reducer（长日志压缩为可回溯引用的收据）、Online Context Compact（按经济性与窗口压力触发原生 compaction）。
3. 成本数据：单研究员单问题上，相比原生 Codex/Claude Code 省 $8.75–$13.50/小时，相比 Pi 省 $4.36–$5.71/小时。
4. 不改 Pi 源码、全部 opt-in、原始观察本地保留，强调证据可回溯。

**与已知内容的关联：**

- 与 [06] ECC、[18] EvolveNet、[19] Harness-R1 同属"harness 自演化"路线，但目标从正确率换成 token 效率。
- 补充 [29] compaction、[30] Headlong microharness 缺失的"可复用效率机制"。

**值得收录的理由 / 不值得的理由：**
有可运行代码、公开博客与量化省钱数据，是"自动研究改进 harness"新范式的具体产物。

---

#### [8]. mini-harness

- **类型：** 开源项目
- **链接：** https://github.com/mini-harness/mini-harness
- **作者/组织：** mini-harness 团队
- **日期：** 2026-09-05
- **信源层级：** Tier 3
- **推荐指数：** ⭐⭐⭐⭐

**一句话摘要：** 约 1700 行 Python 的完整教学型 harness：9 个工具、compaction、重试、流式与 TUI，附基准成绩。

**核心洞察（3-5 条）：**

1. 用最小代码量覆盖 harness 全要素：agent loop、Pydantic 类型化工具、上下文压缩、请求重试、会话记忆。
2. 自报基准（DeepSeek V4 Flash）：SWE-bench Verified 80.2%（401/500）、Terminal-Bench 2.1 69.44%（89 题各 5 次取平均，非 pass@5）。
3. 工具用 Pydantic 定义，执行前校验并生成 JSON Schema，便于组合与编排。
4. 单文件 TUI 可读可改，自我定位是"基线"而非产品。

**与已知内容的关联：**

- 把 [29] 的上下文工程与 [22]/imec 的评测讨论落到可读代码。
- 为 [18][19] 的 harness 研究提供低门槛实验底座，填补"可读、可复现的最小 harness 实现"缺口。

**值得收录的理由 / 不值得的理由：**
代码少而全、有基准与复现说明，适合作为自建 harness 与研究起点；stars 少、基准为自报，需注明。

---

#### [9]. HarnessME

- **类型：** 开源项目
- **链接：** https://github.com/Bonhollow/harnessme
- **作者/组织：** Bonhollow
- **日期：** 2026-09-07
- **信源层级：** Tier 3
- **推荐指数：** ⭐⭐⭐

**一句话摘要：** 读取仓库既有结构与约定，生成并维护 AGENTS.md、模块级指南、agent 集成与关键路径人工闸门。

**核心洞察（3-5 条）：**

1. 把"让 agent 读懂仓库"变成可执行契约：说明改动位置、必须保持的不变量、验证命令、何时必须先问人。
2. 基于真实文件与验证命令生成内容，并检测文档漂移，而非套模板。
3. Critical Gate Manager 对高影响路径设置需开发者确认的闸门。
4. 本地 CLI、无托管服务，支持 diff 预览与快照回滚，且不触碰源码。

**与已知内容的关联：**

- 直接延伸 [20] AGENTS.md Contract 与 [24] "A Few Pages of Markdown"。
- 用工具化方式缓解 [31] 指出的 context 特权提升风险（关键路径加闸门），填补"AGENTS.md 自动生成 + 防漂移"的工具缺口。

**值得收录的理由 / 不值得的理由：**
定位精准、日期在窗口内，但项目很新（37 stars），作为工具线索收录。

---

#### [10]. Beyond Prompts: Measuring and Optimizing LLM Tool-Agent Harnesses

- **类型：** 论文
- **链接：** https://arxiv.org/abs/2609.05736
- **作者/组织：** Cen Mia Zhao, Haibo Ruan, Wenjie Chen, Pei-fen Tu, Usman Abbasi, Joel Hesch
- **日期：** 2026-09-04（v2 修订 2026-09-09）
- **信源层级：** Tier 3
- **推荐指数：** ⭐⭐⭐⭐

**一句话摘要：** 提出资源受限下的 harness 选择协议与保守收益指标 RelLift95(B)，在工具边界用 middleware 优化固定模型 agent。

**核心洞察（3-5 条）：**

1. 把 harness 优化建模为"固定模型 + 资源预算"下的搜索：不改模型，只改 prompt 与工具边界 middleware（guarded intercepts，而非重写执行逻辑）。
2. 提出 optimizer-agnostic 评测协议：held-out lift、worst-condition lift、可重复性、成本诊断、RelLift95(B)。
3. 实例化 prompt-only 与 prompt+middleware（含 PRISM 聚类）优化器并报告各项指标。
4. 强调以"预算 B 下的保守收益估计"汇报，避免过拟合。

**与已知内容的关联：**

- 为 [22] FrontierHarness Eval、观察项 Data-eng-bench 的对比提供可复现统计协议。
- 与 [18] EvolveNet / [19] Harness-R1 的"演化"路线互补（选择 vs 演化），填补 harness 优化缺统一评估口径的缺口。

**值得收录的理由 / 不值得的理由：**
给出 harness 优化的形式化设定与保守收益指标，方法论价值高；纯理论、暂无开源实现。

---

```json
{
  "candidates": [
    {
      "title": "The Anatomy of Harness Engineering: How to Evaluate, Iterate, and Guard AI Coding Agents",
      "url": "https://developers.googleblog.com/the-anatomy-of-harness-engineering-how-to-evaluate-iterate-and-guard-ai-coding-agents/",
      "source": "Google Developers Blog",
      "date": "2026-09-09",
      "stars": 5,
      "summary": "用行为评估替代端到端基准，作为 harness 迭代与防回退的护栏，附可复现代码。",
      "insights": [
        "端到端基准分数变动无法定位原因，行为评估断言中间步骤，相当于 harness 的集成测试",
        "harness 开发分两阶段：先 dogfooding，待 agent 能处理自身代码库后再引入 evals",
        "行为断言应做成快速、确定性、本地可跑的 unit 级检查，在改 prompt/换模型时立即暴露回退",
        "评估首要目的是确认没有整体变差，而非庆祝 +2%",
        "给出基于 Antigravity SDK 的示例与开源仓库链接"
      ],
      "reason": "Tier 1 一手工程方法加可复现代码，直击 harness 迭代缺反馈信号的痛点。"
    },
    {
      "title": "Introducing the Agents API",
      "url": "https://openai.com/index/introducing-the-agents-api/",
      "source": "OpenAI",
      "date": "2026-09-10",
      "stars": 5,
      "summary": "把 Codex harness 变成托管服务：一次调用跑云端长任务，含托管沙箱与子代理编排。",
      "insights": [
        "长程 agent 需要 harness 与基础设施两层：上下文/工具/子代理 + 能连跑数天的环境",
        "多代理原语化：multi_agent.enabled 与 max_concurrent_subagents，子代理各自独立上下文",
        "执行环境三选一：OpenAI 托管沙箱、自建基础设施、沙箱合作伙伴",
        "托管沙箱复用 Codex 与 ChatGPT 的隔离底座，可按文件/包/skills/plugins 配置",
        "声称基于开源 foundation 构建持续演进的 Codex harness，保持 API 稳定"
      ],
      "reason": "Tier 1 官方对 managed agent 基础设施的定调，含 harness/沙箱/子代理实质架构。"
    },
    {
      "title": "Organizing Context in a Multi-Agent Harness",
      "url": "https://www.langchain.com/blog/organizing-context-in-a-multi-agent-harness",
      "source": "LangChain Blog",
      "date": "2026-09-08",
      "stars": 5,
      "summary": "deepagents 新增 isolated/fork 上下文模式，让子代理按需继承主管上下文而非一律从零开始。",
      "insights": [
        "默认 isolated 子代理上下文干净，但会重复主管已做的上下文收集造成浪费",
        "fork 模式把主管对话历史整体传给子代理，等价于当前线程的分叉延续并收敛为单条 tool result",
        "复用主管对话可吃到 prompt caching，通常更快更省",
        "isolated 与 fork 的取舍取决于子代理用途（worker/reviewer）",
        "给出 supervisor/worker/reviewer 模式与 deepagents 具体配置"
      ],
      "reason": "Tier 1 官方给出可落地的上下文模式抽象，把隔离与复用变成两个 API 取值。"
    },
    {
      "title": "How well do agents use test/verification techniques?",
      "url": "https://danluu.com/agentic-testing/",
      "source": "Dan Luu",
      "date": "2026-09-09",
      "stars": 5,
      "summary": "30 种测试/验证条件各约 80 次跑 Zstd 实现：几乎没有技术明显胜出，Default 反高于平均。",
      "insights": [
        "只给技术名字，agent 基本不会真正用对：TDD 跑输，SMT 常证错对象后仍写错代码",
        "有效的是把 agent 从默认行为拨开的小 skill，而非教程式技能；codex 推荐的高星 skill 表现不佳",
        "Fuzzing 仅在生成结构化随机输入时（160 次中 10 次）才真正找到 bug",
        "失败多为 idiosyncretic，而非某语言或技术更适合 agent",
        "瓶颈可能是有效测试知识本身不普及，而非模型能力"
      ],
      "reason": "罕见的大规模预注册实验，直指 harness 验证信号设计，结论反直觉。"
    },
    {
      "title": "Does your harness matter more than your model?",
      "url": "https://aistack.imec-int.com/blog/harness-cost",
      "source": "imec aistack",
      "date": "2026-09-01",
      "stars": 4,
      "summary": "3 个 harness × 2 个模型跑 64 个 SWE-Bench Pro 任务：准确率几乎不变，token 账单可翻倍。",
      "insights": [
        "Codex/Claude Code/Pi 解决率均在 44-53%，差异仅 2-3 个任务",
        "同模型下 Claude Code 输入 token 445.8M/480.2M 显著高于 Codex 330.5M/192.1M，却未多解决任务",
        "每个已解决任务成本区间 0.35-0.70 美元，输出 token 直接占用 GPU 时长",
        "doom-loop 与 prefix caching 错误会显著推高账单，需监控遥测"
      ],
      "reason": "独立第三方实测，量化 harness 主要影响成本而非准确率，可直接用于选型。"
    },
    {
      "title": "企业级 AI Coding 的 Harness 工程实战：8 个 Skill 串起全链路",
      "url": "https://juejin.cn/post/7680079424891011124",
      "source": "掘金（乘风gg）",
      "date": "2026-08-31",
      "stars": 4,
      "summary": "把需求到 Bug 修复拆成 8 个 Skill，产出统一落在 spec/changes/ 目录形成可追溯闭环。",
      "insights": [
        "团队级真痛点在环节交接面：prompt 无 review、产出格式不一、变更范围不可见、经验随人走",
        "8 个 Skill 有固定依赖顺序，下游消费上游 md 产出，进度写入 .spec.yaml",
        "三条共同设计：先读 CLAUDE.md 规范、模糊处停下等人、维护常见坑速查表并回写",
        "bugfix 硬约束：根因说不清不许动手，来自真实翻车",
        "目录约定参考 OpenSpec 的 spec-driven 思路"
      ],
      "reason": "真实企业项目、可复制目录结构与约束设计，中文原创一线经验。"
    },
    {
      "title": "SoL-Pi: Scaling Auto-Research Loops for Efficient Agent Harnesses",
      "url": "https://github.com/NVlabs/SoL-Pi",
      "source": "NVIDIA Labs (GitHub)",
      "date": "2026-09-02",
      "stars": 4,
      "summary": "用可扩展自动研究循环搜出四个 harness 效率机制，作为 Pi 可选扩展显著降低 token 成本。",
      "insights": [
        "先让 AI 把 harness 本身变高效，再谈扩大 RSI，搜索不得早停或跳过验证",
        "四机制：Action Fusion、ObservationPack、Evidence-Preserving Reducer、Online Context Compact",
        "相比原生 Codex/Claude Code 省 8.75-13.50 美元/小时，相比 Pi 省 4.36-5.71 美元/小时",
        "不改 Pi 源码、全部 opt-in、原始观察本地保留以保证证据可回溯"
      ],
      "reason": "有代码、公开博客与量化省钱数据，是自动研究改进 harness 新范式的产物。"
    },
    {
      "title": "mini-harness",
      "url": "https://github.com/mini-harness/mini-harness",
      "source": "GitHub",
      "date": "2026-09-05",
      "stars": 4,
      "summary": "约 1700 行 Python 的完整教学型 harness：工具、compaction、重试、TUI，附基准成绩。",
      "insights": [
        "用最小代码量覆盖 harness 全要素：agent loop、类型化工具、压缩、重试、会话记忆",
        "自报基准：DeepSeek V4 Flash 下 SWE-bench Verified 80.2%、Terminal-Bench 2.1 69.44%",
        "工具用 Pydantic 定义，执行前校验并生成 JSON Schema 便于编排",
        "单文件 TUI 可读可改，定位是基线而非产品"
      ],
      "reason": "代码少而全且有基准与复现说明，适合作为自建 harness 与研究起点。"
    },
    {
      "title": "HarnessME",
      "url": "https://github.com/Bonhollow/harnessme",
      "source": "GitHub",
      "date": "2026-09-07",
      "stars": 3,
      "summary": "读取仓库结构与约定，生成并维护 AGENTS.md、模块级指南、agent 集成与关键路径人工闸门。",
      "insights": [
        "把让 agent 读懂仓库变成可执行契约：改动位置、不变量、验证命令、何时先问人",
        "基于真实文件与验证命令生成内容并检测文档漂移，而非套模板",
        "Critical Gate Manager 对高影响路径设置开发者确认闸门",
        "本地 CLI 无托管服务，支持 diff 预览与快照回滚且不碰源码"
      ],
      "reason": "定位精准且在窗口内，但项目很新，作为 AGENTS.md 自动化的工具线索收录。"
    },
    {
      "title": "Beyond Prompts: Measuring and Optimizing LLM Tool-Agent Harnesses",
      "url": "https://arxiv.org/abs/2609.05736",
      "source": "arXiv cs.AI",
      "date": "2026-09-04",
      "stars": 4,
      "summary": "提出资源受限下的 harness 选择协议与保守收益指标 RelLift95(B)，在工具边界用 middleware 优化。",
      "insights": [
        "把 harness 优化建模为固定模型加资源预算下的搜索，只改 prompt 与工具边界 middleware",
        "提出 optimizer-agnostic 协议：held-out lift、worst-condition lift、可重复性、成本诊断",
        "实例化 prompt-only 与 prompt+middleware（含 PRISM 聚类）优化器",
        "以预算 B 下的保守收益估计汇报，避免过拟合"
      ],
      "reason": "给出 harness 优化的形式化设定与保守收益指标，方法论价值高但暂无开源实现。"
    }
  ]
}
```

---

说明：本周还发现若干贴近主题但未入选的线索，供后续跟踪：Nathan Sutton《Nine coding harnesses vs. your laptop》（2026-09-10，9 个 harness 本地模型实测）、《2026 Agent 产业与技术全景图谱》（掘金，2026-09-10）、arXiv《Consort: Spec-First Agent Framework》（2026-09-09）。EP-Harness 一文实为 2026-08-20 发布，已按时间窗排除。