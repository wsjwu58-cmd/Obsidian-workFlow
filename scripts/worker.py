#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""服务器执行引擎 worker。

站点：服务器（Ubuntu 22.04，root@/root/note-worker）。由 GitHub Actions「调度中枢」
或服务器 cron 触发。职责：

1. git pull --rebase 同步权威仓库
2. 解析 references/articles.md 「待处理」队列
3. 逐个条目：codex exec 处理（抓取原文 → 判定归属 expand/thinking | working/ | prompts/
   → 生成条目 → 回写 articles.md 状态/归属）→ 更新 expand/index.md、expand/log.md
4. 处理完成后 git push 到 feature 分支，开 PR（gh）供人工 review 合并

用法（在服务器 worker 目录内）：
  python3 scripts/worker.py            # 处理所有待处理（默认不多于 3 条）
  python3 scripts/worker.py --limit 1  # 只处理一条
  python3 scripts/worker.py --dry-run  # 只打印待处理清单，不执行 codex
仅依赖标准库 + 服务器上的 codex CLI / gh CLI。
"""
import argparse
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
        print(f"[worker] 命令失败: {cmd}\n{r.stdout}\n{r.stderr}")
        sys.exit(r.returncode)
    return r


def read_articles():
    p = ROOT / "references" / "articles.md"
    return p.read_text(encoding="utf-8", errors="replace")


def parse_queue(text):
    """解析「待处理」队列行（collect.py 写入格式）：
    | 标题 | URL | 来源 | 日期 |
    """
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
    return rows


def create_pr(head, base="main"):
    """用 GitHub REST API 开 PR（服务器不依赖 gh CLI）。需 GH_TOKEN 环境变量。"""
    token = os.environ.get("GH_TOKEN", os.environ.get("GITHUB_TOKEN", ""))
    if not token:
        print("[worker] 缺少 GH_TOKEN，跳过开 PR（分支已推送）")
        return None
    remote = sh("git config --get remote.origin.url", check=False).stdout.strip()
    m = re.search(r"github\.com[:/]([^/]+)/([^/.]+)", remote)
    if not m:
        print(f"[worker] 无法从 remote 解析仓库：{remote}，跳过 PR")
        return None
    owner, repo = m.group(1), m.group(2)
    title = f"worker: 服务器 codex 加工 {__import__('datetime').datetime.now().strftime('%Y%m%d')}"
    payload = {
        "title": title,
        "head": head,
        "base": base,
        "body": "服务器执行引擎 auto-generated，请 review 合并",
    }
    req = urllib.request.Request(
        f"https://api.github.com/repos/{owner}/{repo}/pulls",
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            pr = json.loads(resp.read().decode())
            print(f"[worker] PR 已创建: {pr['html_url']}")
            return pr["html_url"]
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")[:500]
        print(f"[worker] 开 PR 失败（HTTP {e.code}）：{body}")
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=3)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    # 启动时同步权威仓库（服务器 cron/Actions 触发前默认旧，需先拉最新队列）
    pull = sh("git pull --rebase origin main", check=False)
    if pull.returncode != 0:
        print(f"[worker] git pull 警告（可能无分支跟踪或网络），继续：\n{pull.stderr[-300:]}")

    text = read_articles()
    queue = parse_queue(text)
    print(f"[worker] 待处理 {len(queue)} 条（本次上限 {args.limit}）")
    if not queue:
        print("[worker] 队列为空，退出")
        return 0
    if args.dry_run:
        for q in queue[:args.limit]:
            print(f"  [dry] {q['title'][:60]} | {q['url']}")
        return 0

    # 用一个交给 codex 的提示词，让它处理前 N 条
    batch = queue[:args.limit]
    prompt_path = ROOT / "prompts" / "worker.md"
    prompt = prompt_path.read_text(encoding="utf-8").strip() if prompt_path.exists() \
        else "处理 references/articles.md 待处理队列中的条目（见 rules 与 worker 约定）。"
    prompt += "\n\n## 本次待处理条目\n"
    for i, r in enumerate(batch, 1):
        prompt += (f"\n### 待处理 {i}\n标题：{r['title']}\nURL：{r['url']}\n"
                   f"来源：{r['source']} | 日期：{r['date']}\n")
    prompt += ("\n## 输出要求\n严格按注解 machine-readable 要求回写 references/articles.md "
               "（状态→已收录/已淘汰、归属→生成的 expand/thinking 或 working 路径），"
               "完成后告知变更摘要。")

    print(f"[worker] 调用 codex exec 处理 {len(batch)} 条…")
    prompt_file = pathlib.Path(__import__('tempfile').gettempdir(), ".worker_prompt.md")
    prompt_file.write_text(prompt, encoding="utf-8")
    r = sh(
        f"set -a; source /etc/environment; set +a; "
        f"codex exec -C {ROOT} "
        f"--sandbox workspace-write -c sandbox_workspace_write.network_access=true "
        f"< {shlex.quote(str(prompt_file))}",
        check=False,
    )
    print(r.stdout[-4000:] if r.stdout else "")
    if r.stderr:
        print("[codex stderr]", r.stderr[-2000:])
    if r.returncode != 0:
        print(f"[worker] codex 返回 {r.returncode}，任务未完成，退出")
        return r.returncode

    # 刷新权威仓库状态：codex 已写 expand/ 条目 + articles.md；循环无需自行回写

    # ─── git push 分支 + 开 PR（人工 review 合并） ───
    sh("git add -A")
    changed = sh("git status --porcelain", check=False).stdout.strip()
    if not changed:
        print("[worker] 无变更（可能全被标记已淘汰），跳过提交")
        return 0
    branch = f"ai-worker/{__import__('datetime').datetime.now().strftime('%Y%m%d-%H%M%S')}"
    sh(f"git checkout -b {branch}")
    sh("git config user.name note-worker || true")
    sh("git config user.email note-worker@users.noreply.github.com || true")
    sh('git commit -m "worker: 服务器 codex 加工结果（待 review）"')
    sh(f"git push origin {branch}")
    # 开 PR（GitHub API，服务器无需 gh CLI）
    create_pr(branch)
    print(f"[worker] 完成：{branch} 已 push")
    return 0


if __name__ == "__main__":
    sys.exit(main())