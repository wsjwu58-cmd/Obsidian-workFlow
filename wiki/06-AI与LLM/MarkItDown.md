---
created: 2026-08-04
updated: 2026-08-04
sources: [raw/github-2026-08-03-3ba752ee.md]
tags: [AI, RAG, 工具链, Python]
---

# MarkItDown

微软开源的轻量 Python 工具，把 PDF / Office / 图片 / 音频 / HTML / EPUB 等统一转换为 Markdown，供 LLM 与文本分析管道使用。

## 详细说明

MarkItDown 强调保留标题、列表、表格、链接等文档结构，输出 token 效率高且贴近 LLM 原生理解格式；支持 OCR、语音转录、ZIP 遍历、YouTube 链接等多种输入。它正好补足知识库采集管线"把非 Markdown 素材转成 md"的需求，可作为 fetch_full 之外的可选转换器，也是 RAG 数据准备阶段的常用工具。

## 相关条目
- [[RAG处理优化]]
- [[ExtractBench]]
- [[自动化工作流功能与实现方案]]
- [[数据分析学习笔记]]
