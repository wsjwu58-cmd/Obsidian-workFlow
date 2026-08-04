#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Firecrawl 联网搜索（替代 Bing Search API）。

对查询执行 `firecrawl search --scrape`，返回每条结果的**完整页面原文**
（不截断），并过滤掉娱乐/杂谈等非技术类结果，保证 [补充] 素材的技术属性。

调用方（ingest.py）:
    import firecrawl_search
    results = firecrawl_search.search("LangChain RAG", count=3)
    # results[i] = {title, url, snippet, markdown(全文)}

环境变量:
    FIRECRAWL_SEARCH_COUNT   默认返回条数（默认 3，最大 10）
    FIRECRAWL_SEARCH_COUNTRY 搜索地区（默认 US；zh-* 市场自动映射为 CN）
    FIRECRAWL_SEARCH_DISABLED=1 时静默跳过搜索（等价于 --no-search）
"""

import hashlib
import json
import os
import pathlib
import re
import subprocess
import urllib.parse

import firecrawl_cli

ROOT = pathlib.Path(__file__).resolve().parent.parent
CACHE_DIR = ROOT / ".firecrawl"

# 技术关键词：标题 / 摘要 / 正文开头命中任一即视为技术内容
TECH_KEYWORDS = [
    "ai", "agent", "llm", "rag", "mcp", "langchain", "langgraph", "llamaindex",
    "fine-tun", "finetun", "prompt", "gpt", "claude", "deepseek", "ollama",
    "embedding", "vector", "微调", "智能体", "大模型", "机器学习", "深度学习",
    "神经网络", "transformer", "模型", "算法", "编程", "代码", "开发", "架构",
    "开源", "源码", "教程", "框架", "数据库", "后端", "前端", "java", "kotlin",
    "python", "golang", "rust", "typescript", "javascript", "spring",
    "springboot", "mybatis", "redis", "mysql", "postgres", "kafka",
    "rabbitmq", "rocketmq", "android", "flutter", "kubernetes", "docker",
    "devops", "git", "linux", "shell", "安全", "逆向", "渗透", "论文",
    "research", "github", "api", "sdk", "部署", "云原生", "数据库",
]

# 娱乐 / 杂谈特征：标题命中即丢弃（避免把"技术杂谈"等误杀，不列入"杂谈"）
JUNK_KEYWORDS = [
    "娱乐", "八卦", "综艺", "明星", "绯闻", "影视", "电影", "电视剧",
    "星座", "运势", "情感", "探店", "穿搭", "美容", "健身", "段子",
    "笑话", "搞笑", "粉丝", "应援", "娱乐圈", "名媛", "豪门",
]

# 明确非技术类站点（整站排除）
JUNK_DOMAINS = {
    "weibo.com", "douyin.com", "kuaishou.com", "tiktok.com",
    "iqiyi.com", "youku.com", "mgtv.com", "sohu.com",
}

# URL 中的娱乐特征（拼音/英文，如搜狐的 yule-nav 频道）
JUNK_URL_PATTERNS = ["yule", "entertainment", "gossip", "celeb"]


def _domain(url):
    return urllib.parse.urlparse(url or "").netloc.lower()


def is_technical(item):
    """返回 (是否技术类, 丢弃原因)。判定顺序：站点黑名单 → 标题娱乐词 → 技术关键词命中。"""
    url = item.get("url", "") or ""
    title = item.get("title", "") or ""
    desc = item.get("description", "") or ""
    md = item.get("markdown", "") or ""
    domain = _domain(url)
    if any(domain == d or domain.endswith("." + d) for d in JUNK_DOMAINS):
        return False, "站点非技术类"
    if any(p in url.lower() for p in JUNK_URL_PATTERNS):
        return False, "URL 含娱乐特征"
    head = title.lower()
    if any(k in head for k in JUNK_KEYWORDS):
        return False, "标题含娱乐特征"
    probe = (title + " " + desc[:600] + " " + md[:1200]).lower()
    if not any(k.lower() in probe for k in TECH_KEYWORDS):
        return False, "无技术关键词"
    return True, ""


def _run(query, count, country):
    CACHE_DIR.mkdir(exist_ok=True)
    digest = hashlib.sha1(query.encode("utf-8")).hexdigest()[:12]
    tmp = CACHE_DIR / f"search-{digest}-{os.getpid()}.json"
    prefix = firecrawl_cli.firecrawl_args()
    if not prefix:
        print("  [firecrawl-search] 未找到 firecrawl CLI（请先安装/配置）")
        return None
    cmd = prefix + [
        "search", query,
        "--limit", str(count),
        "--scrape",
        "--json",
        "--ignore-invalid-urls",
        "-o", str(tmp),
    ]
    if country:
        cmd += ["--country", country]
    try:
        r = subprocess.run(
            cmd, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=240,
        )
    except Exception as e:
        print(f"  [firecrawl-search] 调用失败：{type(e).__name__}: {e}")
        return None
    if r.returncode != 0 or not tmp.exists():
        tail = (r.stderr or "")[-400:]
        print(f"  [firecrawl-search] 搜索失败：{tail}")
        return None
    try:
        return json.loads(tmp.read_text(encoding="utf-8", errors="replace"))
    finally:
        tmp.unlink(missing_ok=True)


def search(query, count=None, market="zh-CN"):
    """搜索并返回完整结果；自动过滤非技术类。"""
    if os.environ.get("FIRECRAWL_SEARCH_DISABLED") == "1":
        return []
    count = count or int(os.environ.get("FIRECRAWL_SEARCH_COUNT", "3"))
    count = max(1, min(int(count), 10))
    country = os.environ.get("FIRECRAWL_SEARCH_COUNTRY", "")
    if not country and market:
        country = "CN" if str(market).lower().startswith("zh") else "US"
    data = _run(query, count, country)
    if not data:
        return []
    out = []
    for item in data.get("data", {}).get("web", []):
        ok, reason = is_technical(item)
        if not ok:
            print(f"  [firecrawl-search] 已过滤（{reason}）："
                  f"{(item.get('title') or '')[:40]} | {item.get('url', '')}")
            continue
        out.append({
            "title": item.get("title") or "",
            "url": item.get("url") or "",
            "snippet": item.get("description") or "",
            "markdown": item.get("markdown") or "",
        })
    return out


if __name__ == "__main__":
    import sys
    q = " ".join(sys.argv[1:]) or "LLM agent RAG"
    for i, r in enumerate(search(q), 1):
        md = r.get("markdown") or r.get("snippet") or ""
        print(f"{i}. {r['title']}\n   {r['url']}\n   全文长度：{len(md)} 字符")
    print(f"\n（技术过滤后共 {len(search(q))} 条）")
