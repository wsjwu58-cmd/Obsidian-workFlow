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
import urllib.request

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


def sh(cmd, cwd=None, check=True):
    r = subprocess.run(cmd, shell=True, cwd=cwd or ROOT,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if check and r.returncode != 0:
        print(f"[research] 命令失败: {cmd}\n{r.stdout}\n{r.stderr}")
        sys.exit(r.returncode)
    return r


def create_pr(head, base, title, body):
    token = os.environ.get("GH_TOKEN", os.environ.get("GITHUB_TOKEN", ""))
    if not token:
        print("[research] 缺少 GH_TOKEN，跳过开 PR")
        return None
    remote = sh("git config --get remote.origin.url", check=False).stdout.strip()
    m = re.search(r"github\.com[:/]([^/]+)/([^/.]+)", remote)
    if not m:
        return None
    owner, repo = m.group(1), m.group(2)
    payload = {"title": title, "head": head, "base": base, "body": body}
    req = urllib.request.Request(
        f"https://api.github.com/repos/{owner}/{repo}/pulls",
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"token {token}",
                 "Accept": "application/vnd.github+json",
                 "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            pr = json.loads(resp.read().decode())
            print(f"[research] 情报搜索 PR: {pr['html_url']}")
            return pr["html_url"]
    except urllib.error.HTTPError as e:
        print(f"[research] 开 PR 失败（HTTP {e.code}）：{e.read().decode('utf-8', 'replace')[:400]}")
        return None


def run_codex(prompt, root):
    prompt_file = pathlib.Path(__import__("tempfile").gettempdir(), ".research_prompt.md")
    prompt_file.write_text(prompt, encoding="utf-8")
    cmd = (
        f"set -a; source /etc/environment; set +a; "
        f"codex exec -C {shlex.quote(str(root))} "
        f"--sandbox workspace-write -c sandbox_workspace_write.network_access=true "
        f"< {shlex.quote(str(prompt_file))}"
    )
    try:
        r = subprocess.run(
            cmd, shell=True, cwd=root, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=900,
        )
        return r.stdout + "\n" + r.stderr, r.returncode
    except Exception as e:
        print(f"[research] codex 调用失败：{type(e).__name__}: {e}")
        return "", 1


def parse_candidates(stdout):
    """从 codex 输出提取 JSON 候选清单（容忍前后杂质）。"""
    m = re.search(r"\{.*\}", stdout, re.S)
    if not m:
        return []
    try:
        data = json.loads(m.group(0))
    except json.JSONDecodeError:
        return []
    cands = data.get("candidates", [])
    return cands if isinstance(cands, list) else []


def main():
    lock = pathlib.Path(__import__("tempfile").gettempdir(), ".research.lock")
    if lock.exists():
        print("[research] 检测到运行中的 research 实例（锁存在），退出")
        return 0
    lock.touch()
    try:
        return _run()
    finally:
        lock.unlink(missing_ok=True)


def _run():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=14)
    ap.add_argument("--max", type=int, default=10)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    today = datetime.date.today()
    start = today - datetime.timedelta(days=args.days)
    if not args.dry_run:
        subprocess.run("git checkout main", shell=True, cwd=ROOT, capture_output=True, text=True)
        subprocess.run("git pull --rebase origin main", shell=True, cwd=ROOT, capture_output=True, text=True)
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
    body = "情报搜索候选清单，请 review 合并后进入待处理队列：\n\n" + \
           "\n".join(f"- {c.get('title', '')} | {c.get('url', '')}" for c in cands)
    print(f"[research] 完成：新增 {new_count} 条候选")
    # main 受保护不可直推：改为 research/<ts> 分支 + PR，与 curate.py 一致
    if new_count > 0:
        branch = f"research/{__import__('datetime').datetime.now().strftime('%Y%m%d-%H%M%S')}"
        for cmd in [
            "git checkout -b " + branch,
            "git add references/articles.md",
            "git config user.name note-worker || true",
            "git config user.email note-worker@users.noreply.github.com || true",
            "git commit -m 'research: 情报搜索新增候选条目'",
            "git push origin " + branch,
        ]:
            r = subprocess.run(cmd, shell=True, cwd=ROOT, capture_output=True, text=True,
                               encoding="utf-8", errors="replace")
            if r.returncode != 0:
                print(f"[research] git 命令失败: {cmd}\n{r.stderr[-300:]}")
                return 1
        create_pr(branch, "main", "研究：情报搜索候选条目", body)
    return 0


if __name__ == "__main__":
    sys.exit(main())
