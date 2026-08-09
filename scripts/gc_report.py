#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""熵管理 / 垃圾回收 Agent（GC，Track 2）。

借鉴 harness-engineering 的「熵管理与垃圾回收」理念：
- 人类品味一旦编码为规则，就持续应用于每一条目（Golden Rules）
- 定期后台任务扫描偏差 → 更新质量评分 → 给出建议（小步偿还技术债）

本脚本不直接删除/改写任何文件，只产出**建议清单**（.gc-report.md），
由人工（或后续 AI GC 会话）执行。这与参考仓库"大多数需人工审查"一致。

检测维度（数值由 --min- 参数控制）：
  1. 孤立节点：无任何入链的条目（建议：移除或补链接）
  2. 疑似重复：内容相似度高的一对条目（建议：合并去重）
  3. 空笔记：正文过短的条目（建议：补全或移除）
  4. 过期条目：updated 字段距今天超过 N 天的条目（建议：标记过时/重访）
  5. 待办积压：references/raw/ pending 超过 N 天的素材（建议：加工或拒绝）
  6. 断链/死链：指向不存在条目的 [[链接]]（建议：修复引用）
  7. 未完成行动：列表中未勾选的 [[任务]]（建议：重访或移除）

仅依赖标准库，可在 Actions（Linux）与本地（Windows）运行。
"""
import argparse
import datetime
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
EXPAND = ROOT / "expand"
RAW = ROOT / "references" / "raw"

INFRA = {"index.md", "log.md", "知识图谱.md",
         "自动化工作流设计.md", "自动化工作流功能与实现方案.md",
         "动态索引.md", "知识库周报.md"}

LINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]*)?\]\]")
FM_RE = re.compile(r"^---\s*$(.*?)^---\s*$", re.M | re.S)


def read_text(p):
    try:
        return p.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return p.read_text(encoding="utf-8", errors="replace")


def frontmatter(text):
    m = FM_RE.match(text)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip().lower()] = v.strip().strip("\"'")
    return fm


def norm(s):
    s = re.sub(r"```.*?```", " ", s, flags=re.S)
    s = re.sub(r"`[^`\n]*`", " ", s)
    return re.sub(r"[^0-9A-Za-z\u4e00-\u9fff]", "", s.lower())


def strip_code(s):
    s = re.sub(r"```.*?```", " ", s, flags=re.S)
    return re.sub(r"`[^`\n]*`", " ", s)


def collect_files():
    files = [p for p in WIKI.rglob("*.md")]
    if EXPAND.exists():
        files += [p for p in EXPAND.rglob("*.md")]
    return files


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", default=".gc-report.json",
                    help="建议清单输出路径（JSON）")
    ap.add_argument("--markdown", default=".gc-report.md",
                    help="人类可读报告输出路径（Markdown）")
    ap.add_argument("--issue", default=".gc-issues.md",
                    help="仅含 high 项的 Issue 正文路径（无 high 时为空文件）")
    ap.add_argument("--orphan-threshold", type=int, default=0,
                    help="孤立节点入链数阈值，小于等于该值视为孤立（默认 0）")
    ap.add_argument("--empty-len", type=int, default=80,
                    help="正文有效字符数低于此值视为空笔记（默认 80）")
    ap.add_argument("--stale-days", type=int, default=90,
                    help="updated 距今超过该天数视为过期（默认 90）")
    ap.add_argument("--pending-days", type=int, default=7,
                    help="pending 素材超过该天数视为积压（默认 7）")
    args = ap.parse_args()

    files = collect_files()
    by_name = {}
    for p in files:
        by_name.setdefault(p.stem, []).append(p)

    today = datetime.date.today()
    suggestions = []  # [{kind, path, reason, action, severity}]

    def rel(p):
        return str(p.relative_to(ROOT)).replace("\\", "/")

    # ---- 1. 孤立节点 ----
    incoming = {str(p): 0 for p in files}
    for p in files:
        text = strip_code(read_text(p))
        for target in LINK_RE.findall(text):
            t = target.strip()
            if t.endswith(".md"):
                t = t[:-3]
            base = t.split("/")[-1]
            for q in by_name.get(base, []):
                incoming[str(q)] += 1
    for p in files:
        if p.name in INFRA:
            continue
        if incoming[str(p)] <= args.orphan_threshold:
            suggestions.append({
                "kind": "orphan", "path": rel(p), "severity": "low",
                "reason": "孤立节点（无入链或被链接少于 %d 次）" % (args.orphan_threshold + 1),
                "action": "补知识图谱入链，或移除另部分孤立条目",
            })

    # ---- 2. 疑似重复（4-gram Jaccard）----
    shingles = []
    for p in files:
        if p.name in INFRA:
            continue
        n = norm(read_text(p))
        if len(n) < 300:
            continue
        s = set()
        for k in range(len(n) - 3):
            s.add(n[k:k + 4])
        shingles.append((p, s))
    for i in range(len(shingles)):
        p1, s1 = shingles[i]
        for j in range(i + 1, len(shingles)):
            p2, s2 = shingles[j]
            if not 0.5 < len(s1) / len(s2) < 2.0:
                continue
            inter = len(s1 & s2)
            union = len(s1 | s2)
            if union and inter / union >= 0.7:
                suggestions.append({
                    "kind": "重复候选", "path": rel(p1), "severity": "medium",
                    "reason": "与 [%s] 内容高度相似（Jaccard=%.2f）"
                             % (rel(p2), inter / union),
                    "action": "人工核对去重，选择一个保留并建立 [[别名]] 链接",
                })

    # ---- 3. 空笔记 ----
    for p in files:
        if p.name in INFRA:
            continue
        body = re.sub(r"^---.*?---", "", read_text(p), flags=re.S)
        content_len = len(re.sub(r"[^0-9A-Za-z\u4e00-\u9fff]", "", body.lower()))
        if content_len < args.empty_len:
            suggestions.append({
                "kind": "空笔记", "path": rel(p), "severity": "low",
                "reason": "正文有效字符仅 %d（< %d）" % (content_len, args.empty_len),
                "action": "补全内容，或从 index/知识图谱移除",
            })

    # ---- 3. 过期条目 ----
    for p in files:
        if p.name in INFRA:
            continue
        fm = frontmatter(read_text(p))
        upd = fm.get("updated", "")
        if not upd:
            continue
        try:
            d = datetime.date.fromisoformat(upd)
        except ValueError:
            continue
        age = (today - d).days
        if age > args.stale_days:
            suggestions.append({
                "kind": "过期", "path": rel(p), "severity": "low",
                "reason": "updated=%s 距今 %d 天（> %d）" % (upd, age, args.stale_days),
                "action": "重访确认是否仍有效，过时则更新或标记废弃",
            })

    # ---- 4. 断链 ----
    broken = []
    for p in files:
        text = strip_code(read_text(p))
        for target in LINK_RE.findall(text):
            t = target.strip()
            if t.endswith(".md"):
                t = t[:-3]
            if not t:
                continue
            base = t.split("/")[-1]
            if base in by_name:
                continue
            if any(str(f).replace("\\", "/").endswith(t + ".md") for f in files):
                continue
            broken.append((rel(p), target.strip()))
    for path, target in broken:
        suggestions.append({
            "kind": "断链", "path": path, "severity": "high",
            "reason": "[[%s]] 无法解析到任何条目" % target,
            "action": "创建目标条目，或改链为已存在条目",
        })

    # ---- 5. 积压待办 ----
    if RAW.exists():
        for p in RAW.rglob("*.md"):
            if p.name == "README.md":
                continue
            fm = frontmatter(read_text(p))
            if fm.get("status", "").lower() != "pending":
                continue
            c = fm.get("collected", "")
            age = 0
            if c:
                try:
                    age = (today - datetime.date.fromisoformat(c)).days
                except ValueError:
                    pass
            if age > args.stale_days:
                suggestions.append({
                    "kind": "积压", "path": rel(p), "severity": "medium",
                    "reason": "status=pending %d 天未处理" % age,
                    "action": "加工该素材，或标 rejected / 删除",
                })

    # ---- 严重度排序 ----
    sev = {"high": 0, "medium": 1, "low": 2}
    suggestions.sort(key=lambda s: sev.get(s["severity"], 3))

    report = {
        "generated": today.isoformat(),
        "counts": {
            spec: sum(1 for s in suggestions if s["kind"] == spec)
            for spec in ("条目", "重复候选", "空笔记", "过期", "断链", "积压")
        },
        "total": len(suggestions),
        "suggestions": suggestions,
    }
    pathlib.Path(args.report).write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        f"# GC 建议清单（{today.isoformat()}）",
        "",
        f"> 共 {len(suggestions)} 项待处理。源：`{args.report}`（JSON 结构化供 agent 消费）",
        "",
    ]
    for s in suggestions:
        lines.append(f"- [{s['severity']}] **{s['kind']}** `{s['path']}`")
        lines.append(f"  - 原因：{s['reason']}")
        lines.append(f"  - 建议：{s['action']}")
    pathlib.Path(args.markdown).write_text("\n".join(lines) + "\n", encoding="utf-8")

    high_only = [s for s in suggestions if s["severity"] == "high"]
    if high_only:
        issue_lines = [f"# GC 高风险项（{today.isoformat()}）", "",
                       f"共 {len(high_only)} 项（断链/必须修复类）：", ""]
        for s in high_only:
            issue_lines.append(f"- **{s['kind']}** `{s['path']}`")
            issue_lines.append(f"  - {s['reason']} → 建议：{s['action']}")
    else:
        issue_lines = []
    pathlib.Path(args.issue).write_text("\n".join(issue_lines) + "\n", encoding="utf-8")

    print(json.dumps(report["counts"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())