#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""curate 管道共享工具（curate.py / finalize.py / research.py 共用）。"""

import datetime
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent


def make_slug(title):
    """标题 → 安全 slug。与 curate.py 传给 codex 的文件名 slug 保持一致。"""
    s = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", title)[:40].strip("-")
    return s or "item"


def next_article_number(art_text):
    nums = [int(m) for m in re.findall(r"^### (\d+)\s*\.", art_text, re.M)]
    return (max(nums) + 1) if nums else 1


def fmt_article_entry(n, row, status="已收录", moved_file=None, core=None, lineage=None):
    display = row["url"].replace("https://", "").replace("http://", "")
    if status == "已淘汰":
        own = "—"
        core = core or "判定无加工价值，保留 URL 防重复采集"
    elif moved_file:
        own = f"`working/{moved_file}`"
        core = core or (row["title"] if len(row["title"]) <= 80 else row["title"][:80] + "…")
    elif lineage:
        # 仅索引收录：归属不写磁盘路径（避免 K1 归属警示），脉络写入核心
        own = "—"
        base = core or (row["title"] if len(row["title"]) <= 80 else row["title"][:80] + "…")
        core = f"脉络:{lineage}；{base}"
    else:
        own = "—"
        core = core or (row["title"] if len(row["title"]) <= 80 else row["title"][:80] + "…")
    return "\n".join([
        f"### {n:02d}. {row['title']}",
        "",
        f"- **标题：** {row['title']}",
        f"- **链接：** [{display}]({row['url']})",
        f"- **作者：** {row.get('source', 'research')} | **日期：** {row.get('date', '')}",
        f"- **状态：** {status} | **归属：** {own}",
        f"- **核心：** {core}",
    ])


def append_numbered_entries(art_text, entries):
    """把编号条目追加到「## 已收录（编号正文）」段末尾。"""
    hm = re.search(r"^## 已收录（编号正文）\s*$", art_text, re.M)
    if not hm:
        return art_text
    after = hm.end()
    nxt = re.search(r"^## ", art_text[after:], re.M)
    pos = after + nxt.start() if nxt else len(art_text)
    block = "\n\n" + "\n\n".join(entries)
    return art_text[:pos].rstrip("\n") + block + "\n\n" + art_text[pos:].lstrip("\n")


def ensure_observe_section(art_text):
    if re.search(r"^## 观察项\s*$", art_text, re.M):
        return art_text
    block = (
        "\n## 观察项\n\n"
        "> 暂不收录、持续观察的 URL（防重复采集，不计入编号正文主计数）。\n\n"
        "| 标题 | 链接 | 来源 | 日期 | 备注 |\n"
        "| --- | --- | --- | --- | --- |\n"
    )
    # 插在待处理段之后、已收录之前；找不到则追加文末
    m = re.search(r"^## 已收录（编号正文）\s*$", art_text, re.M)
    if m:
        return art_text[:m.start()] + block + "\n" + art_text[m.start():]
    return art_text.rstrip() + "\n" + block + "\n"


def append_observe_row(art_text, row, reason=""):
    art_text = ensure_observe_section(art_text)
    title = (row.get("title") or "").replace("|", "/")[:120]
    url = row.get("url") or ""
    source = row.get("source") or "research"
    date = row.get("date") or datetime.date.today().isoformat()
    note = (reason or "持续观察").replace("|", "/")[:80]
    line = f"| {title} | {url} | {source} | {date} | {note} |"
    # 插到观察项表头后
    m = re.search(
        r"(## 观察项\s*\n(?:.*?\n)*?\| --- \| --- \| --- \| --- \| --- \|\n)",
        art_text,
        re.S,
    )
    if not m:
        return art_text.rstrip() + "\n" + line + "\n"
    return art_text[:m.end()] + line + "\n" + art_text[m.end():]


def remove_pending_urls(art_text, urls):
    """从待处理队列删除指定 URL 行，并更新计数。"""
    url_set = set(urls)
    out_lines = []
    removed = 0
    in_block = False
    for line in art_text.splitlines(keepends=True):
        if "<!-- pending:start -->" in line:
            in_block = True
            out_lines.append(line)
            continue
        if "<!-- pending:end -->" in line:
            in_block = False
            out_lines.append(line)
            continue
        if in_block and line.strip().startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 2 and cells[1] in url_set:
                removed += 1
                continue
        out_lines.append(line)
    t = "".join(out_lines)
    cm = re.search(r"<!-- 当前：(\d+) 条待处理 -->", t)
    if cm and removed:
        n = max(0, int(cm.group(1)) - removed)
        t = t.replace(cm.group(0), f"<!-- 当前：{n} 条待处理 -->")
    return t, removed


def sync_working_agents(moved):
    """登记落位作品到 working/AGENTS.md。"""
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


def sync_knowledge_graph(moved):
    g = ROOT / "expand" / "知识图谱.md"
    if not g.exists() or not moved:
        return
    t = g.read_text(encoding="utf-8")
    lines = "\n".join(
        f"- `working/{name}`：curate 收录译文作品（Phase 4 输出）" for name in moved
    )
    header = "## 作品输出（working/）"
    if header in t:
        t = t.rstrip() + "\n" + lines + "\n"
    else:
        t = t.rstrip() + "\n\n" + header + "\n\n" + lines + "\n"
    g.write_text(t, encoding="utf-8")


