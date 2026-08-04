#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""语义检索（F11）。

将 wiki/ 与 expand/ 向量化建立本地索引（SQLite），Query 按语义而非关键词检索。

- 首选：sentence-transformers（默认 BAAI/bge-small-zh-v1.5）生成 embedding；
  未安装或模型不可用时自动降级为 TF-IDF 余弦检索（仅标准库，无需联网）。
- 索引库：.semantic/index.sqlite（已 gitignore，不入仓）。

用法：
  python scripts/semantic_search.py --index [--rebuild]   # 建立/增量更新索引
  python scripts/semantic_search.py --query "Agent 记忆机制" [--top 5]
  python scripts/semantic_search.py --query "xxx" --top 5 --raw
"""
import argparse
import datetime
import importlib.util
import json
import math
import os
import pathlib
import re
import sqlite3
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
EXPAND = ROOT / "expand"
DB = ROOT / ".semantic" / "index.sqlite"

# 基础设施文档不参与索引（避免检索噪音）
INFRA = {"index.md", "log.md", "知识图谱.md",
         "自动化工作流设计.md", "自动化工作流功能与实现方案.md",
         "动态索引.md", "知识库周报.md"}

MODEL_AVAILABLE = importlib.util.find_spec("sentence_transformers") is not None
DEFAULT_MODEL = os.environ.get("SEMANTIC_MODEL", "BAAI/bge-small-zh-v1.5")


def read_text(p):
    return p.read_text(encoding="utf-8", errors="replace")


def doc_text(p):
    """提取正文：去掉 frontmatter 与代码块，压缩空白"""
    text = read_text(p)
    text = re.sub(r"^---\s*$.*?^---\s*$", "", text, flags=re.S | re.M)
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`\n]*`", " ", text)
    text = re.sub(r"\[\[([^\]|]+)(?:\|[^\]]*)?\]\]", r"\1", text)
    return re.sub(r"\s+", " ", text).strip()


def frontmatter(text):
    m = re.match(r"^---\s*$(.*?)^---\s*$", text, re.S | re.M)
    fm = {}
    if not m:
        return fm
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip().lower()] = v.strip().strip("\"'")
    return fm


def collect_docs():
    docs = []
    for base in (WIKI, EXPAND):
        if not base.exists():
            continue
        for p in base.rglob("*.md"):
            if p.name in INFRA:
                continue
            rel = str(p.relative_to(ROOT)).replace("\\", "/")
            content = doc_text(p)
            if len(content) < 20:
                continue
            fm = frontmatter(read_text(p))
            docs.append({
                "path": rel,
                "title": p.stem,
                "category": fm.get("category", str(p.parent.relative_to(ROOT)).replace("\\", "/")),
                "tags": fm.get("tags", ""),
                "content": content[:6000],
                "updated": datetime.date.today().isoformat(),
            })
    return docs


# ---------------- embedding（可选） ----------------

def load_model():
    if not MODEL_AVAILABLE:
        return None
    try:
        from sentence_transformers import SentenceTransformer
        print(f"加载 embedding 模型：{DEFAULT_MODEL}（首次运行会下载，之后缓存）")
        return SentenceTransformer(DEFAULT_MODEL)
    except Exception as e:
        print(f"embedding 模型加载失败，降级 TF-IDF：{type(e).__name__}: {e}")
        return None


def embed_batch(model, texts):
    if model is None:
        return None
    try:
        import numpy as np
        vecs = model.encode(texts, normalize_embeddings=True)
        return [np.asarray(v, dtype=np.float32).tobytes() for v in vecs]
    except Exception as e:
        print(f"embedding 计算失败，降级 TF-IDF：{type(e).__name__}: {e}")
        return None


# ---------------- TF-IDF（降级方案，纯标准库） ----------------

TOKEN_RE = re.compile(r"[A-Za-z0-9_]{2,}|[\u4e00-\u9fff]")


def tokens(text):
    text = text.lower()
    toks = TOKEN_RE.findall(text)
    cjk = [c for c in toks if len(c) == 1]
    bigrams = [a + b for a, b in zip(cjk, cjk[1:])]
    return [t for t in toks if len(t) > 1] + bigrams


def tfidf_index(contents):
    dfs = {}
    for c in contents:
        for t in set(tokens(c)):
            dfs[t] = dfs.get(t, 0) + 1
    n = len(contents)
    vecs = []
    for c in contents:
        counts = {}
        for t in tokens(c):
            counts[t] = counts.get(t, 0) + 1
        if not counts:
            vecs.append({})
            continue
        maxf = max(counts.values())
        vecs.append({t: 0.5 + 0.5 * (f / maxf) * math.log((1 + n) / (1 + dfs.get(t, 0)) + 1)
                     for t, f in counts.items()})
    return vecs


def cosine(a, b):
    if not a or not b:
        return 0.0
    common = set(a) & set(b)
    if not common:
        return 0.0
    dot = sum(a[t] * b[t] for t in common)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return dot / (na * nb) if na and nb else 0.0


# ---------------- SQLite ----------------

def init_db():
    DB.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB)
    con.execute("""
        CREATE TABLE IF NOT EXISTS docs (
            path TEXT PRIMARY KEY,
            title TEXT,
            category TEXT,
            tags TEXT,
            content TEXT,
            updated TEXT,
            embedding BLOB
        )
    """)
    return con


def cmd_index(rebuild):
    docs = collect_docs()
    if not docs:
        print("没有可索引的文档")
        return 1
    con = init_db()
    if rebuild:
        con.execute("DELETE FROM docs")
        con.commit()
    model = load_model()
    texts = [d["content"] for d in docs]
    emb = embed_batch(model, texts) if model is not None else None
    emb_fallback = None if emb is not None else tfidf_index(texts)

    added = updated = 0
    for i, d in enumerate(docs):
        row = con.execute("SELECT 1 FROM docs WHERE path=?", (d["path"],)).fetchone()
        embed_blob = emb[i] if emb is not None else None
        d["embedding"] = embed_blob
        if emb is None and emb_fallback is not None:
            d["embedding"] = json.dumps(emb_fallback[i]).encode("utf-8")
        if row:
            con.execute("""UPDATE docs SET title=?, category=?, tags=?, content=?,
                           updated=?, embedding=? WHERE path=?""",
                        (d["title"], d["category"], d["tags"], d["content"],
                         d["updated"], d["embedding"], d["path"]))
            updated += 1
        else:
            con.execute("""INSERT INTO docs (path, title, category, tags, content, updated, embedding)
                           VALUES (?,?,?,?,?,?,?)""",
                        (d["path"], d["title"], d["category"], d["tags"],
                         d["content"], d["updated"], d["embedding"]))
            added += 1
    con.commit()
    mode = "sentence-transformers" if emb is not None else "TF-IDF（降级）"
    print(f"索引完成：新增 {added}，更新 {updated}，共 {len(docs)} 篇（向量方式：{mode}）")
    con.close()
    return 0


def cmd_query(query, top, raw):
    con = init_db()
    rows = con.execute(
        "SELECT path, title, content, embedding FROM docs"
    ).fetchall()
    con.close()
    if not rows:
        print("索引为空，请先运行：python scripts/semantic_search.py --index")
        return 1

    model = load_model()
    if model is not None:
        try:
            import numpy as np
            qv = np.asarray(model.encode([query], normalize_embeddings=True)[0],
                            dtype=np.float32)
            scored = []
            for path, title, content, blob in rows:
                if not blob:
                    continue
                try:
                    dv = np.frombuffer(blob, dtype=np.float32)
                    if len(dv) != len(qv):
                        continue
                    score = float(dv @ qv)
                except Exception:
                    continue
                scored.append((score, path, title))
            scored.sort(key=lambda x: -x[0])
            use_emb = True
        except Exception as e:
            print(f"embedding 查询失败，降级 TF-IDF：{type(e).__name__}")
            use_emb = False
    else:
        use_emb = False

    if not use_emb:
        contents = [r[2] for r in rows]
        vecs = tfidf_index(contents)
        qv = tfidf_index([query])[0]
        scored = []
        for (path, title, content, _), v in zip(rows, vecs):
            scored.append((cosine(qv, v), path, title))
        scored.sort(key=lambda x: -x[0])

    print(f"\n语义检索：{query}（top {top}，方式：{'embedding' if use_emb else 'TF-IDF'}）\n")
    for score, path, title in scored[:top]:
        if raw:
            print(f"{score:.4f}\t{path}\t{title}")
        else:
            print(f"[{score:.3f}] {title}  （{path}）")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--index", action="store_true", help="建立/更新索引")
    ap.add_argument("--rebuild", action="store_true", help="重建索引（配合 --index）")
    ap.add_argument("--query", help="语义查询")
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--raw", action="store_true", help="输出 tab 分隔原始结果")
    args = ap.parse_args()

    if args.index:
        return cmd_index(args.rebuild)
    if args.query:
        return cmd_query(args.query, args.top, args.raw)
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
