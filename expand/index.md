---
created: 2026-08-03
updated: 2026-08-03
tags: [知识库, 索引]
---

# 内容总目录

> 知识库分类体系：`01-编程语言` → `02-前端` → `03-后端` → `04-数据库` → `05-数据结构与算法` → `06-AI与LLM` → `07-Linux与工具链` → `08-逆向与安全` → `09-源码解读` → `10-求职面试` → `11-生活杂项`
> 全库共 137 个 Markdown 文件（2026-08-04 巡检：断链 0 / 孤立 0 / 重复 0 / pending 0）。关系总览见 [[知识图谱]]。

## 知识库自动化

- [[自动化工作流设计]]：采集→过滤→加工→入库全自动管线设计文档（Agent 架构 / 平台接入 / LLM 质检 / Ingest 对接）
- [[自动化工作流功能与实现方案]]：GitHub Actions + Codex 混合自动化落地——功能需求清单、workflow 配置、实施路线图与运维指标
- [[动态索引]]：Dataview 按 frontmatter 动态生成的条目总览（F10，与 AI 维护的 index.md 互补）
- [[知识库周报]]：每周五自动生成的采集 / 加工 / 健康度周报（F08）

## 01-编程语言

- [[c++核心编程]]：C++ 内存分区、引用、函数与面向对象核心语法
- [[C++模板和STL]]：模板与 STL 容器/迭代器/算法库
- [[图结构的应用]]：图的基本结构与 BFS/DFS 搜索算法应用
- [[Dijkstra最短路算法]]：C++ 邻接矩阵 Dijkstra 最短路实现（图算法编程练习）
- [[python]]：Python 学习入口（⚠️ 空笔记，待补充）
- [[数据分析学习笔记]]：NumPy / Pandas / Matplotlib 数据分析实战
- [[01-编程语言/python/集合]]：Python 列表/元组/集合/字典四大数据结构对比

## 02-前端

- [[Day01]]：前端入门第一天——工具链与开发环境
- [[Day02]]：前端入门第二天——HTML 图片与常用标签
- [[Day03]]：前端入门第三天——CSS 与样式
- [[Day04]]：前端入门第四天——Bootstrap 与网格布局
- [[Day05]]：前端入门第五天——JavaScript 基础与练习
- [[Day06]]：前端入门第六天——正则表达式基础
- [[Layui表格和表单]]：Layui UI 框架表格与表单组件
- [[VUE]]：Vue 常用指令与渐进式框架核心概念

## 03-后端

- [[面向对象]]：Java 对象内存分配与 OOP 基础
- [[03-后端/java/集合]]：Java 集合框架（ArrayList 等）
- [[Stream]]：Java Stream 流式 API 与 Lambda
- [[java高级技术]]：Java 进阶特性
- [[javaweb]]：JavaWeb 开发（含 Vue 前端集成）
- [[案例]]：JavaWeb 综合案例
- [[Mybatis-plus]]：MyBatis-Plus 持久层框架
- [[mq]]：RabbitMQ 消息队列（异步调用/选型）
- [[redis]]：Redis 启动配置与常用命令
- [[redis分布式缓存]]：Redis 分布式缓存（⚠️ 空笔记，待补充）
- [[rocketmq]]：RocketMQ 发布-订阅消息模型
- [[judge0 API调用]]：Judge0 部署实战与 cgroup 兼容性排查
- [[苍穹]]：苍穹外卖项目——类别/菜品/套餐业务关系设计
- [[JavaGuide]]：Java 后端学习与面试指南（基础 / 集合 / 并发 / JVM / 数据库 / 分布式 / AI）

## 04-数据库

- [[Mysql]]：MySQL SQL 语言分类与基础操作
- [[进阶]]：MySQL 进阶——存储引擎与事务
- [[InnoDB引擎]]：InnoDB 存储引擎原理
- [[管理数据库]]：MySQL 数据库管理操作

## 05-数据结构与算法

- [[BFS经典题目]]：BFS 经典题（奇怪电梯/迷宫）
- [[DP动态规划]]：动态规划与状压 DP
- [[平衡二叉树旋转机制]]：AVL 平衡二叉树旋转调整
- [[排序]]：常见排序算法
- [[红黑树]]：红黑树性质与实现
- [[贪心算法]]：贪心算法思想

## 06-AI与LLM

- [[全量微调]]：全量微调（Full Fine-Tuning）概念（⚠️ 待补充）
- [[高效微调]]：PEFT 高效参数微调（LoRA/QLoRA/Adapter）（⚠️ 待补充）
- [[Agent搭建]]：从符号主义到 LLM Agent，ReAct 模式与 LangGraph 实现
- [[MCP协议与工具调用]]：MCP 协议标准与工具调用演进
- [[RAG处理优化]]：RAG 检索增强生成原理与优化
- [[多智能体与记忆机制]]：多智能体协作与 Agent 记忆机制
- [[langchain4j-study-notes-01-core]]：LangChain4j 核心概念（ChatModel 等）
- [[langchain4j-study-notes-02-rag]]：LangChain4j RAG 实战
- [[langchain4j-study-notes-03-advanced]]：LangChain4j 高级特性
- [[langgraph4j-study-notes-01-core]]：LangGraph4j 有向图工作流（DAG）
- [[langgraph4j-study-notes-02-advanced]]：LangGraph4j 高级应用

