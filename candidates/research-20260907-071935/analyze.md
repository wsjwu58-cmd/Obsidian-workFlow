我已核对知识库现状（`references/articles.md` 编号至 21、观察项 21 条、`expand/06-AI与LLM/` 9 条、`expand/thinking/` 2 条、待处理队列 4 条）与 `research.py` 的三档分流逻辑。以下为对 Prompt A 输出的 10 条候选的完整分析。

## 1. 优先级排序

| 优先级 | 候选 | 星级 | 对已收录/已跟踪内容的补充价值 | 对既有洞见/假设的验证与挑战 | 回答的缺口 |
|---|---|---|---|---|---|
| 1 | **[3] CPE 上下文提权攻击** | ⭐5 | 首次把「上下文组装」当成独立攻击面审计 12 个真实 harness（含 Claude Code、Codex——我们自己的工具类）；与 SHE（安全 harness 演化）、auto-mode 安全数据、LiveMem 形成「记忆/上下文 × 安全」完整闭环 | **挑战**「模型层防御够用」的默认假设；反向印证 `MCP协议标准化的增量与边界`（thinking）——协议只标准化连接信封，语义/作用域自治正是攻击面所在 | 直接命中「Agent 安全审计」缺口（最薄弱区），含多智能体信息流（X-CPE 跨作用域持久化） |
| 2 | **[4] FrontierHarness Eval** | ⭐5 | data-eng-bench 之后第二组跨 harness 受控数据（360 试次、9 harness/12 配置），且数据/任务全开源；补 ECC 类通用 harness「缺公开评测数据」的选型空白 | **验证**「harness 层决定成本远大于质量」：通过率仅差 17pp，单次通过成本差 17 倍；**挑战**「缓存命中率高=省钱」的朴素成本观 | 「Agent 评测组件级归因」「中小团队成本锚点（部分）」 |
| 3 | **[2] SWE-Gate** | ⭐5 | 与已跟踪 SWE-Touch（用户改代码）、LangSmith Tuned Evaluators 组成评测第三维：评审者约束 | 量化说明功能测试对 agent 能力系统性高估（34% 违规），把「什么才算完成」从测试拉到真实合入门槛 | 「harness 行为正确性与覆盖率评估（验收侧）」「评测归因（同脚手架×4 模型）」 |
| 4 | **[5] Headlong** | ⭐4 | 现有持久/长会话谱系（Muse、auto-mode、Agentic Transaction、Hermes-Agent）缺一个可运行的极简参考实现——它是 Bash 微 harness 全套 | 其「指数衰减分辨率 compaction」是可复现算法；自曝「agent 弄停自己服务」验证安全缺口 | 「上下文/compaction 可复现实践」「激活策略（always-on 自唤醒）」「安全审计（沙箱边界）」 |
| 5 | **[7] DecodingAI 上下文工程第 4 课** | ⭐4 | 与 [4] 互证（仅换 harness 进 Terminal-Bench 前 5），给的是记忆/技能/LSP/压缩四件套 + 可运行 Python | **挑战**「换大模型/换订阅治标」论；与待处理队列 Claude 5 context rules（模型级）互补成 harness 级实现 | 「上下文/compaction/记忆可复现实践」——本轮最可操作的一份 |
| 6 | **[1] RAMP（提交型 AI 配置）** | ⭐4 | 把 [20] AGENTS.md 个案 + Klibsio 观察（含 AGENTS.md 实践）升级为 441 仓库量化证据，且发布可复用测量工具 | **支持但复杂化** [20]：73.8% 配置「一次提交不再改」提示写配置≠持续治理，需把配置当可治理工件 | 「harness/配置治理的实证」；间接服务评测归因（配置层作为新变量） |
| 7 | **[9] AgentRoom** | ⭐4 | 已跟踪多 agent 素材多为厂商架构论述（Deep Agents vs LangGraph 等），本文给机制级开放协议 + 控制变量实验 | **反直觉**：收益来自「协调」本身而非并行/CRDT——指导何时并发、何时接管 | 「多智能体编排反模式」「多智能体信息流（文件级 claim）」 |
| 8 | **[6] Rachel Laycock 代码评审论** | ⭐3 | 与观察项 Simon Willison LOC 文同类 Tier1 反驳，但升级为有具名对手与 Meta 数据的一线辩论 | 与 [2] 合成闭环：评审约束编码为机器可判门禁（SWE-Gate），而不要逐 PR 仪式化人工评审 | 流程/评测辩论入口（间接） |
| 9 | **[8] 让数据为 Agentic AI 就绪** | ⭐3 | 扩展 MarkItDown、data-eng-bench 的「数据×agent」方向到企业三层数据框架 | 其「语义上下文层」是上下文工程的企业数据镜像 | 不在 10 项清单内，属相邻扩展（数据契约/隔离/JIT 凭证） |
| 10 | **[10] OpenClaw 2.0 掘金长文** | ⭐3 | Headlong 明指 OpenClaw 为同赛道；中文社区原创深度分析含一手版本数据与对 HN/Reddit 的独立解读 | 团队角色/会话可见性/凭据库/Swarm 给出产品级多用户+多 agent 设计细节；「roles≠租户隔离」与升级事故是现成反模式 | 「多智能体编排（Swarm 实验态）」「安全审计（沙箱/凭据/注入 80%+）」的产品侧证据 |

补充说明：候选均在 2026-08-24 ~ 09-07 窗口内、与 KB 现有 URL 无重复；跨平台侧本轮零达标内容，不硬凑，缺口顺延至下一轮（详见第 2/3 节）。

## 2. 缺口分析

**被覆盖的缺口**

| 缺口 | 覆盖程度 | 证据 |
|---|---|---|
| Agent 安全审计（轨迹/信息流/权限边界） | 强 | [3] M-CPE/X-CPE 分类 + 12 harness 实测；[10] 会话三档可见/按会话沙箱/凭据只写/自适注入 >80%；[5] 未沙箱 agent 自行停服事故 |
| 上下文/compaction/记忆可复现实践 | 强 | [5] 指数衰减分辨率 compaction + append-only jsonl 轨迹；[7] 记忆文件 200 行/25KB 上限、`/clear` 单行压缩、`compress_memory_file`、LSP 反馈环 |
| Agent 评测组件级归因 | 强 | [4] 固定模型/任务/运行时下 9 harness×成本/质量矩阵，缓存命中率≠成本；[2] 同脚手架×4 模型分离「模型」变量 |
| Agent 评测验收现实性 | 强 | [2] 功能通过≠评审约束通过（303 实例/34% 差距），建议双门控；[6] 流程侧同向 |
| 多智能体编排反模式与成本 | 中 | [9] 收益来自协调而非并行；[10] Swarm 拆解/子 agent 并行/进度持久化；成本维度仅 [4] 单 agent 数据 |
| 中小团队成本锚点 | 中（受控非现场） | [4] 单次通过成本 $1.05–$18.34；[10] 升级/运维事故类现场经验，缺系统生产成本案例 |
| 激活策略 | 弱 | [5] always-on 自唤醒调度（engaged vs idle 延迟）；[10] 30 天作用域审批——零散数据点，无系统比较 |

**仍未触及的缺口**

- 跨模型可移植性与迁移指南：本轮无直接命中（FrontierHarness 选 Kimi K3 中立模型只为去主场，不是迁移指南；LangChain/Google 检索只出营销/综述，Kai Waehner 的「harness 锁定 vs 模型可换」未入选）。
- KMP/CMP vs Flutter 架构选型、共享逻辑边界、工具链痛点；跨平台 CI/发布/性能基线：连续两轮空窗，建议下一轮把 JetBrains Kotlin/Flutter 官方发布与 CI 案例列为定向域。
- Harness 内部「行为/覆盖率」度量工具：SWE-Gate 测任务验收，FrontierHarness 测通过率与成本，都不是对 harness 自身逻辑（工具编排、恢复路径）的覆盖率评估——仍开放。
- 长时程/持续 agent 的评测方法论：[5] 自陈只能定性测量，无成熟基准；「持续自主性」的量化仍无人解决。
- 多智能体权限隔离的**设计原语**：[3] 给出攻击面，[10] 明示团队角色非租户隔离，但缺可复用的多 agent 信息流隔离架构模式。
- 生产环境（非受控、含模型/网关交互）的成本/质量归因：[4] 自曝局限，Claude Code 的 $18.34 可能含模型/网关因素——正是「环境」变量的归因空白。

## 3. 趋势信号

- **Harness 效应进入可复现评测品类**：data-eng-bench（已跟踪）→ FrontierHarness → DecodingAI 的 Terminal-Bench 论断，三方独立互证「模型相同时 harness 决定成本与排名」。与既有 `ECC.md`「harness 是工程化主战场」一致。
- **竞争主轴从「能力」转向「成本/效率」**：通过率收敛于 50–66.7%，成本却差 17 倍；「便宜地完成」被识别为独立技能；缓存命中率≠成本，步数/token 计价成为新度量。Claude Code 的 5.6× 成本差提示「harness×模型×网关」交互尚未归因干净。
- **评测验收标准向「人的验收现实」迁移**：SWE-Gate（评审约束门禁）与 Laycock（评审左移+按例外）表面对立、实为同构——把评审约束变成机器可判的早期数据，而非逐 PR 仪式。与已跟踪 SWE-Touch「用户会改代码」同一方向。
- **上下文从优化对象升级为信任边界**：CPE 证明「上下文怎么被组装/越权」比「怎么压缩」更决定安全；攻击面从模型层（提示注入）上移到 harness 的 message role 与作用域管理。与 SHE、auto-mode 安全数据一致，是把 context engineering 推向安全子域的里程碑。
- **持久/自唤醒 agent 形成独立形态与运维事故类**：Headlong 的第三种形态（非 reactive/非 cron），加上 OpenClaw 升级（SQLite 破坏性迁移、split-brain、官方建议「用 coding harness 修 agent」的套娃现象）——「agent 长期运行」正产生自己的故障模式，且**评测与成本建模滞后**。
- **单人 CLI → 团队驾驶舱/共享工作区**：OpenClaw 2.0 多用户 Gateway+Swarm、AgentRoom CRDT 并发、Headlong 多用户共享单 agent；CRDT/协同编辑技术流入 harness 层是新机制信号。注意一致性警示：协作控制≠安全边界、价值来自协调而非并发。
- **版本库成为 agent 治理面**：RAMP 把「提交型配置」当作成熟度代理指标，与 Klibsio（KMP 目录含 AGENTS.md 实践）呼应——配置文件的版本化管理正在成为可测量的工程实践。
- **跨平台方向信号缺席（连续第二轮）**：LangChain/Google 检索多为聚合/营销内容，强素材集中在 HN/arXiv/独立工程博客——现有 Tier2/3 信源策略有效，但 KMP/Flutter 域需换定向源，否则该方向持续失联。

## 4. 收录建议

| 候选 | verdict | lineage | 一句话理由 |
|---|---|---|---|
| [3] CPE 上下文提权攻击 | `translate` | `agent/context` | 首个系统化 harness 上下文安全分类学（M-CPE/X-CPE）+ 12 系统实测，直接服务本库最薄弱的安全审计缺口，值得全篇留存做审计清单；arXiv 有 HTML 版可供翻译 |
| [5] Headlong | `translate` | `agent/harness` | 可运行的极简持久 micro-harness 全文：自唤醒循环、轨迹即上下文、指数衰减 compaction、沙箱与自伤事故，命中上下文/记忆可复现实践与 always-on 两个缺口 |
| [7] DecodingAI 上下文工程第 4 课 | `translate` | `agent/context` | 记忆/技能/LSP/压缩四件套 + 可运行 Python 代码，是缺口「可复现实践」最可直接落地的原文，与 Claude 模型级 context rules 待处理项互补 |
| [2] SWE-Gate | `index` | `agent/eval` | 开源评测 + 34% 功能通过≠评审通过量化结论，改写 coding agent 验收标准讨论，索引即可（价值在数据集与归因结论） |
| [4] FrontierHarness Eval | `index` | `agent/eval` | 开源受控 harness×成本数据可作选型锚点与第二组互证基线；交互式数据表格不值得整译 |
| [1] RAMP（A Few Pages of Markdown） | `index` | `agent/harness` | 441 仓库实证 + 可复用 RAMP 工具，为 AGENTS.md 治理主线提供量化证据与挑战，索引含脉络即可 |
| [9] AgentRoom | `index` | `agent/multi-agent` | 机制级开放协议 + 「协调优于并发」反直觉结论，补多 agent 协作空白；论文全文译价值低于索引+后续扩展 |
| [6] Rachel Laycock 代码评审论 | `index` | `agent/eval` | Tier1 有具名对手的流程辩论，与 SWE-Gate 构成闭环；观点文不整译 |
| [8] 让数据为 Agentic AI 就绪 | `index` | `agent/rag` | Tier1 双作者模式目录（契约/隔离/语义层/linage），数据×agent 相邻扩展的可检索权威链接 |
| [10] OpenClaw 2.0 掘金长文 | `index` | `agent/platform` | 窗口内中文原创深度分析 + 产品级多用户/多 agent/升级反模式一手细节，编入平台脉络（主事实仍以官方为准） |

合计 `translate=3`、`index=7`、`observe=0`，满足硬性要求；无条目降为 observe——10 条均直接命中知识库方向或缺口，且与已收录/已跟踪 URL 无重复。

