#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""统计 references/raw/ 中 status=pending 的素材数量（供 ingest.yml 判断是否需要加工）。"""
import pathlib
import re
import sys

RAW = pathlib.Path(__file__).resolve().parent.parent / "references" / "raw"


def main():
    n = 0
    for p in RAW.rglob("*.md"):
        if p.name == "README.md":
            continue
        head = p.read_text(encoding="utf-8", errors="ignore")[:500]
        if re.search(r"^status:\s*pending\s*$", head, re.M):
            n += 1
    print(n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
