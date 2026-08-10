#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""[已废弃 CLI] 收录落位已内联到 curate.py（唯一终审 PR）。

保留本模块仅作兼容：手动补跑旧 candidates/<batch>/ 时可：
  python scripts/finalize.py --batch 20260809-180901 --no-pr

默认不再开第二次 PR；finalize.yml 已退役。
"""
import argparse
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from kb_common import land_translations, make_slug
import re


def _parse_pending_rows(text, batch_name):
    m = re.search(r"<!-- pending:start -->(.*?)<!-- pending:end -->", text, re.S)
    if not m:
        return []
    rows = []
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        if batch_name and f"candidates/{batch_name}" not in line and batch_name not in line:
            # 兼容：无评审中标记时，不按 batch 过滤（手动补跑传入 queue 文件时）
            if "🔄" in line or "评审中" in line:
                continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) >= 4 and not cells[0].startswith("标题"):
            if batch_name and f"candidates/{batch_name}" not in line and "评审中" in line:
                continue
            if batch_name and ("评审中" in line) and (batch_name not in line):
                continue
            if batch_name and ("评审中" in line) and (batch_name in line):
                rows.append({"title": cells[0], "url": cells[1],
                             "source": cells[2], "date": cells[3]})
            elif batch_name and "评审中" not in line:
                continue
            elif not batch_name:
                rows.append({"title": cells[0], "url": cells[1],
                             "source": cells[2], "date": cells[3]})
    return rows


def main():
    ap = argparse.ArgumentParser(description="已废弃：请优先用 curate.py 内联落位")
    ap.add_argument("--batch", required=True, help="candidates/ 下的批次目录名")
    ap.add_argument("--no-pr", action="store_true", default=True,
                    help="不打开 PR（默认 True）")
    args = ap.parse_args()
    print("[finalize] 警告：本 CLI 已退役；落位逻辑仅供手动补跑旧批次。")
    batch = ROOT / "candidates" / args.batch
    if not batch.is_dir():
        print(f"[finalize] 批次不存在：{batch}")
        return 1
    art = ROOT / "references" / "articles.md"
    rows = _parse_pending_rows(art.read_text(encoding="utf-8") if art.exists() else "", args.batch)
    if not rows:
        # 从 works-ready 文件名反推空 row 无法配对；要求队列仍有行
        print("[finalize] 队列中无本批次行；尝试仅落位 works-ready（articles 可能不完整）")
        wr = batch / "works-ready"
        rows = []
        if wr.exists():
            for f in sorted(wr.glob("*-translation.md")):
                rows.append({
                    "title": f.name.replace("-translation.md", ""),
                    "url": f"https://example.invalid/{make_slug(f.name)}",
                    "source": "finalize-manual",
                    "date": "",
                })
    land_translations(batch, rows, keep_sources=False)
    print("[finalize] 落位完成（未开 PR）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