```json
{
  "analysis": {
    "priority": [
      "CPE 上下文提权攻击最高优先：M-CPE/X-CPE 新分类学 + 12 个真实 harness（含 Codex/Claude Code）系统审计，直击最薄弱的安全审计缺口，translate 全篇留存做审计清单",
      "FrontierHarness Eval 次优：data-eng-bench 之后第二组开源受控 harness×成本数据，通过率差 17pp/成本差 17x + 缓存命中率≠成本，支撑评测归因与选型",
      "SWE-Gate 第三：303 实例证明功能通过≠评审约束通过（34% 差距），把评测验收拉到真实合入门槛，与 Laycock 评审辩论构成闭环",
      "Headlong 与 DecodingAI 第 4 课并列：分别提供可运行的指数衰减 compaction 与记忆/技能/LSP/压缩四件套代码，直接填上下文/记忆可复现实践缺口",
      "RAMP/AgentRoom 其次：前者把 AGENTS.md 个案升级为 441 仓库量化证据，后者给出多 agent『协调优于并发』的机制级实验",
      "跨平台方向本轮零达标，不硬凑；KMP/Flutter 与跨平台 CI/发布缺口顺延并建议下一轮定向补源"
    ],
    "gaps_covered": [
      "Agent 安全审计：CPE 的 M-CPE/X-CPE 攻击分类 + 12 harness 实测（含 Codex/Claude Code），上下文组装首次被当作信任边界",
      "Agent 安全审计（产品侧）：OpenClaw 2.0 会话三档可见/按会话沙箱/凭据只写/出站绑死、roles≠租户隔离、自适应注入>80%",
      "上下文/compaction/记忆可复现实践：Headlong 指数衰减分辨率压缩 + 轨迹即上下文，DecodingAI 记忆文件上限/LSP 反馈环/会话单行压缩",
      "Agent 评测组件级归因：FrontierHarness 固定模型/任务/运行时下 9 harness 的成本×质量矩阵与 17 倍成本差",
      "Agent 评测验收现实性：SWE-Gate 的评审派生约束双门控，644 次功能通过中 221 次违规",
      "多智能体编排反模式：AgentRoom 证明收益来自协调本身而非并行/CRDT；OpenClaw Swarm 提供实验态产品参照",
      "AGENTS.md/提交型配置治理：RAMP 四级成熟度模型 + 441 仓库量化（无配置认知复杂度 +53% vs +27%）",
      "中小团队成本锚点（部分）：FrontierHarness 单次通过成本 $1.05-$18.34 受控基线，非现场数据"
    ],
    "gaps_open": [
      "跨模型可移植性与迁移指南：本轮无直接命中（中立模型选择只是评测去偏，非迁移方法论）",
      "KMP/CMP vs Flutter 架构选型、共享逻辑边界、工具链痛点；跨平台 CI/发布/性能基线（连续两轮空窗，需定向补源）",
      "Harness 自身行为/覆盖率的度量工具：SWE-Gate/FrontierHarness 均测任务侧，不测 harness 内部逻辑覆盖率",
      "激活策略（always-on/per-commit/conditional/human-summoned）系统化比较：仅 Headlong/OpenClaw 零散数据点",
      "长时程/持续 agent 评测方法论：Headlong 自陈仅能定性测量，无成熟基准",
      "多智能体权限隔离设计原语：CPE 给出攻击面，OpenClaw 明示协作控制非安全边界，缺可复用隔离模式",
      "生产环境（含模型/网关交互）的组件级归因：FrontierHarness 自曝局限，环境变量归因仍空"
    ],
    "trends": [
      "Harness 效应进入可复现评测品类：data-eng-bench、FrontierHarness、Terminal-Bench 论断三方独立互证「模型相同、harness 决定成本与排名」，与 ECC 的 harness 主战场论点一致",
      "竞争主轴从能力转向成本/效率：通过率收敛于 50-66.7% 而成本差 17 倍，『便宜地完成』成为独立技能，步数/token 计价成新度量",
      "评测验收向『人的验收现实』迁移：SWE-Gate 评审约束门禁 + Laycock 评审左移/按例外，与 SWE-Touch 同向，评审从仪式变成可机器判定的数据",
      "上下文从优化对象升级为信任边界：CPE 把攻击面上移到 message role 与作用域管理，context engineering 出现安全子域",
      "持久/自唤醒 agent 成为独立形态并产生自有故障类：自调度唤醒、SQLite 破坏性迁移、split-brain、『用 agent 修 agent』，评测与成本建模滞后",
      "单人 CLI 向团队驾驶舱/共享工作区演进：OpenClaw 多用户 Gateway+Swarm、AgentRoom CRDT 并发、Headlong 共享 agent，CRDT 机制流入 harness 层",
      "版本库成为 agent 治理面：RAMP 把提交型配置当成熟度代理指标，与 Klibsio 的 AGENTS.md 实践互证",
      "跨平台方向连续第二轮零信号：LangChain/Google 检索多营销内容，KMP/Flutter 需换定向信源，否则持续失联"
    ]
  },
  "candidates": [
    {
      "title": "What's in Your Agent's Context? Context Privilege Escalation Attacks against AI Agent Harness",
      "url": "http://arxiv.org/abs/2609.01222",
      "source": "arXiv (Zichuan Li, Xiaojing Liao, Luyi Xing 等)",
      "date": "2026-09-01",
      "verdict": "translate",
      "lineage": "agent/context",
      "reason": "首个系统化 harness 上下文安全分类学（M-CPE/X-CPE）+ 含 Codex/Claude Code 的 12 系统实测，直击安全审计最薄弱缺口，值得全篇留存做审计清单",
      "stars": 5
    },
    {
      "title": "Introducing FrontierHarness Eval: 9 harnesses, same model, cost per pass varies 17x",
      "url": "https://runta.com/blog/introducing-frontierharness-eval",
      "source": "Runta (Shilin Zhu, Shiqi Mei)；HN 81 分",
      "date": "2026-09-01",
      "verdict": "index",
      "lineage": "agent/eval",
      "reason": "开源受控 harness×成本×质量数据（360 试次、17 倍成本差、缓存命中率≠成本）作选型锚点与第二组互证基线，价值在数据与归因结论而非全文",
      "stars": 5
    },
    {
      "title": "SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents",
      "url": "http://arxiv.org/abs/2609.04167",
      "source": "arXiv cs.SE (Xin He, Yanlin Wang 等)",
      "date": "2026-09-03",
      "verdict": "index",
      "lineage": "agent/eval",
      "reason": "303 实例/34% 差距证明功能通过≠评审约束通过，开源双门控评测改写 coding agent 验收标准讨论，索引+数据集即可",
      "stars": 5
    },
    {
      "title": "Headlong: a microharness for persistent agents (Laude/MIT)",
      "url": "https://www.laude.org/updates/headlong-a-microharness-for-persistent-agents",
      "source": "Laude Institute；github.com/laude-institute/headlong",
      "date": "2026-08-24",
      "verdict": "translate",
      "lineage": "agent/harness",
      "reason": "可运行极简持久 micro-harness 全文：自唤醒循环、轨迹即上下文、指数衰减 compaction、沙箱与自伤事故，命中记忆可复现实践与 always-on 两个缺口",
      "stars": 4
    },
    {
      "title": "Context Engineering for Coding Agents (Building a Coding Agent From Scratch, Lesson 4)",
      "url": "https://www.decodingai.com/p/context-engineering-for-coding-agents",
      "source": "Paul Iusztin, Decoding AI Magazine",
      "date": "2026-08-25",
      "verdict": "translate",
      "lineage": "agent/context",
      "reason": "记忆/技能/LSP/压缩四件套 + 可运行 Python 代码与容量上限细节，是上下文工程缺口最可直接落地的原文",
      "stars": 4
    },
    {
      "title": "A Few Pages of Markdown: Committed AI Configuration and Lower Quality Cost after Coding-Agent Adoption",
      "url": "http://arxiv.org/abs/2608.25241",
      "source": "arXiv cs.SE (Yegor Denisov-Blanch 等)",
      "date": "2026-08-26",
      "verdict": "index",
      "lineage": "agent/harness",
      "reason": "441 仓库量化 + RAMP 成熟度工具为 AGENTS.md 治理主线提供实证并提示『set-and-forget』治理缺口，索引含脉络即可",
      "stars": 4
    },
    {
      "title": "AgentRoom: Concurrent Multi-Agent Coding in a CRDT-Backed Shared Workspace",
      "url": "http://arxiv.org/abs/2608.23740",
      "source": "arXiv (Seonglae Cho, Donghyun Lee)",
      "date": "2026-08-24",
      "verdict": "index",
      "lineage": "agent/multi-agent",
      "reason": "CRDT 文件系统+MCP claim/broadcast 的机制级开放实验，『协调优于并发』反直觉结论补多 agent 协作空白，索引后按需扩展",
      "stars": 4
    },
    {
      "title": "Maybe We Shouldn't Be Reviewing All This Code",
      "url": "https://martinfowler.com/rachels-ramblings/code-review.html",
      "source": "Rachel Laycock, martinfowler.com",
      "date": "2026-09-02",
      "verdict": "index",
      "lineage": "agent/eval",
      "reason": "Tier1 有具名对手与 Meta 数据的流程辩论，与 SWE-Gate 构成『评审左移+机器可判约束』闭环，观点文索引即可",
      "stars": 3
    },
    {
      "title": "Making Your Data Ready for Agentic AI",
      "url": "https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html",
      "source": "Pramod Sadalage & Prem Chandrasekaran, martinfowler.com",
      "date": "2026-08-27",
      "verdict": "index",
      "lineage": "agent/rag",
      "reason": "Tier1 双作者企业数据三层框架与模式目录，扩展数据×agent 相邻方向的可检索权威链接",
      "stars": 3
    },
    {
      "title": "憋了 7 周没动静，OpenClaw 2.0 带着 16000 个 PR 杀回来了",
      "url": "https://juejin.cn/post/7680352383386107940",
      "source": "一点一木, 稀土掘金",
      "date": "2026-09-01",
      "verdict": "index",
      "lineage": "agent/platform",
      "reason": "窗口内中文原创深度分析：多用户 Gateway/角色边界/Swarm/升级事故一手细节与反模式，编入平台脉络（主事实以官方为准）",
      "stars": 3
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
session id: 01a07910-c72b-7c83-87e1-0cce8141b439
--------
user
# 技术情报分析（Prompt B）

> 运行器：服务器 codex，由 `research.py` 第二段调用。输入为 Prompt A 的搜索结果；**不再负责搜索**。

以下是最近 2 周的技术情报搜索结果。请基于我们项目的已有内容，做以下分析：

Iimo%2F10J7cTtZHAtJmS9UtCM%3D)

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


### 请分析：

1. **优先级排序**：哪些内容最值得我们收录？考虑因素：
   - 对**已收录文章 + 已跟踪内容**（完整清单见下方「已知内容」，或 `references/articles.md` / `python scripts/retrack.py --list` 注入段）的补充价值
   - 对 `expand/thinking/` 中已有洞见的验证或挑战
   - 对开放问题清单的回答程度

2. **缺口分析**：这批内容覆盖了我们的哪些知识缺口？还有哪些缺口未被触及？
   当前已知缺口（对齐本知识库两大方向）：
   - Agent harness 行为正确性与覆盖率评估
   - 上下文 / compaction / 记忆策略的可复现实践
   - 多智能体编排反模式与成本
   - Agent 评测：model / harness / 环境的组件级归因
   - 跨模型可移植性与迁移指南
   - 中小团队 Agent 工程落地案例与成本数据
   - Harness / 控制的激活策略（always-on / per-commit / conditional / human-summoned）
   - Agent 安全审计（轨迹违规、多智能体信息流、工具权限边界）
   - KMP / Compose Multiplatform 与 Flutter 的架构选型、共享逻辑边界、工具链痛点
   - 跨平台 CI / 发布 / 性能基线

3. **趋势信号**：这批内容中是否有新的趋势或方向？与既有 Agent 工程 / 跨平台实践是否一致或冲突？

4. **收录建议**：对每条推荐内容给出具体建议（三选一，互斥）：
   - 收录到 references/articles.md（哪个脉络 lineage）→ verdict=`index`
   - 值得翻译到 working/ → verdict=`translate`
   - 暂不收录，持续观察 → verdict=`observe`

   **分类门槛（务必遵守，不要过度保守）**：
   - `translate`：有深度技术内容（架构方案 / 代码示例 / 基准数据 / 反模式），值得全篇翻译留存。Tier 1 来源（Anthropic / OpenAI / LangChain 官方博客）默认至少 `translate`。
   - `index`：对知识库有增量价值（填补上方缺口 / 验证或挑战既有观点 / 提供可检索的权威链接），但不值得全篇翻译。**如果一篇文章直接命中上方任一知识缺口，verdict 至少为 `index`，不得降为 `observe`。**
   - `observe`：仅当文章与知识库方向无直接关联、或为小版本更新（如 patch release）无实质架构变化时使用。
   - **硬性要求：每批 `translate + index` 合计 ≥ 2 条**；如果认为全部不达标，请在 analysis.priority 中明确说明每篇不达标的理由。

### 已知内容

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

### 输出要求

先用中文写出上述 1–4 的完整分析（可含表格与列表），再在文末附机器可读 JSON：

```json
{
  "analysis": {
    "priority": ["..."],
    "gaps_covered": ["..."],
    "gaps_open": ["..."],
    "trends": ["..."]
  },
  "candidates": [
    {
      "title": "...",
      "url": "...",
      "verdict": "index|translate|observe",
      "lineage": "agent/harness",
      "reason": "一句话",
      "stars": 4
    }
  ]
}
```

脉络（lineage）建议取值：`agent/rag` · `agent/harness` · `agent/orchestration` · `agent/context` · `agent/multi-agent` · `agent/eval` · `agent/platform` · `crossplatform/kmp` · `crossplatform/flutter` · `crossplatform/toolchain` · `general`（慎用）。

warning: Codex could not find bubblewrap on PATH. Install bubblewrap with your OS package manager. See the sandbox prerequisites: https://developers.openai.com/codex/concepts/sandboxing#prerequisites. Codex will use the bundled bubblewrap in the meantime.
warning: Model metadata for `deepseek-v4-flash` not found. Defaulting to fallback metadata; this can degrade performance and cause issues.
codex
我先浏览仓库结构，读取已知内容、thinking 洞见与开放问题，以便让分析与知识库对齐。
exec
/bin/bash -lc "cd /root/note-worker && pwd && ls -la && echo ---- && find . -maxdepth 2 -type d -not -path './.git*' | sort | head -50" in /root/note-worker
 succeeded in 0ms:
/root/note-worker
total 100
drwxr-xr-x 19 root root  4096 Sep  7 07:32 .
dr-xr-x--- 14 root root  4096 Sep  7 01:53 ..
dr-xr-xr-x  2 root root    40 Sep  7 07:32 .agents
dr-xr-xr-x  2 root root    40 Sep  7 07:32 .codex
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
----
.
./.agents
./.codex
./.firecrawl
./.obsidian
./.obsidian/plugins
./assets
./candidates
./candidates/20260809-180901
./candidates/20260810-115607
./candidates/20260817-062607
./candidates/research-20260810-115057
./candidates/research-20260907-071935
./docs
./docs/superpowers
./expand
./expand/03-后端
./expand/06-AI与LLM
./expand/thinking
./prompts
./prompts/feedback
./references
./scripts
./scripts/__pycache__
./templates
./wiki
./wiki/AI与LLM
./wiki/Linux与工具链
./wiki/前端
./wiki/后端
./wiki/数据库
./wiki/数据结构与算法
./wiki/求职面试
./wiki/源码解读
./wiki/生活杂项
./wiki/编程语言
./wiki/逆向与安全
./working

exec
/bin/bash -lc 'cd /root/note-worker && echo ====references==== && ls -la references && echo ====expand/thinking==== && ls -la expand/thinking && echo ====prompts==== && find prompts -type f | head -30 && echo ====candidates/latest==== && ls -la candidates/research-20260907-071935 2>/dev/null | head -20' in /root/note-worker
 succeeded in 0ms:
====references====
total 32
drwxr-xr-x  2 root root  4096 Sep  7 07:19 .
drwxr-xr-x 19 root root  4096 Sep  7 07:32 ..
-rw-r--r--  1 root root  1703 Aug 10 11:38 agents.md
-rw-r--r--  1 root root 20082 Sep  7 07:19 articles.md
====expand/thinking====
total 28
drwxr-xr-x 2 root root 4096 Aug  9 14:21 .
drwxr-xr-x 5 root root 4096 Sep  7 07:19 ..
-rw-r--r-- 1 root root 1032 Aug  9 13:37 AGENTS.md
-rw-r--r-- 1 root root 7019 Aug  9 13:59 MCP协议标准化的增量与边界.md
-rw-r--r-- 1 root root 7300 Aug  9 14:21 Rust2024版次的语义收紧与异步闭合.md
====prompts====
prompts/ingest.md
prompts/research-search.md
prompts/curate-review.md
prompts/curate.md
prompts/AGENTS.md
prompts/feedback/README.md
prompts/research-tracker.md
prompts/worker.md
prompts/deep-research-tracker.md
====candidates/latest====
total 352
drwxr-xr-x 2 root root   4096 Sep  7 07:32 .
drwxr-xr-x 7 root root   4096 Sep  7 07:19 ..
-rw-r--r-- 1 root root 349912 Sep  7 07:32 search.md

exec
/bin/bash -lc 'cd /root/note-worker && cat references/agents.md && echo ======== && cat references/articles.md' in /root/note-worker
 succeeded in 0ms:
# references/ — 外部资源索引

指外：持续输入的源头（Phase 0 采集层）。**这里是指针，不是内容本身。** 原始素材不做留存，
只做「收录 → 判值 → 归入产出模块」的跟踪索引，避免重复采集。

## 文件约定

| 文件 | 职责 | 谁维护 |
|------|------|--------|
| `articles.md` | 文章收录权威索引（编号正文 + 待处理 + 观察项） | `research.py` 分流写入；`curate.py` 落位回写 |
| `agents.md` | 本目录规则（本文） | 人工 + AI |

- 每条记录包含：编号、标题、链接、作者、日期、状态（待处理/已收录/已淘汰）、归属（产出模块路径）
- **状态机**：research `translate`→`待处理`→curate 落位→`已收录`；`index` 直接`已收录`；`observe`→观察项表；或`已淘汰`

## 索引 → 产出的分流规则（codex 处理素材时判定归属）

| 产出方向 | 落点 | 何时 |
|---------|------|------|
| 值得翻译 | `working/`（经 curate 唯一终审 PR） | research `translate` |
| 仅索引收录 | articles.md `已收录`（核心含脉络） | research `index` |
| 持续观察 | articles.md「观察项」表 | research `observe` |
| 独立思考 / 观点 | `expand/thinking/` | 人写；codex 只建议 |
| 提示词沉淀 | `prompts/` | 人判亲测有效 |

## 与其他目录的关系

- `expand/` ← AI 独立思考产物（thinking 主导，concepts/深度笔记存量保留）
- `working/` ← 作品输出（Phase 输出层）
- `prompts/` ← 验证有效提示词
- `feedback/` ← 复盘迭代（lint 巡检报告 + failure 记录）
- 一致性：K1 状态机在本文 + `scripts/check_consistency.py` 把关========
# 文章索引

> **本文件是文章索引与计数的最佳事实来源（single source of truth）。**
>
> **计数规则（machine-checkable）：**
> 一篇文章 = 一个 `### N. {标题}` 形式的编号小节，且不属于本文末尾的「已淘汰 / 待补充」段落。
> 占位条目（"待处理 / 待补充"）**不写在编号正文里**，而是统一进本文末尾的「待处理队列」，避免污染计数。
> 全局连续编号（不按来源重置），最大编号 = 文章总数。
>
> **状态字段（流程机器码）：** `待处理`（research 判定值得翻译，入队） / `已收录`（索引收录或译文已落 working） / `已淘汰`（判定不值，保留 URL 防重复采集）。
> **归属字段：** `working/…` 作品路径，或仅索引时的 `脉络:<lineage>`，或 `prompts/…` / `expand/…`。
> **观察项：** 见文末「观察项」表（不进编号正文、不计入主计数）；research 分流 `observe` 写入。
>
> **流水线（2026-08-10）：** research 写入 `pipeline/queue`（不开 PR）→ curate 落位并开**唯一终审 PR** → 人工合并 main。
>
> **下游引用都是本文的冗余缓存：** 根 `AGENTS.md`、`expand/index.md`、`references/AGENTS.md` 的概览表。
> 新增/更新文章时，必须**同一次提交**更新本文 + 相关下游缓存。

## 待处理（采集队列，计入编号正文前的暂存区）

> 由 `research.py`（verdict=`translate`）写入。curate 加工落位后移入编号正文。

<!-- pending:start -->
<!-- 采集自动化维护，按 `| 标题 | 链接 | 来源 | 日期 |` 追加一行；处理完移入编号正文 -->
<!-- 当前：1 条待处理 -->
| The new rules of context engineering for Claude 5 generation models | https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models | research | 2026-08-09 | 🔄评审中 candidates/20260809-180901/
| One-shotting a Raccoon Heist game using Claude Fable 5 | https://simonwillison.net/2026/Aug/5/raccoon-heist/ | research | 2026-08-09 | 🔄评审中 candidates/20260809-180901/
| Six Agent Orchestration Patterns | https://vercel.com/i/agent-orchestration-patterns | research | 2026-08-09 | 🔄评审中 candidates/20260809-180901/
| Making production-ready agents the default: building Duolingo's agent platform | https://blog.duolingo.com/production-ready-ai-agent-platform/ | research | 2026-08-09 | 🔄评审中 candidates/20260809-180901/
<!-- pending:end -->

## 已收录（编号正文）

### 01. arxiv — When Does On-Policy Interaction Help?

