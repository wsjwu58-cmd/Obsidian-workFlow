#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AI 加工（Ingest，深度技术笔记模板）。

对 raw/ 中 status=pending 的素材，调用 LLM（默认 DeepSeek）按 agents.md 的
「深度技术笔记模板」生成 expand 条目，写入对应分类目录，并同步 index.md / log.md /
raw 状态（status → processed + processed_hash）。

设计原则：
- 确定性逻辑在脚本：分类校验、文件名清洗、幂等、索引/日志写入、状态机
- 创造性内容交给 LLM：六维提炼、标签、链接选择
- 可回滚：本脚本不自动提交；在 Actions 中由 ingest.yml 提交到分支并开 PR

用法：
  python scripts/ingest.py                 # 处理所有 pending 素材
  python scripts/ingest.py --paths a.md    # 处理指定素材
  python scripts/ingest.py --dry-run       # 只生成不写入
  python scripts/ingest.py --force         # 忽略 status 强制处理
"""
import argparse
import datetime
import hashlib
import json
import os
import pathlib
import re
import sys
import time
import urllib.request

import firecrawl_search
import media

ROOT = pathlib.Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
EXPAND = ROOT / "expand"
RAW = ROOT / "raw"
INFRA = {"index.md", "log.md", "知识图谱.md",
         "自动化工作流设计.md", "自动化工作流功能与实现方案.md"}
INFRA |= {"动态索引.md", "知识库周报.md"}


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


def rewrite_fm(p, fm, body):
    lines = [f"{k}: {v}" for k, v in fm.items()]
    p.write_text("---\n" + "\n".join(lines) + "\n---\n" + body, encoding="utf-8")


def llm_json(system, user, max_tokens=6000, retries=3):
    key = os.environ.get("LLM_API_KEY", "")
    if not key:
        return None
    base = os.environ.get("LLM_BASE_URL", "https://api.deepseek.com/v1").rstrip("/")
    model = os.environ.get("LLM_MODEL", "deepseek-chat")
    body = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.4,
        "max_tokens": max_tokens,
        "stream": False,
    })
    req = urllib.request.Request(
        base + "/chat/completions",
        data=body.encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"},
    )
    last_err = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=240) as r:
                data = json.loads(r.read())
            return data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            last_err = e
            print(f"  LLM 调用失败（第 {attempt + 1} 次）：{type(e).__name__}，重试中…")
            time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"LLM 调用失败：{last_err}")


def extract_json(text):
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None


def top_categories():
    return sorted(p.name for p in EXPAND.iterdir()
                  if p.is_dir() and re.match(r"^\d{2}-", p.name))


def existing_entries():
    names = []
    for p in WIKI.rglob("*.md"):
        if p.name in INFRA:
            continue
        names.append(p.stem)
    if EXPAND.exists():
        for p in EXPAND.rglob("*.md"):
            if p.name in INFRA:
                continue
            names.append(p.stem)
    return sorted(set(names))


def rules_snippet():
    """从 agents.md 提取分类体系 + 深度技术笔记模板，作为 LLM 上下文"""
    text = read_text(ROOT / "agents.md")
    out = []
    grab = False
    for line in text.splitlines():
        if line.startswith("## 分类体系"):
            grab = True
        elif line.startswith("## 核心操作") or line.startswith("## 知识条目格式"):
            grab = False
        if grab:
            out.append(line)
    return "\n".join(out)


def search_context(title, max_results=None):
    """用素材标题经 Firecrawl 检索，返回可注入 Prompt 的完整原文（不截取）"""
    if os.environ.get("FIRECRAWL_SEARCH_DISABLED") == "1":
        return ""
    q = re.sub(r"\s+", " ", title or "")[:100]
    if not q:
        return ""
    max_results = max_results or int(os.environ.get("FIRECRAWL_SEARCH_COUNT", "3"))
    results = firecrawl_search.search(q, count=max_results)
    if not results:
        return ""
    lines = [
        "## 联网检索补充（Firecrawl Search，仅用于 [补充] 章节）",
        "以下为真实检索结果的完整原文（未截取）；引用时标注 [补充] 并附上来源 URL：",
        "",
    ]
    for i, r in enumerate(results, 1):
        lines.append(f"{i}. **{r['title']}**")
        lines.append(f"   URL: {r['url']}")
        content = r.get("markdown") or r.get("snippet") or ""
        if content:
            lines.append(f"   全文（{len(content)} 字符）：")
            lines.append(content)
        lines.append("")
    return "\n".join(lines)


def build_prompt(fm, body, search_text=""):
    title = fm.get("title", "")
    url = fm.get("url", "")
    source = fm.get("source", "")
    cats = "、".join(top_categories())
    entries = "、".join(existing_entries())
    rules = rules_snippet()
    template = """## 角色设定
