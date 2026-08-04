#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AI 加工（Ingest，六维框架）。

对 raw/ 中 status=pending 的素材，调用 LLM（默认 DeepSeek）按 agents.md 的
「六维加工框架」生成 wiki 条目，写入对应分类目录，并同步 index.md / log.md /
raw 状态（status → processed + processed_hash）。

设计原则：
- 确定性逻辑在脚本：分类校验、文件名清洗、幂等、索引/日志写入、状态机
- 创造性内容交给 LLM：六维提炼、标签、链接选择
- 可回滚：本脚本不自动提交；在 Actions 中由 ingest.yml 提交到分支并开 PR

用法：
  python scripts/ingest.py                 # 处理所有 pending 素材
  python scripts/ingest.py --paths a.md    # 处理指定素材
  python scripts/ingest.py --dry-run       # 只生成不写入
  python scripts/ingest.py --force         # 忽略 status 强制处理
"""
import argparse
import datetime
import hashlib
import json
import os
import pathlib
import re
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
EXPAND = ROOT / "expand"
RAW = ROOT / "raw"
INFRA = {"index.md", "log.md", "知识图谱.md",
         "自动化工作流设计.md", "自动化工作流功能与实现方案.md"}


def read_text(p):
    return p.read_text(encoding="utf-8", errors="replace")


def parse_fm(text):
    m = re.match(r"^---\s*$(.*?)^---\s*$", text, re.S | re.M)
    fm = {}
    if not m:
        return fm, text
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip().lower()] = v.strip().strip("\"'")
    return fm, text[m.end():]


def rewrite_fm(p, fm, body):
    lines = [f"{k}: {v}" for k, v in fm.items()]
    p.write_text("---\n" + "\n".join(lines) + "\n---\n" + body, encoding="utf-8")


def llm_json(system, user, max_tokens=6000):
    key = os.environ.get("LLM_API_KEY", "")
    if not key:
        return None
    base = os.environ.get("LLM_BASE_URL", "https://api.deepseek.com/v1").rstrip("/")
    model = os.environ.get("LLM_MODEL", "deepseek-chat")
    body = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.4,
        "max_tokens": max_tokens,
        "stream": False,
    })
    req = urllib.request.Request(
        base + "/chat/completions",
        data=body.encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"},
    )
    with urllib.request.urlopen(req, timeout=240) as r:
        data = json.loads(r.read())
    return data["choices"][0]["message"]["content"].strip()


def extract_json(text):
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None


def top_categories():
    return sorted(p.name for p in EXPAND.iterdir()
                  if p.is_dir() and re.match(r"^\d{2}-", p.name))


def existing_entries():
    names = []
    for p in WIKI.rglob("*.md"):
        if p.name in INFRA:
            continue
        names.append(p.stem)
    if EXPAND.exists():
        for p in EXPAND.rglob("*.md"):
            if p.name in INFRA:
                continue
            names.append(p.stem)
    return sorted(set(names))


def rules_snippet():
    """从 agents.md 提取分类体系 + 六维加工框架，作为 LLM 上下文"""
    text = read_text(ROOT / "agents.md")
    out = []
    grab = False
    for line in text.splitlines():
        if line.startswith("## 分类体系"):
            grab = True
        elif line.startswith("## 核心操作") or line.startswith("## 知识条目格式"):
            grab = False
        if grab:
            out.append(line)
    return "\n".join(out)


def build_prompt(fm, body):
    title = fm.get("title", "")
    url = fm.get("url", "")
    source = fm.get("source", "")
    cats = "、".join(top_categories())
    entries = "、".join(existing_entries())
    rules = rules_snippet()
    return f"""你是个人知识库的管理助手。把下面的原始素材加工成符合知识库规则的结构化条目。

## 知识库分类体系（顶层，可带子目录）
{cats}

## 六维加工框架（来自 agents.md）
{rules[:4000]}

## 知识库现有条目（供 ## 相关条目 链接，只从这些里选，也可不选）
{entries[:3000]}

## 原始素材
标题：{title}
来源：{url}（{source}）
素材正文：
{body[:12000]}