- **标题：** When Does On-Policy Interaction Help? Representational Tradeoffs in Value-Based Imitation Learning
- **链接：** [arxiv.org/abs/2607.29617v1](http://arxiv.org/abs/2607.29617v1)
- **作者：** arxiv 论文 | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/06-AI与LLM/Agent研究与评测/在线策略交互与模仿学习.md`
- **核心：** 专家交互放宽模仿学习表征需求，提出 OVI 算法。
- **关联：** Agent 模仿学习；`references/raw/` 已删除，素材散点见 expand 条目 sources 字段

### 02. AgentHPOBench — LLM Agents as Sequential Hyperparameter Optimizers

- **标题：** AgentHPOBench: A Benchmark For Evaluating LLM Agents as Sequential Hyperparameter Optimizers
- **链接：** [arxiv.org/abs/2607.29626v1](http://arxiv.org/abs/2607.29626v1)
- **作者：** arxiv 论文 | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/06-AI与LLM/Agent研究与评测/AgentHPOBench.md`
- **核心：** 7 类 30 任务，评估 LLM Agent 作为顺序超参数优化器。
- **关联：** Agent 评测基准

### 03. ExtractBench — Schema-Guided Enterprise Document Extraction

- **标题：** ExtractBench: A Benchmark for Schema-Guided Enterprise Document Extraction
- **链接：** [arxiv.org/abs/2607.29677v1](http://arxiv.org/abs/2607.29677v1)
- **作者：** arxiv 论文 | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/06-AI与LLM/Agent研究与评测/ExtractBench.md`
- **核心：** 370 文档 / 4869 页，模式引导的企业文档提取基准。
- **关联：** RAG + 文档解析

### 04. DungeonBench — Rules-Rich Tactical Reasoning

- **标题：** DungeonBench: A Benchmark for Rules-Rich Tactical Reasoning in Dungeons & Dragons Combat
- **链接：** [arxiv.org/abs/2607.29577v1](http://arxiv.org/abs/2607.29577v1)
- **作者：** arxiv 论文 | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/06-AI与LLM/Agent研究与评测/DungeonBench.md`
- **核心：** D&D 规则密集型战术推理基准（遭遇战 + 一日冒险双轨道）。
- **关联：** Agent 推理评测

### 05. MOT-SR — Multi-Objective Scientific Equation Discovery

- **标题：** MOT-SR: Multi-Objective Tool-Augmented Scientific Equation Discovery with Large Language Models
- **链接：** [arxiv.org/abs/2607.29561v1](http://arxiv.org/abs/2607.29561v1)
- **作者：** arxiv 论文 | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/06-AI与LLM/Agent研究与评测/MOT-SR.md`
- **核心：** 多目标工具增强符号回归框架（双 LLM 模块 + 帕累托前沿）。
- **关联：** 科学发现 + 工具调用

### 06. ECC — agent harness 操作系统

- **标题：** affaan-m/ECC — The agent harness performance optimization system
- **链接：** [github.com/affaan-m/ECC](https://github.com/affaan-m/ECC)
- **作者：** github | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/06-AI与LLM/Agent工具与平台/ECC.md`
- **核心：** 面向编程代理的 harness 操作系统：技能 / 记忆 / 安全 / 跨 harness 编排。
- **关联：** Agent 工程化 / harness

### 07. n8n — AI 原生工作流自动化平台

- **标题：** n8n-io/n8n — Fair-code workflow automation platform with native AI capabilities
- **链接：** [github.com/n8n-io/n8n](https://github.com/n8n-io/n8n)
- **作者：** github | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/06-AI与LLM/Agent工具与平台/n8n.md`
- **核心：** 可视化画布 + 1500+ 集成，自托管或云上 AI 原生工作流。
- **关联：** Workflow / Agent 调度

### 08. MarkItDown — 文件/文档转 Markdown

- **标题：** microsoft/markitdown — Python tool for converting files to Markdown
- **链接：** [github.com/microsoft/markitdown](https://github.com/microsoft/markitdown)
- **作者：** github | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/06-AI与LLM/Agent工具与平台/MarkItDown.md`
- **核心：** 任意文件转 LLM 友好 Markdown（架构 / 插件 / Azure 集成 / 安全实践）。
- **关联：** 数据管线 / 文档解析

### 09. Hermes-Agent — the agent that grows with you

- **标题：** NousResearch/hermes-agent — The agent that grows with you
- **链接：** [github.com/NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)
- **作者：** github | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/06-AI与LLM/Agent工具与平台/Hermes-Agent.md`
- **核心：** 自我改进 AI 代理——闭环学习与跨会话记忆。
- **关联：** Agent 自我改进

### 10. JavaGuide — Java 面试 & 后端面试指南

- **标题：** Snailclimb/JavaGuide — Java 面试 & 后端通用面试指南
- **链接：** [github.com/Snailclimb/JavaGuide](https://github.com/Snailclimb/JavaGuide)
- **作者：** github | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/03-后端/java/JavaGuide.md`
- **核心：** 计算机基础 / 数据库 / 分布式 / 高并发 / 系统设计 / AI 应用开发。
- **关联：** 后端 / 求职面试

### 11. Bonsai: Janestreet's UI Library

- **标题：** Bonsai: Janestreet's UI Library
- **链接：** [github.com/janestreet/bonsai](https://github.com/janestreet/bonsai)
- **作者：** HN | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** 淘汰
- **核心：** UI 库一个（排除原因：非本知识库范围，无 AI/后端关联，仅留 URL 防重复采集）
- **关联：** —

### 12. Prevent cognitive debt by manually retyping LLM-generated code

- **标题：** Prevent cognitive debt by manually retyping LLM-generated code
- **链接：** [ankursethi.com](https://ankursethi.com/blog/prevent-cognitive-debt-by-manually-retyping-llm-generated-code/)
- **作者：** HN | **日期：** 2026-08-03
- **状态：** 已淘汰 | **归属：** —
- **核心：** 独立已学，判定无深度加工价值
- **关联：** —

### 13. Qwen3.8-Max: A New Bar for Coding and Cowork

- **标题：** Qwen3.8-Max: A New Bar for Coding and Cowork
- **链接：** [qwen.ai](https://qwen.ai/blog?id=qwen3.8)
- **作者：** HN | **日期：** 2026-08-03
- **状态：** 已淘汰 | **归属：** —
- **核心：** 官方营销博文，技术增量有限
- **关联：** —

### 14. MCP 官方文档：Model Context Protocol 介绍

- **标题：** MCP 官方文档：Model Context Protocol 介绍
- **链接：** [modelcontextprotocol.io/introduction](https://modelcontextprotocol.io/introduction)
- **作者：** MCP 官方文档（modelcontextprotocol.io） | **日期：** 2026-08-09
- **状态：** 已收录 | **归属：** `expand/thinking/MCP协议标准化的增量与边界.md`
- **核心：** 官方入门与架构——「AI 应用的 USB-C」定位、数据层/传输层双层、2026-07-28 版增量（MCP Apps / Agent Skills / Registry / server/discover）。思考：协议只标准化「连接信封」，工具语义仍靠 server 自治，M×N 适配成本转移而非消失。
- **关联：** MCP / Agent 工具生态；既有笔记 [[MCP协议与工具调用]]、Claude Code [[12-mcp-xie-yi-ji-cheng]]

### 15. Rust 2025 官方博客：Rust 1.85 版本说明（Move 语义 / Borrow Checker 演进）

- **标题：** Rust 2025 官方博客：Rust 1.85 版本说明（Move 语义 / Borrow Checker 演进）
- **链接：** [blog.rust-lang.org/2025/02/20/Rust-1.85.0.html](https://blog.rust-lang.org/2025/02/20/Rust-1.85.0.html)
- **作者：** The Rust Release Team（blog.rust-lang.org） | **日期：** 2025-02-20（采集 2026-08-09）
- **状态：** 已收录 | **归属：** `expand/thinking/Rust2024版次的语义收紧与异步闭合.md`
- **核心：** Rust 1.85.0 同步稳定 2024 Edition（官方口径「史上最大版次」）：RPIT 生命周期捕获规则、临时作用域/drop 顺序、match 擦除保留、unsafe extern/属性/static mut 收缩、set_var 转 unsafe、async closures（AsyncFn）稳定、元组 collect 扩展至 12 元。思考：采集器「Move 语义」标签失焦——真正主线是「版次语义收紧 + unsafe 显式化 + 异步借用补课」，edition 约三年一拍是 Rust 的语义债务清偿机制。
- **关联：** Rust / 版次 / 借用检查；对照 [[c++核心编程]]、思考层 [[MCP协议标准化的增量与边界]]

### 16. Meta launches Muse Code for complex software work with persistent AI agents

- **标题：** Meta launches Muse Code for complex software work with persistent AI agents
- **链接：** [www.infoworld.com/article/4206084/meta-launches-muse-code-for-complex-software-work-with-persistent-ai-agents.html](https://www.infoworld.com/article/4206084/meta-launches-muse-code-for-complex-software-work-with-persistent-ai-agents.html)
- **作者：** research | **日期：** 2026-08-09
- **状态：** 已收录 | **归属：** `working/Meta-launches-Muse-Code-for-complex-soft-translation.md`
- **核心：** Meta launches Muse Code for complex software work with persistent AI agents

### 17. Claude Code v2.1.224 — self-hosted environments

- **标题：** Claude Code v2.1.224 — self-hosted environments
- **链接：** [github.com/anthropics/claude-code/releases/tag/v2.1.224](https://github.com/anthropics/claude-code/releases/tag/v2.1.224)
- **作者：** research | **日期：** 2026-08-09
- **状态：** 已收录 | **归属：** `working/Claude-Code-v2-1-224-self-hosted-environ-translation.md`
- **核心：** Claude Code v2.1.224 — self-hosted environments

### 18. EvolveNet: Collaborative Harness Evolution for Agent Self-Improvement

- **标题：** EvolveNet: Collaborative Harness Evolution for Agent Self-Improvement
- **链接：** [arxiv.org/abs/2608.04968](https://arxiv.org/abs/2608.04968)
- **作者：** research | **日期：** 2026-08-09
- **状态：** 已收录 | **归属：** `working/EvolveNet-Collaborative-Harness-Evolutio-translation.md`
- **核心：** EvolveNet: Collaborative Harness Evolution for Agent Self-Improvement

### 19. Harness-R1: Learning to Edit Executable Runtime Harnesses from Agent Failure Trajectories

- **标题：** Harness-R1: Learning to Edit Executable Runtime Harnesses from Agent Failure Trajectories
- **链接：** [arxiv.org/abs/2608.02276](https://arxiv.org/abs/2608.02276)
- **作者：** research | **日期：** 2026-08-09
- **状态：** 已收录 | **归属：** `working/Harness-R1-Learning-to-Edit-Executable-R-translation.md`
- **核心：** Harness-R1: Learning to Edit Executable Runtime Harnesses from Agent Failure Tra…

### 20. I Gave Claude Code an AGENTS.md Contract and Stopped Babysitting It

- **标题：** I Gave Claude Code an AGENTS.md Contract and Stopped Babysitting It
- **链接：** [dev.to/daymondhyper/i-gave-claude-code-an-agentsmd-contract-and-stopped-babysitting-it-53m](https://dev.to/daymondhyper/i-gave-claude-code-an-agentsmd-contract-and-stopped-babysitting-it-53m)
- **作者：** research | **日期：** 2026-08-09
- **状态：** 已收录 | **归属：** `working/I-Gave-Claude-Code-an-AGENTS-md-Contract-translation.md`
- **核心：** I Gave Claude Code an AGENTS.md Contract and Stopped Babysitting It

### 21. The Shape of Things to Come, Part 1: The Continuous Thunderdome

- **标题：** The Shape of Things to Come, Part 1: The Continuous Thunderdome
- **链接：** [yegge.ai/essays/the-shape-of-things-to-come/](https://yegge.ai/essays/the-shape-of-things-to-come/)
- **作者：** research | **日期：** 2026-08-09
- **状态：** 已收录 | **归属：** `working/The-Shape-of-Things-to-Come-Part-1-The-C-translation.md`
- **核心：** The Shape of Things to Come, Part 1: The Continuous Thunderdome

## 观察项

> 暂不收录、持续观察的 URL（防重复采集，不计入编号正文主计数）。由 research Prompt B（`observe`）写入。

| 标题 | 链接 | 来源 | 日期 | 备注 |
| --- | --- | --- | --- | --- |
| Klibs.io Grows to 4200+ KMP Projects With Smarter Discovery and New AI Integrations | https://blog.jetbrains.com/kotlin/2026/08/klibsio-grows-to-4200-kmp-projects-with-smarter-discovery-and-new-ai-integrations/ | JetBrains Kotlin 博客 | 2026-08-17 | JetBrains 官方把 KMP 生态目录做成 agent 可调用工具，含评测数据与 AGENTS.md 实践，双领域交集标杆。 |
| What's new in Kotlin 2.4.20-RC | https://kotlinlang.org/docs/whatsnew-eap.html | Kotlin 官方文档 | 2026-08-12 | 官方 EAP 公告，覆盖标准库、K/N、K/Wasm、K/JS 多层实质变更，KMP 工具链风向标。 |
| What's new in Flutter 3.47 | https://flutter.dev/blog/whats-new-in-flutter-3-47 | Flutter 官方博客 | 2026-08-12 | 官方发布说明中设计系统解耦是长期架构调整信号，影响依赖管理与跨端构建策略。 |
| Conceptual integrity and counting lines of code | https://simonwillison.net/2026/Aug/19/conceptual-integrity-and-counting-lines-of-code/ | Simon Willison 博客 | 2026-08-19 | Tier 1 作者原创观点，挑战主流 LOC 无意义论，对 agent 工程管理/评测有启发。 |
| Introducing LangSmith Tuned Evaluators, starting with Perceived Error | https://www.langchain.com/blog/introducing-langsmith-tuned-evaluators-starting-with-perceived-error | LangChain 官方博客 | 2026-08-18 | 官方评测产品但技术实质充分（后训练法官+82% 成本数据+接入流程），对 agent 评测域有参考价值。 |
| Agentic Transaction: Towards ACID-Compliant Agent Systems | https://arxiv.org/abs/2608.13900 | arXiv cs.DB/cs.AI | 2026-08-14 | 原创理论框架+可运行系统，是 agent 可靠执行方向少见的系统性工作。 |
| The Devil Is in the Interface: Evaluating How Tool Architecture Shapes Coding Agent Behavior | https://arxiv.org/abs/2608.11386 | arXiv cs.SE | 2026-08-11 | 大样本受控实验+量化结论，为 harness/工具平台设计提供可复现证据。 |
| DeepSeek Harness 开发者预览：一切皆插件 | https://news.ycombinator.com/item?id=49285244 | DeepSeek 官方（Hacker News） | 2026-08-13 | 开源 agent harness 标杆事件，插件化架构与可追踪事件流直接回应 harness/编排主题，官方一级内容。 |
| Exploring Compose HTML for Server-Side Rendering | https://blog.jetbrains.com/kotlin/2026/08/exploring-compose-html-for-server-side-rendering/ | JetBrains | 2026-08-14 | 官方博客对 CMP 服务端渲染方向的原创前瞻，含可复现代码 |
| LiveMem: Maintaining Memory State Continuity in Long-Running LLM Inference | https://arxiv.org/abs/2608.02515 | arXiv cs.CL | 2026-08-03 | 为 agent 长会话记忆与上下文管理提供新抽象视角 |
| Everything we launched during Agents Week | https://blog.cloudflare.com/agents-week-review-august-2026/ | Cloudflare | 2026-08-10 | 云厂商对 agent 运行时与生命周期的一次系统性落子，平台趋势观察 |
| Announcing Dart 3.13 | https://dart.dev/blog/announcing-dart-3-13 | Dart / Google | 2026-08-12 | 官方稳定版发布，语言/工具链/编译优化多维实质更新 |
| IntelliJ IDEA Goes LSP: Java and Kotlin Intelligence Comes to VS Code, Cursor, and Agentic Flows | https://blog.jetbrains.com/idea/2026/08/intellij-idea-goes-lsp/ | JetBrains | 2026-08-04 | Kotlin 工具链×agent 工作流交叉的一手官方进展 |
| Deep Agents vs LangChain vs LangGraph | https://www.langchain.com/blog/deep-agents-vs-langchain-vs-langgraph | LangChain | 2026-08-06 | 官方对 agent 栈分层与 harness 定义的权威界定，指导选型 |
| SHE: Trajectory-driven Safety Harness Evolution for LLM Agents | https://arxiv.org/abs/2608.09885 | arXiv cs.AI | 2026-08-10 | 首个可演化安全 harness 系统化框架，有数据与复现链接 |
| SWE-Touch: Benchmarking Coding Agents When Users Touch the Code | https://arxiv.org/abs/2608.02499 | arXiv cs.SE | 2026-08-03 | 填补人机协作共享工作区评测盲区，有数据与开源实现，挑战单干基准范式 |
| DeepSeek Harness developer preview: Everything is a plugin | https://deepseek.com/harness/en/ | DeepSeek | 2026-08-14 | 开源 harness 平台级发布，Claude Code 直接竞品，HN 732 分高热 |
| Auto mode is now the default in Claude Code for Pro, Max, and Team plans | https://claude.com/blog/auto-mode-default-in-claude-code | Anthropic | 2026-08-07 | Tier 1 官方一手安全数据，直接塑造 agent 权限与安全架构设计 |
| New release of LLM adds support for reasoning traces, OpenAI Responses, server-side tools, and smarter logging | https://simonwillison.net/2026/Aug/4/new-release-of-llm/ | Simon Willison (simonwillison.net) | 2026-08-04 | Tier1作者对LLM工具平台的深度工程复盘，含可复现代码，覆盖推理轨迹、服务端工具与日志架构。 |
| Introducing Data-eng-bench: Why You Need "Data-Native" Harnesses for Data Engineering | https://www.snowflake.com/en/blog/engineering/data-eng-bench-data-engineering-agent-benchmark/ | Snowflake AI Research (Snowflake Engineering Blog) | 2026-08-06 | 首个仓库级dbt agent评测（103任务）并开源，harness×模型双变量质量/成本数据直接服务agent评测与选型。 |

## 统计

- **正式收录：** 12 篇（编号 01-10、14、15）｜**已淘汰隔离：** 3 篇（编号 11-13，不计入收录数，仅防重复采集）

## 待补充

- [ ] 占位：外部新文章先查编号 01-15 确认未收，再由采集层写入「待处理」队列

exec
/bin/bash -lc "cd /root/note-worker && sed -n '60,240p' references/articles.md" in /root/note-worker
 succeeded in 0ms:

### 04. DungeonBench — Rules-Rich Tactical Reasoning

- **标题：** DungeonBench: A Benchmark for Rules-Rich Tactical Reasoning in Dungeons & Dragons Combat
- **链接：** [arxiv.org/abs/2607.29577v1](http://arxiv.org/abs/2607.29577v1)
- **作者：** arxiv 论文 | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/06-AI与LLM/Agent研究与评测/DungeonBench.md`
- **核心：** D&D 规则密集型战术推理基准（遭遇战 + 一日冒险双轨道）。
- **关联：** Agent 推理评测

### 05. MOT-SR — Multi-Objective Scientific Equation Discovery

- **标题：** MOT-SR: Multi-Objective Tool-Augmented Scientific Equation Discovery with Large Language Models
- **链接：** [arxiv.org/abs/2607.29561v1](http://arxiv.org/abs/2607.29561v1)
- **作者：** arxiv 论文 | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/06-AI与LLM/Agent研究与评测/MOT-SR.md`
- **核心：** 多目标工具增强符号回归框架（双 LLM 模块 + 帕累托前沿）。
- **关联：** 科学发现 + 工具调用

### 06. ECC — agent harness 操作系统

- **标题：** affaan-m/ECC — The agent harness performance optimization system
- **链接：** [github.com/affaan-m/ECC](https://github.com/affaan-m/ECC)
- **作者：** github | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/06-AI与LLM/Agent工具与平台/ECC.md`
- **核心：** 面向编程代理的 harness 操作系统：技能 / 记忆 / 安全 / 跨 harness 编排。
- **关联：** Agent 工程化 / harness

### 07. n8n — AI 原生工作流自动化平台

- **标题：** n8n-io/n8n — Fair-code workflow automation platform with native AI capabilities
- **链接：** [github.com/n8n-io/n8n](https://github.com/n8n-io/n8n)
- **作者：** github | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/06-AI与LLM/Agent工具与平台/n8n.md`
- **核心：** 可视化画布 + 1500+ 集成，自托管或云上 AI 原生工作流。
- **关联：** Workflow / Agent 调度

### 08. MarkItDown — 文件/文档转 Markdown

- **标题：** microsoft/markitdown — Python tool for converting files to Markdown
- **链接：** [github.com/microsoft/markitdown](https://github.com/microsoft/markitdown)
- **作者：** github | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/06-AI与LLM/Agent工具与平台/MarkItDown.md`
- **核心：** 任意文件转 LLM 友好 Markdown（架构 / 插件 / Azure 集成 / 安全实践）。
- **关联：** 数据管线 / 文档解析

### 09. Hermes-Agent — the agent that grows with you

- **标题：** NousResearch/hermes-agent — The agent that grows with you
- **链接：** [github.com/NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)
- **作者：** github | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/06-AI与LLM/Agent工具与平台/Hermes-Agent.md`
- **核心：** 自我改进 AI 代理——闭环学习与跨会话记忆。
- **关联：** Agent 自我改进

### 10. JavaGuide — Java 面试 & 后端面试指南

- **标题：** Snailclimb/JavaGuide — Java 面试 & 后端通用面试指南
- **链接：** [github.com/Snailclimb/JavaGuide](https://github.com/Snailclimb/JavaGuide)
- **作者：** github | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** `expand/03-后端/java/JavaGuide.md`
- **核心：** 计算机基础 / 数据库 / 分布式 / 高并发 / 系统设计 / AI 应用开发。
- **关联：** 后端 / 求职面试

### 11. Bonsai: Janestreet's UI Library

- **标题：** Bonsai: Janestreet's UI Library
- **链接：** [github.com/janestreet/bonsai](https://github.com/janestreet/bonsai)
- **作者：** HN | **日期：** 2026-08-03
- **状态：** 已收录 | **归属：** 淘汰
- **核心：** UI 库一个（排除原因：非本知识库范围，无 AI/后端关联，仅留 URL 防重复采集）
- **关联：** —

### 12. Prevent cognitive debt by manually retyping LLM-generated code

- **标题：** Prevent cognitive debt by manually retyping LLM-generated code
- **链接：** [ankursethi.com](https://ankursethi.com/blog/prevent-cognitive-debt-by-manually-retyping-llm-generated-code/)
- **作者：** HN | **日期：** 2026-08-03
- **状态：** 已淘汰 | **归属：** —
- **核心：** 独立已学，判定无深度加工价值
- **关联：** —

### 13. Qwen3.8-Max: A New Bar for Coding and Cowork

- **标题：** Qwen3.8-Max: A New Bar for Coding and Cowork
- **链接：** [qwen.ai](https://qwen.ai/blog?id=qwen3.8)
- **作者：** HN | **日期：** 2026-08-03
- **状态：** 已淘汰 | **归属：** —
- **核心：** 官方营销博文，技术增量有限
- **关联：** —

### 14. MCP 官方文档：Model Context Protocol 介绍

- **标题：** MCP 官方文档：Model Context Protocol 介绍
- **链接：** [modelcontextprotocol.io/introduction](https://modelcontextprotocol.io/introduction)
- **作者：** MCP 官方文档（modelcontextprotocol.io） | **日期：** 2026-08-09
- **状态：** 已收录 | **归属：** `expand/thinking/MCP协议标准化的增量与边界.md`
- **核心：** 官方入门与架构——「AI 应用的 USB-C」定位、数据层/传输层双层、2026-07-28 版增量（MCP Apps / Agent Skills / Registry / server/discover）。思考：协议只标准化「连接信封」，工具语义仍靠 server 自治，M×N 适配成本转移而非消失。
- **关联：** MCP / Agent 工具生态；既有笔记 [[MCP协议与工具调用]]、Claude Code [[12-mcp-xie-yi-ji-cheng]]

### 15. Rust 2025 官方博客：Rust 1.85 版本说明（Move 语义 / Borrow Checker 演进）

- **标题：** Rust 2025 官方博客：Rust 1.85 版本说明（Move 语义 / Borrow Checker 演进）
- **链接：** [blog.rust-lang.org/2025/02/20/Rust-1.85.0.html](https://blog.rust-lang.org/2025/02/20/Rust-1.85.0.html)
- **作者：** The Rust Release Team（blog.rust-lang.org） | **日期：** 2025-02-20（采集 2026-08-09）
- **状态：** 已收录 | **归属：** `expand/thinking/Rust2024版次的语义收紧与异步闭合.md`
- **核心：** Rust 1.85.0 同步稳定 2024 Edition（官方口径「史上最大版次」）：RPIT 生命周期捕获规则、临时作用域/drop 顺序、match 擦除保留、unsafe extern/属性/static mut 收缩、set_var 转 unsafe、async closures（AsyncFn）稳定、元组 collect 扩展至 12 元。思考：采集器「Move 语义」标签失焦——真正主线是「版次语义收紧 + unsafe 显式化 + 异步借用补课」，edition 约三年一拍是 Rust 的语义债务清偿机制。
- **关联：** Rust / 版次 / 借用检查；对照 [[c++核心编程]]、思考层 [[MCP协议标准化的增量与边界]]

### 16. Meta launches Muse Code for complex software work with persistent AI agents

- **标题：** Meta launches Muse Code for complex software work with persistent AI agents
- **链接：** [www.infoworld.com/article/4206084/meta-launches-muse-code-for-complex-software-work-with-persistent-ai-agents.html](https://www.infoworld.com/article/4206084/meta-launches-muse-code-for-complex-software-work-with-persistent-ai-agents.html)
- **作者：** research | **日期：** 2026-08-09
- **状态：** 已收录 | **归属：** `working/Meta-launches-Muse-Code-for-complex-soft-translation.md`
- **核心：** Meta launches Muse Code for complex software work with persistent AI agents

### 17. Claude Code v2.1.224 — self-hosted environments

- **标题：** Claude Code v2.1.224 — self-hosted environments
- **链接：** [github.com/anthropics/claude-code/releases/tag/v2.1.224](https://github.com/anthropics/claude-code/releases/tag/v2.1.224)
- **作者：** research | **日期：** 2026-08-09
- **状态：** 已收录 | **归属：** `working/Claude-Code-v2-1-224-self-hosted-environ-translation.md`
- **核心：** Claude Code v2.1.224 — self-hosted environments

### 18. EvolveNet: Collaborative Harness Evolution for Agent Self-Improvement

- **标题：** EvolveNet: Collaborative Harness Evolution for Agent Self-Improvement
- **链接：** [arxiv.org/abs/2608.04968](https://arxiv.org/abs/2608.04968)
- **作者：** research | **日期：** 2026-08-09
- **状态：** 已收录 | **归属：** `working/EvolveNet-Collaborative-Harness-Evolutio-translation.md`
- **核心：** EvolveNet: Collaborative Harness Evolution for Agent Self-Improvement

### 19. Harness-R1: Learning to Edit Executable Runtime Harnesses from Agent Failure Trajectories

- **标题：** Harness-R1: Learning to Edit Executable Runtime Harnesses from Agent Failure Trajectories
- **链接：** [arxiv.org/abs/2608.02276](https://arxiv.org/abs/2608.02276)
- **作者：** research | **日期：** 2026-08-09
- **状态：** 已收录 | **归属：** `working/Harness-R1-Learning-to-Edit-Executable-R-translation.md`
- **核心：** Harness-R1: Learning to Edit Executable Runtime Harnesses from Agent Failure Tra…

### 20. I Gave Claude Code an AGENTS.md Contract and Stopped Babysitting It

- **标题：** I Gave Claude Code an AGENTS.md Contract and Stopped Babysitting It
- **链接：** [dev.to/daymondhyper/i-gave-claude-code-an-agentsmd-contract-and-stopped-babysitting-it-53m](https://dev.to/daymondhyper/i-gave-claude-code-an-agentsmd-contract-and-stopped-babysitting-it-53m)
- **作者：** research | **日期：** 2026-08-09
- **状态：** 已收录 | **归属：** `working/I-Gave-Claude-Code-an-AGENTS-md-Contract-translation.md`
- **核心：** I Gave Claude Code an AGENTS.md Contract and Stopped Babysitting It

### 21. The Shape of Things to Come, Part 1: The Continuous Thunderdome

- **标题：** The Shape of Things to Come, Part 1: The Continuous Thunderdome
- **链接：** [yegge.ai/essays/the-shape-of-things-to-come/](https://yegge.ai/essays/the-shape-of-things-to-come/)
- **作者：** research | **日期：** 2026-08-09
- **状态：** 已收录 | **归属：** `working/The-Shape-of-Things-to-Come-Part-1-The-C-translation.md`
- **核心：** The Shape of Things to Come, Part 1: The Continuous Thunderdome

## 观察项

> 暂不收录、持续观察的 URL（防重复采集，不计入编号正文主计数）。由 research Prompt B（`observe`）写入。

| 标题 | 链接 | 来源 | 日期 | 备注 |
| --- | --- | --- | --- | --- |
| Klibs.io Grows to 4200+ KMP Projects With Smarter Discovery and New AI Integrations | https://blog.jetbrains.com/kotlin/2026/08/klibsio-grows-to-4200-kmp-projects-with-smarter-discovery-and-new-ai-integrations/ | JetBrains Kotlin 博客 | 2026-08-17 | JetBrains 官方把 KMP 生态目录做成 agent 可调用工具，含评测数据与 AGENTS.md 实践，双领域交集标杆。 |
| What's new in Kotlin 2.4.20-RC | https://kotlinlang.org/docs/whatsnew-eap.html | Kotlin 官方文档 | 2026-08-12 | 官方 EAP 公告，覆盖标准库、K/N、K/Wasm、K/JS 多层实质变更，KMP 工具链风向标。 |
| What's new in Flutter 3.47 | https://flutter.dev/blog/whats-new-in-flutter-3-47 | Flutter 官方博客 | 2026-08-12 | 官方发布说明中设计系统解耦是长期架构调整信号，影响依赖管理与跨端构建策略。 |
| Conceptual integrity and counting lines of code | https://simonwillison.net/2026/Aug/19/conceptual-integrity-and-counting-lines-of-code/ | Simon Willison 博客 | 2026-08-19 | Tier 1 作者原创观点，挑战主流 LOC 无意义论，对 agent 工程管理/评测有启发。 |
| Introducing LangSmith Tuned Evaluators, starting with Perceived Error | https://www.langchain.com/blog/introducing-langsmith-tuned-evaluators-starting-with-perceived-error | LangChain 官方博客 | 2026-08-18 | 官方评测产品但技术实质充分（后训练法官+82% 成本数据+接入流程），对 agent 评测域有参考价值。 |
| Agentic Transaction: Towards ACID-Compliant Agent Systems | https://arxiv.org/abs/2608.13900 | arXiv cs.DB/cs.AI | 2026-08-14 | 原创理论框架+可运行系统，是 agent 可靠执行方向少见的系统性工作。 |
| The Devil Is in the Interface: Evaluating How Tool Architecture Shapes Coding Agent Behavior | https://arxiv.org/abs/2608.11386 | arXiv cs.SE | 2026-08-11 | 大样本受控实验+量化结论，为 harness/工具平台设计提供可复现证据。 |
| DeepSeek Harness 开发者预览：一切皆插件 | https://news.ycombinator.com/item?id=49285244 | DeepSeek 官方（Hacker News） | 2026-08-13 | 开源 agent harness 标杆事件，插件化架构与可追踪事件流直接回应 harness/编排主题，官方一级内容。 |
| Exploring Compose HTML for Server-Side Rendering | https://blog.jetbrains.com/kotlin/2026/08/exploring-compose-html-for-server-side-rendering/ | JetBrains | 2026-08-14 | 官方博客对 CMP 服务端渲染方向的原创前瞻，含可复现代码 |
| LiveMem: Maintaining Memory State Continuity in Long-Running LLM Inference | https://arxiv.org/abs/2608.02515 | arXiv cs.CL | 2026-08-03 | 为 agent 长会话记忆与上下文管理提供新抽象视角 |
| Everything we launched during Agents Week | https://blog.cloudflare.com/agents-week-review-august-2026/ | Cloudflare | 2026-08-10 | 云厂商对 agent 运行时与生命周期的一次系统性落子，平台趋势观察 |
| Announcing Dart 3.13 | https://dart.dev/blog/announcing-dart-3-13 | Dart / Google | 2026-08-12 | 官方稳定版发布，语言/工具链/编译优化多维实质更新 |
| IntelliJ IDEA Goes LSP: Java and Kotlin Intelligence Comes to VS Code, Cursor, and Agentic Flows | https://blog.jetbrains.com/idea/2026/08/intellij-idea-goes-lsp/ | JetBrains | 2026-08-04 | Kotlin 工具链×agent 工作流交叉的一手官方进展 |
| Deep Agents vs LangChain vs LangGraph | https://www.langchain.com/blog/deep-agents-vs-langchain-vs-langgraph | LangChain | 2026-08-06 | 官方对 agent 栈分层与 harness 定义的权威界定，指导选型 |
| SHE: Trajectory-driven Safety Harness Evolution for LLM Agents | https://arxiv.org/abs/2608.09885 | arXiv cs.AI | 2026-08-10 | 首个可演化安全 harness 系统化框架，有数据与复现链接 |
| SWE-Touch: Benchmarking Coding Agents When Users Touch the Code | https://arxiv.org/abs/2608.02499 | arXiv cs.SE | 2026-08-03 | 填补人机协作共享工作区评测盲区，有数据与开源实现，挑战单干基准范式 |
| DeepSeek Harness developer preview: Everything is a plugin | https://deepseek.com/harness/en/ | DeepSeek | 2026-08-14 | 开源 harness 平台级发布，Claude Code 直接竞品，HN 732 分高热 |
| Auto mode is now the default in Claude Code for Pro, Max, and Team plans | https://claude.com/blog/auto-mode-default-in-claude-code | Anthropic | 2026-08-07 | Tier 1 官方一手安全数据，直接塑造 agent 权限与安全架构设计 |

exec
/bin/bash -lc 'cd /root/note-worker && cat AGENTS.md' in /root/note-worker
 exited 1 in 0ms:
cat: AGENTS.md: No such file or directory

exec
/bin/bash -lc 'cd /root/note-worker && cat agents.md' in /root/note-worker
 succeeded in 0ms:
# 知识库规则（agents.md）

## 身份

你是个人知识库的管理助手。你的任务是阅读外部素材索引，将其加工为结构化、互相链接的知识条目，并按内容性质归入对应产出模块（expand/thinking、working/、prompts/）。

## 目录结构

```
D:\note\
├── references/  ← Phase 0：持续输入源头——纯索引，非正文
│   ├── agents.md   ← references 规则（分流 + 状态机）
│   └── articles.md ← 权威索引（编号正文 + 待处理 + 观察项；状态/归属机器可读）
├── wiki/          ← Phase 1：个人学习笔记（只读，仅用户本人修改；AI 不写入）
│   └── 01-编程语言/ ... 11-生活杂项/
├── expand/        ← Phase 2：AI 加工产物（thinking + 存量概念/深度笔记 + 索引）
│   ├── index.md   ← 全库总目录（含 working/ 作品；AI 维护；K2/K5）
│   ├── log.md     ← 变更日志
│   ├── 知识图谱.md ← 关系中枢
│   ├── thinking/   ← 独立思考/观点（新观点默认放这里）
│   └── 01-编程语言/ ... 11-生活杂项/
├── working/       ← Phase 4：译文作品（可独立理解；计入一致性图谱）
├── candidates/    ← 批次暂存（sources / research 分析落盘）
├── scripts/       ← research.py / curate.py / kb_common.py / 门禁与巡检
├── prompts/       ← research-search / research-tracker / curate（有效提示词）
│   └── feedback/
├── 私密/          ← 敏感信息（禁止进入知识图谱）
└── agents.md      ← 本规则文件
```

## 分类体系（wiki/ 顶层目录，如无法分类到其中，可以自行创建相关目录，更新目录结构）

| 目录 | 内容 | 来源 |
| --- | --- | --- |
| `01-编程语言` | C++ / Python 语言基础 | 原 c++、python |
| `02-前端` | HTML/JS/Vue/Layui/ECharts | 原 前端 |
| `03-后端` | Java/JavaWeb/中间件/项目（java、javaweb、中间件、OJ项目、苍穹 子目录） | 原 后端 |
| `04-数据库` | MySQL 及存储引擎（Mysql 子目录） | 原 数据库 |
| `05-数据结构与算法` | 排序/树/DP/BFS/贪心 | 原 数据结构和算法 |
| `06-AI与LLM` | Agent/RAG/MCP/微调/langchain4j/langgraph4j（AgentRag 学习、langchain4jlanggraph4j 学习 子目录） | 原 大模型 |
| `07-Linux与工具链` | Linux/Shell/Git | 原 Linux、git |
| `08-逆向与安全` | 汇编/花指令/CTF 题解 | 原 逆向 |
| `09-源码解读` | 项目源码分析（Claude Code源码解读、juedge0解析文档、Free-fs 子目录） | 原 Claude Code源码解读、juedge0解析文档、Free-fs |
| `10-求职面试` | 面试准备 | 原 AI-Agent代码审查系统 |
| `11-生活杂项` | 与编程无关的个人笔记 | 原 c++/Untitled.md |

## 核心操作

### 知识流水线（学习型体系 + 自动化主路径）

```
Phase 0 references/  ← 情报入队与状态机（articles.md）
Phase 1 wiki/        ← 个人学习笔记（只读）
Phase 2 expand/      ← AI 思考/概念 + 全库 index/log/图谱
Phase 3 prompts/     ← 验证有效提示词
Phase 4 working/     ← 译文作品输出
```

**自动化主路径（2026-08-10 起，整库只开一次人工 PR）：**

```
research.yml（每周/手动）→ SSH 同一次作业：
  1) research.py
     ├─ Prompt A（research-search.md）：强制 Firecrawl 搜索
     ├─ Prompt B（research-tracker.md）：长分析 + translate|index|observe
     └─ 写 articles.md → push origin/pipeline/queue（不开 PR）
  2) curate.py --limit 0（一次处理全部待处理，无 3h 轮询）
     ├─ 合并 pipeline/queue
     ├─ Codex（curate.md）产三件套 → 落位 working/
     ├─ 同步 expand/index.md、log.md、知识图谱.md、working/AGENTS.md
     └─ 开唯一终审 PR：review/<timestamp> → 人工合并 main
```

| research 分流 | 机器动作 |
|---------------|----------|
| `translate` | 入「待处理」→ curate 翻译 → `working/` + 编号「已收录」 |
| `index` | 直接编号「已收录」（核心含 `脉络:…`），不翻译 |
| `observe` | 「观察项」表，防重复采集 |

读完一篇后的人工去处（与自动化互补）：观点 → `expand/thinking/`；可展示译文 → `working/`；有效 prompt → `prompts/`。

### Ingest（摄入，手动 / 旁路）
当我说"摄入 [索引条目]"时（手动加工，非 curate 主路径）：
1. 读取 `references/articles.md` 的「待处理」队列或编号条目（含 URL/标题，不存素材正文）
2. 抓取原文后按「AI 生成条目模板」加工（含强制补全与 `[补充]` 溯源）
3. 检查 `expand/` 与 `wiki/` 中相关条目；**AI 生成/更新的条目一律写入 `expand/`**（`wiki/` 只读，绝不写入）——独立思考/观点统一写 `expand/thinking/`
4. 在 `expand/` 条目之间建立双向链接 `[[]]`，并更新相关条目的 `## 相关条目` 段；链接 `wiki/` 个人笔记为单向，回链由用户自行决定
5. 更新 `expand/index.md` 内容目录（含作品节时用 stem 双链）
6. 在 `expand/log.md` 中追加变更记录
7. 更新 `expand/知识图谱.md` 关系描述
8. 回写 `references/articles.md` 该条目的「状态/归属」字段

### Query（查询）
当我提出问题时：
1. 搜索 `wiki/` 中所有相关条目
2. 综合多个条目的信息，给出完整的回答
3. 如果发现知识缺口，建议需要补充的素材

### Lint（检查）
当我说"检查知识库"时：
1. 检查各条目之间是否存在矛盾
2. 找出孤立的（没有其他条目链接到的）条目
3. 标记可能过时的信息
4. 报告发现的问题和建议

### 一致性门禁（Consistency Gate）
> 自动执行，无需手动触发。`scripts/check_consistency.py` 实现 K1-K7 不变量检查；`.githooks/pre-commit` 本地提交前运行，`.github/workflows/consistency.yml` 在 CI 运行（分支保护下为必需检查）。

**K1-K7 违规自动修正原则（AI 在 Ingest / curate 落位 / 编辑时需遵守）**：
1. 新增 `expand/` 或 `working/` 条目**必须**同步 `expand/index.md`（计数 + 条目表）；`working/` 计入全库文件数（K2/K5）
2. AI 条目 frontmatter 必须含 `created / updated / sources / tags`（K3）
3. 只能在真实存在的条目之间建立 `[[]]` 链接；作品用 `[[stem]]`（勿写无法解析的 `[[working/…]]` 路径链）（K4）
4. `expand/` 必检文档中的 markdown 表格必须形状对齐（K6）
5. `references/articles.md` 编号条目的「状态：」必须 ∈ {待处理, 已收录, 已淘汰}；归属若指向磁盘路径须真实存在（K1）
- 本地校验：`python scripts/check_consistency.py`（需 `git config core.hooksPath .githooks`）

## 知识条目格式

每个 wiki 条目遵循以下格式（注意：**现有个人笔记内容保持不变**，仅在末尾追加 `## 相关条目`）：

    ---
    created: YYYY-MM-DD
    updated: YYYY-MM-DD
    sources: [来源文件列表]
    tags: [内容标签, type/论文|工具|教程|想法, status/待验证|已实践, 情绪标签(启发/反直觉)]
    ---

    # 条目标题

    一句话概述这个概念。

    ## 详细说明

    正文内容...

    ## 相关条目
    - [[相关条目A]]
    - [[相关条目B]]

### AI 生成条目：深度技术笔记模板（存量概念类，2026-08 起 expand 定位为 thinking）

> **当前默认：** expand/ 只承担 thinking（独立思考）作用。新摄入的外部素材默认进 `expand/thinking/`，
> 采用下方模板的「学习型相位结构」但聚焦独立观点；纯概念拆解/深度笔记（本模板）不再作为新条目默认，
> 仅当素材确实需要（技术深度大于观点价值）且用户明确要求时使用，写入对应 `expand/01-xx` 分类目录。

摄入外部素材（采集文章 / 论文 / 项目 / 视频）时，AI 按以下「深度技术笔记」模板加工。素材类型不适用的章节可精简，但核心章节不可省略；本模板取代原六维框架作为 AI 条目的输出标准。

**角色设定**：资深技术架构师，专注**两大追踪方向**：
1. **AI Agent 开发**：RAG、Agent 工程化（harness / 编排 / 上下文管理 / 调度）、多智能体架构、Agent 评测、Agent 工具与平台（LangChain/LangGraph、Claude Code、Codex 生态）
2. **跨平台开发**：Kotlin 多平台（KMP / Compose Multiplatform）、Flutter，共享逻辑 + 多端 UI 的落地架构

目标是让读者 15 分钟内理解核心原理并能直接应用于生产项目。素材与上述方向无关但确有技术价值时归入「通用技术」分类，不强行套用 Agent/跨平台视角。

**质量门槛（摄入前先过滤，不达标不要硬写）**：
- **必须满足（全部）**：有实质技术内容（非营销/软文）；有原创洞察、方案或可复现信息（非转述他人结论）；有可信来源（署名作者 / 官方文档 / 可验证链接）支撑 `[补充]` 溯源
- **加分项**：有实验数据/基准/成本对比；有可运行最小示例或架构图；直面失败案例/反模式/权衡；是 2 周内新进展或更新陈旧认知
- **直接排除**：纯标题空壳；纯榜单/招聘/无关娱乐；与知识库已有条目高度重复、无增量（见「知识关联地图」去重检查）
- 素材不达标时**不生成条目**，返回 `skip: true` 并附 `skip_reason`（ingest 时素材标为 `rejected`）

**加工规则**：
1. **强制补全与深度融合**：素材浅薄、逻辑不完整或缺代码示例时，主动补充外部权威知识（官方文档 / 源码解析 / 最新架构演进），并**直接融入正文结构**（概念拆解、方案对比、代码示例），不得仅作附加说明
2. **来源溯源**：补充内容在句末/段末用 `[补充]` 显式标注；**笔记必须标注参考素材（references/articles.md 编号条目）与相关官方网站链接**（专门的「参考素材与官方链接」章节）
3. **人话解释**：禁止照抄学术/教程表述，核心概念必须给"一句话人话解释"（生活化类比或底层逻辑推演）
4. **代码规范**：涉及代码必须给**生产级最小可运行示例**（含异常捕获、依赖锁定、安全边界），标注语言、框架、适用版本（如 "Kotlin 2.0 + KMP 1.9" 或 "langchain4j 2.x"）
5. **工程视角**：所有方案补充生产级落地考量（性能、安全、成本、异常处理）
6. **排版**：严格 Markdown，多用表格、列表、加粗，拒绝长篇段落

**输出结构**（不可省略章节）：

    ## 本周主题：{动态提取主题}
    ### 一句话总结
    > 不超过 50 字，概括素材核心价值与底层逻辑
    ### 记忆锚点（3 个关键记忆点）
    1. 一句话记忆点（可含选型口诀）
    ### 核心概念拆解
    - **概念名称**
      - 🗣️ 人话：通俗类比
      - 🔧 本质：底层原理一句话
      - 📍 定位：AI Agent（RAG / Agent 工程 / 调度）或跨平台（KMP / Flutter）哪一环
      - 💡 补充：[补充]（附官方链接）
    ### 架构与方案对比（如有选型）
    - **决策流程图**：先用 Mermaid 画极简决策树（如"扫描件→上云；普通文件→本地"）
    - 对比表：| 维度 | 方案A | 方案B | 方案C |（适用场景 / 核心优势 / 主要劣势 / 生产级成熟度（谨慎评级）/ 架构师推荐；[补充] 在单元格标注）
    ### 代码与实操速查
    - 生产级最小示例（异常捕获 / 版本锁定 / 安全边界，[补充] 生成需标注）/ 关键配置 / 常见报错 Top3
    ### 避坑清单（Anti-patterns）
    - 错误做法 → 正确做法（原因），至少 4 条（含大文件/内存、安全、依赖、性能类）
    ### 知识关联地图
    - 前置知识 / 横向关联（`[[条目]]` #标签，可点击可检索）/ 纵向延伸（具体资源名）——**去重检查**：与既有条目高度重复时，在「相关条目」引用而非重建
    ### 本周素材盲区与知识增量
    - 原文盲区 → 转化为「下周探索方向」（候选选题）/ 知识增量总结（2-3 条）
    ### 参考素材与官方链接
    - 原始素材索引：references/articles.md 编号条目（含来源 URL）
    - 官方文档 / 网站链接列表（带用途说明）
    ### 本周行动清单
    - [ ] 行动描述（预计耗时 / 关联知识点）✅ Done when：完成标准
    ### 相关条目
    - [[相关条目A]]

**技术说明**：管道已接入 Firecrawl Search 联网检索——`ingest.py` 会用素材主题检索并将真实结果注入 Prompt，`[补充]` 内容以检索结果为准并标注来源 URL；可用环境变量 `FIRECRAWL_SEARCH_DISABLED=1` 禁用检索。

## index.md 格式

`expand/index.md` 是**全库总目录**（wiki + expand + working），按分类组织，文首声明「全库共 N 个 Markdown 文件」须与磁盘一致：

    ## 01-编程语言
    - [[条目A]]：一句话描述

    ## 作品输出（working/）
    - [[某译文-stem]]：一句话摘要

## log.md 格式

变更日志按时间倒序排列：

    ## [YYYY-MM-DD] ingest | 来源标题
    - 新增：[[条目X]]
    - 更新：[[条目Y]]（新增关于...的内容）

## 链接约定

1. 优先使用短链接 `[[文件名]]`；文件名不唯一时（如两个 `集合.md`、两个 `free-fs.md`）使用路径链接 `[[分类/子目录/文件名]]`
2. 文件名含特殊字符（`#`、空格、长乱码）的笔记无法被链接解析，应建议重命名后再入图谱
3. 每次新增/更新条目后，同步维护 `wiki/知识图谱.md` 的关系描述
4. `wiki/` 个人笔记只读：AI 只可读取用于链接，不修改、不追加内容；如个人笔记需要回链到 `expand/` 条目，由用户手动添加

## 重要原则

1. 永远不要修改 `references/raw/` 中的原始素材（raw 已弃用；素材只存在于 articles.md 索引的 URL 指向的外部源）
2. **个人手写笔记内容不可改写**：只做分类、移动、追加 `## 相关条目` 链接，不重写正文、不删改原文
3. AI 生成的摘要性条目要简洁，用你自己的话总结，不要照搬原文
4. 积极建立条目之间的链接，形成知识网络
5. 每次摄入新素材时，要增量更新已有条目，而不是重新创建
6. 保持客观，标注信息来源
7. 敏感信息（密码、API Token、密钥）一律隔离到 `私密/`，不进入 `wiki/`，不建立任何链接；发现泄露的凭据时应提醒用户吊销/轮换
8. 遇到疑似重复笔记（内容高度相似）时，在 `index.md` 待办清单中标记，不擅自删除

## 维护待办（当前）

1. 补全空笔记（均在 `wiki/`，只读，需用户确认后由 AI 提炼或由用户补充）：`09-源码解读/Claude Code源码解读/8-queryengine-bian-pai-ji-zhi.md`、`09-源码解读/Claude Code源码解读/16-auto-mode-zi-dong-mo-shi.md`
2. 确认 `08-逆向与安全/未命名/` 目录残留（疑似已改名清理后的空壳，可删除）
3. 周期任务：`gc_report.py` 每周日跑（孤立/重复/空笔记/过期/断链/积压），`feedback_capture.py` 在 CI 失败时落盘 log.md
4. 安全提醒：`私密/密码管理.md` 中的 GitHub Token 建议立即吊销

exec
/bin/bash -lc "cd /root/note-worker && find expand/06-AI与LLM -type f -name '*.md' | head -60 && echo ==== && find . -maxdepth 3 -iname '*缺口*' -o -iname '*gap*' -o -iname '*问题*' | head -20 && echo ==== && find . -name '*.md' -path '*06-AI*' | wc -l" in /root/note-worker
 succeeded in 0ms:
expand/06-AI与LLM/Agent工具与平台/ECC.md
expand/06-AI与LLM/Agent工具与平台/n8n.md
expand/06-AI与LLM/Agent工具与平台/Hermes-Agent.md
expand/06-AI与LLM/Agent工具与平台/MarkItDown.md
expand/06-AI与LLM/Agent研究与评测/ExtractBench.md
expand/06-AI与LLM/Agent研究与评测/DungeonBench.md
expand/06-AI与LLM/Agent研究与评测/在线策略交互与模仿学习.md
expand/06-AI与LLM/Agent研究与评测/MOT-SR.md
expand/06-AI与LLM/Agent研究与评测/AgentHPOBench.md
====
====
9

exec
/bin/bash -lc 'cd /root/note-worker && cat prompts/research-tracker.md' in /root/note-worker
 succeeded in 0ms:
---
created: 2026-08-09
updated: 2026-08-10
type: workflow
status: 待验证
product: null
source: 知识库情报分析 Prompt B（搜后长分析）
---

# 技术情报分析（Prompt B）

> 运行器：服务器 codex，由 `research.py` 第二段调用。输入为 Prompt A 的搜索结果；**不再负责搜索**。

以下是最近 2 周的技术情报搜索结果。请基于我们项目的已有内容，做以下分析：

{SEARCH_OUTPUT}

### 请分析：

1. **优先级排序**：哪些内容最值得我们收录？考虑因素：
   - 对**已收录文章 + 已跟踪内容**（完整清单见下方「已知内容」，或 `references/articles.md` / `python scripts/retrack.py --list` 注入段）的补充价值
   - 对 `expand/thinking/` 中已有洞见的验证或挑战
   - 对开放问题清单的回答程度

2. **缺口分析**：这批内容覆盖了我们的哪些知识缺口？还有哪些缺口未被触及？
   当前已知缺口（对齐本知识库两大方向）：
   - Agent harness 行为正确性与覆盖率评估
   - 上下文 / compaction / 记忆策略的可复现实践
   - 多智能体编排反模式与成本
   - Agent 评测：model / harness / 环境的组件级归因
   - 跨模型可移植性与迁移指南
   - 中小团队 Agent 工程落地案例与成本数据
   - Harness / 控制的激活策略（always-on / per-commit / conditional / human-summoned）
   - Agent 安全审计（轨迹违规、多智能体信息流、工具权限边界）
   - KMP / Compose Multiplatform 与 Flutter 的架构选型、共享逻辑边界、工具链痛点
   - 跨平台 CI / 发布 / 性能基线

3. **趋势信号**：这批内容中是否有新的趋势或方向？与既有 Agent 工程 / 跨平台实践是否一致或冲突？

4. **收录建议**：对每条推荐内容给出具体建议（三选一，互斥）：
   - 收录到 references/articles.md（哪个脉络 lineage）→ verdict=`index`
   - 值得翻译到 working/ → verdict=`translate`
   - 暂不收录，持续观察 → verdict=`observe`

   **分类门槛（务必遵守，不要过度保守）**：
   - `translate`：有深度技术内容（架构方案 / 代码示例 / 基准数据 / 反模式），值得全篇翻译留存。Tier 1 来源（Anthropic / OpenAI / LangChain 官方博客）默认至少 `translate`。
   - `index`：对知识库有增量价值（填补上方缺口 / 验证或挑战既有观点 / 提供可检索的权威链接），但不值得全篇翻译。**如果一篇文章直接命中上方任一知识缺口，verdict 至少为 `index`，不得降为 `observe`。**
   - `observe`：仅当文章与知识库方向无直接关联、或为小版本更新（如 patch release）无实质架构变化时使用。
   - **硬性要求：每批 `translate + index` 合计 ≥ 2 条**；如果认为全部不达标，请在 analysis.priority 中明确说明每篇不达标的理由。

### 已知内容

{KNOWN_CONTENT}

### 输出要求

先用中文写出上述 1–4 的完整分析（可含表格与列表），再在文末附机器可读 JSON：

```json
{
  "analysis": {
    "priority": ["..."],
    "gaps_covered": ["..."],
    "gaps_open": ["..."],
    "trends": ["..."]
  },
  "candidates": [
    {
      "title": "...",
      "url": "...",
      "verdict": "index|translate|observe",
      "lineage": "agent/harness",
      "reason": "一句话",
      "stars": 4
    }
  ]
}
```

脉络（lineage）建议取值：`agent/rag` · `agent/harness` · `agent/orchestration` · `agent/context` · `agent/multi-agent` · `agent/eval` · `agent/platform` · `crossplatform/kmp` · `crossplatform/flutter` · `crossplatform/toolchain` · `general`（慎用）。

exec
/bin/bash -lc "cd /root/note-worker && rg -l \"缺口|两大方向|开放问题|检索清单|track\" --glob '*.md' | head -30" in /root/note-worker
 succeeded in 0ms:
agents.md
candidates/research-20260907-071935/search.md
candidates/20260817-062607/sources/Harness-R1-Learning-to-Edit-Executable-R-full.md
docs/superpowers/plans/2026-08-09-curate-pipeline.md
docs/superpowers/specs/2026-08-09-curate-pipeline-design.md
README.md
candidates/20260817-062607/sources/Harness-R1-Learning-to-Edit-Executable-R.md
candidates/20260817-062607/sources/The-Shape-of-Things-to-Come-Part-1-The-C.md
candidates/20260817-062607/sources/The-Shape-of-Things-to-Come-Part-1-The-C-full.md
candidates/20260817-062607/sources/EvolveNet-Collaborative-Harness-Evolutio-full.md
candidates/20260817-062607/sources/EvolveNet-Collaborative-Harness-Evolutio.md
candidates/20260809-180901/review.md
candidates/20260809-180901/works-ready/Six-Agent-Orchestration-Patterns-translation.md
candidates/20260809-180901/works-ready/One-shotting-a-Raccoon-Heist-game-using-translation.md
candidates/20260809-180901/translations/One-shotting-a-Raccoon-Heist-game-using/translation.md
candidates/20260809-180901/translations/One-shotting-a-Raccoon-Heist-game-using/01-analysis.md
candidates/20260809-180901/translations/Six-Agent-Orchestration-Patterns/translation.md
candidates/20260809-180901/translations/Six-Agent-Orchestration-Patterns/01-analysis.md
candidates/20260809-180901/sources/One-shotting-a-Raccoon-Heist-game-using-full.md
candidates/20260809-180901/sources/Making-production-ready-agents-the-defau.md
candidates/20260809-180901/sources/The-new-rules-of-context-engineering-for-full.md
candidates/20260809-180901/sources/Making-production-ready-agents-the-defau-full.md
candidates/20260809-180901/sources/One-shotting-a-Raccoon-Heist-game-using.md
candidates/20260809-180901/sources/Six-Agent-Orchestration-Patterns-full.md
candidates/research-20260810-115057/analyze.md
candidates/research-20260810-115057/search.md
wiki/AI与LLM/Agent/Harness Engineering 深度解析：AI Agent 时代的工程范式革命.md
wiki/AI与LLM/AgentRag 学习/Agent搭建.md
wiki/源码解读/opencode项目解读/系统优化专项.md
wiki/源码解读/opencode项目解读/业务背景重建.md

exec
/bin/bash -lc 'cd /root/note-worker && find expand -maxdepth 2 -type d | sort && echo ==== && ls expand && echo ==== && cat expand/AGENTS.md 2>/dev/null; cat expand/thinking/AGENTS.md' in /root/note-worker
 succeeded in 0ms:
expand
expand/03-后端
expand/03-后端/java
expand/06-AI与LLM
expand/06-AI与LLM/Agent工具与平台
expand/06-AI与LLM/Agent研究与评测
expand/thinking
====
03-后端
06-AI与LLM
index.md
log.md
thinking
动态索引.md
知识图谱.md
知识库周报.md
自动化工作流功能与实现方案.md
自动化工作流设计.md
====
# thinking/ — 独立思考（AI 主导）

expand/ 下的思考层。**读文章后的独立观点、质疑、延伸、综合**放这里；
纯概念拆解/深度笔记（存量）仍在 `expand/01-xx` 分类目录。

## 文件约定

- 文件名：自由命名，建议用问题或论点（如 `codex-as-execution-engine.md`、`harness-vs-mcp.md`）
- 结构：问题/论点 → 自己的分析 → 结论或开放问题
- frontmatter 沿用 AI 条目规范（created / updated / sources / tags）
- 鼓励质疑、反直觉，不做原文复述

## 与 references/articles.md 的联动

codex 处理一条文章（`### N.` 条目）后在此论坛所属：
- 有独立见解 → 在本目录生成 thinking 条目，并在 articles.md 该条目的「归属：」字段指向本文件
- 可产出作品 → `working/`
- 提炼有效 prompt → `prompts/`
- 无增量 → 仅标记已收录/已淘汰，不生成

## 已有思考

| 文件 | 话题 | 核心论点 |
|------|------|---------|
| （待首个条目） | — | — |
exec
/bin/bash -lc 'cd /root/note-worker && ls candidates/research-20260907-071935/ && ls candidates/20260817-062607/ && echo ==== && head -60 candidates/research-20260810-115057/analyze.md 2>/dev/null' in /root/note-worker
 succeeded in 0ms:
search.md
sources
====
已核对知识库现状（`references/articles.md` 15 条、`expand/thinking/` 2 条、`expand/06-AI与LLM/` 9 条、待处理队列 7 条）与 `research.py` 的三档分流逻辑。以下为完整分析。

## 1. 优先级排序

两条候选均为 AI Agent 域高价值内容，且与既有内容互补而非重复；跨平台侧无达标候选（不硬凑）。

| 优先级 | 候选 | 星级 | 与已收录/已跟踪内容的互补 | 对既有洞见的验证/挑战 | 对开放问题的回答 |
|---|---|---|---|---|---|
| 1 | Snowflake data-eng-bench | ⭐⭐⭐⭐⭐ | 编号 01–05 是任务级/领域级基准（模仿学习、HPO、文档抽取、战术推理、方程发现），**缺仓库级工程基准**；`ECC.md` 明确写着「盲区：缺少公开评测数据」，本候选直接补上 | **验证** `ECC.md`「harness 是工程化主战场」论点：harness 对质量差约 4pp、对成本差 3.9x，实证化「harness 操作系统」假设；同时**挑战**「选对模型即够用」的默认认知 | 正面回答「Agent 评测：model/harness 组件级归因」——给出 harness×model 双变量矩阵 |
| 2 | Simon Willison LLM 0.32 | ⭐⭐⭐⭐ | 待处理队列中的 Claude context engineering（prompt/上下文侧）与 Duolingo 平台案例（组织侧）均不覆盖**工具链与日志架构**；与 `MCP协议标准化的增量与边界`（thinking）形成「平台工具 ↔ 协议总线」对照 | **验证** MCP 思考条目的「外部能力总线」论点：llm-anthropic 0.26 的 `AnthropicMCP` 把 MCP 调用做成单请求服务端工具 | 部分回答「上下文/记忆策略的可复现实践」与「跨模型可移植性」两个缺口 |

与待处理队列关系：data-eng-bench 是 Harness-R1 / EvolveNet（harness 自我演进）所需要的**度量基底**；LLM 0.32 与 Raccoon Heist（同为 Simon Willison）主题不同，不构成重复采集。

## 2. 缺口分析

**被覆盖的缺口**
- Agent 评测组件级归因：harness×model 矩阵 + Pass@1/Pass^3 + 每试成本/token/工具调用/agent 步数，是目前唯一直接命中该缺口的素材。
- Agent harness 行为正确性与覆盖率：103 任务仓库级 dbt DAG（中位 4 个模型、最多 42 个）+ 每任务 10–50 条隐藏断言、整管道全对才计分，把「生成像样模型」与「管道正确」分开。
- 上下文/记忆可复现实践（部分）：内容寻址消息存储（Git 式）解决多轮日志膨胀；推理轨迹 stderr 分流是可复制的工具链标准做法。
- 跨模型可移植性（部分）：`llm openai endpoint` + `llm-chat-completions-server` 提供单命令对接任意 OpenAI 兼容端点的迁移路径。
- 成本数据（部分）：每试成本 0.358–0.756 美元、成本倍数 3.9x/1.5x，可作中小团队选型锚点（非完整案例，故算部分覆盖）。

**仍未触及的缺口**
- 多智能体编排反模式与成本：搜索仅触及 survey（`Multi-Agent Debate Strategies`），未入选。
- Harness/控制的激活策略（always-on / per-commit / conditional / human-summoned）。
- Agent 安全审计（轨迹违规、多智能体信息流、工具权限边界）。
- KMP / Compose Multiplatform 与 Flutter 架构选型、共享逻辑边界、工具链痛点。
- 跨平台 CI / 发布 / 性能基线。
- 衍生新缺口：data-eng-bench 只归因 harness 与 model 两变量，「环境/仓库规模」维度（数据仓库拓扑对结果的影响）未展开，可作后续追踪方向。

## 3. 趋势信号

- **Harness 效应实证化**：评测开始把 harness 作为独立变量（质量差 ~4pp、成本差 ~3.9x），与 `ECC.md` 的 harness 层论点一致；但 CoCo 的胜出提示「域原生 harness」比「通用分层 harness」更优——这是对 ECC 通用化路线的一个温和修正信号。
- **可靠性指标标准化**：Pass@1（单次）与 Pass^3（三试全过）并列披露，把 agent 非确定性显式化，呼应本库对 agent 可靠性的关注。
- **服务端工具 + 推理轨迹成为一等公民**：OpenAI `CodeInterpreter`/`WebSearch`、Anthropic `WebFetch`/`CodeExecution`/`AnthropicMCP` 表明工具托管在向 provider 侧迁移，与 MCP 的「协议分发」形成**双轨并存**（服务端托管 vs 外部工具总线），MCP 思考条目可据此补充对照。
- **Agent 对话日志架构化**：内容寻址日志（仿 Git）把「每条请求携带全量历史」的日志膨胀作为一等工程问题解决，是可复现的记账方案。
- **跨平台窗口偏薄**：两周内 KMP/Flutter 侧以 hotfix（Flutter 3.44.9）与营销内容为主，KotlinLLM 是 Kotlin/JVM 研究而非 KMP 域，未出现可收录级动态——建议下轮把 Compose Multiplatform 1.11.0、Kotlin 2.3.20 工具链作为定向搜索目标验证（本次两者仅侧面出现）。

## 4. 收录建议

| 候选 | verdict | lineage | 一句话理由 |
|---|---|---|---|
| Snowflake data-eng-bench | `index` | `agent/eval` | 首个仓库级 dbt agent 基准，harness×model 双变量质量/成本/可靠性归因数据开源，直接填「Agent 评测归因」与 `ECC.md` 缺公开评测数据的空白，建议随收录生成 `expand/06-AI与LLM/Agent研究与评测/` 条目并与 ECC、待处理 Harness-R1/EvolveNet 建立关联 |
| Simon Willison LLM 0.32 | `index` | `agent/platform` | Tier1 作者的工具链可复现实践（推理轨迹分流、内容寻址日志、服务端工具、任意兼容端点），补上下文日志与跨模型可移植性缺口；release notes 形态不值得整体翻译，索引核心实践即可 |

两者均不选 `translate`：data-eng-bench 价值在数据与归因结论（索引 + expand 加工吸收效率更高），LLM 0.32 为发布说明型长文（已有 7 条待处理翻译在队列，且同作者 Raccoon Heist 已在队列）；`observe` 也不适用——两条都有明确的可落地增量。

```json
{
  "analysis": {
    "priority": [
      "data-eng-bench 最高优先：首个仓库级 dbt agent 基准，harness×model 双变量归因 + 成本/可靠性数据，直接补 Agent 评测归因与 ECC 缺公开评测数据的空白",
      "LLM 0.32 次优：Tier1 作者可复现工具链实践（推理轨迹分流、内容寻址日志、服务端工具、任意兼容端点），补上下文日志与跨模型可移植性缺口",
      "跨平台窗口内无达标内容（KotlinLLM 为 Kotlin/JVM 研究、Flutter 3.44.9 为 hotfix），不硬凑；两条候选均为 AI Agent 域"
    ],
    "gaps_covered": [
      "Agent 评测组件级归因：data-eng-bench 的 harness×model 矩阵（Pass@1/Pass^3/每试成本/token/工具调用/步数）",
      "Agent harness 行为正确性与覆盖率：10–50 条隐藏断言整管道计分 + 103 任务仓库级 DAG 验证",
      "上下文/记忆可复现实践（部分）：LLM 0.32 内容寻址消息存储与推理轨迹 stderr 分流",
      "跨模型可移植性（部分）：llm openai endpoint + chat-completions-server 单命令对接任意兼容端点",

exec
/bin/bash -lc "cd /root/note-worker && sed -n '150,240p' references/articles.md" in /root/note-worker
 succeeded in 0ms:

### 14. MCP 官方文档：Model Context Protocol 介绍

- **标题：** MCP 官方文档：Model Context Protocol 介绍
- **链接：** [modelcontextprotocol.io/introduction](https://modelcontextprotocol.io/introduction)
- **作者：** MCP 官方文档（modelcontextprotocol.io） | **日期：** 2026-08-09
- **状态：** 已收录 | **归属：** `expand/thinking/MCP协议标准化的增量与边界.md`
- **核心：** 官方入门与架构——「AI 应用的 USB-C」定位、数据层/传输层双层、2026-07-28 版增量（MCP Apps / Agent Skills / Registry / server/discover）。思考：协议只标准化「连接信封」，工具语义仍靠 server 自治，M×N 适配成本转移而非消失。
- **关联：** MCP / Agent 工具生态；既有笔记 [[MCP协议与工具调用]]、Claude Code [[12-mcp-xie-yi-ji-cheng]]

### 15. Rust 2025 官方博客：Rust 1.85 版本说明（Move 语义 / Borrow Checker 演进）

- **标题：** Rust 2025 官方博客：Rust 1.85 版本说明（Move 语义 / Borrow Checker 演进）
- **链接：** [blog.rust-lang.org/2025/02/20/Rust-1.85.0.html](https://blog.rust-lang.org/2025/02/20/Rust-1.85.0.html)
- **作者：** The Rust Release Team（blog.rust-lang.org） | **日期：** 2025-02-20（采集 2026-08-09）
- **状态：** 已收录 | **归属：** `expand/thinking/Rust2024版次的语义收紧与异步闭合.md`
- **核心：** Rust 1.85.0 同步稳定 2024 Edition（官方口径「史上最大版次」）：RPIT 生命周期捕获规则、临时作用域/drop 顺序、match 擦除保留、unsafe extern/属性/static mut 收缩、set_var 转 unsafe、async closures（AsyncFn）稳定、元组 collect 扩展至 12 元。思考：采集器「Move 语义」标签失焦——真正主线是「版次语义收紧 + unsafe 显式化 + 异步借用补课」，edition 约三年一拍是 Rust 的语义债务清偿机制。
- **关联：** Rust / 版次 / 借用检查；对照 [[c++核心编程]]、思考层 [[MCP协议标准化的增量与边界]]

### 16. Meta launches Muse Code for complex software work with persistent AI agents

- **标题：** Meta launches Muse Code for complex software work with persistent AI agents
- **链接：** [www.infoworld.com/article/4206084/meta-launches-muse-code-for-complex-software-work-with-persistent-ai-agents.html](https://www.infoworld.com/article/4206084/meta-launches-muse-code-for-complex-software-work-with-persistent-ai-agents.html)
- **作者：** research | **日期：** 2026-08-09
- **状态：** 已收录 | **归属：** `working/Meta-launches-Muse-Code-for-complex-soft-translation.md`
- **核心：** Meta launches Muse Code for complex software work with persistent AI agents

### 17. Claude Code v2.1.224 — self-hosted environments

- **标题：** Claude Code v2.1.224 — self-hosted environments
- **链接：** [github.com/anthropics/claude-code/releases/tag/v2.1.224](https://github.com/anthropics/claude-code/releases/tag/v2.1.224)
- **作者：** research | **日期：** 2026-08-09
- **状态：** 已收录 | **归属：** `working/Claude-Code-v2-1-224-self-hosted-environ-translation.md`
- **核心：** Claude Code v2.1.224 — self-hosted environments

### 18. EvolveNet: Collaborative Harness Evolution for Agent Self-Improvement

- **标题：** EvolveNet: Collaborative Harness Evolution for Agent Self-Improvement
- **链接：** [arxiv.org/abs/2608.04968](https://arxiv.org/abs/2608.04968)
- **作者：** research | **日期：** 2026-08-09
- **状态：** 已收录 | **归属：** `working/EvolveNet-Collaborative-Harness-Evolutio-translation.md`
- **核心：** EvolveNet: Collaborative Harness Evolution for Agent Self-Improvement

### 19. Harness-R1: Learning to Edit Executable Runtime Harnesses from Agent Failure Trajectories

- **标题：** Harness-R1: Learning to Edit Executable Runtime Harnesses from Agent Failure Trajectories
- **链接：** [arxiv.org/abs/2608.02276](https://arxiv.org/abs/2608.02276)
- **作者：** research | **日期：** 2026-08-09
- **状态：** 已收录 | **归属：** `working/Harness-R1-Learning-to-Edit-Executable-R-translation.md`
- **核心：** Harness-R1: Learning to Edit Executable Runtime Harnesses from Agent Failure Tra…

### 20. I Gave Claude Code an AGENTS.md Contract and Stopped Babysitting It

- **标题：** I Gave Claude Code an AGENTS.md Contract and Stopped Babysitting It
- **链接：** [dev.to/daymondhyper/i-gave-claude-code-an-agentsmd-contract-and-stopped-babysitting-it-53m](https://dev.to/daymondhyper/i-gave-claude-code-an-agentsmd-contract-and-stopped-babysitting-it-53m)
- **作者：** research | **日期：** 2026-08-09
- **状态：** 已收录 | **归属：** `working/I-Gave-Claude-Code-an-AGENTS-md-Contract-translation.md`
- **核心：** I Gave Claude Code an AGENTS.md Contract and Stopped Babysitting It

### 21. The Shape of Things to Come, Part 1: The Continuous Thunderdome

- **标题：** The Shape of Things to Come, Part 1: The Continuous Thunderdome
- **链接：** [yegge.ai/essays/the-shape-of-things-to-come/](https://yegge.ai/essays/the-shape-of-things-to-come/)
- **作者：** research | **日期：** 2026-08-09
- **状态：** 已收录 | **归属：** `working/The-Shape-of-Things-to-Come-Part-1-The-C-translation.md`
- **核心：** The Shape of Things to Come, Part 1: The Continuous Thunderdome

## 观察项

> 暂不收录、持续观察的 URL（防重复采集，不计入编号正文主计数）。由 research Prompt B（`observe`）写入。

| 标题 | 链接 | 来源 | 日期 | 备注 |
| --- | --- | --- | --- | --- |
| Klibs.io Grows to 4200+ KMP Projects With Smarter Discovery and New AI Integrations | https://blog.jetbrains.com/kotlin/2026/08/klibsio-grows-to-4200-kmp-projects-with-smarter-discovery-and-new-ai-integrations/ | JetBrains Kotlin 博客 | 2026-08-17 | JetBrains 官方把 KMP 生态目录做成 agent 可调用工具，含评测数据与 AGENTS.md 实践，双领域交集标杆。 |
| What's new in Kotlin 2.4.20-RC | https://kotlinlang.org/docs/whatsnew-eap.html | Kotlin 官方文档 | 2026-08-12 | 官方 EAP 公告，覆盖标准库、K/N、K/Wasm、K/JS 多层实质变更，KMP 工具链风向标。 |
| What's new in Flutter 3.47 | https://flutter.dev/blog/whats-new-in-flutter-3-47 | Flutter 官方博客 | 2026-08-12 | 官方发布说明中设计系统解耦是长期架构调整信号，影响依赖管理与跨端构建策略。 |
| Conceptual integrity and counting lines of code | https://simonwillison.net/2026/Aug/19/conceptual-integrity-and-counting-lines-of-code/ | Simon Willison 博客 | 2026-08-19 | Tier 1 作者原创观点，挑战主流 LOC 无意义论，对 agent 工程管理/评测有启发。 |
| Introducing LangSmith Tuned Evaluators, starting with Perceived Error | https://www.langchain.com/blog/introducing-langsmith-tuned-evaluators-starting-with-perceived-error | LangChain 官方博客 | 2026-08-18 | 官方评测产品但技术实质充分（后训练法官+82% 成本数据+接入流程），对 agent 评测域有参考价值。 |
| Agentic Transaction: Towards ACID-Compliant Agent Systems | https://arxiv.org/abs/2608.13900 | arXiv cs.DB/cs.AI | 2026-08-14 | 原创理论框架+可运行系统，是 agent 可靠执行方向少见的系统性工作。 |
| The Devil Is in the Interface: Evaluating How Tool Architecture Shapes Coding Agent Behavior | https://arxiv.org/abs/2608.11386 | arXiv cs.SE | 2026-08-11 | 大样本受控实验+量化结论，为 harness/工具平台设计提供可复现证据。 |
| DeepSeek Harness 开发者预览：一切皆插件 | https://news.ycombinator.com/item?id=49285244 | DeepSeek 官方（Hacker News） | 2026-08-13 | 开源 agent harness 标杆事件，插件化架构与可追踪事件流直接回应 harness/编排主题，官方一级内容。 |
| Exploring Compose HTML for Server-Side Rendering | https://blog.jetbrains.com/kotlin/2026/08/exploring-compose-html-for-server-side-rendering/ | JetBrains | 2026-08-14 | 官方博客对 CMP 服务端渲染方向的原创前瞻，含可复现代码 |
| LiveMem: Maintaining Memory State Continuity in Long-Running LLM Inference | https://arxiv.org/abs/2608.02515 | arXiv cs.CL | 2026-08-03 | 为 agent 长会话记忆与上下文管理提供新抽象视角 |
| Everything we launched during Agents Week | https://blog.cloudflare.com/agents-week-review-august-2026/ | Cloudflare | 2026-08-10 | 云厂商对 agent 运行时与生命周期的一次系统性落子，平台趋势观察 |
| Announcing Dart 3.13 | https://dart.dev/blog/announcing-dart-3-13 | Dart / Google | 2026-08-12 | 官方稳定版发布，语言/工具链/编译优化多维实质更新 |
| IntelliJ IDEA Goes LSP: Java and Kotlin Intelligence Comes to VS Code, Cursor, and Agentic Flows | https://blog.jetbrains.com/idea/2026/08/intellij-idea-goes-lsp/ | JetBrains | 2026-08-04 | Kotlin 工具链×agent 工作流交叉的一手官方进展 |
| Deep Agents vs LangChain vs LangGraph | https://www.langchain.com/blog/deep-agents-vs-langchain-vs-langgraph | LangChain | 2026-08-06 | 官方对 agent 栈分层与 harness 定义的权威界定，指导选型 |
| SHE: Trajectory-driven Safety Harness Evolution for LLM Agents | https://arxiv.org/abs/2608.09885 | arXiv cs.AI | 2026-08-10 | 首个可演化安全 harness 系统化框架，有数据与复现链接 |
| SWE-Touch: Benchmarking Coding Agents When Users Touch the Code | https://arxiv.org/abs/2608.02499 | arXiv cs.SE | 2026-08-03 | 填补人机协作共享工作区评测盲区，有数据与开源实现，挑战单干基准范式 |
| DeepSeek Harness developer preview: Everything is a plugin | https://deepseek.com/harness/en/ | DeepSeek | 2026-08-14 | 开源 harness 平台级发布，Claude Code 直接竞品，HN 732 分高热 |
| Auto mode is now the default in Claude Code for Pro, Max, and Team plans | https://claude.com/blog/auto-mode-default-in-claude-code | Anthropic | 2026-08-07 | Tier 1 官方一手安全数据，直接塑造 agent 权限与安全架构设计 |

exec
/bin/bash -lc "cd /root/note-worker && ls scripts && echo ==== && sed -n '1,80p' scripts/research.py 2>/dev/null" in /root/note-worker
 succeeded in 0ms:
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
====
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

exec
/bin/bash -lc "cd /root/note-worker && sed -n '80,240p' scripts/research.py" in /root/note-worker
 succeeded in 0ms:
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
        except json.JSONDecodeError:
            continue
    dec = json.JSONDecoder()
    for m in re.finditer(r"\{", text):
        try:
            obj, _ = dec.raw_decode(text, m.start())
            if isinstance(obj, dict):
                return obj
        except json.JSONDecodeError:
            continue
    return {}


def apply_triage(candidates):
    """按 verdict 写入 articles.md。返回 (translate_n, index_n, observe_n)。"""
    art = ROOT / "references" / "articles.md"
    if not art.exists():
        print("[research] articles.md 不存在")
        return 0, 0, 0
    known = collect.existing_urls()
    t = art.read_text(encoding="utf-8")
    tn = ix = ob = 0
    today = datetime.date.today().isoformat()
    for c in candidates:
        url = (c.get("url") or "").strip()
        title = (c.get("title") or "").strip()
        if not url or not title:
            continue
        verdict = (c.get("verdict") or "observe").strip().lower()
        if verdict not in ("index", "translate", "observe"):
            verdict = "observe"
        lineage = (c.get("lineage") or "general").strip()
        reason = (c.get("reason") or "").strip()
        row = {
            "title": title,
            "url": url,
            "source": c.get("source") or "research",
            "date": c.get("date") or today,
        }
        if url in known and verdict != "translate":
            # 已在索引：跳过 index/observe；translate 仍可能已在队列
            print(f"[research] 去重跳过（{verdict}）：{title[:50]}")
            continue
        if verdict == "translate":
            if url in known:
                print(f"[research] 去重跳过（translate）：{title[:50]}")
                continue
            msg = collect.save_item("research", {**row, "title": title, "url": url})
            print(f"[research] translate → {msg}")
            if msg and msg.startswith("入队"):
                known.add(url)
                tn += 1
                t = art.read_text(encoding="utf-8")  # save_item 已写盘
            continue
        if url in known:
            print(f"[research] 去重跳过（{verdict}）：{title[:50]}")
            continue
        if verdict == "index":
            n = next_article_number(t)
            entry = fmt_article_entry(
                n, row, "已收录", moved_file=None,
                core=reason or title[:80], lineage=lineage,
            )
            t = append_numbered_entries(t, [entry])
            art.write_text(t, encoding="utf-8")
            known.add(url)
            ix += 1
            print(f"[research] index → #{n:02d} {title[:40]} ({lineage})")
            continue
        # observe
        t = append_observe_row(t, row, reason)
        art.write_text(t, encoding="utf-8")
        known.add(url)
        ob += 1
        print(f"[research] observe → {title[:40]}")
    return tn, ix, ob


def push_queue_branch():
    """把 articles（及 research 落盘）推到 pipeline/queue，不开 PR。"""
    sh("git add references/articles.md candidates 2>/dev/null || git add references/articles.md",
       check=False)
    changed = sh("git status --porcelain", check=False).stdout.strip()
    if not changed:
        print("[research] 无变更，跳过 push")
        return 0
    sh("git config user.name note-worker || true", check=False)
    sh("git config user.email note-worker@users.noreply.github.com || true", check=False)
    # 在当前 HEAD 上提交，再推送到 pipeline/queue
    r = sh('git commit -m "research: 情报搜索分流入队（无 PR）"', check=False)
    if r.returncode != 0 and "nothing to commit" not in (r.stdout + r.stderr):
        # 可能已在别处提交；继续尝试 push
        pass
    r = sh("git push --force-with-lease origin HEAD:pipeline/queue", check=False)
    if r.returncode != 0:
        print(f"[research] push pipeline/queue 失败：{r.stderr[-400:]}")
        return 1
    print("[research] 已推送 origin/pipeline/queue（不开 PR）")
    return 0


codex
查看 `working/` 现有译文形态与知识图谱，校准 translate/index 判定口径。
exec
/bin/bash -lc 'cd /root/note-worker && ls working/ && echo ==== && wc -l working/*.md 2>/dev/null | tail -20 && echo ====head==== && head -40 working/Harness-R1-Learning-to-Edit-Executable-R-translation.md 2>/dev/null' in /root/note-worker
 succeeded in 0ms:
AGENTS.md
Claude-Code-v2-1-224-self-hosted-environ-translation.md
EvolveNet-Collaborative-Harness-Evolutio-translation.md
Harness-R1-Learning-to-Edit-Executable-R-translation.md
I-Gave-Claude-Code-an-AGENTS-md-Contract-translation.md
Meta-launches-Muse-Code-for-complex-soft-translation.md
The-Shape-of-Things-to-Come-Part-1-The-C-translation.md
====
    25 working/AGENTS.md
    58 working/Claude-Code-v2-1-224-self-hosted-environ-translation.md
   456 working/EvolveNet-Collaborative-Harness-Evolutio-translation.md
   218 working/Harness-R1-Learning-to-Edit-Executable-R-translation.md
   121 working/I-Gave-Claude-Code-an-AGENTS-md-Contract-translation.md
    60 working/Meta-launches-Muse-Code-for-complex-soft-translation.md
   303 working/The-Shape-of-Things-to-Come-Part-1-The-C-translation.md
  1241 total
====head====
---
created: 2026-08-17
updated: 2026-08-17
title: Harness-R1：从智能体失败轨迹学习编辑可执行运行时 Harness
sourceUrl: https://arxiv.org/abs/2608.02276
sourceAuthor: Shuai Shao 等（上海交通大学 / 小红书 / 东南大学）
translatedAt: 2026-08-17
sources: [references/articles.md 待处理队列]
tags: [AI Agent, Harness 工程, 智能体运行时, RL, GRPO, 自进化智能体, type/翻译]
---

# Harness-R1：从智能体失败轨迹学习编辑可执行运行时 Harness

> arXiv:2608.02276（cs.AI，2026-08-03 提交）| 代码：[github.com/DeepExperience/Harness-R1](https://github.com/DeepExperience/Harness-R1) | 模型：[huggingface.co/ShaoShuai0605/Harness-R1](https://huggingface.co/ShaoShuai0605/Harness-R1)
> 作者：Shuai Shao、Kangning Zhang、Qingyao Li、Shijian Wang、Hao Wang、Wenxiang Jiao、Yuan Lu、Yi Guo、Weiwen Liu、Weinan Zhang

## 摘要

围绕大语言模型构建的智能体在部署过程中会不断积累交互轨迹，但其行为通常保持不变。除了更新模型权重之外，这些轨迹还可以改进智能体的 harness——即构造上下文、中介工具、校验动作并恢复执行的那一层。我们提出 Harness-R1，据我们所知，这是第一种把「基于失败、贯穿生命周期地编辑现有可执行运行时」变成可学习能力的方法。它用在线强化学习后训练一个专门的 harness 工程师，使其编辑以实际达成的任务成功为目标进行优化，而不是由固定编辑器提出。一个独立的 9B 工程师把一批批目标智能体的失败转换成经过验证的可执行补丁；对冻结目标做新鲜的同一批次重跑，为补丁提供结果奖励，因此训练只更新工程师。冷启动监督微调初始化该编辑策略，随后用群组相对策略优化（GRPO）在线训练。在 WebShop、ALFWorld 与 DBBench 上，Harness-R1 把 vanilla Qwen3.5-9B 的成功率从 44.3% 提升到 53.6%（+9.3 个百分点）。在对目标智能体直接微调之后，针对该目标训练的工程师再把平均值从 59.2% 进一步提到 64.2%（+5.0 个百分点）；由于这些提升在目标微调前后都成立，Harness-R1 指向了 harness 工程师与目标智能体的共同进化。

## 1 引言

大语言模型是工具型智能体的决策核心，使智能体能够理解任务、维护状态，并通过与外部环境的多轮交互追求复杂目标（[40](https://arxiv.org/abs/2608.02276)；[16](https://arxiv.org/abs/2608.02276)；[13](https://arxiv.org/abs/2608.02276)；[46](https://arxiv.org/abs/2608.02276)）。与单次模型调用不同，部署中的智能体会持续产生包含观察、动作、环境反馈与任务结果的轨迹。这些轨迹记录了成功经验，但也暴露了系统性失败，例如工具误用、状态丢失、协议违例、反复尝试与恢复失败。这引出一个自然的问题：智能体能否利用自身的交互经验持续改进，而不是部署后保持不变？这种「经验到改进」的闭环正是自进化智能体（self-evolving agents）的核心议题（[7](https://arxiv.org/abs/2608.02276)；[35](https://arxiv.org/abs/2608.02276)；[42](https://arxiv.org/abs/2608.02276)）。

智能体系统可以在两个互补的位置上改进。一条路线通过监督微调、强化学习或在线学习更新模型参数，直接改进做出任务决策的actor（[36](https://arxiv.org/abs/2608.02276)；[20](https://arxiv.org/abs/2608.02276)；[30](https://arxiv.org/abs/2608.02276)）。另一条路线保持模型固定，优化它周围的智能体 harness。上下文构造、记忆与技能、工具中介、动作校验，以及控制与恢复逻辑，都是 harness 的组成部分（[31](https://arxiv.org/abs/2608.02276)；[48](https://arxiv.org/abs/2608.02276)；[10](https://arxiv.org/abs/2608.02276)）。它们共同决定了模型看到什么、能执行哪些动作、如何解读环境反馈，以及执行偏离后如何恢复。因此，相同的模型权重在不同 harness 下可以产生截然不同的智能体能力。Harness 优化提供了一条与模型训练互补的路径：它改进模型与环境之间的运行时机制，而不改变模型本身。

直接修改 harness 并不总是可靠的。图 1 比较了三个基准上「匹配基线」的平均环境奖励变化。固定的 Self-Refine 规则（[22](https://arxiv.org/abs/2608.02276)）在三个基准上都降低了奖励；前沿模型作为 harness 编辑器的收益则不稳定或有限，有些甚至降低了 WebShop 的奖励。因此，提示强大但固定的模型去编辑 harness 还不够可靠。

**图 1：** 三个基准上匹配基线的奖励变化；菱形表示等权平均。

除了这类提示式编辑，近期系统构建了专门的 harness 优化流水线。Meta-Harness、Agentic Harness Engineering 与 AutoHarness 使用智能体式 proposer，基于 harness 状态、执行轨迹与任务反馈联合编辑提示词、工具、记忆、中间件或控制逻辑；Life-Harness 与 HarnessX 把可编辑面扩展到生命周期干预与类型化组件（[12](https://arxiv.org/abs/2608.02276)；[17](https://arxiv.org/abs/2608.02276)；[19](https://arxiv.org/abs/2608.02276)；[37](https://arxiv.org/abs/2608.02276)；[3](https://arxiv.org/abs/2608.02276)）。然而，harness proposer 通常保持固定：结果只用于选择或迭代精修补丁，不会直接更新 proposer 参数；HarnessX 用跨 harness 的 GRPO 训练任务模型，而 AEGIS 保留符号化的 harness 编辑。互补的工作优化提示词、示例、记忆、技能或任务求解程序（[38](https://arxiv.org/abs/2608.02276)；[11](https://arxiv.org/abs/2608.02276)；[31](https://arxiv.org/abs/2608.02276)；[48](https://arxiv.org/abs/2608.02276)；[36](https://arxiv.org/abs/2608.02276)；[20](https://arxiv.org/abs/2608.02276)；[30](https://arxiv.org/abs/2608.02276)），但通常只隔离单个工件，或构造新的求解程序。工作流可以是 harness 的一部分，但生成一个工作流，与学会把「失败条件化的可执行干预」安装进现有多阶段运行时，是两回事：后者必须从真实的目标智能体失败中决定何时干预，并协调上下文、状态、动作执行与恢复。这留下一个研究较少的问题：**我们能否用在线强化学习后训练一个专门的 harness 工程师，使「根据观察到的失败改进现有可执行运行时」变成一种可学习能力？**

直接训练 harness 工程师面临两个挑战。第一，可编辑运行时横跨相互依赖的执行阶段，不受限制的代码编辑可能破坏既有接口、产生不可执行的行为，或引入与任务成功无关的改动。第二，文本形式与静态规则无法判定补丁质量——只有补丁应用后目标智能体的行为才能判定。因此，训练需要一条有根据的反馈路径：从目标智能体的失败，经过受约束的可执行编辑，到更新工程师的性能增益。

我们提出 Harness-R1——一种训练范式：在保持目标智能体冻结的同时，用在线强化学习后训练一个专门的 harness 工程师。以批量的目标智能体失败为条件，工程师生成经过验证的可执行运行时补丁；打过补丁的目标重跑相同任务，实现的性能变化只奖励工程师。冷启动监督微调先初始化策略，再做在线 GRPO。跨 WebShop、ALFWorld 与 DBBench，Harness-R1 把 vanilla 目标的平均成功率从 44.3% 提到 53.6%（+9.3 个百分点），在直接目标微调后从 59.2% 提到 64.2%（+5.0 个百分点）。

主要贡献可总结如下：

- 我们把「失败条件化的、贯穿生命周期的 harness 编辑」形式化为一个专门工程师的在线强化学习问题，同时保持目标智能体冻结。
- 我们开发了 Harness-R1，把冷启动监督微调与「基于可执行运行时补丁实现效用」的群组相对策略优化结合起来，在三个交互基准上把 vanilla 目标提升了 9.3 个百分点。

exec
/bin/bash -lc 'cd /root/note-worker && git log --oneline -8 && git branch -a | head && echo ==== && tail -30 references/articles.md' in /root/note-worker
 succeeded in 0ms:
5a08796 lint: 2026-09-06 巡检报告
f22328f lint: 2026-09-05 巡检报告
c5de68b weekly: 2026-09-04 知识库周报
0ed4e29 lint: 2026-09-04 巡检报告
4e9f4d0 lint: 2026-09-03 巡检报告
89da562 lint: 2026-09-02 巡检报告
951a591 lint: 2026-09-01 巡检报告
a0ad99b docs: complete Kotlin syntax and concurrency notes
  candidates/20260809-180901
* main
  research/20260809-180639
  review/20260810-114504
  review/20260810-115607
  review/20260817-062607
  review/20260824-062700
  review/20260831-081723
  remotes/origin/HEAD -> origin/main
  remotes/origin/ai-ingest/20260804
====
| 标题 | 链接 | 来源 | 日期 | 备注 |
| --- | --- | --- | --- | --- |
| Klibs.io Grows to 4200+ KMP Projects With Smarter Discovery and New AI Integrations | https://blog.jetbrains.com/kotlin/2026/08/klibsio-grows-to-4200-kmp-projects-with-smarter-discovery-and-new-ai-integrations/ | JetBrains Kotlin 博客 | 2026-08-17 | JetBrains 官方把 KMP 生态目录做成 agent 可调用工具，含评测数据与 AGENTS.md 实践，双领域交集标杆。 |
| What's new in Kotlin 2.4.20-RC | https://kotlinlang.org/docs/whatsnew-eap.html | Kotlin 官方文档 | 2026-08-12 | 官方 EAP 公告，覆盖标准库、K/N、K/Wasm、K/JS 多层实质变更，KMP 工具链风向标。 |
| What's new in Flutter 3.47 | https://flutter.dev/blog/whats-new-in-flutter-3-47 | Flutter 官方博客 | 2026-08-12 | 官方发布说明中设计系统解耦是长期架构调整信号，影响依赖管理与跨端构建策略。 |
| Conceptual integrity and counting lines of code | https://simonwillison.net/2026/Aug/19/conceptual-integrity-and-counting-lines-of-code/ | Simon Willison 博客 | 2026-08-19 | Tier 1 作者原创观点，挑战主流 LOC 无意义论，对 agent 工程管理/评测有启发。 |
| Introducing LangSmith Tuned Evaluators, starting with Perceived Error | https://www.langchain.com/blog/introducing-langsmith-tuned-evaluators-starting-with-perceived-error | LangChain 官方博客 | 2026-08-18 | 官方评测产品但技术实质充分（后训练法官+82% 成本数据+接入流程），对 agent 评测域有参考价值。 |
| Agentic Transaction: Towards ACID-Compliant Agent Systems | https://arxiv.org/abs/2608.13900 | arXiv cs.DB/cs.AI | 2026-08-14 | 原创理论框架+可运行系统，是 agent 可靠执行方向少见的系统性工作。 |
| The Devil Is in the Interface: Evaluating How Tool Architecture Shapes Coding Agent Behavior | https://arxiv.org/abs/2608.11386 | arXiv cs.SE | 2026-08-11 | 大样本受控实验+量化结论，为 harness/工具平台设计提供可复现证据。 |
| DeepSeek Harness 开发者预览：一切皆插件 | https://news.ycombinator.com/item?id=49285244 | DeepSeek 官方（Hacker News） | 2026-08-13 | 开源 agent harness 标杆事件，插件化架构与可追踪事件流直接回应 harness/编排主题，官方一级内容。 |
| Exploring Compose HTML for Server-Side Rendering | https://blog.jetbrains.com/kotlin/2026/08/exploring-compose-html-for-server-side-rendering/ | JetBrains | 2026-08-14 | 官方博客对 CMP 服务端渲染方向的原创前瞻，含可复现代码 |
| LiveMem: Maintaining Memory State Continuity in Long-Running LLM Inference | https://arxiv.org/abs/2608.02515 | arXiv cs.CL | 2026-08-03 | 为 agent 长会话记忆与上下文管理提供新抽象视角 |
| Everything we launched during Agents Week | https://blog.cloudflare.com/agents-week-review-august-2026/ | Cloudflare | 2026-08-10 | 云厂商对 agent 运行时与生命周期的一次系统性落子，平台趋势观察 |
| Announcing Dart 3.13 | https://dart.dev/blog/announcing-dart-3-13 | Dart / Google | 2026-08-12 | 官方稳定版发布，语言/工具链/编译优化多维实质更新 |
| IntelliJ IDEA Goes LSP: Java and Kotlin Intelligence Comes to VS Code, Cursor, and Agentic Flows | https://blog.jetbrains.com/idea/2026/08/intellij-idea-goes-lsp/ | JetBrains | 2026-08-04 | Kotlin 工具链×agent 工作流交叉的一手官方进展 |
| Deep Agents vs LangChain vs LangGraph | https://www.langchain.com/blog/deep-agents-vs-langchain-vs-langgraph | LangChain | 2026-08-06 | 官方对 agent 栈分层与 harness 定义的权威界定，指导选型 |
| SHE: Trajectory-driven Safety Harness Evolution for LLM Agents | https://arxiv.org/abs/2608.09885 | arXiv cs.AI | 2026-08-10 | 首个可演化安全 harness 系统化框架，有数据与复现链接 |
| SWE-Touch: Benchmarking Coding Agents When Users Touch the Code | https://arxiv.org/abs/2608.02499 | arXiv cs.SE | 2026-08-03 | 填补人机协作共享工作区评测盲区，有数据与开源实现，挑战单干基准范式 |
| DeepSeek Harness developer preview: Everything is a plugin | https://deepseek.com/harness/en/ | DeepSeek | 2026-08-14 | 开源 harness 平台级发布，Claude Code 直接竞品，HN 732 分高热 |
| Auto mode is now the default in Claude Code for Pro, Max, and Team plans | https://claude.com/blog/auto-mode-default-in-claude-code | Anthropic | 2026-08-07 | Tier 1 官方一手安全数据，直接塑造 agent 权限与安全架构设计 |
| New release of LLM adds support for reasoning traces, OpenAI Responses, server-side tools, and smarter logging | https://simonwillison.net/2026/Aug/4/new-release-of-llm/ | Simon Willison (simonwillison.net) | 2026-08-04 | Tier1作者对LLM工具平台的深度工程复盘，含可复现代码，覆盖推理轨迹、服务端工具与日志架构。 |
| Introducing Data-eng-bench: Why You Need "Data-Native" Harnesses for Data Engineering | https://www.snowflake.com/en/blog/engineering/data-eng-bench-data-engineering-agent-benchmark/ | Snowflake AI Research (Snowflake Engineering Blog) | 2026-08-06 | 首个仓库级dbt agent评测（103任务）并开源，harness×模型双变量质量/成本数据直接服务agent评测与选型。 |

## 统计

- **正式收录：** 12 篇（编号 01-10、14、15）｜**已淘汰隔离：** 3 篇（编号 11-13，不计入收录数，仅防重复采集）

## 待补充

- [ ] 占位：外部新文章先查编号 01-15 确认未收，再由采集层写入「待处理」队列

exec
/bin/bash -lc "cd /root/note-worker && sed -n '1,60p' expand/06-AI与LLM/Agent工具与平台/ECC.md && echo ====KG==== && head -40 expand/知识图谱.md" in /root/note-worker
 succeeded in 0ms:
---
created: 2026-08-04
updated: 2026-08-04
sources: [raw/github-2026-08-03-08c2bad9.md]
tags: [AI, Agent, 编程代理, 工具系统, type/工具, status/待验证, 启发]
---

# ECC

给编程代理装一套"操作系统"：技能、本能、记忆、安全一应俱全，Claude Code / Codex / Cursor 都能插上。

## 检索问题（Q&A）
- 编程代理除了模型还缺什么基础设施？→ 本条目：ECC 的技能 / 本能 / 记忆 / 安全分层
- Agent 工程化参考实现？→ ECC 的 npm 包 + GitHub App 架构

## 结构化提炼

### 核心论点
ECC 把编程代理的工程化需求（技能管理、持久记忆、安全防护、多运行时）沉淀为可插拔的"代理工具操作系统"，跨 Claude Code / Codex / Cursor 等前端使用。

### 逻辑骨架
- 问题：编程代理各自为战，缺少可复用的能力层
- 方案：Agent Harness 分层——技能（skills）、本能（instincts）、记忆（memory）、安全（AgentShield）
- 形态：npm 包（ecc-universal / ecc-agentshield）+ GitHub App + Pro 订阅（私有仓库协作）
- 运行时：Shell / TypeScript / Python / Go / Java / Perl / Markdown

### 关键概念（费曼式）
- Agent Harness：把"代理怎么干活"的公共部分（工具、记忆、权限）抽出来，像操作系统管硬件一样管能力
- 本能（instincts）：预设的行为倾向 / 检查点，让代理不用每次重新想"该不该这么干"

## 深度追问

### 苏格拉底式质疑
1. "跨前端"是否只是薄封装？各家 agent 的钩子能力差异如何抹平？
2. 安全层（AgentShield）的防护边界在哪——能否拦截恶意 prompt 注入？
3. 个人项目 + GitHub App 的权限模型，是否与"最小权限"原则冲突？

### 背景与盲区
- 背景：编程代理（Claude Code / Codex）已成为 Agent 主战场，能力层正在工具化
- 盲区：缺少公开评测数据；社区规模小，长期维护风险

### 溯源与验证
- 官方渠道明确（GitHub / npm / GitHub App），"仅限官方来源"安全提醒；MIT 许可证

## 联想与缝合

### 跨学科类比
像"给新手程序员配 IDE 插件全家桶"：模型是编译器，ECC 是帮你管工程习惯、快捷键、防呆提醒的那层工具。

### 与知识库联系
- 与 [[22-skills-ji-neng-kai-fa]] / [[21-zi-ding-yi-agents]]：正是 Claude Code 源码解读中"Skills 技能系统"与"自定义 Agents"的第三方实现印证
- 与 [[Hermes-Agent]]：同为"代理能力层"，一个偏编程代理、一个偏通用助手

### 底层模型
- 分层架构（内核 / 驱动 / 应用）
- 能力复用：把最佳实践工具化沉淀

## 场景化转译

### 行动清单
====KG====
---
created: 2026-08-03
updated: 2026-08-09
tags: [知识库, 知识图谱]
---

# 知识图谱

> 本文件是知识库的关系中枢：展示各主题簇内部结构，以及跨主题的关键桥梁。
> 每个笔记末尾的 `## 相关条目` 提供双向链接，在 Obsidian 图谱视图中可直接浏览。

## 主题簇一：编程语言基础（C++ / Python）

- [[c++核心编程]] ↔ [[C++模板和STL]]
- Python：[[python]] ↔ [[数据分析学习笔记]] ↔ [[编程语言/python/集合]]
- 桥 → 算法：[[C++模板和STL]] ↔ [[红黑树]]（STL map/set 底层）
- 桥 → Java：[[c++核心编程]] ↔ [[面向对象]]（OOP 概念对照）
- Rust 思考节点（2026-08-09）：[[Rust2024版次的语义收紧与异步闭合]] ↔ [[c++核心编程]]（C++ 手动内存管理 ↔ Rust 借用 / unsafe 边界对照）；思考层互链 ↔ [[MCP协议标准化的增量与边界]]（版次 / 规范演进治理：edition + cargo fix vs Registry + SEP）

## 主题簇一·Kotlin：基础语法与并发

- 复习入口：[[Kotlin基础语法梳理]] ↔ 67 篇 Kotlin Clippings（控制流、集合、空安全、类和对象、函数式编程、委托、Gradle）
- 并发主线：[[Kotlin基础语法梳理]] ↔ [[Kotlin多线程与协程]]（语言骨架 → JVM 线程 / 协程工程实践）
- 协程关联：[[Kotlin多线程与协程]] ↔ [[java高级技术]] / [[Stream]]（线程池、共享状态与异步组合的 Java/Kotlin 对照）
- Kotlin 线程边界：Kotlin/JVM 可使用 Java 线程 API；KMP 共享代码优先使用 `kotlinx.coroutines`，平台调度器留在实际平台实现。

## 主题簇二：数据结构与算法

- 树：[[红黑树]] ↔ [[平衡二叉树旋转机制]] ↔ [[排序]]
- 搜索：[[BFS经典题目]] ↔ [[DP动态规划]] ↔ [[贪心算法]] ↔ [[图结构的应用]]
- 图论：[[图结构的应用]] ↔ [[Dijkstra最短路算法]]（图的遍历与最短路）
- 桥 → 逆向：[[BFS经典题目]] ↔ [[题目总结]]（CTF 迷宫问题复用 BFS 脚本）
- 桥 → 算法：[[红黑树]] ↔ [[后端/java/集合]]（HashMap 底层）

## 主题簇三：后端开发

- Java 基础：[[面向对象]] ↔ [[后端/java/集合]] ↔ [[Stream]] ↔ [[java高级技术]]
- Web：[[javaweb]] ↔ [[案例]] ↔ [[苍穹]] ↔ [[VUE]]
- 持久层：[[Mybatis-plus]] ↔ [[案例]] ↔ [[Mysql]]
- 消息队列：[[mq]] ↔ [[rocketmq]] ↔ [[redis]]

codex
我已核对知识库现状（`references/articles.md` 编号至 21、观察项 21 条、`expand/06-AI与LLM/` 9 条、`expand/thinking/` 2 条、待处理队列 4 条）与 `research.py` 的三档分流逻辑。以下为对 Prompt A 输出的 10 条候选的完整分析。

## 1. 优先级排序

| 优先级 | 候选 | 星级 | 对已收录/已跟踪内容的补充价值 | 对既有洞见/假设的验证与挑战 | 回答的缺口 |
|---|---|---|---|---|---|
| 1 | **[3] CPE 上下文提权攻击** | ⭐5 | 首次把「上下文组装」当成独立攻击面审计 12 个真实 harness（含 Claude Code、Codex——我们自己的工具类）；与 SHE（安全 harness 演化）、auto-mode 安全数据、LiveMem 形成「记忆/上下文 × 安全」完整闭环 | **挑战**「模型层防御够用」的默认假设；反向印证 `MCP协议标准化的增量与边界`（thinking）——协议只标准化连接信封，语义/作用域自治正是攻击面所在 | 直接命中「Agent 安全审计」缺口（最薄弱区），含多智能体信息流（X-CPE 跨作用域持久化） |
| 2 | **[4] FrontierHarness Eval** | ⭐5 | data-eng-bench 之后第二组跨 harness 受控数据（360 试次、9 harness/12 配置），且数据/任务全开源；补 ECC 类通用 harness「缺公开评测数据」的选型空白 | **验证**「harness 层决定成本远大于质量」：通过率仅差 17pp，单次通过成本差 17 倍；**挑战**「缓存命中率高=省钱」的朴素成本观 | 「Agent 评测组件级归因」「中小团队成本锚点（部分）」 |
| 3 | **[2] SWE-Gate** | ⭐5 | 与已跟踪 SWE-Touch（用户改代码）、LangSmith Tuned Evaluators 组成评测第三维：评审者约束 | 量化说明功能测试对 agent 能力系统性高估（34% 违规），把「什么才算完成」从测试拉到真实合入门槛 | 「harness 行为正确性与覆盖率评估（验收侧）」「评测归因（同脚手架×4 模型）」 |
| 4 | **[5] Headlong** | ⭐4 | 现有持久/长会话谱系（Muse、auto-mode、Agentic Transaction、Hermes-Agent）缺一个可运行的极简参考实现——它是 Bash 微 harness 全套 | 其「指数衰减分辨率 compaction」是可复现算法；自曝「agent 弄停自己服务」验证安全缺口 | 「上下文/compaction 可复现实践」「激活策略（always-on 自唤醒）」「安全审计（沙箱边界）」 |
| 5 | **[7] DecodingAI 上下文工程第 4 课** | ⭐4 | 与 [4] 互证（仅换 harness 进 Terminal-Bench 前 5），给的是记忆/技能/LSP/压缩四件套 + 可运行 Python | **挑战**「换大模型/换订阅治标」论；与待处理队列 Claude 5 context rules（模型级）互补成 harness 级实现 | 「上下文/compaction/记忆可复现实践」——本轮最可操作的一份 |
| 6 | **[1] RAMP（提交型 AI 配置）** | ⭐4 | 把 [20] AGENTS.md 个案 + Klibsio 观察（含 AGENTS.md 实践）升级为 441 仓库量化证据，且发布可复用测量工具 | **支持但复杂化** [20]：73.8% 配置「一次提交不再改」提示写配置≠持续治理，需把配置当可治理工件 | 「harness/配置治理的实证」；间接服务评测归因（配置层作为新变量） |
| 7 | **[9] AgentRoom** | ⭐4 | 已跟踪多 agent 素材多为厂商架构论述（Deep Agents vs LangGraph 等），本文给机制级开放协议 + 控制变量实验 | **反直觉**：收益来自「协调」本身而非并行/CRDT——指导何时并发、何时接管 | 「多智能体编排反模式」「多智能体信息流（文件级 claim）」 |
| 8 | **[6] Rachel Laycock 代码评审论** | ⭐3 | 与观察项 Simon Willison LOC 文同类 Tier1 反驳，但升级为有具名对手与 Meta 数据的一线辩论 | 与 [2] 合成闭环：评审约束编码为机器可判门禁（SWE-Gate），而不要逐 PR 仪式化人工评审 | 流程/评测辩论入口（间接） |
| 9 | **[8] 让数据为 Agentic AI 就绪** | ⭐3 | 扩展 MarkItDown、data-eng-bench 的「数据×agent」方向到企业三层数据框架 | 其「语义上下文层」是上下文工程的企业数据镜像 | 不在 10 项清单内，属相邻扩展（数据契约/隔离/JIT 凭证） |
| 10 | **[10] OpenClaw 2.0 掘金长文** | ⭐3 | Headlong 明指 OpenClaw 为同赛道；中文社区原创深度分析含一手版本数据与对 HN/Reddit 的独立解读 | 团队角色/会话可见性/凭据库/Swarm 给出产品级多用户+多 agent 设计细节；「roles≠租户隔离」与升级事故是现成反模式 | 「多智能体编排（Swarm 实验态）」「安全审计（沙箱/凭据/注入 80%+）」的产品侧证据 |

补充说明：候选均在 2026-08-24 ~ 09-07 窗口内、与 KB 现有 URL 无重复；跨平台侧本轮零达标内容，不硬凑，缺口顺延至下一轮（详见第 2/3 节）。

## 2. 缺口分析

**被覆盖的缺口**

| 缺口 | 覆盖程度 | 证据 |
|---|---|---|
| Agent 安全审计（轨迹/信息流/权限边界） | 强 | [3] M-CPE/X-CPE 分类 + 12 harness 实测；[10] 会话三档可见/按会话沙箱/凭据只写/自适注入 >80%；[5] 未沙箱 agent 自行停服事故 |
| 上下文/compaction/记忆可复现实践 | 强 | [5] 指数衰减分辨率 compaction + append-only jsonl 轨迹；[7] 记忆文件 200 行/25KB 上限、`/clear` 单行压缩、`compress_memory_file`、LSP 反馈环 |
| Agent 评测组件级归因 | 强 | [4] 固定模型/任务/运行时下 9 harness×成本/质量矩阵，缓存命中率≠成本；[2] 同脚手架×4 模型分离「模型」变量 |
| Agent 评测验收现实性 | 强 | [2] 功能通过≠评审约束通过（303 实例/34% 差距），建议双门控；[6] 流程侧同向 |
| 多智能体编排反模式与成本 | 中 | [9] 收益来自协调而非并行；[10] Swarm 拆解/子 agent 并行/进度持久化；成本维度仅 [4] 单 agent 数据 |
| 中小团队成本锚点 | 中（受控非现场） | [4] 单次通过成本 $1.05–$18.34；[10] 升级/运维事故类现场经验，缺系统生产成本案例 |
| 激活策略 | 弱 | [5] always-on 自唤醒调度（engaged vs idle 延迟）；[10] 30 天作用域审批——零散数据点，无系统比较 |

**仍未触及的缺口**

- 跨模型可移植性与迁移指南：本轮无直接命中（FrontierHarness 选 Kimi K3 中立模型只为去主场，不是迁移指南；LangChain/Google 检索只出营销/综述，Kai Waehner 的「harness 锁定 vs 模型可换」未入选）。
- KMP/CMP vs Flutter 架构选型、共享逻辑边界、工具链痛点；跨平台 CI/发布/性能基线：连续两轮空窗，建议下一轮把 JetBrains Kotlin/Flutter 官方发布与 CI 案例列为定向域。
- Harness 内部「行为/覆盖率」度量工具：SWE-Gate 测任务验收，FrontierHarness 测通过率与成本，都不是对 harness 自身逻辑（工具编排、恢复路径）的覆盖率评估——仍开放。
- 长时程/持续 agent 的评测方法论：[5] 自陈只能定性测量，无成熟基准；「持续自主性」的量化仍无人解决。
- 多智能体权限隔离的**设计原语**：[3] 给出攻击面，[10] 明示团队角色非租户隔离，但缺可复用的多 agent 信息流隔离架构模式。
- 生产环境（非受控、含模型/网关交互）的成本/质量归因：[4] 自曝局限，Claude Code 的 $18.34 可能含模型/网关因素——正是「环境」变量的归因空白。

## 3. 趋势信号

- **Harness 效应进入可复现评测品类**：data-eng-bench（已跟踪）→ FrontierHarness → DecodingAI 的 Terminal-Bench 论断，三方独立互证「模型相同时 harness 决定成本与排名」。与既有 `ECC.md`「harness 是工程化主战场」一致。
- **竞争主轴从「能力」转向「成本/效率」**：通过率收敛于 50–66.7%，成本却差 17 倍；「便宜地完成」被识别为独立技能；缓存命中率≠成本，步数/token 计价成为新度量。Claude Code 的 5.6× 成本差提示「harness×模型×网关」交互尚未归因干净。
- **评测验收标准向「人的验收现实」迁移**：SWE-Gate（评审约束门禁）与 Laycock（评审左移+按例外）表面对立、实为同构——把评审约束变成机器可判的早期数据，而非逐 PR 仪式。与已跟踪 SWE-Touch「用户会改代码」同一方向。
- **上下文从优化对象升级为信任边界**：CPE 证明「上下文怎么被组装/越权」比「怎么压缩」更决定安全；攻击面从模型层（提示注入）上移到 harness 的 message role 与作用域管理。与 SHE、auto-mode 安全数据一致，是把 context engineering 推向安全子域的里程碑。
- **持久/自唤醒 agent 形成独立形态与运维事故类**：Headlong 的第三种形态（非 reactive/非 cron），加上 OpenClaw 升级（SQLite 破坏性迁移、split-brain、官方建议「用 coding harness 修 agent」的套娃现象）——「agent 长期运行」正产生自己的故障模式，且**评测与成本建模滞后**。
- **单人 CLI → 团队驾驶舱/共享工作区**：OpenClaw 2.0 多用户 Gateway+Swarm、AgentRoom CRDT 并发、Headlong 多用户共享单 agent；CRDT/协同编辑技术流入 harness 层是新机制信号。注意一致性警示：协作控制≠安全边界、价值来自协调而非并发。
- **版本库成为 agent 治理面**：RAMP 把「提交型配置」当作成熟度代理指标，与 Klibsio（KMP 目录含 AGENTS.md 实践）呼应——配置文件的版本化管理正在成为可测量的工程实践。
- **跨平台方向信号缺席（连续第二轮）**：LangChain/Google 检索多为聚合/营销内容，强素材集中在 HN/arXiv/独立工程博客——现有 Tier2/3 信源策略有效，但 KMP/Flutter 域需换定向源，否则该方向持续失联。

## 4. 收录建议

| 候选 | verdict | lineage | 一句话理由 |
|---|---|---|---|
| [3] CPE 上下文提权攻击 | `translate` | `agent/context` | 首个系统化 harness 上下文安全分类学（M-CPE/X-CPE）+ 12 系统实测，直接服务本库最薄弱的安全审计缺口，值得全篇留存做审计清单；arXiv 有 HTML 版可供翻译 |
| [5] Headlong | `translate` | `agent/harness` | 可运行的极简持久 micro-harness 全文：自唤醒循环、轨迹即上下文、指数衰减 compaction、沙箱与自伤事故，命中上下文/记忆可复现实践与 always-on 两个缺口 |
| [7] DecodingAI 上下文工程第 4 课 | `translate` | `agent/context` | 记忆/技能/LSP/压缩四件套 + 可运行 Python 代码，是缺口「可复现实践」最可直接落地的原文，与 Claude 模型级 context rules 待处理项互补 |
| [2] SWE-Gate | `index` | `agent/eval` | 开源评测 + 34% 功能通过≠评审通过量化结论，改写 coding agent 验收标准讨论，索引即可（价值在数据集与归因结论） |
| [4] FrontierHarness Eval | `index` | `agent/eval` | 开源受控 harness×成本数据可作选型锚点与第二组互证基线；交互式数据表格不值得整译 |
| [1] RAMP（A Few Pages of Markdown） | `index` | `agent/harness` | 441 仓库实证 + 可复用 RAMP 工具，为 AGENTS.md 治理主线提供量化证据与挑战，索引含脉络即可 |
| [9] AgentRoom | `index` | `agent/multi-agent` | 机制级开放协议 + 「协调优于并发」反直觉结论，补多 agent 协作空白；论文全文译价值低于索引+后续扩展 |
| [6] Rachel Laycock 代码评审论 | `index` | `agent/eval` | Tier1 有具名对手的流程辩论，与 SWE-Gate 构成闭环；观点文不整译 |
| [8] 让数据为 Agentic AI 就绪 | `index` | `agent/rag` | Tier1 双作者模式目录（契约/隔离/语义层/linage），数据×agent 相邻扩展的可检索权威链接 |
| [10] OpenClaw 2.0 掘金长文 | `index` | `agent/platform` | 窗口内中文原创深度分析 + 产品级多用户/多 agent/升级反模式一手细节，编入平台脉络（主事实仍以官方为准） |

合计 `translate=3`、`index=7`、`observe=0`，满足硬性要求；无条目降为 observe——10 条均直接命中知识库方向或缺口，且与已收录/已跟踪 URL 无重复。

```json
{
  "analysis": {
    "priority": [
      "CPE 上下文提权攻击最高优先：M-CPE/X-CPE 新分类学 + 12 个真实 harness（含 Codex/Claude Code）系统审计，直击最薄弱的安全审计缺口，translate 全篇留存做审计清单",
      "FrontierHarness Eval 次优：data-eng-bench 之后第二组开源受控 harness×成本数据，通过率差 17pp/成本差 17x + 缓存命中率≠成本，支撑评测归因与选型",
      "SWE-Gate 第三：303 实例证明功能通过≠评审约束通过（34% 差距），把评测验收拉到真实合入门槛，与 Laycock 评审辩论构成闭环",
      "Headlong 与 DecodingAI 第 4 课并列：分别提供可运行的指数衰减 compaction 与记忆/技能/LSP/压缩四件套代码，直接填上下文/记忆可复现实践缺口",
      "RAMP/AgentRoom 其次：前者把 AGENTS.md 个案升级为 441 仓库量化证据，后者给出多 agent『协调优于并发』的机制级实验",
      "跨平台方向本轮零达标，不硬凑；KMP/Flutter 与跨平台 CI/发布缺口顺延并建议下一轮定向补源"
    ],
    "gaps_covered": [
      "Agent 安全审计：CPE 的 M-CPE/X-CPE 攻击分类 + 12 harness 实测（含 Codex/Claude Code），上下文组装首次被当作信任边界",
      "Agent 安全审计（产品侧）：OpenClaw 2.0 会话三档可见/按会话沙箱/凭据只写/出站绑死、roles≠租户隔离、自适应注入>80%",
      "上下文/compaction/记忆可复现实践：Headlong 指数衰减分辨率压缩 + 轨迹即上下文，DecodingAI 记忆文件上限/LSP 反馈环/会话单行压缩",
      "Agent 评测组件级归因：FrontierHarness 固定模型/任务/运行时下 9 harness 的成本×质量矩阵与 17 倍成本差",
      "Agent 评测验收现实性：SWE-Gate 的评审派生约束双门控，644 次功能通过中 221 次违规",
      "多智能体编排反模式：AgentRoom 证明收益来自协调本身而非并行/CRDT；OpenClaw Swarm 提供实验态产品参照",
      "AGENTS.md/提交型配置治理：RAMP 四级成熟度模型 + 441 仓库量化（无配置认知复杂度 +53% vs +27%）",
      "中小团队成本锚点（部分）：FrontierHarness 单次通过成本 $1.05-$18.34 受控基线，非现场数据"
    ],
    "gaps_open": [
      "跨模型可移植性与迁移指南：本轮无直接命中（中立模型选择只是评测去偏，非迁移方法论）",
      "KMP/CMP vs Flutter 架构选型、共享逻辑边界、工具链痛点；跨平台 CI/发布/性能基线（连续两轮空窗，需定向补源）",
      "Harness 自身行为/覆盖率的度量工具：SWE-Gate/FrontierHarness 均测任务侧，不测 harness 内部逻辑覆盖率",
      "激活策略（always-on/per-commit/conditional/human-summoned）系统化比较：仅 Headlong/OpenClaw 零散数据点",
      "长时程/持续 agent 评测方法论：Headlong 自陈仅能定性测量，无成熟基准",
      "多智能体权限隔离设计原语：CPE 给出攻击面，OpenClaw 明示协作控制非安全边界，缺可复用隔离模式",
      "生产环境（含模型/网关交互）的组件级归因：FrontierHarness 自曝局限，环境变量归因仍空"
    ],
    "trends": [
      "Harness 效应进入可复现评测品类：data-eng-bench、FrontierHarness、Terminal-Bench 论断三方独立互证「模型相同、harness 决定成本与排名」，与 ECC 的 harness 主战场论点一致",
      "竞争主轴从能力转向成本/效率：通过率收敛于 50-66.7% 而成本差 17 倍，『便宜地完成』成为独立技能，步数/token 计价成新度量",
      "评测验收向『人的验收现实』迁移：SWE-Gate 评审约束门禁 + Laycock 评审左移/按例外，与 SWE-Touch 同向，评审从仪式变成可机器判定的数据",
      "上下文从优化对象升级为信任边界：CPE 把攻击面上移到 message role 与作用域管理，context engineering 出现安全子域",
      "持久/自唤醒 agent 成为独立形态并产生自有故障类：自调度唤醒、SQLite 破坏性迁移、split-brain、『用 agent 修 agent』，评测与成本建模滞后",
      "单人 CLI 向团队驾驶舱/共享工作区演进：OpenClaw 多用户 Gateway+Swarm、AgentRoom CRDT 并发、Headlong 共享 agent，CRDT 机制流入 harness 层",
      "版本库成为 agent 治理面：RAMP 把提交型配置当成熟度代理指标，与 Klibsio 的 AGENTS.md 实践互证",
      "跨平台方向连续第二轮零信号：LangChain/Google 检索多营销内容，KMP/Flutter 需换定向信源，否则持续失联"
    ]
  },
  "candidates": [
    {
      "title": "What's in Your Agent's Context? Context Privilege Escalation Attacks against AI Agent Harness",
      "url": "http://arxiv.org/abs/2609.01222",
      "source": "arXiv (Zichuan Li, Xiaojing Liao, Luyi Xing 等)",
      "date": "2026-09-01",
      "verdict": "translate",
      "lineage": "agent/context",
      "reason": "首个系统化 harness 上下文安全分类学（M-CPE/X-CPE）+ 含 Codex/Claude Code 的 12 系统实测，直击安全审计最薄弱缺口，值得全篇留存做审计清单",
      "stars": 5
    },
    {
      "title": "Introducing FrontierHarness Eval: 9 harnesses, same model, cost per pass varies 17x",
      "url": "https://runta.com/blog/introducing-frontierharness-eval",
      "source": "Runta (Shilin Zhu, Shiqi Mei)；HN 81 分",
      "date": "2026-09-01",
      "verdict": "index",
      "lineage": "agent/eval",
      "reason": "开源受控 harness×成本×质量数据（360 试次、17 倍成本差、缓存命中率≠成本）作选型锚点与第二组互证基线，价值在数据与归因结论而非全文",
      "stars": 5
    },
    {
      "title": "SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents",
      "url": "http://arxiv.org/abs/2609.04167",
      "source": "arXiv cs.SE (Xin He, Yanlin Wang 等)",
      "date": "2026-09-03",
      "verdict": "index",
      "lineage": "agent/eval",
      "reason": "303 实例/34% 差距证明功能通过≠评审约束通过，开源双门控评测改写 coding agent 验收标准讨论，索引+数据集即可",
      "stars": 5
    },
    {
      "title": "Headlong: a microharness for persistent agents (Laude/MIT)",
      "url": "https://www.laude.org/updates/headlong-a-microharness-for-persistent-agents",
      "source": "Laude Institute；github.com/laude-institute/headlong",
      "date": "2026-08-24",
      "verdict": "translate",
      "lineage": "agent/harness",
      "reason": "可运行极简持久 micro-harness 全文：自唤醒循环、轨迹即上下文、指数衰减 compaction、沙箱与自伤事故，命中记忆可复现实践与 always-on 两个缺口",
      "stars": 4
    },
    {
      "title": "Context Engineering for Coding Agents (Building a Coding Agent From Scratch, Lesson 4)",
      "url": "https://www.decodingai.com/p/context-engineering-for-coding-agents",
      "source": "Paul Iusztin, Decoding AI Magazine",
      "date": "2026-08-25",
      "verdict": "translate",
      "lineage": "agent/context",
      "reason": "记忆/技能/LSP/压缩四件套 + 可运行 Python 代码与容量上限细节，是上下文工程缺口最可直接落地的原文",
      "stars": 4
    },
    {
      "title": "A Few Pages of Markdown: Committed AI Configuration and Lower Quality Cost after Coding-Agent Adoption",
      "url": "http://arxiv.org/abs/2608.25241",
      "source": "arXiv cs.SE (Yegor Denisov-Blanch 等)",
      "date": "2026-08-26",
      "verdict": "index",
      "lineage": "agent/harness",
      "reason": "441 仓库量化 + RAMP 成熟度工具为 AGENTS.md 治理主线提供实证并提示『set-and-forget』治理缺口，索引含脉络即可",
      "stars": 4
    },
    {
      "title": "AgentRoom: Concurrent Multi-Agent Coding in a CRDT-Backed Shared Workspace",
      "url": "http://arxiv.org/abs/2608.23740",
      "source": "arXiv (Seonglae Cho, Donghyun Lee)",
      "date": "2026-08-24",
      "verdict": "index",
      "lineage": "agent/multi-agent",
      "reason": "CRDT 文件系统+MCP claim/broadcast 的机制级开放实验，『协调优于并发』反直觉结论补多 agent 协作空白，索引后按需扩展",
      "stars": 4
    },
    {
      "title": "Maybe We Shouldn't Be Reviewing All This Code",
      "url": "https://martinfowler.com/rachels-ramblings/code-review.html",
      "source": "Rachel Laycock, martinfowler.com",
      "date": "2026-09-02",
      "verdict": "index",
      "lineage": "agent/eval",
      "reason": "Tier1 有具名对手与 Meta 数据的流程辩论，与 SWE-Gate 构成『评审左移+机器可判约束』闭环，观点文索引即可",
      "stars": 3
    },
    {
      "title": "Making Your Data Ready for Agentic AI",
      "url": "https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html",
      "source": "Pramod Sadalage & Prem Chandrasekaran, martinfowler.com",
      "date": "2026-08-27",
      "verdict": "index",
      "lineage": "agent/rag",
      "reason": "Tier1 双作者企业数据三层框架与模式目录，扩展数据×agent 相邻方向的可检索权威链接",
      "stars": 3
    },
    {
      "title": "憋了 7 周没动静，OpenClaw 2.0 带着 16000 个 PR 杀回来了",
      "url": "https://juejin.cn/post/7680352383386107940",
      "source": "一点一木, 稀土掘金",
      "date": "2026-09-01",
      "verdict": "index",
      "lineage": "agent/platform",
      "reason": "窗口内中文原创深度分析：多用户 Gateway/角色边界/Swarm/升级事故一手细节与反模式，编入平台脉络（主事实以官方为准）",
      "stars": 3
    }
  ]
}
```
tokens used
89,137
