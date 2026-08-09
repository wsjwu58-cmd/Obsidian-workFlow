#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""情报搜索层：Firecrawl 深度搜索 → codex 综合为候选清单 → 机械去重 → 入队列。

由 research.yml（每周 + 手动）触发，运行在服务器。替代 collect.py 的固定源采集。

职责：
1. 用 firecrawl_search.search() 按情报分析师提示词的信源/关键词搜索真实结果
2. 组装 prompt（prompts/research-tracker.md + 注入已知内容去重段 + 日期窗口 + 搜索结果）
3. codex exec 综合为候选清单（JSON）
4. 机械去重（URL 精确比对 existing_urls + 队列查重）→ collect.save_item 入队

仅依赖标准库 + firecrawl_search + codex CLI。
"""
import argparse
import datetime
import json
import os
import pathlib
import re
import shlex
import subprocess
import sys

import firecrawl_search

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import collect


def known_content_block():
    """从 articles.md 抽已收录标题+URL，构造去重注入段。"""
    art = ROOT / "references" / "articles.md"
    if not art.exists():
        return "（暂无）"
    t = art.read_text(encoding="utf-8", errors="replace")
    titles = re.findall(r"### \d+\. (.+)", t)
    urls = collect.existing_urls()
    lines = [f"- {x}" for x in titles[:80]]
    lines.append("URL 清单（已收录 + 待处理，去重用）：")
    lines += [f"  - {u}" for u in sorted(urls)[:120]]
    return "\n".join(lines)


def run_codex(prompt, root):
    prompt_file = pathlib.Path(__import__("tempfile").gettempdir(), ".research_prompt.md")
    prompt_file.write_text(prompt, encoding="utf-8")
    r = subprocess.run(
        f"set -a; source /etc/environment; set +a; "
        f"codex exec -C {root} "
        f"--sandbox workspace-write -c sandbox_workspace_write.network_access=true "
        f"< {shlex.quote(str(prompt_file))}",
        shell=True, cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=900,
    )
    return r.stdout, r.returncode


def parse_candidates(stdout):
    """从 codex 输出提取 JSON 候选清单（容忍前后杂质）。"""
    m = re.search(r"\{.*\}", stdout, re.S)
    if not m:
        return []
    try:
        data = json.loads(m.group(0))
    except json.JSONDecodeError:
        return []
    return data.get("candidates", [])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=14)
    ap.add_argument("--max", type=int, default=10)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    today = datetime.date.today()
    start = today - datetime.timedelta(days=args.days)
    template = (ROOT / "prompts" / "research-tracker.md").read_text(encoding="utf-8")
    known = known_content_block()
    prompt = template.replace("{START_DATE}", start.isoformat()) \
                      .replace("{END_DATE}", today.isoformat()) \
                      .replace("{KNOWN_CONTENT}", known) \
                      .replace("{MAX_ITEMS}", str(args.max))

    # Firecrawl 搜索结果注入（为 codex 提供真实候选素材）
    search_results = firecrawl_search.search("harness engineering coding agent", count=args.max)
    if search_results:
        lines = ["\n## 联网检索到的候选（Firecrawl，仅作线索）\n"]
        for i, r in enumerate(search_results, 1):
            lines.append(f"{i}. {r['title']} | {r['url']}")
        prompt += "\n" + "\n".join(lines)

    if args.dry_run:
        print("[research] dry-run：以下为将注入的提示词（截断）")
        print(prompt[:2000])
        return 0

    print("[research] 调用 codex 情报分析…")
    stdout, rc = run_codex(prompt, ROOT)
    if rc != 0:
        print(f"[research] codex 返回 {rc}，失败")
        print(stdout[-1500:])
        return rc

    cands = parse_candidates(stdout)
    print(f"[research] codex 产出候选 {len(cands)} 条")
    new_count = 0
    known = collect.existing_urls()
    for c in cands:
        url = (c.get("url") or "").strip()
        title = (c.get("title") or "").strip()
        if not url or not title:
            continue
        if url in known:
            print(f"[research] 去重跳过：{title[:50]}")
            continue
        msg = collect.save_item("research", c)
        print(f"[research] {msg}")
        if msg and msg.startswith("入队"):
            known.add(url)
            new_count += 1
    print(f"[research] 完成：新增 {new_count} 条候选")
    return 0


if __name__ == "__main__":
    sys.exit(main())
