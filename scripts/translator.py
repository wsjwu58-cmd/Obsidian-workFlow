#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""可插拔的翻译后端（替代纯 LLM 翻译，节省 token 开销）。

后端（环境变量 TRANSLATE_BACKEND，默认 auto）：
  local  → 本地 MarianMT（Helsinki-NLP/opus-mt-en-zh，离线、零 token 成本；
            依赖 transformers + torch，见 requirements-semantic.txt）
  google → 免费 Google 翻译（deep-translator，轻量、零成本；国内网络/云端 IP 可能受限）
  llm    → DeepSeek 等 OpenAI 兼容接口（质量最高，兜底）
  auto   → 按 local → google → llm 顺序自动选择可用后端

用法：
  python scripts/translator.py --text "Hello world"
  python scripts/translator.py --file note.txt --backend local
"""
import argparse
import json
import os
import pathlib
import re
import sys
import urllib.request

MAX_TRANSLATE_CHARS = int(os.environ.get("TRANSLATE_MAX_CHARS", "60000"))

_LOCAL_MODEL_NAME = os.environ.get("TRANSLATE_LOCAL_MODEL",
                                   "Helsinki-NLP/opus-mt-en-zh")


def is_mostly_chinese(text, threshold=0.3):
    """正文 CJK 占比高于阈值则视为已中文化，无需翻译"""
    letters = sum(1 for ch in text if ch.isalpha())
    if not letters:
        return False
    cjk = sum(1 for ch in text if "\u4e00" <= ch <= "\u9fff")
    return cjk / letters > threshold


def split_chunks(text, size=4500):
    chunks, cur, n = [], [], 0
    for para in text.split("\n"):
        cur.append(para)
        n += len(para) + 1
        if n >= size:
            chunks.append("\n".join(cur))
            cur, n = [], 0
    if cur:
        chunks.append("\n".join(cur))
    return chunks


# ---------------- 后端：本地 MarianMT ----------------

_LOCAL = {"model": None, "tokenizer": None, "ready": False, "failed": False}


def _load_local():
    if _LOCAL["ready"] or _LOCAL["failed"]:
        return _LOCAL["ready"]
    try:
        from transformers import MarianMTModel, MarianTokenizer
        import torch
        print(f"  加载本地翻译模型 {_LOCAL_MODEL_NAME}（首次运行会下载，之后缓存）…")
        _LOCAL["tokenizer"] = MarianTokenizer.from_pretrained(_LOCAL_MODEL_NAME)
        _LOCAL["model"] = MarianMTModel.from_pretrained(_LOCAL_MODEL_NAME)
        _LOCAL["model"].eval()
        _LOCAL["ready"] = True
        _LOCAL["torch"] = torch
    except Exception as e:
        _LOCAL["failed"] = True
        print(f"  本地翻译模型不可用（{type(e).__name__}），切换其它后端")
    return _LOCAL["ready"]


def _local_translate(text):
    if not _load_local():
        return None
    tokenizer, model = _LOCAL["tokenizer"], _LOCAL["model"]
    # 按句切分，控制单批 token 量；小批量生成以提升 CPU 吞吐
    sentences = re.split(r"(?<=[.!?。！？])\s*|\n+", text)
    batch, size, results = [], 0, []
    for s in sentences:
        s = s.strip()
        if not s:
            continue
        batch.append(s)
        size += len(s)
        if size >= 1400:
            results.extend(_local_batch(tokenizer, model, batch))
            batch, size = [], 0
    if batch:
        results.extend(_local_batch(tokenizer, model, batch))
    return "\n".join(results)


def _local_batch(tokenizer, model, sentences):
    tok = tokenizer(sentences, return_tensors="pt", padding=True,
                    truncation=True, max_length=512)
    with _LOCAL["torch"].no_grad():
        gen = model.generate(**tok, max_new_tokens=512)
    return tokenizer.batch_decode(gen, skip_special_tokens=True)


# ---------------- 后端：Google 免费翻译 ----------------

def _google_available():
    try:
        import deep_translator  # noqa: F401
        return True
    except Exception:
        return False


def _google_translate(text):
    if not _google_available():
        print("  未安装 deep-translator（pip install deep-translator），跳过 google 后端")
        return None
    from deep_translator import GoogleTranslator
    tr = GoogleTranslator(source="en", target="zh-CN")
    out = []
    for c in split_chunks(text):
        for attempt in range(3):
            try:
                out.append(tr.translate(c))
                break
            except Exception as e:
                print(f"  google 翻译第 {attempt + 1} 次失败：{type(e).__name__}")
                if attempt == 2:
                    return None
    return "\n\n".join(out)


# ---------------- 后端：LLM（兜底） ----------------

def _llm_available():
    return bool(os.environ.get("LLM_API_KEY"))


def _llm_translate(text):
    if not _llm_available():
        return None
    key = os.environ.get("LLM_API_KEY", "")
    base = os.environ.get("LLM_BASE_URL", "https://api.deepseek.com/v1").rstrip("/")
    model = os.environ.get("LLM_MODEL", "deepseek-chat")
    system = ("你是专业的技术文档翻译。把英文内容翻译成简体中文，"
              "保持 Markdown 结构、代码块、链接、列表、专业术语不变。只输出译文，不要解释。")
    out = []
    for c in split_chunks(text):
        body = json.dumps({
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": f"原文：\n\n{c}"},
            ],
            "temperature": 0.3,
            "max_tokens": 3000,
            "stream": False,
        })
        req = urllib.request.Request(
            base + "/chat/completions",
            data=body.encode("utf-8"),
            headers={"Content-Type": "application/json",
                     "Authorization": f"Bearer {key}"},
        )
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                data = json.loads(r.read())
            out.append(data["choices"][0]["message"]["content"].strip())
        except Exception as e:
            print(f"  LLM 翻译失败：{type(e).__name__}: {e}")
            return None
    return "\n\n".join(out)


BACKENDS = {
    "local": _local_translate,
    "google": _google_translate,
    "llm": _llm_translate,
}
AUTO_ORDER = ("local", "google", "llm")


def translate_to_zh(text, backend="auto"):
    """把英文/外文内容翻译成简体中文；失败或已中文化时返回 None/原文"""
    text = (text or "").strip()
    if not text:
        return None
    if len(text) > MAX_TRANSLATE_CHARS:
        text = text[:MAX_TRANSLATE_CHARS] + "\n\n（内容过长，已截断翻译）"
    if is_mostly_chinese(text):
        return text
    if backend == "auto":
        for b in AUTO_ORDER:
            out = BACKENDS[b](text)
            if out:
                return out
        return None
    fn = BACKENDS.get(backend)
    if not fn:
        print(f"未知翻译后端：{backend}（可用：local / google / llm / auto）")
        return None
    return fn(text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", help="待翻译文本")
    ap.add_argument("--file", help="读取文件内容翻译")
    ap.add_argument("--backend", default=os.environ.get("TRANSLATE_BACKEND", "auto"),
                    choices=["local", "google", "llm", "auto"])
    args = ap.parse_args()
    if args.file:
        text = pathlib.Path(args.file).read_text(encoding="utf-8", errors="replace")
    else:
        text = args.text
    if not text:
        ap.error("请提供 --text 或 --file")
    out = translate_to_zh(text, backend=args.backend)
    if out is None:
        print("翻译失败", file=sys.stderr)
        return 1
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
