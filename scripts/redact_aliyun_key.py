#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""阿里云 AccessKey 脱敏工具：
- extract 模式：从 stdin 的 Markdown 中提取 AccessKey ID/Secret（值独占一行），
  追加到 私密/阿里云AccessKey.md（只打印掩码，不泄露完整值）。
- redact 模式：把 wiki/ 下所有包含 AccessKey 块的 .md 替换为占位符（幂等，
  供 git filter-branch 的 --tree-filter 使用；不写私密目录）。
"""
import argparse
import datetime
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SECRET_FILE = ROOT / "私密" / "阿里云AccessKey.md"
PLACEHOLDER = "[已移至私密/阿里云AccessKey.md，请勿重新粘贴]"
HEADER_RE = re.compile(r"^\s*(?:#+|\*\*)?\s*AccessKey\s*(ID|Secret)\s*(?:\*\*)?\s*:?\s*$", re.I)
VALUE_RE = re.compile(r"^[ \t]*([A-Za-z0-9+/=]{16,64})[ \t]*$")


def find_blocks(text):
    """返回 [(kind, value), ...]"""
    lines = text.splitlines()
    blocks = []
    for i, line in enumerate(lines):
        m = HEADER_RE.match(line)
        if not m:
            continue
        kind = m.group(1).upper()
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        if j < len(lines):
            vm = VALUE_RE.match(lines[j].strip())
            if vm and not lines[j].strip().startswith("["):
                blocks.append((kind, vm.group(1)))
    return blocks


def redact_text(text):
    lines = text.splitlines(keepends=True)
    out = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        if HEADER_RE.match(line.strip()):
            out.append(line)
            i += 1
            # 该 AccessKey 段内（直到下一个头）的所有值行统一替换为占位符
            while i < n and not HEADER_RE.match(lines[i].strip()):
                val = lines[i].strip()
                if VALUE_RE.match(val) and not val.startswith("["):
                    out.append(lines[i].replace(val, PLACEHOLDER, 1))
                else:
                    out.append(lines[i])
                i += 1
            continue
        out.append(line)
        i += 1
    return "".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["extract", "redact"])
    ap.add_argument("--path", default=None, help="redact 模式指定文件；缺省扫描 wiki/")
    args = ap.parse_args()

    if args.mode == "extract":
        text = sys.stdin.read()
        blocks = find_blocks(text)
        if not blocks:
            print("extract: 未发现 AccessKey 块")
            return 0
        parts = [f"## 阿里云 AccessKey（{datetime.date.today().isoformat()} 从 wiki 移出）", ""]
        for kind, val in blocks:
            masked = val[:4] + "***" + val[-4:] if len(val) > 8 else "***"
            parts.append(f"- AccessKey {kind}：{val}")
            print(f"extract: AccessKey {kind} 已提取（{masked}）")
        parts.append("- ⚠️ 该密钥曾在 wiki 中明文保存并尝试推送，请到阿里云控制台吊销并重新创建")
        parts.append("")
        SECRET_FILE.parent.mkdir(parents=True, exist_ok=True)
        with SECRET_FILE.open("a", encoding="utf-8") as f:
            f.write("\n".join(parts))
        print(f"extract: 已追加到 {SECRET_FILE}")
        return 0

    targets = []
    if args.path:
        targets = [pathlib.Path(args.path).resolve()]
    else:
        # filter-branch 的 --tree-filter 在临时检出目录中运行，应基于 CWD 扫描
        targets = list(pathlib.Path("wiki").rglob("*.md"))
    for p in targets:
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        new = redact_text(text)
        if new != text:
            p.write_text(new, encoding="utf-8")
            print(f"redact: {p} 已脱敏")
    return 0


if __name__ == "__main__":
    sys.exit(main())
