#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""候选加工层：攒批 → codex 产三件套 → 内联落位 → 唯一终审 PR。

由 dispatch-worker.yml（每 3h）触发，运行在服务器。

职责：
1. git pull main；合并 origin/pipeline/queue 的 articles 变更
2. 解析待处理队列，取前 N（默认 4）条
3. codex 为每篇产 candidates/<batch>/ 三件套（sources + translations + works-ready）
4. 内联落位：works-ready → working/；回写 articles；同步 index/log/图谱/AGENTS
5. 开**唯一**终审 PR（人工评审后合并 main）——不再开 research/finalize 中间 PR
6. 取消 curate-review 后置 AI 打分

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
sys.path.insert(0, str(ROOT / "scripts"))

from kb_common import land_translations, make_slug


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
        if "评审中" in line:
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
        return r.stdout + "\n" + r.stderr, r.returncode
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
            print(f"[curate] 终审 PR: {pr['html_url']}")
            return pr["html_url"]
    except urllib.error.HTTPError as e:
        print(f"[curate] 开 PR 失败（HTTP {e.code}）：{e.read().decode('utf-8', 'replace')[:400]}")
        return None


def merge_pipeline_queue():
    """把 origin/pipeline/queue 的 articles（及 research 产物）合入工作树。"""
    sh("git fetch origin pipeline/queue", check=False)
    # 仅检出 articles.md；若分支不存在则跳过
    r = sh("git show origin/pipeline/queue:references/articles.md", check=False)
    if r.returncode != 0 or not r.stdout.strip():
        print("[curate] 无 origin/pipeline/queue 或 articles 为空，跳过合并")
        return False
    art = ROOT / "references" / "articles.md"
    art.write_text(r.stdout, encoding="utf-8")
    print("[curate] 已合并 origin/pipeline/queue 的 articles.md")
    # 尝试带上 research-* 分析落盘（可选）
    sh("git checkout origin/pipeline/queue -- candidates/research-* 2>/dev/null || true",
       check=False)
    return True


def main():
    lock = pathlib.Path(__import__("tempfile").gettempdir(), ".curate.lock")
    if lock.exists():
        print("[curate] 检测到运行中的 curate 实例（锁存在），退出")
        return 0
    lock.touch()
    try:
        return _run()
    finally:
        lock.unlink(missing_ok=True)


def _run():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=4)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if args.dry_run:
        art = ROOT / "references" / "articles.md"
        text = art.read_text(encoding="utf-8") if art.exists() else ""
        queue = parse_queue(text, args.limit)
        print(f"[curate] 待处理 {len(queue)} 条（本次上限 {args.limit}）")
        for q in queue:
            print(f"  [dry] {q['title'][:60]} | {q['url']}")
        return 0

    pull = sh("git pull --rebase origin main", check=False)
    if pull.returncode != 0:
        print(f"[curate] git pull 警告：{pull.stderr[-300:]}")

    git_ref = os.environ.get("NOTE_GIT_REF", "main")
    sh(f"git fetch origin {git_ref}", check=False)
    co = sh(f"git checkout {git_ref}", check=False)
    if co.returncode != 0:
        # 无本地分支时从远程建
        co = sh(f"git checkout -B {git_ref} origin/{git_ref}", check=False)
    if co.returncode != 0:
        print(f"[curate] 无法切到 {git_ref}，终止")
        return 1
    sh(f"git reset --hard origin/{git_ref}", check=False)
    sh("git clean -fd candidates 2>/dev/null || true", check=False)

    merged_queue = merge_pipeline_queue()

    text = (ROOT / "references" / "articles.md").read_text(encoding="utf-8")
    queue = parse_queue(text, args.limit)
    print(f"[curate] 待处理 {len(queue)} 条（本次上限 {args.limit}）")

    batch_id = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    batch = f"candidates/{batch_id}"
    batch_dir = ROOT / batch
    ok_items = []

    if queue:
        batch_dir.mkdir(parents=True, exist_ok=True)
        curate_prompt = (ROOT / "prompts" / "curate.md").read_text(encoding="utf-8")
        if curate_prompt.startswith("---"):
            curate_prompt = re.sub(
                r"^---\s*\n.*?\n---\s*\n", "", curate_prompt, count=1, flags=re.S
            )
        for i, item in enumerate(queue, 1):
            slug = make_slug(item["title"])
            p = curate_prompt + (
                f"\n\n## 本次条目\n标题：{item['title']}\nURL：{item['url']}\n"
                f"来源：{item['source']} | 日期：{item['date']}\n"
                f"批次目录：{batch}/\nslug：{slug}\n"
            )
            print(f"[curate] 加工 {i}/{len(queue)}：{item['title'][:40]}…")
            (batch_dir / "sources").mkdir(exist_ok=True)
            (batch_dir / "works-ready").mkdir(exist_ok=True)
            (batch_dir / "translations" / slug).mkdir(parents=True, exist_ok=True)
            stdout, rc = run_codex(p, ROOT, ".curate_prompt.md")
            if rc != 0:
                print(f"[curate] 加工失败 {item['title'][:30]}，继续")
                continue
            ok_items.append(item)

        if ok_items:
            print(f"[curate] 内联落位 {len(ok_items)} 篇…")
            land_translations(batch_dir, ok_items, keep_sources=True)
        elif queue:
            print("[curate] 全部条目加工失败，不落位")
            if not merged_queue:
                return 0

    # 无翻译但有 queue 分支 articles 变更时，仍开终审 PR
    sh("git add -A")
    changed = sh("git status --porcelain", check=False).stdout.strip()
    if not changed:
        print("[curate] 无变更，退出")
        return 0

    branch = f"review/{batch_id}"
    sh(f"git checkout -b {branch}")
    sh("git config user.name note-worker || true", check=False)
    sh("git config user.email note-worker@users.noreply.github.com || true", check=False)
    sh('git commit -m "review: AI 产出待人工终审（唯一 PR）"')
    sh(f"git push origin {branch}")

    moved = sorted((ROOT / "working").glob("*-translation.md"))
    body_lines = [
        "## 待人工终审（本仓库唯一 AI PR）",
        "",
        f"- 批次：`{batch_id}`",
        f"- 本批翻译落位：{len(ok_items)} 篇",
        "- 已同步：`references/articles.md` / `expand/index.md` / `expand/log.md` / "
        "`expand/知识图谱.md` / `working/AGENTS.md`",
        "",
        "### 操作",
        "- 同意 → 合并本 PR",
        "- 某篇不收录 → 删除对应 `working/*-translation.md`，并改 articles 状态后合并",
        "",
        "### 本批条目",
    ]
    for it in ok_items:
        body_lines.append(f"- {it['title']} | {it['url']}")
    if not ok_items:
        body_lines.append("- （无新译文；含 research 索引/观察项变更）")

    create_pr(branch, "main", f"待审：AI 产出 {len(ok_items)} 篇（{batch_id}）",
              "\n".join(body_lines)[:3000])
    print(f"[curate] 完成：{branch}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
