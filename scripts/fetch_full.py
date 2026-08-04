#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全文抓取与翻译：
对 raw/ 中 status=pending 的素材，按来源/URL 类型抓取完整内容并翻译成简体中文，
回写为 Markdown 格式。

类型分发：
- github   → GitHub API 抓取 README
- arxiv    → ar5iv HTML 全文（失败回退原摘要）
- article  → trafilatura 正文提取（HN 与通用链接）
- youtube  → 字幕转录（youtube-transcript-api）
- bilibili → 字幕 API
- pdf      → pypdf 文本提取

翻译：可插拔后端（scripts/translator.py）——本地 MarianMT（零 token 成本）→
Google 免费翻译 → DeepSeek LLM 兜底；用环境变量 TRANSLATE_BACKEND=local|google|llm|auto
切换，翻译失败保留原文。
"""
import argparse
import datetime
import io
import json
import os
import pathlib
import re
import urllib.request

import translator

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"
UA = {"User-Agent": "Mozilla/5.0 (compatible; kb-collector/1.0)"}
MAX_TRANSLATE_CHARS = 60000
def http_get(url, timeout=30, headers=None, binary=False):
    req = urllib.request.Request(url, headers={**UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read()
    return data if binary else data.decode("utf-8", "ignore")


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


def rewrite(p, fm, body):
    lines = [f"{k}: {v}" for k, v in fm.items()]
    p.write_text("---\n" + "\n".join(lines) + "\n---\n" + body, encoding="utf-8")


def fetch_github_readme(url):
    m = re.match(r"https?://github\.com/([^/]+)/([^/]+)", url)
    if not m:
        return None
    owner, repo = m.group(1), m.group(2)
    api = f"https://api.github.com/repos/{owner}/{repo}/readme"
    headers = {"Accept": "application/vnd.github.raw+json"}
    token = os.environ.get("GH_PAT") or os.environ.get("GITHUB_TOKEN") or ""
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return http_get(api, headers=headers)


def fetch_article(url):
    import trafilatura
    # 用带超时的下载，避免外部站点无响应时挂死整个流水线
    downloaded = http_get(url, timeout=30)
    if not downloaded:
        return None
    return trafilatura.extract(downloaded, include_comments=False,
                               include_tables=True, output_format="markdown")


def fetch_arxiv(url):
    html_url = url.replace("arxiv.org/abs/", "ar5iv.labs.arxiv.org/html/")
    try:
        text = fetch_article(html_url)
        if text and len(text) > 500:
            return text
    except Exception as e:
        print(f"  ar5iv 失败：{e}")
    return None


def fetch_youtube(url):
    from youtube_transcript_api import YouTubeTranscriptApi
    m = re.search(r"(?:v=|youtu\.be/|shorts/)([A-Za-z0-9_-]{11})", url)
    if not m:
        return None
    api = YouTubeTranscriptApi()
    transcript = api.fetch(m.group(1))
    parts = [x["text"] for x in transcript.to_raw_data()]
    return "\n".join(parts)


def fetch_bilibili(url):
    m = re.search(r"(?:bilibili\.com/video/|b23\.tv/)(BV[0-9A-Za-z]+)", url)
    if not m:
        return None
    bvid = m.group(1)
    headers = {**UA, "Referer": "https://www.bilibili.com/"}
    info = json.loads(http_get(f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}",
                               headers=headers))
    cid = info["data"]["cid"]
    title = info["data"]["title"]
    player = json.loads(http_get(f"https://api.bilibili.com/x/player/v2?bvid={bvid}&cid={cid}",
                                 headers=headers))
    subs = player["data"].get("subtitle", {}).get("subtitles", [])
    if not subs:
        return f"视频标题：{title}\n\n（无可用字幕，建议人工补充内容）"
    sub_url = "https:" + subs[0]["subtitle_url"]
    data = json.loads(http_get(sub_url, headers=headers))
    lines = "\n".join(x["content"] for x in data["body"])
    return f"视频标题：{title}\n\n字幕内容：\n{lines}"


def fetch_pdf(url):
    from pypdf import PdfReader
    data = http_get(url, timeout=90, binary=True)
    reader = PdfReader(io.BytesIO(data))
    parts = []
    for page in reader.pages[:40]:
        t = page.extract_text() or ""
        if t.strip():
            parts.append(t)
    return "\n\n".join(parts) if parts else None


FETCHERS = {
    "github": fetch_github_readme,
    "arxiv": fetch_arxiv,
    "article": fetch_article,
    "youtube": fetch_youtube,
    "bilibili": fetch_bilibili,
    "pdf": fetch_pdf,
}


def classify(url, source):
    u = (url or "").lower()
    if "youtube.com" in u or "youtu.be" in u:
        return "youtube"
    if "bilibili.com" in u or "b23.tv" in u:
        return "bilibili"
    if source == "github" or u.startswith("https://github.com") or u.startswith("https://raw.githubusercontent.com"):
        return "github"
    if source == "arxiv" or "arxiv.org" in u:
        return "arxiv"
    if u.endswith(".pdf") or "/pdf/" in u or "arxiv.org/pdf" in u:
        return "pdf"
    return "article"


def write_full(p, fm, body, content):
    today = datetime.date.today().isoformat()
    title = fm.get("title", "")
    new_body = (f"# {title}\n\n"
                f"> 原文链接：{fm.get('url', '')}\n"
                f"> 全文抓取：{today}（已翻译）\n\n"
                f"{content.strip()}\n")
    fm["translated"] = "true"
    fm["updated"] = today
    rewrite(p, fm, new_body)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--paths", nargs="*", help="指定 raw 文件；缺省处理所有 pending 素材")
    ap.add_argument("--no-translate", action="store_true", help="只抓全文不翻译")
    ap.add_argument("--backend", default=None,
                    choices=["local", "google", "llm", "auto"],
                    help="翻译后端（缺省读 TRANSLATE_BACKEND，再缺省 auto）")
    ap.add_argument("--force", action="store_true", help="忽略 translated 标记，重新抓取/翻译")
    args = ap.parse_args()
    if args.backend:
        os.environ["TRANSLATE_BACKEND"] = args.backend

    if args.paths:
        files = [pathlib.Path(p) for p in args.paths]
    else:
        files = [p for p in RAW.rglob("*.md") if p.name != "README.md"]

    ok = fail = 0
    for p in files:
        text = read_text(p)
        fm, body = parse_fm(text)
        if not args.paths and fm.get("status", "").lower() not in ("pending", ""):
            continue
        if not args.force and fm.get("translated", "").lower() == "true":
            continue
        url = fm.get("url", "")
        source = fm.get("source", "")
        kind = classify(url, source)
        print(f"[{p.name}] 类型={kind}，抓取全文…")
        content = None
        try:
            content = FETCHERS.get(kind, fetch_article)(url)
        except Exception as e:
            print(f"  抓取失败：{type(e).__name__}: {e}")
        if content and isinstance(content, str) and len(content.strip()) < 200:
            content = None
        if content and not args.no_translate:
            print(f"  翻译中（{len(content)} 字符）…")
            zh = translator.translate_to_zh(content)
            if zh:
                content = zh
            else:
                print("  翻译失败，保留原文")
        if content:
            write_full(p, fm, body, content)
            ok += 1
            print(f"  完成：{p.name}")
        else:
            fail += 1
            print(f"  未能抓取全文，保留原摘要：{p.name}")
    print(f"全文抓取完成：成功 {ok}，失败/跳过 {fail}")


if __name__ == "__main__":
    main()
