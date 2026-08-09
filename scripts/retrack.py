#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""references 去重查询接口（适配 harness 格式 articles.md）。

把 references/ 变为"持续输入的源头"：采集/追踪前查询 articles.md 去重权威，
判定给定 URL / 标题是否已收录（含已淘汰，防止重复采集）。

用法：
  python scripts/retrack.py --url "https://x.com/y"
  python scripts/retrack.py --title "Harness Engineering"
  python scripts/retrack.py --list            # 列出全部索引条目（供 collect/research 注入）

退出码：0 = 未收录（可收集）；1 = 已收录（含已淘汰）；2 = 索引不可读。
"""
import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ARTICLES = ROOT / "references" / "articles.md"

# articles.md 编号条目结构：
#   ### N. 标题
#   - **标题：** …
#   - **链接：** [x](url)
#   - **作者：** … | **日期：** …
#   - **状态：** 已收录 | **归属：** …
#   - **核心：** …
#   - **关联：** …
ENTRY_RE = re.compile(r"^### (\d+)\s*\.\s*(.+)$", re.M)
TITLE_FIELD_RE = re.compile(r"- \*\*标题：\*\*\s*(.+)$", re.M)
URL_FIELD_RE = re.compile(r"- \*\*链接：\*\*\s*\[[^\]]*\]\(([^)]+)\)", re.M)
STATE_FIELD_RE = re.compile(r"- \*\*状态：\*\*\s*([^|]+)", re.M)


def read_articles():
    if not ARTICLES.exists():
        sys.stderr.write("references/articles.md 不存在\n")
        return None
    try:
        return ARTICLES.read_text(encoding="utf-8")
    except OSError as e:
        sys.stderr.write(f"读取失败：{e}\n")
        return None


def parse_entries(text):
    """解析编号正文条目 -> [(编号, 标题, url, 状态, 归属)]。

    「## 待处理」队列中的占位行不计入；待处理队列用独立标记行表示，不写 ### 编号。
    """
    out = []
    starts = list(ENTRY_RE.finditer(text))
    for i, m in enumerate(starts):
        nxt = starts[i + 1].start() if i + 1 < len(starts) else len(text)
        seg = text[m.end():nxt]
        num = int(m.group(1))
        tm = TITLE_FIELD_RE.search(seg)
        title = tm.group(1).strip() if tm else m.group(2).strip()
        um = URL_FIELD_RE.search(seg)
        url = um.group(1).strip() if um else ""
        sm = STATE_FIELD_RE.search(seg)
        state = sm.group(1).strip() if sm else ""
        om = re.search(r"\*\*归属：\*\*\s*(.+)", seg, re.M)
        belong = om.group(1).strip() if om else ""
        out.append((num, title, url, state, belong))
    return out


def check(url="", title="", threshold=0.6):
    text = read_articles()
    if text is None:
        return 2, "索引不可读"
    entries = parse_entries(text)
    known_urls = {e[2] for e in entries if e[2]}
    known_titles = [e[1] for e in entries]

    if url:
        for u in known_urls:
            if u == url or u.rstrip("/").split("?")[0] == url.rstrip("/").split("?")[0]:
                return 1, f"URL 已收录：{u}"
        core = re.sub(r"^https?://", "", url).split("?")[0].rstrip("/")
        for u in known_urls:
            u_core = re.sub(r"^https?://", "", u).split("?")[0].rstrip("/")
            if u_core and u_core == core:
                return 1, f"URL（归一化）已收录：{u}"

    if title:
        tl = title.lower().strip()
        for t in known_titles:
            if t and tl and (tl in t.lower() or t.lower() in tl):
                return 1, f"标题近似匹配：{t}"
        set_t = set(re.sub(r"\W+", "", tl))
        for t in known_titles:
            st = set(re.sub(r"\W+", "", t.lower()))
            if set_t and st:
                sim = len(set_t & st) / max(len(set_t), len(st))
                if sim >= threshold:
                    return 1, f"标题模糊匹配：{t}"
    return 0, "未收录，可收集"


def list_all(text):
    out = []
    for num, title, url, state, _bl in parse_entries(text):
        out.append(f"[{num:02d}] {title} | {url} | {state}")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="")
    ap.add_argument("--title", default="")
    ap.add_argument("--threshold", type=float, default=0.4,
                    help="标题 jaccard 相似度阈值（默认 0.4）")
    ap.add_argument("--list", action="store_true", help="输出全部已收录条目清单")
    args = ap.parse_args()

    if args.list:
        text = read_articles()
        if text is None:
            return 2
        print(list_all(text))
        return 0

    if not args.url and not args.title:
        ap.print_usage()
        return 2

    code, msg = check(args.url, args.title, args.threshold)
    print(msg)
    return code


if __name__ == "__main__":
    sys.exit(main())