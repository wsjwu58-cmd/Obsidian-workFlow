#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""失败反馈捕获（Feedback Flywheel，Track 2b）。

借鉴 harness-engineering「反馈飞轮」：失败信号 → 记录根因 → 沉淀为护栏。
本脚本把 GitHub Actions / 本地任务的工作流失败事件，以统一格式追加到
expand/log.md，供后续 AI 会话与人工复盘引用（失败不再只进 Webhook 通知）。

对每种失败按「根因分类」标注（可手动传，供后续护栏改进）：
  - context   上下文信号：缺上下文 / 过期依赖
  - instruction 指令信号：提示词 / 配置不当
  - workflow  工作流信号：任务拆解 / 时序问题
  - infra    模型 / 环境 / 基础设施
  - unknown   未分类

用法（CI 失败事件以环境变量传入）：
  python scripts/feedback_capture.py
    --workflow "AI 加工（深度 Ingest）"
    --run-id 1234567
    --branch main
    --sha abc123
    --url https://github.com/x/y/actions/runs/1234567
    --classification infra

幂等：同一 (workflow, run_id) 只写一次；不写文件仅打印时用 --dry-run。
仅依赖标准库。
"""
import argparse
import datetime
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOG = ROOT / "expand" / "log.md"

SIGNS = {
    "collect": None, "ingest": None, "lint": None,
    "scan-secrets": None, "weekly-report": None, "consistency": None,
}


def read_text(p):
    try:
        return p.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return p.read_text(encoding="utf-8", errors="replace")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workflow", required=True, help="失败的工作流名")
    ap.add_argument("--run-id", required=True, help="运行 ID（幂等键）")
    ap.add_argument("--branch", default="")
    ap.add_argument("--sha", default="")
    ap.add_argument("--url", default="")
    ap.add_argument("--classification", default="unknown",
                    choices=["context", "instruction", "workflow", "infra", "unknown"])
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    today = datetime.date.today().isoformat()
    section = (
        f"## [{today}] feedback | 失败反馈：{args.workflow}\n\n"
        f"- 运行：{args.workflow}（id {args.run_id}{'，分支 ' + args.branch if args.branch else ''}"
        f"{'@' + args.sha[:7] if args.sha else ''}）\n"
        f"- 链接：{args.url or '（未提供）'}\n"
        f"- 信号分类：`{args.classification}`\n"
        f"- 处理建议：见 `scripts/gc_report.py` 或人工复盘后，把根因补齐到本条\n\n"
    )

    if args.dry_run:
        print(section)
        return 0

    text = read_text(LOG)
    # 幂等：该 run_id 已存在则跳过
    if f"id {args.run_id}" in text:
        print(f"已存在 run_id={args.run_id}，跳过")
        return 0

    marker = "> 时间倒序排列\n"
    if marker in text:
        text = text.replace(marker, marker + "\n" + section, 1)
    else:
        text = section + text
    LOG.write_text(text, encoding="utf-8")
    print("feedback 已追加到 expand/log.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())