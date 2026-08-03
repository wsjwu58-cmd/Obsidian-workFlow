#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""凭据扫描：在仓库文件中查找疑似密钥/Token，命中即非零退出。
跳过：私密/、.git、.claudian、二进制/图片等文件。
输出：类型 + 掩码后的值（不泄露完整密钥）。
"""
import argparse
import pathlib
import re
import sys

EXCLUDE_DIRS = {".git", "私密", ".claudian", "node_modules", "__pycache__",
                ".venv", "venv", ".idea", ".vscode"}
SKIP_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".webp",
                 ".pdf", ".chm", ".chw", ".base", ".zip", ".7z", ".gz", ".db",
                 ".exe", ".dll", ".ttf", ".woff", ".woff2"}

PATTERNS = [
    ("GitHub Token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
    ("API Key (sk-)", re.compile(r"\bsk-[A-Za-z0-9]{20,}\b")),
    ("AWS Access Key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Google API Key", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b")),
    ("Slack Token", re.compile(r"\bxox[baprs]-[0-9A-Za-z_\-]{10,}\b")),
    ("Private Key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("Generic Secret 赋值", re.compile(
        r"(?i)\b(?:api[_-]?key|apikey|access[_-]?token|secret[_-]?key|client[_-]?secret)"
        r"\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}")),
]


def mask(value: str) -> str:
    return value[:4] + "***" + value[-4:] if len(value) > 10 else "***"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", default=".", help="要扫描的根目录")
    args = ap.parse_args()
    root = pathlib.Path(args.path)
    findings = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if any(part in EXCLUDE_DIRS for part in p.parts):
            continue
        if p.suffix.lower() in SKIP_SUFFIXES:
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for name, rx in PATTERNS:
            for m in rx.finditer(text):
                findings.append((str(p), m.start(), name, mask(m.group(0))))
    if findings:
        for f, pos, name, val in findings:
            print(f"{f}:{pos} [{name}] {val}")
        print(f"发现 {len(findings)} 处疑似凭据，请处理后再提交。")
        return 1
    print("OK：未发现疑似凭据。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