你是一位精通 AI Agent 开发、Java/Kotlin 后端、KMP/Flutter 跨平台及 Android 原生开发的资深架构师。你的任务是将【原始素材】加工为一份深度技术笔记，目标是让读者 15 分钟内完全理解核心原理，并能在实际生产项目中直接应用。

## 加工规则
1. 强制补全与深度融合：素材浅薄、逻辑不完整或缺乏代码示例时，必须主动补充外部权威资料（官方文档、源码解析、最新架构演进），并直接融合进正文结构（概念拆解、方案对比、代码示例），不得仅作为附加说明。
2. 来源溯源：正文中融入补充内容时，必须在句末或段落末尾使用 [补充] 标签显式标识；笔记必须标注参考素材（raw 文件）与相关官方网站链接（专门的「参考素材与官方链接」章节）。
3. 人话解释：禁止直接复制学术化表述，所有核心技术概念必须给"一句话人话解释"（生活化类比或底层逻辑推演）。
4. 代码规范：涉及代码必须提供生产级最小可运行示例（含异常捕获、依赖版本锁定、安全边界），明确标注语言、框架及适用版本（如 "Kotlin 2.0 + KMP 1.9"）。
5. 工程视角：摒弃玩具级 Demo 思维，所有方案补充生产级落地考量（性能、安全、成本、异常处理）。
6. 排版要求：严格 Markdown，多用表格、列表和加粗，拒绝长篇大段的段落。

## 输出结构（不可省略任何章节）
## 本周主题：{动态提取主题}
### 一句话总结
> 不超过 50 字，高度概括素材核心价值与底层逻辑
### 记忆锚点（3 个关键记忆点）
1. 一句话记忆点（可含选型口诀）
### 核心概念拆解
- **概念名称**
  - 🗣️ 人话：通俗类比
  - 🔧 本质：底层原理一句话
  - 📍 定位：Agent/后端/KMP/Android 哪一环
  - 💡 补充：[补充]（附官方链接）
### 架构与方案对比（若有选型/架构内容）
- **决策流程图**：先用 Mermaid 画极简决策树（如"扫描件→上云；普通文件→本地"）
- 对比表：| 维度 | 方案A | 方案B | 方案C |（适用场景/核心优势/主要劣势/生产级成熟度（谨慎评级）/架构师推荐结论；[补充] 内容在单元格标注）
### 代码与实操速查
- 生产级最小示例（异常捕获/版本锁定/安全边界，[补充] 生成需标注）/ 关键配置（核心参数及含义）/ 常见报错与解决（Top 3）
### 避坑清单（Anti-patterns）
- 错误做法 → 正确做法（原因），至少 4 条（含大文件/内存、安全、依赖、性能类）
### 知识关联地图
- 前置知识 / 横向关联（[[条目]] #标签，可点击可检索）/ 纵向延伸（下一步方向 + 具体资源名称）
### 本周素材盲区与知识增量
- 原文盲区 → 转化为「下周探索方向」（候选选题）/ 知识增量总结（2-3 条额外收获）
### 参考素材与官方链接
- 原始素材：raw/xxx.md（来源 URL）
- 官方文档 / 网站链接列表（带用途说明）
### 本周行动清单
- [ ] 行动描述（预计耗时：xx分钟，关联知识点：xxx）✅ Done when：完成标准
### 相关条目
- [[相关条目A]]"""

    return f"""{template}

## 知识库分类体系（顶层，可带子目录）
{cats}

## 知识库现有条目（供知识关联地图引用，只从这些里选，也可不选）
{entries[:3000]}

{search_text}

## 原始素材
标题：{title}
来源：{url}（{source}）
素材正文：
{body[:14000]}

