#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""采集层：从 GitHub Search / HackerNews / ArXiv 抓取候选素材，写入 references/raw/。
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
ARTICLES = ROOT / "references" / "articles.md"

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
        "click here", "sign up now",
        "娱乐", "八卦", "综艺", "明星", "绯闻", "星座", "运势", "探店", "穿搭"]

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
    """去重权威：articles.md 编号正文全部 URL + 待处理队列 URL（防重复采集）"""
    urls = set()
    art = ROOT / "references" / "articles.md"
    if art.exists():
        t = art.read_text(encoding="utf-8", errors="ignore")
        urls.update(set(re.findall(r"https?://[^\s)\]|]+", t)))
    return urls


def save_item(source, item):
    """把新素材追加到 references/articles.md 的「待处理」队列（纯索引，不存正文）。

    返回 None（成功）或错误字符串。队列行格式（机器可读）：
      `| {标题} | {URL} | {来源} | {日期} |`
    """
    url = item["url"]
    title = item["title"].strip().replace("|", "/")[:120]
    today = datetime.date.today().isoformat()
    row = f"| {title} | {url} | {source} | {today} |"
    art = ARTICLES
    if not art.exists():
        return "references/articles.md 不存在，跳过"
    text = art.read_text(encoding="utf-8", errors="ignore")
    # 定位待处理队列区（<!-- pending:start --> ... <!-- pending:end -->）
    m_start = re.search(r"<!-- pending:start -->", text)
    m_end = re.search(r"<!-- pending:end -->", text)
    if not m_start or not m_end:
        return "articles.md 缺待处理队列标记，跳过"
    queue = text[m_start.end():m_end.start()]
    if url in existing_urls():
        return "URL 已在索引，跳过"
    # 追加一行，并更新队列计数「当前：N 条待处理」
    content = text[:m_end.start()] + row + "\n" + text[m_end.start():]
    cm = re.search(r"当前：(\d+) 条待处理", content)
    if cm:
        content = content.replace(cm.group(0), f"当前：{int(cm.group(1)) + 1} 条待处理", 1)
    art.write_text(content, encoding="utf-8")
    return f"入队 {url}"


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


RSSHUB_BASE = (os.environ.get("RSSHUB_BASE") or "https://hub.slarker.me").rstrip("/")
# RSSHub 国内源（二期）：掘金分类 / 知乎热榜。公共实例不稳定，失效时在仓库 Secret
# 设置 RSSHUB_BASE 指向自建实例（推荐 docker 部署 RSSHub）。
RSSHUB_FEEDS = [
    ("juejin-backend", "/juejin/category/backend"),
    ("juejin-ai", "/juejin/category/ai"),
    ("juejin-android", "/juejin/category/android"),
    ("zhihu-hot", "/zhihu/hot"),
]


def fetch_rsshub(max_items):
    """RSSHub 聚合：掘金分类 + 知乎热榜（Atom/RSS 兼容解析，仅标准库）"""
    import xml.etree.ElementTree as ET
    out = []
    for name, route in RSSHUB_FEEDS:
        url = RSSHUB_BASE + route
        try:
            data = http_get(url, timeout=30)
        except Exception as e:
            print(f"[rsshub:{name}] 抓取失败：{type(e).__name__}: {e}")
            continue
        try:
            root = ET.fromstring(data)
        except Exception:
            print(f"[rsshub:{name}] 解析失败")
            continue
        items = []
        # RSS 2.0
        for it in root.iter("item"):
            title = (it.findtext("title") or "").strip()
            link = (it.findtext("link") or "").strip()
            desc = re.sub(r"<[^>]+>", " ", it.findtext("description") or "").strip()
            desc = re.sub(r"\s+", " ", desc)[:500]
            if title and link:
                items.append({"title": title, "url": link, "desc": desc})
        # Atom
        ns = {"a": "http://www.w3.org/2005/Atom"}
        for e in root.findall(".//a:entry", ns):
            title = " ".join((e.findtext("a:title", default="", namespaces=ns) or "").split())
            link_el = e.find("a:link", ns)
            link = link_el.get("href", "") if link_el is not None else ""
            summary = e.findtext("a:summary", default="", namespaces=ns) or ""
            desc = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", summary)).strip()[:500]
            if title and link:
                items.append({"title": title, "url": link, "desc": desc})
        print(f"[rsshub:{name}] 候选 {len(items)} 条")
        out.extend(items)
        if len(out) >= max_items * 3:
            break
    return out[: max_items * 3]


SOURCES = {"github": fetch_github, "hn": fetch_hn, "arxiv": fetch_arxiv,
           "rsshub": fetch_rsshub}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sources", nargs="+", default=["github", "hn", "arxiv"])
    ap.add_argument("--max", type=int, default=10)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

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
                msg = save_item(src, it)
                print(f"[{src}] {msg}")
                if msg and msg.startswith("入队"):
                    known.add(it["url"])
                    new_count += 1
                elif msg and msg.startswith("URL"):
                    skip_count += 1
    print(f"采集完成：新增 {new_count} 条，URL 重复跳过 {skip_count} 条")


if __name__ == "__main__":
    main()