### 外部摄入 · Agent研究与评测（2026-08-04）

- [[AgentHPOBench]]：评估 LLM Agent 作为顺序超参数优化器的基准（7 类 30 任务）
- [[ExtractBench]]：模式引导的企业文档提取基准（370 文档 / 4869 页）
- [[DungeonBench]]：D&D 规则密集型战术推理基准（遭遇战 + 一日冒险双轨道）
- [[MOT-SR]]：多目标工具增强符号回归框架（双 LLM 模块 + 帕累托前沿）
- [[在线策略交互与模仿学习]]：专家交互放宽模仿学习表征需求，提出 OVI 算法
- [[SWE-Touch-编码Agent共享工作空间基准]]：SWE-Touch 基准揭示编码 Agent 对用户代码修改的适应能力不足，平均解决率下降 7.7 个百分点
- [[ParEvalLayer-部分LLM代理评价决策层]]：通过部分评价结果提前做出可靠决策，基准测试成本降低 75%+
- [[Magnet跨会话AI滥用检测]]：通过能力累积检测跨会话 AI 滥用（跨会话目标分解攻击 + 磁铁式证据聚合）
- [[Tiny-Damage-车辆损伤评估Agentic-VLM分割落地]]：专用分割模型为 Agentic VLM 提供空间 grounding，报告幻觉率 92%→31%
- [[UEmbed统一稀疏与稠密多模态嵌入]]：解码器专用统一稀疏与稠密多模态嵌入模型
- [[PRECOG-边缘语言模型结构化内存与O1状态注入]]：O(1) SSM 状态注入实现边缘 LLM 持久上下文，RAG 预填成本降至常数级
- [[AtumAI-数据中心控制面策略生成框架]]：LLM + 进化搜索融合的数据中心控制面策略生成 Agent 框架
- [[认知能力差距分类学与适应性认知智能架构ACIA]]：五维度认知能力差距分类法 + 适应性认知智能架构（ACIA）
- [[实时检测与修复LLM-Agent失败]]：基于单步遥测的轻量级实时检测与修复，成功率提升至 73%

### 外部摄入 · Agent工具与平台（2026-08-04）

- [[ECC]]：面向编程代理的"代理工具操作系统"（技能 / 记忆 / 安全）
- [[Hermes-Agent]]：Nous 的自我改进 AI 代理——闭环学习与跨会话记忆
- [[n8n]]：AI 原生工作流自动化平台（可视化画布 + 1500+ 集成）
- [[MarkItDown]]：深度解析——任意文件转 LLM 友好 Markdown（架构 / 插件 / Azure 集成 / 安全实践）
- [[dify-llm-app-platform-deep-dive]]：深度解析开源 LLM 应用开发平台 Dify（工作流 / RAG / Agent / LLMOps）
- [[langchain-agent-engineering-platform]]：LangChain 作为 Agent 工程平台的核心价值与生产级选型指南
- [[open-webui-自托管AI平台深度解析]]：可扩展、支持离线部署的自托管 AI 平台（Ollama/OpenAI 集成、本地 RAG）
- [[cc-switch-跨平台AI编码代理配置管理器]]：Tauri 跨平台工具，统一管理 Claude Code / Codex 等代理配置
- [[awesome-llm-apps-开源AI代理与RAG应用集锦]]：100+ 开源 AI 代理、技能与 RAG 应用模板
- [[llms-reward-expertise-领域知识决定LLM使用上限]]：领域知识是发挥 LLM 潜力的关键，专家引导优于通用提示技巧
- [[DeepSeek-V4-Flash-0731-斩杀线分析]]：DeepSeek V4 Flash 以 284B 参数成为性价比"斩杀线"的架构与工程拆解
- [[DeepSeek-V4-Flash-8万亿Token调用量信号解读]]：8 万亿 Token 单日调用量背后的 AI 编程 Agent 规模化落地信号

## 07-Linux与工具链

- [[Linux操作系统]]：Linux 目录结构、systemctl 等系统管理
- [[Shell]]：Shell 脚本入门（bash）
- [[git]]：Git 配置、工作区域与基本操作

## 08-逆向与安全

- [[base64]]：Base64 编码原理与码表
- [[取余与逆向脚本]]：CTF 逆向脚本——字符数组异或解码
- [[Destination 逆向题解]]：CTF 逆向综合题——花指令、XXTEA、天堂之门、Lua 魔改
- [[标志寄存器]]：x86 汇编基础——寄存器、指令与寻址
- [[花指令]]：花指令混淆原理与 angr 符号执行入门
- [[题目总结]]：NSSCTF 题目总结——迷宫 BFS、base64 换表、取模、Z3

