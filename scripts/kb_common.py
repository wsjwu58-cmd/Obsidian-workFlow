#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""curate 管道共享工具函数（curate.py / finalize.py 共用）。"""

import re


def make_slug(title):
    """标题 → 安全 slug。与 curate.py 传给 codex 的文件名 slug 保持一致，
    供 finalize 把 works-ready 文件名匹配回队列行。"""
    s = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", title)[:40].strip("-")
    return s or "item"
