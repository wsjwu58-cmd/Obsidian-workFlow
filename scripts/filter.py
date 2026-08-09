#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""过滤层：对 references/raw/ 中 status=pending 的素材执行
1) 标题相似度去重（4-gram Jaccard >= 0.85 视为重复，标记 rejected）
2) 可选 LLM 三维打分（相关性/深度/新鲜度，pass 且 total>=threshold 才保留）
   LLM 不可用时回退启发式 score（collect.py 已写入）。
仅依赖标准库。
"""
import argparse
import datetime
import json
import os
import pathlib
import re
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "references" / "raw"


def read_text(p):
    return p.read_text(encoding="utf-8", errors="replace")


def norm(s):
    return re.sub(r"[^0-9A-Za-z\u4e00-\u9fff]", "", (s or "").lower())


def shingles(s, n=4):
    s = norm(s)
    return {s[i:i + n] for i in range(max(0, len(s) - n + 1))}


def jaccard(a, b):
    sa, sb = shingles(a), shingles(b)
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


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


def llm_score(title, url, desc):
    key = os.environ.get("LLM_API_KEY", "")
    if not key:
        return None
    base = os.environ.get("LLM_BASE_URL", "https://api.deepseek.com/v1").rstrip("/")
    model = os.environ.get("LLM_MODEL", "deepseek-chat")
    prompt = f"""你是技术内容审核助手。对以下内容进行 3 维度评分（每项 0-10）：

标题：{title}
摘要：{desc[:800]}
来源：{url}

1. 相关性：是否涉及 AI 应用 / Agent 智能体 / 后端开发（Java/Kotlin/Python/Android）？
2. 技术深度：是否包含可操作的技术方案而非泛泛而谈？
3. 新鲜度：相对当前日期 {datetime.date.today().isoformat()} 是否是新信息？

纯广告/纯标题党/低质水文 → pass=false。
只输出 JSON：{{"pass": true/false, "relevance": 0-10, "depth": 0-10, "freshness": 0-10, "total": 0-10, "reason": "一句话"}}"""
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
    })
    req = urllib.request.Request(
        base + "/chat/completions",
        data=body.encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            data = json.loads(r.read())
        txt = data["choices"][0]["message"]["content"]
        m = re.search(r"\{.*\}", txt, re.S)
        return json.loads(m.group(0))
    except Exception as e:
        print(f"LLM 打分失败（回退启发式）：{type(e).__name__}: {e}")
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--threshold", type=int, default=7, help="总分低于该值标记 rejected")
    args = ap.parse_args()

    files = [p for p in RAW.rglob("*.md") if p.name != "README.md"]
    pending = []
    for p in files:
        fm, _ = parse_fm(read_text(p))
        if fm.get("status", "").lower() == "pending":
            pending.append(p)
    if not pending:
        print("过滤：无待处理素材")
        return 0

    rejected_dup = 0
    rejected_low = 0
    kept = 0
    for p in pending:
        text = read_text(p)
        fm, body = parse_fm(text)
        title = fm.get("title", "")
        # 标题去重：与其他非 rejected 素材比较
        dup = False
        for q in files:
            if q == p:
                continue
            fmq, _ = parse_fm(read_text(q))
            if fmq.get("status", "").lower() in ("rejected", "processed"):
                continue
            if jaccard(title, fmq.get("title", "")) >= 0.85:
                dup = True
                break
        if dup:
            fm["status"] = "rejected"
            fm["reason"] = "标题相似度过高（疑似重复）"
            rewrite(p, fm, body)
            rejected_dup += 1
            print(f"rejected(重复): {p.name}")
            continue

        result = llm_score(title, fm.get("url", ""), body)
        if result is not None:
            total = float(result.get("total", 0))
            passed = bool(result.get("pass", False)) and total >= args.threshold
            fm["score"] = str(int(total))
            fm["reason"] = str(result.get("reason", ""))[:120]
        else:
            total = float(fm.get("score", 5))
            passed = total >= args.threshold
        if passed:
            fm["status"] = "pending"  # 保持待加工
            kept += 1
        else:
            fm["status"] = "rejected"
            fm.setdefault("reason", f"评分 {total} 低于阈值 {args.threshold}")
            rejected_low += 1
        rewrite(p, fm, body)
        print(f"{'保留' if passed else 'rejected(低分)'}: {p.name} (score={total})")

    print(f"过滤完成：保留 {kept}，重复拒绝 {rejected_dup}，低分拒绝 {rejected_low}")


if __name__ == "__main__":
    main()
