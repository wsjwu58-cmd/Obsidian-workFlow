#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bing Web Search API v7 封装（供 ingest.py 联网检索 [补充] 素材）。

配置：
  BING_SEARCH_API_KEY   必填，Azure Bing Search 资源密钥
  BING_SEARCH_ENDPOINT  可选，默认 https://api.bing.microsoft.com/v7.0/search

未配置密钥或调用失败时返回空列表（调用方优雅降级为模型内部知识）。
"""
import json
import os
import urllib.parse
import urllib.request

DEFAULT_ENDPOINT = "https://api.bing.microsoft.com/v7.0/search"


def search(query, count=5, market="zh-CN"):
    key = os.environ.get("BING_SEARCH_API_KEY", "")
    if not key:
        return []
    endpoint = os.environ.get("BING_SEARCH_ENDPOINT", DEFAULT_ENDPOINT)
    params = urllib.parse.urlencode({
        "q": query,
        "count": count,
        "mkt": market,
        "responseFilter": "Webpages",
    })
    req = urllib.request.Request(
        f"{endpoint}?{params}",
        headers={
            "Ocp-Apim-Subscription-Key": key,
            "User-Agent": "Mozilla/5.0 (compatible; kb-collector/1.0)",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read())
    except Exception as e:
        print(f"  [bing] 检索失败：{type(e).__name__}: {e}")
        return []
    out = []
    for item in data.get("webPages", {}).get("value", []):
        out.append({
            "title": item.get("name", ""),
            "url": item.get("url", ""),
            "snippet": item.get("snippet", ""),
        })
    return out


if __name__ == "__main__":
    import sys
    q = " ".join(sys.argv[1:]) or "LLM agent"
    results = search(q)
    for i, r in enumerate(results, 1):
        print(f"{i}. {r['title']}\n   {r['url']}\n   {r['snippet'][:150]}")
    if not results:
        print("（无结果或未配置 BING_SEARCH_API_KEY）")