def sync_expand_index(moved, summaries=None):
    """把 working 作品登记进 expand/index.md「作品输出（working/）」节。"""
    p = ROOT / "expand" / "index.md"
    if not p.exists() or not moved:
        return
    summaries = summaries or {}
    t = p.read_text(encoding="utf-8")
    header = "## 作品输出（working/）"
    lines = []
    for name in moved:
        stem = name[:-3] if name.endswith(".md") else name
        summary = summaries.get(name) or "curate 收录译文作品"
        # 避免重复追加
        if f"[[working/{stem}]]" in t or f"[[working/{name}]]" in t:
            continue
        lines.append(f"- [[working/{stem}]]：{summary}")
    if not lines:
        return
    block = "\n".join(lines) + "\n"
    if header in t:
        # 插在该节标题后、下一 ## 前
        m = re.search(rf"({re.escape(header)}\s*\n)", t)
        if m:
            t = t[:m.end()] + "\n" + block + t[m.end():]
        else:
            t = t.rstrip() + "\n" + block
    else:
        # 插在「待办清单」之前，否则文末
        todo = re.search(r"^## 待办清单", t, re.M)
        insert = f"\n{header}\n\n{block}\n"
        if todo:
            t = t[:todo.start()] + insert + t[todo.start():]
        else:
            t = t.rstrip() + "\n" + insert
    # 更新文首计数（兼容「条目」与「文件」两种措辞）
    m = re.search(r"全库共 (\d+) 个 Markdown (?:条目|文件)", t)
    if m:
        t = t.replace(m.group(0), f"全库共 {int(m.group(1)) + len(lines)} 个 Markdown 文件", 1)
    today = datetime.date.today().isoformat()
    t = re.sub(r"^updated:.*$", f"updated: {today}", t, count=1, flags=re.M)
    p.write_text(t, encoding="utf-8")


def append_log(batch_name, moved, obs=None, rej=None):
    log = ROOT / "expand" / "log.md"
    if not log.exists():
        return
    entry = (
        f"\n## [{datetime.date.today().isoformat()}] curate | {batch_name}\n"
        f"- 收录：{', '.join(moved) if moved else '无'}\n"
        f"- 观察项：{', '.join(obs or []) if obs else '无'}\n"
        f"- 淘汰：{', '.join(rej or []) if rej else '无'}\n"
    )
    with log.open("a", encoding="utf-8") as fh:
        fh.write(entry)


def land_translations(batch_dir, queue_rows, keep_sources=True):
    """把 batch 的 works-ready 落位到 working/，回写 articles，同步索引。

    无 AI 评审判定：凡成功产出的 works-ready 一律视为收录。
    queue_rows: [{title,url,source,date}, ...] 本批处理的待处理行。
    返回 moved 文件名列表。
    """
    batch_dir = pathlib.Path(batch_dir)
    wr = batch_dir / "works-ready"
    all_wr = sorted(f.name for f in wr.glob("*-translation.md")) if wr.exists() else []
    moved = []
    summaries = {}
    for name in all_wr:
        src = wr / name
        dest = ROOT / "working" / name
        text = src.read_text(encoding="utf-8")
        dest.write_text(text, encoding="utf-8")
        moved.append(name)
        # 尝试从 frontmatter title 取摘要
        m = re.search(r"^title:\s*[\"']?(.+?)[\"']?\s*$", text, re.M)
        summaries[name] = (m.group(1).strip() if m else name)[:80]
        print(f"[land] {name} → working/")

    art = ROOT / "references" / "articles.md"
    if art.exists() and (moved or queue_rows):
        t = art.read_text(encoding="utf-8")
        # 配对
        remaining = list(queue_rows)
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
        n = next_article_number(t)
        entries = []
        for row, mf in pairs:
            core = row["title"] if len(row["title"]) <= 80 else row["title"][:80] + "…"
            entries.append(fmt_article_entry(n, row, "已收录", mf, core))
            n += 1
        for row in remaining:
            entries.append(fmt_article_entry(n, row, "已淘汰"))
            n += 1
        if entries:
            t = append_numbered_entries(t, entries)
        urls = [r["url"] for r in queue_rows]
        t, _ = remove_pending_urls(t, urls)
        art.write_text(t, encoding="utf-8")

    sync_working_agents(moved)
    sync_knowledge_graph(moved)
    sync_expand_index(moved, summaries)
    append_log(batch_dir.name, moved)

    # 清理过程稿；可选保留 sources 供终审对照
    import shutil
    for sub in ("translations", "works-ready"):
        p = batch_dir / sub
        if p.exists():
            shutil.rmtree(p, ignore_errors=True)
    if not keep_sources:
        shutil.rmtree(batch_dir, ignore_errors=True)
    else:
        # 删掉空的子目录后若只剩 sources，保留 batch
        for leftover in list(batch_dir.iterdir()) if batch_dir.exists() else []:
            if leftover.name not in ("sources",) and leftover.is_dir():
                shutil.rmtree(leftover, ignore_errors=True)
    return moved
