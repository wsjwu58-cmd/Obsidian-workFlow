# feedback/ — 提示词效果反馈

使用 `prompts/` 中各条提示词的实测效果记录。**驱动提示词积累闭环**：

```
用 → 效果（好/中/差/翻车） → 积累 → 回 prompts/ 补改进记录
```

## 格式建议

```markdown
## [YYYY-MM-DD] {prompt 名} 效果 {好|中|差|翻车}

- 场景：...
- 结果：...
- 问题：...
- 改进方向：...
```

## 当前台账

由 `scripts/feedback_capture.py` 把 CI 工作流失败自动记录到 `expand/log.md`（`[YYYY-MM-DD] feedback | ...`）。如需人工沉淀 prompts 效果，在本目录新建条目。