## 09-源码解读

### Claude Code（终端 AI 编程助手逆向分析，23 篇）

- [[1-xiang-mu-gai-lan]]：项目概览与技术定位
- [[2-kuai-su-kai-shi]]：快速开始
- [[3-huan-jing-yao-qiu-yu-an-zhuang]]：环境要求与安装
- [[4-deng-lu-yu-ping-tai-pei-zhi]]：登录与平台配置
- [[5-feature-flags-gong-neng-kai-guan]]：Feature Flags 功能开关
- [[6-wu-ceng-jia-gou-she-ji]]：五层架构设计
- [[7-agentic-loop-he-xin-xun-huan]]：Agentic Loop 核心循环
- [[8-queryengine-bian-pai-ji-zhi]]：QueryEngine 编排机制（⚠️ 空笔记）
- [[9-hui-hua-zhuang-tai-guan-li]]：会话状态管理
- [[10-gong-ju-xi-tong-jia-gou]]：工具系统架构
- [[11-nei-zhi-gong-ju-xiang-jie]]：内置工具详解
- [[12-mcp-xie-yi-ji-cheng]]：MCP 协议集成
- [[13-computer-use-dian-nao-cao-kong]]：Computer Use 电脑操控
- [[14-voice-mode-yu-yin-mo-shi]]：语音模式
- [[15-quan-xian-mo-xing-yu-gui-ze-yin-qing]]：权限模型与规则引擎
- [[16-auto-mode-zi-dong-mo-shi]]：自动模式（⚠️ 空笔记）
- [[17-sha-xiang-an-quan-ji-zhi]]：沙箱安全机制
- [[18-remote-control-yuan-cheng-kong-zhi]]：远程控制
- [[19-agent-xie-diao-mo-shi]]：Agent 协调模式
- [[20-memory-ji-yi-xi-tong]]：Memory 记忆系统
- [[21-zi-ding-yi-agents]]：自定义 Agents
- [[22-skills-ji-neng-kai-fa]]：Skills 技能开发
- [[23-hooks-ji-zhi]]：Hooks 机制

### Judge0（开源在线代码执行系统解析，19 篇）

- [[1-概述：开源在线代码执行系统]]：系统定位与技术架构总览
- [[2-快速启动：Docker Compose 部署指南]]：Docker Compose 快速部署
- [[3-提交（Submission）核心概念]]：Submission 核心概念
- [[4-编程语言与状态枚举]]：编程语言与状态枚举
- [[5-系统架构设计]]：系统架构设计
- [[6-SubmissionsController 控制器]]：提交控制器
- [[7-IsolateJob 沙箱执行任务]]：沙箱执行任务
- [[8-IsolateRunner 任务调度器]]：任务调度器
- [[9-Submission 数据模型与字段编码]]：数据模型与字段编码
- [[10-Language 语言配置模型]]：语言配置模型
- [[11-创建提交 API]]：创建提交 API
- [[12-批量提交与查询 API]]：批量提交与查询 API
- [[13-系统配置信息 API]]：系统配置信息 API
- [[14-认证机制]]：认证机制
- [[15-授权机制]]：授权机制
- [[16-配置文件详解]]：配置文件详解
- [[17-Docker Compose 服务架构]]：Docker Compose 服务架构
- [[18-安全机制与沙箱隔离]]：安全机制与沙箱隔离
- [[19-性能调优与扩展]]：性能调优与扩展

### Free-fs（网盘项目解析）

- [[09-源码解读/Free-fs（网盘项目的解析）/free-fs]]：网盘项目存储系统模块——SPI 服务发现与存储插件

## 10-求职面试

- [[面试]]：AI 代码审查系统面试——MCP 工具生态与 RAG 架构设计

## 11-生活杂项

- [[驾照考试要点]]：驾照考试扣分/罚款知识点（与编程无关）

## 待办清单（维护提醒）

1. ⚠️ **安全**：`私密/密码管理.md` 含真实密码与 GitHub Token，已移出 wiki 图谱。建议立即**吊销该 Token** 并开启两步验证。
2. ⚠️ **安全**：`wiki/03-后端/javaweb/案例.md` 曾含阿里云 AccessKey（已移入私密并重写历史），请到阿里云控制台**吊销**该密钥。
3. ✅ 已完成（2026-08-03）：Free-fs 去重，保留 `Free-fs（网盘项目的解析）` 一份
4. 补全：4 个空笔记（`python`、`redis分布式缓存`、Claude Code 8/16 篇）+ 2 个占位笔记（`全量微调`、`高效微调`）。
5. ✅ 已完成（2026-08-03）：`x #includestdio.md`→[[取余与逆向脚本]]、`x #include iostream...`→[[Dijkstra最短路算法]]、`未命名.md`→[[Destination 逆向题解]]、`Untitled.md`→[[驾照考试要点]]
