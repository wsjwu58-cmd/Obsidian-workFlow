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
import subprocess
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from kb_common import make_slug


def list_batches():
    c = ROOT / "candidates"
    if not c.exists():
        return []
    return sorted([p for p in c.iterdir() if p.is_dir()])


def _parse_pending_rows(text, batch_name):
    """解析待处理队列中属于本批次的行（含评审中标记）。"""
    m = re.search(r"<!-- pending:start -->(.*?)<!-- pending:end -->", text, re.S)
    if not m:
        return []
    rows = []
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        if f"candidates/{batch_name}" not in line:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) >= 4 and not cells[0].startswith("标题"):
            rows.append({"title": cells[0], "url": cells[1],
                         "source": cells[2], "date": cells[3]})
    return rows


def _next_number(art_text):
    nums = [int(m) for m in re.findall(r"^### (\d+)\s*\.", art_text, re.M)]
    return (max(nums) + 1) if nums else 1


def _fmt_entry(n, row, status="已收录", moved_file=None, core=None):
    display = row["url"].replace("https://", "").replace("http://", "")
    if status == "已淘汰":
        own = "—"
        core = core or "评审判定无加工价值，保留 URL 防重复采集"
    else:
        own = f"`working/{moved_file}`" if moved_file else "—"
        core = core or (row["title"] if len(row["title"]) <= 80 else row["title"][:80] + "…")
    return "\n".join([
        f"### {n:02d}. {row['title']}",
        "",
        f"- **标题：** {row['title']}",
        f"- **链接：** [{display}]({row['url']})",
        f"- **作者：** {row['source']} | **日期：** {row['date']}",
        f"- **状态：** {status} | **归属：** {own}",
        f"- **核心：** {core}",
    ])


def _pair_rows(moved, batch_rows):
    """把 works-ready 落位文件匹配回队列行。

    优先按 slug（与 curate.py 传给 codex 的文件名 slug 一致）匹配：
    `make_slug(标题)` 出现在文件名中即命中；匹配不到则退回剩余行的行序。
    返回 (pairs, dropped)：pairs=[(row, filename)] 收录；dropped=[row] 淘汰。
    """
    remaining = list(batch_rows)
    pairs = []
    for f in moved:
        idx = None
        for i, row in enumerate(remaining):
            if make_slug(row["title"]) in f:
                idx = i
                break
        if idx is None:
            idx = 0 if remaining else None
        if idx is None:
            break
        pairs.append((remaining.pop(idx), f))
    return pairs, remaining


def _classify_verdict(text):
    """把评审「建议去向」文本归入 include / observation / reject / tools。

    排除必须依赖清晰信号：只有明确出现 淘汰 / 观察项 / tools（待实测）才不落位；
    无法识别/缺失的去向默认收录（保守回退——评审缺表或格式漂移时不丢内容，
    与「解析失败默认全收录」一致）。
    """
    t = text or ""
    if "淘汰" in t:
        return "reject"
    if "观察项" in t:
        return "observation"
    if "tools/" in t or "待实测" in t:
        return "tools"
    if "working/" in t and "收录" in t:
        return "include"
    return "include"


def _parse_review_verdicts(review_text):
    """解析 review.md 汇总表，返回 {篇名: 收录判定}。

    review.md 是 codex 自由输出，汇总表可能缺失/错位。只认同时含「篇名」
    与「建议去向」（且为末列）的 markdown 表头，其后 `|` 开头行解析到表
    结束（空行/非表格行即止）；跳过分隔行。表缺失/无法解析时返回空 dict，
    调用方按「默认全收录」处理。
    """
    verdicts = {}
    for i, line in enumerate(review_text.splitlines()):
        if not line.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if "篇名" not in cells or "建议去向" not in cells:
            continue
        if cells.index("建议去向") != len(cells) - 1:
            continue  # 建议去向不是末列 → 不是汇总表
        ti = cells.index("篇名")
        for row in review_text.splitlines()[i + 1:]:
            rs = row.strip()
            if not rs.startswith("|"):
                break
            rc = [c.strip() for c in rs.strip().strip("|").split("|")]
            if len(rc) < 2 or all(re.fullmatch(r"[-:\s]*", c) for c in rc):
                continue  # 分隔行
            title, cell = rc[ti], rc[-1]
            if title and cell:
                verdicts[title] = _classify_verdict(cell)
    return verdicts


