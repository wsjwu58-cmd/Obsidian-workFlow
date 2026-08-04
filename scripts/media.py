#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""图片本地化工具：把 Markdown 里的远程图片下载到 D:\note\assets\，
并把链接改写为相对路径，解决外链图片无法显示 / 防盗链 / 相对路径缺失等问题。

供 fetch_full.py 与 ingest.py 共用；对 raw 与 expand 条目都生效。
重复 URL 通过内容哈希去重，同图不重复下载。

环境变量:
    LOCALIZE_IMAGE_MAX  单篇最多下载图片数（默认 30）
"""

import hashlib
import os
import pathlib
import re
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT / "assets"

UA = {"User-Agent": "Mozilla/5.0 (compatible; kb-collector/1.0)"}
IMG_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
LOCAL_ASSET_RE = re.compile(r"^(?:\.\./)*assets/[^/]+$")
MAX_IMAGES = int(os.environ.get("LOCALIZE_IMAGE_MAX", "30"))

_EXT_MAP = {"svg+xml": "svg", "x-icon": "ico", "jpeg": "jpg", "vnd.microsoft.icon": "ico"}


def ensure_assets():
    ASSETS_DIR.mkdir(exist_ok=True)
    return ASSETS_DIR


def _relative_link(md_file, name):
    rel = os.path.relpath(ASSETS_DIR, md_file.parent)
    return rel.replace("\\", "/") + "/" + name


def _ext_from_url(url):
    ext = pathlib.Path(urllib.parse.urlparse(url).path).suffix.lower()
    return ext if ext in {
        ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".ico",
        ".avif", ".bmp", ".jfif",
    } else ""


def _download(url, referer):
    """下载图片，返回 (文件名, 字节)；失败返回 None。"""
    headers = dict(UA)
    if referer:
        headers["Referer"] = referer
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=25) as r:
        data = r.read()
    if len(data) < 64:
        return None  # 过小响应：占位图 / 防盗链占位 / 错误页
    ext = _ext_from_url(url)
    if not ext:
        ctype = (r.headers.get("Content-Type") or "").lower()
        m = re.search(r"image/([\w.+-]+)", ctype)
        if m:
            ext = "." + _EXT_MAP.get(m.group(1), m.group(1).split(".")[-1])
    if not ext:
        ext = ".img"
    name = hashlib.sha1(url.encode("utf-8")).hexdigest()[:16] + ext
    return name, data


def localize_images(md, page_url="", md_file=None, max_images=MAX_IMAGES):
    """把 md 中远程图片下载到 assets/ 并改写为相对路径；已本地化的链接只重算相对路径。"""
    if not md or md_file is None:
        return md
    md_file = pathlib.Path(md_file)
    ensure_assets()
    base = (page_url or "").strip()
    count = 0
    out_lines = []
    in_code = False

    def repl(m):
        nonlocal count
        if count >= max_images:
            return m.group(0)
        alt, link = m.group(1), m.group(2).strip()
        if LOCAL_ASSET_RE.match(link):
            name = link.rsplit("/", 1)[-1]
            return f"![{alt}]({_relative_link(md_file, name)})"
        if link.startswith(("data:", "mailto:", "#")):
            return m.group(0)
        if link.startswith(("http://", "https://")):
            url = link
        elif base:
            # 相对路径图片：以页面 URL 为基准解析为绝对地址
            url = urllib.parse.urljoin(base, link)
        else:
            return m.group(0)
        try:
            got = _download(url, base or None)
        except Exception as e:
            print(f"  [media] 图片下载失败：{url}（{type(e).__name__}: {e}）")
            return m.group(0)
        if not got:
            return m.group(0)
        name, data = got
        dest = ASSETS_DIR / name
        if not dest.exists():
            dest.write_bytes(data)
        count += 1
        return f"![{alt}]({_relative_link(md_file, name)})"

    for line in md.split("\n"):
        if line.lstrip().startswith("```"):
            in_code = not in_code
            out_lines.append(line)
            continue
        if in_code or line.startswith("    ") or line.startswith("\t"):
            out_lines.append(line)
            continue
        out_lines.append(IMG_RE.sub(repl, line))
    return "\n".join(out_lines)


if __name__ == "__main__":
    import sys
    print(localize_images(sys.stdin.read(), "https://example.com/", pathlib.Path("raw/demo.md"))[:2000])
