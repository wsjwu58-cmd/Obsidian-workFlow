#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""知识库周报（F08）。

汇总最近 7 天：
- 新增/更新条目（解析 expand/log.md 的 ingest / maintenance 记录）
- 采集量（references/raw/ 中 collected 在窗口内、status=processed/rejected 的数量）
- 通过率（processed / (processed + rejected)）
- 积压（pending 数量与超时）
- 链接健康度 / 孤立 / 重复 / 空笔记（运行 lint.py 获取最新巡检结果）

输出：追加「本周周报」章节到 expand/知识库周报.md。
仅依赖标准库，可在 Actions（Linux）与本地（Windows）直接运行。
"""
import argparse
import datetime
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
EXPAND = ROOT / "expand"
RAW = ROOT / "references" / "raw"
LOG = EXPAND / "log.md"
REPORT = EXPAND / "知识库周报.md"
LINT_REPORT = ROOT / ".lint-report.md"
WINDOW_DAYS = 7


def read_text(p):
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8", errors="replace")


def parse_fm(text):
    m = re.match(r"^---\s*$(.*?)^---\s*$", text, re.S | re.M)
    fm = {}
    if not m:
        return fm, text
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip().lower()] = v.strip().strip("\"'")
    return fm, text[m.end():]


def run_lint():
    """重新生成 .lint-report.md，返回摘要行文本"""
    script = ROOT / "scripts" / "lint.py"
    subprocess.run([sys.executable, str(script), "--report", str(LINT_REPORT)],
                   cwd=ROOT, capture_output=True, text=True)
    for line in read_text(LINT_REPORT).splitlines():
        if line.startswith("> 巡检时间"):
            return line.strip("> ").strip()
    return ""


def log_events(days):
    """解析 log.md，返回窗口内的 [(日期, 类型, 章节文本)]"""
    text = read_text(LOG)
    events = []
    today = datetime.date.today()
    for m in re.finditer(r"^## \[(\d{4}-\d{2}-\d{2})\] (.+)$", text, re.M):
        try:
            date = datetime.date.fromisoformat(m.group(1))
        except ValueError:
            continue
        if (today - date).days >= days:
            continue
        nxt = re.search(r"^## \[", text[m.end():], re.M)
        section = text[m.end(): m.end() + (nxt.start() if nxt else len(text))]
        events.append((date, m.group(2).strip(), section.strip()))
    return events


def raw_stats(days):
    today = datetime.date.today()
    processed = rejected = pending = 0
    names = []
    for p in RAW.rglob("*.md"):
        if p.name == "README.md":
            continue
        fm, _ = parse_fm(read_text(p))
        c = fm.get("collected", "")
        try:
            age = (today - datetime.date.fromisoformat(c)).days
        except ValueError:
            continue
        if age >= days:
            continue
        st = fm.get("status", "").lower()
        if st == "processed":
            processed += 1
        elif st == "rejected":
            rejected += 1
        elif st == "pending":
            pending += 1
        names.append(p.name)
    return processed, rejected, pending, sorted(names)


def count_links(section, prefix):
    return len(re.findall(rf"^- {re.escape(prefix)}.*?\[\[", section, re.M))


def parse_lint_summary(summary):
    out = {}
    if not summary:
        return out
    for key in ("断链", "孤立", "重复对", "pending", "index 缺失", "空笔记"):
        m = re.search(rf"{key}[:：]\s*(\d+)", summary)
        if m:
            out[key] = int(m.group(1))
    return out


def build_report(events, proc, rej, pend, names, lint_summary):
    today = datetime.date.today()
    iso = today.isocalendar()
    start = today - datetime.timedelta(days=WINDOW_DAYS - 1)

    new_entries = sum(count_links(s, "新增") for _, _, s in events)
    upd_entries = sum(count_links(s, "更新") for _, _, s in events)
    total = proc + rej
    pass_rate = f"{proc / total * 100:.0f}%" if total else "—"

    lines = [f"## 第 {iso[0]}-W{iso[1]:02d} 周报（{start} ~ {today}）", ""]
    lines.append(f"> 生成时间：{today}  |  数据窗口：最近 {WINDOW_DAYS} 天")
    lines.append("")
    lines.append("### 本周概览")
    lines.append("")
    lines.append("| 指标 | 数值 |")
    lines.append("| --- | --- |")
    lines.append(f"| 新增条目 | {new_entries} |")
    lines.append(f"| 更新条目 | {upd_entries} |")
    lines.append(f"| 采集素材（窗口内） | {total}（processed {proc} / rejected {rej}） |")
    lines.append(f"| 通过率 | {pass_rate} |")
    lines.append(f"| 当前 pending（references/raw/） | {pend} |")
    for k, v in lint_summary.items():
        lines.append(f"| 巡检：{k} | {v} |")
    lines.append("")
    lines.append("### 本周 ingest / 维护记录")
    lines.append("")
    if events:
        for date, title, section in events:
            head = next((ln.strip("- ") for ln in section.splitlines()
                         if ln.strip().startswith("- ")), "")
            lines.append(f"- [{date}] {title}")
            if head:
                lines.append(f"  - {head}")
    else:
        lines.append("- 无")
    lines.append("")
    lines.append("### 本周采集素材")
    lines.append("")
    if names:
        for n in names:
            lines.append(f"- `{n}`")
    else:
        lines.append("- 无")
    lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=WINDOW_DAYS)
    args = ap.parse_args()

    events = log_events(args.days)
    proc, rej, pend, names = raw_stats(args.days)
    lint_summary = parse_lint_summary(run_lint())
    section = build_report(events, proc, rej, pend, names, lint_summary)

    text = read_text(REPORT)
    marker = "> 时间倒序排列（最新在上）\n"
    if text:
        if marker in text:
            text = text.replace(marker, marker + "\n" + section + "\n", 1)
        else:
            text = section + "\n" + text
    else:
        text = ("---\ncreated: 2026-08-04\nupdated: 2026-08-04\n"
                "tags: [知识库, 周报]\n---\n\n# 知识库周报\n\n"
                f"{marker}\n{section}\n")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(text, encoding="utf-8")
    print(f"周报已生成：{REPORT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
