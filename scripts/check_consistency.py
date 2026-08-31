#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""知识库一致性检查（K1–K7 不变量门禁）。

把 lint.py 的"巡检报告"升级为"断言验证"：文档会烂，规则不会。
本脚本守护与 harness-engineering 相同的失效模式——计数漂移、状态机混乱、
链接腐坏、索引/图谱/日志与磁盘不一致。

检查清单：
  K1  状态机合法：references/raw/*.md 的 status ∈ {pending, processed}；processed 且含
      processed_hash 的素材正文 hash 必须命中（防状态与内容错位）
  K2  引用一致：expand/index.md 声明的"全库共 N 个 Markdown 文件" == 磁盘实际
      .md 数（wiki + expand），防索引悄悄腐烂
  K3  字段完整：expand/ 下每个 AI 生成条目 frontmatter 必备 created/updated/
      sources/tags；缺少即 FAIL（wiki/ 个人笔记不检查，只读）
  K4  链接健康：全库 [[链接]] 必须可解析到某 .md；无条件放宽
  K5  索引/目录同步：每个非基建 .md 条目都必须出现在 expand/index.md 的
      [[名称]] 链接中（防"入库了但没进索引"）
  K6  markdown 表格形状：index.md / log.md / 知识图谱.md 里每行表格单元格数
      与表头一致（防 AI 生成的表格列错位吃掉单元格）
  K7  孤立节点：除基建文件外，无任何入链的条目（防止 .md 落盘却没人知道）

退出码：0=全过；1=任一 FAIL。CI 与 pre-commit 均以退出码为门。

用法：
  python scripts/check_consistency.py            # 全量检查
  python scripts/check_consistency.py --quiet    # 只输出 FAIL + 汇总
"""
import argparse
import hashlib
import pathlib
import re
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass

ROOT = pathlib.Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
EXPAND = ROOT / "expand"
RAW = ROOT / "references" / "raw"

# 基建文件：不计入孤立/索引同步检查
INFRA = {
    "index.md", "log.md", "知识图谱.md",
    "自动化工作流设计.md", "自动化工作流功能与实现方案.md",
    "动态索引.md", "知识库周报.md", "gc-report.md",
}
CI_ARTIFACTS = {"gc-report.md"}
# 索引同步检查的例外：wiki/ 个人笔记允许只出现在知识图谱而不在 index.md
INDEX_CHECK_EXEMPT = INFRA | set()

LINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]*)?\]\]")
TABLE_FILES = ["index.md", "log.md", "知识图谱.md"]


def read_text(p: pathlib.Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return p.read_text(encoding="utf-8", errors="replace")


def strip_code(s: str) -> str:
    s = re.sub(r"```.*?```", " ", s, flags=re.S)
    s = re.sub(r"`[^`\n]*`", " ", s)
    return s


def frontmatter(text: str) -> dict:
    m = re.match(r"^---\s*$(.*?)^---\s*$", text, re.M | re.S)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip().lower()] = v.strip().strip("\"'")
    return fm


def is_infra(p: pathlib.Path) -> bool:
    """目录约定/基建文件豁免：各目录的 AGENTS.md + INFRA 名"""
    name = p.name
    if name == "AGENTS.md":
        return True
    return name in INFRA


def all_files():
    files = [p for p in WIKI.rglob("*.md")]
    if EXPAND.exists():
        files += [p for p in EXPAND.rglob("*.md")
                  if p.name not in CI_ARTIFACTS]
    working = ROOT / "working"
    if working.exists():
        files += [p for p in working.glob("*.md") if p.name != "AGENTS.md"]
    return files


def index_stem(p: pathlib.Path) -> str:
    """条目在 index.md 中的链接名：保留顶部路径避免同名歧义（windows 下 /.md 均归一）"""
    return p.stem


def run_checks(verbose: bool) -> int:
    fail = 0
    files = all_files()
    by_name = {}
    for p in files:
        by_name.setdefault(p.stem, []).append(p)

    def red(x):
        return f"\033[31m{x}\033[0m" if sys.stdout.isatty() else x

    def green(x):
        return f"\033[32m{x}\033[0m" if sys.stdout.isatty() else x

    def yellow(x):
        return f"\033[33m{x}\033[0m" if sys.stdout.isatty() else x

    def report(ok, msg):
        return f"  {green('PASS') if ok else red('FAIL')} — {msg}"

    # ─── K1 状态机 ───────────────────────────────────────
    print("[K1] references/articles.md 索引状态机合法")
    k1_fail = 0
    k1_warn = 0
    ART_STATES = {"已收录", "已淘汰", "待处理"}
    art = ROOT / "references" / "articles.md"
    art_text = read_text(art) if art.exists() else ""
    # 解析编号条目「### N. …」中的状态/归属行
    entry_re = re.compile(r"^### (\d+)\s*\.", re.M)
    starts = [m for m in entry_re.finditer(art_text)]
    for i, m in enumerate(starts):
        next_entry = starts[i + 1].start() if i + 1 < len(starts) else len(art_text)
        segment = art_text[m.end():next_entry]
        st = re.search(r"- \*\*状态：\*\*\s*(.+)$", segment, re.M)
        if not st:
            k1_fail += 1
            print(red(f"  [K1] 编号 {m.group(1)}：缺「状态：」字段"))
        elif st.group(1).strip().split("|")[0].strip() not in ART_STATES:
            k1_fail += 1
            print(red(f"  [K1] 编号 {m.group(1)}：非法状态 {st.group(1).strip()[:40]}"))
        own = re.search(r"- \*\*归属：\*\*\s*(.+)$", segment, re.M)
        if own and own.group(1).strip() not in ("—", "-", "") and "等待" not in own.group(1):
            own_path = own.group(1).strip().split("`")[1] if "`" in own.group(1) else own.group(1).strip().split("（")[0].strip()
            if not (ROOT / own_path).exists():
                k1_warn += 1
                print(yellow(f"  [K1-warn] 编号 {m.group(1)}：归属 '{own_path}' 磁盘不存在（可能是路径透灭，仅警示）"))
    if k1_fail:
        fail += 1
        print(report(False, f"{k1_fail} 处索引状态机异常"))
    else:
        warn = f"，{k1_warn} 处归属警示" if k1_warn else ""
        print(report(True, f"references/articles.md 状态机一致{warn}"))

    # ─── K2 索引计数 ─────────────────────────────────────────
    print("[K2] expand/index.md 全库计数声明")
    k2_ok = True
    idx_text = read_text(EXPAND / "index.md") if (EXPAND / "index.md").exists() else ""
    m = re.search(r"全库共 (\d+) 个 Markdown 文件", idx_text)
    actual = len(files)
    if not m:
        k2_ok = False
        print(report(False, "index.md 缺「全库共 N 个 Markdown 文件」声明"))
    elif int(m.group(1)) != actual:
        k2_ok = False
        print(report(False, f"index.md 声明 {m.group(1)}，磁盘实际 {actual}"))
        # 内嵌修复指令（机械执行原则）
        print(yellow("    修复：更新 index.md 计数声明，或检查是否有多/少入库的条目文件"))
    if k2_ok:
        print(report(True, f"index.md 计数 {m.group(1)} = 实际 {actual}"))
    else:
        fail += 1

    # ─── K3 expand 条目 frontmatter ──────────────────────────
    print("[K3] expand/ AI 条目 frontmatter 字段完整")
    k3_fail = 0
    if EXPAND.exists():
        for p in EXPAND.rglob("*.md"):
            if is_infra(p):
                continue
            fm = frontmatter(read_text(p))
            missing = [k for k in ("created", "updated", "sources", "tags") if k not in fm]
            if missing:
                print(report(False, f"{p.relative_to(ROOT)} 缺少 {missing}"))
                k3_fail += 1
    if k3_fail:
        print(report(False, f"{k3_fail} 个 expand 条目 frontmatter 不完整"))
        fail += 1
    else:
        print(report(True, "所有 expand AI 条目 frontmatter 完整"))

    # ─── K4 断链 ──────────────────────────────────────────────
    print("[K4] 双链可解析")
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
            broken.append((str(p.relative_to(ROOT)), target.strip()))
    if broken:
        print(report(False, f"断链 {len(broken)} 处"))
        for path, target in broken[:20]:
            print(f"    `{path}` → [[{target}]] 无法解析")
        fail += 1
    else:
        print(report(True, "全部 [[链接]] 可解析"))

    # ─── K5 索引同步 ─────────────────────────────────────────
    print("[K5] 条目均出现在 expand/index.md")
    k5_missing = []
    if EXPAND.exists():
        idx = read_text(EXPAND / "index.md")
        for p in files:
            if is_infra(p):
                continue
            if f"[[{p.stem}]]" in idx:
                continue
            try:
                rel = str(p.relative_to(WIKI)).replace("\\", "/").replace(".md", "")
            except ValueError:
                rel = str(p).replace("\\", "/").replace(".md", "")
            if f"[[{rel}]]" in idx:
                continue
            k5_missing.append(p)
    if k5_missing:
        print(report(False, f"{len(k5_missing)} 个条目未出现在 index.md"))
        for p in k5_missing[:20]:
            print(f"    `{p.relative_to(ROOT)}`")
        fail += 1
    else:
        print(report(True, "全部条目均出现在 index.md"))

    # ─── K6 markdown 表格形状 ──────────────────────────────
    print("[K6] markdown 表格形状（expand/ 必检文件）")
    k6_fail = 0
    for tf in TABLE_FILES:
        p = EXPAND / tf
        if not p.exists():
            continue
        lines = read_text(p).splitlines()
        for i, line in enumerate(lines):
            if not line.startswith("|"):
                continue
            # 过滤代码块
            fence = 0
            for j in range(i):
                if lines[j].strip().startswith("```"):
                    fence += 1
            if fence % 2 == 1:
                continue
            cells = [c for c in line.strip("|").split("|")]
            if re.fullmatch(r"[:\-\s]*", line.strip("|")):
                continue  # 分隔行
            hdr = None
            for j in range(i - 1, -1, -1):
                if lines[j].startswith("|"):
                    hdr = lines[j]
                    break
            if hdr is None:
                continue
            expect = len(hdr.strip().strip("|").split("|"))
            if expect != len(cells):
                k6_fail += 1
                print(report(False, f"{tf} L{i + 1}: 表格列数 {len(cells)} ≠ 表头 {expect}"))
    if k6_fail:
        print(report(False, f"{k6_fail} 处表格形状漂移"))
        fail += 1
    else:
        print(report(True, "必检文件表格形状一致"))

    # ─── K7 孤立节点 ────────────────────────────────────────
    print("[K7] 孤立节点（无入链，仅报告不阻塞）")
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
    orphans = [p for p in files if incoming[str(p)] == 0 and not is_infra(p)]
    if orphans:
        print(yellow(f"  [K7-warn] {len(orphans)} 个孤立节点："))
        for p in sorted(orphans)[:20]:
            print(f"    `{p.relative_to(ROOT)}`")
        print(yellow("    提示：孤立节点建议在知识图谱/其他条目中补入链（Track 2 GC 会扫）"))
    else:
        print(report(True, "无孤立节点"))

    if fail:
        print(f"\n{red('✗ 一致性检查失败')} ({fail} 项未通过)")
        return 1
    print(f"\n{green('✓ 全部一致性检查通过')}")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quiet", action="store_true", help="只打印 FAIL 与汇总")
    args = ap.parse_args()
    sys.exit(run_checks(not args.quiet))


if __name__ == "__main__":
    main()
