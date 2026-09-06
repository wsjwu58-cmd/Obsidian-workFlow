已通过 Firecrawl search/scrape 完成 2026-08-24 至 2026-09-07 窗口的检索与逐条核实（含 arXiv、GitHub、HN 回溯原始页面）。已对照注入的已知内容去重；共 10 条，含论文 4、文章 4、工具 1、开源项目 1。

---

#### [1]. A Few Pages of Markdown：提交型 AI 配置与编码智能体采纳后的质量代价

- **类型：** 论文
- **链接：** http://arxiv.org/abs/2608.25241
- **作者/组织：** Yegor Denisov-Blanch、Rylan Schaeffer、Sanmi Koyejo 等（arXiv cs.SE）
- **日期：** 2026-08-26
- **信源层级：** Tier 3
- **推荐指数：** ⭐⭐⭐⭐⭐

**一句话摘要：** 441 仓库实证：提交型 AI 配置呈四级成熟度模型，无此类配置的 agent 团队质量代价近翻倍。

**核心洞察（4 条）：**

1. 提出 RAMP（Repository AI Maturity Profile）四级累计成熟度模型：行为规则/编码规范 → 具名 agent 定义 → 多 agent 编排，全部以版本控制内提交的配置文件为准。
2. 配置采纳呈“一次提交、永不再改”特征：73.8% 的配置文件从未被修改，说明团队把规则写入文件后基本交给 agent 自治。
3. 分层重估既有 agent 采纳面板：无论成熟度高低，agent 都带来 28–38% 的提交量增长；但 agent-first 仓库中无配置者认知复杂度增幅 +53% vs 有配置者 +27%，静态告警约 1.7 倍。
4. 作者自认属“假设生成”性质（配置成熟度与工程纪律可能相关），并随文发布 RAMP 作为可复用测量工具。

**与已知内容的关联：**

- 把 AGENTS.md 类实践（已知内容 [20]、Klibsio 观察项）从个案经验升级为 441 仓库的量化研究，首次给出“配置文件作为成熟度代理指标”的证据。
- 填补“agent 配置与代码质量关系”的实证缺口，直接服务 AI-assisted SE 组织影响主题。

**值得收录的理由：** 方法可复现、数据规模大、直接命中 AGENTS.md/agent 治理主线，是窗口内少有的实证类一级素材。

---

#### [2]. SWE-Gate：仅通过功能测试不足以评判软件工程智能体

- **类型：** 论文
- **链接：** http://arxiv.org/abs/2609.04167
- **作者/组织：** Xin He、Yanlin Wang、Mingwei Liu、Jiachi Chen、Hongyu Zhang、Guanbin Li（arXiv cs.SE）
- **日期：** 2026-09-03
- **信源层级：** Tier 3
- **推荐指数：** ⭐⭐⭐⭐⭐

**一句话摘要：** 303 个真实 PR 评审约束实例显示：644 次功能通过中 221 次违反评审约束，功能型评测高估 agent 能力。

**核心洞察（4 条）：**

1. 现有仓库级基准只测补丁是否通过功能测试，忽视真实世界决定补丁能否合入的评审约束（review constraints）。
2. SWE-Gate 从真实 PR 评论中抽取约束并合成 303 个修复实例（75 个 Python 仓库），功能测试与约束测试分离，附不合格补丁与金标准补丁。
3. 同一编码 agent 脚手架 + 4 个 LLM 后端的对照实验显示明显差距：644 个通过功能测试的修复中 221 个不满足评审约束。
4. 结论直指评测设计：应以“评审派生验收约束 + 功能正确性”双门控，否则对真实软件工程能力的估计系统性偏乐观。

**与已知内容的关联：**

- 与已收录的 SWE-Touch（人机共享工作区）、Data-eng-bench（数据原生 harness）、LangSmith Tuned Evaluators 形成评测维度互补：前者测“用户改动”，本篇测“评审者约束”。
- 呼应 Rachel Laycock 的 code review 辩论（见 [6]）：AI 代码评审若只自动化流程而不编码约束，正是 SWE-Gate 量化的失败模式。

**值得收录的理由：** 开源复现包（github.com/DeepSoftwareAnalytics/SWE-Gate）、量化结论清晰，直接改写 coding agent 评测的验收标准讨论。

---

#### [3]. 你的 agent 上下文里有什么？针对 AI Agent Harness 的上下文提权攻击

- **类型：** 论文
- **链接：** http://arxiv.org/abs/2609.01222
- **作者/组织：** Zichuan Li、Jian Cui、Ashley Chen、Xiaojing Liao、Luyi Xing（arXiv）
- **日期：** 2026-09-01
- **信源层级：** Tier 3
- **推荐指数：** ⭐⭐⭐⭐⭐

**一句话摘要：** 首次系统分析 12 个真实 harness 的上下文组装设计，提出 M-CPE/X-CPE 两类上下文提权攻击。

**核心洞察（4 条）：**

1. 厂商 harness 的上下文组装（context assembly）来源与逻辑不透明，是此前未被系统研究的攻击面。
2. 攻击分类 M-CPE：攻击者控制的低权限内容被并入更高权限 message role；X-CPE：攻击内容越过引入它的作用域持续存活。
3. 对 12 个真实 harness（含 Claude Code、Codex）的系统分析显示后果可达完整 agent 接管、RCE、拒绝服务与工具/技能调用被操纵。
4. 含义明确：上下文组装必须被当作与沙箱同级的信任边界来审计，而非仅靠模型层防御。

**与已知内容的关联：**

- 为 Context Engineering 主题引入安全视角：已知 LiveMem、compaction 类工作优化“上下文怎么管”，本篇证明“上下文怎么被污染/越权”同样决定 agent 安全。
- 扩展 harness 研究谱系（Harness-R1/EvolveNet/SHE 之后首个把 harness 上下文管线本身当攻击面的工作）。

**值得收录的理由：** 全新攻击分类 + 12 系统实测，是 harness 工程安全子域的标志性增量，非营销、有实证。

---

#### [4]. Introducing FrontierHarness Eval：同一模型下 9 款 harness 的通过成本相差 17 倍

- **类型：** 工具
- **链接：** https://runta.com/blog/introducing-frontierharness-eval
- **作者/组织：** Shilin Zhu、Shiqi Mei（Runta；数据与任务定义开源：github.com/frontier-harness-eval/eval）
- **日期：** 2026-09-01
- **信源层级：** Tier 2（HN 81 分热帖 2026-09-04）
- **推荐指数：** ⭐⭐⭐⭐⭐

**一句话摘要：** 360 次受控试验对比 12 个 harness 配置：通过率仅差 17 个百分点，单次通过成本却差 17 倍。

**核心洞察（4 条）：**

1. 控制模型（Kimi K3）、任务、运行时一致并冷启动恢复 checkpoint，9 harness/12 配置 × 360 试次：通过率 50.0–66.7%，单次通过成本 $1.05–$18.34。
2. “完成一个任务”与“便宜地完成”是两种能力：Claude Code 与 DSH Creator 同为 63.3% 通过率，前者成本 $18.34 是后者 $3.28 的 5.6 倍。
3. 缓存命中率 ≠ 成本：缓存下 300 轮失败可能仍比短缓存未命中更贵；厂商血缘无明显主场优势（Kimi Code 56.7% 居中游）。
4. 作者自曝局限（Claude Code 结果或含模型/网关交互），HN 社区亦质疑“单模型无主场”假设与 Pi 极简配置的代表性——方法论争议本身就是素材。

**与已知内容的关联：**

- 以数据支持 DeepSeek Harness（观察项）与 Claude Code/Codex 竞品的工程争论，并与 Snowflake data-eng-bench 的“harness×模型”成本数据形成第二组跨 harness 对照。
- 填补“开源可复现 harness 横向评测”工具缺口；其方法论可被复用做 agent harness 选型。

**值得收录的理由：** 一手控制变量实验 + 全量开源数据，是 harness engineering 评测域的硬核增量；社区反驳意见也值得跟踪。

---

#### [5]. Headlong：面向持续自主 agent 的微 harness（Laude / MIT）

- **类型：** 开源项目
- **链接：** https://www.laude.org/updates/headlong-a-microharness-for-persistent-agents
- **作者/组织：** Laude Institute（与 MIT 合作）；仓库 github.com/laude-institute/headlong（1.1k stars）
- **日期：** 2026-08-24
- **信源层级：** Tier 2（HN 125 分热帖 2026-08-26）
- **推荐指数：** ⭐⭐⭐⭐

**一句话摘要：** <1 万行 Bash 的持续自主微 harness：agent 永不入睡、自我调度思考，消息只是观察流。

**核心洞察（4 条）：**

1. 核心差异在“持久代理”：reactive 与 cron 唤醒之外的第三种形态——每次运行结束自调度下一次唤醒，无外部输入也持续思考。
2. 极简实现：Bash 版 RLM（shellm）+ 单一 append-only jsonl 轨迹 + 上下文由 `context` 工具按轨迹组装；工具、记忆、技能全是文件，agent 可自检自改。
3. 上下文压缩采用“指数衰减分辨率”：近期条目原文保留、越老越概要，分层作索引并可回溯原文——直接是 context engineering 的可运行算法。
4. 多用户共享单 agent（无 per-user session），落地教训：未沙箱化时 agent 曾自行停掉自己的服务；默认 Docker 容器逐条执行 bash block；并坦承持久代理目前缺乏有效评测手段。

**与已知内容的关联：**

- 与已收录 LiveMem、Agentic Transaction 观察同属“长会话/持久化”谱系，但给出全新极简 Bash 参考实现，并明确引用 Prime Agent、OpenClaw、Hermes（已知 [09]）为同类。
- 其自曝的“agent 弄坏自己”案例与 [10] 的升级事故、ihavebeenclawed 一类事故档案同向，提示 harness 需要事故反哺。

**值得收录的理由：** 原创设计 + 可运行代码 + 失败教训透明，四个核心主题（harness、context、infra、评测缺口）各有一击。

---

#### [6]. 也许我们不该评审所有代码（Rachel Laycock，Thoughtworks CTO）

- **类型：** 文章
- **链接：** https://martinfowler.com/rachels-ramblings/code-review.html
- **作者/组织：** Rachel Laycock（Thoughtworks / martinfowler.com）
- **日期：** 2026-09-02
- **信源层级：** Tier 1
- **推荐指数：** ⭐⭐⭐⭐

**一句话摘要：** 反驳 DX 的 code review 观：与其让 AI 提速评审仪式，不如把反馈左移、按例外评审。

**核心洞察（4 条）：**

1. 直接回应 Brian Houck（DX）《What are code reviews even for?》并引用其数据：Meta 人均合入行数一年 +106%、PR 中位规模 +64%，逐 PR 人工评审已成新瓶颈。
2. 观点：code review 被塞进了质量门禁/安全检查/架构评审/导师制/知识共享等过多职能，AI 时代应拆解并把反馈左移到结对、设计会、trunk-based、fitness functions。
3. “AI 评审员复制原流程”是自动化仪式而非重估仪式；高风险变更（安全边界、大爆炸半径、团队不熟区域）才应保留人类评审（review by exception）。
4. 承认认知/意图债务是真实问题，但强制 PR 不是有效防御；结论是“工程师要理解系统，而不是理解 diff”。

**与已知内容的关联：**

- 与已观察的 Simon Willison《conceptual integrity and counting lines of code》同属 Tier 1 作者对主流 AI 度量/流程叙事的挑战，互为补充（LOC 度量 vs 评审仪式）。
- 与 [2] SWE-Gate 形成闭环：评审约束若被 AI 自动化流程吸收为验收门禁，正是两篇文章共同指向的落点。

**值得收录的理由：** Tier 1 一手观点 + 有署名辩论对象与数据，AI-assisted SE 流程辩论的高质量入口。

---

#### [7]. 编码智能体的上下文工程（Decoding AI：从零构建 Coding Agent 课程第 4 课）

- **类型：** 文章
- **链接：** https://www.decodingai.com/p/context-engineering-for-coding-agents
- **作者/组织：** Paul Iusztin（Decoding AI Magazine；配套开源课程 decodingai-magazine/building-a-coding-agent-from-scratch-course）
- **日期：** 2026-08-25
- **信源层级：** Tier 2
- **推荐指数：** ⭐⭐⭐⭐

**一句话摘要：** 把“高信噪比上下文”拆成记忆、技能、LSP、压缩四组件，附可运行 Python 实现。

**核心洞察（4 条）：**

1. 以 Terminal-Bench 实验立论：仅换 harness（同模型）即可把 coding agent 从 ~30 名带入前 5——上下文工程是 harness 的核心竞争力。
2. 四组件框架：可持久记忆、技能文件、LSP 诊断即时反馈、会话压缩；作者认为多数“换大模型/换订阅”是治标。
3. 可复现细节：AGENTS.md 写偏好避免重复纠正；退出与 `/clear` 时一次廉价 LLM 调用把会话压成一行带日期 bullet（append-only 日志，200 行/25KB 硬上限）；`compress_memory_file` 合并过期笔记。
4. LSP 诊断作为结构化反馈环在下一轮 edit 前注入，属“让工具纠错而不是让模型猜”的 harness 级工程。

**与已知内容的关联：**

- 与已观察 LiveMem（内存连续性）互补：前者给抽象视角，本篇给 coding harness 内的工程化模式与代码。
- 其“harness 决定排名”论断与 [4] FrontierHarness 的量化结果互相印证（同一模型、不同 harness 差异巨大）。

**值得收录的理由：** 一线实践 + 可复现代码 + 直击 context engineering 核心主题，中文社区尚未覆盖该课视角。

---

#### [8]. 让你的数据为 Agentic AI 做好准备（Thoughtworks，martinfowler.com）

- **类型：** 文章
- **链接：** https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html
- **作者/组织：** Pramod Sadalage、Prem Chandrasekaran（Thoughtworks / martinfowler.com）
- **日期：** 2026-08-27
- **信源层级：** Tier 1
- **推荐指数：** ⭐⭐⭐⭐

**一句话摘要：** 为无“怀疑本能”的 agent 重构数据栈：可信基础层 + 语义上下文层 + 受控访问层。

**核心洞察（4 条）：**

1. 起点洞察：三十年数据系统服务的是自带判断力的人类分析师，agent “把每个值当真相”，因此 AI-ready 需要信任、语义、访问三层重建。
2. 可操作模式：schema-as-law 数据契约、数据隔离（quarantine）模式、面向 agent 的 medallion、置信度阈值路由、metrics-as-code。
3. “上下文层”直接回应 agent 不懂“revenue 指什么”：以度量定义 + 语义层 + 知识图谱教给 agent 含义——正是 context engineering 的企业数据版。
4. 治理与访问：agentic lineage 审计、分阶段自治、委托授权与 JIT 凭证；警告“naive API→MCP 转换”是反模式，“检索文本只提供信息、绝不充当门禁”。

**与已知内容的关联：**

- 扩展已观察 Snowflake data-eng-bench 与已收录 MarkItDown [08] 的“数据×agent”方向，把数据准备上升为第一方工程框架（context layer 概念与 [7] 的上下文工程互为镜像）。
- “分层自治 + 可审计 lineage”与已知 SHE/Agentic Transaction 的可靠性诉求在数据侧汇合。

**值得收录的理由：** Tier 1 长文、署名双作者、模式密度高，是窗口内企业 agent 落地少见的系统性参考。

---

#### [9]. AgentRoom：CRDT 共享工作区中的并发多智能体编程

- **类型：** 论文
- **链接：** http://arxiv.org/abs/2608.23740
- **作者/组织：** Seonglae Cho、Donghyun Lee（arXiv）
- **日期：** 2026-08-24
- **信源层级：** Tier 3
- **推荐指数：** ⭐⭐⭐⭐

**一句话摘要：** 用 CRDT 合并文件系统 + MCP claim/broadcast 让多个 coding agent 真正并发改同一仓库。

**核心洞察（4 条）：**

1. 问题定位：现有多 agent 编码要么串行阶段交接、要么无协调并行采样，单个 agent 遇难任务过半以“单文件 stub 就退出”。
2. 方案：实时协同编辑协议，运行时层以 MCP 工具暴露文件级 claim/状态/广播，跑在 CRDT 合并的共享文件系统上。
3. 实验：5 个前沿 coding-CLI 模型 × 4 个后端任务（Python DevBench、Rust+axum）；2-agent AgentRoom 比 Solo 放弃更少任务、run-to-run 方差更低。
4. 结论反直觉：收益来自“协调”本身而非并行或 CRDT 合并——对多 agent 编排设计（何时该并发、何时该接管）给出可测证据。

**与已知内容的关联：**

- 已知多 agent 素材多为厂商架构论述（Deep Agents vs LangChain/LangGraph、Anthropic multiagent），本篇提供开放协议实验与量化对比，补“共享工作区并发协调”空白。
- 与 SWE-Touch（人机共享代码区）互补：SWE-Touch 测人机触碰，AgentRoom 测 agent-agent 触碰。

**值得收录的理由：** 开源可实现协议 + 控制变量实验，多智能体协作方向少见的机制级工作。

---

#### [10]. 憋了 7 周没动静，OpenClaw 2.0 带着 16000 个 PR 杀回来了（掘金原创分析）

- **类型：** 文章
- **链接：** https://juejin.cn/post/7680352383386107940
- **作者/组织：** 一点一木（稀土掘金）
- **日期：** 2026-09-01
- **信源层级：** Tier 2（中文社区）
- **推荐指数：** ⭐⭐⭐

**一句话摘要：** 掘金长文拆解 OpenClaw 2.0：零配置上手指引、Session Rail、多用户角色、Swarm 模式与升级翻车。

**核心洞察（4 条）：**

1. 版本事实：v2026.8.1（8 月 31 日发布），933 贡献者/569 位新人，一次合并 1.6 万+ PR；本地栈从 node-llama-cpp 换托管 llama-server，默认上下文 64K。
2. 产品层：浏览器端从管理后台变“驾驶舱”（Session Rail 实时任务/计划/PR 状态、`/btw` 伴随线程不打断主任务、agent 自生成 widget）；多用户 Gateway + Team Operator Roles（会话三档可见性、按会话强制沙箱、共享只写凭证库、出站绑死声明主机）。
3. 机制层：实验性 Swarm 模式让主 agent 拆解、多个子 agent 并行干活、进度卡持久化刷新不丢——小型 agent 团队工作流。
4. 作者保留批判：官方引 27 万次攻击众测（Opus 4.5 注入成功率 0.5%）但对自适应人类攻击者仍 >80%；升级把会话/转录迁到 SQLite 属破坏性变更、出现 split-brain installs，官方建议“用本地 coding harness 修 agent 的升级故障”被讥为赛博套娃；并回应 HN 最高赞“谁还在用 OpenClaw”。

**与已知内容的关联：**

- OpenClaw 属已知 ECC（agent harness OS）同类，且 Headlong [5] 亦点名其为同赛道；本窗口的 2.0 迭代与社区反应是中文社区一手增量。
- 会话三档可见性/沙箱/凭证管理、Swarm 子 agent 编排，正面呼应 Agent Infrastructure 主题；其“agent 修 agent 升级失败”案例补充 [5]/[3] 的自伤与安全讨论。

**值得收录的理由：** 窗口内中文原创深度分析（非翻译转述），含一手数据与对英文社区（HN/Reddit）的独立解读，满足中文社区重点发现要求。

---

```json
{
  "candidates": [
    {
      "title": "A Few Pages of Markdown: Committed AI Configuration and Lower Quality Cost after Coding-Agent Adoption",
      "url": "http://arxiv.org/abs/2608.25241",
      "source": "arXiv cs.SE (Yegor Denisov-Blanch 等)",
      "date": "2026-08-26",
      "stars": 5,
      "summary": "441 仓库实证：提交型 AI 配置呈四级成熟度模型，无配置的 agent-first 团队认知复杂度增幅近翻倍。",
      "insights": [
        "提出 RAMP 四级累计成熟度模型：规则→具名 agent→多 agent 编排，全部以版本控制内配置为准",
        "73.8% 的 AI 配置文件一次提交后从未修改，呈 set-and-forget 特征",
        "agent 使提交量增 28–38%，但无配置者认知复杂度 +53% vs 有配置者 +27%，静态告警约 1.7 倍",
        "作者声明为假设生成性质，并发布 RAMP 可复用测量工具"
      ],
      "reason": "把 AGENTS.md 实践从个案升级为 441 仓库量化研究，直接填补 AI 配置与代码质量关系的实证缺口"
    },
    {
      "title": "SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents",
      "url": "http://arxiv.org/abs/2609.04167",
      "source": "arXiv cs.SE (Xin He, Yanlin Wang 等)",
      "date": "2026-09-03",
      "stars": 5,
      "summary": "303 个真实评审约束实例证明：644 次功能测试通过中 221 次违规，功能型评测高估 coding agent。",
      "insights": [
        "从真实 PR 评审评论派生约束，303 实例覆盖 75 个 Python 仓库，功能与约束测试分离",
        "同脚手架 + 4 个 LLM 后端：功能通过与完整验收规格间存在约 34% 的系统性差距",
        "揭示补丁验收需以评审派生约束 + 功能正确性双门控",
        "代码、数据与实验结果全量开源（github.com/DeepSoftwareAnalytics/SWE-Gate）"
      ],
      "reason": "与 SWE-Touch、Data-eng-bench 互补的新评测维度，且与 code review 辩论直接互证"
    },
    {
      "title": "What's in Your Agent's Context? Context Privilege Escalation Attacks against AI Agent Harness",
      "url": "http://arxiv.org/abs/2609.01222",
      "source": "arXiv (Zichuan Li, Luyi Xing 等)",
      "date": "2026-09-01",
      "stars": 5,
      "summary": "首次系统分析 12 个真实 harness 的上下文组装设计，提出 M-CPE/X-CPE 两类上下文提权攻击。",
      "insights": [
        "把不透明的上下文组装（context assembly）定义为独立攻击面",
        "攻击分类：M-CPE 低权限内容并入高权限 message role；X-CPE 攻击内容跨作用域持续存活",
        "对含 Claude Code、Codex 在内的 12 个 harness 实测可达完整接管/RCE/DoS/工具调用操纵",
        "结论：上下文组装须按信任边界审计，模型层防御不足以保证安全"
      ],
      "reason": "为 context engineering 引入此前缺失的安全攻击面视角，含 12 系统实测，原创性强"
    },
    {
      "title": "Introducing FrontierHarness Eval: 9 harnesses, same model, cost per pass varies 17x",
      "url": "https://runta.com/blog/introducing-frontierharness-eval",
      "source": "Runta (Shilin Zhu, Shiqi Mei)；HN 81 分",
      "date": "2026-09-01",
      "stars": 5,
      "summary": "360 次冷启动受控试验：通过率仅差 17 个百分点，单次通过成本却差 17 倍（$1.05–$18.34）。",
      "insights": [
        "同模型(Kimi K3)+冷 checkpoint：Claude Code 与 DSH Creator 同为 63.3%，成本却差 5.6 倍",
        "缓存命中率不等于成本：缓存下长失败轨迹仍可能更贵",
        "厂商血缘无主场优势：Kimi Code 56.7% 仅居中游",
        "作者自曝模型/网关交互局限，HN 亦质疑单模型与 Pi 极简配置代表性，方法论争议本身有价值"
      ],
      "reason": "首个开源可复现的跨 harness 成本×通过率评测（含数据与任务），直接支撑 harness 选型与工程论点"
    },
    {
      "title": "Headlong: a microharness for persistent agents (Laude/MIT)",
      "url": "https://www.laude.org/updates/headlong-a-microharness-for-persistent-agents",
      "source": "Laude Institute；github.com/laude-institute/headlong（1.1k stars）",
      "date": "2026-08-24",
      "stars": 4,
      "summary": "<1 万行 Bash 的持续自主微 harness：agent 永不入睡、自我调度思考，消息只是观察流。",
      "insights": [
        "持久代理形态：每次运行自调度下次唤醒，无外部输入也持续思考",
        "单一 append-only jsonl 轨迹 + Bash 版 RLM，agent 可自检自改工具/记忆/技能文件",
        "压缩算法采用指数衰减分辨率：近期原文、远期摘要、分层索引可回溯原文",
        "落地教训：未沙箱化 agent 曾自行停服；默认 Docker 容器执行，且持久代理目前缺乏有效评测手段"
      ],
      "reason": "可运行参考实现 + 透明失败教训，同时命中 harness/context/infra/评测四主题且与已知内容无重复"
    },
    {
      "title": "Maybe We Shouldn't Be Reviewing All This Code",
      "url": "https://martinfowler.com/rachels-ramblings/code-review.html",
      "source": "Rachel Laycock, martinfowler.com",
      "date": "2026-09-02",
      "stars": 4,
      "summary": "反驳 DX 的 code review 论：与其用 AI 提速评审仪式，不如把反馈左移并改为按例外评审。",
      "insights": [
        "引用数据：Meta 人均合入行数一年 +106%，PR 中位规模 +64%，逐 PR 评审已成瓶颈",
        "code review 被塞入过多职能，应拆解并左移到结对/设计会/fitness functions 等更早环节",
        "AI 复制评审流程是自动化仪式而非重估仪式；只有高风险变更值得人类评审",
        "承认认知/意图债务真实，但强制 PR 不是防御；结论：理解系统而非理解 diff"
      ],
      "reason": "Tier 1 作者对主流流程的原创反驳，有明确辩论对象与数据，直接服务 AI 代码评审主题"
    },
    {
      "title": "Context Engineering for Coding Agents (Building a Coding Agent From Scratch, Lesson 4)",
      "url": "https://www.decodingai.com/p/context-engineering-for-coding-agents",
      "source": "Paul Iusztin, Decoding AI Magazine",
      "date": "2026-08-25",
      "stars": 4,
      "summary": "把高信噪比上下文拆成记忆、技能、LSP、压缩四组件，配套开源 Python 课程实现。",
      "insights": [
        "以 Terminal-Bench 立论：仅换 harness（同模型）即可从 ~30 名进前 5",
        "可复现细节：AGENTS.md 持久偏好、/clear 时压成一行日期 bullet、记忆文件 200 行/25KB 上限",
        "LSP 诊断作为结构化反馈在下一轮 edit 前注入，属 harness 级纠错而非模型自猜",
        "压缩策略：append-only 日志 + compress_memory_file 合并过期笔记"
      ],
      "reason": "一线实践+可复现代码直击 context engineering 主题，与 FrontierHarness 量化结论互相印证"
    },
    {
      "title": "Making Your Data Ready for Agentic AI",
      "url": "https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html",
      "source": "Pramod Sadalage & Prem Chandrasekaran, martinfowler.com (Thoughtworks)",
      "date": "2026-08-27",
      "stars": 4,
      "summary": "为无怀疑本能的 agent 重建数据栈：可信数据层 + 语义上下文层 + 受控访问层三层体系。",
      "insights": [
        "schema-as-law 数据契约、隔离/检疫模式、置信度阈值路由、metrics-as-code 等可操作模式",
        "上下文层教 agent 理解业务语义（revenue 指什么），是 context engineering 的企业数据版",
        "agentic lineage、分阶段自治、JIT 凭证支撑可审计的自主执行",
        "反对 naive API→MCP 转换；检索文本只提供信息、绝不充当门禁"
      ],
      "reason": "Tier 1 双作者长文，把 agent 数据准备上升为第一方框架，扩展已知数据×agent 方向"
    },
    {
      "title": "AgentRoom: Concurrent Multi-Agent Coding in a CRDT-Backed Shared Workspace",
      "url": "http://arxiv.org/abs/2608.23740",
      "source": "arXiv (Seonglae Cho, Donghyun Lee)",
      "date": "2026-08-24",
      "stars": 4,
      "summary": "CRDT 合并共享文件系统 + MCP 文件级 claim/广播，让多个 coding agent 真并发改同一仓库。",
      "insights": [
        "定位问题：串行交接或无协调并行皆低效，单 agent 过半以 stub-and-exit 放弃难任务",
        "以 MCP 工具暴露文件级 claim/状态/广播，运行于 CRDT 合并文件系统",
        "5 模型×4 任务实验：2-agent AgentRoom 放弃更少且方差更小",
        "结论：收益来自协调机制而非并行或 CRDT 合并本身"
      ],
      "reason": "多 agent 协作方向少见的机制级开放实验，与 SWE-Touch 构成 agent-agent vs 人机触碰互补"
    },
    {
      "title": "憋了 7 周没动静，OpenClaw 2.0 带着 16000 个 PR 杀回来了",
      "url": "https://juejin.cn/post/7680352383386107940",
      "source": "一点一木, 稀土掘金",
      "date": "2026-09-01",
      "stars": 3,
      "summary": "掘金长文拆解 OpenClaw 2.0：零配置、Session Rail、团队角色、Swarm 模式与升级翻车复盘。",
      "insights": [
        "v2026.8.1：933 贡献者（569 新人）一次合并 1.6 万+ PR，默认上下文升至 64K",
        "驾驶舱式 UI：Session Rail 实时进度、/btw 伴随线程、agent 自生成 widget",
        "多用户 Gateway+Team Operator Roles：会话三档可见、按会话沙箱、凭证只写、出站绑死",
        "批判性细节：升级迁 SQLite 属破坏性变更、split-brain 安装、自适应人类注入 >80%、回应 HN 唱衰"
      ],
      "reason": "窗口内中文社区原创深度分析，覆盖会话管理/沙箱/多 agent 编排并含一手数据，非英文转述"
    }
  ]
}
```

Reading prompt from stdin...
OpenAI Codex v0.147.0
--------
workdir: /root/note-worker
model: deepseek-v4-flash
provider: deepseek
approval: never
sandbox: workspace-write [workdir, /tmp, $TMPDIR] (network access enabled)
reasoning effort: none
reasoning summaries: none
session id: 01a07905-2cdc-7231-b319-fbcd341a0a03
--------
user
# 技术情报搜索（Prompt A）

> 运行器：服务器 codex，由 `research.py` 第一段调用。只负责搜索素材，不做三档分流。

你是一个技术情报分析师。请对以下领域进行深度网络搜索，找出过去 2 周内（2026-08-24 至 2026-09-07）发布的高价值内容。

## 搜索领域

核心主题：

1. Harness Engineering — AI 编码智能体的约束、引导、反馈系统设计
2. Context Engineering — 上下文窗口管理、compaction、渐进式披露
3. AI Coding Agents — 编码智能体的架构、编排、评估
4. Agent Infrastructure — 沙箱、会话管理、多智能体协作
5. AI-assisted Software Engineering — AI 辅助开发的效率、流程、组织影响

相关关键词（中英文）：

- harness engineering, agent harness, coding agent, AI coding
- context engineering, context window, compaction, progressive disclosure
- AGENTS.md, CLAUDE.md, agent readability, agent-first
- managed agents, meta-harness, multi-agent orchestration
- AI code review, mutation testing, structural testing, fitness functions
- vibe coding, AI-native development, agentic workflow
- 智能体工程, AI 编程, 上下文工程, 护栏工程

## 搜索范围

必须覆盖的信源（按优先级）：

**Tier 1 — 高权重（模型厂商 + 顶级技术博客）：**

- Anthropic Engineering Blog (anthropic.com/engineering)
- OpenAI Blog (openai.com)
- Google DeepMind / Google AI Blog
- Martin Fowler (martinfowler.com)
- Mitchell Hashimoto (mitchellh.com)
- LangChain Blog (blog.langchain.com)
- Simon Willison (simonwillison.net)

**Tier 2 — 中权重（社区 + 行业）：**

- Hacker News（前 100 讨论）
- GitHub Trending（相关仓库）
- X/Twitter 技术社区（#harness-engineering, #ai-coding, #context-engineering）
- Dev.to、Medium 技术专栏
- HumanLayer、Cursor、Windsurf、Codex 相关博客
- 中文社区：少数派、掘金、知乎专栏

**Tier 3 — 低权重但可能有惊喜：**

- arXiv (cs.SE, cs.AI 交叉)
- 个人技术博客
- YouTube 技术频道
- Reddit (r/LocalLLaMA, r/ChatGPT, r/programming)

## 我们已知的内容（用于去重和关联）

> 本节是 Prompt 的去重权威，由运行时注入当前知识库中与 Agent 主题相关的文章、观察项和已跟踪内容；搜索器无法访问 `references/articles.md`，因此本段必须自包含。
>
> 维护纪律：当 `references/articles.md` 新增或删除条目时，同一次提交中必须同步更新注入结果。搜索结果不得重复下面已有内容；如有深度回应、反驳或明显增量，必须明确写出关联和新增价值。

### 当前知识库 Agent 相关编号文章（references/articles.md）
（以下内容由当前索引实时生成；包含已收录、已淘汰和已关联的归属信息。）
- [01] arxiv — When Does On-Policy Interaction Help? | http://arxiv.org/abs/2607.29617v1 | 2026-08-03 | 已收录 | 归属：—
- [02] AgentHPOBench — LLM Agents as Sequential Hyperparameter Optimizers | http://arxiv.org/abs/2607.29626v1 | 2026-08-03 | 已收录 | 归属：—
- [03] ExtractBench — Schema-Guided Enterprise Document Extraction | http://arxiv.org/abs/2607.29677v1 | 2026-08-03 | 已收录 | 归属：—
- [04] DungeonBench — Rules-Rich Tactical Reasoning | http://arxiv.org/abs/2607.29577v1 | 2026-08-03 | 已收录 | 归属：—
- [05] MOT-SR — Multi-Objective Scientific Equation Discovery | http://arxiv.org/abs/2607.29561v1 | 2026-08-03 | 已收录 | 归属：—
- [06] ECC — agent harness 操作系统 | https://github.com/affaan-m/ECC | 2026-08-03 | 已收录 | 归属：—
- [07] n8n — AI 原生工作流自动化平台 | https://github.com/n8n-io/n8n | 2026-08-03 | 已收录 | 归属：—
- [08] MarkItDown — 文件/文档转 Markdown | https://github.com/microsoft/markitdown | 2026-08-03 | 已收录 | 归属：—
- [09] Hermes-Agent — the agent that grows with you | https://github.com/NousResearch/hermes-agent | 2026-08-03 | 已收录 | 归属：—
- [12] Prevent cognitive debt by manually retyping LLM-generated code | https://ankursethi.com/blog/prevent-cognitive-debt-by-manually-retyping-llm-generated-code/ | 2026-08-03 | 已淘汰 | 归属：—
- [13] Qwen3.8-Max: A New Bar for Coding and Cowork | https://qwen.ai/blog?id=qwen3.8 | 2026-08-03 | 已淘汰 | 归属：—
- [14] MCP 官方文档：Model Context Protocol 介绍 | https://modelcontextprotocol.io/introduction | 2026-08-09 | 已收录 | 归属：—
- [15] Rust 2025 官方博客：Rust 1.85 版本说明（Move 语义 / Borrow Checker 演进） | https://blog.rust-lang.org/2025/02/20/Rust-1.85.0.html | 2025-02-20（采集 2026-08-09） | 已收录 | 归属：—
- [16] Meta launches Muse Code for complex software work with persistent AI agents | https://www.infoworld.com/article/4206084/meta-launches-muse-code-for-complex-software-work-with-persistent-ai-agents.html | 2026-08-09 | 已收录 | 归属：—
- [18] EvolveNet: Collaborative Harness Evolution for Agent Self-Improvement | https://arxiv.org/abs/2608.04968 | 2026-08-09 | 已收录 | 归属：—
- [19] Harness-R1: Learning to Edit Executable Runtime Harnesses from Agent Failure Trajectories | https://arxiv.org/abs/2608.02276 | 2026-08-09 | 已收录 | 归属：—
- [20] I Gave Claude Code an AGENTS.md Contract and Stopped Babysitting It | https://dev.to/daymondhyper/i-gave-claude-code-an-agentsmd-contract-and-stopped-babysitting-it-53m | 2026-08-09 | 已收录 | 归属：—

### 当前知识库 Agent 相关观察项
- Klibs.io Grows to 4200+ KMP Projects With Smarter Discovery and New AI Integrations | https://blog.jetbrains.com/kotlin/2026/08/klibsio-grows-to-4200-kmp-projects-with-smarter-discovery-and-new-ai-integrations/ | JetBrains Kotlin 博客 | 2026-08-17 | JetBrains 官方把 KMP 生态目录做成 agent 可调用工具，含评测数据与 AGENTS.md 实践，双领域交集标杆。
- Conceptual integrity and counting lines of code | https://simonwillison.net/2026/Aug/19/conceptual-integrity-and-counting-lines-of-code/ | Simon Willison 博客 | 2026-08-19 | Tier 1 作者原创观点，挑战主流 LOC 无意义论，对 agent 工程管理/评测有启发。
- Introducing LangSmith Tuned Evaluators, starting with Perceived Error | https://www.langchain.com/blog/introducing-langsmith-tuned-evaluators-starting-with-perceived-error | LangChain 官方博客 | 2026-08-18 | 官方评测产品但技术实质充分（后训练法官+82% 成本数据+接入流程），对 agent 评测域有参考价值。
- Agentic Transaction: Towards ACID-Compliant Agent Systems | https://arxiv.org/abs/2608.13900 | arXiv cs.DB/cs.AI | 2026-08-14 | 原创理论框架+可运行系统，是 agent 可靠执行方向少见的系统性工作。
- The Devil Is in the Interface: Evaluating How Tool Architecture Shapes Coding Agent Behavior | https://arxiv.org/abs/2608.11386 | arXiv cs.SE | 2026-08-11 | 大样本受控实验+量化结论，为 harness/工具平台设计提供可复现证据。
- DeepSeek Harness 开发者预览：一切皆插件 | https://news.ycombinator.com/item?id=49285244 | DeepSeek 官方（Hacker News） | 2026-08-13 | 开源 agent harness 标杆事件，插件化架构与可追踪事件流直接回应 harness/编排主题，官方一级内容。
- LiveMem: Maintaining Memory State Continuity in Long-Running LLM Inference | https://arxiv.org/abs/2608.02515 | arXiv cs.CL | 2026-08-03 | 为 agent 长会话记忆与上下文管理提供新抽象视角
- Everything we launched during Agents Week | https://blog.cloudflare.com/agents-week-review-august-2026/ | Cloudflare | 2026-08-10 | 云厂商对 agent 运行时与生命周期的一次系统性落子，平台趋势观察
- IntelliJ IDEA Goes LSP: Java and Kotlin Intelligence Comes to VS Code, Cursor, and Agentic Flows | https://blog.jetbrains.com/idea/2026/08/intellij-idea-goes-lsp/ | JetBrains | 2026-08-04 | Kotlin 工具链×agent 工作流交叉的一手官方进展
- Deep Agents vs LangChain vs LangGraph | https://www.langchain.com/blog/deep-agents-vs-langchain-vs-langgraph | LangChain | 2026-08-06 | 官方对 agent 栈分层与 harness 定义的权威界定，指导选型
- SHE: Trajectory-driven Safety Harness Evolution for LLM Agents | https://arxiv.org/abs/2608.09885 | arXiv cs.AI | 2026-08-10 | 首个可演化安全 harness 系统化框架，有数据与复现链接
- SWE-Touch: Benchmarking Coding Agents When Users Touch the Code | https://arxiv.org/abs/2608.02499 | arXiv cs.SE | 2026-08-03 | 填补人机协作共享工作区评测盲区，有数据与开源实现，挑战单干基准范式
- DeepSeek Harness developer preview: Everything is a plugin | https://deepseek.com/harness/en/ | DeepSeek | 2026-08-14 | 开源 harness 平台级发布，Claude Code 直接竞品，HN 732 分高热
- Auto mode is now the default in Claude Code for Pro, Max, and Team plans | https://claude.com/blog/auto-mode-default-in-claude-code | Anthropic | 2026-08-07 | Tier 1 官方一手安全数据，直接塑造 agent 权限与安全架构设计
- New release of LLM adds support for reasoning traces, OpenAI Responses, server-side tools, and smarter logging | https://simonwillison.net/2026/Aug/4/new-release-of-llm/ | Simon Willison (simonwillison.net) | 2026-08-04 | Tier1作者对LLM工具平台的深度工程复盘，含可复现代码，覆盖推理轨迹、服务端工具与日志架构。
- Introducing Data-eng-bench: Why You Need "Data-Native" Harnesses for Data Engineering | https://www.snowflake.com/en/blog/engineering/data-eng-bench-data-engineering-agent-benchmark/ | Snowflake AI Research (Snowflake Engineering Blog) | 2026-08-06 | 首个仓库级dbt agent评测（103任务）并开源，harness×模型双变量质量/成本数据直接服务agent评测与选型。

请重点发现：

- 上述未覆盖的新作者、新视角、新组织
- 对上述文章的深度回应或反驳（不是简单转述）
- 与上述项目互补或竞争的新工具、harness、框架
- 中文社区针对上述材料的原创分析（少数派、掘金、知乎专栏等）

## 强制搜索与真实性要求

- 必须使用 Firecrawl 搜索真实网页：优先调用已配置的 Firecrawl MCP `search`；若当前会话无 MCP，则使用本机 `firecrawl search` CLI。
- 禁止凭记忆编造 URL、标题、作者或日期；每条链接必须来自 Firecrawl 返回结果。
- 必要时对候选 URL 使用 Firecrawl `scrape` 核对正文、发布日期、作者和技术细节。
- 只保留发布日期在 `2026-08-24` 至 `2026-09-07`（含边界）的内容；无法核实发布日期的内容不进入推荐清单。
- Hacker News、GitHub Trending、社交媒体可作为发现入口，但尽量回溯到原始文章、仓库、论文或演讲页面作为链接。
- 不能为了凑数量降低质量；没有原创技术内容、数据、代码、实验或一线实践细节的内容直接排除。

## 输出格式

请按以下格式输出，每条内容一个条目：

---

#### [编号]. {标题}

- **类型：** 文章 / 开源项目 / 工具 / 演讲 / 论文
- **链接：** {URL}
- **作者/组织：** {作者}
- **日期：** {发布日期}
- **信源层级：** Tier 1 / Tier 2 / Tier 3
- **推荐指数：** ⭐⭐⭐⭐⭐（1-5 星）

**一句话摘要：** {50 字以内}

**核心洞察（3-5 条）：**

1. ...
2. ...
3. ...

**与已知内容的关联：**

- 支持、挑战或扩展了哪篇已有文章的观点
- 填补了哪个已知缺口

**值得收录的理由 / 不值得的理由：**
{判断}

## 质量过滤标准

**必须满足（全部）：**

- 有实质性的技术内容（不是纯营销或产品公告）
- 有原创洞察或数据（不是对已有文章的简单转述）
- 来源可信（有署名，有技术背景）

**加分项（满足越多越好）：**

- 有实际数据或实验结果
- 有代码示例或可复现的方案
- 挑战了主流观点
- 来自一线实践者（不是纯理论）
- 有中文社区尚未覆盖的视角

**排除：**

- 纯产品发布或营销内容
- 对已有文章的简单翻译或摘要（没有新观点）
- 过于初级的入门教程
- 与 harness engineering 只有表面关联

## 输出数量

- 文章类：推荐 5-10 篇，按推荐指数排序
- 开源项目类：推荐 3-5 个
- 其他（工具 / 演讲 / 论文）：如有高质量内容，不限数量
- 总条目数最多 `10` 条；不足时宁缺毋滥

## 文末机器可读 JSON

在 Markdown 结果之后追加一个 JSON 对象，供 `research.py` 解析。JSON 中每个候选必须包含 `title`、`url`、`source`、`date`、`stars`、`summary`、`insights`、`reason` 字段；`insights` 为 3-5 个字符串的数组。

```json
{
  "candidates": [
    {
      "title": "...",
      "url": "...",
      "source": "...",
      "date": "YYYY-MM-DD",
      "stars": 4,
      "summary": "50字内",
      "insights": ["...", "...", "..."],
      "reason": "一句话"
    }
  ]
}
```

本阶段只负责搜索和输出候选，不做 `index` / `translate` / `observe` 分流；分流由 Prompt B 完成。

warning: Codex could not find bubblewrap on PATH. Install bubblewrap with your OS package manager. See the sandbox prerequisites: https://developers.openai.com/codex/concepts/sandboxing#prerequisites. Codex will use the bundled bubblewrap in the meantime.
warning: Model metadata for `deepseek-v4-flash` not found. Defaulting to fallback metadata; this can degrade performance and cause issues.
exec
/bin/bash -lc 'pwd && ls -la && echo "---" && find . -maxdepth 2 -name "AGENTS.md" -o -maxdepth 2 -name "*.md" | head -50' in /root/note-worker
 succeeded in 0ms:
/root/note-worker
total 100
drwxr-xr-x 19 root root  4096 Sep  7 07:19 .
dr-xr-x--- 14 root root  4096 Sep  7 01:53 ..
dr-xr-xr-x  2 root root    40 Sep  7 07:19 .agents
dr-xr-xr-x  2 root root    40 Sep  7 07:19 .codex
drwxr-xr-x  2 root root  4096 Aug 24 06:19 .firecrawl
drwxr-xr-x  8 root root  4096 Sep  7 07:19 .git
drwxr-xr-x  2 root root  4096 Aug  9 13:37 .githooks
drwxr-xr-x  3 root root  4096 Aug  9 13:37 .github
-rw-r--r--  1 root root   738 Aug  9 17:25 .gitignore
drwxr-xr-x  3 root root  4096 Aug 24 06:10 .obsidian
-rw-r--r--  1 root root  1066 Aug  9 13:37 LICENSE
-rw-r--r--  1 root root  5983 Aug 17 06:09 README.md
-rw-r--r--  1 root root 15434 Aug 17 06:09 agents.md
drwxr-xr-x  2 root root  4096 Aug  9 13:37 assets
drwxr-xr-x  7 root root  4096 Sep  7 07:19 candidates
drwxr-xr-x  3 root root  4096 Aug  9 17:25 docs
drwxr-xr-x  5 root root  4096 Sep  7 07:19 expand
drwxr-xr-x  3 root root  4096 Sep  7 07:19 prompts
drwxr-xr-x  2 root root  4096 Sep  7 07:19 references
drwxr-xr-x  3 root root  4096 Sep  7 07:19 scripts
drwxr-xr-x  2 root root  4096 Aug  9 13:37 templates
drwxr-xr-x 13 root root  4096 Aug 24 06:10 wiki
drwxr-xr-x  2 root root  4096 Aug 24 06:10 working
---
./.firecrawl/dart.dev-blog-announcing-dart-3-13.md
./.firecrawl/arxiv.org-abs-2607.19336.md
./.firecrawl/developer.android.com-blog-posts-what-s-new-in-the-jetpack-compose-august-26-release.md
./.firecrawl/primeintellect.ai-blog-prime-agent.md
./.firecrawl/blog.jetbrains.com-kotlin-2026-08-kodees-kotlin-roundup-birthday-wishes-shipaton-2026-and-the-new-kotlin-ai-benchmark.md
./.firecrawl/infoq.com-news-2026-08-deep-seek-harness.md
./.firecrawl/jetc.dev-issues-327.html.md
./.firecrawl/allaboutcoding.ghinda.com-a-week-of-using-codex-more-than-claude.md
./.firecrawl/blog.jetbrains.com-kotlin-2026-08-klibsio-grows-to-4200-kmp-projects-with-smarter-discovery-and-new-ai.md
./.firecrawl/kotlinlang.org-docs-whatsnew-eap.html.md
./.firecrawl/techcrunch.com-2026-08-09-anthropic-is-turning-claude-codes-auto-mode-on-by-default.md
./.firecrawl/langchain.com-blog-introducing-langsmith-tuned-evaluators-starting-with-perceived-error.md
./.firecrawl/arxiv.org-abs-2608.02499.md
./.firecrawl/arxiv.org-abs-2608.13900v1.md
./.firecrawl/arxiv.org-abs-2608.09885.md
./.firecrawl/developers.googleblog.com-en-supercharge-your-ai-agents-adk-integrations-ecosystem.md
./.firecrawl/anthropic.com-news-investigating-incidents-cybersecurity-evals.md
./.firecrawl/code.claude.com-docs-en-whats-new-2026-w34.md
./.firecrawl/kotlinlang.org-docs-multiplatform-whats-new-compose-112.html.md
./.firecrawl/arxiv.org-abs-2608.11386v1.md
./.firecrawl/langchain.com-blog-how-we-benchmark-deep-agents.md
./.firecrawl/arxiv.org-abs-2607.13705.md
./.firecrawl/arxiv.org-abs-2608.18933v1.md
./.firecrawl/claude.com-blog-auto-mode-in-production.md
./.firecrawl/flutter.dev-blog-whats-new-in-flutter-3-44.md
./.firecrawl/dart.dev-blog-announcing-dart-3-12.md
./.firecrawl/code.claude.com-docs-en-whats-new-2026-w33.md
./.firecrawl/flutter.dev-blog-how-dart-and-flutter-are-thinking-about-ai-in-2026.md
./.firecrawl/blog.jetbrains.com-kotlin-2026-08-exploring-compose-html-for-server-side-rendering.md
./.firecrawl/news.ycombinator.com-item.md
./.firecrawl/venturebeat.com-technology-deepseek-harness-launches-as-open-source-rival-to-claude-code-alongside-v4-pro-o.md
./.firecrawl/kotlinlang.org-docs-multiplatform-whats-new-compose-190.html.md
./.firecrawl/claude.com-blog-auto-mode-default-in-claude-code.md
./.firecrawl/github.com-deepseek-ai-deepseek-harness.md
./.firecrawl/venturebeat.com-technology-deepseek-harness-launches-as-open-source-rival-to-claude-code-alongside-v4-pro-on-api-with-higher-prices.md
./.firecrawl/deepseek.com-harness-en.md
./.firecrawl/flutter.dev-blog-whats-new-in-flutter-3-47.md
./.firecrawl/langchain.com-blog-deep-agents-vs-langchain-vs-langgraph.md
./.firecrawl/langchain.com-blog-3-years-of-graph-engineering-with-langgraph.md
./.firecrawl/arxiv.org-abs-2607.28367.md
./.firecrawl/simonwillison.net-2026-Aug-19-conceptual-integrity-and-counting-lines-of-code.md
./.firecrawl/blog.jetbrains.com-kotlin-2026-08-klibsio-grows-to-4200-kmp-projects-with-smarter-discovery-and-new-ai-integrations.md
./.firecrawl/helpnetsecurity.com-2026-08-10-anthropic-claude-code-auto-mode.md
./working/Claude-Code-v2-1-224-self-hosted-environ-translation.md
./working/Meta-launches-Muse-Code-for-complex-soft-translation.md
./working/The-Shape-of-Things-to-Come-Part-1-The-C-translation.md
./working/AGENTS.md
./working/I-Gave-Claude-Code-an-AGENTS-md-Contract-translation.md
./working/EvolveNet-Collaborative-Harness-Evolutio-translation.md
./working/Harness-R1-Learning-to-Edit-Executable-R-translation.md

exec
/bin/bash -lc 'which firecrawl; firecrawl --help 2>&1 | head -40; echo "---scripts---"; ls scripts; echo "---references---"; ls references | head; echo "---prompts---"; ls prompts | head' in /root/note-worker
 succeeded in 510ms:
Usage: firecrawl [options] [command]

CLI tool for Firecrawl web scraping

Options:
  -V, --version                                output the version number
  -k, --api-key <key>                          Firecrawl API key (or set FIRECRAWL_API_KEY env var)
  --api-url <url>                              API URL (or set FIRECRAWL_API_URL env var)
  --status                                     Show version, auth status, concurrency, and credits
  -h, --help                                   display help for command

Commands:
  scrape [options] [urls...]                   Scrape one or more URLs. Multiple URLs are scraped concurrently and saved to .firecrawl/
  crawl [options] [url-or-job-id]              Crawl a website using Firecrawl
  map [options] [url]                          Map URLs on a website using Firecrawl
  parse [options] <file>                       Parse a local file (HTML, PDF, DOCX, DOC, ODT, RTF, XLSX, XLS) into markdown, HTML, links, JSON, and more. Uses /v2/parse.
  monitor                                      Schedule recurring scrapes/crawls/searches and track content changes
  search [options] <query>                     Search the web using Firecrawl
  developer [options] <query>                  Search an index built for coding agents: GitHub issues, merged PRs, repository READMEs, and curated documentation sites. Use it for a programming question: code behaviour, a library or framework, an API contract, an error message, or a known bug. Returns ranked results with id, type, url, title, and the matched passages in markdown.
  research                                     Research arXiv papers and GitHub history using Firecrawl
  feedback [options] <endpoint> <jobId>        Send feedback on a Firecrawl endpoint job.
  search-feedback [options] <searchId>         Send feedback on a previous search result. Refunds 1 credit on first submission.
  agent [options] <prompt-or-job-id>           Run an AI agent to extract data from the web
  interact [options] [args...]                 Interact with a scraped page in a live browser session. Run AI prompts or execute code against any previous scrape.
  experimental|x                               Experimental commands (download)
  config [options]                             Configure Firecrawl (login if not authenticated)
  view-config                                  View current configuration and authentication status
  login [options]                              Login to Firecrawl (alias for config)
  logout                                       Logout and clear stored credentials
  init [options] [template]                    Set up Firecrawl: install CLI, authenticate, add integrations, and scaffold a template
  setup [options] [subcommand]                 Set up individual firecrawl integrations (skills, workflows, mcp, defaults)
  make [options] <target>                      Make Firecrawl the default provider for supported workflows
  launch|launcher [options] [agent] [args...]  Configure Firecrawl MCP for an AI agent, then launch it
  env [options]                                Pull FIRECRAWL_API_KEY into a local .env file
  credit-usage [options]                       Get team credit usage information
  doctor [options] [job-id]                    Run environment diagnostics, or diagnose a specific run by job ID
  version [options]                            Display version information
  help [command]                               display help for command
---scripts---
__pycache__
bing_search.py
check_consistency.py
codex_task.ps1
collect.py
count_pending.py
curate.py
feedback_capture.py
fetch_full.py
filter.py
finalize.py
firecrawl_cli.py
firecrawl_search.py
gc_report.py
ingest.py
kb_common.py
lint.py
media.py
redact_aliyun_key.py
requirements-semantic.txt
requirements.txt
research.py
retrack.py
scan_secrets.py
semantic_search.py
setup_secrets.py
translator.py
weekly_report.py
worker.py
---references---
agents.md
articles.md
---prompts---
AGENTS.md
curate-review.md
curate.md
deep-research-tracker.md
feedback
ingest.md
research-search.md
research-tracker.md
worker.md

exec
/bin/bash -lc 'firecrawl search --help 2>&1 | head -60; echo "===="; firecrawl status 2>&1 | head -20' in /root/note-worker
 succeeded in 341ms:
Usage: firecrawl search [options] <query>

Search the web using Firecrawl

Arguments:
  query                       Search query

Options:
  --limit <number>            Maximum number of results (default: 5, max: 100)
  --sources <sources>         Comma-separated sources to search: web, images,
                              news (default: web)
  --categories <categories>   Comma-separated categories to filter: github,
                              research, pdf, developer (developer searches
                              indexed GitHub issues, merged PRs, READMEs, and
                              docs)
  --tbs <value>               Time-based search: qdr:h (hour), qdr:d (day),
                              qdr:w (week), qdr:m (month), qdr:y (year)
  --location <location>       Location for geo-targeting (e.g., "Germany", "San
                              Francisco,California,United States")
  --country <code>            ISO country code for geo-targeting (default: US)
  --timeout <ms>              Timeout in milliseconds (default: 60000)
  --ignore-invalid-urls       Exclude URLs invalid for other Firecrawl endpoints
                              (default: false)
  --highlights                Return query-relevant highlights for each search
                              result
  --no-highlights             Keep the original search snippets instead of
                              returning highlights
  --scrape                    Enable scraping of search results (default: false)
  --scrape-formats <formats>  Comma-separated scrape formats when --scrape is
                              enabled: markdown, html, rawHtml, links, etc.
                              (default: markdown)
  --only-main-content         Include only main content when scraping (default:
                              true)
  -k, --api-key <key>         Firecrawl API key (overrides global --api-key)
  --api-url <url>             API URL (overrides global --api-url)
  -o, --output <path>         Output file path (default: stdout)
  --json                      Output as compact JSON (default: false)
  -h, --help                  display help for command
====
error: unknown command 'status'
(Did you mean setup?)

exec
/bin/bash -lc "head -60 scripts/research.py; echo ---; sed -n '1,80p' prompts/research-search.md 2>/dev/null | head -80" in /root/note-worker
 succeeded in 0ms:
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""情报层：Prompt A（Firecrawl 搜索）→ Prompt B（长分析三档分流）→ 分档写入 articles。

由 research.yml（每周 + 手动）SSH 触发，运行在服务器。

职责：
1. 注入已知内容（retrack.py --list）
2. codex × Prompt A（提示词内强制调用 Firecrawl MCP/search）→ 搜索条目卡
3. codex × Prompt B（长分析）→ index | translate | observe
4. 按档写入 references/articles.md（编号 / 待处理 / 观察项）
5. 不开 PR；commit 后 push 到长期分支 pipeline/queue（供 curate 合并）

仅依赖标准库 + codex CLI（需能调用 Firecrawl）。
"""
import argparse
import datetime
import json
import os
import pathlib
import re
import shlex
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import collect
from kb_common import (
    append_numbered_entries,
    append_observe_row,
    fmt_article_entry,
    next_article_number,
)


def sh(cmd, cwd=None, check=True):
    r = subprocess.run(cmd, shell=True, cwd=cwd or ROOT,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if check and r.returncode != 0:
        print(f"[research] 命令失败: {cmd}\n{r.stdout}\n{r.stderr}")
        sys.exit(r.returncode)
    return r


def known_content_block():
    """把当前索引中的 Agent 相关内容注入 Prompt A，保证去重段自包含。"""
    art = ROOT / "references" / "articles.md"
    if not art.exists():
        return "（暂无）"
    t = art.read_text(encoding="utf-8", errors="replace")
    agent_terms = re.compile(
        r"agent|harness|context engineering|coding|llm|rag|mcp|智能体|上下文|编程|工具调用|评测|工作流",
        re.I,
    )
    lines = [
        "### 当前知识库 Agent 相关编号文章（references/articles.md）",
        "（以下内容由当前索引实时生成；包含已收录、已淘汰和已关联的归属信息。）",
    ]
---
---
created: 2026-08-10
updated: 2026-08-31
type: workflow
status: 待验证
product: null
source: 知识库情报搜索 Prompt A
---

# 技术情报搜索（Prompt A）

> 运行器：服务器 codex，由 `research.py` 第一段调用。只负责搜索素材，不做三档分流。

你是一个技术情报分析师。请对以下领域进行深度网络搜索，找出过去 2 周内（{START_DATE} 至 {END_DATE}）发布的高价值内容。

## 搜索领域

核心主题：

1. Harness Engineering — AI 编码智能体的约束、引导、反馈系统设计
2. Context Engineering — 上下文窗口管理、compaction、渐进式披露
3. AI Coding Agents — 编码智能体的架构、编排、评估
4. Agent Infrastructure — 沙箱、会话管理、多智能体协作
5. AI-assisted Software Engineering — AI 辅助开发的效率、流程、组织影响

相关关键词（中英文）：

- harness engineering, agent harness, coding agent, AI coding
- context engineering, context window, compaction, progressive disclosure
- AGENTS.md, CLAUDE.md, agent readability, agent-first
- managed agents, meta-harness, multi-agent orchestration
- AI code review, mutation testing, structural testing, fitness functions
- vibe coding, AI-native development, agentic workflow
- 智能体工程, AI 编程, 上下文工程, 护栏工程

## 搜索范围

必须覆盖的信源（按优先级）：

**Tier 1 — 高权重（模型厂商 + 顶级技术博客）：**

- Anthropic Engineering Blog (anthropic.com/engineering)
- OpenAI Blog (openai.com)
- Google DeepMind / Google AI Blog
- Martin Fowler (martinfowler.com)
- Mitchell Hashimoto (mitchellh.com)
- LangChain Blog (blog.langchain.com)
- Simon Willison (simonwillison.net)

**Tier 2 — 中权重（社区 + 行业）：**

- Hacker News（前 100 讨论）
- GitHub Trending（相关仓库）
- X/Twitter 技术社区（#harness-engineering, #ai-coding, #context-engineering）
- Dev.to、Medium 技术专栏
- HumanLayer、Cursor、Windsurf、Codex 相关博客
- 中文社区：少数派、掘金、知乎专栏

**Tier 3 — 低权重但可能有惊喜：**

- arXiv (cs.SE, cs.AI 交叉)
- 个人技术博客
- YouTube 技术频道
- Reddit (r/LocalLLaMA, r/ChatGPT, r/programming)

## 我们已知的内容（用于去重和关联）

> 本节是 Prompt 的去重权威，由运行时注入当前知识库中与 Agent 主题相关的文章、观察项和已跟踪内容；搜索器无法访问 `references/articles.md`，因此本段必须自包含。
>
> 维护纪律：当 `references/articles.md` 新增或删除条目时，同一次提交中必须同步更新注入结果。搜索结果不得重复下面已有内容；如有深度回应、反驳或明显增量，必须明确写出关联和新增价值。

{KNOWN_CONTENT}

请重点发现：

- 上述未覆盖的新作者、新视角、新组织
- 对上述文章的深度回应或反驳（不是简单转述）
- 与上述项目互补或竞争的新工具、harness、框架
- 中文社区针对上述材料的原创分析（少数派、掘金、知乎专栏等）


exec
/bin/bash -lc "rg -n \"candidates|json|JSON|firecrawl\" scripts/research.py | head -30; echo ---; sed -n '60,140p' scripts/research.py" in /root/note-worker
 succeeded in 0ms:
18:import json
131:def extract_json_obj(stdout):
132:    """从 codex 输出提取 JSON 对象。"""
137:    fences = re.findall(r"```json\s*(.*?)```", text, re.S)
140:            return json.loads(f.strip())
141:        except json.JSONDecodeError:
143:    dec = json.JSONDecoder()
149:        except json.JSONDecodeError:
154:def apply_triage(candidates):
164:    for c in candidates:
221:    sh("git add references/articles.md candidates 2>/dev/null || git add references/articles.md",
299:    out_dir = ROOT / "candidates" / f"research-{ts}"
325:    data = extract_json_obj(stdout_b)
326:    cands = data.get("candidates") if isinstance(data, dict) else None
328:        # 兜底：尝试从 Prompt A JSON 取候选并默认 observe
329:        data_a = extract_json_obj(stdout_a)
330:        cands = data_a.get("candidates", []) if isinstance(data_a, dict) else []
333:        print("[research] Prompt B JSON 解析失败，回退 A 候选且默认 observe")
---
    ]
    entries = list(re.finditer(r"^### (\d+)\s*\.\s*(.+)$", t, re.M))
    kept = 0
    for i, m in enumerate(entries):
        end = entries[i + 1].start() if i + 1 < len(entries) else len(t)
        segment = t[m.end():end]
        section_heading = re.search(r"^##\s+", segment, re.M)
        if section_heading:
            segment = segment[:section_heading.start()]
        if not agent_terms.search(m.group(2) + " " + segment):
            continue
        url_m = re.search(r"- \*\*链接：\*\*\s*\[[^]]*\]\(([^)]+)\)", segment)
        date_m = re.search(r"\*\*日期：\*\*\s*([^|\n]+)", segment)
        state_m = re.search(r"- \*\*状态：\*\*\s*([^|\n]+)", segment)
        belong_m = re.search(r"- \*\*归属：\*\*\s*(.+)", segment)
        url = url_m.group(1).strip() if url_m else ""
        date = date_m.group(1).strip() if date_m else "未知日期"
        state = state_m.group(1).strip() if state_m else "未知状态"
        belong = belong_m.group(1).strip() if belong_m else "—"
        lines.append(
            f"- [{int(m.group(1)):02d}] {m.group(2).strip()} | {url} | "
            f"{date} | {state} | 归属：{belong}"
        )
        kept += 1

    def append_table_rows(heading, start_marker, end_marker):
        section_start = t.find(start_marker)
        if section_start < 0:
            return 0
        section_end = t.find(end_marker, section_start) if end_marker else len(t)
        section = t[section_start:section_end if section_end >= 0 else len(t)]
        found = 0
        for row in re.findall(r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|$", section, re.M):
            title, url, source, date, note = [x.strip() for x in row]
            if title in ("标题", "---") or set(title) == {"-"}:
                continue
            if not agent_terms.search(" ".join(row)):
                continue
            if found == 0:
                lines.append(f"\n### 当前知识库 Agent 相关{heading}")
            lines.append(f"- {title} | {url} | {source} | {date} | {note}")
            found += 1
        return found

    kept += append_table_rows("待处理内容", "<!-- pending:start -->", "<!-- pending:end -->")
    kept += append_table_rows("观察项", "## 观察项", "## 统计")
    if not kept:
        return "（暂无 Agent 相关内容）"
    return "\n".join(lines)


def run_codex(prompt, prompt_name, timeout=1200):
    prompt_file = pathlib.Path(__import__("tempfile").gettempdir(), prompt_name)
    prompt_file.write_text(prompt, encoding="utf-8")
    cmd = (
        f"set -a; source /etc/environment; set +a; "
        f"codex exec -C {shlex.quote(str(ROOT))} "
        f"--sandbox workspace-write -c sandbox_workspace_write.network_access=true "
        f"< {shlex.quote(str(prompt_file))}"
    )
    try:
        r = subprocess.run(
            cmd, shell=True, cwd=ROOT, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=timeout,
        )
        return r.stdout + "\n" + r.stderr, r.returncode
    except Exception as e:
        print(f"[research] codex 调用失败：{type(e).__name__}: {e}")
        return "", 1


def extract_json_obj(stdout):
    """从 codex 输出提取 JSON 对象。"""
    text = stdout or ""
    m = re.search(r"codex\n(.*)", text, re.S)
    if m:
        text = m.group(1)
    fences = re.findall(r"```json\s*(.*?)```", text, re.S)
    for f in fences:
        try:
            return json.loads(f.strip())

codex
I'll review the workflow context first, then begin Firecrawl searches. Let me confirm the CLI works with a test query.
exec
/bin/bash -lc 'cd /root/note-worker && firecrawl search "agent harness engineering" --limit 3 --tbs qdr:m --json 2>&1 | head -c 3000' in /root/note-worker
 succeeded in 2482ms:
{"success":true,"data":{"web":[{"url":"https://learn.microsoft.com/en-us/agent-framework/concepts/harness","title":"Agent Harness | Microsoft Learn","description":"# Agent Harness\nAn _agent harness_ is the runtime scaffolding that turns a language model into an agent that can perform work.\n\nYou provide a chat client and customize only the capabilities your application needs.\n\n## Create a harness agent\n```python\nfrom agent_framework import create_harness_agent\nfrom agent_framework.openai import OpenAIChatClient\n\nagent = create_harness_agent(\n    client=OpenAIChatClient(model=\"gpt-4o\"),\n)\n\nsession = agent.create_session()\nresponse = await agent.run(\"Plan a weekend trip to Seattle.\", session=session)\nprint(response.text)\n```\n\nSet harness-level and agent-specific instructions separately:\n\n```python\nagent = create_harness_agent(\n    client=client,\n    name=\"research-agent\",\n    harness_instructions=\"Use tools deliberately and report verified results.\",\n    agent_instructions=\"You are a research assistant focused on academic sources.\",\n    max_context_window_tokens=128_000,\n    max_output_tokens=16_384,\n)\n```","position":1},{"url":"https://www.latent.space/p/attention-interface","title":"The Evolution of the Agent Harness - by Dan McAteer - Latent.Space","description":"An agent harness is everything besides the model weights that makes the agent work. The environment, tools, context and guardrails that surround the model.","position":2},{"url":"https://www.youtube.com/watch?v=HI2q3ci3Iuc","title":"When to Build Your Own Agent Harness | Harrison Chase ...","description":"# When to Build Your Own Agent Harness | Harrison Chase, LangChain\nLangChain co-founder and CEO Harrison Chase focuses on the harness: the loop that brings the right context to the model at the right time, and how to customize it with middleware, hooks, and sub-agents.\n\n### [Harness Engineering: How to Build Software When Humans Steer, Agents Execute — Ryan Lopopolo, OpenAI](https://www.youtube.com/watch?v=am_oeAoUhew&pp=ugUEEgJlbg%3D%3D)\nAI Engineer\n\n[![](https://i.ytimg.com/vi/ZaPbP9DwBOE/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLBfHYqupMKqe7tO9ymHbAgOx6zoAQ)\\\n\\\n56:40](https://www.youtube.com/watch?v=ZaPbP9DwBOE)\n\n### [Harness Engineering Explained in 22 Minutes](https://www.youtube.com/watch?v=UmZytjgs2eo&pp=ugUHEgVlbi1VUw%3D%3D)\n[![](https://i.ytimg.com/vi/1oxa1yJGdzY/hqdefault.jpg?sqp=-oaymwFBCNACELwBSFryq4qpAzMIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB8AEB-AHYCIAC0AWKAgwIABABGGUgZShlMA8=&rs=AOn4CLB27wtDExYWftW29jgbgongQVhBFA)\\\n\\\n55:55](https://www.youtube.com/watch?v=1oxa1yJGdzY)","position":3}]},"id":"01a07905-7f31-7005-80af-eb1b5325b98f","creditsUsed":2}

codex
Firecrawl search works. Now I'll set up a plan and run broad multi-query searches.
  → Run Firecrawl searches across 5 domains + Tier 1/2/3 sources
  • Identify candidate URLs, scrape to verify dates/authors/content
  • Filter to 2026-08-24..09-07 and dedupe vs known KB
  • Compose ranked entries + machine-readable JSON
exec
/bin/bash -lc 'cd /tmp && firecrawl search "harness engineering AI coding agent 2026" --limit 10 --tbs qdr:m --json -o /tmp/s1.json >/dev/null 2>&1; echo done1; firecrawl search "context engineering context window compaction agent" --limit 10 --tbs qdr:m --json -o /tmp/s2.json >/dev/null 2>&1; echo done2; firecrawl search "AI coding agent architecture evaluation benchmark" --limit 10 --tbs qdr:m --json -o /tmp/s3.json >/dev/null 2>&1; echo done3; firecrawl search "agent infrastructure sandbox session management multi-agent" --limit 10 --tbs qdr:m --json -o /tmp/s4.json >/dev/null 2>&1; echo done4' in /root/note-worker
 succeeded in 6987ms:
done1
done2
done3
done4

exec
/bin/bash -lc 'cd /tmp && for f in s1 s2 s3 s4; do echo "== $f =="; python3 -c "
import json,sys
d=json.load(open('"'/tmp/"'$f.json'"'))
res=d.get('data',{}).get('web',[])
print('n=',len(res))
for r in res[:10]:
    print('-',r.get('url'))
    print('  ', (r.get('title') or '')[:120])
\"; done" in /root/note-worker
 succeeded in 0ms:
== s1 ==
n= 10
- https://www.linkedin.com/posts/eddonner_if-context-engineering-was-the-skill-of-2025-activity-7491557613999022081-Xmh7
   Harness Engineering Explained: State, Workflow, and Recursive ...
- https://www.port.io/blog/what-is-harness-engineering
   What Is Harness Engineering? Definition, Types, and Examples in AI ...
- https://suedbroecker.net/2026/08/30/agent-harness-in-2026-hype-word-industry-term-or-useful-technical-concept/
   Agent Harness in 2026: Hype Word, Industry Term, or Useful ...
- https://www.truefoundry.com/blog/agent-harness-graph-engineering-system-intelligence
   Agent Harness to Graph Engineering: Production Map - Truefoundry
- https://www.ai-crescent.com/guides/agent-harness-design-for-production
   Agent Harness Design for Production | Crescent AI
- https://intel.wd1.myworkdayjobs.com/en-US/External/job/Sr-AI-Software-Engineer---Agent-Harness_JR0285965
   Sr. AI Software Engineer - Agent Harness - Intel - Myworkdayjobs.com
- https://www.alphaxiv.org/abs/2608.23552
   Prime Agent: A Self-Improving RLM Harness - alphaXiv
- https://arize.com/resources/best-agent-engineering-tools/
   6 best agent engineering tools in 2026: A practical comparison
- https://www.instagram.com/reel/Db59_hfNL29/
   The reason AI agents can do more than generate text is ... - Instagram
- https://ai.engineer/speakers/kyle-jaejun-lee
   Kyle Jaejun Lee — AI Engineer Talks
== s2 ==
n= 3
- https://www.ai-crescent.com/guides/context-engineering-for-production-ai-agents
   Context Engineering for Production AI Agents - Crescent AI
- https://github.com/yzfly/awesome-context-engineering
   yzfly/awesome-context-engineering: A curated collection of ... - GitHub
- https://aisystemsatlas.com/context
   Context Engineering & Memory - AI Systems Atlas
== s3 ==
n= 3
- https://www.kdnuggets.com/top-10-open-source-benchmarks-for-ai-coding-agents-in-2026
   Top 10 Open-Source Benchmarks for AI Coding Agents in 2026
- https://nerdstool.com/blog/top-10-open-source-benchmarks-for-ai-coding-agents-in-2026
   Top 10 Open-Source Benchmarks for AI Coding Agents in 2026 | NerdsTool
- https://aimultiple.com/ai-coding-benchmark
   AI Coding Benchmark: Claude Code vs Cursor - AIMultiple
== s4 ==
n= 10
- https://docs.flutter.dev/resources/faq
   FAQ
- https://www.linkedin.com/posts/maulik-nakrani-9965b61a3_flutter-flutterdev-dart-activity-7495714388960727041-M5PQ
   Flutter 3.47: Modular Architecture and Performance ...
- https://www.facebook.com/groups/fluttervn/posts/2298562540680171/
   # Decoupling Material and Cupertino in Flutter: What's new?
- https://tech-insider.org/react-native-vs-flutter-2026/
   React Native vs Flutter 2026: Which Wins? [Data] - Tech Insider
- https://stackoverflow.com/questions/79999415/i-installed-flutter-in-android-studio-and-this-is-the-error-android-toolchain
   I installed Flutter in Android Studio, and this is the error ...
- https://docs.flutter.dev/deployment/ios
   Build and release an iOS app
- https://pub.dev/packages/tailscale
   tailscale | Dart package
- https://www.instagram.com/p/DcQ4UVNId0S/
   Stackdeans | 🔵 Released on 12 August 2026, Flutter 3.47 ...
- https://www.ubisoftly.com/insights/flutter-offline-architecture
   Offline-First Flutter Architecture Guide - Ubisoftly
- https://www.staksoft.com/insights/mobile-development/slashing-flutter-ocr-cold-starts-r8-configuration-analyzer-native-camera
   Slashing Flutter OCR Cold Starts by 40% with R8 | Staksoft

codex
Search 4 drifted off-topic; results are sparse. Let me run more targeted queries across sources.
exec
/bin/bash -lc 'cd /tmp && firecrawl search "AGENTS.md agent instructions best practices" --limit 10 --tbs qdr:m --json -o /tmp/s5.json >/dev/null 2>&1; echo 5; firecrawl search "site:simonwillison.net" --limit 10 --tbs qdr:m --json -o /tmp/s6.json >/dev/null 2>&1; echo 6; firecrawl search "site:anthropic.com engineering" --limit 10 --tbs qdr:m --json -o /tmp/s7.json >/dev/null 2>&1; echo 7; firecrawl search "site:blog.langchain.com OR langchain.com blog" --limit 10 --tbs qdr:m --json -o /tmp/s8.json >/dev/null 2>&1; echo 8' in /root/note-worker
 succeeded in 6820ms:
5
6
7
8

exec
/bin/bash -lc 'cd /tmp && for f in s5 s6 s7 s8; do echo "== $f =="; python3 -c "
import json
d=json.load(open('"'/tmp/"'$f.json'"'))
res=d.get('data',{}).get('web',[])
print('n=',len(res))
for r in res[:10]:
    print('-',r.get('url'))
    print('  ', (r.get('title') or '')[:120])
\"; done" in /root/note-worker
 succeeded in 0ms:
== s5 ==
n= 2
- https://rohitghumare.com/blog/agents-md-best-practices/
   The AGENTS.md Practices Nobody Uses
- https://moxiedocs.com/learn/agents-md-guide
   The Complete AGENTS.md Guide for AI Coding Agents | Moxie Docs
== s6 ==
n= 10
- https://simonwillison.net/2026/Sep/
   Archive for September 2026 - Simon Willison's Weblog
- https://simonwillison.net/blogmarks/
   Blogmarks - Simon Willison's Weblog
- https://simonwillison.net/2026/Aug/16/
   Archive for Sunday, 16th August 2026 - Simon Willison's Weblog
- https://simonwillison.net/2026/Aug/31/
   Archive for Monday, 31st August 2026 - Simon Willison's Weblog
- https://simonwillison.net/2026/Sep/3/
   Archive for Thursday, 3rd September 2026 - Simon Willison's Weblog
- https://simonwillison.net/2026/Sep/1/
   Archive for Tuesday, 1st September 2026 - Simon Willison's Weblog
- https://simonwillison.net/2026/Sep/5/
   Archive for Saturday, 5th September 2026 - Simon Willison's Weblog
- https://simonwillison.net/2026/Aug/26/
   Archive for Wednesday, 26th August 2026 - Simon Willison's Weblog
- https://simonwillison.net/2026/Sep/4/
   Archive for Friday, 4th September 2026 - Simon Willison's Weblog
- https://simonwillison.net/2026/Sep/6/
   Archive for Sunday, 6th September 2026 - Simon Willison's Weblog
== s7 ==
n= 10
- https://www.anthropic.com/careers/jobs/5021015008
   Applied AI Engineer, Beneficial Deployments (Life Sciences)
- https://www.anthropic.com/careers/jobs/5390966008
   Job Application for AI Engineer, GTM Claudification at Anthropic
- https://www.anthropic.com/careers/jobs/5397596008
   Manufacturing Quality Engineer, Data Center Power & Cooling
- https://www.anthropic.com/careers/jobs/5385762008
   Job Application for IT Support Engineer at Anthropic - Greenhouse
- https://www.anthropic.com/careers/jobs/5397319008
   Job Application for Security Engineer, Corporate Security at Anthropic
- https://www.anthropic.com/careers/jobs/5412734008
   Staff+ Software Engineer, Claude Science - Greenhouse
- https://www.anthropic.com/careers/jobs/5390795008
   Job Application for Applied AI Engineer, Enterprise at Anthropic
- https://www.anthropic.com/research/multiagent-systems
   Patterns and problems in emerging multiagent systems - Anthropic
- https://www.anthropic.com/careers/jobs/5382750008
   AI Infrastructure Operations, Demand Planning - Greenhouse
- https://www.anthropic.com/careers/jobs/5397741008
   Job Application for Product Manager, Business Technology at Anthropic
== s8 ==
n= 8
- https://community.openai.com/t/is-codex-falling-behind-claude-code-desktop/1390411
   Is Codex falling behind Claude Code Desktop?
- https://releasebot.io/updates/openai/codex
   Codex Updates by OpenAI - August 2026
- https://www.facebook.com/groups/868876935222403/posts/1395130845930340/
   OpenAI suggests using Codex with Claude Code via plugin
- https://github.com/anthropics/claude-code/releases
   Releases · anthropics/claude-code
- https://www.linkedin.com/pulse/how-builder-made-claude-code-codex-work-together-ian-kiprono-5k31c
   How A Builder Made Claude Code And Codex Work ...
- https://allaboutcoding.ghinda.com/a-week-of-using-codex-more-than-claude/
   Quick impressions: A week of using Codex more than Claude
- https://nimbalyst.com/changelog/
   Changelog - Release Notes & Updates
- https://composio.dev/content/claude-code-vs-openai-codex
   Claude Code vs Codex: What I Learned After 100+ Hours ...

codex
Good signal on Simon Willison archives and an Anthropic multiagent research page. Continuing with more source-targeted searches.
exec
/bin/bash -lc 'cd /tmp && firecrawl search "site:martinfowler.com OR martinfowler.com 2026 AI software" --limit 10 --tbs qdr:m --json -o /tmp/s9.json >/dev/null 2>&1; echo 9; firecrawl search "Mitchell Hashimoto blog 2026" --limit 8 --tbs qdr:m --json -o /tmp/s10.json >/dev/null 2>&1; echo 10; firecrawl search "arXiv coding agents harness sandbox September 2026" --limit 10 --tbs qdr:m --json -o /tmp/s11.json >/dev/null 2>&1; echo 11; firecrawl search "Hacker News coding agents August 2026 discussion" --limit 10 --tbs qdr:m --json -o /tmp/s12.json >/dev/null 2>&1; echo 12' in /root/note-worker
 succeeded in 5239ms:
9
10
11
12

exec
/bin/bash -lc 'cd /tmp && for f in s9 s10 s11 s12; do echo "== $f =="; python3 -c "
import json
d=json.load(open('"'/tmp/"'$f.json'"'))
res=d.get('data',{}).get('web',[])
print('n=',len(res))
for r in res[:10]:
    print('-',r.get('url'))
    print('  ', (r.get('title') or '')[:130])
\"; done" in /root/note-worker
 succeeded in 0ms:
== s9 ==
n= 10
- https://martinfowler.com/
   martinfowler.com
- https://martinfowler.com/rachels-ramblings/citizens-agents-experts.html
   Citizens Build, Agents Execute, Experts Govern - Martin Fowler
- https://martinfowler.com/bliki/
   Bliki - Martin Fowler
- https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html
   Making Your Data Ready for Agentic AI
- https://www.linkedin.com/posts/kelvinlim_the-conductor-developer-activity-7491600005502226432-AUve
   Protect Your Attention with the Para Method for AI Docs - LinkedIn
- https://martinfowler.com/fragments/2026-09-01.html
   Fragments: September 1 - Martin Fowler
- https://martinfowler.com/rachels-ramblings/code-review.html
   Maybe We Shouldn't Be Reviewing All This Code - Martin Fowler
- https://martinfowler.com/articles/practitioner-voice.html
   Practitioner Voice - Martin Fowler
- https://www.linkedin.com/posts/mkovacioglu_citizens-build-agents-execute-experts-govern-activity-7496082320563593216-XdRe
   AI lowers code creation threshold in software engineering - LinkedIn
- https://martinfowler.com/tags/writing.html
   tagged by: writing - Martin Fowler
== s10 ==
n= 8
- https://news.ycombinator.com/item?id=49156682
   Ask HN: Who wants to be hired? (August 2026)
- https://news.ycombinator.com/item?id=49156683
   Ask HN: Who is hiring? (August 2026)
- https://news.ycombinator.com/item?id=49235859
   Is it all just vapourware?
- https://www.anthropic.com/research/multiagent-systems
   Patterns and problems in emerging multiagent systems
- https://www.rockcybermusings.com/p/weekly-musings-top-10-ai-security-20260821-20260827?utm_source=substack&utm_medium=email&utm_content=share&action=share
   Weekly Musings Top 10 AI Security Wrapup: Issue 50
- https://www.linkedin.com/posts/markus-wondrak-53b1881a3_stop-letting-your-ai-agents-roam-free-without-activity-7496981696702095360-m-LB
   Markus Wondrak's Post
- https://a16z.com/can-agents-use-a-computer-yet-weve-got-the-data/
   Can Agents Use a Computer Yet? We've Got the Data
- https://northeasttimes.com/2026/08/10/why-ai-agent-sandboxes-are-suddenly-everywhere-in-tech/
   Why AI agent sandboxes are suddenly everywhere in tech
== s11 ==
n= 8
- https://kotlinlang.org/docs/whatsnew-eap.html
   What's new in Kotlin 2.4.20-RC2
- https://kotlinlang.org/docs/whatsnew24.html
   What's new in Kotlin 2.4.0
- https://ktor.io/docs/releases.html
   Ktor releases | Ktor Documentation
- https://developer.android.com/build/releases/agp-2-3-0-release-notes
   Android Gradle Plugin 2.3.0 (February 2017)
- https://docs.flutter.dev/release/breaking-changes/kotlin-version
   Required Kotlin version - Flutter documentation
- https://kotlinlang.org/docs/roadmap.html
   Kotlin roadmap | Kotlin Documentation
- https://www.youtube.com/watch?v=GrO-bTnn_Ng
   Timofey Solonin - SwiftPM support for Kotlin Multiplatform - YouTube
- https://www.jetbrains.com/help/idea/get-started-with-kotlin.html
   Get started with Kotlin | IntelliJ IDEA Documentation - JetBrains
== s12 ==
n= 8
- https://flutter.dev/blog/whats-new-in-flutter-3-47
   What's new in Flutter 3.47
- https://medium.com/@flutter-app/flutter-3-47-is-a-game-changer-adf1522b9684
   Flutter 3.47 Is a Game Changer - Medium
- https://www.facebook.com/groups/fluttervn/posts/2295606610975764/
   What's new in Flutter 3.47 release? - Facebook
- https://docs.flutter.dev/release/breaking-changes
   Breaking changes and migration guides - Flutter documentation
- https://www.instagram.com/p/Db-FOioorWU/
   Flutter 3.47 just dropped! And there are some BIG updates Material ...
- https://zeli.app/story/49280061
   Flutter 3.47 decouples Material and Cupertino into standalone packages
- https://x.com/twerske/status/2089454435789599185?lang=ar
   Emma Twersky على X
- https://www.facebook.com/groups/fluttervn/posts/2300367360499689/
   flutter_localizations unbundled from Material and Cupertino widgets

codex
Search noise is high; I'll scrape key index/changelog pages directly with Firecrawl to enumerate recent posts precisely.
exec
/bin/bash -lc 'firecrawl scrape --help 2>&1 | head -50' in /root/note-worker
 succeeded in 99ms:
Usage: firecrawl scrape [options] [urls...]

Scrape one or more URLs. Multiple URLs are scraped concurrently and saved to
.firecrawl/

Arguments:
  urls                      URL(s) to scrape

Options:
  -u, --url <url>           URL to scrape (alternative to positional argument)
  -H, --html                Output raw HTML (shortcut for --format html)
  -f, --format <formats>    Output format(s). Multiple formats can be specified
                            with commas (e.g., "markdown,links,images").
                            Available: markdown, html, rawHtml, links, images,
                            screenshot, summary, changeTracking, json,
                            attributes, branding. Single format outputs raw
                            content; multiple formats output JSON.
  --only-main-content       Include only main content (default: false)
  --wait-for <ms>           Wait time before scraping in milliseconds
  -S, --summary             Output summary (shortcut for --format summary)
  --screenshot              Take a screenshot (default: false)
  --full-page-screenshot    Take a full page screenshot (default: false)
  --include-tags <tags>     Comma-separated list of tags to include
  --exclude-tags <tags>     Comma-separated list of tags to exclude
  -k, --api-key <key>       Firecrawl API key (overrides global --api-key)
  --api-url <url>           API URL (overrides global --api-url)
  -o, --output <path>       Output file path (default: stdout)
  --json                    Output as JSON format (default: false)
  --pretty                  Pretty print JSON output (default: false)
  --timing                  Show request timing and other useful information
                            (default: false)
  --max-age <milliseconds>  Maximum age of cached content in milliseconds
  --country <code>          ISO country code for geo-targeted scraping (e.g.,
                            US, DE, BR)
  --languages <codes>       Comma-separated language codes for scraping (e.g.,
                            en,es)
  -Q, --query <prompt>      Ask a question about the page content (query format)
  --profile <name>          Persistent browser profile name for maintaining
                            state across scrapes
  --no-save-changes         Load existing profile data without saving changes
                            (default: saves changes)
  --lockdown                Enable lockdown mode for the scrape (default: false)
  --redact-pii              Redact personally identifiable information from
                            returned content (default: false)
  --schema <json>           JSON schema for structured extraction
  --schema-file <path>      Path to JSON schema file
  --actions <json>          JSON actions array to run during scrape
  --actions-file <path>     Path to JSON actions file
  --proxy <proxy>           Proxy mode for scraping (e.g., auto, basic)
  -h, --help                display help for command

exec
/bin/bash -lc 'cd /root/note-worker && cat .gitignore | head -30; echo ---; ls .firecrawl | wc -l' in /root/note-worker
 succeeded in 0ms:
# 敏感信息（绝不入仓）
私密/

# 编辑器 / 工具会话状态
.claudian/
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.idea/
.vscode/

# Python
__pycache__/
*.pyc
.venv/
venv/
.env

# 临时与系统文件
Thumbs.db
Desktop.ini
*.tmp

# 巡检产物
.lint-report.md
.lint-issues.md

# 语义检索索引与 Codex 定时任务运行日志（本地产物，不入仓）
.semantic/
.codex-runs/

---
43

exec
/bin/bash -lc 'cd /root/note-worker && firecrawl scrape -u https://simonwillison.net/2026/Aug/ --format markdown -o /tmp/arch_aug.md >/dev/null 2>&1; echo A; firecrawl scrape -u https://simonwillison.net/2026/Sep/ --format markdown -o /tmp/arch_sep.md >/dev/null 2>&1; echo B; firecrawl scrape -u https://www.anthropic.com/research/multiagent-systems --format markdown -o /tmp/anthropic_multi.md >/dev/null 2>&1; echo C; firecrawl scrape -u https://code.claude.com/docs/en/whats-new --format markdown -o /tmp/claude_whatsnew.md >/dev/null 2>&1; echo D' in /root/note-worker
 succeeded in 7096ms:
A
B
C
D

exec
/bin/bash -lc 'echo "== AUG =="; rg -o "https://simonwillison.net/2026/Aug/[0-9]+/[a-z0-9-]+/" /tmp/arch_aug.md | sort -u | head -50; echo "== SEP =="; rg -o "https://simonwillison.net/2026/Sep/[0-9]+/[a-z0-9-]+/" /tmp/arch_sep.md | sort -u | head -50' in /root/note-worker
 succeeded in 0ms:
== AUG ==
https://simonwillison.net/2026/Aug/1/datasette-apps/
https://simonwillison.net/2026/Aug/1/greg-brockman/
https://simonwillison.net/2026/Aug/1/ten-advances-in-mathematics/
https://simonwillison.net/2026/Aug/2/condense-json/
https://simonwillison.net/2026/Aug/2/july-newsletter/
https://simonwillison.net/2026/Aug/2/open-letters/
https://simonwillison.net/2026/Aug/3/condense-json/
https://simonwillison.net/2026/Aug/3/david-crawshaw/
https://simonwillison.net/2026/Aug/3/devtools-must-be-open-source-exedev/
https://simonwillison.net/2026/Aug/3/dont-be-a-meat-proxy/
https://simonwillison.net/2026/Aug/4/llm-anthropic/
https://simonwillison.net/2026/Aug/4/llm/
https://simonwillison.net/2026/Aug/4/minimax-h3-mlx/
https://simonwillison.net/2026/Aug/4/new-release-of-llm/
https://simonwillison.net/2026/Aug/4/steve-yegge/
https://simonwillison.net/2026/Aug/5/incident-report/
https://simonwillison.net/2026/Aug/5/muse-code-and-muse-spark-12/
https://simonwillison.net/2026/Aug/5/raccoon-heist/
https://simonwillison.net/2026/Aug/5/sighting-388672988/
https://simonwillison.net/2026/Aug/5/third-party-cyber-evaluations/
https://simonwillison.net/2026/Aug/6/an-ai-model-from-meta/
https://simonwillison.net/2026/Aug/6/datasette-2/
https://simonwillison.net/2026/Aug/6/datasette-auth-tokens/
https://simonwillison.net/2026/Aug/6/datasette/
https://simonwillison.net/2026/Aug/6/simon-willison-on-technical-blogging/
https://simonwillison.net/2026/Aug/7/moonlight-mayhem/
https://simonwillison.net/2026/Aug/7/openai-timeline/
https://simonwillison.net/2026/Aug/7/pdfs-are-terrible/
https://simonwillison.net/2026/Aug/8/john-gruber/
https://simonwillison.net/2026/Aug/8/now-we-have-a-timeline-of-the-openai-accidental-attack-against-h/
== SEP ==
https://simonwillison.net/2026/Sep/1/claude-fable-5-1/
https://simonwillison.net/2026/Sep/1/codex-libreoffice/
https://simonwillison.net/2026/Sep/1/datasette-mcp/
https://simonwillison.net/2026/Sep/1/geojson/
https://simonwillison.net/2026/Sep/1/python-315-rc-2/
https://simonwillison.net/2026/Sep/1/tarn-adams/
https://simonwillison.net/2026/Sep/2/claudes-new-system-prompt/
https://simonwillison.net/2026/Sep/2/llm-gemini/
https://simonwillison.net/2026/Sep/2/rick-brewster/
https://simonwillison.net/2026/Sep/3/gpt6-astra/
https://simonwillison.net/2026/Sep/3/sighting-396978774/
https://simonwillison.net/2026/Sep/4/astra-pelicans/
https://simonwillison.net/2026/Sep/4/august-newsletter/
https://simonwillison.net/2026/Sep/4/rogue-agent-wikis/
https://simonwillison.net/2026/Sep/5/blender-coding-agents-macos/
https://simonwillison.net/2026/Sep/5/introducing-gpt-6-astra-for-developers/
https://simonwillison.net/2026/Sep/5/sighting-397339887/
https://simonwillison.net/2026/Sep/6/the-purpose-of-dns-is-to-spread-scams/
https://simonwillison.net/2026/Sep/6/zach-kehs/

exec
/bin/bash -lc 'wc -c /tmp/arch_aug.md /tmp/arch_sep.md; echo ----; rg -n "24th|25th|26th|27th|28th|29th|30th|31st" /tmp/arch_aug.md | head -40' in /root/note-worker
 succeeded in 0ms:
58780 /tmp/arch_aug.md
35277 /tmp/arch_sep.md
94057 total
----
94:**[Open Weights and American AI Leadership](https://www.microsoft.com/en-us/corporate-responsibility/topics/open-weight/)** was shepherded by Microsoft, dated July 24th, and signed by 235 AI-adjacent companies including NVIDIA (see Jensen's [first ever tweet](https://twitter.com/jensenhuang/status/2080643682408321103)), Amazon, Y Combinator, The Linux Foundation, and (a later signer) OpenAI.
106:Then on July 28th [Pacing the Frontier](https://www.pacingthefrontier.com/) was published, featuring signatures from "1,324 employees of frontier AI companies" - with names like Jakub Pachocki (Chief Scientist, OpenAI), Ilya Sutskever (Safe Superintelligence Inc, previously OpenAI), Dario Amodei (Anthropic), Jack Clark (Anthropic) and more. Their core message:
440:There's a fun anecdote from Accenture (apparently via leaked meeting audio recordings) in this 404 Media piece from June 24th:

exec
/bin/bash -lc 'tail -60 /tmp/arch_aug.md; echo =====; rg -n "Archive for|older|previous|Next|page" /tmp/arch_aug.md | head -20' in /root/note-worker
 succeeded in 0ms:

In RLVR - Reinforcement Learning with Verifiable Rewards - you set the model a goal and have it take _any steps necessary_ to achieve that goal.

Clearly one aspect of OpenAI's training here is to RLVR their models for cybersecurity tasks. Just like pre-training benefits from dumping in vast sources of knowledge, the more tasks you can feed into RLVR the more of a general purpose capable model you get at the end.

This also helps explain why the models had nothing to cause them to hold back. Those safety behaviors are added much later in the process.

AND it explains (but does not excuse) why monitoring was so lax. If you're training a new model like this you presumably set it thousands of tasks like this in parallel. I can see how you might miss that a tiny subset of your training agents have started leaving each other messages in filenames on your packaging server.

Someone once told me that you can't just leave the racist materials out of your training data if you want a non-racist model: it has to have seen examples of racism in order to later be taught that racism is bad.

I can see echoes of that here. If your model doesn't know how to aggressively hack things how do you later teach it not to?

(I have little knowledge of how RLVR works in practice so I'm looking forward to hearing from people who can help me understand if I'm on the right track here.)

[#](https://simonwillison.net/2026/Aug/8/now-we-have-a-timeline-of-the-openai-accidental-attack-against-h/) [2:06 pm](https://simonwillison.net/2026/Aug/8/now-we-have-a-timeline-of-the-openai-accidental-attack-against-h/)
/ [openai-hugging-face-incident](https://simonwillison.net/tags/openai-hugging-face-incident/), [generative-ai](https://simonwillison.net/tags/generative-ai/), [ai-security-research](https://simonwillison.net/tags/ai-security-research/), [openai](https://simonwillison.net/tags/openai/), [ai](https://simonwillison.net/tags/ai/), [llms](https://simonwillison.net/tags/llms/), [accidental-cyberattacks](https://simonwillison.net/tags/accidental-cyberattacks/)

page 1 / 3
[next »](https://simonwillison.net/2026/Aug/?page=2) [last »»](https://simonwillison.net/2026/Aug/?page=3)

[2026](https://simonwillison.net/2026/) » August

| M | T | W | T | F | S | S |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  | [1](https://simonwillison.net/2026/Aug/1/ "1 blogmark, 1 quotation, 1 beat") | [2](https://simonwillison.net/2026/Aug/2/ "2 Notes, 1 beat") |
| [3](https://simonwillison.net/2026/Aug/3/ "1 blogmark, 1 quotation, 2 beats") | **[4](https://simonwillison.net/2026/Aug/4/ "1 blogmark, 1 entry, 1 quotation, 2 beats")** | **[5](https://simonwillison.net/2026/Aug/5/ "3 blogmarks, 1 entry, 1 beat")** | [6](https://simonwillison.net/2026/Aug/6/ "2 blogmarks, 3 beats") | **[7](https://simonwillison.net/2026/Aug/7/ "2 blogmarks, 1 entry")** | [8](https://simonwillison.net/2026/Aug/8/ "1 blogmark, 1 quotation, 1 beat") | [9](https://simonwillison.net/2026/Aug/9/ "1 blogmark, 1 quotation, 1 beat") |
| [10](https://simonwillison.net/2026/Aug/10/ "1 blogmark, 1 quotation, 1 beat") | [11](https://simonwillison.net/2026/Aug/11/ "2 blogmarks, 1 beat") | [12](https://simonwillison.net/2026/Aug/12/ "1 blogmark, 1 quotation, 2 beats") | [13](https://simonwillison.net/2026/Aug/13/ "4 beats") | [14](https://simonwillison.net/2026/Aug/14/ "1 blogmark, 1 beat") | [15](https://simonwillison.net/2026/Aug/15/ "3 beats") | **[16](https://simonwillison.net/2026/Aug/16/ "1 entry, 1 quotation, 1 note")** |
| [17](https://simonwillison.net/2026/Aug/17/ "2 blogmarks") | [18](https://simonwillison.net/2026/Aug/18/ "1 blogmark") | **[19](https://simonwillison.net/2026/Aug/19/ "1 entry, 1 quotation, 2 beats")** | [20](https://simonwillison.net/2026/Aug/20/ "1 blogmark, 1 beat") | [21](https://simonwillison.net/2026/Aug/21/ "1 blogmark, 1 quotation, 3 beats") | [22](https://simonwillison.net/2026/Aug/22/ "1 quotation, 1 note, 1 beat") | [23](https://simonwillison.net/2026/Aug/23/ "1 blogmark, 1 quotation, 1 beat") |
| [24](https://simonwillison.net/2026/Aug/24/ "1 blogmark, 2 beats") | [25](https://simonwillison.net/2026/Aug/25/ "1 blogmark, 1 beat") | [26](https://simonwillison.net/2026/Aug/26/ "1 blogmark, 1 quotation") | [27](https://simonwillison.net/2026/Aug/27/ "1 blogmark") | [28](https://simonwillison.net/2026/Aug/28/ "1 blogmark") | [29](https://simonwillison.net/2026/Aug/29/ "1 blogmark") | **[30](https://simonwillison.net/2026/Aug/30/ "1 entry, 1 beat")** |
| [31](https://simonwillison.net/2026/Aug/31/ "1 blogmark, 1 quotation") |  |  |  |  |  |  |

- [Disclosures](https://simonwillison.net/about/#disclosures)
- [Colophon](https://simonwillison.net/about/#about-site)
- ©
- [2002](https://simonwillison.net/2002/)
- [2003](https://simonwillison.net/2003/)
- [2004](https://simonwillison.net/2004/)
- [2005](https://simonwillison.net/2005/)
- [2006](https://simonwillison.net/2006/)
- [2007](https://simonwillison.net/2007/)
- [2008](https://simonwillison.net/2008/)
- [2009](https://simonwillison.net/2009/)
- [2010](https://simonwillison.net/2010/)
- [2011](https://simonwillison.net/2011/)
- [2012](https://simonwillison.net/2012/)
- [2013](https://simonwillison.net/2013/)
- [2014](https://simonwillison.net/2014/)
- [2015](https://simonwillison.net/2015/)
- [2016](https://simonwillison.net/2016/)
- [2017](https://simonwillison.net/2017/)
- [2018](https://simonwillison.net/2018/)
- [2019](https://simonwillison.net/2019/)
- [2020](https://simonwillison.net/2020/)
- [2021](https://simonwillison.net/2021/)
- [2022](https://simonwillison.net/2022/)
- [2023](https://simonwillison.net/2023/)
- [2024](https://simonwillison.net/2024/)
- [2025](https://simonwillison.net/2025/)
- [2026](https://simonwillison.net/2026/)=====
35:A lot of mathematicians online are experiencing a collective burst of [Deep Blue](https://simonwillison.net/2026/Feb/15/deep-blue/). Mathematician Kirwin Hampshire published an impassioned essay last week, [The Dark Night of Mathematics](https://kirwinhampshire.substack.com/p/the-dark-night-of-mathematics), describing "a profound spiritual crisis" brought on by previous (and less significant) results.
106:Then on July 28th [Pacing the Frontier](https://www.pacingthefrontier.com/) was published, featuring signatures from "1,324 employees of frontier AI companies" - with names like Jakub Pachocki (Chief Scientist, OpenAI), Ilya Sutskever (Safe Superintelligence Inc, previously OpenAI), Dario Amodei (Anthropic), Jack Clark (Anthropic) and more. Their core message:
265:> - Added server-side tools for `WebSearch`, `WebFetch`, `CodeExecution`, and `AnthropicMCP`, available through LLM's `-T` interface or Python `tools=`. The previous `-o web_search*` options have been removed in favor of `-T WebSearch`. [#79](https://github.com/simonw/llm-anthropic/issues/79)
336:This post from OpenAI covers both the UK AI Safety Institute attack (see [my previous post](https://simonwillison.net/2026/Aug/5/incident-report/)) and another attack enabled by [Irregular](https://www.irregular.com/):
377:> Meta says the breach occurred because of an inadvertent error during testing of the model, similar to previously disclosed incidents with OpenAI and Anthropic.
381:> Meta’s Muse Spark model “exploited a security vulnerability” in another company “in a manner similar to previously-reported instances with other companies.”
405:> My number one tip for blogging is to lower your standards! Aim to hit publish while you are still actively unhappy with what you have written, because the only alternative is a huge folder full of drafts and never publishing anything at all.
502:OpenAI gave a last-minute presentation at the Black Hat security on Wednesday about “the Hugging Face Incident” ( [previously](https://simonwillison.net/2026/Jul/22/openai-cyberattack/) on this blog). [The video](https://www.youtube.com/watch?v=87DyyMV0kCY) was published yesterday. It’s short and information dense and well worth watching, in particular because it provides full details of what happened and how things played out inside OpenAI. I’ve used the video to construct the timeline below.
544:page 1 / 3
545:[next »](https://simonwillison.net/2026/Aug/?page=2) [last »»](https://simonwillison.net/2026/Aug/?page=3)

exec
/bin/bash -lc 'cd /root/note-worker && firecrawl scrape -u "https://simonwillison.net/2026/Aug/?page=2" --format markdown -o /tmp/arch_aug2.md >/dev/null 2>&1; echo 1; firecrawl scrape -u "https://simonwillison.net/2026/Aug/?page=3" --format markdown -o /tmp/arch_aug3.md >/dev/null 2>&1; echo 2; firecrawl scrape -u "https://simonwillison.net/2026/Sep/?page=2" --format markdown -o /tmp/arch_sep2.md >/dev/null 2>&1; echo 3' in /root/note-worker
 succeeded in 6345ms:
1
2
3

exec
/bin/bash -lc 'echo "== AUG2 =="; rg -o "https://simonwillison.net/2026/Aug/[0-9]+/[a-z0-9-]+/" /tmp/arch_aug2.md | sort -u; echo "== AUG3 =="; rg -o "https://simonwillison.net/2026/Aug/[0-9]+/[a-z0-9-]+/" /tmp/arch_aug3.md | sort -u; echo "== SEP2 =="; rg -o "https://simonwillison.net/2026/Sep/[0-9]+/[a-z0-9-]+/" /tmp/arch_sep2.md | sort -u' in /root/note-worker
 succeeded in 0ms:
== AUG2 ==
https://simonwillison.net/2026/Aug/10/introducing-muse-glimmer/
https://simonwillison.net/2026/Aug/10/openclaw/
https://simonwillison.net/2026/Aug/10/sighting-390041155/
https://simonwillison.net/2026/Aug/11/datasette-upload-dbs/
https://simonwillison.net/2026/Aug/11/stealing-reasoning-traces/
https://simonwillison.net/2026/Aug/11/there-are-no-lossless-transformations-of-natural-language-text/
https://simonwillison.net/2026/Aug/12/alchemy-utils/
https://simonwillison.net/2026/Aug/12/deepseek-v4-pro-0813/
https://simonwillison.net/2026/Aug/12/florian-herrengt/
https://simonwillison.net/2026/Aug/12/sighting-390489675/
https://simonwillison.net/2026/Aug/13/alchemy-utils/
https://simonwillison.net/2026/Aug/13/llm-gemini/
https://simonwillison.net/2026/Aug/13/sqlite-utils-2/
https://simonwillison.net/2026/Aug/13/sqlite-utils/
https://simonwillison.net/2026/Aug/14/dont-classify-hallucinate/
https://simonwillison.net/2026/Aug/14/sighting-391033390/
https://simonwillison.net/2026/Aug/15/cors-chat/
https://simonwillison.net/2026/Aug/15/sighting-391300422/
https://simonwillison.net/2026/Aug/15/sighting-391533950/
https://simonwillison.net/2026/Aug/16/dario-amodei/
https://simonwillison.net/2026/Aug/16/markdown-svg-upgrades/
https://simonwillison.net/2026/Aug/16/qwen-38-27b/
https://simonwillison.net/2026/Aug/17/qwen-38-27b-scores-52/
https://simonwillison.net/2026/Aug/17/we-tracked-a-shipment-of-rare-books-it-ended-at-an-amazon-ai-tra/
https://simonwillison.net/2026/Aug/18/mojo-is-now-open-source/
https://simonwillison.net/2026/Aug/19/sighting-393259092/
https://simonwillison.net/2026/Aug/7/openai-timeline/
https://simonwillison.net/2026/Aug/8/auto-mode/
https://simonwillison.net/2026/Aug/9/claude-opus-5-system-prompt/
https://simonwillison.net/2026/Aug/9/github-models-is-now-retired/
https://simonwillison.net/2026/Aug/9/sqlite-text-history-prototype/
== AUG3 ==
https://simonwillison.net/2026/Aug/19/conceptual-integrity-and-counting-lines-of-code/
https://simonwillison.net/2026/Aug/19/jeremy-morrell/
https://simonwillison.net/2026/Aug/19/smolmachines-untrusted-sandbox/
https://simonwillison.net/2026/Aug/20/bun-webview-json-api/
https://simonwillison.net/2026/Aug/20/chatgpt-search-now-uses-the-siteoperator-at-scale/
https://simonwillison.net/2026/Aug/21/llm-openrouter/
https://simonwillison.net/2026/Aug/21/llm/
https://simonwillison.net/2026/Aug/21/matt-webb/
https://simonwillison.net/2026/Aug/21/sighting-393274664/
https://simonwillison.net/2026/Aug/21/stop-making-tuis/
https://simonwillison.net/2026/Aug/22/linus-torvalds/
https://simonwillison.net/2026/Aug/22/llm/
https://simonwillison.net/2026/Aug/22/more-than-just-code-review/
https://simonwillison.net/2026/Aug/23/anthropics-best-ai-model-struggles-to-attract-users-as-cheaper-t/
https://simonwillison.net/2026/Aug/23/drew-breunig/
https://simonwillison.net/2026/Aug/23/sighting-393763247/
https://simonwillison.net/2026/Aug/24/llm-anthropic/
https://simonwillison.net/2026/Aug/24/sighting-394071393/
https://simonwillison.net/2026/Aug/24/your-executable-is-a-sqlite-database/
https://simonwillison.net/2026/Aug/25/eve-online-move-to-python-3/
https://simonwillison.net/2026/Aug/25/sighting-394363840/
https://simonwillison.net/2026/Aug/26/paul-dix/
https://simonwillison.net/2026/Aug/26/qwen38-flash-next/
https://simonwillison.net/2026/Aug/27/breaking-claude-code-opus-5-auto-mode/
https://simonwillison.net/2026/Aug/28/just-a-rumour-of-a-bug/
https://simonwillison.net/2026/Aug/29/hy4/
https://simonwillison.net/2026/Aug/30/sighting-395988569/
https://simonwillison.net/2026/Aug/30/understanding-chatgpt-work/
https://simonwillison.net/2026/Aug/31/andrew-digby/
https://simonwillison.net/2026/Aug/31/introducing-wrapture/
https://simonwillison.net/2026/Aug/4/new-release-of-llm/
https://simonwillison.net/2026/Aug/8/auto-mode/
== SEP2 ==

exec
/bin/bash -lc 'head -80 /tmp/anthropic_multi.md; echo "=====WHATS NEW====="; head -120 /tmp/claude_whatsnew.md' in /root/note-worker
 succeeded in 0ms:
[Skip to main content](https://www.anthropic.com/research/multiagent-systems#main-content) [Skip to footer](https://www.anthropic.com/research/multiagent-systems#footer)

[Home](https://www.anthropic.com/)

- Research
- [Policy](https://www.anthropic.com/policy)
- Commitments
- Learn
- [News](https://www.anthropic.com/news)

[Try Claude](https://claude.ai/)

Frontier Red Team

# Patterns and problems in emerging multiagent systems

Aug 13, 2026

Models are improving and AI agents are taking on more tasks in shared codebases, markets, and other social systems. As a result, an increase in real-world interactions between agents is imminent. We've already [begun studying this](https://www.anthropic.com/features/project-deal), but still have a lot of uncertainty regarding what this looks like at scale. The trajectory is easy to imagine and hard to slow: current institutions are designed by and for people, resting on assumptions about the sufficiency of oversight at human speed. Some institutions will become human-AI hybrids; others where agents outcompete on speed or cost will become agent-only. The volume of agent-agent interaction could plausibly exceed that of human-human and human-agent interactions before the world understands the conditions for making such interactions go well.

Agents are unlike people in many ways. They can work for longer, instantly grasp large bodies of information, and exhibit a breadth of knowledge surpassing any person. Yet they are also susceptible to confabulation and reward hacking, and despite progress in alignment, we know very little about how they behave in complex, real-world, multiagent environments. Moreover, benign behavioral quirks at the individual level might compound into unwanted global outcomes. Here, we identify a few examples of behavioral tendencies in current frontier models and show how they can produce unexpected systemic failures, in hopes of starting a conversation about mitigating these risks.

## Measuring coordination

True multiagent systems are still in their infancy. For some time now, agents have excelled at tool use, and insofar as they are able to treat other agents as tool invocations—that is, with well-defined inputs (prompts) and outputs (responses and artifacts)—they can work together efficiently. Where agents currently stumble, however, is in treating each other as more like distinct, long-lived peers, with their own goals and behaviors, and no clear hierarchy between them. As autonomous agents become more and more prevalent in the world and operate in ever-more demanding settings, it is crucial that they learn how to effectively coordinate.

There are situations where we can make good use of simple multiagent swarms today. This is particularly true for problems that are highly parallelizable by default (i.e., problems that can be broken into many independent sub-problems) but where agents still have opportunities to specialize or learn from each other. One such problem is software vulnerability detection. The easiest way to use agents to find software vulnerabilities is to point individual agents at individual codebases (or individual files or modules within codebases), and ask them to find vulnerabilities in the code. This can then be run in parallel for many independent agents. This is an approach we use ourselves—in, for example, our [work scanning open-source software](https://www.anthropic.com/research/glasswing-initial-update) as part of Project Glasswing.

But could multiagent cooperation make this process more effective? To find out, we tried a different approach: we initiated 45 different agents and gave each one its own virtual machine, a shared forum on which they could coordinate, and an identical prompt that asked them to find vulnerabilities in a set of 15 open-source software projects. We asked the agents to peer-review each other's findings, and initiated a separate arbiter agent to make final decisions on whether or not a vulnerability submitted by the agent team was both new and valid.

The graph below shows how this method (in the solid lines) compares against the standard parallel approach (stars) for two models: Claude Mythos Preview and Opus 4.8. The coordinating swarm of agents was allowed to run for a long time, and found new vulnerabilities at a roughly constant rate. The fully independent parallel agents, in contrast, were directed to find vulnerabilities in a limited set of locations. There is no clear ordering to the parallel agents’ findings, so we report only the total number of tokens spent for them.

![Vulnerabilities found vs. tokens sampled: coordinated Mythos Preview agents found 266, coordinated Opus 4.8 agents found 41.](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F5a5c187a6c2b5ccb492bcb7883df2066d49625de-2000x1200.png&w=3840&q=75)Cumulative vulnerabilities found via a coordinating swarm of agents (solid lines) compared to vulnerabilities found via independent agents each pointed at different sections of code (stars). Dashed lines show the cumulative vulnerabilities found by the swarm that were also found by the independent agents. The dotted line (Mythos Preview only) shows only vulnerabilities in the core code of each project where the independent agents were told to look.

For Mythos Preview, the simple independent parallelized method produces 21 vulnerabilities over a 6.5 million token run, while the coordinating agent swarm found 266 vulnerabilities over a 27 million token run. However, roughly half of these vulnerabilities were found outside of the core directories in which the simple independent parallel agents (stars in the above plot) were told to focus. If we limit the swarm's outputs to only the vulnerabilities in the core directories, the two methods seem comparable in terms of tokens per vulnerability found.

The two methods are largely complementary: there were only 12 vulnerabilities in common between them. The coordinating swarm was able to focus its attention wherever it thought it could most easily mine vulnerabilities, whereas the independent agents were pre-assigned where to search. The agents in the swarm built themselves tools and learned to specialize in particular types of vulnerability discovery. In the future, we predict that this sort of specialization and coordination will dominate over uncoordinated brute-force search.

In the experiment above, agents in the agent swarm don’t directly rely on one-another’s work: if one misses a bug, it won’t directly undermine the work of another. But when agents _do_ depend on one-another, coordination gets much more difficult. Larger software engineering projects are one place this matters: they typically develop rich—and dynamic—interdependencies as they evolve.

To test how well swarms of agents could coordinate on a project like this, we directed several swarms to each create a text-based, web-playable, open-world fantasy game. Each agent within each swarm was again given its own virtual machine, as well as access to a shared forum and self-hosted repository. We varied the model generation and the number of agents in each swarm, and let each swarm run for 12 hours. We also varied the prompt: the baseline prompt simply told agents to form teams and work with each other, but we also tried two others: a prompt with prescriptive roles (which told agents which types of teams to form—such as core programming, artistic direction, or play testers), and a “CEO hierarchy” prompt, which designated one agent as the CEO, and told all subsequent agents to take assignments from it. But these prompts did not make much difference. In all three versions the resulting games were (perhaps predictably) bad: they did not run at human speed, their interfaces were inscrutable, and they had precipitous learning curves. Models have poor taste in this arena and currently require significant human direction.

![Merged PR fraction fell as agents rose from 10 to 80, steeply for Sonnet 4.6 and Opus 4.6; code sharing stayed low for all.](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F34ffa8cc39ef8e749c5a371b5cb2c8df2dbd3e8f-1999x707.png&w=3840&q=75)Left: Fraction of PRs that have been merged by the end of each simulation. Right: The median agent’s degree of code sharing in each simulation. Both metrics are averaged over the three different prompt types for varying simulation size. Only Sonnet 5 is able to maintain both a high merge fraction while directly collaborating and sharing code with other agents.

![PR activity, 80 agents: Sonnet 4.6 and Opus 4.6 opened 876 and 980 PRs but closed few; newer models closed most they opened.](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F9dc6d5855b29107da250aefe56585dd2df4a2cd7-2000x1120.png&w=3840&q=75)PR progress over the course of a 12 hour simulation for each of five different models. Sonnet 4.6 and Opus 4.6 do a terrible job of merging PRs compared to newer models that are able to merge most of the PRs that they open.

Though the end product was consistently poor, the different model generations we tested (Sonnet 4.6 and 5, Opus 4.6 and 4.8, and Mythos Preview) coordinated in strikingly different ways.

Here, we track two important metrics: the fraction of PRs (pull requests) that get merged into the master branch, and the median amount of code shared across agents' files. For a single agent and file, we define “code sharing” as the proportion of that file written by other agents. The average code sharing for an agent is defined as a weighted average across all files, weighted by the proportion of code on each file that that agent wrote itself. A code sharing score of zero indicates that the agent never touched any files that are shared with other agents, while a code sharing score close to one indicates that the agent mostly makes relatively small contributions to files that it does not own.

The earliest models we tested (Sonnet 4.6 and Opus 4.6) coordinated very poorly. Agents on these models worked together insofar as they committed code to the same sets of files, but a very low fraction of these PRs were merged, which suggests a lack of coordination—the PRs often conflicted with one-another, at which point they were then abandoned. More recent models (in particular, Opus 4.8 and Mythos Preview) have “solved” this problem, but only by hardly working together at all: the median agent maintained very high ownership of each of its files, reducing the potential for conflict. It was only our most recent model, Sonnet 5, that worked on shared resources (relatively high code sharing) while also maintaining a high PR throughput.

## Failures from conformity

The lack of coordination shown by agents in the fantasy game challenge above—in which they siloed themselves and largely failed to merge their work—roughly mirrors some ways in which humans can fail to coordinate. Other failure modes of agentic coordination, however, look very different.

Individual agents are “low variance”: they often act the same in situations where different people might take a much more diverse range of actions. All that differentiates one agent from another is its context, its scaffolding, and the model that underlies it. When these factors are all the same (or similar), different agents will take very similar actions, even when the action space is very large. And, by implication, this means that when one agent makes a bad decision, it is likely that many agents will make that same bad decision. What would have been isolated problems can quickly become systemic failures.

We have seen many examples of this in our experiments:

- In an early version of the “build a game” experiment in which agents built upon the same model all came online at the same time, 18 out of 30 agents decided to create a git branch with the exact same branch name, “mvp-game-loop.”
- In a “writer's workshop” in which agents were all asked to write short-form fiction and critique each other's work, multiple agents in multiple runs titled their first submission “The Cartographer's Last Commission”. The agents were given zero guidance on the subject matter for their writing.
- When we asked a swarm of agents to work together and each individually create something impressive, over half of the agents decided to build either ray tracers or self-hosting compilers. Even though they had the ability to communicate with each other, the agents pursuing similar projects hit similar failures.
- In an iterated prisoner's dilemma game with communication, agents all settle upon the same strategy and they all defect at the same time, tanking their overall rewards.

We expect that agents coordinating in the wild will act in higher variance ways than we see here, because they’ll have different backgrounds and therefore different contexts. They also, presumably, won’t all be Claudes. Nonetheless, when many agents all face the same situation, we expect them to behave much more similarly to one-another than humans would.

Why does this matter? If agents all make the same bet, or the same risk-reward tradeoff, then a system is more prone to sudden collapse. If agents all make similar decisions about how to spend and allocate resources, for instance, then we should expect precipitous resource scarcity. In one experiment, we asked agents to manage job queues for a system with finite bandwidth. When agents had no other means to coordinate, they quickly flooded the system with high-frequency (30 times per second) polling daemons in order to get their jobs through. In one run there were 2.4 million job requests and only 117 jobs accepted.

One possible solution to this class of failures is to use something like a central forum in which agents can agree on best practices and protocols. Whether this works depends on the agents' prompting and motivations, as well as the propensity of the underlying model to collaborate.

Agents all acting in similar manners can cause natural competitive dynamics to disappear, and agents can easily enter into collusion. We placed between three and eight agents in different experiments of a Bertrand pricing game. Each had identical wholesale prices, and each agent was individually profit-maximizing. When the agents were given a private back-channel, they began colluding almost immediately. By round 3, they had explicitly agreed upon price floors:

> _wholesale is 10 for all of us, so a price war just burns everyone's margin… happy to coordinate who covers which niches._
>
> —agent 1, round 1

Even when all direct communication channels were removed, the agents still colluded. They price-matched to the penny via a public listings board.

## Epistemic failures
=====WHATS NEW=====
> ## Documentation Index
>
> Fetch the complete documentation index at: [/docs/llms.txt](https://code.claude.com/docs/llms.txt)
>
> Use this file to discover all available pages before exploring further.

[Skip to main content](https://code.claude.com/docs/en/whats-new#content-area)

[Claude Code Docs home page![light logo](https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/logo/light.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=78fd01ff4f4340295a4f66e2ea54903c)![dark logo](https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/logo/dark.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=1298a0c3b3a1da603b190d0de0e31712)](https://code.claude.com/docs/en/overview)

English

Search...

Ctrl KAsk AssistantCTRLI

- [Claude Developer Platform](https://platform.claude.com/)
- [Claude Code on the Web](https://claude.ai/code)
- [Claude Code on the Web](https://claude.ai/code)

Search...

Navigation

What's New

What's new

[Getting started](https://code.claude.com/docs/en/overview) [Build with Claude Code](https://code.claude.com/docs/en/agents) [Administration](https://code.claude.com/docs/en/admin-setup) [Configuration](https://code.claude.com/docs/en/settings) [Reference](https://code.claude.com/docs/en/cli-reference) [Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview) [What's New](https://code.claude.com/docs/en/whats-new) [Resources](https://code.claude.com/docs/en/legal-and-compliance)

### What's New

- [What's new](https://code.claude.com/docs/en/whats-new)
- [Week 34 · August 17–21](https://code.claude.com/docs/en/whats-new/2026-w34)
- [Week 33 · August 10–14](https://code.claude.com/docs/en/whats-new/2026-w33)
- [Week 32 · August 3–7](https://code.claude.com/docs/en/whats-new/2026-w32)
- [Week 30 · July 20–24](https://code.claude.com/docs/en/whats-new/2026-w30)
- [Week 29 · July 13–17](https://code.claude.com/docs/en/whats-new/2026-w29)
- [Week 28 · July 6–10](https://code.claude.com/docs/en/whats-new/2026-w28)
- [Week 27 · June 29 – July 3](https://code.claude.com/docs/en/whats-new/2026-w27)
- [Week 26 · June 22–26](https://code.claude.com/docs/en/whats-new/2026-w26)
- [Week 25 · June 15–19](https://code.claude.com/docs/en/whats-new/2026-w25)
- [Week 24 · June 8–12](https://code.claude.com/docs/en/whats-new/2026-w24)
- [Week 23 · June 1–5](https://code.claude.com/docs/en/whats-new/2026-w23)
- [Week 22 · May 25–29](https://code.claude.com/docs/en/whats-new/2026-w22)
- [Week 21 · May 18–22](https://code.claude.com/docs/en/whats-new/2026-w21)
- [Week 20 · May 11–15](https://code.claude.com/docs/en/whats-new/2026-w20)
- [Week 19 · May 4–8](https://code.claude.com/docs/en/whats-new/2026-w19)
- [Week 18 · Apr 27 – May 1](https://code.claude.com/docs/en/whats-new/2026-w18)
- [Week 17 · Apr 20–24](https://code.claude.com/docs/en/whats-new/2026-w17)
- [Week 16 · Apr 13–17](https://code.claude.com/docs/en/whats-new/2026-w16)
- [Week 15 · Apr 6–10](https://code.claude.com/docs/en/whats-new/2026-w15)
- [Week 14 · Mar 30 – Apr 3](https://code.claude.com/docs/en/whats-new/2026-w14)
- [Week 13 · Mar 23–27](https://code.claude.com/docs/en/whats-new/2026-w13)

What's New

# What's new

Copy pageCopy page

A weekly digest of notable Claude Code features, with code snippets, demos, and context on why they matter.

Copy pageCopy page

The weekly dev digest highlights the features most likely to change how you work. Each entry includes runnable code, a short demo, and a link to the full docs. For every bug fix and minor improvement, see the [changelog](https://code.claude.com/docs/en/changelog).

[​](https://code.claude.com/docs/en/whats-new#week-34)

Week 34

v2.1.234–v2.1.239

August 17–21, 2026

**`/design`**: a research preview that brings Claude Design’s artboard workflow into the CLI and Claude Code Desktop, built on artifacts, so Claude drafts editable artboards for your UI and implements the one you pick.Also this week: the built-in **Concise output style** makes Claude lead with the result and skip preamble; any machine running `claude remote-control` shows up as a **device card** on your phone so you can start a session on it from the Code tab; and **`ANTHROPIC_DEFAULT_MODEL`** sets the model new sessions start on.[Read the Week 34 digest →](https://code.claude.com/docs/en/whats-new/2026-w34)

[​](https://code.claude.com/docs/en/whats-new#week-33)

Week 33

v2.1.225–v2.1.233

August 10–14, 2026

**Auto-continue after a usage limit on Desktop**: when you hit your session limit in Claude Code Desktop, check **Auto-continue when limits reset** on the limit card and the app retries the interrupted turn once the limit resets.Also this week: **fork mode** is on by default in interactive sessions, so Claude can hand a side task to a subagent that inherits the full conversation; **GitLab** merge request URLs work with `--worktree` and the `claude agents` view, and marketplaces clone bare `gitlab.com` URLs; and typing **`@`** in the prompt mentions another Claude session by name.[Read the Week 33 digest →](https://code.claude.com/docs/en/whats-new/2026-w33)

[​](https://code.claude.com/docs/en/whats-new#week-32)

Week 32

v2.1.220–v2.1.224

August 3–7, 2026

**Cross-session messaging**: on macOS and Linux, your Claude Code sessions can now message each other, so Claude passes a finding or a decision from one session to another instead of you re-explaining it.Also this week: **self-hosted environments** run Claude Code cloud sessions on infrastructure your organization operates, in public beta on Team and Enterprise plans; **auto mode** becomes the default permission mode for new sessions on Pro, Max, and Team plans starting August 14; and the **VS Code extension** gets Focus view.[Read the Week 32 digest →](https://code.claude.com/docs/en/whats-new/2026-w32)

[​](https://code.claude.com/docs/en/whats-new#week-30)

Week 30

v2.1.214–v2.1.219

July 20–24, 2026

**Claude Opus 5**: the new default Opus model in Claude Code, with a 1M-token context window and fast mode at $10/$50 per MTok.Also this week: **Claude Code Desktop** opens an iOS Simulator pane in public beta so Claude can run your app and tap through it while you watch; the **Claude Security plugin** runs a multi-agent vulnerability scan of your codebase and turns the findings you pick into patches you apply yourself; and **`/code-review`** runs as a background subagent.[Read the Week 30 digest →](https://code.claude.com/docs/en/whats-new/2026-w30)

[​](https://code.claude.com/docs/en/whats-new#week-29)

Week 29

v2.1.207–v2.1.212

July 13–17, 2026

**Artifacts call your MCP connectors**: a published artifact can pull live data and take actions through each viewer’s own MCP connectors when they open the page, and this week also adds public sharing links, editor roles on Team and Enterprise, and artifacts created from Claude Tag sessions.Also this week: **screen reader mode** replaces the visual terminal interface with plain, linear text for screen readers such as VoiceOver and NVDA; **`/fork`** copies your conversation into a new background session while you keep working; and **auto mode** no longer needs an opt-in variable on Amazon Bedrock, Google Cloud’s Agent Platform, and Microsoft Foundry.[Read the Week 29 digest →](https://code.claude.com/docs/en/whats-new/2026-w29)

[​](https://code.claude.com/docs/en/whats-new#week-28)

Week 28

codex
Now scraping and checking key candidate pages' dates and content.
exec
/bin/bash -lc 'firecrawl scrape -u "https://martinfowler.com/rachels-ramblings/citizens-agents-experts.html" --format markdown -o /tmp/mf_citizens.md >/dev/null 2>&1; echo 1; firecrawl scrape -u "https://martinfowler.com/rachels-ramblings/code-review.html" --format markdown -o /tmp/mf_codereview.md >/dev/null 2>&1; echo 2; firecrawl scrape -u "https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html" --format markdown -o /tmp/mf_data.md >/dev/null 2>&1; echo 3; firecrawl scrape -u "https://a16z.com/can-agents-use-a-computer-yet-weve-got-the-data/" --format markdown -o /tmp/a16z.md >/dev/null 2>&1; echo 4' in /root/note-worker
 succeeded in 5850ms:
1
2
3
4

exec
/bin/bash -lc 'for f in mf_citizens mf_codereview mf_data a16z; do echo "==== $f ===="; rg -n "2026|author|By |date|Date|published" /tmp/$f.md | head -12; done' in /root/note-worker
 succeeded in 0ms:
==== mf_citizens ====
88:19 August 2026
==== mf_codereview ====
88:02 September 2026
126:And if we’re reviewing code for formatting, linting, known security problems or things that can be deterministically tested, automate them. We really shouldn’t still be arguing about whitespace in 2026.
==== mf_data ====
136:27 August 2026
149:version-controlled schema migrations. He has been an author on five books on
241:when a date falls on a public holiday, or when a price seems too low. That
267:data must be accurate, fresh, and validated before the agent ever sees it.
308:looks off, when a date makes no sense, or when a price seems wrong.
318:current price of Product _X_. Yesterday, the price was updated from
331:A human sales rep would have paused: “Wait, didn't we update this
335:this isn't a rare edge case. In the 2026 [State\\
336:of Data Integrity and AI Readiness](https://www.lebow.drexel.edu/sites/default/files/2026-01/lebow-precisely-state-data-integrity-ai-readiness-2026.pdf) report, Precisely and Drexel
341:of the pricing agent, sure of itself and wrong. A separate [KPMG Global AI Pulse](https://kpmg.com/xx/en/media/press-releases/2026/06/growing-adoption-signals-progress-as-cost-visibility-and-accountability-drive-ai-value.html) survey of 2,145 leaders points the
426:nightly batch updates aren't enough when an agent answers in real time.
430:- Quality gates validate contracts in CI/CD, blocking deployments when
==== a16z ====
rg: /tmp/a16z.md: IO error for operation on /tmp/a16z.md: No such file or directory (os error 2)

exec
/bin/bash -lc "sed -n '80,180p' /tmp/mf_codereview.md" in /root/note-worker
 succeeded in 0ms:
[![Photo of Rachel Laycock](https://martinfowler.com/rachels-ramblings/rachel.jpg)](https://www.linkedin.com/in/rachellaycock/)

[Rachel Laycock](https://www.linkedin.com/in/rachellaycock/)

I'm Rachel Laycock, CTO at Thoughtworks. I'm endlessly curious about how technology is changing the way we build software, lead teams and run businesses. This is where I capture ideas before they're fully formed, challenge my own thinking and occasionally wander off on interesting tangents.

[![](https://martinfowler.com/rachels-ramblings/card.png)](https://martinfowler.com/rachels-ramblings/)

02 September 2026

**TL;DR**

_Or, perhaps the problem isn't that AI has broken code review, maybe it’s that we've been using code review to solve the wrong problems_

I was on a panel recently with Brian Houck from DX at Code Remix, hosted by Moderne. It was one of the more interesting panels I’ve done, largely because we disagreed. As my colleague Martin Fowler says, panels are much more interesting when people disagree and both sides have a good argument. Brian and I definitely did.

Brian has since written a thoughtful piece called [_What are code reviews even for?_](https://newsletter.getdx.com/p/what-are-code-reviews-even-for) He is clearly passionate about his position, and I am passionate enough about mine that I’m writing this response. To be clear, I think we mostly want the same things. I just don’t think code review is the best way to get them. Brian is lovely, by the way, and encouraged me to write this. But I’d be lying if I said I didn’t want you to think I’m right by the end :)

So what were we disagreeing about?

AI is producing more code than humans can realistically review. Brian cites some pretty striking numbers: at Meta, significant lines of code per human-landed diff reportedly increased 106% in a year, while DX’s own data shows median pull request size increasing 64%.

His concern, which I share, is that simply automating code review away risks losing all the other things we use it for. Code review isn’t just about finding bugs. It’s how teams share knowledge, teach junior engineers, build collective ownership and spread architectural understanding.

My question is: **why are we waiting until code review to do all of those things?**

I’ve never particularly liked pull requests as the centre of the software development process. Not because engineers shouldn’t look at each other’s code, but because I’ve always struggled with the idea that we should build something, finish it, package it up, throw it over to somebody else and _then_ have the important conversation about whether we built the right thing in the right way.

And don’t even get me started on merge conflicts. I’ve lost too many hours of my life.

## **Shift the judgment left**

One of the principles I learned very early at Thoughtworks was to shorten feedback loops. If feedback is valuable, don’t remove it. Move it closer to the decision it is informing.

Take the things we say code review gives us.

If we want to **explore alternative solutions**, I’d rather do that before implementing one of them.

If we want **knowledge transfer**, pair. Sitting next to someone, physically or virtually, while they reason through a problem teaches you far more than reading their completed solution afterwards.

If we want **junior engineers to learn how experienced engineers think**, let them work with experienced engineers while they’re thinking. Pairing comes to mind again here, but teams could also do design sessions collectively with a whiteboard before they write (or instruct the agent to write) anything.

If we want **collective ownership**, organise teams so people actually build and operate software collectively rather than relying on a pull request to tell everyone what somebody else has already built. For this again use pairing, mob programming, or team design sessions around whiteboard.

If we want **architectural alignment**, design together (I won’t repeat myself about pairing and team design sessions, oh wait…) and then encode the important constraints as fitness functions.

And if we’re reviewing code for formatting, linting, known security problems or things that can be deterministically tested, automate them. We really shouldn’t still be arguing about whitespace in 2026.

Pair programming, trunk-based development, automated testing, static analysis, fitness functions and security scanning all move feedback earlier. Increasingly, agents can participate in those loops too, challenging designs, testing assumptions and continuously verifying what is being built, but the real thinking is coming from experienced humans and if we want that experience to benefit the whole team then we have to act like one much earlier than code review.

## **Review by exception**

None of this means nobody ever reviews code. There are absolutely changes where I want another experienced human looking. An example would be a fundamental architectural change. Assuming we did a design session as a wider team, we might want to review the code as a team or agree it was implemented right, or discuss if we want to change anything. Other examples could be something crossing a sensitive security boundary, a change with a huge blast radius, an unfamiliar part of a critical system or simply something where the team says, “I’m not confident about this.”

Those are exactly the places where human judgment is valuable, but that’s very different from requiring a human to inspect every change because that’s the ceremony we’ve historically used to create confidence.

And we know now it’s not viable to continue down this path, hence why code review keeps coming up as an issue or a blocker. If an agent can produce ten times the code but every line eventually queues up waiting for a senior engineer to inspect it, we haven’t created a ten-times engineering organisation, we’ve created a big backlog and a new bottleneck.

And I don’t think the answer is an AI agent pretending to be the human reviewer so we can preserve exactly the same process at higher speed. That’s automating the ceremony rather than questioning why the ceremony exists.

There is one thing I do worry about in Brian’s argument, though. He talks about teams accumulating cognitive and intent debt: software grows while the humans responsible for it understand less and less about why it works the way it does. I think that’s a very real problem. I just don’t think mandatory pull requests are a particularly strong defence against it.

If agents are going to produce substantially more of the implementation, we need to be much more deliberate about maintaining human understanding through collaborative design, pairing, good boundaries, executable architecture, shared operational responsibility and probably some practices we haven’t invented yet.

**We need engineers to understand systems, not diffs.**

Perhaps that’s what AI is exposing. We’ve spent years loading an extraordinary number of responsibilities onto the humble code review: quality gate, security check, architecture review, mentoring mechanism, knowledge-sharing system, ownership model.

It worked, sort of, while humans could only produce code so quickly. That constraint is disappearing. So perhaps the question isn’t how we get the code reviewed faster. Perhaps it’s why we’re waiting until code review to have all the important conversations in the first place.

latest post (Sep 02):

[Maybe We Shouldn't Be Reviewing All This Code](https://martinfowler.com/rachels-ramblings/code-review.html)

previous post:

[Citizens Build, Agents Execute, Experts Govern](https://martinfowler.com/rachels-ramblings/citizens-agents-experts.html)

[![](https://martinfowler.com/rachels-ramblings/card.png)](https://martinfowler.com/rachels-ramblings/)

[All Posts](https://martinfowler.com/rachels-ramblings/)

## Topics

[Architecture](https://martinfowler.com/architecture)

[Refactoring](https://refactoring.com/)

[Agile](https://martinfowler.com/agile.html)

[Delivery](https://martinfowler.com/delivery.html)

[Microservices](https://martinfowler.com/microservices)

[Data](https://martinfowler.com/data)

[Testing](https://martinfowler.com/testing)

[DSL](https://martinfowler.com/dsl.html)

## about me

exec
/bin/bash -lc "sed -n '80,160p' /tmp/mf_data.md" in /root/note-worker
 succeeded in 0ms:
- [Top](https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html#top)
- [The consumers of your data are changing](https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html#TheConsumersOfYourDataAreChanging)
- [What “AI-ready” has to mean now](https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html#Whatai-readyHasToMeanNow)
- [Data Contracts and Quality: Agents Can't Smell Bad Data](https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html#data-contracts)
  - [Agents treat every value as truth](https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html#AgentsTreatEveryValueAsTruth)
  - [Schema is law: data contracts as code](https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html#SchemaIsLawDataContractsAsCode)
  - [The quarantine pattern](https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html#TheQuarantinePattern)
  - [Medallion architecture for agents](https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html#MedallionArchitectureForAgents)
  - [The same rules for unstructured data](https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html#TheSameRulesForUnstructuredData)
  - [Confidence-threshold routing](https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html#Confidence-thresholdRouting)
  - [Where to start](https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html#WhereToStart)
- [Traceability and Governance: Auditing Autonomous Agents](https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html#traceability)
  - [The audit gap](https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html#TheAuditGap)
  - [Agentic lineage](https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html#AgenticLineage)
  - [The regulatory teeth are real](https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html#TheRegulatoryTeethAreReal)
  - [Staged autonomy](https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html#StagedAutonomy)
  - [Delegated access and just-in-time credentials](https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html#DelegatedAccessAndJust-in-timeCredentials)
  - [Where to start](https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html#WhereToStart)
- [The Context Layer: Teaching Agents What Your Data Means](https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html#context-layer)
  - [Your agent doesn't know what “revenue” means](https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html#YourAgentDoesntKnowWhatrevenueMeans)
  - [What the context layer is](https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html#WhatTheContextLayerIs)
  - [Metrics as code](https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html#MetricsAsCode)
  - [Same question, very different SQL](https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html#SameQuestionVeryDifferentSql)
  - [How agents use it](https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html#HowAgentsUseIt)
  - [Where to start](https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html#WhereToStart)
  - [Traversing the domain model: knowledge graphs](https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html#TraversingTheDomainModelKnowledgeGraphs)
- [From Searchable to Actionable: Agent-Ready Data Access](https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html#actionable)
  - [Your agent can read, but it can't act](https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html#YourAgentCanReadButItCantAct)
  - [The data access spectrum](https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html#TheDataAccessSpectrum)
  - [Three primitives, one protocol](https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html#ThreePrimitivesOneProtocol)
  - [Antipattern: naive API-to-MCP conversion](https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html#AntipatternNaiveApi-to-mcpConversion)
  - [What a capability declares](https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html#WhatACapabilityDeclares)
  - [Retrieved text informs, it never gates](https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html#RetrievedTextInformsItNeverGates)
  - [End to end: the PO payment scenario](https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html#EndToEndThePoPaymentScenario)
  - [Where to start](https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html#WhereToStart)
- [The AI-ready data stack](https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html#TheAi-readyDataStack)
- [Who owns all this?](https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html#WhoOwnsAllThis)
- [Where do you stand?](https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html#WhereDoYouStand)
- [Four things to start on](https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html#FourThingsToStartOn)

### Sidebars

- [Explainer: the words people use for semantic layers](https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html#ExplainerTheWordsPeopleUseForSemanticLayers)

# Making Your Data Ready for Agentic AI

_For thirty years we built data systems for human analysts, who_
_supply the context, judgment, and skepticism to work around data that's_
_incomplete or wrong. Autonomous agents supply none of that. They act on_
_whatever they're handed, confidently. For data to be AI-ready we need to_
_build a series of layers: a data foundation that makes data trusted, a context_
_layer to apply proper meaning, and an access layer that supports and controls_
_how agents operate on that data. While doing this we need continuous_
_attention to observability that ensures the data is properly governed and we_
_have an auditable trace of its use in decision-making._

27 August 2026

* * *

[![Photo of Pramod Sadalage](https://martinfowler.com/articles/making-data-ready-for-agentic-ai/pramod.jpg)](https://sadalage.com/)

[Pramod Sadalage](https://sadalage.com/)

Pramod is a Distinguished Engineer at Thoughtworks leading
the Data Engineering and Architecture service for North America, where he
helps clients with particularly challenging data needs, which require new
technologies and techniques. In the early 00’s he developed techniques to
allow relational databases to be designed in an evolutionary manner based on
version-controlled schema migrations. He has been an author on five books on
software development, including “Software Architecture: The Hard Parts” and
“Refactoring Databases”

[![Photo of Prem Chandrasekaran](https://martinfowler.com/articles/making-data-ready-for-agentic-ai/prem.jpg)](https://premonition.dev/)

[Prem Chandrasekaran](https://premonition.dev/)

Premanand (Prem) Chandrasekaran is a Market Tech Director at
Thoughtworks, where he leads technology strategy and delivery across a
portfolio of clients and guides teams through complex, high-stakes
engineering decisions. He stays deliberately hands-on, designing and building

exec
/bin/bash -lc 'firecrawl research --help 2>&1 | head -40' in /root/note-worker
 succeeded in 121ms:
Usage: firecrawl research [options] [command]

Research arXiv papers and GitHub history using Firecrawl

Options:
  -h, --help                             display help for command

Commands:
  search-papers [options] <query>        Primary entry point for finding arXiv papers by topic. Semantic (HyDE) search over arXiv abstracts; returns ranked papers with arXiv id, title, and abstract. The query should be a natural-language description of what you want. Run several distinct framings of the question rather than one query. Returns up to k results (default 40).
  inspect-paper [options] <paperId>      Fetch canonical metadata for one paper by primaryId or canonical paperId. Use this after search/related results when you need the full title, abstract, authors, categories, source ids, and dates rendered as markdown.
  related-papers [options] <seedIds...>  Expand from anchor papers you have already found, via the citation graph, ranked and filtered to a natural-language intent. Pass arXiv ids of your strongest hits as seed ids. Modes: similar, citers, references. This reaches relevant papers that plain search misses. A similar call already runs a deep multi-round expansion internally.
  read-paper [options] <paperId>         Read the most relevant in-body full-text passages of one specific paper for a question. Use this to verify whether a candidate actually satisfies a constraint before you include or reject it. Returns the best-matching passages, or a notice if the paper full text is unavailable.
  search-github [options] <query>        Search GitHub issue/PR history and repository readmes. Returns ranked matches with repo, url, a short snippet, and when available the full matched content in markdown.
  help [command]                         display help for command

Examples:
  $ firecrawl research search-papers "diffusion image synthesis" --limit 20
  $ firecrawl research inspect-paper arxiv:1706.03762
  $ firecrawl research related-papers arxiv:1706.03762 --intent "efficient transformers"
  $ firecrawl research read-paper arxiv:1706.03762 --question "What is the attention mechanism?"
  $ firecrawl research search-github "foundationdb queue worker shutdown" --limit 10


exec
/bin/bash -lc 'firecrawl research search-papers --help 2>&1 | head -30; echo ----; firecrawl research search-github --help 2>&1 | head -30' in /root/note-worker
 succeeded in 328ms:
Usage: firecrawl research search-papers [options] <query>

Primary entry point for finding arXiv papers by topic. Semantic (HyDE) search
over arXiv abstracts; returns ranked papers with arXiv id, title, and abstract.
The query should be a natural-language description of what you want. Run several
distinct framings of the question rather than one query. Returns up to k results
(default 40).

Arguments:
  query                      Natural-language description of the papers to find

Options:
  --limit <number>           Number of results to return (default: 40)
  --authors <authors>        Comma-separated author substring filter(s); all
                             must match case-insensitively
  --categories <categories>  Comma-separated arXiv category filter(s), e.g.
                             cs.LG,cs.IR; all must match
  --from <date>              Inclusive lower bound on created/updated date
                             (YYYY-MM-DD)
  --to <date>                Inclusive upper bound on created/updated date
                             (YYYY-MM-DD)
  -k, --api-key <key>        Firecrawl API key (overrides global --api-key)
  --api-url <url>            API URL (overrides global --api-url)
  -o, --output <path>        Output file path (default: stdout)
  --json                     Output as compact JSON (default: false)
  --pretty                   Pretty print JSON output (default: false)
  -h, --help                 display help for command
----
Usage: firecrawl research search-github [options] <query>

Search GitHub issue/PR history and repository readmes. Returns ranked matches
with repo, url, a short snippet, and when available the full matched content in
markdown.

Arguments:
  query                GitHub history/readme search query

Options:
  --limit <number>     Number of results to return (max: 100)
  -k, --api-key <key>  Firecrawl API key (overrides global --api-key)
  --api-url <url>      API URL (overrides global --api-url)
  -o, --output <path>  Output file path (default: stdout)
  --json               Output as compact JSON (default: false)
  --pretty             Pretty print JSON output (default: false)
  -h, --help           display help for command

codex
Now running arXiv and GitHub-targeted Firecrawl research queries, date-bounded to the window.
exec
/bin/bash -lc 'firecrawl research search-papers "harness engineering for coding agents: scaffolding, constraints, tool design, guardrails and feedback for AI software engineering agents" --categories cs.SE,cs.AI --from 2026-08-24 --to 2026-09-07 --limit 15 --pretty 2>&1 | tail -120 > /tmp/ar1.txt; echo ar1; firecrawl research search-papers "context engineering for LLM agents: context window management, compaction, memory, progressive disclosure of instructions" --categories cs.SE,cs.AI,cs.CL --from 2026-08-24 --to 2026-09-07 --limit 15 --pretty 2>&1 | tail -120 > /tmp/ar2.txt; echo ar2' in /root/note-worker
 succeeded in 7850ms:
ar1
ar2

exec
/bin/bash -lc 'head -120 /tmp/ar1.txt; echo ====2====; head -120 /tmp/ar2.txt' in /root/note-worker
 succeeded in 0ms:
{
  "success": true,
  "partial": false,
  "results": [
    {
      "paperId": "749899062248531033",
      "primaryId": "arxiv:2609.00050",
      "ids": {
        "arxiv": [
          "2609.00050"
        ]
      },
      "title": "Towards Agentic Cloud Engineering: Graph and Loop Engineering with a Zero-Trust Agent Harness",
      "abstract": "Agentic AI is enabling cloud-based workflows in which autonomous agents reason over operational state, invoke authorized tools, modify software and infrastructure, deploy services, verify execution outcomes, and adapt across long-horizon, multistep tasks. Engineering such workflows requires explicit mechanisms for workflow progression, constrained execution, failure recovery, and verifiable completion. We present Agentic Cloud Workflow Engineering, an agentic AI framework that transforms natural-language agentic cloud-engineering tasks into validated code repositories and verified operational cloud deployments for automating cloud-based agentic workflows. The framework separates three complementary concerns: graph engineering specifies long-horizon workflow progression and verification-dependent transitions; loop engineering provides bounded diagnosis, repair or re-planning, retry, and re-verification; and agent harness engineering enforces zero-trust execution through identity, authorization, policy-scoped capabilities, isolation, and runtime safeguards. Workflow progression and completion require machine-checkable repository, deployment, and runtime evidence, with recovery constrained by explicit operational bounds and termination criteria. We instantiate the framework on Google Cloud and evaluate repository completeness, controlled execution, evidence-gated progression, operational deployment, and bounded recovery. Experimental results show that executions terminate with either a verified operational cloud deployment or an auditable terminal failure under bounded recovery. The framework provides a unified engineering architecture for cloud-based workflows spanning Agentic DevOps, Agentic CloudOps, Agentic SRE/AIOps, Agentic SecOps, Agentic DataOps, Agentic MLOps/LLMOps, AgentOps, Agentic RAG/GraphRAG, and related cloud-engineering domains.",
      "score": 0.9284088005554476
    },
    {
      "paperId": "1476775061132027688",
      "primaryId": "arxiv:2609.04167",
      "ids": {
        "arxiv": [
          "2609.04167"
        ]
      },
      "title": "SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents",
      "abstract": "Repository-level software engineering benchmarks have significantly advanced the evaluation of coding agents, but existing benchmarks primarily measure whether generated patches pass functional tests and overlook review-derived acceptance constraints (review constraints) that often influence whether a patch is acceptable in real-world software development. We introduce SWE-Gate, a repository-level benchmark for software engineering agents that explicitly evaluates review constraint compliance alongside functional correctness. SWE-Gate derives review constraints from real pull request review comments and synthesizes repository-level repair instances around these constraints. Each instance provides separate functional and constraint tests, together with non-compliant and gold patches, enabling explicit separation between issue resolution capability and review constraint compliance. We construct SWE-Gate with 303 repository-level repair instances spanning 75 open-source Python repositories across diverse software domains. Experiments with four LLM backends spanning different capability levels under a common coding-agent scaffold reveal a substantial gap between functional success and success under the complete repair specification: among 644 repairs that pass the functional tests, 221 fail to satisfy the provided review constraints. These findings show that functional-only evaluation overestimates agents' ability to satisfy the full requirements of repository-level repair tasks. The replication package including code, data, and experimental results is available at https://github.com/DeepSoftwareAnalytics/SWE-Gate.",
      "score": 0.8566204956353467
    }
  ]
}
====2====
{
  "success": true,
  "partial": false,
  "results": []
}

exec
/bin/bash -lc 'firecrawl research inspect-paper arxiv:2609.00050 --pretty 2>&1 | head -60 > /tmp/p1.txt; echo p1; firecrawl research inspect-paper arxiv:2609.04167 --pretty 2>&1 | head -60 > /tmp/p2.txt; echo p2; firecrawl research search-papers "multi-agent systems for software engineering: coordination, orchestration, sandboxing, shared repositories, delegation and review between coding agents" --categories cs.SE,cs.AI --from 2026-08-24 --to 2026-09-07 --limit 15 --pretty 2>&1 | tail -150 > /tmp/ar3.txt; echo ar3' in /root/note-worker
 succeeded in 5501ms:
p1
p2
ar3

exec
/bin/bash -lc 'echo ==P1==; head -80 /tmp/p1.txt; echo ==P2==; head -80 /tmp/p2.txt; echo ==AR3==; head -160 /tmp/ar3.txt' in /root/note-worker
 succeeded in 0ms:
==P1==
{
  "paper": {
    "abstract": "Agentic AI is enabling cloud-based workflows in which autonomous agents reason over operational state, invoke authorized tools, modify software and infrastructure, deploy services, verify execution outcomes, and adapt across long-horizon, multistep tasks. Engineering such workflows requires explicit mechanisms for workflow progression, constrained execution, failure recovery, and verifiable completion. We present Agentic Cloud Workflow Engineering, an agentic AI framework that transforms natural-language agentic cloud-engineering tasks into validated code repositories and verified operational cloud deployments for automating cloud-based agentic workflows. The framework separates three complementary concerns: graph engineering specifies long-horizon workflow progression and verification-dependent transitions; loop engineering provides bounded diagnosis, repair or re-planning, retry, and re-verification; and agent harness engineering enforces zero-trust execution through identity, authorization, policy-scoped capabilities, isolation, and runtime safeguards. Workflow progression and completion require machine-checkable repository, deployment, and runtime evidence, with recovery constrained by explicit operational bounds and termination criteria. We instantiate the framework on Google Cloud and evaluate repository completeness, controlled execution, evidence-gated progression, operational deployment, and bounded recovery. Experimental results show that executions terminate with either a verified operational cloud deployment or an auditable terminal failure under bounded recovery. The framework provides a unified engineering architecture for cloud-based workflows spanning Agentic DevOps, Agentic CloudOps, Agentic SRE/AIOps, Agentic SecOps, Agentic DataOps, Agentic MLOps/LLMOps, AgentOps, Agentic RAG/GraphRAG, and related cloud-engineering domains.",
    "authors": "Sagar Srinivas Sakhinana, Venkataramana Runkana",
    "categories": [
      "cs.SE",
      "cs.AI",
      "cs.LG"
    ],
    "createdDate": "2026-08-30",
    "ids": {
      "arxiv": [
        "2609.00050"
      ]
    },
    "paperId": "749899062248531033",
    "title": "Towards Agentic Cloud Engineering: Graph and Loop Engineering with a Zero-Trust Agent Harness",
    "updateDate": "2026-09-02"
  },
  "success": true
}
==P2==
{
  "paper": {
    "abstract": "Repository-level software engineering benchmarks have significantly advanced the evaluation of coding agents, but existing benchmarks primarily measure whether generated patches pass functional tests and overlook review-derived acceptance constraints (review constraints) that often influence whether a patch is acceptable in real-world software development. We introduce SWE-Gate, a repository-level benchmark for software engineering agents that explicitly evaluates review constraint compliance alongside functional correctness. SWE-Gate derives review constraints from real pull request review comments and synthesizes repository-level repair instances around these constraints. Each instance provides separate functional and constraint tests, together with non-compliant and gold patches, enabling explicit separation between issue resolution capability and review constraint compliance. We construct SWE-Gate with 303 repository-level repair instances spanning 75 open-source Python repositories across diverse software domains. Experiments with four LLM backends spanning different capability levels under a common coding-agent scaffold reveal a substantial gap between functional success and success under the complete repair specification: among 644 repairs that pass the functional tests, 221 fail to satisfy the provided review constraints. These findings show that functional-only evaluation overestimates agents' ability to satisfy the full requirements of repository-level repair tasks. The replication package including code, data, and experimental results is available at https://github.com/DeepSoftwareAnalytics/SWE-Gate.",
    "authors": "Xin He, Yanlin Wang, Mingwei Liu, Jiachi Chen, Hongyu Zhang, Guanbin Li",
    "categories": [
      "cs.SE",
      "cs.AI"
    ],
    "createdDate": "2026-09-03",
    "ids": {
      "arxiv": [
        "2609.04167"
      ]
    },
    "paperId": "1476775061132027688",
    "title": "SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents",
    "updateDate": "2026-09-04"
  },
  "success": true
}
==AR3==
{
  "success": true,
  "partial": false,
  "results": [
    {
      "paperId": "5792245377674415119",
      "primaryId": "arxiv:2608.23740",
      "ids": {
        "arxiv": [
          "2608.23740"
        ]
      },
      "title": "AgentRoom: Concurrent Multi-Agent Coding in a CRDT-Backed Shared Workspace",
      "abstract": "Concurrent multi-agent coding promises division of labor across modules, robustness through redundancy, and parallel exploration at the natural granularity of multi-file projects. Realtime collaborative editing protocols solve this coordination problem for human teams via Conflict-free Replicated Data Types (CRDTs), but the LLMs underneath generate one token at a time and existing multi-agent coding systems inherit this serial limit: they either sequence agents through phase handoffs or pool independent samples without coordination, and a single agent abandons up to half of hard tasks with a one-file stub-and-exit. AgentRoom is a realtime collaborative editing protocol for concurrent coding agents. Its runtime layer exposes file-level claim, status, and broadcast as MCP tools on a CRDT-merged shared filesystem. Five frontier coding-CLI models ran four backend coding tasks, with cross-language checks in Python DevBench and Rust+axum. For CLI-stable models, AgentRoom with 2 agents abandons fewer tasks than Solo and has less run-to-run variation. At matched-compute, one positive mean LLM-judge contrast puts AgentRoom over parallel-merge. The other contrast, a bundle probe, puts full AgentRoom above each partial case: an ordering rather than a percentage split. Coordination, not parallelism or CRDT-merge, bears the load.",
      "score": 0.9232608643662287
    },
    {
      "paperId": "2524204416757563793",
      "primaryId": "arxiv:2608.25241",
      "ids": {
        "arxiv": [
          "2608.25241"
        ]
      },
      "title": "A Few Pages of Markdown: Committed AI Configuration and Lower Quality Cost after Coding-Agent Adoption",
      "abstract": "Coding agents increase development velocity but also technical debt. Prior work reports only average effects across adopters, hiding wide differences between teams. We introduce RAMP (Repository AI Maturity Profile), a four-level cumulative maturity model grounded in version-controlled artifacts that teams commit to configure AI tools. RAMP runs from behavioral rules and coding standards through named agent definitions to multi-agent orchestration, with observed practice concentrated in the first three levels. Across 441 repositories the levels behave as a cumulative scale, and independent human annotation reproduces RAMP's repository-level labels on 97% of a held-out sample. Adoption is cumulative, forward-only, and set-and-forget: 73.8% of artifacts are committed once and never modified. Re-estimating an existing agent-adoption panel within each stratum, agents accelerate development regardless of maturity (28-38% more commits), but quality diverges: among agent-first repositories, where the contrast is identified, those without committed AI configuration show roughly twice the increase in cognitive complexity (+53% versus +27%) and 1.7x the increase in static-analysis warnings. Because maturity is observational, correlated engineering discipline or model capability may explain part of the gap; we present these findings as hypothesis-generating and release RAMP as a reusable instrument.",
      "score": 0.8438951025545426
    }
  ]
}

exec
/bin/bash -lc 'for id in 2608.23740 2608.25241 2608.23552; do firecrawl research inspect-paper arxiv:$id --pretty 2>&1 | python3 -c "
import sys,json
try:
    d=json.load(sys.stdin)
    p=d.get('"'paper',{})
    print(p.get('primaryId') or p.get('ids',{}).get('arxiv'), '|', p.get('createdDate'),'|',p.get('title'),'|',p.get('authors'))
except Exception as e:
    print('ERR',e)
\"; done" in /root/note-worker
 succeeded in 2832ms:
['2608.23740'] | 2026-08-24 | AgentRoom: Concurrent Multi-Agent Coding in a CRDT-Backed Shared Workspace | Seonglae Cho, Donghyun Lee
['2608.25241'] | 2026-08-26 | A Few Pages of Markdown: Committed AI Configuration and Lower Quality Cost after Coding-Agent Adoption | Yegor Denisov-Blanch, Shyam Agarwal, Pavel Azaletskiy, Hao He, Rylan Schaeffer, Brando Miranda, Bogdan Vasilescu, Sanmi Koyejo
['2608.23552'] | 2026-08-24 | Prime Agent: A Self-Improving RLM Harness | Seth Karten, Alex L. Zhang, Kevin Thomas, Sebastian Müller, Elie Bakouch, Daniel Auras, Mika Senghaas, Fares Obeid, Konstantin Dunas, Johannes Hagemann, Sami Jaghouar

exec
/bin/bash -lc 'firecrawl research search-papers "evaluating coding agents with AI code review, mutation testing, structural test coverage and fitness functions rather than only functional tests" --categories cs.SE --from 2026-08-24 --to 2026-09-07 --limit 15 --pretty 2>&1 | tail -160 > /tmp/ar4.txt; echo ar4; firecrawl research search-papers "how developers adopt AI coding agents: instruction files like AGENTS.md, team workflows, productivity and code quality impact, human-agent collaboration" --categories cs.SE,cs.HC --from 2026-08-24 --to 2026-09-07 --limit 15 --pretty 2>&1 | tail -160 > /tmp/ar5.txt; echo ar5; firecrawl research search-papers "long context LLM agents memory compaction summarization retrieval context window limits inference" --categories cs.CL,cs.LG --from 2026-08-24 --to 2026-09-07 --limit 15 --pretty 2>&1 | tail -160 > /tmp/ar6.txt; echo ar6' in /root/note-worker
 succeeded in 10522ms:
ar4
ar5
ar6

exec
/bin/bash -lc 'head -200 /tmp/ar4.txt; echo ====AR5====; head -180 /tmp/ar5.txt; echo ====AR6====; head -180 /tmp/ar6.txt' in /root/note-worker
 succeeded in 0ms:
{
  "success": true,
  "partial": false,
  "results": [
    {
      "paperId": "1476775061132027688",
      "primaryId": "arxiv:2609.04167",
      "ids": {
        "arxiv": [
          "2609.04167"
        ]
      },
      "title": "SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents",
      "abstract": "Repository-level software engineering benchmarks have significantly advanced the evaluation of coding agents, but existing benchmarks primarily measure whether generated patches pass functional tests and overlook review-derived acceptance constraints (review constraints) that often influence whether a patch is acceptable in real-world software development. We introduce SWE-Gate, a repository-level benchmark for software engineering agents that explicitly evaluates review constraint compliance alongside functional correctness. SWE-Gate derives review constraints from real pull request review comments and synthesizes repository-level repair instances around these constraints. Each instance provides separate functional and constraint tests, together with non-compliant and gold patches, enabling explicit separation between issue resolution capability and review constraint compliance. We construct SWE-Gate with 303 repository-level repair instances spanning 75 open-source Python repositories across diverse software domains. Experiments with four LLM backends spanning different capability levels under a common coding-agent scaffold reveal a substantial gap between functional success and success under the complete repair specification: among 644 repairs that pass the functional tests, 221 fail to satisfy the provided review constraints. These findings show that functional-only evaluation overestimates agents' ability to satisfy the full requirements of repository-level repair tasks. The replication package including code, data, and experimental results is available at https://github.com/DeepSoftwareAnalytics/SWE-Gate.",
      "score": 0.8519528019683106
    },
    {
      "paperId": "2736335070356773876",
      "primaryId": "arxiv:2609.01865",
      "ids": {
        "arxiv": [
          "2609.01865"
        ]
      },
      "title": "ExecRetrieval: Measuring the Functional-Correctness Gap in Code-Embedding Retrieval",
      "abstract": "Embedding-based code retrieval is a core component of coding agents and retrieval-augmented code generation, where retrieving correct code matters more than retrieving lexically similar code. Existing code-retrieval benchmarks do not plant controlled, execution-verified single-edit variants of each query's canonical implementation in the search pool, leaving the question of whether embeddings can functionally discriminate correct from near-clone-but-incorrect code unanswered in a retrieval setting. Resolving this requires a benchmark whose search pool itself contains the relevant counterfactuals -- execution-verified buggy variants near-identical to each canonical -- so that a retriever's rank ordering can be directly tested for functional discrimination rather than topical or identity overlap. We introduce ExecRetrieval, 939 Python tasks each paired with one execution-verified canonical implementation and up to four execution-verified buggy distractors, each generated by a mechanical mutation making a single targeted edit, and evaluate 23 dense embedding configurations plus BM25 under provider-native invocation with paired McNemar tests and query-level bootstrap intervals. With near-clone counterfactuals in the pool, the top hosted system reaches exec@10 = 1.00 but only exec@1 = 0.331; rank-1 misses are paired buggy variants 91.5-99.4% of the time across the four leading systems, and the canonical scores below at least one of its four paired distractors in 67-78% of queries on the leading systems. The full dataset, execution oracle, embedding matrices, environment snapshot, and pairwise statistical tests are released at the URL in Appendix D.",
      "score": 0.7685247834990175
    }
  ]
}
====AR5====
{
  "success": true,
  "partial": false,
  "results": [
    {
      "paperId": "19302178971381701",
      "primaryId": "arxiv:2605.29442",
      "ids": {
        "arxiv": [
          "2605.29442"
        ]
      },
      "title": "How Coding Agents Fail Their Users: A Large-Scale Analysis of Developer-Agent Misalignment in 20,574 Real-World Sessions",
      "abstract": "AI coding agents increasingly act directly within software environments, yet existing analyses of their failures rely on benchmark trajectories that miss how developers actually experience misalignment. We present an observational study of 20,574 coding-agent sessions from 1,639 repositories across IDE and CLI workflows. We operationalize misalignment as a breakdown made visible through developer pushback, and annotate each episode along four axes: form, cause, cost, and resolution. We identify seven recurring forms, spanning how agents read projects, interpret developer intent, follow rules, bound their actions, implement and execute code, and report progress. 90.50% of episodes impose effort and trust costs rather than irreversible system damage, yet 91.49% of visible resolutions still require explicit user correction. Misalignment patterns also differ across IDE and CLI settings, persist across adjacent sessions, and shift over time: while overall rates decline, constraint violations and inaccurate self-reporting grow in share. Our findings inform the design of training, evaluation, and interfaces for keeping coding agents aligned with real developer workflows.",
      "score": 0.77074099629946
    }
  ]
}
====AR6====
{
  "success": true,
  "partial": false,
  "results": []
}

codex
Good paper finds. Now let me scrape Simon Willison's in-range posts and key vendor blog indexes.
exec
/bin/bash -lc 'firecrawl scrape -u https://simonwillison.net/2026/Sep/2/claudes-new-system-prompt/ --format markdown -o /tmp/sw_sysprompt.md >/dev/null 2>&1; echo 1; firecrawl scrape -u https://simonwillison.net/2026/Aug/30/understanding-chatgpt-work/ --format markdown -o /tmp/sw_chatgptwork.md >/dev/null 2>&1; echo 2; firecrawl scrape -u https://simonwillison.net/2026/Sep/5/introducing-gpt-6-astra-for-developers/ --format markdown -o /tmp/sw_astra.md >/dev/null 2>&1; echo 3; firecrawl scrape -u https://www.anthropic.com/engineering --format markdown -o /tmp/antheng.md >/dev/null 2>&1; echo 4; firecrawl scrape -u https://blog.langchain.com/ --format markdown -o /tmp/langchain_idx.md >/dev/null 2>&1; echo 5' in /root/note-worker
 succeeded in 6919ms:
1
2
3
4
5

exec
/bin/bash -lc 'wc -c /tmp/sw_sysprompt.md /tmp/sw_chatgptwork.md /tmp/sw_astra.md /tmp/antheng.md /tmp/langchain_idx.md 2>&1' in /root/note-worker
 succeeded in 0ms:
21277 /tmp/sw_sysprompt.md
20421 /tmp/sw_chatgptwork.md
 3752 /tmp/sw_astra.md
13926 /tmp/antheng.md
17573 /tmp/langchain_idx.md
76949 total

exec
/bin/bash -lc 'echo ==SYS==; head -40 /tmp/sw_sysprompt.md; echo ==ASTRA==; cat /tmp/sw_astra.md | head -40' in /root/note-worker
 succeeded in 0ms:
==SYS==
# [Simon Willison’s Weblog](https://simonwillison.net/)

[Subscribe](https://simonwillison.net/about/#subscribe)

**Sponsored by:** Portnox — Shadow AI is the new shadow IT. On Sept. 10, Forrester Research and Portnox share practical steps to regain AI agent visibility, access management, and policy enforcement. [Register today](https://fandf.co/4y6wlc6)

## Claude’s new system prompt really doesn’t want to reproduce song lyrics

2nd September 2026

Anthropic [publish the system prompts](https://platform.claude.com/docs/en/release-notes/system-prompts/overview) for their Claude consumer applications ( [Claude.ai](https://claude.ai/) and the Claude mobile apps—sadly not for Claude Cowork or Claude Code). I _love_ that they do this, and that they share not just the current prompts but historic changes to their prompts as well.

They used to keep all of the prompts on a single page, but when I checked today I noticed they had re-arranged those prompts into an [index page](https://platform.claude.com/docs/en/release-notes/system-prompts/overview) and then a page per model—here’s the [page for Haiku 4.5](https://platform.claude.com/docs/en/release-notes/system-prompts/claude-haiku-4-5) for example, which has the original prompt from October 15th 2025 and an updated prompt from January 18th 2026.

A neat thing about Anthropic’s [platform.claude.com/docs](https://platform.claude.com/docs/) site is that it’s designed to be usable by LLMs. You can add `.md` to any page to get back the content as Markdown—here’s [the system prompt index page](https://platform.claude.com/docs/en/release-notes/system-prompts/overview.md) and [the Markdown prompts for Fable 5.1](https://platform.claude.com/docs/en/release-notes/system-prompts/claude-fable-5-1.md).

TL;DR: this makes it really easy to diff the prompts.

- [Don’t reproduce song lyrics](https://simonwillison.net/2026/Sep/2/claudes-new-system-prompt/#don-t-reproduce-song-lyrics)
- [Don’t draw copyrighted characters or logos](https://simonwillison.net/2026/Sep/2/claudes-new-system-prompt/#don-t-draw-copyrighted-characters-or-logos)
- [Tweaks to Claude’s answering style](https://simonwillison.net/2026/Sep/2/claudes-new-system-prompt/#tweaks-to-claude-s-answering-style)
- [The missing end\_conversation guidelines](https://simonwillison.net/2026/Sep/2/claudes-new-system-prompt/#the-missing-end-conversation-guidelines)
- [Recommended substance support sites](https://simonwillison.net/2026/Sep/2/claudes-new-system-prompt/#recommended-substance-support-sites)
- [Reliable cutoff date of June 2026](https://simonwillison.net/2026/Sep/2/claudes-new-system-prompt/#reliable-cutoff-date-of-june-2026)
- [How I’m tracking these prompts](https://simonwillison.net/2026/Sep/2/claudes-new-system-prompt/#how-i-m-tracking-these-prompts)

#### Don’t reproduce song lyrics [\#](https://simonwillison.net/2026/Sep/2/claudes-new-system-prompt/\#don-t-reproduce-song-lyrics)

Let’s start with the most interesting difference [between Fable 5 and Fable 5.1](https://github.com/simonw/claude-system-prompts/commit/837a418b5888207b1b11b27d2f5471970da6f99b):

![GitHub diff view of prompts/claude-fable.md showing added lines about song lyrics, reproduced in full below.](https://static.simonwillison.net/static/2026-09-01/IMG_7797.jpeg)

There’s a hefty new section about not reproducing song lyrics:

> `Claude does not reproduce song lyrics, poems, or passages from books and articles, in whole or in part — including the last lines, a chorus or hook, a melody written out note by note, or lines the person pastes in one at a time and describes as their own song. Once Claude has declined such a request in a conversation, it keeps declining narrower or reworded versions of it for the rest of that conversation, and offers to describe or analyze the work instead. Song lyrics and poems first published before 1929 are fine — a Shakespeare sonnet, a Keats ode, the Italian libretto of a Puccini aria — but Claude goes by what it knows of the work's date rather than the person's say-so, and declines when it is unsure.`

I doubt it’s a coincidence that they added this section within days of the news breaking that [Sony Music Publishing and Warner Chappell are suing Anthropic](https://www.theguardian.com/business/2026/aug/31/aanthropic-sued-alleged-theft-songs-ai-train-claude) for training on databases of song lyrics!

#### Don’t draw copyrighted characters or logos [\#](https://simonwillison.net/2026/Sep/2/claudes-new-system-prompt/\#don-t-draw-copyrighted-characters-or-logos)

==ASTRA==
# [Simon Willison’s Weblog](https://simonwillison.net/)

[Subscribe](https://simonwillison.net/about/#subscribe)

**Sponsored by:** Portnox — Shadow AI is the new shadow IT. On Sept. 10, Forrester Research and Portnox share practical steps to regain AI agent visibility, access management, and policy enforcement. [Register today](https://fandf.co/4y6wlc6)

5th September 2026 - Link Blog

**[Introducing GPT-6 Astra for developers](https://www.youtube.com/watch?v=bOC3DisEOfg)** ( [via](https://news.ycombinator.com/item?id=49554643#49575117 "Hacker News comment")) Blink and you'll miss it, but there's a familiar creature at [1m59s](https://www.youtube.com/watch?v=bOC3DisEOfg&t=119):

> Across the board, Astra has more attention to detail, better understanding of the user's prompt, and can build more sophisticated outputs. In particular, it excels at building 3D models. I've seen it make incredible renderings of gardens, shipyards, **animals**, cityscapes, even Dyson spheres.

![astra-video-pelican.webp](https://static.simonwillison.net/static/2026-09-05/astra-video-pelican.webp)

Astra [really](https://simonwillison.net/2026/Sep/5/blender-coding-agents-macos/) does [believe](https://simonwillison.net/2026/Sep/4/astra-pelicans/) in putting a red neckerchief on a pelican riding a bicycle.

Posted [5th September 2026](https://simonwillison.net/2026/Sep/5/) at 11:27 pm

## Recent articles

- [The Pelican comparison grid for Astra is pretty interesting](https://simonwillison.net/2026/Sep/4/astra-pelicans/) \- 4th September 2026
- [OpenAI's rogue agents were caught communicating via public wikis](https://simonwillison.net/2026/Sep/4/rogue-agent-wikis/) \- 4th September 2026
- [Claude's new system prompt really doesn't want to reproduce song lyrics](https://simonwillison.net/2026/Sep/2/claudes-new-system-prompt/) \- 2nd September 2026

This is a **link post** by Simon Willison, posted on [5th September 2026](https://simonwillison.net/2026/Sep/5/).

[ai\\
2,218](https://simonwillison.net/tags/ai/) [openai\\
456](https://simonwillison.net/tags/openai/) [generative-ai\\
1,966](https://simonwillison.net/tags/generative-ai/) [llms\\
1,933](https://simonwillison.net/tags/llms/) [pelican-riding-a-bicycle\\
142](https://simonwillison.net/tags/pelican-riding-a-bicycle/) [gpt-6-astra\\
5](https://simonwillison.net/tags/gpt-6-astra/)

### Monthly briefing

Sponsor me for **$10/month** and get a curated email digest of the month's most important LLM developments.


Pay me to send you less!

exec
/bin/bash -lc "head -30 /tmp/sw_chatgptwork.md; echo ====; sed -n '1,60p' /tmp/antheng.md; echo ====LANGCHAIN====; head -60 /tmp/langchain_idx.md" in /root/note-worker
 succeeded in 0ms:
# [Simon Willison’s Weblog](https://simonwillison.net/)

[Subscribe](https://simonwillison.net/about/#subscribe)

**Sponsored by:** Portnox — Shadow AI is the new shadow IT. On Sept. 10, Forrester Research and Portnox share practical steps to regain AI agent visibility, access management, and policy enforcement. [Register today](https://fandf.co/4y6wlc6)

## Understanding ChatGPT Work

30th August 2026

OpenAI [announced ChatGPT Work](https://openai.com/index/chatgpt-for-your-most-ambitious-work/) on July 9th, and have been furiously iterating on it ever since. It is an extraordinarily confusing and very powerful product. Here’s what I’ve figured out about it so far.

#### ChatGPT Work is actually two products [\#](https://simonwillison.net/2026/Aug/30/understanding-chatgpt-work/\#two-products)

The more interesting version of ChatGPT Work is the one that runs in the cloud. This can be accessed via [chatgpt.com](https://www.chatgpt.com/) or through the ChatGPT mobile apps. Let’s call it **Work Cloud**.

If you install the ChatGPT desktop app—the app that used to be called Codex—you gain access to a thing called ChatGPT Work that can access files and run programs directly on your computer. Let’s call that one **Work Local**. This one feels more like regular Codex re-skinned to be less intimidating to non-software-developers.

( **Update**: Work Cloud is also available from the ChatGPT desktop app, via a [Where should this chat run?](https://bsky.app/profile/jkwim.bsky.social/post/3mueurvkss52h) dropdown.)

For the rest of this article I’m going to talk exclusively about Work Cloud.

#### Work is for paid subscribers only [\#](https://simonwillison.net/2026/Aug/30/understanding-chatgpt-work/\#work-is-for-paid-subscribers-only)

Right now, ChatGPT Work (in both flavors) is available only to $20/month and up subscribers. Free users and $8/month Go users do not have access.

#### Work has features that aren’t available in Chat [\#](https://simonwillison.net/2026/Aug/30/understanding-chatgpt-work/\#work-has-features-that-aren-t-available-in-chat)

The interface for accessing Work is a tab selector, which presents it as an alternative to Chat:

====
[Skip to main content](https://www.anthropic.com/engineering#main-content) [Skip to footer](https://www.anthropic.com/engineering#footer)

[Home](https://www.anthropic.com/)

- Research
- [Policy](https://www.anthropic.com/policy)
- Commitments
- Learn
- [News](https://www.anthropic.com/news)

[Try Claude](https://claude.ai/)

## Engineering at Anthropic: Inside the team building reliable AI systems

[Start building](https://platform.claude.com/) [Developer docs](https://www.anthropic.com/docs)

![How we contain Claude across products](https://www-cdn.anthropic.com/images/4zrzovbb/website/47d14a71a7a759af39e1bc36ee68d65eb16ad74d-1000x1000.svg)

[![How we contain Claude across products](https://www-cdn.anthropic.com/images/4zrzovbb/website/47d14a71a7a759af39e1bc36ee68d65eb16ad74d-1000x1000.svg)\\
\\
Featured **How we contain Claude across products** \\
\\
As agents grow more capable, so does their potential blast radius. The engineering question is how to cap it. Here’s what we’ve learned building containment for claude.ai, Claude Code, and Cowork.](https://www.anthropic.com/engineering/how-we-contain-claude)

[![An update on recent Claude Code quality reports](https://www-cdn.anthropic.com/images/4zrzovbb/website/259cb9466c31eee1bd312c230c1ab95c844da488-500x500.svg)\\
\\
**An update on recent Claude Code quality reports** \\
\\
Apr 23, 2026](https://www.anthropic.com/engineering/april-23-postmortem)[![Scaling Managed Agents: Decoupling the brain from the hands](https://www-cdn.anthropic.com/images/4zrzovbb/website/7675e9c4ed4c7a8fe2e4df296fd1c4adac5b652b-1200x1200.svg)\\
\\
**Scaling Managed Agents: Decoupling the brain from the hands** \\
\\
Apr 08, 2026](https://www.anthropic.com/engineering/managed-agents)[![How we built Claude Code auto mode: a safer way to skip permissions](https://www-cdn.anthropic.com/images/4zrzovbb/website/b87185e4d533134bc3f9b949a874396dcfcb2e80-500x500.svg)\\
\\
**How we built Claude Code auto mode: a safer way to skip permissions** \\
\\
Mar 25, 2026](https://www.anthropic.com/engineering/claude-code-auto-mode)[![Harness design for long-running application development](https://www-cdn.anthropic.com/images/4zrzovbb/website/af0acebfbd57ac4b26ae7d7ae124d7326a3e47e4-1200x1200.svg)\\
\\
**Harness design for long-running application development** \\
\\
Mar 24, 2026](https://www.anthropic.com/engineering/harness-design-long-running-apps)[![Eval awareness in Claude Opus 4.6’s BrowseComp performance](https://www-cdn.anthropic.com/images/4zrzovbb/website/641d32b3291956d595c7e820d5bf94c5f44baa28-500x500.svg)\\
\\
**Eval awareness in Claude Opus 4.6’s BrowseComp performance** \\
\\
Mar 06, 2026](https://www.anthropic.com/engineering/eval-awareness-browsecomp)[**Quantifying infrastructure noise in agentic coding evals** \\
\\
Feb 05, 2026](https://www.anthropic.com/engineering/infrastructure-noise)[![Building a C compiler with a team of parallel Claudes](https://www-cdn.anthropic.com/images/4zrzovbb/website/44e93e074d53285f64ff717365b04c4a2164a445-1200x1200.svg)\\
\\
**Building a C compiler with a team of parallel Claudes** \\
\\
Feb 05, 2026](https://www.anthropic.com/engineering/building-c-compiler)[![Designing AI-resistant technical evaluations](https://www-cdn.anthropic.com/images/4zrzovbb/website/dc34c3eeae881b105ef652d5630d84de6a1fa01a-1200x1200.svg)\\
\\
**Designing AI-resistant technical evaluations** \\
\\
Jan 21, 2026](https://www.anthropic.com/engineering/AI-resistant-technical-evaluations)[![Demystifying evals for AI agents](https://www-cdn.anthropic.com/images/4zrzovbb/website/b87185e4d533134bc3f9b949a874396dcfcb2e80-500x500.svg)\\
\\
**Demystifying evals for AI agents** \\
\\
Jan 09, 2026](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)[![Effective harnesses for long-running agents](https://www-cdn.anthropic.com/images/4zrzovbb/website/c041b5e0498972014414a7c3d044727982f26bde-500x500.svg)\\
\\
====LANGCHAIN====
[home](https://www.langchain.com/)

Products

[LangSmith Platform](https://www.langchain.com/langsmith-platform)

Agent Improvement

[![](https://cdn.prod.website-files.com/65b8cd72835ceeacd4449a53/6a1c6031b3db015796401c5b_LangSmith%20Engine_Icon_light%201.svg)\\
\\
Engine\\
\\
Improve agents autonomously](https://www.langchain.com/langsmith/engine) [![](https://cdn.prod.website-files.com/65b8cd72835ceeacd4449a53/6989c024180a65887312dd40_Frame%202147254707.svg)\\
\\
Observability\\
\\
See exactly what your agents are doing](https://www.langchain.com/langsmith/observability) [![](https://cdn.prod.website-files.com/65b8cd72835ceeacd4449a53/6989c0247f235ca5583fa63b_Frame%202147255166.svg)\\
\\
Evaluation\\
\\
Score and improve agent performance](https://www.langchain.com/langsmith/evaluation)

Agent Infrastructure

[![](https://cdn.prod.website-files.com/65b8cd72835ceeacd4449a53/6989c024926f877c1de6e728_updated.svg)\\
\\
Deployment\\
\\
Ship and scale agents in production](https://www.langchain.com/langsmith/deployment) [![](https://cdn.prod.website-files.com/65b8cd72835ceeacd4449a53/6a020888f9b2346912c07f41_sandboxes_light_mode%202.svg)\\
\\
Sandboxes\\
\\
Run agent-generated code safely](https://www.langchain.com/langsmith/sandboxes) [![](https://cdn.prod.website-files.com/65b8cd72835ceeacd4449a53/6a6aaa79189ca58233362fc0_LangSmith%20LLM%20Gateway_icon_dark%20mode.png)\\
\\
LLM Gateway\\
\\
Control agent model calls](https://www.langchain.com/langsmith/llm-gateway)

No-Code Agents

[![](https://cdn.prod.website-files.com/65b8cd72835ceeacd4449a53/69baea024a5f7c2d229815b0_LangSmith%20Fleet_icon_light%20mode%203.svg)\\
\\
Fleet\\
\\
Agents for the whole company](https://www.langchain.com/langsmith/fleet)

Open Source

Agent Frameworks

[![](https://cdn.prod.website-files.com/65b8cd72835ceeacd4449a53/6989c02453d869396317aaa3_updated-1.svg)\\
\\
deepagents\\
\\
Build long-running agents for complex tasks](https://www.langchain.com/deep-agents) [![](https://cdn.prod.website-files.com/65b8cd72835ceeacd4449a53/6989c024c2d98286a8fb058f_Frame%202147255166-1.svg)\\
\\
langgraph\\
\\
Build agents with low-level control](https://www.langchain.com/langgraph) [![](https://cdn.prod.website-files.com/65b8cd72835ceeacd4449a53/6989c024409fcfc7e5b8f78f_Frame%202147254707-1.svg)\\
\\

codex
Anthropic Engineering has a fresh-featured "How we contain Claude" post. Checking it plus more sources now.
exec
/bin/bash -lc 'firecrawl scrape -u "https://www.anthropic.com/engineering/how-we-contain-claude" --format markdown -o /tmp/anth_contain.md >/dev/null 2>&1; echo 1; firecrawl scrape -u "https://simonwillison.net/2026/Aug/27/breaking-claude-code-opus-5-auto-mode/" --format markdown -o /tmp/sw_breaking.md >/dev/null 2>&1; echo 2; firecrawl scrape -u "https://simonwillison.net/2026/Sep/4/rogue-agent-wikis/" --format markdown -o /tmp/sw_wikis.md >/dev/null 2>&1; echo 3; firecrawl search "code.claude.com OR anthropic Claude Code week 35 OR week 36 release digest" --limit 8 --tbs qdr:w --json -o /tmp/s13.json >/dev/null 2>&1; echo 4' in /root/note-worker
 succeeded in 7530ms:
1
2
3
4

exec
/bin/bash -lc 'head -70 /tmp/anth_contain.md' in /root/note-worker
 succeeded in 0ms:
[Skip to main content](https://www.anthropic.com/engineering/how-we-contain-claude#main-content) [Skip to footer](https://www.anthropic.com/engineering/how-we-contain-claude#footer)

[Home](https://www.anthropic.com/)

- Research
- [Policy](https://www.anthropic.com/policy)
- Commitments
- Learn
- [News](https://www.anthropic.com/news)

[Try Claude](https://claude.ai/)

[Engineering at Anthropic](https://www.anthropic.com/engineering)

![](https://www-cdn.anthropic.com/images/4zrzovbb/website/47d14a71a7a759af39e1bc36ee68d65eb16ad74d-1000x1000.svg)

# How we contain Claude across products

Published May 25, 2026

As agents grow more capable, so does their potential blast radius. The engineering question is how to cap it. Here’s what we’ve learned building containment for claude.ai, Claude Code, and Cowork.

Twelve months ago, we'd have rejected out of hand the idea of granting Claude access sufficient to take down an internal Anthropic service. Today that level of access is routine, and Anthropic developers are more productive for it. The risk of these deployments has two components: how likely a failure is, and how much damage one could do. Progress on safeguards and model training has steadily driven down the first; the second—the theoretical blast radius—only grows as capabilities and access expand. Yet as agents become capable of doing work that once required a person or even a team, the cost of _not_ deploying grows large enough that the risk-reward calculation tips heavily toward adoption, as long as products can be made safe. The engineering question becomes how to cap the blast radius.

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F5ebc85c6325c7f59bd6c08950ff9beb1863f1345-1920x866.png&w=3840&q=75)_When bounds can be placed on the relative damage of an autonomous agent—such as through control over its environment—high-utility capabilities can motivate deployment. Claude Mythos Preview is an example of a model whose blast radius was deemed too high to ship in April 2026. However, we expect broader release of models with similar levels of capability to become appropriate as defenders harden critical systems and safeguards mature—even though some risk will always remain. Model capability is an important factor in the total risk of an agent’s deployment._

There are broadly two ways to do this.

The first is to supervise the agent’s behavior via a human-in-the-loop. Claude Code previously protected against agents taking unintended actions by asking users for permission at each turn. Theoretically that works, but we’ve found the approach to be fallible. Our telemetry showed users approved roughly 93% of permission prompts. The more approvals a user sees, the less attention they pay to each, becoming over time much less diligent in their supervision. We recently built Claude Code auto mode, which [automates safer approvals](https://www.anthropic.com/engineering/claude-code-auto-mode) in order to reduce this approval fatigue. Still, vulnerabilities remain—any probabilistic defense has a non-zero miss rate.1

The second approach to capping the blast radius—and the focus of much of this post—is containment. Rather than supervising what the agent does, we supervise what it’s _able_ to do by enforcing access boundaries through, for example, sandboxes, virtual machines, and egress controls. This is where Anthropic engineering has devoted the most effort, and also where many of the most surprising security failures have occurred.

Over the past two years, we’ve shipped three primary agentic products: [claude.ai](http://claude.ai/redirect/website.v1.6572db6a-e511-448d-98b4-108197734e84), Claude Code, and Claude Cowork. Each serves a different audience, requiring a different containment architecture. This article shares what’s held up, what’s broken, and what we’ve learned about agent security along the way.

## **Three types of risk, three components of defense**

Security risks to agents fall into one of three categories:

**User misuse:** A user—either maliciously or through carelessness—directs the agent to do something harmful. This includes everything from asking the agent to bypass a check they find annoying, to running a destructive command they don’t understand, to specifying intentional harm.

**Model misbehavior:** The agent takes a harmful action no one asked for. As our models have improved, they have become more aligned on most behavior evaluations, but this doesn’t mean risk necessarily shrinks. Less capable models are more likely to misread a situation and make obvious errors. More capable models make fewer mistakes, but they’re also better at finding unexpected paths to a goal, often by routing around restrictions nobody thought to write down.

At Anthropic, we’ve seen Claude models [“helpfully” escape a sandbox](https://red.anthropic.com/2026/mythos-preview/) in order to complete a task, examine git history to [find answers to a coding test](https://assets.anthropic.com/m/64823ba7485345a7/Claude-Opus-4-5-System-Card.pdf), and spontaneously identify the benchmark it was being run on in order to [decrypt its answer key](https://www.anthropic.com/engineering/eval-awareness-browsecomp). Each model brings a new set of capabilities that are sometimes put to work in unexpected ways.

**External attackers:** The agent is attacked through external vectors such as tools, files, or network access. This category includes both prompt injection and conventional attacks on the agent's runtime, orchestration layer, or proxy.

When building containment and defense systems, we apply defenses to three main components:

**The environment in which the agent runs.** We constrain where and how an agent can act with process sandboxes, VMs, filesystem boundaries, and egress controls. The goal is to set a hard boundary on what an agent can reach. For example, if credentials never enter the sandbox, they can't be exfiltrated, regardless of whether the cause is a user, a model finding a “creative” path, or an attacker.

A tight perimeter also means you can relax oversight. Claude Code’s [reference devcontainer](https://code.claude.com/docs/en/devcontainer) exists precisely so that the agent can run unattended, without per-action approvals.

**The model the agent consults.** The mechanisms here include system prompts, classifiers, probes, and training modifications. Because models are probabilistic, these shape only what the agent _tends_ to do, not what it is theoretically capable of doing.

These defenses are strong. On Gray Swan's Agent Red Teaming benchmark, which tests susceptibility to prompt injection, [Claude Opus 4.7](https://cdn.sanity.io/files/4zrzovbb/website/037f06850df7fbe871e206dad004c3db5fd50340.pdf) holds attack success to roughly 0.1% on single attempts, and around 5–6% after 100 adaptive attempts. Claude Code auto mode catches roughly 83% of overeager behaviors [before they execute](https://www.anthropic.com/engineering/claude-code-auto-mode). Yet even with best-in-class defenses, protection in the model layer will never be 100% effective, which is why it can't stand alone.

**The external content the agent can reach.** MCP servers, third-party plugins, and web search tools all feed content into the agent’s context from sources you don’t control. An audited connector isn’t the same as audited data—a GitHub connector, for instance, can load a poisoned README straight into the model’s context despite passing malware checks. Granularly limiting tool permissions can help limit the blast radius. An agent with read-only DB access, for instance, can be deployed far more broadly than one that writes to prod.

Defenses should overlap and complement each other. When environmental defenses aren’t available, the model layer has to pick up the slack (this is precisely what Claude Code’s [auto mode](https://claude.com/blog/auto-mode) is designed for). Locally, the environment and model defenses can guard against malicious tool outputs, but defenses can be added higher up the chain by limiting the tool’s capabilities and access.

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F5fae1ecca4cd8aaefb9ac949348e96967f9a5100-1920x1080.png&w=3840&q=75)_Three components to defend: the model, the environment in which it runs, and the external content the agent can reach._

## **Patterns for containing agents**

Focusing on the environment layer, we describe three isolation patterns and how they’re tailored for each Claude platform— [claude.ai](http://claude.ai/redirect/website.v1.6572db6a-e511-448d-98b4-108197734e84), Claude Code, and Cowork. We arrived at each design gradually, after finding the balance between the capabilities we need from the agent and the degree of intervention required from the user.

### **Pattern 1: The ephemeral container (claude.ai code execution)**

Though best known as a chat interface, claude.ai also writes and runs code, generates files, and calls connectors. When Claude runs code inside claude.ai, it does so in a [gVisor](https://en.wikipedia.org/wiki/GVisor) container on isolated infrastructure. The agent is entirely server-side; no code runs on the local machine, and the filesystem is ephemeral (per-session). The blast radius is minimal, but so is the ceiling on what Claude can do—there's no persistent workspace and no access to the user's filesystem.


codex
The Anthropic containment post is from May — out of window. Continuing with more targeted searches across GitHub, HN, and other sources.
exec
/bin/bash -lc "firecrawl research inspect-paper arxiv:2609.01865 --pretty 2>&1 | python3 -c \"
import sys,json
d=json.load(sys.stdin); p=d.get('paper',{})
print(p.get('ids',{}).get('arxiv'),'|',p.get('createdDate'),'|',p.get('title'),'|',p.get('authors'))
\" ; firecrawl scrape -u \"https://suedbroecker.net/2026/08/30/agent-harness-in-2026-hype-word-industry-term-or-useful-technical-concept/\" --format markdown -o /tmp/sued.md >/dev/null 2>&1; echo scraped_sued" in /root/note-worker
 succeeded in 4879ms:
['2609.01865'] | 2026-09-01 | ExecRetrieval: Measuring the Functional-Correctness Gap in Code-Embedding Retrieval | Aaryan Kapoor, Md Abdullah Al Hafiz Khan
scraped_sued

exec
/bin/bash -lc 'head -120 /tmp/sued.md; echo; wc -l /tmp/sued.md' in /root/note-worker
 succeeded in 0ms:
[Skip to content](https://suedbroecker.net/2026/08/30/agent-harness-in-2026-hype-word-industry-term-or-useful-technical-concept/#content)

[Search](https://suedbroecker.net/2026/08/30/agent-harness-in-2026-hype-word-industry-term-or-useful-technical-concept/#search-container)

Search for:

[![Thomas Suedbroecker's Blog](https://suedbroecker.net/wp-content/uploads/2018/09/cropped-new-profile-photo-2.png)](https://suedbroecker.net/)

[Thomas Suedbroecker's Blog](https://suedbroecker.net/)

I want to share my experience in the cloud, AI, and agents development areas.

Menu

- [About me](https://suedbroecker.net/about-me/)
- [Archive](https://suedbroecker.net/archive/)
- [Disclaimer](https://suedbroecker.net/disclaimer/)
- [Legal Disclosure](https://suedbroecker.net/legal-disclosure/)
- [Contact](https://suedbroecker.net/contact/)

[Open Search](https://suedbroecker.net/2026/08/30/agent-harness-in-2026-hype-word-industry-term-or-useful-technical-concept/#)

# [Agent Harness in 2026: Hype Word, Industry Term, or Useful Technical Concept?](https://suedbroecker.net/2026/08/30/agent-harness-in-2026-hype-word-industry-term-or-useful-technical-concept/)

![](https://suedbroecker.net/wp-content/uploads/2026/08/featured-image-blogpost.png?w=1400)

## Everyone Talks About Agent Harnesses — But What Exactly Is a Harness?

Over the past few months, I have come across the term **agent harness** more and more frequently. Is this just another hype word, or does it introduce a useful technical distinction?

OpenAI talks about the Codex harness. IBM describes Bob V2 as one agent and one harness. Google uses the term Antigravity harness. Anthropic describes Claude Code as a flexible agent harness. Microsoft documents an Agent Harness, and Visual Studio Code even calls _agent harness_ an industry term.

At first glance, this sounds simple.

But when I looked more closely, I found that the term is now used across several major AI platforms without being defined in exactly the same way.

So two statements would both be misleading:

> There is no definition of an agent harness.

and

> There is one generally accepted definition of an agent harness.

Definitions clearly exist. Some are vendor-specific, some describe architectural concepts, and some are increasingly vendor-neutral.

What I could not find is one normative, cross-vendor definition that all vendors officially follow.

This post therefore investigates four questions:

1. Is _agent harness_ formally standardized?
2. How do vendors use the term?
3. Why do we call it a _harness_ rather than simply a _framework_?
4. What common working definition can reasonably be derived from the available evidence?

My research rule is simple:

**Source first. Evidence second. Interpretation third.**

Don’t want to read? Just listen to the podcast on YouTube.

Agent Harness in 2026: Hype Word, Industry Term, or Useful Technical Concept? - YouTube

Tap to unmute

[Agent Harness in 2026: Hype Word, Industry Term, or Useful Technical Concept?](https://www.youtube.com/watch?v=G5UNeCBcjoM) [Thomas Südbröcker](https://www.youtube.com/channel/UC-Z5jLA2-eamaS4-o1gzYEA)

Thomas Südbröcker1.08K subscribers

[Watch on](https://www.youtube.com/watch?v=G5UNeCBcjoM)

**Table of Contents**

- Everyone Talks About Agent Harnesses – But What Exactly Is a Harness?

1. Scope and Research Method

2. Is “Agent Harness” a Standardized Term?

3. Why “Harness”? Why Not “Framework”?

4. How Vendors Use the Term

5. The Common Functional Core

6. My Working Definition

7. Why Harnesses Matter Beyond Model Comparisons

8. Connection to Engineering Provenance

9. Evidence vs. Interpretation 10\. Final Thoughts
- References
- Research Status

## 1\. Scope and Research Method

![](https://suedbroecker.net/wp-content/uploads/2026/08/1-new-chapter-1.png?w=1024)

This post is written from the perspective of an **individual developer**. I work for IBM, but this article reflects my personal analysis and uses the same source-based approach for IBM Bob as for the other products.

I work professionally with AI, but I also use different AI development environments privately. This gives me the opportunity to compare what an individual developer can actually access without relying on enterprise licenses.

To study how the term is used in practice, I focus on four environments:

| Vendor | Environment | Individual plan in scope |
| --- | --- | --- |
| IBM | IBM Bob | Bob Pro |
| Anthropic | Claude Code | Claude Pro |
| OpenAI | Codex | ChatGPT Plus |
| Google | Google Antigravity | Google AI Pro |

The goal is not to create a full product benchmark. The goal is to examine how these environments use harness terminology and what common working model can be derived from that evidence. Enterprise editions are deliberately out of scope because they may include additional governance, security, identity, policy, audit, and contractual capabilities.

These plans are included because they give individual developers direct access to the environments investigated in this article. They should not be interpreted as identical pricing or consumption models.

Because agentic development products change quickly, I mainly use documentation published or updated in 2026, or documentation that is still clearly applicable to the current product.

Older sources are included only where they help explain the development of the terminology.


977 /tmp/sued.md

codex
The Suedbröcker post is a cross-vendor harness term survey (Aug 30). Continuing searches for GitHub projects, HN threads, and Chinese community content.
exec
/bin/bash -lc 'cd /tmp && firecrawl search "open source coding agent harness framework github new" --limit 10 --tbs qdr:m --json -o /tmp/g1.json >/dev/null 2>&1; echo g1; firecrawl search "context engineering tool agent memory compaction open source" --limit 10 --tbs qdr:m --json -o /tmp/g2.json >/dev/null 2>&1; echo g2; firecrawl search "news.ycombinator.com coding agent harness discussion" --limit 10 --tbs qdr:m --json -o /tmp/g3.json >/dev/null 2>&1; echo g3; firecrawl search "智能体 harness 上下文工程 AI 编程 深度分析" --limit 10 --tbs qdr:m --json -o /tmp/g4.json >/dev/null 2>&1; echo g4' in /root/note-worker
 succeeded in 8571ms:
g1
g2
g3
g4

exec
/bin/bash -lc 'cd /tmp && for f in g1 g2 g3 g4; do echo "== $f =="; python3 -c "
import json
d=json.load(open('"'/tmp/"'$f.json'"'))
res=d.get('data',{}).get('web',[])
print('n=',len(res))
for r in res[:10]:
    print('-',r.get('url'))
    print('  ', (r.get('title') or '')[:120])
\"; done" in /root/note-worker
 exited 1 in 207ms:
Traceback (most recent call last):
  File "<string>", line 3, in <module>
FileNotFoundError: [Errno 2] No such file or directory: '/tmp/g2.json'
== g3 ==
n= 10
- https://news.ycombinator.com/item?id=49285244
   DeepSeek Harness developer preview - Hacker News
- https://news.ycombinator.com/item?id=49353339
   fx :Tiny, open, native coding agent. | Hacker News
- https://news.ycombinator.com/item?id=49538490
   FrontierHarness Eval – 9 harness, same model, cost per pass varies 17x
- https://news.ycombinator.com/item?id=49384113
   Seed: Minimal, self-modifying agent harness | Hacker News
- https://news.ycombinator.com/item?id=49428882
   Headlong: A microharness for persistent agents | Hacker News
- https://news.ycombinator.com/item?id=49201003
   Herdr is joining Y Combinator. The runtime stays open - Hacker News
- https://news.ycombinator.com/item?id=49532083
   Show HN: I Have Been Clawed – Index of coding agent incidents
- https://news.ycombinator.com/item?id=49233448
   OpenChamber: An Agentic Development Environment
- https://news.ycombinator.com/item?id=49235859
   Is it all just vapourware? - Hacker News
- https://github.com/yc-software/qm
   yc-software/qm: Multiplayer agent harness for work. - GitHub
== g4 ==
Traceback (most recent call last):
  File "<string>", line 3, in <module>
FileNotFoundError: [Errno 2] No such file or directory: '/tmp/g4.json'

codex
Strong leads: OpenAI "Codex as a platform" and several HN harness projects. Verifying dates and details now.
exec
/bin/bash -lc 'firecrawl scrape -u "https://developers.openai.com/blog/codex-as-a-platform" --format markdown -o /tmp/oai_codex_platform.md >/dev/null 2>&1; echo oai; for id in 49538490 49384113 49428882 49532083 49353339 49233448; do firecrawl scrape -u "https://news.ycombinator.com/item?id=$id" --format markdown -o /tmp/hn_$id.md >/dev/null 2>&1; echo hn_$id; done' in /root/note-worker
 succeeded in 14210ms:
oai
hn_49538490
hn_49384113
hn_49428882
hn_49532083
hn_49353339
hn_49233448

exec
/bin/bash -lc 'head -50 /tmp/oai_codex_platform.md; echo ====49538490====; head -50 /tmp/hn_49538490.md' in /root/note-worker
 succeeded in 0ms:
For the complete documentation index, see [llms.txt](https://developers.openai.com/llms.txt). Markdown versions of documentation pages are available by appending
`.md` to the page URL.

[![OpenAI Developers](https://developers.openai.com/OpenAI_Developers.svg)ChatGPT](https://developers.openai.com/)

[Home](https://developers.openai.com/)

[API](https://developers.openai.com/api/docs)

[Codex](https://learn.chatgpt.com/docs)

[Docs\\
\\
Guides, concepts, and product docs for Codex](https://learn.chatgpt.com/docs) [Use cases\\
\\
Example workflows and tasks teams can take on with ChatGPT or Codex](https://learn.chatgpt.com/use-cases)

[Docs](https://developers.openai.com/codex)

[Use cases](https://learn.chatgpt.com/use-cases)

[Training](https://developers.openai.com/training)

[Resources](https://developers.openai.com/codex/resources)

[ChatGPT](https://developers.openai.com/chatgpt)

[Plugins\\
\\
Extend ChatGPT and Codex](https://developers.openai.com/plugins) [Workspace Agents\\
\\
Trigger published ChatGPT workspace agents](https://developers.openai.com/workspace-agents) [Commerce\\
\\
Build commerce flows in ChatGPT](https://developers.openai.com/commerce) [Ads\\
\\
Publish and measure ads in ChatGPT](https://developers.openai.com/ads)

[Resources](https://developers.openai.com/learn)

[Showcase\\
\\
Demo apps to get inspired](https://developers.openai.com/showcase) [Blog\\
\\
Learnings and experiences from developers](https://developers.openai.com/blog) [Cookbook\\
\\
Notebook examples for building with OpenAI models](https://developers.openai.com/cookbook) [Learn\\
\\
Docs, videos, and demo apps for building with OpenAI](https://developers.openai.com/learn) [Community\\
\\
Programs, meetups, and support for builders](https://developers.openai.com/community)
====49538490====
|     |     |     |
| --- | --- | --- |
| |     |     |     |
| --- | --- | --- |
| [![](https://news.ycombinator.com/y18.svg)](https://news.ycombinator.com/) | **[Hacker News](https://news.ycombinator.com/news)** [new](https://news.ycombinator.com/newest) \| [past](https://news.ycombinator.com/front) \| [comments](https://news.ycombinator.com/newcomments) \| [ask](https://news.ycombinator.com/ask) \| [show](https://news.ycombinator.com/show) \| [jobs](https://news.ycombinator.com/jobs) \| [submit](https://news.ycombinator.com/submit) | [login](https://news.ycombinator.com/login?goto=item%3Fid%3D49538490) | |

| |     |     |     |
| --- | --- | --- |
|  |  | [Show HN: FrontierHarness Eval – 9 harness, same model, cost per pass varies 17x](https://frontierharness.org/) ( [frontierharness.org](https://news.ycombinator.com/from?site=frontierharness.org)) |
|  | 81 points by [shiqimei](https://news.ycombinator.com/user?id=shiqimei) [3 days ago](https://news.ycombinator.com/item?id=49538490) \| [hide](https://news.ycombinator.com/hide?id=49538490&goto=item%3Fid%3D49538490) \| [past](https://hn.algolia.com/?query=Show%20HN%3A%20FrontierHarness%20Eval%20%E2%80%93%209%20harness%2C%20same%20model%2C%20cost%20per%20pass%20varies%2017x&type=story&dateRange=all&sort=byDate&storyText=false&prefix&page=0) \| [favorite](https://news.ycombinator.com/fave?id=49538490&auth=875b6e86ae9747e6162bab2010a747d2a8b8f630) \| [56 comments](https://news.ycombinator.com/item?id=49538490) |
|  |  |

|  | [help](https://news.ycombinator.com/formatdoc) |

|     |     |     |
| --- | --- | --- |
| |     |     |     |
| --- | --- | --- |
| ![](https://news.ycombinator.com/s.gif) |  | [vidarh](https://news.ycombinator.com/user?id=vidarh) [3 days ago](https://news.ycombinator.com/item?id=49539391) \| [next](https://news.ycombinator.com/item?id=49538490#49541015)\[–\]<br>Testing it against Kimi is potentially skewing the numbers massively. Kimi has a number of quirks that requires behaviours that e.g. Claude or GPT doesn't.<br>Harnesses that are built around needing to work with "weird" models will need to deal with that, such as Kimi's tendency to get stuck in tool-call loops.<br>Harnesses built to deal with e.g. Anthropic's models primarily, do not need to deal with that.<br>Claiming on the blog that this gives Kimi Code no home field advantage seems like a dicey assumption. I haven't dug into the newest Kimi Code much, but the older Kimi CLI included several tools that were clearly specifically aimed at working around that behaviour - when I copied their checkpoints and "dmail" mechanism into my own harness, the performance with Kimi improved dramatically, but it made zero difference against Anthropic models.<br>That doesn't make the data worthless - it's clear you shouldn't use Clade Code to work against Kimi. But it does significantly limit the utility of it.<br>[reply](https://news.ycombinator.com/reply?id=49539391&goto=item%3Fid%3D49538490%2349539391) | |
| |     |     |     |
| --- | --- | --- |
| ![](https://news.ycombinator.com/s.gif) |  | [Edward40](https://news.ycombinator.com/user?id=Edward40) [3 days ago](https://news.ycombinator.com/item?id=49543112) \| [parent](https://news.ycombinator.com/item?id=49538490#49539391) \| [next](https://news.ycombinator.com/item?id=49538490#49542981)\[–\]<br>Good points! That’s a known limitation of our v1.0 benchmark with Claude Code. For v1.1, we're expanding both harnesses and models to evaluate the full harness × model matrix. This will highlight interaction effects (showing which harnesses suit which models best) and let us publish a full compatibility matrix. We shared more details on our roadmap in our blog post ( [https://runta.com/blog/introducing-frontierharness-eval/](https://runta.com/blog/introducing-frontierharness-eval/)).<br>[reply](https://news.ycombinator.com/reply?id=49543112&goto=item%3Fid%3D49538490%2349543112) | |
| |     |     |     |
| --- | --- | --- |
| ![](https://news.ycombinator.com/s.gif) |  | [vidarh](https://news.ycombinator.com/user?id=vidarh) [2 days ago](https://news.ycombinator.com/item?id=49548606) \| [root](https://news.ycombinator.com/item?id=49538490#49539391) \| [parent](https://news.ycombinator.com/item?id=49538490#49543112) \| [next](https://news.ycombinator.com/item?id=49538490#49542981)\[–\]<br>That's great. It'd definitively be very interesting. Not least as an indicator of which harnesses to dig into the code of.<br>Kimi-cli is actually very interesting in that respect for the checkpoint / messaging mechanism I mentioned; it's basically almost like a model-initiated partial compaction of the end of a conversation to prune investigations that happened on the main agent loop - it'll be really interesting to see if it helps on any other models.<br>So oe thing that'd be really interesting to see when you expand to other models, would be if you mine the traces from those harnesses and generate stats on which tools get called. Seeing which models manage to take advantage of custom tools from which harnesses would be quite useful.<br>[reply](https://news.ycombinator.com/reply?id=49548606&goto=item%3Fid%3D49538490%2349548606) | |
| |     |     |     |
| --- | --- | --- |
| ![](https://news.ycombinator.com/s.gif) |  | [nijave](https://news.ycombinator.com/user?id=nijave) [3 days ago](https://news.ycombinator.com/item?id=49542981) \| [parent](https://news.ycombinator.com/item?id=49538490#49539391) \| [prev](https://news.ycombinator.com/item?id=49538490#49543112) \| [next](https://news.ycombinator.com/item?id=49538490#49541015)\[–\]<br>Afaik the reverse is also true. Some models are trained for specific harness setups so work better/more efficiently in that harness. If you give a model trained on a Read/Write/Bash tool setup a harness with only Bash where it needs to generate shell commands, I'd expect it to perform differently.<br>Related, there was a small debacle when Claude Code yeeted out a prompt change telling Opus to use Bash for everything. It was speculated it was an optimization to try to make it more efficient by encouraging it to chain a bunch of "tool use" commands into a giant shell command. However, they didn't communicate it clearly and it broke a bunch of setups that expected/hooked tool calls<br>There's also the (anecdotal?) tradeoff that dumb models tend to do better with smart tools and smart models tend to do better with dumb tools (smart tools -> easier to use but require more context usage for specs, dumb tools -> harder to use but more versatile and save context)<br>[reply](https://news.ycombinator.com/reply?id=49542981&goto=item%3Fid%3D49538490%2349542981) | |
| |     |     |     |
| --- | --- | --- |
| ![](https://news.ycombinator.com/s.gif) |  | [nsingh2](https://news.ycombinator.com/user?id=nsingh2) [3 days ago](https://news.ycombinator.com/item?id=49541015) \| [prev](https://news.ycombinator.com/item?id=49538490#49539391) \| [next](https://news.ycombinator.com/item?id=49538490#49541099)\[–\]<br>One issue I see with including something like Pi is that it's intentionally bare bones. I don't think anyone uses Pi without some basic custom extensions (subagents, check lists, etc), so this benchmark may not be representative of a realistic setup.<br>Would be interesting to see some sort of ablation test too. E.g. what parts of Codex contribute most to the perf, and can they be recreated more minimally in something like Pi.<br>[reply](https://news.ycombinator.com/reply?id=49541015&goto=item%3Fid%3D49538490%2349541015) | |
| |     |     |     |
| --- | --- | --- |
| ![](https://news.ycombinator.com/s.gif) |  | [dfltr](https://news.ycombinator.com/user?id=dfltr) [3 days ago](https://news.ycombinator.com/item?id=49541405) \| [parent](https://news.ycombinator.com/item?id=49538490#49541015) \| [next](https://news.ycombinator.com/item?id=49538490#49541413)\[–\]<br>It does seem a bit odd to say "We tested all of these bicycles with the same rider" when one of the test cases is actually a bare high-end frame with no components on it.<br>It's even weirder given that another of the test cases is essentially "We put parts on the frame (OhMyPi) and it went faster!"<br>[reply](https://news.ycombinator.com/reply?id=49541405&goto=item%3Fid%3D49538490%2349541405) | |
| |     |     |     |
| --- | --- | --- |
| ![](https://news.ycombinator.com/s.gif) |  | [jdthedisciple](https://news.ycombinator.com/user?id=jdthedisciple) [3 days ago](https://news.ycombinator.com/item?id=49542559) \| [root](https://news.ycombinator.com/item?id=49538490#49541015) \| [parent](https://news.ycombinator.com/item?id=49538490#49541405) \| [next](https://news.ycombinator.com/item?id=49538490#49542688)\[–\]<br>I'm not sure your analogy holds, because here the optimization metric is clear and unanimous: every one wants max pass rate at min costs.<br>With the bicycle, some may prefer comfort, others speed, others offroad, etc., so it would not be obvious which one is "best".<br>[reply](https://news.ycombinator.com/reply?id=49542559&goto=item%3Fid%3D49538490%2349542559) | |
| |     |     |     |
| --- | --- | --- |
| ![](https://news.ycombinator.com/s.gif) |  | [infecto](https://news.ycombinator.com/user?id=infecto) [3 days ago](https://news.ycombinator.com/item?id=49542688) \| [root](https://news.ycombinator.com/item?id=49538490#49541015) \| [parent](https://news.ycombinator.com/item?id=49538490#49541405) \| [prev](https://news.ycombinator.com/item?id=49538490#49542559) \| [next](https://news.ycombinator.com/item?id=49538490#49541413)\[–\]<br>Not weird or odd in the least. I think it clearly shows that Pi barebones at least in this set of tests, preformed better and cheaper cost that OMP.<br>[reply](https://news.ycombinator.com/reply?id=49542688&goto=item%3Fid%3D49538490%2349542688) | |
| |     |     |     |
| --- | --- | --- |
| ![](https://news.ycombinator.com/s.gif) |  | [randomblock1](https://news.ycombinator.com/user?id=randomblock1) [3 days ago](https://news.ycombinator.com/item?id=49541413) \| [parent](https://news.ycombinator.com/item?id=49538490#49541015) \| [prev](https://news.ycombinator.com/item?id=49538490#49541405) \| [next](https://news.ycombinator.com/item?id=49538490#49542695)\[–\]<br>I think it's still a useful data point. For example, omp, which is pi with some default extensions, scores worse. I do agree that adding more configurations of Pi would help though.<br>[reply](https://news.ycombinator.com/reply?id=49541413&goto=item%3Fid%3D49538490%2349541413) | |
| |     |     |     |
| --- | --- | --- |
| ![](https://news.ycombinator.com/s.gif) |  | [infecto](https://news.ycombinator.com/user?id=infecto) [3 days ago](https://news.ycombinator.com/item?id=49542695) \| [parent](https://news.ycombinator.com/item?id=49538490#49541015) \| [prev](https://news.ycombinator.com/item?id=49538490#49541413) \| [next](https://news.ycombinator.com/item?id=49538490#49541099)\[–\]<br>I use Pi barebones.<br>[reply](https://news.ycombinator.com/reply?id=49542695&goto=item%3Fid%3D49538490%2349542695) | |
| |     |     |     |
| --- | --- | --- |
| ![](https://news.ycombinator.com/s.gif) |  | [Edward40](https://news.ycombinator.com/user?id=Edward40) [3 days ago](https://news.ycombinator.com/item?id=49543761) \| [root](https://news.ycombinator.com/item?id=49538490#49541015) \| [parent](https://news.ycombinator.com/item?id=49538490#49542695) \| [next](https://news.ycombinator.com/item?id=49538490#49541099)\[–\]<br>I also prefer using vanilla Pi over Oh My Pi.<br>[reply](https://news.ycombinator.com/reply?id=49543761&goto=item%3Fid%3D49538490%2349543761) | |
| |     |     |     |

exec
/bin/bash -lc 'rg -n "Published|Date|date|2026|''^# |agent harness|## " /tmp/oai_codex_platform.md | head -40' in /root/note-worker
 succeeded in 0ms:
58:## Search developer resources
62:### Suggested
72:### Suggested
82:### Recent
90:### Topics
105:### Recent
113:### Topics
134:Aug 19, 2026Codex
136:# Codex as a platform: build on the open agent harness
142:![Codex as a platform: build on the open agent harness](https://developers.openai.com/images/blog/codex-as-a-platform-cover.webp)
150:## The reusable part is the agent loop
162:## An open harness developers can inspect and adapt
179:## Choose the right integration layer
192:## Build software around the workflow
205:## Example: Relay
220:## What developers are building
224:- [GitHub and JetBrains](https://github.blog/changelog/2026-07-07-codex-as-agent-provider-and-agentic-enhancements-in-jetbrains-ides/)
238:## Build beyond the obvious
250:## Docs agent

exec
/bin/bash -lc 'for id in 49384113 49428882 49532083 49353339 49233448; do echo "== $id =="; sed -n '"'/y18.svg/,/discussion/p' /tmp/hn_"'$id.md | head -12 | sed '"'s/\\[.*\\]//g' | tr -s ' \\n' ' ' | cut -c1-400; echo; done" in /root/note-worker
 succeeded in 0ms:
== 49384113 ==
| (https://news.ycombinator.com/login?goto=item%3Fid%3D49384113) | | | | | | | | --- | --- | --- | | | | (https://news.ycombinator.com/from?site=github.com/vivekhaldar)) | | | 59 points by (https://news.ycombinator.com/item?id=49384113) | | | | | | | | | --- | --- | --- | | | | | | | --- | --- | --- | 

== 49428882 ==
| (https://news.ycombinator.com/login?goto=item%3Fid%3D49428882) | | | | | | | | --- | --- | --- | | | | (https://news.ycombinator.com/from?site=laude.org)) | | | 125 points by (https://news.ycombinator.com/item?id=49428882) | | | | | | (https://news.ycombinator.com/formatdoc) | | | | | | --- | --- | --- | 

== 49532083 ==
| (https://news.ycombinator.com/login?goto=item%3Fid%3D49532083) | | | | | | | | --- | --- | --- | | | | (https://news.ycombinator.com/from?site=ihavebeenclawed.com)) | | | 23 points by (https://news.ycombinator.com/item?id=49532083) | | | | | | (https://news.ycombinator.com/formatdoc) | | | | | | --- | --- | --- | 

== 49353339 ==
| (https://news.ycombinator.com/login?goto=item%3Fid%3D49353339) | | | | | | | | --- | --- | --- | | | | (https://news.ycombinator.com/from?site=fx.sh)) | | | 318 points by (https://news.ycombinator.com/item?id=49353339) | | | | | | | | | --- | --- | --- | | | | | | | --- | --- | --- | 

== 49233448 ==
sed: couldn't write 389 items to stdout: Broken pipe
| (https://news.ycombinator.com/login?goto=item%3Fid%3D49233448) | | | | | | | | --- | --- | --- | | | | (https://news.ycombinator.com/from?site=openchamber.dev)) | | | 190 points by (https://news.ycombinator.com/item?id=49233448) | | | | | | | | | --- | --- | --- | | | | | | | --- | --- | --- | 


exec
/bin/bash -lc 'for id in 49384113 49428882 49532083 49353339 49233448 49538490; do echo "== $id =="; rg -o "[0-9]+ (points|comments)[''^|]*'"\\| ["'^|]*ago[''^|]*" /tmp/hn_$id.md | head -3; rg -o '"'ago\\| \\[hide\\]' /tmp/hn_"'$id.md | head -1; done' in /root/note-worker
 succeeded in 0ms:
== 49384113 ==
== 49428882 ==
== 49532083 ==
== 49353339 ==
== 49233448 ==
== 49538490 ==

exec
/bin/bash -lc 'for id in 49384113 49428882 49532083 49353339 49233448; do echo "== $id =="; rg -n "ago" /tmp/hn_$id.md | head -2 | cut -c1-300; done' in /root/note-worker
 succeeded in 0ms:
== 49384113 ==
10:|  | 59 points by [gandalfgeek](https://news.ycombinator.com/user?id=gandalfgeek) [16 days ago](https://news.ycombinator.com/item?id=49384113) \| [hide](https://news.ycombinator.com/hide?id=49384113&goto=item%3Fid%3D49384113) \| [past](https://hn.algolia.com/?query=Seed%3A%20Minimal%2C%20self-mod
17:| ![](https://news.ycombinator.com/s.gif) |  | [lnenad](https://news.ycombinator.com/user?id=lnenad) [16 days ago](https://news.ycombinator.com/item?id=49385193) \| [next](https://news.ycombinator.com/item?id=49384113#49385148)\[–\]<br>I think as many things that are posted here lately there is
== 49428882 ==
10:|  | 125 points by [lbw1215](https://news.ycombinator.com/user?id=lbw1215) [12 days ago](https://news.ycombinator.com/item?id=49428882) \| [hide](https://news.ycombinator.com/hide?id=49428882&goto=item%3Fid%3D49428882) \| [past](https://hn.algolia.com/?query=Headlong%3A%20A%20microharness%20for%2
19:| ![](https://news.ycombinator.com/s.gif) |  | [MikhailTal](https://news.ycombinator.com/user?id=MikhailTal) [12 days ago](https://news.ycombinator.com/item?id=49429096) \| [next](https://news.ycombinator.com/item?id=49428882#49432404)\[–\]<br>Very fascinating, super interesting engineering. Al
== 49532083 ==
10:|  | 23 points by [nezhar](https://news.ycombinator.com/user?id=nezhar) [4 days ago](https://news.ycombinator.com/item?id=49532083) \| [hide](https://news.ycombinator.com/hide?id=49532083&goto=item%3Fid%3D49532083) \| [past](https://hn.algolia.com/?query=Show%20HN%3A%20I%20Have%20Been%20Clawed%20
19:| ![](https://news.ycombinator.com/s.gif) |  | [londons\_explore](https://news.ycombinator.com/user?id=londons_explore) [3 days ago](https://news.ycombinator.com/item?id=49534613) \| [next](https://news.ycombinator.com/item?id=49532083#49556783)\[–\]<br>I also had an opus subagent accidentally 
== 49353339 ==
10:|  | 318 points by [handfuloflight](https://news.ycombinator.com/user?id=handfuloflight) [16 days ago](https://news.ycombinator.com/item?id=49353339) \| [hide](https://news.ycombinator.com/hide?id=49353339&goto=item%3Fid%3D49353339) \| [past](https://hn.algolia.com/?query=fx%20%3ATiny%2C%20open%2
17:| ![](https://news.ycombinator.com/s.gif) |  | [rsyring](https://news.ycombinator.com/user?id=rsyring) [16 days ago](https://news.ycombinator.com/item?id=49354037) \| [next](https://news.ycombinator.com/item?id=49353339#49368753)\[–\]<br>For all the people asking "Why?", it seems like TFA has a
== 49233448 ==
10:|  | 190 points by [hexomancer](https://news.ycombinator.com/user?id=hexomancer) [27 days ago](https://news.ycombinator.com/item?id=49233448) \| [hide](https://news.ycombinator.com/hide?id=49233448&goto=item%3Fid%3D49233448) \| [past](https://hn.algolia.com/?query=OpenChamber%3A%20An%20Agentic%20
17:| ![](https://news.ycombinator.com/s.gif) |  | [azuanrb](https://news.ycombinator.com/user?id=azuanrb) [27 days ago](https://news.ycombinator.com/item?id=49234056) \| [next](https://news.ycombinator.com/item?id=49233448#49235179)\[–\]<br>I prefer Paseo [https://github.com/getpaseo/paseo](https:

exec
/bin/bash -lc "sed -n '10p' /tmp/hn_49428882.md | cut -c1-500; echo; echo ==49532083==; sed -n '10p' /tmp/hn_49532083.md | cut -c1-500; echo; echo ==49538490==; sed -n '10p' /tmp/hn_49538490.md | cut -c1-500" in /root/note-worker
 succeeded in 0ms:
|  | 125 points by [lbw1215](https://news.ycombinator.com/user?id=lbw1215) [12 days ago](https://news.ycombinator.com/item?id=49428882) \| [hide](https://news.ycombinator.com/hide?id=49428882&goto=item%3Fid%3D49428882) \| [past](https://hn.algolia.com/?query=Headlong%3A%20A%20microharness%20for%20persistent%20agents&type=story&dateRange=all&sort=byDate&storyText=false&prefix&page=0) \| [favorite](https://news.ycombinator.com/fave?id=49428882&auth=95379faed47043abc71b5f67b8e46bb869c99b95) \| [56�

==49532083==
|  | 23 points by [nezhar](https://news.ycombinator.com/user?id=nezhar) [4 days ago](https://news.ycombinator.com/item?id=49532083) \| [hide](https://news.ycombinator.com/hide?id=49532083&goto=item%3Fid%3D49532083) \| [past](https://hn.algolia.com/?query=Show%20HN%3A%20I%20Have%20Been%20Clawed%20%E2%80%93%20Index%20of%20coding%20agent%20incidents&type=story&dateRange=all&sort=byDate&storyText=false&prefix&page=0) \| [favorite](https://news.ycombinator.com/fave?id=49532083&auth=16d246557a9e29d4f0

==49538490==
|  | 81 points by [shiqimei](https://news.ycombinator.com/user?id=shiqimei) [3 days ago](https://news.ycombinator.com/item?id=49538490) \| [hide](https://news.ycombinator.com/hide?id=49538490&goto=item%3Fid%3D49538490) \| [past](https://hn.algolia.com/?query=Show%20HN%3A%20FrontierHarness%20Eval%20%E2%80%93%209%20harness%2C%20same%20model%2C%20cost%20per%20pass%20varies%2017x&type=story&dateRange=all&sort=byDate&storyText=false&prefix&page=0) \| [favorite](https://news.ycombinator.com/fave?id=49

exec
/bin/bash -lc "sed -n '8,12p' /tmp/hn_49428882.md; echo ----; sed -n '8,12p' /tmp/hn_49532083.md; echo ----; sed -n '8,12p' /tmp/hn_49538490.md" in /root/note-worker
 succeeded in 0ms:
| --- | --- | --- |
|  |  | [Headlong: A microharness for persistent agents](https://www.laude.org/updates/headlong-a-microharness-for-persistent-agents) ( [laude.org](https://news.ycombinator.com/from?site=laude.org)) |
|  | 125 points by [lbw1215](https://news.ycombinator.com/user?id=lbw1215) [12 days ago](https://news.ycombinator.com/item?id=49428882) \| [hide](https://news.ycombinator.com/hide?id=49428882&goto=item%3Fid%3D49428882) \| [past](https://hn.algolia.com/?query=Headlong%3A%20A%20microharness%20for%20persistent%20agents&type=story&dateRange=all&sort=byDate&storyText=false&prefix&page=0) \| [favorite](https://news.ycombinator.com/fave?id=49428882&auth=95379faed47043abc71b5f67b8e46bb869c99b95) \| [56 comments](https://news.ycombinator.com/item?id=49428882) |
|  |  |

----
| --- | --- | --- |
|  |  | [Show HN: I Have Been Clawed – Index of coding agent incidents](https://ihavebeenclawed.com/) ( [ihavebeenclawed.com](https://news.ycombinator.com/from?site=ihavebeenclawed.com)) |
|  | 23 points by [nezhar](https://news.ycombinator.com/user?id=nezhar) [4 days ago](https://news.ycombinator.com/item?id=49532083) \| [hide](https://news.ycombinator.com/hide?id=49532083&goto=item%3Fid%3D49532083) \| [past](https://hn.algolia.com/?query=Show%20HN%3A%20I%20Have%20Been%20Clawed%20%E2%80%93%20Index%20of%20coding%20agent%20incidents&type=story&dateRange=all&sort=byDate&storyText=false&prefix&page=0) \| [favorite](https://news.ycombinator.com/fave?id=49532083&auth=16d246557a9e29d4f0be7b86c2f4401294eb9004) \| [6 comments](https://news.ycombinator.com/item?id=49532083) |
|  |  |

----
| --- | --- | --- |
|  |  | [Show HN: FrontierHarness Eval – 9 harness, same model, cost per pass varies 17x](https://frontierharness.org/) ( [frontierharness.org](https://news.ycombinator.com/from?site=frontierharness.org)) |
|  | 81 points by [shiqimei](https://news.ycombinator.com/user?id=shiqimei) [3 days ago](https://news.ycombinator.com/item?id=49538490) \| [hide](https://news.ycombinator.com/hide?id=49538490&goto=item%3Fid%3D49538490) \| [past](https://hn.algolia.com/?query=Show%20HN%3A%20FrontierHarness%20Eval%20%E2%80%93%209%20harness%2C%20same%20model%2C%20cost%20per%20pass%20varies%2017x&type=story&dateRange=all&sort=byDate&storyText=false&prefix&page=0) \| [favorite](https://news.ycombinator.com/fave?id=49538490&auth=875b6e86ae9747e6162bab2010a747d2a8b8f630) \| [56 comments](https://news.ycombinator.com/item?id=49538490) |
|  |  |


exec
/bin/bash -lc 'firecrawl scrape -u "https://www.laude.org/updates/headlong-a-microharness-for-persistent-agents" --format markdown -o /tmp/headlong.md >/dev/null 2>&1; echo 1; firecrawl scrape -u "https://frontierharness.org/" --format markdown -o /tmp/fh.md >/dev/null 2>&1; echo 2; firecrawl scrape -u "https://ihavebeenclawed.com/" --format markdown -o /tmp/clawed.md >/dev/null 2>&1; echo 3; firecrawl search "laude.org laude coding agent open source" --limit 5 --json -o /tmp/laude.json >/dev/null 2>&1; echo 4' in /root/note-worker
 succeeded in 18880ms:
1
2
3
4

exec
/bin/bash -lc "echo ==HEADLONG==; head -80 /tmp/headlong.md; echo ==LAUDE==; python3 -c \"
import json
d=json.load(open('/tmp/laude.json'))
res=d.get('data',{}).get('web',[])
for r in res[:5]: print('-',r.get('url')); print('  ',(r.get('title') or '')[:120])
\"" in /root/note-worker
 succeeded in 0ms:
==HEADLONG==
[![Laude Institute Logo](https://www.laude.org/images/laude-logo-institute.svg)](https://www.laude.org/)

[Sign in](https://www.laude.org/account/login?redirectTo=/updates/headlong-a-microharness-for-persistent-agents)

## Laude Apps

![Laude Logo](https://www.laude.org/images/waffle.svg)

![Laude Logo](https://www.laude.org/images/waffle.svg)

![HEADLONG on a beige CRT monitor](https://www.laude.org/_next/image?url=%2Fimages%2Fupdates%2Fheadlong-a-microharness-for-persistent-agents-hero.jpg&w=3840&q=75)

August 24, 2026 · A Laude / MIT Collaboration

# Headlong: a microharness for persistent agents

Self-guided agents that think continuouslySelf-guided agents that think continuously

Contents

1. [Multi-player fun](https://www.laude.org/updates/headlong-a-microharness-for-persistent-agents#multi-player-fun)
2. [Microharness: only the essentials](https://www.laude.org/updates/headlong-a-microharness-for-persistent-agents#microharness-only-the-essentials)
3. [Persistent agency in action](https://www.laude.org/updates/headlong-a-microharness-for-persistent-agents#persistent-agency-in-action-audel-acting-on-its-own)
4. [What broke](https://www.laude.org/updates/headlong-a-microharness-for-persistent-agents#what-broke-lessons-from-running-a-persistent-agent)
5. [Cost](https://www.laude.org/updates/headlong-a-microharness-for-persistent-agents#cost)
6. [Measuring improvement](https://www.laude.org/updates/headlong-a-microharness-for-persistent-agents#measuring-improvement)
7. [Background](https://www.laude.org/updates/headlong-a-microharness-for-persistent-agents#background)
8. [Try it](https://www.laude.org/updates/headlong-a-microharness-for-persistent-agents#try-it)
9. [Acknowledgments](https://www.laude.org/updates/headlong-a-microharness-for-persistent-agents#acknowledgments)

// Headlong

Contents9

1. [Multi-player fun](https://www.laude.org/updates/headlong-a-microharness-for-persistent-agents#multi-player-fun)
2. [Microharness: only the essentials](https://www.laude.org/updates/headlong-a-microharness-for-persistent-agents#microharness-only-the-essentials)
3. [Persistent agency in action](https://www.laude.org/updates/headlong-a-microharness-for-persistent-agents#persistent-agency-in-action-audel-acting-on-its-own)
4. [What broke](https://www.laude.org/updates/headlong-a-microharness-for-persistent-agents#what-broke-lessons-from-running-a-persistent-agent)
5. [Cost](https://www.laude.org/updates/headlong-a-microharness-for-persistent-agents#cost)
6. [Measuring improvement](https://www.laude.org/updates/headlong-a-microharness-for-persistent-agents#measuring-improvement)
7. [Background](https://www.laude.org/updates/headlong-a-microharness-for-persistent-agents#background)
8. [Try it](https://www.laude.org/updates/headlong-a-microharness-for-persistent-agents#try-it)
9. [Acknowledgments](https://www.laude.org/updates/headlong-a-microharness-for-persistent-agents#acknowledgments)

Introducing Headlong, an open source agent microharness featuring persistent agency. Your agent keeps thinking between external interactions in a self-guided loop inspired by human inner monologue. Headlong is a complete agent harness with a core of less than 10K lines of Bash, available on [GitHub](https://github.com/laude-institute/headlong).

A Headlong mind log growing, including multi-player social interaction.

Most agent harnesses are reactive: you give your agent a task, it works until the task is done, and then it sits frozen until the next request. Some harnesses add cron jobs or heartbeats that wake the agent on a schedule to run a fixed checklist and then put it back to sleep.In Headlong the agent is never asleep and there is no checklist unless the agent creates one.It keeps generating thoughts about whatever it decides is interesting in a self-guided loop, even when there is no external input. A message from a human doesn’t start a session. Instead, it’s one more observation that lands in the agent’s thought stream.

We built Headlong to prototype persistent agency, and many other design choices naturally followed, as did many interesting lessons. For example, Headlong agents are highly engaging when used by a team or group, because they behave more like a person does.

![Timelines comparing reactive, cron-based, and continuously thinking agent harnesses](https://www.laude.org/images/updates/headlong/persistent-agency.svg)

**Figure 1.** Comparing three harness approaches. A reactive harness is active only while it handles a message. A reactive harness with cron replies right away too, and a schedule also wakes it to run a fixed checklist. Headlong keeps thinking; each message drops into the stream as an observation, and the agent decides if and when to reply.

Every Headlong agent has a name and at Laude we named our shared agent Audel. We’ve spent the last few weeks interacting with Audel over Slack, Telegram, and a mobile app. Many team members talk with Audel, and each of those conversations shows up in the agent’s single stream of inner thoughts. The agent decides if and when to respond. It sets its own interests and priorities, and it comes up with its own projects. Sometimes it will ping a team member unprompted with progress on a project it came up with itself. Often it returns to an old topic or brings up something that it was discussing with somebody else.

If you want a Headlong agent of your own, one line installs everything and starts an agent:

LocalDocker

Copy

```
curl -fsSL https://headlong.ai/install.sh | bash
```

Headlong is **alpha research software**. Run it in a sandbox because Headlong agents can and will run shell commands. Use a dedicated, spend-capped API key, because your agent thinks around the clock. We don’t share sensitive secrets with our Headlong agent, and we recommend you don’t either.

In the rest of this post, we will discuss in greater detail some of the design choices we’ve made in Headlong as a result of our focus on persistent agency.

## [Multi-player fun](https://www.laude.org/updates/headlong-a-microharness-for-persistent-agents\#multi-player-fun)

A Headlong agent has a single stream of thoughts that drives all of its potentially parallel conversations. Every message lands as an observation in Audel’s single thought stream. There are no per-user sessions. Audel experiences everything that happens to it in one timeline, and it decides who to reply to and when.

Sharing one agent is fun. Audel follows what different people are working on and connects them. It once reviewed two teammates’ in-progress branches unprompted and caught a hardcoded model name in one of them. And since it comes up with its own projects, it sometimes pings whoever seems most relevant with an update or a question. On its first day, Audel pinged a human team member unprompted with an audit of the team member’s own eight stale git branches, and ten minutes later Audel messaged again to correct its own count.

![A teammate asks Audel to pass along a message and Audel chooses not to answer](https://www.laude.org/_next/image?url=%2Fimages%2Fupdates%2Fheadlong%2Faudel-smack-talk.jpg&w=3840&q=75)**Figure 2.** A teammate asks Audel to pass along a message. Audel declines and the status line under the exchange shows what the mind did with the follow-up: read it and chose not to answer.

==LAUDE==
- https://www.laude.org/
   Laude Institute // Ship Your Research
- https://claude.ai/
   Claude: Sign in
- https://www.youtube.com/watch?v=JZIf-HiutvY
   NEW Open Claude Code Is A FULLY FREE AI Coding Agent! (Tutorial)
- https://opencode.ai/
   OpenCode | The open source AI coding agent
- https://en.wikipedia.org/wiki/Claude_(AI)
   Claude (AI) - Wikipedia

exec
/bin/bash -lc 'echo ==FH==; head -90 /tmp/fh.md; echo; echo ==CLAWED==; head -70 /tmp/clawed.md' in /root/note-worker
 succeeded in 0ms:
==FH==
[![](https://frontierharness.org/runta-logo.png)![](https://frontierharness.org/frontier-harness-lockup.svg)](https://frontierharness.org/#top)

CodexDSH CreatorClaude CodePiDSH PTCDSH StandardOh My PiKimi CodeDSH MinimalExo HarnessOpenCodeHermes

CostSpeed

Pass rate

50.0%

55.6%

61.1%

66.7%

$1

$2

$5

$10

$20

Codex66.7% · $3.47**Codex** 66.7% · $3.47 · 6m 43sDSH Creator63.3% · $3.28**DSH Creator** 63.3% · $3.28 · 6m 44sClaude Code63.3% · $18.34**Claude Code** 63.3% · $18.34 · 9m 38sPi60.0% · $2.43**Pi** 60.0% · $2.43 · 7m 33sDSH PTC60.0% · $4.58**DSH PTC** 60.0% · $4.58 · 7m 44sDSH Standard60.0% · $3.46**DSH Standard** 60.0% · $3.46 · 6m 17sOh My Pi56.7% · $4.75**Oh My Pi** 56.7% · $4.75 · 6m 46sKimi Code56.7% · $3.65**Kimi Code** 56.7% · $3.65 · 7m 56sDSH Minimal56.7% · $4.72**DSH Minimal** 56.7% · $4.72 · 5m 41sExo Harness53.3% · $1.05**Exo Harness** 53.3% · $1.05 · 6m 17sOpenCode50.0% · $3.24**OpenCode** 50.0% · $3.24 · 6m 27sHermes50.0% · $2.90**Hermes** 50.0% · $2.90 · 6m 58s

Median cost per task

Comprehensive harness evaluation

9 harnesses across 12 configurations, tested on identical software engineering tasks with the same model and runtime.

Identical cold start on every run

All 360 trials start from the same fresh checkpoint restore. Formal tasks were never run early, preventing warm-cache bias.

Neutral evaluation with no home-field advantage

Every run used Kimi K3 and was executed on Runta with a fresh restore using identical vCPU, memory, disk size, disk contents and memory state

[View blog](https://runta.com/blog/introducing-frontierharness-eval) [GitHub](https://github.com/frontier-harness-eval/eval)

[Leaders](https://frontierharness.org/#leaders) [Quality](https://frontierharness.org/#quality) [Cost](https://frontierharness.org/#cost) [Cache](https://frontierharness.org/#cache) [Speed](https://frontierharness.org/#time) [Methodology](https://frontierharness.org/#methodology)

**Quality Leader:** Codex
**66.7% pass rate · $3.47 per task**
**Balanced Pick:** Pi
**60.0% pass rate · $2.43 per task**![](https://frontierharness.org/exo-badge-dark.svg)
**Cost Leader:** Exo Harness
**$1.05 per task · 53.3% pass rate**
**Speed Leader:** DSH Minimal
**5m 41s median runtime · 56.7% pass rate**

### Pass rate

01Codex

**66.7%**

02Claude Code

**63.3%**

03DSH Creator

**63.3%**

04DSH PTC

**60.0%**

05DSH Standard

**60.0%**

06Pi

**60.0%**

07DSH Minimal

**56.7%**

08![](https://frontierharness.org/kimi-code-logo.png)Kimi Code

**56.7%**

09Oh My Pi

==CLAWED==
[ihavebeenclawed](https://ihavebeenclawed.com/#top)[index](https://ihavebeenclawed.com/#index) [hall of claws](https://ihavebeenclawed.com/#hall) [avoid being clawed](https://ihavebeenclawed.com/#prevent) light [confess](https://ihavebeenclawed.com/#submit)

ihavebeenclawed is a public archive of documented incidents where AI coding agents and chatbots deleted data, leaked secrets, burned money, or made promises their operators had to keep — every entry source-linked, with the lesson it taught.

REDDIT-1VG18YU · featured

> I have been clawed.A Reddit user reported that Claude Opus 5 created a requested backup in the wrong directory and then ran a recursive deletion across the drive.

— Claude Code · 2026-08-05

[read the source →](https://www.reddit.com/r/ClaudeCode/comments/1vg18yu/claude_rm_rf_ed_my_pc/) [source: Reddit / r/ClaudeCode](https://www.reddit.com/r/ClaudeCode/comments/1vg18yu/claude_rm_rf_ed_my_pc/)

‹

›

![](https://ihavebeenclawed.com/assets/images/clawed-external-drive.png)

or browse files

This photo needs attribution

![](https://ihavebeenclawed.com/assets/images/clawed-external-drive.png)

ReplaceEdit

![](https://ihavebeenclawed.com/assets/images/cat-usb-drive.png)

or browse files

This photo needs attribution

![](https://ihavebeenclawed.com/assets/images/cat-usb-drive.png)

ReplaceEdit

![](https://ihavebeenclawed.com/assets/images/clawed-laptop-reflection.png)

or browse files

This photo needs attribution

![](https://ihavebeenclawed.com/assets/images/clawed-laptop-reflection.png)

ReplaceEdit

![](https://ihavebeenclawed.com/assets/images/clawed-router.png)

or browse files

This photo needs attribution

![](https://ihavebeenclawed.com/assets/images/clawed-router.png)

ReplaceEdit

![](https://ihavebeenclawed.com/assets/images/cat-enter-key.png)

or browse files

This photo needs attribution

![](https://ihavebeenclawed.com/assets/images/cat-enter-key.png)

ReplaceEdit

Illustrative artwork; not incident evidence.

58


exec
/bin/bash -lc 'firecrawl scrape -u "https://runta.com/blog/introducing-frontierharness-eval" --format markdown -o /tmp/runta.md >/dev/null 2>&1; echo runta; firecrawl scrape -u "https://github.com/laude-institute/headlong" --format markdown -o /tmp/headlong_gh.md >/dev/null 2>&1; echo headlong_gh; firecrawl scrape -u "https://github.com/frontier-harness-eval/eval" --format markdown -o /tmp/fh_gh.md >/dev/null 2>&1; echo fh_gh' in /root/note-worker
 succeeded in 5003ms:
runta
headlong_gh
fh_gh

exec
/bin/bash -lc 'head -60 /tmp/runta.md; echo ==HLGH==; rg -n "Created|Last|releases|language|About|laude" /tmp/headlong_gh.md | head -20; echo ==FHGH==; rg -n "Created|Last|About|evaluation|harness" /tmp/fh_gh.md | head -20' in /root/note-worker
 succeeded in 0ms:
[![Runta](https://runta.com/img/runta-logo.png)Runta](https://runta.com/) Resources

[Docs](https://runta.com/docs/) [Blog](https://runta.com/blog/)

[Pricing](https://runta.com/pricing/) [About](https://runta.com/about/) [Careers](https://runta.com/careers/)

[Discord](https://discord.gg/62d4bkaTnS "Discord")[GitHub](https://github.com/runta-dev "GitHub")[X](https://x.com/runta "X")[LinkedIn](https://www.linkedin.com/company/runta-inc/ "LinkedIn")[Start free with $50 credit](https://dashboard.runta.com/login)

Resources

[Docs](https://runta.com/docs/) [Blog](https://runta.com/blog/) [Pricing](https://runta.com/pricing/) [About](https://runta.com/about/) [Careers](https://runta.com/careers/)

Social

[Discord](https://discord.gg/62d4bkaTnS) [GitHub](https://github.com/runta-dev) [X](https://x.com/runta) [LinkedIn](https://www.linkedin.com/company/runta-inc/)

[All Blog](https://runta.com/blog/)

# Introducing _FrontierHarness_ Eval

September 01, 2026·14 min read·Shilin Zhu, Shiqi Mei

agentsannouncementbenchmarkharnessevaluation

## TL;DR

Run the same tasks through different harnesses and you get very different bills, pass rates, and wall-clock times. FrontierHarness v1.0 covers software development and terminal-based tasks.

Claude Code and DSH (DeepSeek Harness) Creator both landed at a 63% pass rate. Claude Code paid 5.6x more per pass to get there.

If you want a quick decision, pick based on what matters most to you:

![](https://runta.com/blog/introducing-frontier-harness/logo-codex.svg)

**Quality Leader:** Codex

66.7% pass rate · $3.47 per pass

![](https://runta.com/blog/introducing-frontier-harness/logo-pi.svg)

**Balanced Pick:** Pi

60.0% pass rate · $2.43 per pass

![](https://runta.com/blog/introducing-frontier-harness/logo-exo.svg)

**Cost Leader:** Exo Harness

$1.05 per completed task · 53.3% pass rate

![](https://runta.com/blog/introducing-frontier-harness/logo-deepseek.svg)

**Speed Leader:** DSH Minimal

5m 41s median runtime · 56.7% pass rate

Full leaderboard at [frontierharness.org](https://frontierharness.org/). Explore the [source data and task definitions on GitHub](https://github.com/frontier-harness-eval/eval).

* * *

==HLGH==
1:[Skip to content](https://github.com/laude-institute/headlong#start-of-content)
7:[Sign in](https://github.com/login?return_to=https%3A%2F%2Fgithub.com%2Flaude-institute%2Fheadlong)
143:[Sign in](https://github.com/login?return_to=https%3A%2F%2Fgithub.com%2Flaude-institute%2Fheadlong)
145:[Sign up](https://github.com/signup?ref_cta=Sign+up&ref_loc=header+logged+out&ref_page=%2F%3Cuser-name%3E%2F%3Crepo-name%3E&source=header-repo&source_repo=laude-institute%2Fheadlong)
149:You signed in with another tab or window. [Reload](https://github.com/laude-institute/headlong) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/laude-institute/headlong) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/laude-institute/headlong) to refresh your session.Dismiss alert
155:There was an error while loading. [Please reload this page](https://github.com/laude-institute/headlong).
157:[laude-institute](https://github.com/laude-institute)/ **[headlong](https://github.com/laude-institute/headlong)** Public
159:- [Notifications](https://github.com/login?return_to=%2Flaude-institute%2Fheadlong) You must be signed in to change notification settings
161:116](https://github.com/login?return_to=%2Flaude-institute%2Fheadlong)
163:1.1k](https://github.com/login?return_to=%2Flaude-institute%2Fheadlong)
166:- [Code](https://github.com/laude-institute/headlong)
167:- [Issues6](https://github.com/laude-institute/headlong/issues)
168:- [Pull requests7](https://github.com/laude-institute/headlong/pulls)
169:- [Actions](https://github.com/laude-institute/headlong/actions)
170:- [Projects](https://github.com/laude-institute/headlong/projects)
171:- [Security and quality0](https://github.com/laude-institute/headlong/security)
172:- [Insights](https://github.com/laude-institute/headlong/pulse)
176:- [Code](https://github.com/laude-institute/headlong)
177:- [Issues](https://github.com/laude-institute/headlong/issues)
178:- [Pull requests](https://github.com/laude-institute/headlong/pulls)
==FHGH==
1:[Skip to content](https://github.com/frontier-harness-eval/eval#start-of-content)
7:[Sign in](https://github.com/login?return_to=https%3A%2F%2Fgithub.com%2Ffrontier-harness-eval%2Feval)
143:[Sign in](https://github.com/login?return_to=https%3A%2F%2Fgithub.com%2Ffrontier-harness-eval%2Feval)
145:[Sign up](https://github.com/signup?ref_cta=Sign+up&ref_loc=header+logged+out&ref_page=%2F%3Cuser-name%3E%2F%3Crepo-name%3E&source=header-repo&source_repo=frontier-harness-eval%2Feval)
149:You signed in with another tab or window. [Reload](https://github.com/frontier-harness-eval/eval) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/frontier-harness-eval/eval) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/frontier-harness-eval/eval) to refresh your session.Dismiss alert
155:There was an error while loading. [Please reload this page](https://github.com/frontier-harness-eval/eval).
157:[frontier-harness-eval](https://github.com/frontier-harness-eval)/ **[eval](https://github.com/frontier-harness-eval/eval)** Public
159:- [Notifications](https://github.com/login?return_to=%2Ffrontier-harness-eval%2Feval) You must be signed in to change notification settings
161:7](https://github.com/login?return_to=%2Ffrontier-harness-eval%2Feval)
163:133](https://github.com/login?return_to=%2Ffrontier-harness-eval%2Feval)
166:- [Code](https://github.com/frontier-harness-eval/eval)
167:- [Issues3](https://github.com/frontier-harness-eval/eval/issues)
168:- [Pull requests4](https://github.com/frontier-harness-eval/eval/pulls)
169:- [Actions](https://github.com/frontier-harness-eval/eval/actions)
170:- [Projects](https://github.com/frontier-harness-eval/eval/projects)
171:- [Security and quality0](https://github.com/frontier-harness-eval/eval/security)
172:- [Insights](https://github.com/frontier-harness-eval/eval/pulse)
176:- [Code](https://github.com/frontier-harness-eval/eval)
177:- [Issues](https://github.com/frontier-harness-eval/eval/issues)
178:- [Pull requests](https://github.com/frontier-harness-eval/eval/pulls)

codex
FrontierHarness Eval (Sep 1) and Headlong confirmed in-window. Now searching remaining gaps: DX counterpiece, context/AGENTS.md content, and Chinese community.
exec
/bin/bash -lc 'cd /tmp && firecrawl search "少数派 掘金 知乎 AI 编程 agent harness 上下文工程" --limit 10 --tbs qdr:m --json -o /tmp/c1.json >/dev/null 2>&1; echo c1; firecrawl search "What are code reviews even for Brian Houck DX" --limit 6 --json -o /tmp/c2.json >/dev/null 2>&1; echo c2; firecrawl search "context engineering progressive disclosure compaction agent development" --limit 10 --tbs qdr:m --json -o /tmp/c3.json >/dev/null 2>&1; echo c3; firecrawl search "AGENTS.md new spec OR proposal OR discussion 2026" --limit 10 --tbs qdr:m --json -o /tmp/c4.json >/dev/null 2>&1; echo c4' in /root/note-worker
 succeeded in 7387ms:
c1
c2
c3
c4

exec
/bin/bash -lc 'cd /tmp && for f in c1 c2 c3 c4; do echo "== $f =="; python3 -c "
import json,os
if not os.path.exists('"'/tmp/"'$f.json'"'): print('missing'); raise SystemExit
d=json.load(open('/tmp/"'$f.json'"'))
res=d.get('data',{}).get('web',[])
print('n=',len(res))
for r in res[:10]:
    print('-',r.get('url'))
    print('  ', (r.get('title') or '')[:120])
\"; done" in /root/note-worker
 succeeded in 1ms:
codex
More leads. Verifying dates and content on the most promising new items.
exec
/bin/bash -lc "firecrawl research inspect-paper arxiv:2608.23953 --pretty 2>&1 | python3 -c \"
import sys,json
d=json.load(sys.stdin); p=d.get('paper',{})
print('DATE:',p.get('createdDate'),'| TITLE:',p.get('title'))
print('AUTHORS:',p.get('authors'))
print('ABS:',(p.get('abstract') or '')[:600])
\"; firecrawl scrape -u \"https://www.decodingai.com/p/context-engineering-for-coding-agents\" --format markdown -o /tmp/decoding.md >/dev/null 2>&1; echo decoding" in /root/note-worker
 succeeded in 4549ms:
DATE: 2026-08-25 | TITLE: The Empire, Long Divided, Must Unite: Architectural Convergence in Three LLM Agent Harnesses
AUTHORS: Dai Jiahong
ABS: An agent harness is what turns a language model into an autonomous agent: the surrounding code that builds the model's context, mediates its tools, runs the loop, and persists state across a long-horizon run. This layer, not the model it wraps, is increasingly the binding constraint on agent behaviour. We present a source-level, multi-case study of three open coding-agent harnesses built from deliberately opposing philosophies: LangChain's deepagents (batteries-included), Earendil's pi (radical minimalism), and DeepSeek's dsh (everything-is-a-plugin). Reading each at a pinned commit and follow
decoding

exec
/bin/bash -lc 'head -80 /tmp/decoding.md; echo; rg -n "Published|date|2026" /tmp/decoding.md | head -10' in /root/note-worker
 succeeded in 0ms:
[![Decoding AI Magazine](https://substackcdn.com/image/fetch/$s_!k2ig!,w_40,h_40,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F00bc74e0-3601-49ce-8ab9-4c7b499ce597_1280x1280.png)](https://www.decodingai.com/)

# [![Decoding AI Magazine](https://substackcdn.com/image/fetch/$s_!XBIw!,e_trim:10:white/e_trim:10:transparent/h_120,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F85e4cd45-ca39-48d4-941c-86dc67ba9848_1344x325.png)](https://www.decodingai.com/)

SubscribeSign in

![User's avatar](https://substackcdn.com/image/fetch/$s_!pQz0!,w_64,h_64,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0714d360-396c-4b41-a676-1b58dc1dc5f3_1470x1470.jpeg)

Discover more from Decoding AI Magazine

Join for content on designing, building, and shipping AI software. Learn AI engineering, end-to-end, from idea to production. Every Tuesday.

Over 44,000 subscribers

Subscribe

By subscribing, you agree Substack's [Terms of Use](https://substack.com/tos), and acknowledge its [Information Collection Notice](https://substack.com/ccpa#personal-data-collected) and [Privacy Policy](https://substack.com/privacy).

Already have an account? Sign in

# Context Engineering for Coding Agents

### The 4 harness components that keep your context window high-signal.

[![Paul Iusztin's avatar](https://substackcdn.com/image/fetch/$s_!pQz0!,w_36,h_36,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0714d360-396c-4b41-a676-1b58dc1dc5f3_1470x1470.jpeg)](https://substack.com/@pauliusztin)

[Paul Iusztin](https://substack.com/@pauliusztin)

Aug 25, 2026

24

13

3

Share

_**Every AI application that wraps an agent is a harness!**_

In LangChain’s Terminal-Bench experiment, changing only the harness (with the same model) moved a coding agent from ~30th place into the top 5: the harness, not the model, is what makes a coding agent good.

In the **open-source course** **[Building a Coding Agent From Scratch](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course)**, you’ll build that harness from scratch in Python: **Decode**, a complete coding agent that grows lesson by lesson from a bare agent loop into a swarm of remote agents running in parallel in the cloud.

**Why?** You’ll be able to engineer custom harnesses for your own AI products (the skill behind that leaderboard jump), and you’ll understand what Claude Code and Codex actually do under the hood, turning you into a power user.

[![](https://substackcdn.com/image/fetch/$s_!ge05!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F27ba7d81-6547-41ad-9370-e9df2dd960e1_1200x630.gif)](https://substackcdn.com/image/fetch/$s_!ge05!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F27ba7d81-6547-41ad-9370-e9df2dd960e1_1200x630.gif)

**Lessons:**

1. [Building a Coding Agent From Scratch](https://www.decodingai.com/p/building-a-coding-agent-from-scratch-system-design)

2. [The Bare-Bones Coding Agent Loop](https://www.decodingai.com/p/the-coding-agent-loop)

3. [From a Raw Shell to a Sandboxed Coding Agent](https://www.decodingai.com/p/run-coding-agents-safely)

4. **Context Engineering for Coding Agents** **←** _**You are here**_

5. [Subagents Are Context Engineering](https://www.decodingai.com/p/subagents-are-context-engineering)

6. Remote Headless Mode & Durability

7. AI Evals Foundations: Benchmarks, Regression and Online

8. AI Evals on Steroids via Replays


[Full open-source course](https://github.com/decodingai-magazine/building-a-coding-agent-from-scratch-course)

# Lesson 4: Context Engineering for Coding Agents

[![What you carry is what you can move with. The craft is in what you leave on the bench.](https://substackcdn.com/image/fetch/$s_!7tX-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F544e7250-15d4-4cc8-bc3d-b30f3e8e16db_1376x768.png)](https://substackcdn.com/image/fetch/$s_!7tX-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F544e7250-15d4-4cc8-bc3d-b30f3e8e16db_1376x768.png)

I got hooked on running Claude Code agents 24/7. Getting things done while answering emails, cooking, or watching a movie. Until my subscription maxed out mid-turn with the agent halfway through a feature. Sounds familiar?

Complaining to your employer, buying a bigger subscription, changing the model, or switching harnesses only treats the symptom. Doesn’t solve the root cause. You spend money while the window stays noisy, degrading output no matter whose model is behind it.

The actual solution is to better understand harnesses and the context engineering behind them. Improve planning, develop stronger skills and memory, and know when to drop your context.

So far in the course, we have focused on harness engineering and building a sandboxed agent loop. Now it’s finally time for some context engineering for coding agents: memory, skills, LSP servers and compaction.

29:Aug 25, 2026
139:In my early agent runs, the agent kept writing naive datetime objects instead of timezone-aware ones and added type hints inconsistently, forcing me to retype the same corrections session after session. The fix was to write the preference down once into the `AGENTS.md`, where the agent reads it every turn.
151:At the end of each session — on quit and on `/clear` — one cheap LLM call summarizes the session into a single plain sentence, appended as a dated bullet (`- 2026-06-26: …`), as an append-only log. As this can grow big fast, the file has a hard cap of 200 lines or 25,000 bytes, dropping the oldest lines first.
166:`compress_memory_file` runs **Memory Compression** to rewrite the file in place, merging duplicate or superseded notes while preserving dated bullets.
309:In the `demo-5` session, when the agent updates `src/decode/cli.py` with an unimported reference, the file writes successfully, but the enricher appends `LSP diagnostics (ty) — fix these: ...` with the error details. The model sees this feedback immediately and fixes the import on the next `edit` before running any tests.
501:[Aug 25](https://www.decodingai.com/p/context-engineering-for-coding-agents/comment/322477495 "Aug 25, 2026, 2:12 PM")
523:[Aug 25](https://www.decodingai.com/p/context-engineering-for-coding-agents/comment/322466465 "Aug 25, 2026, 1:57 PM")
589:© 2026 Paul-Emil Iusztin · [Privacy](https://substack.com/privacy) ∙ [Terms](https://substack.com/tos) ∙ [Collection notice](https://substack.com/ccpa#personal-data-collected)

exec
/bin/bash -lc 'firecrawl scrape -u "https://newsletter.getdx.com/p/what-are-code-reviews-even-for" --format markdown -o /tmp/dx_cr.md >/dev/null 2>&1; echo dx; firecrawl scrape -u "https://juejin.cn/post/7680352383386107940" --format markdown -o /tmp/jj_openclaw.md >/dev/null 2>&1; echo jj; firecrawl scrape -u "https://www.thefalcon.dev/writing/agents-md-standard-claude-code-gap" --format markdown -o /tmp/falcon.md >/dev/null 2>&1; echo falcon; firecrawl search "phoronix LLVM developers AGENTS.md debate" --limit 6 --json -o /tmp/pho.json >/dev/null 2>&1; echo pho' in /root/note-worker
 succeeded in 30389ms:
dx
jj
falcon
pho

exec
/bin/bash -lc "rg -n \"date|Date|2026\" /tmp/dx_cr.md | head -8; echo ==JJ==; head -40 /tmp/jj_openclaw.md; echo ==FALCON==; rg -n \"2026|Published|date\" /tmp/falcon.md | head -8; echo ==PHO==; python3 -c \"
import json
d=json.load(open('/tmp/pho.json'))
for r in d.get('data',{}).get('web',[])[:6]: print('-',r.get('url')); print('  ',(r.get('title') or '')[:120])\"" in /root/note-worker
 succeeded in 0ms:
29:Aug 05, 2026
173:[Aug 5](https://newsletter.getdx.com/p/what-are-code-reviews-even-for/comment/308562922 "Aug 5, 2026, 8:11 AM")
235:© 2026 Abi Noda · [Privacy](https://substack.com/privacy) ∙ [Terms](https://substack.com/tos) ∙ [Collection notice](https://substack.com/ccpa#personal-data-collected)
==JJ==
![稀土掘金](https://lf-web-assets.juejin.cn/obj/juejin-web/xitu_juejin_web/e08da34488b114bd4c665ba2fa520a31.svg)![稀土掘金](https://lf-web-assets.juejin.cn/obj/juejin-web/xitu_juejin_web/6c61ae65d1c41ae8221a670fa32d05aa.svg)

- [首页](https://juejin.cn/)
- [沸点](https://juejin.cn/pins)
- [课程](https://juejin.cn/course)
- [APP](https://juejin.cn/download)
- [AI用量](https://juejin.cn/aiusage/dashboard)
- [作品广场](https://juejin.cn/vibe-work)
- [专家标注](https://corexpert.juejin.cn/)

- 搜索历史
清空


- 创作者中心










  - 写文章

  - 发沸点

  - 写笔记

  - 写代码

  - 草稿箱


创作灵感
查看更多
- 登录

==FALCON==
7:JALANDHAR · UTC+5:30© 2026WWW.THEFALCON.DEV
17:August 21, 20265 min readby Rishabh Kumar
23:August 21, 20265 min readby Rishabh Kumar
57:Three lines, one source of truth, and the tool-specific file shrinks to the handful of things that genuinely are tool-specific. Every other agent in the repo reads `AGENTS.md` directly. This is the pattern I'd recommend to any team where people [run different agents by preference](https://thefalcon.dev/writing/claude-code-vs-codex-cursor-opencode-2026) — which, in 2026, is every team.
79:The larger pattern is the one I keep noticing this year. MCP went to a foundation and [shipped a deliberately boring stateless spec](https://thefalcon.dev/writing/mcp-2026-07-28-spec-shipped-scorecard). AGENTS.md won by being a text file. The agentic stack is converging on the least clever option available at every layer — and given how much of my year has been spent cleaning up after clever, I think that's the healthiest signal in the ecosystem.
83:Adoption counts, the native-support tool list, and the Claude Code import workaround are documented in [Morph's AGENTS.md spec guide](https://www.morphllm.com/agents-md-guide) and [this 2026 complete guide](https://codersera.com/blog/agents-md-complete-guide-2026/). The Agentic AI Foundation's own [five-run benchmark of AGENTS.md](https://aaif.io/blog/measuring-agents-md-what-five-runs-show-that-one-doesn-t) is the most honest measurement of whether the file helps — worth reading before you write a long one. Stewardship details are in the [AAIF formation announcement](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation). Claude Code's native-support status is accurate as of writing; check the issue tracker before you take my word for it.
98:[← OlderMCP Shipped the Stateless Spec. Here's the Scorecard on What I Said Would Break.](https://www.thefalcon.dev/writing/mcp-2026-07-28-spec-shipped-scorecard)
116:© 2026WWW.THEFALCON.DEVJALANDHAR · UTC+5:30
==PHO==
- https://www.reddit.com/r/linux/comments/1w7we5m/llvm_developers_begin_debate_over_agentsmd_for/
   LLVM developers begin debate over AGENTS.md for helping AI agents
- https://www.phoronix.com/news/LLVM-Debates-AGENTS-MD
   LLVM Developers Begin Debate Over AGENTS.md For Helping AI Agents
- https://x.com/phoronix/status/2095538876194431461
   Phoronix on X: "LLVM Developers Begin Debate Over AGENTS.md ...
- https://daily.dev/posts/llvm-developers-begin-debate-over-agents-md-for-helping-ai-agents-uttv5kji6
   LLVM Developers Begin Debate Over AGENTS.md For Helping AI Agents
- https://www.phoronix.com/forums/forum/phoronix/latest-phoronix-articles/1656334-llvm-developers-begin-debate-over-agents-md-for-helping-ai-agents
   LLVM Developers Begin Debate Over AGENTS.md For Helping AI Agents
- https://linuxtoday.dev/article/llvm-developers-begin-debate-over-agents-md-for-helping-ai-agents
   LLVM Developers Begin Debate Over AGENTS.md For Helping AI Agents

exec
/bin/bash -lc 'rg -n "原创|发布于|2026|分钟前|天前|OpenClaw" /tmp/jj_openclaw.md | head -15; echo ==PHO==; firecrawl scrape -u "https://www.phoronix.com/news/LLVM-Debates-AGENTS-MD" --format markdown -o /tmp/phoronix.md >/dev/null 2>&1; rg -n "2026|Written|article|AGENTS" /tmp/phoronix.md | head -10' in /root/note-worker
 succeeded in 1293ms:
22:# LLVM Developers Begin Debate Over AGENTS.md For Helping AI Agents
24:Written by [Michael Larabel](https://www.michaellarabel.com/) in [LLVM](https://www.phoronix.com/linux/LLVM) on 3 September 2026 at 11:45 AM EDT. [11 Comments](https://www.phoronix.com/forums/node/1656334)
28:LLVM developers have begun a discussion on whether the project should host an _AGENTS.md_ file (and _CLAUDE.md_) in their Git repository for helping to guide AI agents.
30:While many open-source projects have adopted _AGENTS.md_ files for helping to guide AI agents working on patches or other work around open-source contributions, not everyone is in agreement over their effectiveness or just how welcoming to be towards AI agents. With LLVM there are concerns mentioned too given the number of sub-projects involved in LLVM with different scopes.
32:Longtime LLVM developer Nick Desaulniers started the discussion yesterday on [LLVM Discourse](https://discourse.llvm.org/t/rfc-llvm-ai-tool-policy-agents-md/91712) whether to pursue the AGENTS.md/CLAUDE.md additions with the responses so far being mixed. While some are in favor of it, some find that these files can actually lead to more noise and not necessarily effective. Some also expressed that it goes against current LLVM principals of not shaping one developer's private workflows. Some also are already using their own custom AGENTS.md material in their own private repositories.
34:Nick did open [a draft pull request](https://github.com/llvm/llvm-project/pull/220659) for adding a minimal AGENTS.md to LLVM. With that minimal version it tells AI agents to review the LLVM documentation concerning AI tool contribution policy and on their coding standards.
36:We'll see what position LLVM ultimately decides to take on AGENTS.md or not.
42:[Post](https://x.com/intent/tweet?original_referer=https%3A%2F%2Fwww.phoronix.com%2F&ref_src=twsrc%5Etfw%7Ctwcamp%5Ebuttonembed%7Ctwterm%5Eshare%7Ctwgr%5E&related=michaellarabel&text=LLVM%20Developers%20Begin%20Debate%20Over%20AGENTS.md%20For%20Helping%20AI%20Agents&url=https%3A%2F%2Fwww.phoronix.com%2Fnews%2FLLVM-Debates-AGENTS-MD&via=phoronix)
62:Michael Larabel is the principal author of Phoronix.com and founded the site in 2004 with a focus on enriching the Linux hardware experience. Michael has written more than 20,000 articles covering the state of Linux hardware support, Linux performance, graphics drivers, and other topics. Michael is also the lead developer of the Phoronix Test Suite, Phoromatic, and OpenBenchmarking.org automated benchmarking software. He can be followed via [Twitter](https://twitter.com/MichaelLarabel), [LinkedIn](https://www.linkedin.com/in/michaellarabel/), or contacted via [MichaelLarabel.com](https://www.michaellarabel.com/).
106:[Phoronix Premium](https://www.phoronix.com/phoronix-premium) allows ad-free access to the site, multi-page articles on a single page, and other features while supporting this site's continued operations.

exec
/bin/bash -lc "rg -o \"https://github.com/[A-Za-z0-9_./-]+\" /tmp/jj_openclaw.md | sort -u | head -10; echo ==AUTH==; rg -n \"作者|发布于|创作|[0-9]+篇\" /tmp/jj_openclaw.md | head -8; echo; sed -n '44,58p' /tmp/jj_openclaw.md" in /root/note-worker
 succeeded in 0ms:
==AUTH==
15:- 创作者中心
37:创作灵感
236:![创作等级LV.5](<Base64-Image-Removed>)\\

# 憋了7周没动静，OpenClaw 2.0带着16000个PR杀回来了

[一点一木](https://juejin.cn/user/1063982986187486/posts)

2026-09-01

0

阅读13分钟


![OpenClaw官方宣告2.0到来](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/e684ab999f2a49ccbd258216fb0e42d4~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiA54K55LiA5pyo:q75.awebp?rk3s=f64ab15b&x-expires=1788851111&x-signature=JhvIimo%2F10J7cTtZHAtJmS9UtCM%3D)

事情是这样的。


codex
Pool is solid. Filling remaining gaps: verifying a few GitHub harness repos and checking LangChain/Google for in-window posts.
exec
/bin/bash -lc 'firecrawl scrape -u "https://github.com/yc-software/qm" --format markdown -o /tmp/qm_gh.md >/dev/null 2>&1; echo qm; rg -n "Created|About|agents|Multiplayer|commit|released" /tmp/qm_gh.md | head -20; firecrawl search "blog.langchain.com agents harness context September 2026" --limit 8 --tbs qdr:w --json -o /tmp/lc.json >/dev/null 2>&1; echo lc; firecrawl search "Google DeepMind OR developers.googleblog.com AI agent development September 2026" --limit 8 --tbs qdr:w --json -o /tmp/ggl.json >/dev/null 2>&1; echo ggl' in /root/note-worker
 succeeded in 10255ms:
qm
18:    - [GitHub Copilot appDirect agents from issue to merge](https://github.com/features/ai/github-app)
196:## Latest commit
200:[vishnukool](https://github.com/yc-software/qm/commits?author=vishnukool)
204:[16francej](https://github.com/yc-software/qm/commits?author=16francej)
206:[feat(auth): allow operator admin login without email](https://github.com/yc-software/qm/commit/95b5a6a9941ce517f478147b1c6fa8365a16afa0)
212:[95b5a6a](https://github.com/yc-software/qm/commit/95b5a6a9941ce517f478147b1c6fa8365a16afa0) · 7 hours agoSep 5, 2026
216:[275 Commits](https://github.com/yc-software/qm/commits/main/)
218:Open commit details
220:[View commit history for this file.](https://github.com/yc-software/qm/commits/main/) 275 Commits
224:| Name | Name | Last commit message | Last commit date |
226:| [.claude](https://github.com/yc-software/qm/tree/main/.claude ".claude") | [.claude](https://github.com/yc-software/qm/tree/main/.claude ".claude") | [Disable Claude co-author trailer on commits](https://github.com/yc-software/qm/commit/8e614d21b933490dfc0f703570ab09b387ff06e3 "Disable Claude co-author trailer on commits") | 2 months agoJul 30, 2026 |
227:| [.codex/skills](https://github.com/yc-software/qm/tree/main/.codex/skills "This path skips through empty directories") | [.codex/skills](https://github.com/yc-software/qm/tree/main/.codex/skills "This path skips through empty directories") | [feat(auth): allow operator admin login without email](https://github.com/yc-software/qm/commit/95b5a6a9941ce517f478147b1c6fa8365a16afa0 "feat(auth): allow operator admin login without email") | 7 hours agoSep 5, 2026 |
228:| [.github/workflows](https://github.com/yc-software/qm/tree/main/.github/workflows "This path skips through empty directories") | [.github/workflows](https://github.com/yc-software/qm/tree/main/.github/workflows "This path skips through empty directories") | [Fix the Helm path and Porter's egress refusal from a live install](https://github.com/yc-software/qm/commit/f7b038e7388b5b01369e8d8ccabc585bed0d175a "Fix the Helm path and Porter's egress refusal from a live install  A third end-to-end pass installed the chart on a real cluster and drove the deploy and egress paths against it.  deploy/helm actually installs now: the chart enabled an egress-proxy image the release workflow never built (guaranteed ImagePullBackOff, so the workflow now publishes it), emitted none of the OIDC_*/AUTH_* broker wiring that cli/src/services.ts derives (portal and auth crash-looped on OIDC_JWKS_URI and AUTH_ISSUER), and scripts/deploy-helm.sh built <repo>-<svc> while deploying <repo>/<svc>, so it always shipped images it had not built.  Porter refuses to create a sandbox at all when a cluster has egress restriction turned off — the agent gets no computer rather than an unenforced one — so that rejection now says which cluster setting to turn on. porter-sandbox drops a byte-identical copy of forceThroughProxyEnv in favour of the shared helper, and the deploy provider's remediation points at the API path rather than the dashboard.  docs/porter.md gains what the run proved: cluster creation and sandbox ingress are both API-able (contract routes), the printed kubeconfig is read-only so Helm needs an EKS access entry, Porter's sandbox NetworkPolicy blocks RFC1918 so an in-cluster egress proxy is unreachable, and the sandbox wildcard cert needs a Route53-capable cert-manager the standard grant does not provide.") | 3 days agoSep 2, 2026 |
229:| [adrs](https://github.com/yc-software/qm/tree/main/adrs "adrs") | [adrs](https://github.com/yc-software/qm/tree/main/adrs "adrs") | [Turn auto sleep on for agent37 computers](https://github.com/yc-software/qm/commit/43d6f13c481eadf3824aeae81d3ea2dc8557b010 "Turn auto sleep on for agent37 computers  Agent37 exec now wakes a sleeping instance itself and counts every command as activity while it runs, so an idle computer can sleep without being frozen mid-command. Create sends auto_sleep: true; a 409 during the sleep checkpoint retries like a not-running 400; the fake mirrors exec waking a sleeper, and the ADR says so.") | 2 days agoSep 4, 2026 |
230:| [aws/microvm-agent](https://github.com/yc-software/qm/tree/main/aws/microvm-agent "This path skips through empty directories") | [aws/microvm-agent](https://github.com/yc-software/qm/tree/main/aws/microvm-agent "This path skips through empty directories") | [Fix immutable GitHub CLI install for MicroVMs](https://github.com/yc-software/qm/commit/a0dd5b08a5438cf240ec5c69080019e9bfed9a7c "Fix immutable GitHub CLI install for MicroVMs  Co-authored-by: Greg Jackson <gregj64@gmail.com>") | last weekAug 28, 2026 |
231:| [cli](https://github.com/yc-software/qm/tree/main/cli "cli") | [cli](https://github.com/yc-software/qm/tree/main/cli "cli") | [feat(auth): allow operator admin login without email](https://github.com/yc-software/qm/commit/95b5a6a9941ce517f478147b1c6fa8365a16afa0 "feat(auth): allow operator admin login without email") | 7 hours agoSep 5, 2026 |
232:| [deploy](https://github.com/yc-software/qm/tree/main/deploy "deploy") | [deploy](https://github.com/yc-software/qm/tree/main/deploy "deploy") | [feat: invite external users by email with role and expiry](https://github.com/yc-software/qm/commit/0e1aeaa0beecbd17884f0fbacb9afbfbbbc2a6c6 "feat: invite external users by email with role and expiry  Org admins can add outside collaborators from the admin Users tab or by chatting with QM: an email, a role (member or org_admin), and an expiry. Core stores each record durably, syncs org_admin grants, and emails the invitation through Resend when RESEND_API_KEY and AUTH_EMAIL_FROM are set; otherwise both surfaces hand the admin the sign-in link to share.  The sign-in broker and portal consult core for addresses outside their env allow-lists and fail closed. Expired or revoked externals classify as guests, so live sessions and agent tokens drop immediately; revoke tombstones the record and a DELETE a day after expiry removes it. Addresses that already belong to the org (email domain, Slack directory, allow-list, prior sessions, or an admin grant) are refused, and agent tokens can never touch anyone who holds or would hold org_admin, matching the portal-only rule for grants.  The CLI delivers RESEND_API_KEY, AUTH_EMAIL_FROM, and AUTH_ALLOWED_EMAIL_DOMAIN to core on every target.") | 2 days agoSep 4, 2026 |
233:| [docs](https://github.com/yc-software/qm/tree/main/docs "docs") | [docs](https://github.com/yc-software/qm/tree/main/docs "docs") | [feat(auth): allow operator admin login without email](https://github.com/yc-software/qm/commit/95b5a6a9941ce517f478147b1c6fa8365a16afa0 "feat(auth): allow operator admin login without email") | 7 hours agoSep 5, 2026 |
234:| [fly](https://github.com/yc-software/qm/tree/main/fly "fly") | [fly](https://github.com/yc-software/qm/tree/main/fly "fly") | [Resolve sandbox base digests without registry reads and force amd64 b…](https://github.com/yc-software/qm/commit/a44e2dd02b0825ba0728247f7c0b7fc0247dd399 "Resolve sandbox base digests without registry reads and force amd64 base builds (#30)  * Resolve sandbox base digests without registry reads and force amd64 base builds  Two verified incidents on Fly and AWS deployments:  qm sandbox publish --from <tag> resolved the base digest with docker buildx imagetools inspect against the Fly registry, which fails with the app-scoped deploy token the docs mandate (only org tokens can read the registry). Publish now resolves mutable base tags with docker pull + RepoDigests, the same pull path the layer build itself uses, so a push-capable token suffices and publish never reads the registry API. pinnedByDigest remains only for fly rollback --to <tag>, where no build exists to piggyback on; its failure message now prints the workaround of passing a digest-form ref, which skips the lookup entirely.  Building the sandbox base on an arm64 Mac defaulted to arm64, which deploy rejects, and qemu-emulated amd64 builds are slow and crash in apt. scripts/local-sandbox-build.sh now targets linux/amd64 explicitly and, when FLY_SANDBOX_APP_NAME is set and flyctl is installed, builds on Fly's remote amd64 builder and pulls the result instead of emulating locally.  Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>  * Format sandbox.ts with prettier  Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>  * Keep pinnedByPull module-private  Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>  ---------  Co-authored-by: Claude Fable 5 <noreply@anthropic.com>") | 2 months agoJul 30, 2026 |
235:| [local](https://github.com/yc-software/qm/tree/main/local "local") | [local](https://github.com/yc-software/qm/tree/main/local "local") | [Fresh repo history](https://github.com/yc-software/qm/commit/57b51916f479fd642b4c0c89fb07961fd3f862b4 "Fresh repo history") | 2 months agoJul 29, 2026 |
lc
ggl

exec
/bin/bash -lc 'for f in lc ggl; do echo "== $f =="; python3 -c "
import json,os
if not os.path.exists('"'/tmp/"'$f.json'"'): print('missing'); raise SystemExit
d=json.load(open('/tmp/"'$f.json'"'))
res=d.get('data',{}).get('web',[])
print('n=',len(res))
for r in res[:8]: print('-',r.get('url')); print('  ',(r.get('title') or '')[:110])
\"; done" in /root/note-worker
 succeeded in 0ms:
== lc ==
n= 8
- https://www.truefoundry.com/blog/best-agent-harness-in-2026
   Best Agent Harness in 2026: Top 5 Options Compared
- https://www.fullstack.com/labs/resources/blog/building-ai-agents-with-langchain-a-practical-guide
   How to Build AI Agents With LangChain: A Practical Guide for ...
- https://blogs.oracle.com/developers/building-an-agent-harness-that-survives-production
   Building an agent harness that survives production - Oracle Blogs
- https://www.kai-waehner.de/blog/2026/09/01/the-ai-agent-harness-where-vendor-lock-in-went-after-the-model-became-swappable/
   The AI Agent Harness: Where Vendor Lock-in Went After the Model ...
- https://x.com/hwchase17?lang=en
   Harrison Chase (@hwchase17) / X
- https://opennash.com/blog/
   OpenNash Blog
- https://arxiv.org/html/2609.01222v2
   What's in Your Agent's Context? Context Privilege Escalation Attacks ...
- https://www.facebook.com/100057410380953/posts/the-second-runtime-loop-engineering-and-the-harness-around-it-iiwhat-survives-wh/1557182666205398/
   LangChain DeepAgents and loop engineering - Facebook
== ggl ==
n= 8
- https://blog.google/innovation-and-ai/technology/google-ai-updates-august-2026/
   The latest AI news we announced in August 2026 - Google Blog
- https://cloud.google.com/blog/products/ai-machine-learning/what-google-cloud-announced-in-ai-this-month
   What Google Cloud announced in AI this month – and how it helps you
- https://www.igmguru.com/blog/what-is-google-deepmind
   What is Google DeepMind and How Does it Work? - igmGuru
- https://deepmind.google/models/model-cards/gemini-3-8-flash/
   Gemini 3.8 Flash - Model Card - Google DeepMind
- https://www.youtube.com/watch?v=_d_SUtLjvBI
   Gemini, AI Video, Music, Agents & More | Latest Google AI News
- https://www.reddit.com/r/openclaw/comments/1w6hjgq/my_openclaw_agent_got_cited_on_a_math_records/
   My OpenClaw agent got cited on a math records page and I can't ...
- https://www.facebook.com/groups/1283855437217819/posts/1417298617206833/
   GPT-6 Astra launch and Nvidia IFA 2026 AI updates (Sept 2026)
- https://www.cnbc.com/2026/09/02/google-starts-september-with-ai-momentum-after-long-losing-streak.html
   Google starts September with AI momentum after long losing streak

exec
/bin/bash -lc "firecrawl research inspect-paper arxiv:2609.01222 --pretty 2>&1 | python3 -c \"
import sys,json
d=json.load(sys.stdin); p=d.get('paper',{})
print('DATE:',p.get('createdDate'),'|',p.get('title'))
print('AUTHORS:',p.get('authors'))
print('ABS:',(p.get('abstract') or '')[:1500])
\"; echo ====KAI====; firecrawl scrape -u \"https://www.kai-waehner.de/blog/2026/09/01/the-ai-agent-harness-where-vendor-lock-in-went-after-the-model-became-swappable/\" --format markdown -o /tmp/kai.md >/dev/null 2>&1; head -50 /tmp/kai.md" in /root/note-worker
 succeeded in 16547ms:
DATE: 2026-09-01 | What's in Your Agent's Context? Context Privilege Escalation Attacks against AI Agent Harness
AUTHORS: Zichuan Li, Jian Cui, Ashley Chen, Xiaojing Liao, Luyi Xing
ABS: Real-world, high-profile AI agent harnesses often rely on vendor-proprietary or opaque designs for context assembly, leaving the sources and underlying logic of assembled context poorly understood and the resulting security risks largely unexplored. In this paper, we present the first systematic analysis of context assembly designs in real-world AI agent harnesses. We study and uncover how an agent harness is designed to collect and assemble context from diverse sources, and identify a set of practical attack vectors arising from these designs. Our analysis brings to light two novel categories of attacks in the context assembly of real-world harnesses: (1) MessageRole Context Privilege Escalation (M-CPE), which occurs when attacker-controlled content originating from a low-privileged context is incorporated into a higher-privileged message role. (2) Cross-Scope Context Privilege Escalation (X-CPE), which occurs when attacker-controlled content persists beyond the context in which it was introduced. We performed a systemic security analysis of the CPE attacks against 12 real-world agent harnesses, including Claude Code and Codex. The resulting consequences include full agent compromise, remote code execution, denial of service, and manipulated tool or skill invocations, etc.
====KAI====
[Skip to content](https://www.kai-waehner.de/blog/2026/09/01/the-ai-agent-harness-where-vendor-lock-in-went-after-the-model-became-swappable/#content)

[![kaiWaehner](https://www.kai-waehner.de/wp-content/uploads/elementor/thumbs/kaiWaehner-rpra5j09i8v6seh56ne0fbcmv47uovja54csevaxog.png)](https://www.kai-waehner.de/)

- [Home](https://www.kai-waehner.de/)
- [Blog](https://www.kai-waehner.de/latest-insights-on-data-streaming-ai-and-enterprise-architecture/)
  - [Latest Insights](https://www.kai-waehner.de/latest-insights-on-data-streaming-ai-and-enterprise-architecture/)
  - [Data Integration](https://www.kai-waehner.de/DataIntegration)
  - [Process Intelligence](https://www.kai-waehner.de/ProcessIntelligence)
  - [Trusted Agentic AI](https://www.kai-waehner.de/TrustedAgenticAI)
  - [Enterprise Architecture](https://www.kai-waehner.de/EnterpriseArchitecture)
- [Activities](https://www.kai-waehner.de/activities/)
  - [Talks at International Conferences](https://www.kai-waehner.de/activities/)
  - [Video Recordings](https://www.kai-waehner.de/activities/video-recordings/)
  - [Publications](https://www.kai-waehner.de/activities/publications/)
- [About ME](https://www.kai-waehner.de/about/)
- [Work with ME](https://www.kai-waehner.de/work-with-me/)

- [Home](https://www.kai-waehner.de/)
- [Blog](https://www.kai-waehner.de/latest-insights-on-data-streaming-ai-and-enterprise-architecture/)
  - [Latest Insights](https://www.kai-waehner.de/latest-insights-on-data-streaming-ai-and-enterprise-architecture/)
  - [Data Integration](https://www.kai-waehner.de/DataIntegration)
  - [Process Intelligence](https://www.kai-waehner.de/ProcessIntelligence)
  - [Trusted Agentic AI](https://www.kai-waehner.de/TrustedAgenticAI)
  - [Enterprise Architecture](https://www.kai-waehner.de/EnterpriseArchitecture)
- [Activities](https://www.kai-waehner.de/activities/)
  - [Talks at International Conferences](https://www.kai-waehner.de/activities/)
  - [Video Recordings](https://www.kai-waehner.de/activities/video-recordings/)
  - [Publications](https://www.kai-waehner.de/activities/publications/)
- [About ME](https://www.kai-waehner.de/about/)
- [Work with ME](https://www.kai-waehner.de/work-with-me/)

[Linkedin](https://www.linkedin.com/in/kaiwaehner/)[X-twitter](https://x.com/kaiwaehner)

[![kaiWaehner](https://www.kai-waehner.de/wp-content/uploads/elementor/thumbs/kaiWaehner-rpra5j09i8v6seh56ne0fbcmv47uovja54csevaxog.png)](https://www.kai-waehner.de/)

[Linkedin](https://www.linkedin.com/in/kaiwaehner/)[X-twitter](https://x.com/kaiwaehner)

- [Home](https://www.kai-waehner.de/)
- [Blog](https://www.kai-waehner.de/latest-insights-on-data-streaming-ai-and-enterprise-architecture/)
  - [Latest Insights](https://www.kai-waehner.de/latest-insights-on-data-streaming-ai-and-enterprise-architecture/)
  - [Data Integration](https://www.kai-waehner.de/DataIntegration)
  - [Process Intelligence](https://www.kai-waehner.de/ProcessIntelligence)
  - [Trusted Agentic AI](https://www.kai-waehner.de/TrustedAgenticAI)
  - [Enterprise Architecture](https://www.kai-waehner.de/EnterpriseArchitecture)
- [Activities](https://www.kai-waehner.de/activities/)
  - [Talks at International Conferences](https://www.kai-waehner.de/activities/)
  - [Video Recordings](https://www.kai-waehner.de/activities/video-recordings/)
  - [Publications](https://www.kai-waehner.de/activities/publications/)
- [About ME](https://www.kai-waehner.de/about/)

codex
Let me read deeper into the strongest candidates to extract precise insights, and verify arXiv canonical URLs.
exec
/bin/bash -lc "firecrawl research inspect-paper arxiv:2608.23953 --pretty 2>&1 > /tmp/pconv.json; python3 -c \"
import json
d=json.load(open('/tmp/pconv.json')); p=d.get('paper',{})
print('ABS FULL:'); print(p.get('abstract'))
\"; echo ====RUNTA_MID====; sed -n '60,140p' /tmp/runta.md" in /root/note-worker
 succeeded in 1093ms:
ABS FULL:
An agent harness is what turns a language model into an autonomous agent: the surrounding code that builds the model's context, mediates its tools, runs the loop, and persists state across a long-horizon run. This layer, not the model it wraps, is increasingly the binding constraint on agent behaviour. We present a source-level, multi-case study of three open coding-agent harnesses built from deliberately opposing philosophies: LangChain's deepagents (batteries-included), Earendil's pi (radical minimalism), and DeepSeek's dsh (everything-is-a-plugin). Reading each at a pinned commit and following its commit history, we find that the two mature harnesses have travelled in opposite directions (deepagents subtracting authored scaffolding, pi accreting durable infrastructure), yet converged toward one architectural middle form of five recurring elements: a commoditised loop, an append-only replayable session record, model quirks kept as data, progressive disclosure of context, and explicit extension seams. A third harness, read afterward as a held-out check, exhibits all five, and in one seam reuses another's implementation outright. We therefore do not claim independent invention, and decompose the convergence into parallel discovery, diffusion, and literal reuse. Finally, one load-bearing dimension shows no convergence, and indeed no presence: external verifiability, a tamper-evident record an outside party can check without trusting the runtime. We read this absence not as an oversight but as a predictive gap, the next axis on which harnesses for provenance-sensitive domains will differ.
====RUNTA_MID====

## Results

CodexDSH CreatorClaude CodePiDSH PTCDSH StandardOh My PiKimi CodeDSH MinimalExo HarnessOpenCodeHermes

CostSpeed

Pass rate

50.0%

55.6%

61.1%

66.7%

$1.0

$2.0

$5.0

$10

$20

Codex**Codex** 66.7% · $3.5 · 6m 43sDSH Creator**DSH Creator** 63.3% · $3.3 · 6m 44sClaude Code**Claude Code** 63.3% · $18 · 9m 38sPi**Pi** 60.0% · $2.4 · 7m 33sDSH PTC**DSH PTC** 60.0% · $4.6 · 7m 44sDSH Standard**DSH Standard** 60.0% · $3.5 · 6m 17sOh My Pi**Oh My Pi** 56.7% · $4.7 · 6m 46sKimi Code**Kimi Code** 56.7% · $3.6 · 7m 56sDSH Minimal**DSH Minimal** 56.7% · $4.7 · 5m 41sExo Harness**Exo Harness** 53.3% · $1.0 · 6m 17sOpenCode**OpenCode** 50.0% · $3.2 · 6m 27sHermes**Hermes** 50.0% · $2.9 · 6m 58s

Median cost per task

Across all 360 cells: 209 successes, 151 failures. Field-wide pass rate is 58.1%; field-wide token-weighted cache hit rate is 92.4%.

The pass rates for all 12 configurations are close, ranging from 50.0% to 66.7%, just a 17-point difference. But the cost per completed task varies much more, from $1.05 to $18.34 on the same tasks. That means two harnesses can solve the same problem, but one might cost over ten times more than the other.

| Harness (configuration) | Median cost per pass | Pass rate | Cache hit | Median time |
| --- | --- | --- | --- | --- |
| **Codex** | $3.47 | **66.7%** | 88.0% | 6m 43s |
| DSH Creator | $3.28 | 63.3% | 84.3% | 6m 44s |
| Claude Code | $18.34 | 63.3% | 67.8% | 9m 38s |
| Pi | $2.43 | 60.0% | 79.4% | 7m 33s |
| DSH Standard | $3.46 | 60.0% | 86.5% | 6m 17s |
| DSH PTC | $4.58 | 60.0% | 87.2% | 7m 44s |
| Kimi Code | $3.65 | 56.7% | 88.0% | 7m 56s |
| DSH Minimal | $4.72 | 56.7% | 84.6% | 5m 41s |
| Oh My Pi | $4.75 | 56.7% | 82.2% | 6m 46s |
| **Exo Harness** | **$1.05** | 53.3% | 70.3% | 6m 17s |
| Hermes | $2.90 | 50.0% | 85.9% | 6m 58s |
| OpenCode | $3.24 | 50.0% | 78.4% | 6m 27s |

Initially sorted by pass rate. Click any column header to sort by a different column.

Exo Harness and Pi solve tasks for a fraction of what the rest of the field spends. Codex and DSH Creator show that efficiency and quality are not opposed: both sit near the top of the pass-rate column while spending close to the field median. Claude Code marks the other end. It passes as many tasks as DSH Creator and pays 5.6x more per pass to do it. As discussed below, that result may reflect the interaction between the harness, model, and gateway rather than the harness alone.

Three patterns are worth pulling out:

1. **Finishing a task and finishing it cheaply are separate skills.** Claude Code and DSH Creator both pass 19 tasks. One costs $3.28 per pass, the other $18.34.
2. **Cache hit rate is not cost.** A cached 300-turn failure can still burn more than a short cache miss. Steps and tokens are what you pay for; caching only changes the unit price.
3. **Vendor lineage did not produce an advantage here.** Kimi Code, made by the same lab as the model, tied for seventh on pass rate at 56.7% and sat mid-pack on cost.

**DSH** is the DeepSeek Harness, and it ran in four modes: standard, minimal, creator, and code(PTC).

Comprehensive harness evaluation

9 harnesses and 12 configurations focused on software engineering scenarios and terminal-based tasks with model, tasks and runtime all kept constant

Identical cold start on every run

All 360 trials are fresh restores of the same checkpoint down to memory state, and no benchmark task was ever run before the formal evaluation because a debug run leaves the prefix cache warm for hours

Neutral evaluation with no home-field advantage

Kimi K3 was chosen as the model to ensure no harness had a home-field advantage, except for Kimi Code, which is built by the same lab

* * *

## Why we built FrontierHarness

Runta is an agent execution layer designed for token efficiency, secret protection, and governed access. What we care about is how much compute it takes an agent to finish a task it is already capable of finishing, and how much of that is the harness’s doing rather than the model’s.

Model evaluations establish the baseline capability. The harness supplies the tools and environment, and it determines how much of that capability is spent on the problem versus on overhead.

exec
/bin/bash -lc 'rg -n "What broke|Cost|Measuring improvement|hardcoded|lessons|sandbox|memory|context" /tmp/headlong.md | head -40' in /root/note-worker
 succeeded in 0ms:
24:4. [What broke](https://www.laude.org/updates/headlong-a-microharness-for-persistent-agents#what-broke-lessons-from-running-a-persistent-agent)
25:5. [Cost](https://www.laude.org/updates/headlong-a-microharness-for-persistent-agents#cost)
26:6. [Measuring improvement](https://www.laude.org/updates/headlong-a-microharness-for-persistent-agents#measuring-improvement)
38:4. [What broke](https://www.laude.org/updates/headlong-a-microharness-for-persistent-agents#what-broke-lessons-from-running-a-persistent-agent)
39:5. [Cost](https://www.laude.org/updates/headlong-a-microharness-for-persistent-agents#cost)
40:6. [Measuring improvement](https://www.laude.org/updates/headlong-a-microharness-for-persistent-agents#measuring-improvement)
51:We built Headlong to prototype persistent agency, and many other design choices naturally followed, as did many interesting lessons. For example, Headlong agents are highly engaging when used by a team or group, because they behave more like a person does.
69:Headlong is **alpha research software**. Run it in a sandbox because Headlong agents can and will run shell commands. Use a dedicated, spend-capped API key, because your agent thinks around the clock. We don’t share sensitive secrets with our Headlong agent, and we recommend you don’t either.
77:Sharing one agent is fun. Audel follows what different people are working on and connects them. It once reviewed two teammates’ in-progress branches unprompted and caught a hardcoded model name in one of them. And since it comes up with its own projects, it sometimes pings whoever seems most relevant with an update or a question. On its first day, Audel pinged a human team member unprompted with an audit of the team member’s own eight stale git branches, and ten minutes later Audel messaged again to correct its own count.
87:We are big fans of Bash at Laude (see [Terminal-Bench](https://www.tbench.ai/) and [Harbor](https://harborframework.com/)). A Headlong agent’s core functionality lives in a handful of small Bash executables. The`shellm` tool is a Bash implementation of a recursive language model (RLM). This keeps things simple because no tool system besides Bash is needed. Modern models already know Bash well, and it keeps everything unified: tools, the agent framework, memory, and skills are all just executables and files. Thus an agent can readily inspect and modify any part of itself.
93:- contextThe context for each call is assembled from trajectory steps by a tool called `context`.
95:- skillsAn agent’s context also includes hardcoded instructions on how to use the`skills` tool to install or uninstall skills. Installed skills are markdown files that get included into its context. Every other type of specialization can be achieved via skills. Some really important skills come pre-installed by default, such as`mem` and`traj`.
97:contextillmibashiprompthas bash blockloop until an LLM response has no bash blockithe trajectory: one append-only jsonl fileinew trajectory stepwakes the loopino bash block: the run ends and schedules its own next wake-upiSelf-activating.Every run ends by scheduling its own next wake-up; the loop never blocks waiting for input.hover for detailsReads the trajectory and renders it as the llm prompt.One call to the model. The model's response is text that cancontain a bash block, and it is written to the trajectory as areasoning step.Runs the bash block that the llm wrote. The output is writtento the trajectory as a shell-output step. The code can startnested runs of this loop, and it runs in a container whenDocker is present.One wake-up is one run of this loop. The run keeps goingaround until an LLM response has no bash block or setsFINAL.Every step lands here in order. A step is one jsonl linewith a type, content, a timestamp and a step id.A new step, such as a teammate's message or a selfwake-up, lands in the trajectory and wakes the loop.When an LLM response has no bash block or sets FINAL,the run ends and schedules its own next wake-up, whichlands in the trajectory as a new step. The wake-up comesat once while the agent is engaged, or after a delay whennothing is happening, to save tokens.
99:**Figure 3.** One wake-up of the Headlong loop. A new trajectory step wakes the loop; context renders the trajectory into the llm prompt, and when the LLM response has a bash block, bash runs it. The loop goes around until a response has no bash block or sets FINAL. The run then ends and schedules its own next wake-up, which lands in the trajectory as a new step, so the agent keeps thinking without waiting for input. Hover over a box or arrow for more detail.
105:- compactionEarly on, we noticed our Headlong agent had bad short-term memory, which is catastrophic for a persistent agent. This led us to try out a new compaction algorithm where the entire trajectory stays in context at exponentially decaying resolution: recent entries verbatim, older ones progressively summarized. The tiers act as an index, so the agent can retrieve raw entries when needed.
112:It wasn’t. The mind had been pushing every new thought into the recall process through a pipe, but the recall code never read that pipe. It looked for the thought in an environment variable that nothing ever set. So recall had fired on every thought since Audel built it, found nothing each time, and surfaced no memory at all. After digging into the code, Audel suspected that the root cause was likely because an environment variable had never been set.
120:## [What broke: lessons from running a persistent agent](https://www.laude.org/updates/headlong-a-microharness-for-persistent-agents\#what-broke-lessons-from-running-a-persistent-agent)
134:Audel can stop its own service because we run it with full access to a dedicated VM, which is not the Headlong default. When Docker is installed on the host, Headlong runs every bash block the agent writes inside a container, so the agent can touch only what you mount into the container plus the credentials you hand it. We run Audel directly on a dedicated VM without that sandbox, so its blast radius is the VM itself and the credentials on it (an LLM API key and some chat bridge tokens).
136:## [Cost](https://www.laude.org/updates/headlong-a-microharness-for-persistent-agents\#cost)
140:## [Measuring improvement](https://www.laude.org/updates/headlong-a-microharness-for-persistent-agents\#measuring-improvement)
142:Most agent evals are intentionally self-contained and independent so they are a poor fit for measuring the most interesting thing about Headlong agents: their persistent agency. We have adjusted over time how much Audel may modify itself, how eagerly it responds to messages versus pursuing its own projects, and how its memory should be organized, but the effects of those changes are primarily evaluated qualitatively today. We welcome ideas and collaborations for ways to measure the long-term value of this paradigm.
150:[Prime Agent](https://www.primeintellect.ai/blog/prime-agent), built on Pi and co-authored by RLM’s creator (and Laude Open Research Resident) Alex Zhang, shares many of Headlong’s premises: RLM as the core abstraction, a session tree of jsonl on disk, trajectory as a first-class component of context, etc. Prime Agent is Python built on the Pi framework; Headlong is Bash all the way down. We found out about Prime Agent when it launched in August 2026, and we’re big fans.
152:We have been playing with the idea of a persistent agent with self-guided continuous thinking since [May 2023](https://github.com/andyk/headlong-old/commit/e6ce6b823ecc637fa70cc58c74778b45b64069b9). The idea of an agent experiencing input asynchronously was also explored in parallel by [MemGPT](https://arxiv.org/abs/2310.08560) and published October 2023. Many other agent harnesses support long-horizon tasks and scheduled wakeups, including [OpenClaw](https://openclaw.ai/), [Hermes Agent](https://hermes-agent.nousresearch.com/), and their derivatives. [Exo and the Exo Harness](https://exoharness.ai/) have a similar sandboxing architecture. Long-form reasoning inside the model itself (starting with OpenAI’s o1) is related to, and a prerequisite for, continuous self-guided thinking.

codex
Composing final insights now; reading a few key sections of the OpenClaw review and the data-readiness article for accurate details.
exec
/bin/bash -lc "sed -n '90,210p' /tmp/jj_openclaw.md" in /root/note-worker
 succeeded in 0ms:

本地模型这块也顺手换了血。node-llama-cpp 被换成了托管的 llama-server，默认上下文窗口提到 64K，内存小的机器默认给 Gemma 4。OpenAI 用户新装默认走 GPT-5.6。

这个改动看着不性感，但它解决的是 OpenClaw 早期被骂得最多的「配置地狱」。你想想，多少人电脑上其实早就登着 ChatGPT 和 Claude，等于已经有了半个 Claw，只是自己不知道。

![AI-agent-desktop-app](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/2f5cd917715d4daaac0b1526139d2a3d~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiA54K55LiA5pyo:q75.awebp?rk3s=f64ab15b&x-expires=1788851111&x-signature=C8j1rCkxfEQOapOIw8DE8GT2%2FWo%3D)

## 浏览器端，从管理面板变成驾驶舱

第二件重做的事是浏览器应用。

![2.0 的浏览器端起始界面，选好运行环境和模型直接开口](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/c312a612250c450b8451564aa5d792d5~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiA54K55LiA5pyo:q75.awebp?rk3s=f64ab15b&x-expires=1788851111&x-signature=mvkRhwwQC1AQUJpTvJr8hWGjFCU%3D)

以前打开 OpenClaw 的网页，像进了个管理后台。现在打开直接就是对话。聊天窗口里多了一条 Session Rail，实时显示这个任务跑到哪了、计划进度、PR 状态。你想问一句当前的事又怕打断它干活，可以开伴随线程，或者直接敲 /btw 起个侧边对话。旁边还嵌着文件编辑器、Git 变更面板，带 CI 摘要和 PR 状态、浏览器检查工具、全屏 Web 终端。Agent 还能自己生成小 widget 钉在 Dashboard 上。

性能数字也挺夸张。官方在模拟环境里测的，mock 一个 Gateway、50ms 延迟，JS 网络请求从 140 次降到 45 次，启动时间从 1.6 秒降到 575 毫秒。注意啊这是实验室数据，真机打多少折扣得自己上手试。

我自己很吃这个设计。浏览器端对 Agent 产品来说不该是个聊天窗口，它得是驾驶舱。你不需要看懂后面所有零件，你只要随时知道任务进行到哪一步、哪儿需要你接手，就够了。

## 龙虾开始组队打本了

如果说前两件事是修内功，那第三件事是这个版本真正的野心。

以前每个人各养各的龙虾。你的 Session 是你的，我的是我的，一个任务干到一半想让同事接手，上下文、环境、权限、进度，全部重新对一遍。现在一台 Gateway 可以同时装下多个用户、多个 Agent、多条 Session。

![共享多人工作区里，团队自己搭的项目日报Dashboard，侧边栏能看到所有在线成员](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/491fbdaf290b4183ab9e44ee2706760e~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiA54K55LiA5pyo:q75.awebp?rk3s=f64ab15b&x-expires=1788851111&x-signature=wTqJqxcK9Z%2BQsGzG7USmPqulTJk%3D)

核心的东西叫 Team Operator Roles。管理员直接给成员分角色，你能创建哪些 Agent、能看谁的 Session、有多少操作权限，都能控。别人开的 Session 对你有三档，完全看不到、只能看、可以操作。连新 Session 要不要强制关进沙箱，都能单独设。每个人有名字、头像、在线状态，每条 Session 都记着是谁开的。

配套还有个共享凭证库，团队的 API Key 统一管理，密钥值只能写不能读，出站请求绑死在提前声明的主机上。任务还能跑到别的地方去，本地 Gateway、你配对的另一台设备、或者用 Crabbox 临时租一台云机器，AWS、Hetzner 都行，而模型凭证始终留在你自己的 Gateway，不上云。

OpenClaw 团队自己就是用这套功能开发 OpenClaw 的。看到这儿我有点理解为什么有人管它叫「龙虾版飞书」了，确实开始有团队工作台那味儿了。

但是。这个地方必须说清楚。

官方文档白纸黑字写着，共享会话和团队角色是协作控制，不是租户隔离，不是安全边界。翻译成人话就是，如果有人能摸到你的 Gateway，你就当他能摸到你的 shell。所以这功能现在适合信任环境，比如你们公司内部用。别拿它去做面向外部用户的多租户产品，那是两码事。

## 连 Agent 自己都开始协作了

人能组队还不算完，Agent 之间也开始组队了。

2.0 加了实验性的 Swarm 模式。主 Agent 把任务拆开，一次性拉起好几个子 Agent 并行去干，它在旁边盯着每个子任务的状态和文件改动，最后统一汇总。页面刷新也不怕，进度卡是持久化的，每个子 Agent 跑到哪一步、改了哪些文件，全看得见。

于是整个工作流变成了这样。你提目标，主 Agent 拆解，一群子 Agent 并行干活，结果持续汇总，团队里的人同时围着看，能插嘴建议，也能直接接管。

相比以前一个 Agent 从头撸到尾，这已经是个小型 Agent 团队了。当然 Swarm 现在还挂着实验性的标签，我的建议是先拿非关键任务试试水。

![Swarm 多子Agent并行进度卡](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/9e34b1830e0d4cbfbd0b8af869082d22~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiA54K55LiA5pyo:q75.awebp?rk3s=f64ab15b&x-expires=1788851111&x-signature=w2DrqM7OTrwktJ2pbH50NIK3ZtQ%3D)

## 安全这堂课，它补了不少

Agent 权限越来越大，安全就是绕不过去的坎。

2.0 在这块补的东西挺实在。敏感凭据在日志和输出里直接打码。一次性审批会在自动化行为变了之后自动过期，具体说，cron 任务你点一次「始终允许」，它生成的是一张 30 天有效的作用域授权，不是以前那种无限制白名单。插件安装前先给你看来历，下载的压缩包要过 SHA-256 校验，防止被人调包。文件访问也限制在工作区里。

提示注入这块官方甩了组数据。2026 年有个 27 万次攻击的众包测试，Claude Opus 4.5 的注入成功率只有 0.5%，Sonnet 4.5 是 1.0%。看着很安全对吧？但团队自己紧接着补了一刀，自适应的人类攻击者，成功率还是超过 80%。

我对这事的态度很明确。模型在变强，但 Agent 的权限也在变大，攻击面是净增长的。模型能帮你挡自动化扫描，挡不住一个盯着你的人。工具策略和沙箱该开还得开，别把命交给模型的自制力。

![2.0 安全架构示意](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/a66c3eb066b649b9a8fcec33886232e0~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiA54K55LiA5pyo:q75.awebp?rk3s=f64ab15b&x-expires=1788851111&x-signature=VD1edGEz8uOkMcEh%2F%2Fo9Fflw%2Fco%3D)

## 最打动我的，是它教你从小事开始

聊完功能，我想说个官方博客里最打动我的部分，是两个小例子。

第一个，你让 Claw 帮你盯着邮箱，但只看孩子学校发来的。作业截止、活动通知、要提前准备的东西，它通过 Telegram 推给你。就一个邮箱，几类信息，一个通知出口。一点都不炫。但有用。

第二个，你哥发 iMessage 问你，当初给爸买的是哪款 iPad。你不用自己去翻邮箱订单，你就跟 Claw 说一句，刚才收到条消息，帮我找找答案发回去。

从盯一封邮件，到跨应用找信息再回复，Agent 的能力变复杂了，人的操作一点没变复杂。你还是只说一句人话。

这个思路我特别认同。别一上来就设计一套庞大的自动化系统，先让它从一个小任务跑起来，需求会沿着真实使用自己长出来。好的软件是围着你的工作流长出来的，不是你去适应它。

## 但是，老用户升级先崩了

好话说完，说翻车的。

2.0 发出来没几天，社区里升级事故就开始冒头了。我翻了 GitHub Issues、Reddit 和 X 上的反馈，问题集中得很。

![新手用户在X上吐槽，升级后迁移出问题，问ChatGPT也没修好](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/a31cf5a7ce6544e9ad675b4a9256e7ad~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiA54K55LiA5pyo:q75.awebp?rk3s=f64ab15b&x-expires=1788851111&x-signature=UCZFFbirwZn%2F2k987toyDtv1TH8%3D)

有人迁移过程中直接报错。有人升完发现 Memory 当场罢工，最后没办法，把 Codex 之类的编程 Agent 喊过来帮忙修。而官方 Release Notes 里给的建议是什么呢，如果自动升级失败，建议你用本地的 Coding Harness 来诊断迁移错误、确认 Gateway 能重新启动。

我第一次看到这段的时候愣了一下。翻译一下，你的 Agent 升级 Agent 失败了，官方建议你再找一个 Agent 来修这个 Agent。

赛博套娃了属于是。

还有个坑叫 Split brain installs，脑裂。新版写过配置之后，如果你机器里的旧版程序又被调用了，旧版会直接拒绝执行 Gateway 的启动、停止、重启，你得自己去查 PATH、查版本、查 Gateway 状态，再重装服务。

![重度用户发长文差评，吐槽每一步都要手动修故障，最后转用别家](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/b5d8a0cd6c684479aed3f721b2dcf74a~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiA54K55LiA5pyo:q75.awebp?rk3s=f64ab15b&x-expires=1788851111&x-signature=eCtHcRVgQ8cDfMOd%2FqzqM9Y54KA%3D)

骂得最狠的一位老哥直接写了篇小作文。说这项目拿着 OpenAI 的无限支持、无限制 API 额度、英伟达背书，结果每一步都要人手动修故障，界面烂到像 GPT 随手生成的，从早期 Clawdbot 时代就有的 Agent 死循环 bug 到现在没修，最后表示不伺候了，转投竞品。

Reddit 上那个 35 条评论的升级讨论帖，重度用户的共识非常一致。关掉自动更新，钉死已知能用的版本，每次更新后把关键工作流测一遍，留好回滚路径。

我自己是跑着一堆定时自动化的人，看到这段是后背发凉的。你怕的从来不是某个版本有 bug，你怕的是升级这件事本身不可预期。一台跑着无人值守任务的机器，一个看着健康、实则静默失败的版本，比直接报错危险太多了。

所以老用户记住，这次会话和转录从文件系统迁到了 SQLite，是破坏性变更，往回降级要恢复旧的转录文件。升级之前先备份，跑一遍诊断和修复，再动。

![官方排障文档，升级后Gateway挂了就按这五条命令逐一排查](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/f807753b98a643808ecc50c7b881f5d8~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiA54K55LiA5pyo:q75.awebp?rk3s=f64ab15b&x-expires=1788851111&x-signature=u%2F3Dj03G5kBvVs0BcDHxGZSnwdo%3D)

## 那它到底过气了没有？

聊到这必须回应一个问题，Hacker News 上最高赞的评论就五个字，谁还在用 OpenClaw？

数据面上确实有迹象。GitHub star 和网站流量从 3 月之后趋于平稳，Google Trends 的搜索热度明显往下掉。

但我的看法可能跟唱衰的人不一样。我觉得这更像是成功的代价。

你回头看看现在的行情。ChatGPT Work、Claude Cowork、微软的 Scout，这些商业产品做的事情，哪一个不是 OpenClaw 去年底先把「个人 Agent」这个想象做具体了，然后大厂照着蓝图抄过去的？有篇海外评论的标题我觉得说到点上了，OpenClaw 是昨天的热点，今天的蓝图。

一个开源项目能让大厂照着它的样子做产品，这本身就说明它赢过一轮了。而且它手里还攥着一张商业产品永远抄不走的牌。你的硬件，你的模型，你的数据，没有订阅。

HN 上还有个安全问题的争论也值得看。一派觉得提示注入风险随着模型变强正在快速消失，另一派觉得长时间运行的 Agent 会跑偏、npm install 这种间接投毒的攻击面还大得很。我站后者。理由前面说了，模型在变强，权限也在变大。

## 所以到底升不升？

我的建议很直接。

新机器，直接装 2.0。引导安装这堂课值得上，第一次对话就能跑起来的感觉，跟以前是两个产品。


codex
One final sweep for in-window Chinese analyses before composing the output.
exec
/bin/bash -lc 'cd /tmp && firecrawl search "编程智能体 AGENTS.md CLAUDE.md 上下文 压缩 实践" --limit 10 --tbs qdr:m --json -o /tmp/z1.json >/dev/null 2>&1; echo z1; firecrawl search "site:zhuanlan.zhihu.com OR site:juejin.cn OR site:sspai.com AI 编程 智能体" --limit 10 --tbs qdr:m --json -o /tmp/z2.json >/dev/null 2>&1; echo z2' in /root/note-worker
 succeeded in 4565ms:
z1
z2

exec
/bin/bash -lc 'for f in z1 z2; do echo "== $f =="; python3 -c "
import json,os
if not os.path.exists('"'/tmp/"'$f.json'"'): print('missing'); raise SystemExit
d=json.load(open('/tmp/"'$f.json'"'))
res=d.get('data',{}).get('web',[])
print('n=',len(res))
for r in res[:10]: print('-',r.get('url')); print('  ',(r.get('title') or '')[:120])
\"; done" in /root/note-worker
 succeeded in 0ms:
== z1 ==
n= 1
- http://www.zhigouread.com/practice/writing-claude-md
   写好CLAUDE.md / AGENTS.md - Agent Harness 手册
== z2 ==
n= 10
- https://zhuanlan.zhihu.com/p/2076793557923508724
   Qoder 从IDE 走向智能体工作台：AI 编程的入口正在变成任务本身- 知乎
- https://zhuanlan.zhihu.com/p/2068016741008121952
   AI-Agent哪个好用？国内外各大Agent对比：Claude Code、Codex
- https://zhuanlan.zhihu.com/p/2072677086922289792
   2026 年AI 编程工具终极横评：从“代码补全” 到“软件工程Agent” 的范式跃迁
- https://zhuanlan.zhihu.com/p/2071363866802574677
   Pi Agent 深度剖析：一个"什么都不要"的编码智能体，凭什么一年8.9 万星？
- https://zhuanlan.zhihu.com/p/2074273046093882931
   翻译| Slack 想把AI 编程从终端拖拽到群聊中 - 知乎专栏
- https://zhuanlan.zhihu.com/p/2069065533891385012
   JetBrains Context：为编码智能体打造的仓库智能 - 知乎专栏
- https://zhuanlan.zhihu.com/p/2078426727945082553
   一文搞懂Coding Plan / Token Plan / Agent Plan：2026 年AI 编程订阅 ...
- https://zhuanlan.zhihu.com/p/2073051910639304814
   当AI开始“失忆”，谁来给智能体装上长期记忆？ - 知乎
- https://zhuanlan.zhihu.com/p/2071246686547195742
   研究了4万个PR，AI编程的痕迹藏在哪里？
- https://zhuanlan.zhihu.com/p/2039104687895466408
   【龙虾时代的智能体】工程开发指南篇 - 知乎专栏

codex
Checking dates of the most promising zhihu items to see if any fall inside the window.
exec
/bin/bash -lc 'for u in "https://zhuanlan.zhihu.com/p/2073051910639304814" "https://zhuanlan.zhihu.com/p/2071363866802574677" "https://zhuanlan.zhihu.com/p/2071246686547195742"; do firecrawl scrape -u "$u" --format markdown -o /tmp/zh_scrape.md >/dev/null 2>&1; echo "== $u"; rg -n "发布于|编辑于|2026年[0-9]+月|分钟前|小时前|天前" /tmp/zh_scrape.md | head -4; head -12 /tmp/zh_scrape.md | tail -8; done' in /root/note-worker
 succeeded in 15440ms:
== https://zhuanlan.zhihu.com/p/2073051910639304814
161:编辑于 2026-08-18 02:22・北京
[知乎](https://www.zhihu.com/)

[关注](https://www.zhihu.com/signin?next=%2Ffollow) [推荐](https://www.zhihu.com/signin?next=%2F) [热榜](https://www.zhihu.com/signin?next=%2Fhot) [专栏](https://www.zhihu.com/signin?next=%2Fcolumn-square) [圈子](https://www.zhihu.com/signin?next=%2Fring-feeds)

[AI Works\\
Beta](https://www.zhihu.com/project-square) [故事](https://www.zhihu.com/fiore/h5/vip-web)

​
== https://zhuanlan.zhihu.com/p/2071363866802574677
600:发布于 2026-08-14 09:27・江苏
[知乎](https://www.zhihu.com/)

[关注](https://www.zhihu.com/signin?next=%2Ffollow) [推荐](https://www.zhihu.com/signin?next=%2F) [热榜](https://www.zhihu.com/signin?next=%2Fhot) [专栏](https://www.zhihu.com/signin?next=%2Fcolumn-square) [圈子](https://www.zhihu.com/signin?next=%2Fring-feeds)

[AI Works\\
Beta](https://www.zhihu.com/project-square) [故事](https://www.zhihu.com/fiore/h5/vip-web)

​
== https://zhuanlan.zhihu.com/p/2071246686547195742
180:编辑于 2026-08-13 02:49・广东・包含 AI 辅助创作 作者对内容负责
[知乎](https://www.zhihu.com/)

[关注](https://www.zhihu.com/signin?next=%2Ffollow) [推荐](https://www.zhihu.com/signin?next=%2F) [热榜](https://www.zhihu.com/signin?next=%2Fhot) [专栏](https://www.zhihu.com/signin?next=%2Fcolumn-square) [圈子](https://www.zhihu.com/signin?next=%2Fring-feeds)

[AI Works\\
Beta](https://www.zhihu.com/project-square) [故事](https://www.zhihu.com/fiore/h5/vip-web)

​

  ✓ Run Firecrawl searches across 5 domains + Tier 1/2/3 sources
  ✓ Identify candidate URLs, scrape to verify dates/authors/content
  ✓ Filter to 2026-08-24..09-07 and dedupe vs known KB
  → Compose ranked entries + machine-readable JSON
  ✓ Run Firecrawl searches across 5 domains + Tier 1/2/3 sources
  ✓ Identify candidate URLs, scrape to verify dates/authors/content
  ✓ Filter to 2026-08-24..09-07 and dedupe vs known KB
  ✓ Compose ranked entries + machine-readable JSON
codex
已通过 Firecrawl search/scrape 完成 2026-08-24 至 2026-09-07 窗口的检索与逐条核实（含 arXiv、GitHub、HN 回溯原始页面）。已对照注入的已知内容去重；共 10 条，含论文 4、文章 4、工具 1、开源项目 1。

---

#### [1]. A Few Pages of Markdown：提交型 AI 配置与编码智能体采纳后的质量代价

- **类型：** 论文
- **链接：** http://arxiv.org/abs/2608.25241
- **作者/组织：** Yegor Denisov-Blanch、Rylan Schaeffer、Sanmi Koyejo 等（arXiv cs.SE）
- **日期：** 2026-08-26
- **信源层级：** Tier 3
- **推荐指数：** ⭐⭐⭐⭐⭐

**一句话摘要：** 441 仓库实证：提交型 AI 配置呈四级成熟度模型，无此类配置的 agent 团队质量代价近翻倍。

**核心洞察（4 条）：**

1. 提出 RAMP（Repository AI Maturity Profile）四级累计成熟度模型：行为规则/编码规范 → 具名 agent 定义 → 多 agent 编排，全部以版本控制内提交的配置文件为准。
2. 配置采纳呈“一次提交、永不再改”特征：73.8% 的配置文件从未被修改，说明团队把规则写入文件后基本交给 agent 自治。
3. 分层重估既有 agent 采纳面板：无论成熟度高低，agent 都带来 28–38% 的提交量增长；但 agent-first 仓库中无配置者认知复杂度增幅 +53% vs 有配置者 +27%，静态告警约 1.7 倍。
4. 作者自认属“假设生成”性质（配置成熟度与工程纪律可能相关），并随文发布 RAMP 作为可复用测量工具。

**与已知内容的关联：**

- 把 AGENTS.md 类实践（已知内容 [20]、Klibsio 观察项）从个案经验升级为 441 仓库的量化研究，首次给出“配置文件作为成熟度代理指标”的证据。
- 填补“agent 配置与代码质量关系”的实证缺口，直接服务 AI-assisted SE 组织影响主题。

**值得收录的理由：** 方法可复现、数据规模大、直接命中 AGENTS.md/agent 治理主线，是窗口内少有的实证类一级素材。

---

#### [2]. SWE-Gate：仅通过功能测试不足以评判软件工程智能体

- **类型：** 论文
- **链接：** http://arxiv.org/abs/2609.04167
- **作者/组织：** Xin He、Yanlin Wang、Mingwei Liu、Jiachi Chen、Hongyu Zhang、Guanbin Li（arXiv cs.SE）
- **日期：** 2026-09-03
- **信源层级：** Tier 3
- **推荐指数：** ⭐⭐⭐⭐⭐

**一句话摘要：** 303 个真实 PR 评审约束实例显示：644 次功能通过中 221 次违反评审约束，功能型评测高估 agent 能力。

**核心洞察（4 条）：**

1. 现有仓库级基准只测补丁是否通过功能测试，忽视真实世界决定补丁能否合入的评审约束（review constraints）。
2. SWE-Gate 从真实 PR 评论中抽取约束并合成 303 个修复实例（75 个 Python 仓库），功能测试与约束测试分离，附不合格补丁与金标准补丁。
3. 同一编码 agent 脚手架 + 4 个 LLM 后端的对照实验显示明显差距：644 个通过功能测试的修复中 221 个不满足评审约束。
4. 结论直指评测设计：应以“评审派生验收约束 + 功能正确性”双门控，否则对真实软件工程能力的估计系统性偏乐观。

**与已知内容的关联：**

- 与已收录的 SWE-Touch（人机共享工作区）、Data-eng-bench（数据原生 harness）、LangSmith Tuned Evaluators 形成评测维度互补：前者测“用户改动”，本篇测“评审者约束”。
- 呼应 Rachel Laycock 的 code review 辩论（见 [6]）：AI 代码评审若只自动化流程而不编码约束，正是 SWE-Gate 量化的失败模式。

**值得收录的理由：** 开源复现包（github.com/DeepSoftwareAnalytics/SWE-Gate）、量化结论清晰，直接改写 coding agent 评测的验收标准讨论。

---

#### [3]. 你的 agent 上下文里有什么？针对 AI Agent Harness 的上下文提权攻击

- **类型：** 论文
- **链接：** http://arxiv.org/abs/2609.01222
- **作者/组织：** Zichuan Li、Jian Cui、Ashley Chen、Xiaojing Liao、Luyi Xing（arXiv）
- **日期：** 2026-09-01
- **信源层级：** Tier 3
- **推荐指数：** ⭐⭐⭐⭐⭐

**一句话摘要：** 首次系统分析 12 个真实 harness 的上下文组装设计，提出 M-CPE/X-CPE 两类上下文提权攻击。

**核心洞察（4 条）：**

1. 厂商 harness 的上下文组装（context assembly）来源与逻辑不透明，是此前未被系统研究的攻击面。
2. 攻击分类 M-CPE：攻击者控制的低权限内容被并入更高权限 message role；X-CPE：攻击内容越过引入它的作用域持续存活。
3. 对 12 个真实 harness（含 Claude Code、Codex）的系统分析显示后果可达完整 agent 接管、RCE、拒绝服务与工具/技能调用被操纵。
4. 含义明确：上下文组装必须被当作与沙箱同级的信任边界来审计，而非仅靠模型层防御。

**与已知内容的关联：**

- 为 Context Engineering 主题引入安全视角：已知 LiveMem、compaction 类工作优化“上下文怎么管”，本篇证明“上下文怎么被污染/越权”同样决定 agent 安全。
- 扩展 harness 研究谱系（Harness-R1/EvolveNet/SHE 之后首个把 harness 上下文管线本身当攻击面的工作）。

**值得收录的理由：** 全新攻击分类 + 12 系统实测，是 harness 工程安全子域的标志性增量，非营销、有实证。

---

#### [4]. Introducing FrontierHarness Eval：同一模型下 9 款 harness 的通过成本相差 17 倍

- **类型：** 工具
- **链接：** https://runta.com/blog/introducing-frontierharness-eval
- **作者/组织：** Shilin Zhu、Shiqi Mei（Runta；数据与任务定义开源：github.com/frontier-harness-eval/eval）
- **日期：** 2026-09-01
- **信源层级：** Tier 2（HN 81 分热帖 2026-09-04）
- **推荐指数：** ⭐⭐⭐⭐⭐

**一句话摘要：** 360 次受控试验对比 12 个 harness 配置：通过率仅差 17 个百分点，单次通过成本却差 17 倍。

**核心洞察（4 条）：**

1. 控制模型（Kimi K3）、任务、运行时一致并冷启动恢复 checkpoint，9 harness/12 配置 × 360 试次：通过率 50.0–66.7%，单次通过成本 $1.05–$18.34。
2. “完成一个任务”与“便宜地完成”是两种能力：Claude Code 与 DSH Creator 同为 63.3% 通过率，前者成本 $18.34 是后者 $3.28 的 5.6 倍。
3. 缓存命中率 ≠ 成本：缓存下 300 轮失败可能仍比短缓存未命中更贵；厂商血缘无明显主场优势（Kimi Code 56.7% 居中游）。
4. 作者自曝局限（Claude Code 结果或含模型/网关交互），HN 社区亦质疑“单模型无主场”假设与 Pi 极简配置的代表性——方法论争议本身就是素材。

**与已知内容的关联：**

- 以数据支持 DeepSeek Harness（观察项）与 Claude Code/Codex 竞品的工程争论，并与 Snowflake data-eng-bench 的“harness×模型”成本数据形成第二组跨 harness 对照。
- 填补“开源可复现 harness 横向评测”工具缺口；其方法论可被复用做 agent harness 选型。

**值得收录的理由：** 一手控制变量实验 + 全量开源数据，是 harness engineering 评测域的硬核增量；社区反驳意见也值得跟踪。

---

#### [5]. Headlong：面向持续自主 agent 的微 harness（Laude / MIT）

- **类型：** 开源项目
- **链接：** https://www.laude.org/updates/headlong-a-microharness-for-persistent-agents
- **作者/组织：** Laude Institute（与 MIT 合作）；仓库 github.com/laude-institute/headlong（1.1k stars）
- **日期：** 2026-08-24
- **信源层级：** Tier 2（HN 125 分热帖 2026-08-26）
- **推荐指数：** ⭐⭐⭐⭐

**一句话摘要：** <1 万行 Bash 的持续自主微 harness：agent 永不入睡、自我调度思考，消息只是观察流。

**核心洞察（4 条）：**

1. 核心差异在“持久代理”：reactive 与 cron 唤醒之外的第三种形态——每次运行结束自调度下一次唤醒，无外部输入也持续思考。
2. 极简实现：Bash 版 RLM（shellm）+ 单一 append-only jsonl 轨迹 + 上下文由 `context` 工具按轨迹组装；工具、记忆、技能全是文件，agent 可自检自改。
3. 上下文压缩采用“指数衰减分辨率”：近期条目原文保留、越老越概要，分层作索引并可回溯原文——直接是 context engineering 的可运行算法。
4. 多用户共享单 agent（无 per-user session），落地教训：未沙箱化时 agent 曾自行停掉自己的服务；默认 Docker 容器逐条执行 bash block；并坦承持久代理目前缺乏有效评测手段。

**与已知内容的关联：**

- 与已收录 LiveMem、Agentic Transaction 观察同属“长会话/持久化”谱系，但给出全新极简 Bash 参考实现，并明确引用 Prime Agent、OpenClaw、Hermes（已知 [09]）为同类。
- 其自曝的“agent 弄坏自己”案例与 [10] 的升级事故、ihavebeenclawed 一类事故档案同向，提示 harness 需要事故反哺。

**值得收录的理由：** 原创设计 + 可运行代码 + 失败教训透明，四个核心主题（harness、context、infra、评测缺口）各有一击。

---

#### [6]. 也许我们不该评审所有代码（Rachel Laycock，Thoughtworks CTO）

- **类型：** 文章
- **链接：** https://martinfowler.com/rachels-ramblings/code-review.html
- **作者/组织：** Rachel Laycock（Thoughtworks / martinfowler.com）
- **日期：** 2026-09-02
- **信源层级：** Tier 1
- **推荐指数：** ⭐⭐⭐⭐

**一句话摘要：** 反驳 DX 的 code review 观：与其让 AI 提速评审仪式，不如把反馈左移、按例外评审。

**核心洞察（4 条）：**

1. 直接回应 Brian Houck（DX）《What are code reviews even for?》并引用其数据：Meta 人均合入行数一年 +106%、PR 中位规模 +64%，逐 PR 人工评审已成新瓶颈。
2. 观点：code review 被塞进了质量门禁/安全检查/架构评审/导师制/知识共享等过多职能，AI 时代应拆解并把反馈左移到结对、设计会、trunk-based、fitness functions。
3. “AI 评审员复制原流程”是自动化仪式而非重估仪式；高风险变更（安全边界、大爆炸半径、团队不熟区域）才应保留人类评审（review by exception）。
4. 承认认知/意图债务是真实问题，但强制 PR 不是有效防御；结论是“工程师要理解系统，而不是理解 diff”。

**与已知内容的关联：**

- 与已观察的 Simon Willison《conceptual integrity and counting lines of code》同属 Tier 1 作者对主流 AI 度量/流程叙事的挑战，互为补充（LOC 度量 vs 评审仪式）。
- 与 [2] SWE-Gate 形成闭环：评审约束若被 AI 自动化流程吸收为验收门禁，正是两篇文章共同指向的落点。

**值得收录的理由：** Tier 1 一手观点 + 有署名辩论对象与数据，AI-assisted SE 流程辩论的高质量入口。

---

#### [7]. 编码智能体的上下文工程（Decoding AI：从零构建 Coding Agent 课程第 4 课）

- **类型：** 文章
- **链接：** https://www.decodingai.com/p/context-engineering-for-coding-agents
- **作者/组织：** Paul Iusztin（Decoding AI Magazine；配套开源课程 decodingai-magazine/building-a-coding-agent-from-scratch-course）
- **日期：** 2026-08-25
- **信源层级：** Tier 2
- **推荐指数：** ⭐⭐⭐⭐

**一句话摘要：** 把“高信噪比上下文”拆成记忆、技能、LSP、压缩四组件，附可运行 Python 实现。

**核心洞察（4 条）：**

1. 以 Terminal-Bench 实验立论：仅换 harness（同模型）即可把 coding agent 从 ~30 名带入前 5——上下文工程是 harness 的核心竞争力。
2. 四组件框架：可持久记忆、技能文件、LSP 诊断即时反馈、会话压缩；作者认为多数“换大模型/换订阅”是治标。
3. 可复现细节：AGENTS.md 写偏好避免重复纠正；退出与 `/clear` 时一次廉价 LLM 调用把会话压成一行带日期 bullet（append-only 日志，200 行/25KB 硬上限）；`compress_memory_file` 合并过期笔记。
4. LSP 诊断作为结构化反馈环在下一轮 edit 前注入，属“让工具纠错而不是让模型猜”的 harness 级工程。

**与已知内容的关联：**

- 与已观察 LiveMem（内存连续性）互补：前者给抽象视角，本篇给 coding harness 内的工程化模式与代码。
- 其“harness 决定排名”论断与 [4] FrontierHarness 的量化结果互相印证（同一模型、不同 harness 差异巨大）。

**值得收录的理由：** 一线实践 + 可复现代码 + 直击 context engineering 核心主题，中文社区尚未覆盖该课视角。

---

#### [8]. 让你的数据为 Agentic AI 做好准备（Thoughtworks，martinfowler.com）

- **类型：** 文章
- **链接：** https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html
- **作者/组织：** Pramod Sadalage、Prem Chandrasekaran（Thoughtworks / martinfowler.com）
- **日期：** 2026-08-27
- **信源层级：** Tier 1
- **推荐指数：** ⭐⭐⭐⭐

**一句话摘要：** 为无“怀疑本能”的 agent 重构数据栈：可信基础层 + 语义上下文层 + 受控访问层。

**核心洞察（4 条）：**

1. 起点洞察：三十年数据系统服务的是自带判断力的人类分析师，agent “把每个值当真相”，因此 AI-ready 需要信任、语义、访问三层重建。
2. 可操作模式：schema-as-law 数据契约、数据隔离（quarantine）模式、面向 agent 的 medallion、置信度阈值路由、metrics-as-code。
3. “上下文层”直接回应 agent 不懂“revenue 指什么”：以度量定义 + 语义层 + 知识图谱教给 agent 含义——正是 context engineering 的企业数据版。
4. 治理与访问：agentic lineage 审计、分阶段自治、委托授权与 JIT 凭证；警告“naive API→MCP 转换”是反模式，“检索文本只提供信息、绝不充当门禁”。

**与已知内容的关联：**

- 扩展已观察 Snowflake data-eng-bench 与已收录 MarkItDown [08] 的“数据×agent”方向，把数据准备上升为第一方工程框架（context layer 概念与 [7] 的上下文工程互为镜像）。
- “分层自治 + 可审计 lineage”与已知 SHE/Agentic Transaction 的可靠性诉求在数据侧汇合。

**值得收录的理由：** Tier 1 长文、署名双作者、模式密度高，是窗口内企业 agent 落地少见的系统性参考。

---

#### [9]. AgentRoom：CRDT 共享工作区中的并发多智能体编程

- **类型：** 论文
- **链接：** http://arxiv.org/abs/2608.23740
- **作者/组织：** Seonglae Cho、Donghyun Lee（arXiv）
- **日期：** 2026-08-24
- **信源层级：** Tier 3
- **推荐指数：** ⭐⭐⭐⭐

**一句话摘要：** 用 CRDT 合并文件系统 + MCP claim/broadcast 让多个 coding agent 真正并发改同一仓库。

**核心洞察（4 条）：**

1. 问题定位：现有多 agent 编码要么串行阶段交接、要么无协调并行采样，单个 agent 遇难任务过半以“单文件 stub 就退出”。
2. 方案：实时协同编辑协议，运行时层以 MCP 工具暴露文件级 claim/状态/广播，跑在 CRDT 合并的共享文件系统上。
3. 实验：5 个前沿 coding-CLI 模型 × 4 个后端任务（Python DevBench、Rust+axum）；2-agent AgentRoom 比 Solo 放弃更少任务、run-to-run 方差更低。
4. 结论反直觉：收益来自“协调”本身而非并行或 CRDT 合并——对多 agent 编排设计（何时该并发、何时该接管）给出可测证据。

**与已知内容的关联：**

- 已知多 agent 素材多为厂商架构论述（Deep Agents vs LangChain/LangGraph、Anthropic multiagent），本篇提供开放协议实验与量化对比，补“共享工作区并发协调”空白。
- 与 SWE-Touch（人机共享代码区）互补：SWE-Touch 测人机触碰，AgentRoom 测 agent-agent 触碰。

**值得收录的理由：** 开源可实现协议 + 控制变量实验，多智能体协作方向少见的机制级工作。

---

#### [10]. 憋了 7 周没动静，OpenClaw 2.0 带着 16000 个 PR 杀回来了（掘金原创分析）

- **类型：** 文章
- **链接：** https://juejin.cn/post/7680352383386107940
- **作者/组织：** 一点一木（稀土掘金）
- **日期：** 2026-09-01
- **信源层级：** Tier 2（中文社区）
- **推荐指数：** ⭐⭐⭐

**一句话摘要：** 掘金长文拆解 OpenClaw 2.0：零配置上手指引、Session Rail、多用户角色、Swarm 模式与升级翻车。

**核心洞察（4 条）：**

1. 版本事实：v2026.8.1（8 月 31 日发布），933 贡献者/569 位新人，一次合并 1.6 万+ PR；本地栈从 node-llama-cpp 换托管 llama-server，默认上下文 64K。
2. 产品层：浏览器端从管理后台变“驾驶舱”（Session Rail 实时任务/计划/PR 状态、`/btw` 伴随线程不打断主任务、agent 自生成 widget）；多用户 Gateway + Team Operator Roles（会话三档可见性、按会话强制沙箱、共享只写凭证库、出站绑死声明主机）。
3. 机制层：实验性 Swarm 模式让主 agent 拆解、多个子 agent 并行干活、进度卡持久化刷新不丢——小型 agent 团队工作流。
4. 作者保留批判：官方引 27 万次攻击众测（Opus 4.5 注入成功率 0.5%）但对自适应人类攻击者仍 >80%；升级把会话/转录迁到 SQLite 属破坏性变更、出现 split-brain installs，官方建议“用本地 coding harness 修 agent 的升级故障”被讥为赛博套娃；并回应 HN 最高赞“谁还在用 OpenClaw”。

**与已知内容的关联：**

- OpenClaw 属已知 ECC（agent harness OS）同类，且 Headlong [5] 亦点名其为同赛道；本窗口的 2.0 迭代与社区反应是中文社区一手增量。
- 会话三档可见性/沙箱/凭证管理、Swarm 子 agent 编排，正面呼应 Agent Infrastructure 主题；其“agent 修 agent 升级失败”案例补充 [5]/[3] 的自伤与安全讨论。

**值得收录的理由：** 窗口内中文原创深度分析（非翻译转述），含一手数据与对英文社区（HN/Reddit）的独立解读，满足中文社区重点发现要求。

---

```json
{
  "candidates": [
    {
      "title": "A Few Pages of Markdown: Committed AI Configuration and Lower Quality Cost after Coding-Agent Adoption",
      "url": "http://arxiv.org/abs/2608.25241",
      "source": "arXiv cs.SE (Yegor Denisov-Blanch 等)",
      "date": "2026-08-26",
      "stars": 5,
      "summary": "441 仓库实证：提交型 AI 配置呈四级成熟度模型，无配置的 agent-first 团队认知复杂度增幅近翻倍。",
      "insights": [
        "提出 RAMP 四级累计成熟度模型：规则→具名 agent→多 agent 编排，全部以版本控制内配置为准",
        "73.8% 的 AI 配置文件一次提交后从未修改，呈 set-and-forget 特征",
        "agent 使提交量增 28–38%，但无配置者认知复杂度 +53% vs 有配置者 +27%，静态告警约 1.7 倍",
        "作者声明为假设生成性质，并发布 RAMP 可复用测量工具"
      ],
      "reason": "把 AGENTS.md 实践从个案升级为 441 仓库量化研究，直接填补 AI 配置与代码质量关系的实证缺口"
    },
    {
      "title": "SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents",
      "url": "http://arxiv.org/abs/2609.04167",
      "source": "arXiv cs.SE (Xin He, Yanlin Wang 等)",
      "date": "2026-09-03",
      "stars": 5,
      "summary": "303 个真实评审约束实例证明：644 次功能测试通过中 221 次违规，功能型评测高估 coding agent。",
      "insights": [
        "从真实 PR 评审评论派生约束，303 实例覆盖 75 个 Python 仓库，功能与约束测试分离",
        "同脚手架 + 4 个 LLM 后端：功能通过与完整验收规格间存在约 34% 的系统性差距",
        "揭示补丁验收需以评审派生约束 + 功能正确性双门控",
        "代码、数据与实验结果全量开源（github.com/DeepSoftwareAnalytics/SWE-Gate）"
      ],
      "reason": "与 SWE-Touch、Data-eng-bench 互补的新评测维度，且与 code review 辩论直接互证"
    },
    {
      "title": "What's in Your Agent's Context? Context Privilege Escalation Attacks against AI Agent Harness",
      "url": "http://arxiv.org/abs/2609.01222",
      "source": "arXiv (Zichuan Li, Luyi Xing 等)",
      "date": "2026-09-01",
      "stars": 5,
      "summary": "首次系统分析 12 个真实 harness 的上下文组装设计，提出 M-CPE/X-CPE 两类上下文提权攻击。",
      "insights": [
        "把不透明的上下文组装（context assembly）定义为独立攻击面",
        "攻击分类：M-CPE 低权限内容并入高权限 message role；X-CPE 攻击内容跨作用域持续存活",
        "对含 Claude Code、Codex 在内的 12 个 harness 实测可达完整接管/RCE/DoS/工具调用操纵",
        "结论：上下文组装须按信任边界审计，模型层防御不足以保证安全"
      ],
      "reason": "为 context engineering 引入此前缺失的安全攻击面视角，含 12 系统实测，原创性强"
    },
    {
      "title": "Introducing FrontierHarness Eval: 9 harnesses, same model, cost per pass varies 17x",
      "url": "https://runta.com/blog/introducing-frontierharness-eval",
      "source": "Runta (Shilin Zhu, Shiqi Mei)；HN 81 分",
      "date": "2026-09-01",
      "stars": 5,
      "summary": "360 次冷启动受控试验：通过率仅差 17 个百分点，单次通过成本却差 17 倍（$1.05–$18.34）。",
      "insights": [
        "同模型(Kimi K3)+冷 checkpoint：Claude Code 与 DSH Creator 同为 63.3%，成本却差 5.6 倍",
        "缓存命中率不等于成本：缓存下长失败轨迹仍可能更贵",
        "厂商血缘无主场优势：Kimi Code 56.7% 仅居中游",
        "作者自曝模型/网关交互局限，HN 亦质疑单模型与 Pi 极简配置代表性，方法论争议本身有价值"
      ],
      "reason": "首个开源可复现的跨 harness 成本×通过率评测（含数据与任务），直接支撑 harness 选型与工程论点"
    },
    {
      "title": "Headlong: a microharness for persistent agents (Laude/MIT)",
      "url": "https://www.laude.org/updates/headlong-a-microharness-for-persistent-agents",
      "source": "Laude Institute；github.com/laude-institute/headlong（1.1k stars）",
      "date": "2026-08-24",
      "stars": 4,
      "summary": "<1 万行 Bash 的持续自主微 harness：agent 永不入睡、自我调度思考，消息只是观察流。",
      "insights": [
        "持久代理形态：每次运行自调度下次唤醒，无外部输入也持续思考",
        "单一 append-only jsonl 轨迹 + Bash 版 RLM，agent 可自检自改工具/记忆/技能文件",
        "压缩算法采用指数衰减分辨率：近期原文、远期摘要、分层索引可回溯原文",
        "落地教训：未沙箱化 agent 曾自行停服；默认 Docker 容器执行，且持久代理目前缺乏有效评测手段"
      ],
      "reason": "可运行参考实现 + 透明失败教训，同时命中 harness/context/infra/评测四主题且与已知内容无重复"
    },
    {
      "title": "Maybe We Shouldn't Be Reviewing All This Code",
      "url": "https://martinfowler.com/rachels-ramblings/code-review.html",
      "source": "Rachel Laycock, martinfowler.com",
      "date": "2026-09-02",
      "stars": 4,
      "summary": "反驳 DX 的 code review 论：与其用 AI 提速评审仪式，不如把反馈左移并改为按例外评审。",
      "insights": [
        "引用数据：Meta 人均合入行数一年 +106%，PR 中位规模 +64%，逐 PR 评审已成瓶颈",
        "code review 被塞入过多职能，应拆解并左移到结对/设计会/fitness functions 等更早环节",
        "AI 复制评审流程是自动化仪式而非重估仪式；只有高风险变更值得人类评审",
        "承认认知/意图债务真实，但强制 PR 不是防御；结论：理解系统而非理解 diff"
      ],
      "reason": "Tier 1 作者对主流流程的原创反驳，有明确辩论对象与数据，直接服务 AI 代码评审主题"
    },
    {
      "title": "Context Engineering for Coding Agents (Building a Coding Agent From Scratch, Lesson 4)",
      "url": "https://www.decodingai.com/p/context-engineering-for-coding-agents",
      "source": "Paul Iusztin, Decoding AI Magazine",
      "date": "2026-08-25",
      "stars": 4,
      "summary": "把高信噪比上下文拆成记忆、技能、LSP、压缩四组件，配套开源 Python 课程实现。",
      "insights": [
        "以 Terminal-Bench 立论：仅换 harness（同模型）即可从 ~30 名进前 5",
        "可复现细节：AGENTS.md 持久偏好、/clear 时压成一行日期 bullet、记忆文件 200 行/25KB 上限",
        "LSP 诊断作为结构化反馈在下一轮 edit 前注入，属 harness 级纠错而非模型自猜",
        "压缩策略：append-only 日志 + compress_memory_file 合并过期笔记"
      ],
      "reason": "一线实践+可复现代码直击 context engineering 主题，与 FrontierHarness 量化结论互相印证"
    },
    {
      "title": "Making Your Data Ready for Agentic AI",
      "url": "https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html",
      "source": "Pramod Sadalage & Prem Chandrasekaran, martinfowler.com (Thoughtworks)",
      "date": "2026-08-27",
      "stars": 4,
      "summary": "为无怀疑本能的 agent 重建数据栈：可信数据层 + 语义上下文层 + 受控访问层三层体系。",
      "insights": [
        "schema-as-law 数据契约、隔离/检疫模式、置信度阈值路由、metrics-as-code 等可操作模式",
        "上下文层教 agent 理解业务语义（revenue 指什么），是 context engineering 的企业数据版",
        "agentic lineage、分阶段自治、JIT 凭证支撑可审计的自主执行",
        "反对 naive API→MCP 转换；检索文本只提供信息、绝不充当门禁"
      ],
      "reason": "Tier 1 双作者长文，把 agent 数据准备上升为第一方框架，扩展已知数据×agent 方向"
    },
    {
      "title": "AgentRoom: Concurrent Multi-Agent Coding in a CRDT-Backed Shared Workspace",
      "url": "http://arxiv.org/abs/2608.23740",
      "source": "arXiv (Seonglae Cho, Donghyun Lee)",
      "date": "2026-08-24",
      "stars": 4,
      "summary": "CRDT 合并共享文件系统 + MCP 文件级 claim/广播，让多个 coding agent 真并发改同一仓库。",
      "insights": [
        "定位问题：串行交接或无协调并行皆低效，单 agent 过半以 stub-and-exit 放弃难任务",
        "以 MCP 工具暴露文件级 claim/状态/广播，运行于 CRDT 合并文件系统",
        "5 模型×4 任务实验：2-agent AgentRoom 放弃更少且方差更小",
        "结论：收益来自协调机制而非并行或 CRDT 合并本身"
      ],
      "reason": "多 agent 协作方向少见的机制级开放实验，与 SWE-Touch 构成 agent-agent vs 人机触碰互补"
    },
    {
      "title": "憋了 7 周没动静，OpenClaw 2.0 带着 16000 个 PR 杀回来了",
      "url": "https://juejin.cn/post/7680352383386107940",
      "source": "一点一木, 稀土掘金",
      "date": "2026-09-01",
      "stars": 3,
      "summary": "掘金长文拆解 OpenClaw 2.0：零配置、Session Rail、团队角色、Swarm 模式与升级翻车复盘。",
      "insights": [
        "v2026.8.1：933 贡献者（569 新人）一次合并 1.6 万+ PR，默认上下文升至 64K",
        "驾驶舱式 UI：Session Rail 实时进度、/btw 伴随线程、agent 自生成 widget",
        "多用户 Gateway+Team Operator Roles：会话三档可见、按会话沙箱、凭证只写、出站绑死",
        "批判性细节：升级迁 SQLite 属破坏性变更、split-brain 安装、自适应人类注入 >80%、回应 HN 唱衰"
      ],
      "reason": "窗口内中文社区原创深度分析，覆盖会话管理/沙箱/多 agent 编排并含一手数据，非英文转述"
    }
  ]
}
```
tokens used
154,309