## 输出要求
只输出一个 JSON 对象，不要任何其他文字：
{{
  "category": "06-AI与LLM/Agent工具与平台",
  "filename": "条目文件名.md（简短描述性，不含路径）",
  "tags": ["内容标签", "type/论文|工具|教程", "status/待验证|已实践", "情绪标签"],
  "index_summary": "index.md 用的一句话摘要",
  "entry": "严格按上述「输出结构」生成的完整 Markdown 深度技术笔记（不要写 frontmatter，不要用代码块包裹）"
}}"""


def sanitize_filename(name):
    name = re.sub(r"[\\/:*?\"<>|\s]+", "-", name).strip("-")
    if not name.endswith(".md"):
        name += ".md"
    return name


def resolve_category(suggested):
    """校验/创建分类目录：顶层必须为 01-xx 格式；子目录按需创建"""
    parts = [p for p in (suggested or "").strip("/").split("/") if p]
    if not parts or not re.match(r"^\d{2}-", parts[0]):
        return None, "分类非法"
    top_dir = EXPAND / parts[0]
    top_dir.mkdir(exist_ok=True)
    cur = top_dir
    for sub in parts[1:]:
        cur = cur / re.sub(r"[\\/:*?\"<>|\s]+", "-", sub).strip("-")
        cur.mkdir(exist_ok=True)
    return cur, None


def update_index(top, line):
    p = EXPAND / "index.md"
    text = read_text(p)
    header = f"## {top}"
    if header in text:
        pos = text.index(header) + len(header)
        nl = text.find("\n\n", pos)
        if nl == -1:
            text += f"\n{line}\n"
        else:
            text = text[:nl + 2] + line + "\n" + text[nl + 2:]
    else:
        text += f"\n{header}\n\n{line}\n"
    m = re.search(r"全库共 (\d+) 个 Markdown 条目", text)
    if m:
        text = text.replace(m.group(0), f"全库共 {int(m.group(1)) + 1} 个 Markdown 条目")
    p.write_text(text, encoding="utf-8")


def update_log(created):
    p = EXPAND / "log.md"
    text = read_text(p)
    today = datetime.date.today().isoformat()
    section = f"## [{today}] ingest | 深度技术笔记模板加工 {len(created)} 条\n\n"
    for c in created:
        section += f"- 新增：[[{c['stem']}]]（{c['summary']}）\n"
    section += "\n"
    marker = "> 时间倒序排列\n"
    if marker in text:
        text = text.replace(marker, marker + "\n" + section, 1)
    else:
        text = section + text
    p.write_text(text, encoding="utf-8")


def process_one(p, dry_run, force, no_search):
    text = read_text(p)
    fm, body = parse_fm(text)
    if not force and fm.get("status", "").lower() != "pending":
        return None, "非 pending，跳过"
    if fm.get("translated") != "true" and len(body.strip()) < 300:
        return None, "素材过短（可能未抓全文），跳过"

    search_text = "" if no_search else search_context(fm.get("title", ""))
    out = llm_json("你是知识库管理助手，严格按用户要求输出 JSON。",
                   build_prompt(fm, body, search_text))
    if out is None:
        return None, "LLM 调用失败"
    data = extract_json(out)
    if not data or not data.get("entry"):
        return None, "LLM 输出非 JSON，跳过"

    category_dir, err = resolve_category(data.get("category", ""))
    if err:
        return None, err
    top = data.get("category", "").strip("/").split("/")[0]
    filename = sanitize_filename(data.get("filename", "未命名条目"))
    target = category_dir / filename
    if target.exists() and not force:
        return None, f"条目已存在：{target.relative_to(ROOT)}"

    today = datetime.date.today().isoformat()
    tags = data.get("tags", [])
    tags_line = "[" + ", ".join(tags) + "]" if tags else "[]"
    entry = media.localize_images(
        (data.get("entry") or "").strip(), fm.get("url", ""), target)
    entry_md = f"---\ncreated: {today}\nupdated: {today}\nsources: [{p.name}]\ntags: {tags_line}\n---\n\n{entry}\n"

    if dry_run:
        return target, f"[dry-run] 将写入 {target.relative_to(ROOT)}\n{entry_md[:400]}"

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(entry_md, encoding="utf-8")
    summary = data.get("index_summary", "") or ""
    line = f"- [[{target.stem}]]：{summary}"
    update_index(top, line)
    # raw 状态机
    fm["status"] = "processed"
    fm["processed_hash"] = hashlib.sha256(
        (p.name + body[:200]).encode("utf-8")).hexdigest()[:12]
    rewrite_fm(p, fm, body)
    return target, f"已生成 {target.relative_to(ROOT)}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--paths", nargs="*", help="指定 raw 素材；缺省处理所有 pending")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--no-search", action="store_true", help="禁用 Bing 联网检索")
    args = ap.parse_args()

    if args.paths:
        files = [pathlib.Path(p) for p in args.paths]
    else:
        files = [p for p in RAW.rglob("*.md") if p.name != "README.md"]

    created = []
    for p in files:
        target, msg = process_one(p, args.dry_run, args.force, args.no_search)
        print(f"[{p.name}] {msg}")
        if target and not args.dry_run:
            created.append({"stem": target.stem, "summary": ""})
    if created:
        update_log(created)
        print(f"完成：新增 {len(created)} 条（log.md 已同步）")
    else:
        print("完成：无新增（见上方原因）")


if __name__ == "__main__":
    sys.exit(main())