## 输出要求
只输出一个 JSON 对象，不要任何其他文字：
{{
  "category": "06-AI与LLM/Agent工具与平台",
  "filename": "条目文件名.md（简短描述性，不含路径）",
  "tags": ["内容标签", "type/论文|工具|教程", "status/待验证|已实践", "情绪标签"],
  "index_summary": "index.md 用的一句话摘要",
  "entry": "完整 Markdown 条目（# 标题 + ## 检索问题（Q&A） + ## 结构化提炼 + ## 深度追问 + ## 联想与缝合 + ## 场景化转译 + ## 相关条目；不要写 frontmatter，不要用代码块包裹）"
}}"""


def sanitize_filename(name):
    name = re.sub(r"[\\/:*?\"<>|\s]+", "-", name).strip("-")
    if not name.endswith(".md"):
        name += ".md"
    return name


def resolve_category(suggested):
    """校验/创建分类目录：顶层必须为 01-xx 格式；子目录按需创建"""
    parts = [p for p in (suggested or "").strip("/").split("/") if p]
    if not parts or not re.match(r"^\d{2}-", parts[0]):
        return None, "分类非法"
    top_dir = EXPAND / parts[0]
    top_dir.mkdir(exist_ok=True)
    cur = top_dir
    for sub in parts[1:]:
        cur = cur / re.sub(r"[\\/:*?\"<>|\s]+", "-", sub).strip("-")
        cur.mkdir(exist_ok=True)
    return cur, None


def update_index(top, line):
    p = EXPAND / "index.md"
    text = read_text(p)
    header = f"## {top}"
    if header in text:
        pos = text.index(header) + len(header)
        nl = text.find("\n\n", pos)
        if nl == -1:
            text += f"\n{line}\n"
        else:
            text = text[:nl + 2] + line + "\n" + text[nl + 2:]
    else:
        text += f"\n{header}\n\n{line}\n"
    m = re.search(r"全库共 (\d+) 个 Markdown 条目", text)
    if m:
        text = text.replace(m.group(0), f"全库共 {int(m.group(1)) + 1} 个 Markdown 条目")
    p.write_text(text, encoding="utf-8")


def update_log(created):
    p = EXPAND / "log.md"
    text = read_text(p)
    today = datetime.date.today().isoformat()
    section = f"## [{today}] ingest | 自动化六维加工 {len(created)} 条\n\n"
    for c in created:
        section += f"- 新增：[[{c['stem']}]]（{c['summary']}）\n"
    section += "\n"
    marker = "> 时间倒序排列\n"
    if marker in text:
        text = text.replace(marker, marker + "\n" + section, 1)
    else:
        text = section + text
    p.write_text(text, encoding="utf-8")


def process_one(p, dry_run, force):
    text = read_text(p)
    fm, body = parse_fm(text)
    if not force and fm.get("status", "").lower() != "pending":
        return None, "非 pending，跳过"
    if fm.get("translated") != "true" and len(body.strip()) < 300:
        return None, "素材过短（可能未抓全文），跳过"

    out = llm_json("你是知识库管理助手，严格按用户要求输出 JSON。", build_prompt(fm, body))
    if out is None:
        return None, "LLM 调用失败"
    data = extract_json(out)
    if not data or not data.get("entry"):
        return None, "LLM 输出非 JSON，跳过"

    category_dir, err = resolve_category(data.get("category", ""))
    if err:
        return None, err
    top = data.get("category", "").strip("/").split("/")[0]
    filename = sanitize_filename(data.get("filename", "未命名条目"))
    target = category_dir / filename
    if target.exists() and not force:
        return None, f"条目已存在：{target.relative_to(ROOT)}"

    today = datetime.date.today().isoformat()
    tags = data.get("tags", [])
    tags_line = "[" + ", ".join(tags) + "]" if tags else "[]"
    entry_md = f"---\ncreated: {today}\nupdated: {today}\nsources: [{p.name}]\ntags: {tags_line}\n---\n\n{data['entry'].strip()}\n"

    if dry_run:
        return target, f"[dry-run] 将写入 {target.relative_to(ROOT)}\n{entry_md[:400]}"

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(entry_md, encoding="utf-8")
    summary = data.get("index_summary", "") or ""
    line = f"- [[{target.stem}]]：{summary}"
    update_index(top, line)
    # raw 状态机
    fm["status"] = "processed"
    fm["processed_hash"] = hashlib.sha256(
        (p.name + body[:200]).encode("utf-8")).hexdigest()[:12]
    rewrite_fm(p, fm, body)
    return target, f"已生成 {target.relative_to(ROOT)}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--paths", nargs="*", help="指定 raw 素材；缺省处理所有 pending")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    if args.paths:
        files = [pathlib.Path(p) for p in args.paths]
    else:
        files = [p for p in RAW.rglob("*.md") if p.name != "README.md"]

    created = []
    for p in files:
        target, msg = process_one(p, args.dry_run, args.force)
        print(f"[{p.name}] {msg}")
        if target and not args.dry_run:
            created.append({"stem": target.stem, "summary": ""})
    if created:
        update_log(created)
        print(f"完成：新增 {len(created)} 条（log.md 已同步）")
    else:
        print("完成：无新增（见上方原因）")


if __name__ == "__main__":
    sys.exit(main())
