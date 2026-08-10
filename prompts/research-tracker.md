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