def _append_entries(art_text, entries):
    """把编号条目追加到「## 已收录（编号正文）」段末尾（下一个二级标题前）。"""
    hm = re.search(r"^## 已收录（编号正文）\s*$", art_text, re.M)
    if not hm:
        print("[finalize] 找不到编号正文 header，跳过编号写入")
        return art_text
    after = hm.end()
    nxt = re.search(r"^## ", art_text[after:], re.M)
    pos = after + nxt.start() if nxt else len(art_text)
    block = "\n\n" + "\n\n".join(entries)
    return art_text[:pos].rstrip("\n") + block + "\n\n" + art_text[pos:].lstrip("\n")


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
    # 评审建议去向 → 判定 收录/观察项/淘汰；解析失败或缺失默认全收录（保守回退）。
    # 落位规则：仅「已收录」进 working/；观察项/tools/淘汰 → 写编号条目但不落位。
    verdicts = {}
    review_p = batch / "review.md"
    if review_p.exists():
        verdicts = _parse_review_verdicts(review_p.read_text(encoding="utf-8"))
    verdict_by_slug = {make_slug(t): v for t, v in verdicts.items()}

    def verdict_for(name):
        """按 works-ready 文件名（含 make_slug(篇名) 前缀，同 _pair_rows）匹配评审判定。"""
        best_v, best_len = "include", -1
        for slug, v in verdict_by_slug.items():
            if slug and slug in name and len(slug) > best_len:
                best_v, best_len = v, len(slug)
        return best_v

    # 落位 works-ready → working/（仅已收录）；观察项/淘汰的草稿删除不残留
    wr = batch / "works-ready"
    all_wr = sorted(f.name for f in wr.glob("*-translation.md")) if wr.exists() else []
    moved, obs, rej = [], [], []
    for name in all_wr:
        v = verdict_for(name)
        if v == "include":
            dest = ROOT / "working" / name
            dest.write_text((wr / name).read_text(encoding="utf-8"), encoding="utf-8")
            moved.append(name)
            print(f"[finalize] 落位 {name} → working/（已收录）")
            continue
        p = wr / name
        if p.exists():
            p.unlink()
        if v == "reject":
            rej.append(name)
            print(f"[finalize] {name} → 已淘汰（不落位 working/）")
        else:
            obs.append(name)
            print(f"[finalize] {name} → 观察项（不落位 working/）")

    # 回写 articles.md：先写收录条目到编号正文，再移除本批次已处理的行
    art = ROOT / "references" / "articles.md"
    dropped = []
    if art.exists():
        t = art.read_text(encoding="utf-8")

        # 配对：works-ready 文件名按 slug 匹配回队列行（与 curate.py 传给 codex
        # 的 slug 一致）；匹配不到退回行序。未配到的行 → 淘汰，同样写编号正文
        # 保留 URL 防重复采集。
        batch_rows = [r for r in _parse_pending_rows(t, batch.name)]
        pairs, dropped = _pair_rows(all_wr, batch_rows)
        n = _next_number(t)
        entries = []
        for row, mf in pairs:
            v = verdict_for(mf)
            if v == "include":
                core = row["title"] if len(row["title"]) <= 80 else row["title"][:80] + "…"
                entries.append(_fmt_entry(n, row, "已收录", mf, core))
            elif v == "reject":
                entries.append(_fmt_entry(n, row, "已淘汰"))
            else:
                entries.append(_fmt_entry(n, row, "已收录", None,
                                          "观察项：评审建议仅作观察项（防重复采集），译文不收录"))
            n += 1
        for row in dropped:
            entries.append(_fmt_entry(n, row, "已淘汰"))
            n += 1
        if entries:
            t = _append_entries(t, entries)
            print(f"[finalize] 编号正文写入 {len(entries)} 条"
                  f"（收录 {len(moved)} / 观察项 {len(obs)} / 淘汰 {len(rej) + len(dropped)}）")

        out_lines = []
        removed = 0
        in_block = False
        for line in t.splitlines(keepends=True):
            if "<!-- pending:start -->" in line:
                in_block = True
                out_lines.append(line)
                continue
            if "<!-- pending:end -->" in line:
                in_block = False
                out_lines.append(line)
                continue
            if in_block and f"candidates/{batch.name}" in line:
                removed += 1
                continue
            out_lines.append(line)
        t = "".join(out_lines)
        cm = re.search(r"<!-- 当前：(\d+) 条待处理 -->", t)
        if cm:
            n = max(0, int(cm.group(1)) - removed)
            t = t.replace(cm.group(0), f"<!-- 当前：{n} 条待处理 -->")
        art.write_text(t, encoding="utf-8")

    # 同步 log.md
    log = ROOT / "expand" / "log.md"
    if log.exists():
        entry = (f"\n## [{datetime.date.today().isoformat()}] curate-finalize | {batch.name}\n"
                 f"- 收录：{', '.join(moved) if moved else '无'}\n"
                 f"- 观察项：{', '.join(obs) if obs else '无'}\n"
                 f"- 淘汰：{', '.join(rej) if rej else '无'}\n")
        with log.open("a", encoding="utf-8") as fh:
            fh.write(entry)

    # 同步 working/AGENTS.md（作品索引）与知识图谱关系中枢（仅含实际落位文件）
    _sync_working_index(moved)
    _sync_knowledge_graph(moved)

    # 清理 candidates/<batch>/
    import shutil
    shutil.rmtree(batch, ignore_errors=True)
    print(f"[finalize] 清理 {batch.name}")
    return bool(moved) or bool(dropped) or bool(obs) or bool(rej)


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
    for cmd in [
        "git checkout -b " + branch,
        "git add -A",
        "git config user.name kb-bot",
        "git config user.email kb-bot@users.noreply.github.com",
        "git commit -m 'finalize: 收录候选批次'",
        "git push origin " + branch,
    ]:
        r = subprocess.run(cmd, shell=True, cwd=ROOT, capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        if r.returncode != 0:
            print(f"[finalize] git 命令失败: {cmd}\n{r.stderr[-300:]}")
            return 1
    create_pr(branch, "main", "收录：curate 候选批次", "AI 落位 + 索引回写，请 review 合并。")
    print("[finalize] 完成")
    return 0


if __name__ == "__main__":
    sys.exit(main())
