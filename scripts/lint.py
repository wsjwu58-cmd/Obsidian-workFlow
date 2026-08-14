#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""知识库每日巡检（Lint）：
1. 断链检查：[[链接]] 是否可解析到 wiki/ 下的 .md 文件
2. 孤立节点：没有任何其他条目链接到它
3. 重复检测：内容相似度 >= 0.85 的条目对
4. 积压检查：references/raw/ 中 pending 素材超时未处理
5. index 同步：每个条目是否出现在 index.md
6. 空笔记提示：正文过短的条目
输出：Markdown 报告 + 可选 issue 文件；--log 时追加摘要到 wiki/log.md。
仅依赖标准库，可在 Actions（Linux）与本地（Windows）直接运行。
"""
import argparse
import datetime
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
EXPAND = ROOT / "expand"
RAW = ROOT / "references" / "raw"

# 基础设施文件不计入孤立/同步检查
INFRA = {"index.md", "log.md", "知识图谱.md", "AGENTS.md",
         "自动化工作流设计.md", "自动化工作流功能与实现方案.md"}
INFRA |= {"动态索引.md", "知识库周报.md"}
LINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]*)?\]\]")
FM_RE = re.compile(r"^---\s*$(.*?)^---\s*$", re.M | re.S)


def index_rel_candidates(p: pathlib.Path) -> list[str]:
    """index.md 可能用 stem 或 wiki/expand 相对路径链接。"""
    cands = [p.stem]
    for base in (WIKI, EXPAND, ROOT):
        try:
            rel = str(p.relative_to(base)).replace("\\", "/").removesuffix(".md")
            if rel and rel not in cands:
                cands.append(rel)
        except ValueError:
            continue
    return cands


def read_text(p: pathlib.Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return p.read_text(encoding="utf-8", errors="replace")


def strip_code(s: str) -> str:
    s = re.sub(r"```.*?```", " ", s, flags=re.S)
    s = re.sub(r"`[^`\n]*`", " ", s)
    return s


def norm(s: str) -> str:
    return re.sub(r"[^0-9A-Za-z\u4e00-\u9fff]", "", strip_code(s).lower())


def frontmatter(text: str) -> dict:
    m = FM_RE.match(text)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip().lower()] = v.strip().strip("\"'")
    return fm


def wiki_md_files():
    files = [p for p in WIKI.rglob("*.md")]
    if EXPAND.exists():
        files += [p for p in EXPAND.rglob("*.md")]
    return files


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", default=".lint-report.md")
    ap.add_argument("--issues", default=".lint-issues.md")
    ap.add_argument("--log", default=None, help="expand/log.md 路径，传入则追加巡检摘要")
    args = ap.parse_args()

    files = wiki_md_files()
    by_name = {}
    for p in files:
        by_name.setdefault(p.stem, []).append(p)

    report = []
    issues = []
    today = datetime.date.today().isoformat()

    # ---- 1. 断链检查 ----
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
            broken.append((str(p.relative_to(ROOT)), target.strip()))
    report.append(f"## 1. 断链检查：共 {len(broken)} 处")
    for path, target in broken[:30]:
        report.append(f"- `{path}` → [[{target}]] 无法解析")
    if broken:
        issues.append(f"### 断链 {len(broken)} 处")
        for path, target in broken[:30]:
            issues.append(f"- `{path}` → [[{target}]]")

    # ---- 2. 孤立节点 ----
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
    orphans = [p for p in files if incoming[str(p)] == 0 and p.name not in INFRA]
    report.append(f"\n## 2. 孤立节点（无入链）：{len(orphans)} 个")
    for p in sorted(orphans):
        report.append(f"- `{p.relative_to(ROOT)}`")

    # ---- 3. 重复检测（4-gram Jaccard 相似度）----
    dups = []
    shingle_sets = []
    for p in files:
        if p.name in INFRA:
            continue
        n = norm(read_text(p))
        if len(n) < 300:
            continue
        shingles = set()
        for k in range(len(n) - 3):
            shingles.add(n[k:k + 4])
        shingle_sets.append((p, shingles))
    for i in range(len(shingle_sets)):
        p1, s1 = shingle_sets[i]
        for j in range(i + 1, len(shingle_sets)):
            p2, s2 = shingle_sets[j]
            if not 0.5 < len(s1) / len(s2) < 2.0:
                continue
            inter = len(s1 & s2)
            union = len(s1 | s2)
            if union and inter / union >= 0.75:
                ratio = round(inter / union, 3)
                dups.append((p1, p2, round(ratio, 3)))
    report.append(f"\n## 3. 重复检测（4-gram Jaccard ≥ 0.75）：{len(dups)} 对")
    for p1, p2, r in dups[:20]:
        report.append(f"- `{p1.relative_to(ROOT)}` ↔ `{p2.relative_to(ROOT)}`（{r}）")
    if dups:
        issues.append(f"### 疑似重复 {len(dups)} 对")
        for p1, p2, r in dups[:20]:
            issues.append(f"- `{p1.relative_to(ROOT)}` ↔ `{p2.relative_to(ROOT)}`（{r}）")

    # ---- 4. 积压检查 ----
    pending = stale_24 = stale_7 = 0
    if RAW.exists():
        for p in RAW.rglob("*.md"):
            fm = frontmatter(read_text(p))
            if fm.get("status", "").lower() == "pending":
                pending += 1
                c = fm.get("collected", "")
                if c:
                    try:
                        age = (datetime.date.today() - datetime.date.fromisoformat(c)).days
                        if age >= 7:
                            stale_7 += 1
                        elif age >= 1:
                            stale_24 += 1
                    except ValueError:
                        pass
    report.append(f"\n## 4. 积压检查：pending={pending}（>24h: {stale_24}，>7d: {stale_7}）")
    if stale_7:
        issues.append(f"### 积压告警：references/raw/ 有 {stale_7} 条素材超过 7 天未处理")

    # ---- 5. index 同步 ----
    idx = read_text(EXPAND / "index.md")
    missing = []
    for p in files:
        if p.name in INFRA:
            continue
        if any(f"[[{rel}]]" in idx for rel in index_rel_candidates(p)):
            continue
        missing.append(p)
    report.append(f"\n## 5. index 同步：{len(missing)} 个条目未出现在 index.md")
    for p in sorted(missing):
        report.append(f"- `{p.relative_to(ROOT)}`")

    # ---- 6. 空笔记提示 ----
    empties = []
    for p in files:
        if p.name in INFRA:
            continue
        body = re.sub(r"^---.*?---", "", read_text(p), flags=re.S)
        content_len = len(re.sub(r"[^0-9A-Za-z\u4e00-\u9fff]", "", body.lower()))
        if content_len < 80:
            empties.append(p)
    report.append(f"\n## 6. 空笔记/超短条目提示：{len(empties)} 个")
    for p in sorted(empties):
        report.append(f"- `{p.relative_to(ROOT)}`")

    # ---- 汇总 ----
    summary = (f"巡检时间：{today} | 条目数：{len(files)} | 断链：{len(broken)} | "
               f"孤立：{len(orphans)} | 重复对：{len(dups)} | pending：{pending} | "
               f"index 缺失：{len(missing)} | 空笔记：{len(empties)}")
    report.insert(0, f"# 巡检报告\n\n> {summary}\n")
    pathlib.Path(args.report).write_text("\n".join(report) + "\n", encoding="utf-8")
    if issues:
        pathlib.Path(args.issues).write_text("\n".join(issues) + "\n", encoding="utf-8")
    elif pathlib.Path(args.issues).exists():
        pathlib.Path(args.issues).unlink()

    if args.log:
        log_p = ROOT / args.log
        log = read_text(log_p)
        section = f"## [{today}] lint | 巡检报告\n\n- {summary}\n"
        if issues:
            heads = "；".join(i.splitlines()[0].lstrip("# ").strip() for i in issues)
            section += f"- ⚠️ 发现异常：{heads}\n\n"
        else:
            section += "\n"
        marker = "> 时间倒序排列\n"
        if marker in log:
            log = log.replace(marker, marker + "\n" + section, 1)
        else:
            log = section + log
        log_p.write_text(log, encoding="utf-8")

    print(summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
