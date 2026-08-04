#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""采集层：从 GitHub Search / HackerNews / ArXiv 抓取候选素材，写入 raw/。
粗滤（相关性关键词 + 垃圾特征）与 URL 去重在此完成；
内容去重与 LLM 打分由 filter.py 负责。
仅依赖标准库，可在 Actions（Linux）与本地（Windows）直接运行。
"""
import argparse
import datetime
import json
import os
import pathlib
import re
import urllib.parse
import urllib.request
import uuid

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"

# 相关性关键词：标题/描述命中任一即通过粗滤
KEYWORDS = [
    "ai", "agent", "llm", "rag", "mcp", "langchain", "langgraph", "fine-tun",
    "finetun", "prompt", "gpt", "claude", "deepseek", "ollama", "embedding",
    "vector db", "java", "kotlin", "python", "spring", "springboot", "mybatis",
    "redis", "mysql", "kafka", "rabbitmq", "rocketmq", "android", "backend",
    "微调", "智能体", "大模型", "后端", "数据库", "工作流",
]

# 垃圾/广告特征：命中即丢弃
JUNK = ["discount", "sale now", "促销", "特惠", "免费领取", "兼职", "刷单",
        "click here", "sign up now"]

UA = {"User-Agent": "Mozilla/5.0 (compatible; kb-collector/1.0)"}


def http_get(url, timeout=25, headers=None):
    req = urllib.request.Request(url, headers={**UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def coarse_filter(text):
    t = (text or "").lower()
    if any(j in t for j in JUNK):
        return False
    return any(k.lower() in t for k in KEYWORDS)


def existing_urls():
    urls = set()
    if RAW.exists():
        for p in RAW.rglob("*.md"):
            txt = p.read_text(encoding="utf-8", errors="ignore")
            m = re.search(r"^url:\s*(.+)$", txt, re.M)
            if m:
                urls.add(m.group(1).strip())
    return urls


def save_item(source, item):
    url = item["url"]
    title = item["title"]
    desc = item.get("desc", "")
    today = datetime.date.today().isoformat()
    fname = f"{source}-{today}-{uuid.uuid4().hex[:8]}.md"
    text = title + " " + desc
    hits = [k for k in KEYWORDS if k.lower() in text.lower()]
    score = min(5 + len(hits), 10)
    content = (
        f"---\n"
        f"source: {source}\n"
        f"url: {url}\n"
        f"title: {title}\n"
        f"collected: {today}\n"
        f"status: pending\n"
        f"score: {score}\n"
        f"tags: [{', '.join(hits[:5])}]\n"
        f"---\n\n"
        f"# {title}\n\n"
        f"> 来源：{source} | 采集日期：{today}\n\n"
        f"{desc}\n"
    )
    out = RAW / fname
    out.write_text(content, encoding="utf-8")
    return out


def fetch_github(max_items, token):
    """GitHub Search API：按 topic 逐项查询（qualifier 不支持 OR），按 stars 合并排序"""
    topics = ["ai-agent", "langchain", "rag", "mcp", "fine-tuning", "llm-agent"]
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    seen = {}
    for t in topics:
        url = ("https://api.github.com/search/repositories?" +
               urllib.parse.urlencode({"q": f"topic:{t}", "sort": "stars",
                                       "order": "desc", "per_page": 10}))
        data = json.loads(http_get(url, headers=headers))
        for r in data.get("items", []):
            seen.setdefault(r["html_url"], r)
    out = []
    for r in sorted(seen.values(), key=lambda x: -x.get("stargazers_count", 0))[:max_items]:
        desc = r.get("description") or ""
        out.append({
            "url": r["html_url"],
            "title": f"{r['full_name']} - {desc}",
            "desc": f"⭐ {r.get('stargazers_count', 0)} | {r.get('language') or '多语言'} | {desc}",
        })
    return out


def fetch_hn(max_items):
    """HackerNews 官方 Firebase API"""
    out = []
    ids = json.loads(http_get("https://hacker-news.firebaseio.com/v0/topstories.json"))
    for sid in ids[: max_items * 4]:
        item = json.loads(http_get(f"https://hacker-news.firebaseio.com/v0/item/{sid}.json"))
        if item and item.get("type") == "story" and item.get("title"):
            out.append({
                "url": item.get("url") or f"https://news.ycombinator.com/item?id={sid}",
                "title": item["title"],
                "desc": f"HN | score={item.get('score', 0)} | by {item.get('by', '')}",
            })
        if len(out) >= max_items:
            break
    return out


def fetch_arxiv(max_items):
    """ArXiv API（Atom 格式）"""
    import xml.etree.ElementTree as ET
    q = urllib.parse.quote('cat:cs.AI AND (agent OR RAG OR "fine-tuning" OR LLM OR MCP)')
    url = ("https://export.arxiv.org/api/query?"
           f"search_query={q}&sortBy=submittedDate&sortOrder=descending&max_results={max_items}")
    data = http_get(url)
    ns = {"a": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(data)
    out = []
    for e in root.findall("a:entry", ns):
        title = " ".join((e.findtext("a:title", default="", namespaces=ns) or "").split())
        summary = " ".join((e.findtext("a:summary", default="", namespaces=ns) or "").split())
        link = e.find("a:id", ns)
        out.append({
            "url": link.text if link is not None else "",
            "title": title,
            "desc": summary[:500],
        })
    return out


SOURCES = {"github": fetch_github, "hn": fetch_hn, "arxiv": fetch_arxiv}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sources", nargs="+", default=["github", "hn", "arxiv"])
    ap.add_argument("--max", type=int, default=10)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    RAW.mkdir(exist_ok=True)
    known = existing_urls()
    token = os.environ.get("GH_PAT") or os.environ.get("GITHUB_TOKEN") or ""
    new_count = skip_count = 0
    for src in args.sources:
        if src not in SOURCES:
            print(f"[{src}] 未知来源，跳过")
            continue
        try:
            if src == "github":
                items = SOURCES[src](args.max, token)
            else:
                items = SOURCES[src](args.max)
        except Exception as e:
            print(f"[{src}] 采集失败：{type(e).__name__}: {e}")
            continue
        for it in items:
            if not it.get("url") or not it.get("title"):
                continue
            if it["url"] in known:
                skip_count += 1
                continue
            if not coarse_filter(it["title"] + " " + it.get("desc", "")):
                continue
            if args.dry_run:
                print(f"[dry-run] {src}: {it['title'][:70]}")
            else:
                p = save_item(src, it)
                print(f"[{src}] 入库 {p.name}: {it['title'][:60]}")
                known.add(it["url"])
                new_count += 1
    print(f"采集完成：新增 {new_count} 条，URL 重复跳过 {skip_count} 条")


if __name__ == "__main__":
    main()
