---
created: 2026-08-03
updated: 2026-08-09
tags: [知识库, 日志]
---

# 变更日志

> 时间倒序排列

## [2026-08-24] lint | 巡检报告

- 巡检时间：2026-08-24 | 条目数：143 | 断链：6 | 孤立：0 | 重复对：0 | pending：0 | index 缺失：0 | 空笔记：5
- ⚠️ 发现异常：断链 6 处；- `expand/index.md` → [[Claude-Code-v2-1-224-self-hosted-environ-translation]]；- `expand/index.md` → [[EvolveNet-Collaborative-Harness-Evolutio-translation]]；- `expand/index.md` → [[Harness-R1-Learning-to-Edit-Executable-R-translation]]；- `expand/index.md` → [[I-Gave-Claude-Code-an-AGENTS-md-Contract-translation]]；- `expand/index.md` → [[The-Shape-of-Things-to-Come-Part-1-The-C-translation]]；- `expand/index.md` → [[Meta-launches-Muse-Code-for-complex-soft-translation]]


## [2026-08-09] ingest | Rust 2025 官方博客：Rust 1.85 版本说明（Move 语义 / Borrow Checker 演进）

- 处理：`references/articles.md` 待处理 → 已收录（编号 15，归属 `expand/thinking/`）
- 新增：[[Rust2024版次的语义收紧与异步闭合]]——Rust 1.85 / 2024 版次判值思考（采集器「Move 语义」标签纠偏；edition ≈ 语义债务清偿机制；unsafe 边界从 lint 升级为语言规则；async closures 补齐「闭包 × 借用 × await」三角；版本号不承载语义里程碑）
- 更新：[[index]]（thinking 段 + 计数 132→133）、[[知识图谱]]（编程语言簇补 Rust 思考节点）、`references/articles.md`（待处理清空 + 编号 15 + 统计 11→12）

## [2026-08-09] ingest | MCP 官方文档：Model Context Protocol 介绍

- 处理：`references/articles.md` 待处理 → 已收录（编号 14）
- 新增：[[MCP协议标准化的增量与边界]]——expand/thinking/ 首条独立思考条目（USB-C 类比只到接口层 / 语义适配 M×N / 2026-07-28 版增量：MCP Apps、Agent Skills、Registry、server/discover）
- 更新：[[index]]（thinking 段 + 计数 131→132）、[[知识图谱]]（AI 主题簇补 MCP 思考节点）、[[ECC]]（相关条目回链）

## [2026-08-09] maintenance | 素材层迁移：raw/ → references/raw/ + working/ + Codex 情报追踪

- 迁移：`raw/`（14 个素材）物理移入 `references/raw/`，`references/` 成为 Phase 0 顶层（素材库 + 去重索引）
- 新增：`references/agents.md`——references 层规则（raw 素材状态机 + articles.md 去重权威双层约定）
- 新增：`references/articles.md`——文章去重索引表（模板，`scripts/retrack.py --list/--url` 查询）
- 新增：`working/` + `working/AGENTS.md`——Phase 4 作品输出层（译文/工具/模板，可独立理解）
- 新增：`scripts/retrack.py`——文章去重权威查询 CLI
- 更新：`scripts/check_consistency.py` K1 改为检查 `references/raw/` 状态机
- 更新：`scripts/collect.py` existing_urls 合并 `references/articles.md` URL 作为去重输入
- 更新：`scripts/ingest.py` build_prompt 注入 `{art_titles}`（references/articles.md 去重权威段）
- 更新：9 个脚本 + codex_task.ps1 + 2 个 workflow（collect.yml / ingest.yml）+ pre-commit 的 `raw/` 路径批量改为 `references/raw/`
- 新增：`.github/workflows/research.yml` + `prompts/deep-research-tracker.md`——Codex 情报追踪自动化（三层 prompt：广度/分析/注入，术语每周 1-2 次）
- agents.md 目录结构同步（raw/ 迁入 references/、新增 working/、Phase 0-4 映射表）

