#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""统计 references/articles.md 待处理队列条数（供 ingest.yml 判断是否需要加工）。

与 curate.parse_queue 一致：跳过「评审中」行；raw/ 已弃用，不再作为计数源。
"""
import pathlib
import re
import sys

ARTICLES = pathlib.Path(__file__).resolve().parent.parent / "references" / "articles.md"


def count_pending(text: str) -> int:
    m = re.search(r"<!-- pending:start -->(.*?)<!-- pending:end -->", text, re.S)
    if not m:
        return 0
    n = 0
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        if "评审中" in line:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) >= 4 and not cells[0].startswith("标题"):
            n += 1
    return n


def main():
    if not ARTICLES.exists():
        print(0)
        return 0
    text = ARTICLES.read_text(encoding="utf-8", errors="replace")
    print(count_pending(text))
    return 0


if __name__ == "__main__":
    sys.exit(main())
