#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""候选加工层：攒批 3-4 篇 → codex 产三件套 → 串行评审 → 开评审 PR。

由 dispatch-worker.yml（每 3h）触发，运行在服务器。替代 worker.py 的全自动加工。

职责：
1. git pull --rebase 同步权威仓库
2. 解析 references/articles.md 待处理队列，取前 N（默认 4）条
3. codex exec 为每篇产 candidates/<batch>/ 三件套（sources/ + translations/ + works-ready/）
4. 串行评审：单 codex exec 对 N 篇统一打分（prompts/curate-review.md）
5. 汇总 candidates/<batch>/review.md「候选 × 定性 × 去向」表
6. 更新 articles.md：各条 → 评审中
7. push 分支 candidates/<batch>，开评审 PR（GitHub REST API）

仅依赖标准库 + codex CLI。
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

ROOT = pathlib.Path(__file__).resolve().parent.parent


def sh(cmd, cwd=None, check=True):
    r = subprocess.run(cmd, shell=True, cwd=cwd or ROOT,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if check and r.returncode != 0:
        print(f"[curate] 命令失败: {cmd}\n{r.stdout}\n{r.stderr}")
        sys.exit(r.returncode)
    return r


def parse_queue(text, limit):
    m = re.search(r"<!-- pending:start -->(.*?)<!-- pending:end -->", text, re.S)
    if not m:
        return []
    rows = []
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) >= 4 and not cells[0].startswith("标题"):
            rows.append({"title": cells[0], "url": cells[1],
                         "source": cells[2], "date": cells[3]})
        if len(rows) >= limit:
            break
    return rows


def run_codex(prompt, root, prompt_name):
    prompt_file = pathlib.Path(__import__("tempfile").gettempdir(), prompt_name)
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
        return r.stdout, r.returncode
    except Exception as e:
        print(f"[curate] codex 调用失败：{type(e).__name__}: {e}")
        return "", 1


def create_pr(head, base, title, body):
    token = os.environ.get("GH_TOKEN", os.environ.get("GITHUB_TOKEN", ""))
    if not token:
        print("[curate] 缺少 GH_TOKEN，跳过开 PR")
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
            print(f"[curate] 评审 PR: {pr['html_url']}")
            return pr["html_url"]
    except urllib.error.HTTPError as e:
        print(f"[curate] 开 PR 失败（HTTP {e.code}）：{e.read().decode('utf-8', 'replace')[:400]}")
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=4)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    pull = sh("git pull --rebase origin main", check=False)
    if pull.returncode != 0:
        print(f"[curate] git pull 警告：{pull.stderr[-300:]}")

    text = sh("cat references/articles.md", check=False).stdout
    queue = parse_queue(text, args.limit)
    print(f"[curate] 待处理 {len(queue)} 条（本次上限 {args.limit}）")
    if not queue:
        print("[curate] 队列为空，退出")
        return 0
    if args.dry_run:
        for q in queue:
            print(f"  [dry] {q['title'][:60]} | {q['url']}")
        return 0

    batch = f"candidates/{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}"
    batch_dir = ROOT / batch
    batch_dir.mkdir(parents=True, exist_ok=True)

    # 1) 每篇产三件套
    curate_prompt = (ROOT / "prompts" / "curate.md").read_text(encoding="utf-8")
    for i, item in enumerate(queue, 1):
        slug = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", item["title"])[:40].strip("-") or f"item{i}"
        p = curate_prompt + (
            f"\n\n## 本次条目\n标题：{item['title']}\nURL：{item['url']}\n"
            f"来源：{item['source']} | 日期：{item['date']}\n"
            f"批次目录：{batch}/\nslu：{slug}\n"
        )
        print(f"[curate] 加工 {i}/{len(queue)}：{item['title'][:40]}…")
        stdout, rc = run_codex(p, ROOT, ".curate_prompt.md")
        if rc != 0:
            print(f"[curate] 加工失败 {item['title'][:30]}，继续")
            continue
        (batch_dir / "sources").mkdir(exist_ok=True)
        (batch_dir / "works-ready").mkdir(exist_ok=True)
        (batch_dir / "translations" / slug).mkdir(parents=True, exist_ok=True)

    # 2) 串行评审
    review_prompt = (ROOT / "prompts" / "curate-review.md").read_text(encoding="utf-8")
    items_block = "\n".join(f"- {q['title']} | {q['url']}" for q in queue)
    review_prompt = review_prompt.replace("{ITEMS}", items_block) \
                                 .replace("{BATCH}", batch)
    print(f"[curate] 评审 {len(queue)} 篇…")
    stdout, rc = run_codex(review_prompt, ROOT, ".curate_review_prompt.md")
    if rc == 0:
        (batch_dir / "review.md").write_text(stdout, encoding="utf-8")
    else:
        (batch_dir / "review.md").write_text("评审失败，请人工查看。\n" + stdout[-2000:], encoding="utf-8")

    # 3) 回写 articles.md：待处理 → 评审中
    art = ROOT / "references" / "articles.md"
    t = art.read_text(encoding="utf-8")
    for item in queue:
        url = re.escape(item["url"])
        t = re.sub(rf"(\|.*\| {url} \|[^\n]*)", rf"\1 🔄评审中→{batch}/", t)
    art.write_text(t, encoding="utf-8")

    # 4) push + 开评审 PR
    sh("git add -A")
    changed = sh("git status --porcelain", check=False).stdout.strip()
    if not changed:
        print("[curate] 无变更，退出")
        return 0
    branch = f"candidates/{batch.split('/')[-1]}"
    sh(f"git checkout -b {branch}")
    sh("git config user.name note-worker || true")
    sh("git config user.email note-worker@users.noreply.github.com || true")
    sh('git commit -m "curate: 候选批次（待人工评审）"')
    sh(f"git push origin {branch}")
    review_text = (batch_dir / "review.md").read_text(encoding="utf-8", errors="replace")
    title = f"候选：{batch}（{len(queue)} 篇）"
    create_pr(branch, "main", title, review_text[:3000])
    print(f"[curate] 完成：{branch}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