## [2026-08-09] maintenance | prompts/ 有效提示词积累目录落地

- 新增：`prompts/AGENTS.md`——目录规则（只收录验证有效的提示词，两种形态，效果评价闭环）
- 新增：`prompts/ingest.md`——ingest 深度加工提示词沉淀（权威源 `scripts/ingest.py:176`，含质量门槛/skip/补充溯源设计说明）
- 新增：`prompts/feedback/README.md`——提示词效果反馈台账
- 更新：`agents.md` 目录结构加入 `prompts/` 说明（不属知识图谱、不参与一致性门禁）

## [2026-08-09] maintenance | Ingest 提示词与 agents.md 模板方向聚焦（Track 3）

- 更新：`agents.md` AI 生成条目模板——角色设定改为聚焦两大追踪方向（AI Agent 开发 / 跨平台开发），新增「质量门槛」三段式（必须满足/加分项/直接排除）与 `skip` 机制（不达标标记 `rejected`），知识关联地图补充去重检查
- 更新：`技术说明` 由 Bing Search API 修正为 Firecrawl Search（含 `FIRECRAWL_SEARCH_DISABLED` 开关），与 `ingest.py` 实际行为保持一致
- 更新：`scripts/ingest.py` 提示词——角色聚焦 Agent / 跨平台、质量门槛 + skip 跳过、已知条目升级为「去重权威」段、LLM 返回 `skip: true` 时素材标 `rejected` 而非硬生成

## [2026-08-09] maintenance | 一致性门禁上线（Track 1：不变量检查 K1-K7）

- 新增：`scripts/check_consistency.py`——K1 raw 状态机 / K2 index 计数声明 / K3 expand frontmatter 完整 / K4 双链可解析 / K5 条目均入 index / K6 表格形状 / K7 孤立节点（仅警告）。退出码供 CI / 钩子使用
- 新增：`.githooks/pre-commit`——本地提交前触发 K1-K7，staging 涉及 `expand/` `wiki/` `scripts/` `.githooks/` `.github/workflows/` 才运行，不合格阻断 commit
- 新增：`.github/workflows/consistency.yml`——CI 门禁，job 名固定 `consistency / check`（分支保护按 check run 匹配），不做路径过滤
- 经验：PS 5.1 `Set-Content -Encoding UTF8` 会写 BOM 破坏 shebang，钩子必须 BOM-free 写入；Git for Windows 钩子 CWD 在 git 安装目录，须用 `git rev-parse --show-toplevel` 定位仓库根
- 配置：`git config core.hooksPath .githooks`
- 实测：违规条目提交被拦截（K2/K3/K5 报错）；无关文件与全绿提交均放行

## [2026-08-09] lint | 巡检报告

- 巡检时间：2026-08-09 | 条目数：120 | 断链：0 | 孤立：0 | 重复对：0 | pending：0 | index 缺失：0 | 空笔记：6

## [2026-08-08] lint | 巡检报告

- 巡检时间：2026-08-08 | 条目数：120 | 断链：0 | 孤立：0 | 重复对：0 | pending：0 | index 缺失：0 | 空笔记：6

## [2026-08-07] lint | 巡检报告

- 巡检时间：2026-08-07 | 条目数：120 | 断链：0 | 孤立：0 | 重复对：0 | pending：0 | index 缺失：0 | 空笔记：6

## [2026-08-06] lint | 巡检报告

- 巡检时间：2026-08-06 | 条目数：120 | 断链：0 | 孤立：0 | 重复对：0 | pending：0 | index 缺失：0 | 空笔记：6

## [2026-08-05] lint | 巡检报告

- 巡检时间：2026-08-05 | 条目数：120 | 断链：0 | 孤立：0 | 重复对：0 | pending：0 | index 缺失：0 | 空笔记：6

## [2026-08-04] maintenance | 翻译后端去 LLM 化——本地 MarianMT / Google / LLM 兜底

