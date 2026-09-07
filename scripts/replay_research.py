"""Replay saved, explicit triage decisions; default is read-only preview."""
import argparse
import collections
import pathlib

import research


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("analysis", type=pathlib.Path)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    data = research.extract_json_obj(args.analysis.read_text(encoding="utf-8"), require_verdict=True)
    if "candidates" not in data:
        parser.error("分析中没有合法的分流结果；不会回退搜索候选")
    print(dict(collections.Counter(c["verdict"] for c in data["candidates"])))
    if args.apply:
        art = research.ROOT / "references/articles.md"
        original = art.read_bytes()
        try:
            print(research.apply_triage(data["candidates"], promote_observed=True))
        except Exception:
            art.write_bytes(original)
            raise
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
