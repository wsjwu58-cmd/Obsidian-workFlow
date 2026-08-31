#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""情报层：Prompt A（Firecrawl 搜索）→ Prompt B（长分析三档分流）→ 分档写入 articles。

由 research.yml（每周 + 手动）SSH 触发，运行在服务器。

职责：
1. 注入已知内容（retrack.py --list）
2. codex × Prompt A（提示词内强制调用 Firecrawl MCP/search）→ 搜索条目卡
3. codex × Prompt B（长分析）→ index | translate | observe
4. 按档写入 references/articles.md（编号 / 待处理 / 观察项）
5. 不开 PR；commit 后 push 到长期分支 pipeline/queue（供 curate 合并）

仅依赖标准库 + codex CLI（需能调用 Firecrawl）。
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

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import collect
from kb_common import (
    append_numbered_entries,
    append_observe_row,
    fmt_article_entry,
    next_article_number,
)


def sh(cmd, cwd=None, check=True):
    r = subprocess.run(cmd, shell=True, cwd=cwd or ROOT,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if check and r.returncode != 0:
        print(f"[research] 命令失败: {cmd}\n{r.stdout}\n{r.stderr}")
        sys.exit(r.returncode)
    return r


def known_content_block():
    """把当前索引中的 Agent 相关内容注入 Prompt A，保证去重段自包含。"""
    art = ROOT / "references" / "articles.md"
    if not art.exists():
        return "（暂无）"
    t = art.read_text(encoding="utf-8", errors="replace")
    agent_terms = re.compile(
        r"agent|harness|context engineering|coding|llm|rag|mcp|智能体|上下文|编程|工具调用|评测|工作流",
        re.I,
    )
    lines = [
        "### 当前知识库 Agent 相关编号文章（references/articles.md）",
        "（以下内容由当前索引实时生成；包含已收录、已淘汰和已关联的归属信息。）",
    ]
    entries = list(re.finditer(r"^### (\d+)\s*\.\s*(.+)$", t, re.M))
    kept = 0
    for i, m in enumerate(entries):
        end = entries[i + 1].start() if i + 1 < len(entries) else len(t)
        segment = t[m.end():end]
        section_heading = re.search(r"^##\s+", segment, re.M)
        if section_heading:
            segment = segment[:section_heading.start()]
        if not agent_terms.search(m.group(2) + " " + segment):
            continue
        url_m = re.search(r"- \*\*链接：\*\*\s*\[[^]]*\]\(([^)]+)\)", segment)
        date_m = re.search(r"\*\*日期：\*\*\s*([^|\n]+)", segment)
        state_m = re.search(r"- \*\*状态：\*\*\s*([^|\n]+)", segment)
        belong_m = re.search(r"- \*\*归属：\*\*\s*(.+)", segment)
        url = url_m.group(1).strip() if url_m else ""
        date = date_m.group(1).strip() if date_m else "未知日期"
        state = state_m.group(1).strip() if state_m else "未知状态"
        belong = belong_m.group(1).strip() if belong_m else "—"
        lines.append(
            f"- [{int(m.group(1)):02d}] {m.group(2).strip()} | {url} | "
            f"{date} | {state} | 归属：{belong}"
        )
        kept += 1

    def append_table_rows(heading, start_marker, end_marker):
        section_start = t.find(start_marker)
        if section_start < 0:
            return 0
        section_end = t.find(end_marker, section_start) if end_marker else len(t)
        section = t[section_start:section_end if section_end >= 0 else len(t)]
        found = 0
        for row in re.findall(r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|$", section, re.M):
            title, url, source, date, note = [x.strip() for x in row]
            if title in ("标题", "---") or set(title) == {"-"}:
                continue
            if not agent_terms.search(" ".join(row)):
                continue
            if found == 0:
                lines.append(f"\n### 当前知识库 Agent 相关{heading}")
            lines.append(f"- {title} | {url} | {source} | {date} | {note}")
            found += 1
        return found

    kept += append_table_rows("待处理内容", "<!-- pending:start -->", "<!-- pending:end -->")
    kept += append_table_rows("观察项", "## 观察项", "## 统计")
    if not kept:
        return "（暂无 Agent 相关内容）"
    return "\n".join(lines)


def run_codex(prompt, prompt_name, timeout=1200):
    prompt_file = pathlib.Path(__import__("tempfile").gettempdir(), prompt_name)
    prompt_file.write_text(prompt, encoding="utf-8")
    cmd = (
        f"set -a; source /etc/environment; set +a; "
        f"codex exec -C {shlex.quote(str(ROOT))} "
        f"--sandbox workspace-write -c sandbox_workspace_write.network_access=true "
        f"< {shlex.quote(str(prompt_file))}"
    )
    try:
        r = subprocess.run(
            cmd, shell=True, cwd=ROOT, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=timeout,
        )
        return r.stdout + "\n" + r.stderr, r.returncode
    except Exception as e:
        print(f"[research] codex 调用失败：{type(e).__name__}: {e}")
        return "", 1


def extract_json_obj(stdout):
    """从 codex 输出提取 JSON 对象。"""
    text = stdout or ""
    m = re.search(r"codex\n(.*)", text, re.S)
    if m:
        text = m.group(1)
    fences = re.findall(r"```json\s*(.*?)```", text, re.S)
    for f in fences:
        try:
            return json.loads(f.strip())
        except json.JSONDecodeError:
            continue
    dec = json.JSONDecoder()
    for m in re.finditer(r"\{", text):
        try:
            obj, _ = dec.raw_decode(text, m.start())
            if isinstance(obj, dict):
                return obj
        except json.JSONDecodeError:
            continue
    return {}


def apply_triage(candidates):
    """按 verdict 写入 articles.md。返回 (translate_n, index_n, observe_n)。"""
    art = ROOT / "references" / "articles.md"
    if not art.exists():
        print("[research] articles.md 不存在")
        return 0, 0, 0
    known = collect.existing_urls()
    t = art.read_text(encoding="utf-8")
    tn = ix = ob = 0
    today = datetime.date.today().isoformat()
    for c in candidates:
        url = (c.get("url") or "").strip()
        title = (c.get("title") or "").strip()
        if not url or not title:
            continue
        verdict = (c.get("verdict") or "observe").strip().lower()
        if verdict not in ("index", "translate", "observe"):
            verdict = "observe"
        lineage = (c.get("lineage") or "general").strip()
        reason = (c.get("reason") or "").strip()
        row = {
            "title": title,
            "url": url,
            "source": c.get("source") or "research",
            "date": c.get("date") or today,
        }
        if url in known and verdict != "translate":
            # 已在索引：跳过 index/observe；translate 仍可能已在队列
            print(f"[research] 去重跳过（{verdict}）：{title[:50]}")
            continue
        if verdict == "translate":
            if url in known:
                print(f"[research] 去重跳过（translate）：{title[:50]}")
                continue
            msg = collect.save_item("research", {**row, "title": title, "url": url})
            print(f"[research] translate → {msg}")
            if msg and msg.startswith("入队"):
                known.add(url)
                tn += 1
                t = art.read_text(encoding="utf-8")  # save_item 已写盘
            continue
        if url in known:
            print(f"[research] 去重跳过（{verdict}）：{title[:50]}")
            continue
        if verdict == "index":
            n = next_article_number(t)
            entry = fmt_article_entry(
                n, row, "已收录", moved_file=None,
                core=reason or title[:80], lineage=lineage,
            )
            t = append_numbered_entries(t, [entry])
            art.write_text(t, encoding="utf-8")
            known.add(url)
            ix += 1
            print(f"[research] index → #{n:02d} {title[:40]} ({lineage})")
            continue
        # observe
        t = append_observe_row(t, row, reason)
        art.write_text(t, encoding="utf-8")
        known.add(url)
        ob += 1
        print(f"[research] observe → {title[:40]}")
    return tn, ix, ob


def push_queue_branch():
    """把 articles（及 research 落盘）推到 pipeline/queue，不开 PR。"""
    sh("git add references/articles.md candidates 2>/dev/null || git add references/articles.md",
       check=False)
    changed = sh("git status --porcelain", check=False).stdout.strip()
    if not changed:
        print("[research] 无变更，跳过 push")
        return 0
    sh("git config user.name note-worker || true", check=False)
    sh("git config user.email note-worker@users.noreply.github.com || true", check=False)
    # 在当前 HEAD 上提交，再推送到 pipeline/queue
    r = sh('git commit -m "research: 情报搜索分流入队（无 PR）"', check=False)
    if r.returncode != 0 and "nothing to commit" not in (r.stdout + r.stderr):
        # 可能已在别处提交；继续尝试 push
        pass
    r = sh("git push --force-with-lease origin HEAD:pipeline/queue", check=False)
    if r.returncode != 0:
        print(f"[research] push pipeline/queue 失败：{r.stderr[-400:]}")
        return 1
    print("[research] 已推送 origin/pipeline/queue（不开 PR）")
    return 0


def main():
    lock = pathlib.Path(__import__("tempfile").gettempdir(), ".research.lock")
    if lock.exists():
        age = time.time() - lock.stat().st_mtime
        if age < 7200:  # 2h 内视为占用
            print("[research] 检测到运行中的 research 实例（锁存在），退出")
            return 0
        print(f"[research] 清除过期锁（age={int(age)}s）")
        lock.unlink(missing_ok=True)
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
    git_ref = os.environ.get("NOTE_GIT_REF", "main")
    if not args.dry_run:
        subprocess.run(f"git fetch origin {git_ref}", shell=True, cwd=ROOT,
                       capture_output=True, text=True)
        subprocess.run(f"git checkout {git_ref}", shell=True, cwd=ROOT,
                       capture_output=True, text=True)
        subprocess.run(f"git pull --rebase origin {git_ref}", shell=True, cwd=ROOT,
                       capture_output=True, text=True)
        # 若本地跟踪不到远程分支，硬对齐 origin/<ref>
        subprocess.run(f"git reset --hard origin/{git_ref}", shell=True, cwd=ROOT,
                       capture_output=True, text=True)

    known = known_content_block()
    search_tpl = (ROOT / "prompts" / "research-search.md").read_text(encoding="utf-8")
    # 去掉 YAML frontmatter，避免干扰模型
    if search_tpl.startswith("---"):
        search_tpl = re.sub(r"^---\s*\n.*?\n---\s*\n", "", search_tpl, count=1, flags=re.S)
    prompt_a = (search_tpl
                .replace("{START_DATE}", start.isoformat())
                .replace("{END_DATE}", today.isoformat())
                .replace("{KNOWN_CONTENT}", known)
                .replace("{MAX_ITEMS}", str(args.max)))

    if args.dry_run:
        snippet = prompt_a[:2000]
        try:
            print("[research] dry-run Prompt A（截断）：\n", snippet)
        except UnicodeEncodeError:
            sys.stdout.buffer.write(("[research] dry-run Prompt A:\n" + snippet + "\n").encode("utf-8", "replace"))
        return 0

    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = ROOT / "candidates" / f"research-{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)

    print("[research] Prompt A：搜索（要求调用 Firecrawl）…")
    stdout_a, rc_a = run_codex(prompt_a, ".research_search_prompt.md")
    (out_dir / "search.md").write_text(stdout_a, encoding="utf-8")
    if rc_a != 0:
        print(f"[research] Prompt A 失败 rc={rc_a}")
        print(stdout_a[-1500:])
        return rc_a

    analyze_tpl = (ROOT / "prompts" / "research-tracker.md").read_text(encoding="utf-8")
    if analyze_tpl.startswith("---"):
        analyze_tpl = re.sub(r"^---\s*\n.*?\n---\s*\n", "", analyze_tpl, count=1, flags=re.S)
    prompt_b = (analyze_tpl
                .replace("{SEARCH_OUTPUT}", stdout_a[-60000:])
                .replace("{KNOWN_CONTENT}", known))

    print("[research] Prompt B：长分析 + 三档分流…")
    stdout_b, rc_b = run_codex(prompt_b, ".research_analyze_prompt.md")
    (out_dir / "analyze.md").write_text(stdout_b, encoding="utf-8")
    if rc_b != 0:
        print(f"[research] Prompt B 失败 rc={rc_b}")
        print(stdout_b[-1500:])
        return rc_b

    data = extract_json_obj(stdout_b)
    cands = data.get("candidates") if isinstance(data, dict) else None
    if not isinstance(cands, list):
        # 兜底：尝试从 Prompt A JSON 取候选并默认 observe
        data_a = extract_json_obj(stdout_a)
        cands = data_a.get("candidates", []) if isinstance(data_a, dict) else []
        for c in cands:
            c.setdefault("verdict", "observe")
        print("[research] Prompt B JSON 解析失败，回退 A 候选且默认 observe")

    print(f"[research] 分流候选 {len(cands)} 条")
    tn, ix, ob = apply_triage(cands)
    print(f"[research] 完成：translate={tn} index={ix} observe={ob}")
    return push_queue_branch()


if __name__ == "__main__":
    sys.exit(main())