- 新增：`scripts/translator.py` 可插拔翻译后端——`TRANSLATE_BACKEND=local|google|llm|auto`（默认 auto：本地 MarianMT 零 token → Google 免费 → DeepSeek 兜底；已中文内容自动跳过）
- 更新：`scripts/fetch_full.py` 改用 translator 模块，新增 `--backend` 参数；`requirements.txt` 增加 `deep-translator`（Actions 云端走 Google 后端）
- 更新：`scripts/requirements-semantic.txt` 增加 `sentencepiece`（本地翻译 / 语义检索共用依赖）
- 实测：本地 opus-mt-en-zh 翻译 RAG 段落正常，零 token 消耗；质量中等，需要出版级措辞时可切回 `llm`

## [2026-08-04] maintenance | README 文档重写

- 更新：`README.md` 完整重写——项目简介、架构图、目录结构、6 条 GitHub Actions 流水线与 2 个 Codex 定时任务、核心脚本表、快速开始（依赖 / 密钥 / 使用）、Obsidian 配置、质量指标与安全说明

## [2026-08-04] maintenance | 自动化四件套落地（模式A / 周报·告警 / F10·F11 / RSSHub）

- 模式 A：Codex 定时任务上线——Windows 任务计划程序 `Codex-KB-Weekly-Ingest`（周一 06:30 周加工）与 `Codex-KB-Daily-Lint`（每天 09:00 日巡检），经 `scripts/codex_task.ps1` 调用 Codex CLI（workspace-write 沙箱）
- F08：新增 `scripts/weekly_report.py` + `weekly-report.yml`（每周五 19:00），首次生成 [[知识库周报]]
- F09：新增 `failure-notify.yml`，任一 workflow 失败经 `NOTIFY_WEBHOOK` 告警（未配置则跳过）
- F10：安装 Dataview / Templater 插件，新增 [[动态索引]] 与 `templates/新条目模板.md`
- F11：新增 `scripts/semantic_search.py`（sentence-transformers + SQLite，TF-IDF 降级），已建 110 篇索引，embedding 检索实测通过
- RSSHub：`collect.py` 接入掘金分类 / 知乎热榜（`RSSHUB_BASE` 可配置；公共实例建议替换为自建）
- 配置：`scripts/setup_secrets.py` 一键同步密钥到 GitHub Secrets（已同步 LLM_API_KEY / LLM_BASE_URL / LLM_MODEL / BING_SEARCH_ENDPOINT）
- 文案：`ingest.yml` / `ingest.py` 由「六维」统一改为「深度技术笔记模板」

## [2026-08-04] lint | 巡检报告

- 巡检时间：2026-08-04 | 条目数：120 | 断链：0 | 孤立：0 | 重复对：0 | pending：0 | index 缺失：0 | 空笔记：6

## [2026-08-04] maintenance | 接入 Bing Search API（[补充] 联网检索）

- 新增：`scripts/bing_search.py`（Bing Web Search API v7 封装，未配置密钥时优雅降级）
- 更新：`scripts/ingest.py` 用素材主题检索并把结果注入 Prompt，`[补充]` 内容可基于真实来源并附 URL；新增 `--no-search` 开关
- 更新：`ingest.yml` 传入 `BING_SEARCH_API_KEY` / `BING_SEARCH_ENDPOINT` Secrets
- 待配置：密钥需由用户提供后写入 `私密/API密钥.md` 并设置仓库 Secret

## [2026-08-04] ingest | MarkItDown 按深度技术笔记模板重加工

- 更新：[[MarkItDown]]（`expand/06-AI与LLM/Agent工具与平台/`）——六维格式升级为深度技术笔记模板（核心概念拆解 / 方案对比 / 代码速查 / 避坑清单 / 知识关联地图）
- 加固：`scripts/ingest.py` LLM 调用增加自动重试（503 容错，最多 3 次退避）

## [2026-08-04] maintenance | AI 加工升级：深度技术笔记模板

