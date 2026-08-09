#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""references 去重查询接口。

把 references/ 变为"持续输入的源头"：采集/追踪前查询 articles.md 去重权威，
判定给定 URL / 标题是否已收录。

用法：
  python scripts/retrack.py --url "https://x.com/y" [--check-repo]
  python scripts/retrack.py --title "Harness Engineering"
  python scripts/retrack.py --list            # 列出全部索引条目（供 collect/research 注入）

退出码：0 = 未收录（可收集）；1 = 已收录；2 = 索引不可读。
"""
import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ARTICLES = ROOT / "references" / "articles.md"

# articles.md 的索引表：每行   | # | 标题 | 作者/来源 | 日期 | 状态 | 去向 |
URL_PAT = r"https?://[^\s|]+"
ROW_PAT = re.compile(r"^\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|$", re.MULTILINE)


def read_index():
    if not ARTICLES.exists():
        sys.stderr.write("references/articles.md 不存在\n")
        return None
    try:
        return ARTICLES.read_text(encoding="utf-8")
    except OSError as e:
        sys.stderr.write(f"读取失败：{e}\n")
        return None


def all_urls(text):
    """从 articles.md 表格中提取所有行内 URL"""
    urls = set()
    for m in ROW_PAT.finditer(text):
        for col in m.groups():
            urls.update(re.findall(URL_PAT, col))
    return urls


def all_titles(text):
    return [m.group(2).lower().strip() for m in ROW_PAT.finditer(text)]


def raw_urls():
    """从 references/raw/*.md 的 frontmatter 提取 url（已采集/已加工素材的真实 URL）"""
    urls = set()
    raw_dir = ROOT / "references" / "raw"
    if raw_dir.exists():
        for p in raw_dir.glob("*.md"):
            m = re.search(r"(?m)^url:\s*(.+)$", p.read_text(encoding="utf-8", errors="ignore"))
            if m:
                urls.add(m.group(1).strip())
    return urls


def check(url="", title="", threshold=0.6):
    text = read_index()
    if text is None:
        return 2, "索引不可读"
    known_urls = all_urls(text) | raw_urls()
    known_titles = all_titles(text)
    hits = []
    if url and url in known_urls:
        return 1, "URL 已收录"
    if url:
        # 模糊：域名+路径主干匹配
        core = re.sub(r"^https?://", "", url).split("?")[0].strip("/")
        for u in known_urls:
            u_core = re.sub(r"^https?://", "", u).split("?")[0].strip("/")
            if u_core == core and core:
                return 1, "URL（归一化）已收录"
    if title:
        tl = title.lower().strip()
        for t in all_titles(text):
            if t and (tl in t or t in tl):
                return 1, f"标题近似匹配：{t}"
        # 模糊 Jaccard
        set_t = set(tl.replace(" ", ""))
        for t in all_titles(text):
            st = set(t.replace(" ", ""))
            if st and len(set_t & st) / max(len(set_t), len(st)) >= threshold:
                return 1, f"标题模糊匹配：{t}"
    return 0, "未收录，可收集"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="")
    ap.add_argument("--title", default="")
    ap.add_argument("--threshold", type=float, default=0.4,
                    help="标题 jaccard 相似度阈值（默认 0.4）")
    ap.add_argument("--list", action="store_true", help="输出全部已收录 URL")
    args = ap.parse_args()

    if args.list:
        text = read_index()
        if text is None:
            return 2
        for u in sorted(all_urls(text)):
            print(u)
        return 0

    if not args.url and not args.title:
        ap.print_usage()
        return 2

    code, msg = check(args.url, args.title, args.threshold)
    print(msg)
    return code


if __name__ == "__main__":
    sys.exit(main())