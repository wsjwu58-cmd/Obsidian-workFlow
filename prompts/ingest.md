---
created: 2026-08-09
updated: 2026-08-09
type: workflow
source: scripts/ingest.py:176
status: 已实践
---

# Ingest 深度加工提示词

把 `raw/` 采集素材加工为可入 `expand/` 的深度技术笔记。**权威源：`scripts/ingest.py` 的 `build_prompt()`，本文仅沉淀使用说明与效果记录，正文以代码为准。**

## 工作流目标

1. 输入 `raw/`.md（title + url + source + body）
2. 过滤：不满足「质量门槛」直接返回 `skip: true`（素材标 `rejected`）
3. 加工：按深度技术笔记模板输出结构化章节
4. 入库：写入 `expand/`，同步更新 index.md / log.md / 知识图谱

## 关键设计

- **角色聚焦**：AI Agent 开发 + 跨平台开发两大方向，无关但有价值的归「通用技术」
- **质量门槛三段式**：必须满足（实质内容/原创洞察/可信来源）→ 加分项 → 直接排除（重量/无关/重复）
- **skip 机制**：不达标输出 `skip: true` + `skip_reason`，不硬生成
- **[补充] 溯源**：正文融合外部权威信息时标注来源，最优先用 Firecrawl 联网检索的真实结果
- **知识关联地图**：要求从知识库现有条目中建立双链，防止重复主题

### 全文（`scripts/ingest.py:176-270` 动态读取）

```python
# 使用方式（仓库内）
python scripts/ingest.py --dry-run          # 演练，不落盘
python scripts/ingest.py                    # 处理所有 status=pending 素材
python scripts/ingest.py --paths file.md    # 处理指定素材
```

## 效果评价（实测）

| 场景 | 结果 | 备注 |
|------|------|------|
| 2026-08-09 Track 3 聚焦后 dry-run | 好 | prompt 生成正常，含 skip/去重权威段 |

> 待积累：跑满 2 周后按「好/中/差/翻车」补充评价与改进记录。

## 参考素材与相关链接

- 知识库规则：`agents.md`「AI 生成条目：深度技术笔记模板」
- 参考仓库：harness-engineering（`prompts/` 深度调研 tracker 结构，见 `harness-engineering-main/`）