- 更新：`agents.md` AI 生成条目标准由六维框架升级为「深度技术笔记模板」（角色设定 / 强制补全 `[补充]` 溯源 / 人话解释 / 代码规范 / 工程视角 / 表格化排版）
- 更新：`scripts/ingest.py` Prompt 接入新模板；`自动化工作流设计.md` 与 `自动化工作流功能与实现方案.md` 同步
- 实测：MarkItDown 素材按新模板生成成功——含方案对比表、带版本代码示例、Top3 报错、知识关联地图（自动链接知识库真实条目）
- 说明：自动化管道中 `[补充]` 内容来自模型内部知识，建议人工抽检；实时联网检索为后续增强项

## [2026-08-04] maintenance | P3 模式 B 上线：自动六维加工 + PR 审阅

- 新增：`scripts/ingest.py`（raw pending → DeepSeek 六维生成 wiki 条目 → 自动分类 / 索引 / 日志 / 状态机）、`scripts/count_pending.py`、`.github/workflows/ingest.yml`（每天 08:00，改动提交 `ai-ingest` 分支并开 PR）
- 设计：确定性逻辑在脚本（分类校验 / 幂等 / 索引写入），创造性交给 LLM；`私密/` 不离开本地；PR 人工审阅闭环；git 全程可回滚
- 验证：本地 dry-run 通过（六维条目生成 + JSON 解析 + 分类校验）；远端待触发验证

## [2026-08-04] ingest | 六维加工框架落地 + 首批条目重写

- 更新：`agents.md` 知识条目格式新增「六维加工框架」（结构化提炼 / 深度追问 / 联想缝合 / 场景转译 / 媒介转换 / 元数据标签）
- 重构：首批 10 条摄入条目按六维框架重写，归入新子目录 `06-AI与LLM/Agent研究与评测`、`06-AI与LLM/Agent工具与平台`
- 更新：[[index]]（子目录分组）、[[知识图谱]]（簇说明）、[[自动化工作流设计]] 与 [[自动化工作流功能与实现方案]]（六维加工 Prompt / 标准）

## [2026-08-04] ingest | 首批采集素材摄入（10 条）

- 新增：[[AgentHPOBench]]、[[ExtractBench]]、[[MOT-SR]]、[[DungeonBench]]、[[在线策略交互与模仿学习]]、[[ECC]]、[[Hermes-Agent]]、[[n8n]]、[[MarkItDown]]、[[JavaGuide]]
- 更新：[[index]]（+10 条目，共 115）、[[知识图谱]]（AI 外部摄入簇 + Agent 工具簇 + JavaGuide 指南桥）
- 标记：`raw/` 中 10 条素材 `status` → `processed`

## [2026-08-04] maintenance | P2 采集管道升级：全文抓取 + DeepSeek 翻译

- 新增：`scripts/fetch_full.py`（GitHub README / 文章正文 / arXiv / YouTube / B站字幕 / PDF 全文抓取，经 DeepSeek 翻译为简体中文）
- 更新：`scripts/filter.py` 与 `collect.yml` 默认 DeepSeek（`LLM_BASE_URL` / `LLM_MODEL` 已配置为仓库 Secrets）；`collect.yml` 增加依赖安装与全文翻译步骤
- 实测：13 条素材 → 全文抓取成功 11 条 → DeepSeek 打分保留 10 条（7-8.7 分）
- 说明：2 条外部文章站点抓取失败保留原摘要；视频/PDF 抓取逻辑已实现，待真实链接验证

## [2026-08-03] lint | 巡检报告

- 巡检时间：2026-08-03 | 条目数：108 | 断链：0 | 孤立：0 | 重复对：0 | pending：0 | index 缺失：0 | 空笔记：6


## [2026-08-03] security | 阿里云 AccessKey 泄露处置

