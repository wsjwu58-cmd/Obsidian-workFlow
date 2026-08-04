#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""将 私密/API密钥.md 中已填写的值写入 GitHub Actions Secrets。

读取格式（每行一个，冒号或等号分隔，`#` 开头为注释）：
  LLM_API_KEY: sk-xxx
  LLM_BASE_URL: https://api.deepseek.com/v1
  LLM_MODEL: deepseek-chat
  BING_SEARCH_API_KEY: xxx
  BING_SEARCH_ENDPOINT: https://api.bing.microsoft.com/v7.0/search
  GH_PAT: ghp_xxx
  NOTIFY_WEBHOOK: https://sctapi.ftqq.com/xxx.send

只设置已填写且长度 >= 8 的项；缺失项仅提示名称，绝不打印任何值。
依赖 gh CLI 登录态（gh auth status）；仓库默认从 git remote origin 解析。
"""
import argparse
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_FILE = ROOT / "私密" / "API密钥.md"

RECOGNIZED = {
    "LLM_API_KEY", "LLM_BASE_URL", "LLM_MODEL",
    "BING_SEARCH_API_KEY", "BING_SEARCH_ENDPOINT",
    "GH_PAT", "NOTIFY_WEBHOOK",
}


def parse_keys(text):
    keys = {}
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        m = re.match(r"^([A-Z][A-Z0-9_]*)\s*[:=]\s*(.*)$", s)
        if m:
            keys[m.group(1)] = m.group(2).strip()
    return keys


def repo_from_git():
    try:
        out = subprocess.run(["git", "remote", "get-url", "origin"],
                             capture_output=True, text=True, cwd=ROOT).stdout.strip()
        m = re.search(r"(?:github\.com[:/]|git@github\.com:)([^/\s]+/[^/\s]+?)(?:\.git)?$", out)
        if m:
            return m.group(1)
    except Exception:
        pass
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default=str(DEFAULT_FILE), help="密钥文件路径")
    ap.add_argument("--repo", default=None, help="owner/repo；缺省从 git remote 解析")
    args = ap.parse_args()

    path = pathlib.Path(args.file)
    if not path.exists():
        print(f"未找到密钥文件：{path}（可先创建模板，填写后重跑）")
        return 1
    repo = args.repo or repo_from_git()
    if not repo:
        print("无法解析 GitHub 仓库（owner/repo），请用 --repo 指定")
        return 1

    keys = parse_keys(path.read_text(encoding="utf-8", errors="replace"))
    set_ok, missing, skipped = [], [], []
    for name in sorted(RECOGNIZED):
        val = keys.get(name, "")
        if len(val) >= 8:
            r = subprocess.run(["gh", "secret", "set", name, "--repo", repo],
                               input=val.encode("utf-8"), capture_output=True)
            if r.returncode == 0:
                set_ok.append(name)
            else:
                skipped.append((name, r.stderr.decode("utf-8", "replace").strip()))
        else:
            missing.append(name)

    print(f"仓库：{repo}")
    print(f"已设置：{', '.join(set_ok) if set_ok else '无'}")
    print(f"未填写（跳过）：{', '.join(missing) if missing else '无'}")
    for name, err in skipped:
        print(f"设置失败：{name} -> {err}")
    return 0 if not skipped else 2


if __name__ == "__main__":
    sys.exit(main())
