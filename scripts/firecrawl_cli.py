#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""解析 Firecrawl CLI 在本机的可执行入口，供 Python 子进程调用。

Firecrawl CLI 通常以 npm 全局包安装：PATH 里只有 firecrawl.cmd（Windows），
Python 的 CreateProcess 无法直接执行 .cmd，因此解析出真实的
node + dist/index.js 入口，避免 WinError 2。
"""

import os
import pathlib
import re
import shutil


def _js_from_cmd(cmd_path):
    try:
        text = pathlib.Path(cmd_path).read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None
    m = re.search(r'"%dp0%\\([^"]+\.js)"', text)
    if not m:
        return None
    return str(pathlib.Path(cmd_path).parent / m.group(1))


def firecrawl_args():
    """返回调用 firecrawl 的子进程参数前缀（如 [node, 入口.js]）；找不到返回 None。"""
    exe = shutil.which("firecrawl")
    if not exe:
        for base in (pathlib.Path.home() / "AppData/Roaming/npm",
                     pathlib.Path.home() / ".npm-global"):
            p = base / "firecrawl.cmd"
            if p.exists():
                exe = str(p)
                break
    if not exe:
        return None
    if os.name == "nt" and exe.lower().endswith((".cmd", ".bat")):
        js = _js_from_cmd(exe)
        node = shutil.which("node")
        if js and node:
            return [node, js]
        return ["cmd", "/c", exe]
    return [exe]


if __name__ == "__main__":
    print(firecrawl_args())