- 拦截：GitHub push protection 检测到 `wiki/03-后端/javaweb/案例.md` 含阿里云 AccessKey ID/Secret，推送被拒
- 处置：密钥已移入 `私密/阿里云AccessKey.md`；笔记中替换为占位符；重写全部本地提交历史，已确认无残留
- 加固：`scripts/scan_secrets.py` 新增 Alibaba AccessKey 检测模式
- 提醒：请到阿里云控制台**吊销**该 AccessKey 并重新创建

## [2026-08-03] maintenance | P1 巡检与安全上线

- 新增：`scripts/lint.py`（断链 / 孤立 / 重复 / 积压 / index 同步 / 空笔记六项巡检，首跑全绿）、`scripts/scan_secrets.py`（凭据扫描，本地验证 0 命中）
- 新增：`.github/workflows/lint.yml`（每日 08:30）、`.github/workflows/scan-secrets.yml`（push/PR 触发）
- 更新：[[index]]（Day02-06 摘要细化）；Free-fs 去重后引用清理（保留「网盘项目的解析」版）
- 安全：LLM_API_KEY 已存入 `私密/API密钥.md`，待配置为 GitHub Secret

## [2026-08-03] lint | 巡检报告

- 巡检时间：2026-08-03 | 条目数：108 | 断链：0 | 孤立：0 | 重复对：0 | pending：0 | index 缺失：0 | 空笔记：6


## [2026-08-03] maintenance | P0 地基：git 初始化与文件名规范化

- 初始化：`D:\note` 建立 git 仓库（main 分支），`.gitignore` 排除 `私密/`、`.claudian/`、Obsidian 工作区状态
- 重命名：[[取余与逆向脚本]]、[[Dijkstra最短路算法]]、[[Destination 逆向题解]]、[[驾照考试要点]]（原文件名含特殊字符或不可描述，无法被链接解析）
- 更新：[[index]]（新增两条目摘要、待办标记完成）、[[知识图谱]]（引用更新与孤立节点清理）

## [2026-08-03] design | 自动化工作流功能与实现方案

- 新增：[[自动化工作流功能与实现方案]]（GitHub Actions + Codex 混合自动化落地：11 项功能需求清单、5 个 workflow 设计、实施路线图 P0-P4、运维指标与风险对策）

## [2026-08-03] design | 自动化工作流架构设计

- 新增：[[自动化工作流设计]]（采集→过滤→加工→入库全自动管线设计文档）

## [2026-08-03] init | 知识库初始化与全量重组

- 建立三层结构：`raw/`（原始素材，只读）、`wiki/`（结构化知识）、`agents.md`（规则文件）
- 将根目录 16 个散落文件夹的 **104 个笔记**按主题分类移入 `wiki/` 下 11 个分类目录（01-编程语言 ~ 11-生活杂项）
- 新增：[[知识图谱]]（关系中枢）
- 为 **100 个笔记**追加 `## 相关条目` 双向链接段，构建全库知识图谱
- 新增：`wiki/index.md` 内容总目录（含 104 条目一句话摘要）
- 新增：`agents.md` 知识库管理规则文件
- 隔离：`c++/密码管理.md` → `私密/密码管理.md`（含真实凭据，不进入知识图谱）
- 修复：移除 `wiki/08-逆向与安全/.obsidian` 嵌套库配置（已备份至临时目录）
- 待办：去重 Free-fs 两份笔记；补全 4 个空笔记；重命名不规范文件名（详见 [[index]] 待办清单）

## [2026-08-10] curate | 20260810-115607
- 收录：Meta-launches-Muse-Code-for-complex-soft-translation.md
- 观察项：无
- 淘汰：无

## [2026-08-17] curate | 20260817-062607
- 收录：Claude-Code-v2-1-224-self-hosted-environ-translation.md, EvolveNet-Collaborative-Harness-Evolutio-translation.md, Harness-R1-Learning-to-Edit-Executable-R-translation.md, I-Gave-Claude-Code-an-AGENTS-md-Contract-translation.md, The-Shape-of-Things-to-Come-Part-1-The-C-translation.md
- 观察项：无
- 淘汰：无
