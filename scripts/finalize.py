#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""收录落位层：候选 PR 合并后，把 works-ready 草稿落位到 working/，回写 articles.md。

由 finalize.yml（监听候选 PR 合并 closed+merged）触发，运行在 GitHub Actions runner。

职责：
1. 遍历 candidates/<batch>/，读各篇 review.md 收录标记
2. 收录：works-ready/*.md → working/；淘汰：仅回写状态
3. 回写 articles.md：评审中 → 已收录（归属 working/<slug>）/ 已淘汰
4. 同步 working/AGENTS.md（作品索引）、expand/log.md、知识图谱.md
5. 清理 candidates/<batch>/
6. 开「收录：<batch>」PR（供人类合并 → CI K1-K7）

仅依赖标准库。
"""
import argparse
import datetime
import json
import os
import pathlib
import re
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent


def list_batches():
    c = ROOT / "candidates"
    if not c.exists():
        return []
    return sorted([p for p in c.iterdir() if p.is_dir()])


def read_review(batch):
    rv = batch / "review.md"
    if not rv.exists():
        return ""
    return rv.read_text(encoding="utf-8", errors="replace")


def _sync_working_index(moved):
    """登记落位作品到 working/AGENTS.md（working 目录索引）。"""
    p = ROOT / "working" / "AGENTS.md"
    if not p.exists() or not moved:
        return
    t = p.read_text(encoding="utf-8")
    rows = "\n".join(f"| [[working/{name}]] | curate 收录译文作品 |" for name in moved)
    if re.search(r"^\s*\|", t, flags=re.M):
        lines = t.rstrip("\n").splitlines()
        last = max(i for i, ln in enumerate(lines) if re.match(r"^\s*\|", ln))
        lines.insert(last + 1, rows)
        t = "\n".join(lines) + "\n"
    else:
        block = f"## 已有作品\n\n| 作品 | 说明 |\n| --- | --- |\n{rows}"
        if re.search(r"^## 已有作品", t, flags=re.M):
            t = re.sub(r"^## 已有作品[^\n]*$", lambda m: block, t, flags=re.M, count=1)
            t = t.rstrip() + "\n"
        else:
            t = t.rstrip() + "\n\n" + block + "\n"
    p.write_text(t, encoding="utf-8")


def _sync_knowledge_graph(moved):
    """把落位作品记入 expand/知识图谱.md 关系中枢。"""
    g = ROOT / "expand" / "知识图谱.md"
    if not g.exists() or not moved:
        return
    t = g.read_text(encoding="utf-8")
    lines = "\n".join(f"- `working/{name}`：curate 收录译文作品（Phase 4 输出）" for name in moved)
    header = "## 作品输出（working/）"
    if header in t:
        t = t.rstrip() + "\n" + lines + "\n"
    else:
        t = t.rstrip() + "\n\n" + header + "\n\n" + lines + "\n"
    g.write_text(t, encoding="utf-8")


def create_pr(head, base, title, body):
    token = os.environ.get("GH_TOKEN", os.environ.get("GITHUB_TOKEN", ""))
    if not token:
        print("[finalize] 缺少 GH_TOKEN，跳过开 PR")
        return None
    remote = os.environ.get("GITHUB_REPOSITORY", "wsjwu58-cmd/Obsidian-workFlow")
    owner, repo = remote.split("/")
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
            print(f"[finalize] 收录 PR: {pr['html_url']}")
            return pr["html_url"]
    except urllib.error.HTTPError as e:
        print(f"[finalize] 开 PR 失败（HTTP {e.code}）：{e.read().decode('utf-8', 'replace')[:400]}")
        return None


def finalize_batch(batch):
    """处理单个候选批次。返回是否产生变更。"""
    # 落位 works-ready → working/
    wr = batch / "works-ready"
    moved = []
    if wr.exists():
        for f in wr.glob("*-translation.md"):
            dest = ROOT / "working" / f.name
            dest.write_text(f.read_text(encoding="utf-8"), encoding="utf-8")
            moved.append(f.name)
            print(f"[finalize] 落位 {f.name} → working/")

    # 回写 articles.md：评审中 → 已收录/已淘汰（锚定本批次，防跨批污染）
    art = ROOT / "references" / "articles.md"
    if art.exists():
        t = art.read_text(encoding="utf-8")
        marker = rf"🔄评审中 candidates/{re.escape(batch.name)}/"
        if moved:
            for name in moved:
                t, _ = re.subn(marker, f"已收录（归属 working/{name}）", t, count=1)
        t = re.sub(marker, "已淘汰（留 URL 防重复）", t)
        art.write_text(t, encoding="utf-8")

    # 同步 log.md
    log = ROOT / "expand" / "log.md"
    if log.exists():
        entry = (f"\n## [{datetime.date.today().isoformat()}] curate-finalize | {batch.name}\n"
                 f"- 收录：{', '.join(moved) if moved else '无'}\n")
        with log.open("a", encoding="utf-8") as fh:
            fh.write(entry)

    # 同步 working/AGENTS.md（作品索引）与知识图谱关系中枢
    _sync_working_index(moved)
    _sync_knowledge_graph(moved)

    # 清理 candidates/<batch>/
    import shutil
    shutil.rmtree(batch, ignore_errors=True)
    print(f"[finalize] 清理 {batch.name}")
    return bool(moved)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", default=None, help="指定处理某批次，默认处理全部")
    args = ap.parse_args()

    batches = list_batches()
    if args.batch:
        batches = [b for b in batches if b.name == args.batch]
    if not batches:
        print("[finalize] 无待处理候选批次")
        return 0

    changed = False
    for b in batches:
        changed |= finalize_batch(b)

    if not changed:
        print("[finalize] 无落位变更（全淘汰），直接提交")
    # 提交变更到分支 + 开收录 PR（main 受保护，不能直推）
    branch = f"finalize/{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}"
    os.system(f"cd {ROOT} && git checkout -b {branch} && git add -A && "
              f"git config user.name kb-bot && git config user.email kb-bot@users.noreply.github.com && "
              f"git commit -m 'finalize: 收录候选批次' && git push origin {branch}")
    create_pr(branch, "main", "收录：curate 候选批次", "AI 落位 + 索引回写，请 review 合并。")
    print("[finalize] 完成")
    return 0


if __name__ == "__main__":
    sys.exit(main())
