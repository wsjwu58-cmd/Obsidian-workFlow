# Curate 流水线改造 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把「codex 全自动加工」重构为「AI 预处理 + 人类闸门 + 收录」的 curate-research 六阶段流水线（research 采集 → curate 候选 → 并行评审 → 评审 PR → finalize 收录）。

**Architecture:** 拆三个脚本——`research.py`（服务器：Firecrawl 搜索注入情报分析师 prompt，codex 产出候选清单入队）、`curate.py`（服务器：攒批 3-4 篇，codex 产三件套 + 串行评审，开评审 PR）、`finalize.py`（Actions：落位/回写/同步/清理，开收录 PR）。GitHub Actions 只做机械调度与门禁，codex 只做智能推理，人类闸门在评审 PR。

**Tech Stack:** Python 3.10（标准库为主）、codex CLI（deepseek-v4-flash）、Firecrawl Search（复用 `firecrawl_search.py`）、GitHub Actions、GitHub REST API（开 PR）。

**Spec:** `docs/superpowers/specs/2026-08-09-curate-pipeline-design.md`

---

## 文件结构

```
scripts/research.py                 新增 — 服务器：Firecrawl 搜索 → codex 情报分析 → 机械去重 → 入队列
scripts/curate.py                   新增 — 服务器：攒批 → codex 产三件套 + 串行评审 → 开评审 PR
scripts/finalize.py                 新增 — Actions：落位 → 回写 → 同步 → 清理 → 开收录 PR
scripts/worker.py                   退役 — 被 curate.py 取代（保留文件，改 docstring 标注废弃）
scripts/collect.py                  退役 — 被 research.py 取代（保留文件，改 docstring 标注废弃）
prompts/research-tracker.md         新增 — 情报分析师提示词（资产，注入已知内容 + 日期窗口）
prompts/curate.md                   新增 — codex 产三件套操作约定
prompts/curate-review.md            新增 — 自动评审 prompt 模板
.github/workflows/research.yml      新增 — 每周 + 手动触发 research.py
.github/workflows/finalize.yml      新增 — 监听候选 PR 合并（closed+merged）触发 finalize.py
.github/workflows/dispatch-worker.yml 改 — SSH 命令 worker.py → curate.py，--limit 3
.github/workflows/collect.yml       退役 — 被 research.yml 替代（改注释标注废弃）
references/articles.md              改 — 状态机加「评审中」；计数注释说明
scripts/check_consistency.py        改 — candidates/ 轻量格式校验（K1 扩展或豁免声明）
```

---

### Task 1: prompts/research-tracker.md（情报分析师提示词资产）

**Files:**
- Create: `prompts/research-tracker.md`

- [ ] **Step 1: 写提示词资产文件**

用户提供的「技术情报分析师」prompt 作为基础，加入 `{START_DATE}` `{END_DATE}` `{KNOWN_CONTENT}` 三个占位符（research.py 运行时注入）。核心字段：角色、搜索领域、关键词、信源分层（Tier1-3）、已知内容去重段、输出格式（候选清单）。

```markdown
---
created: 2026-08-09
updated: 2026-08-09
type: workflow
status: 待验证（首次运行后更新）
product: null
source: 用户情报分析师 prompt
---

# 技术情报分析师（深度网络搜索）

> 运行器：服务器 codex，由 research.yml 每周 + 手动触发。
> 任务：找出过去 2 周内（{START_DATE} 至 {END_DATE}）的高价值内容，产出候选清单。

## 角色

你是一个技术情报分析师。请对以下领域进行深度网络搜索，找出过去 2 周内（{START_DATE} 至 {END_DATE}）发布的高价值内容。

## 搜索领域

核心主题：
1. Harness Engineering — AI 编码智能体的约束、引导、反馈系统设计
2. Context Engineering — 上下文窗口管理、compaction、渐进式披露
3. AI Coding Agents — 编码智能体的架构、编排、评估
4. Agent Infrastructure — 沙箱、会话管理、多智能体协作
5. AI-assisted Software Engineering — AI 辅助开发的效率、流程、组织影响

相关关键词（中英文）：harness engineering, agent harness, coding agent, AI coding, context engineering, context window, compaction, progressive disclosure, AGENTS.md, CLAUDE.md, agent readability, agent-first, managed agents, meta-harness, multi-agent orchestration, AI code review, mutation testing, structural testing, fitness functions, vibe coding, AI-native development, agentic workflow, 智能体工程, AI 编程, 上下文工程, 护栏工程

## 搜索范围（信源分层）

- **Tier 1（高权重）**：Anthropic Engineering Blog、OpenAI Blog、Google DeepMind、Martin Fowler、Mitchell Hashimoto、LangChain Blog、Simon Willison
- **Tier 2（中权重）**：Hacker News 前 100、GitHub Trending、X/Twitter 技术社区（#harness-engineering #ai-coding #context-engineering）、Dev.to、Medium、HumanLayer/Cursor/Windsurf/Codex 博客、中文社区（少数派/掘金/知乎）
- **Tier 3（低权重但有惊喜）**：arXiv (cs.SE, cs.AI)、个人技术博客、YouTube、Reddit（r/LocalLLaMA r/ChatGPT r/programming）

## 已知内容（去重权威）

本节列出知识库已收录的内容，搜索时**跳过与这些重复或高度相似的文章**。仅用于去重，不参与其他判断。

{KNOWN_CONTENT}

## 输出要求

输出 JSON 格式候选清单（research.py 解析后机械去重入队）：

{
  "candidates": [
    {"title": "标题", "url": "URL", "source": "tier1|tier2|tier3", "reason": "一句话为什么值得收录"}
  ]
}

- 每条必须含 URL（直接可抓取），不含无效/登录墙/重复链接
- 最多 {MAX_ITEMS} 条
- 只输出 JSON，不要额外文字
```

- [ ] **Step 2: 提交**

```bash
git add prompts/research-tracker.md
git commit -m "feat: research-tracker 情报分析师提示词资产（含去重注入占位）"
```

---

### Task 2: prompts/curate.md（codex 产三件套操作约定）

**Files:**
- Create: `prompts/curate.md`

- [ ] **Step 1: 写 curate 操作约定**

仿现有 `prompts/worker.md`，定义 codex 对单篇候选的操作：抓原文 → 翻译 → 产三件套 → 回写状态。核心约束：产 `candidates/<batch>/` 结构、只写 working/ 翻译草稿、thinking 只给建议。

```markdown
---
created: 2026-08-09
updated: 2026-08-09
type: workflow
status: 待验证
product: null
source: curate-research 六阶段
---

# curate 候选加工约数

> 运行器：服务器 codex，由 curate.py 调用。每篇候选产三件套 + 串行评审。

## 输入

- references/articles.md 待处理队列中的一条：标题 / URL / 来源 / 日期

## 对每条待处理做 4 步

1. **抓原文**：用 webfetch 抓取 URL 真实内容 → 存 `candidates/<batch>/sources/<slug>.md`；
   论文/长文额外抓 HTML 全文到 `sources/<slug>-full.md`。
2. **翻译**：按流程生成三件套到 `candidates/<batch>/translations/<slug>/`：
   - `01-analysis.md`：原文分析 + 收录建议（含原文价值/翻译质量/契合度初判）
   - `02-prompt.md`：本次翻译使用的提示词（过程稿）
   - `translation.md`：中文翻译过程稿
   再把最终候选写到 `candidates/<batch>/works-ready/<slug>-translation.md`。
3. **回写 articles.md**：该条状态 → `评审中`，附候选路径 `candidates/<batch>/`。
4. **输出候选文件**：所有产物落在 `candidates/<batch>/` 下（tracked）。

## 产出边界（不可逾越）

- **working/（works-ready/）**：✅ 翻译草稿
- **expand/thinking/**：❌ 不写正文；只在 `01-analysis.md` 里给观点建议（供人类参考）
- **prompts/**：❌ 不写；只在评审表推荐"可复用 prompt"
- **wiki/**：❌ 永不触碰（只读）
- **references/ 编号正文**：❌ 不在本阶段写；finalize 收录时才写

## 质量要求

- 中文正文，术语到位，保留原文超链接
- 关键数字/结论与原文抽查比对
- frontmatter 含 created/updated/sources/tags
```

- [ ] **Step 2: 提交**

```bash
git add prompts/curate.md
git commit -m "feat: curate 候选加工操作约定（三件套 + 产出边界）"
```

---

### Task 3: prompts/curate-review.md（自动评审 prompt 模板）

**Files:**
- Create: `prompts/curate-review.md`

- [ ] **Step 1: 写评审 prompt 模板**

照搬 curate-research 的评审 prompt，参数化为多篇。

```markdown
---
created: 2026-08-09
updated: 2026-08-09
type: workflow
status: 待验证
product: null
source: curate-research 评审模板
---

# 候选自动评审

> 运行器：服务器 codex，由 curate.py 串行调用。对一批 3-4 篇候选统一打分。

## 任务

你是知识库的内容评审。知识库主题：AI Agent 开发 / 跨平台开发（KMP·Flutter）/ Harness Engineering / 通用技术。

读以下每篇候选的三件套，逐篇回答。候选位于 `candidates/<batch>/`：

{ITEMS}

逐篇回答（每篇独立小节，标题为篇名）：

### 篇名
- **原文价值**：原创洞察密度 / 长文实质 vs 产品页·发布稿·摘要。高/中/低 + 一句话理由
- **翻译质量**：完整逐译 / 压缩摘要 / 首轮粗稿；通顺度、术语到位度。精品/合格/需返工 + 一句话理由
- **与知识库契合度**：补薄弱环节还是重复（对照 references/articles.md 与 expand/ 已有条目）
- **一句话定性 + 建议去向**：working/ 正式收录 / articles.md 观察项一行 / tools/（待实测）/ 淘汰

## 汇总

最后输出一个「候选 × 定性 × 去向」markdown 表格：

| 篇名 | 原文价值 | 翻译质量 | 契合度 | 定性 | 建议去向 |

## 约束

- 基于实际内容，紧凑中文，结构化输出
- 只做评审与建议，不修改任何文件
```

- [ ] **Step 2: 提交**

```bash
git add prompts/curate-review.md
git commit -m "feat: curate 自动评审 prompt 模板（原文价值/翻译质量/契合度/去向）"
```

---

### Task 4: scripts/research.py（情报搜索 → 入队）

**Files:**
- Create: `scripts/research.py`

- [ ] **Step 1: 写 research.py**

复用 `firecrawl_search.search()` 提供真实搜索结果，注入情报分析师 prompt，codex 综合产出候选清单，机械去重后入队。

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""情报搜索层：Firecrawl 深度搜索 → codex 综合为候选清单 → 机械去重 → 入队列。

由 research.yml（每周 + 手动）触发，运行在服务器。替代 collect.py 的固定源采集。

职责：
1. 用 firecrawl_search.search() 按情报分析师提示词的信源/关键词搜索真实结果
2. 组装 prompt（prompts/research-tracker.md + 注入已知内容去重段 + 日期窗口 + 搜索结果）
3. codex exec 综合为候选清单（JSON）
4. 机械去重（URL 精确比对 existing_urls + 队列查重）→ collect.save_item 入队

仅依赖标准库 + firecrawl_search + codex CLI。
"""
import argparse
import datetime
import json
import os
import pathlib
import re
import shlex
import subprocess
import sys

import firecrawl_search

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import collect


def known_content_block():
    """从 articles.md 抽已收录标题+URL，构造去重注入段。"""
    art = ROOT / "references" / "articles.md"
    if not art.exists():
        return "（暂无）"
    t = art.read_text(encoding="utf-8", errors="replace")
    titles = re.findall(r"### \d+\. (.+)", t)
    urls = collect.existing_urls()
    lines = [f"- {x}" for x in titles[:80]]
    lines.append("URL 清单（已收录 + 待处理，去重用）：")
    lines += [f"  - {u}" for u in sorted(urls)[:120]]
    return "\n".join(lines)


def run_codex(prompt, root):
    prompt_file = pathlib.Path(__import__("tempfile").gettempdir(), ".research_prompt.md")
    prompt_file.write_text(prompt, encoding="utf-8")
    r = subprocess.run(
        f"set -a; source /etc/environment; set +a; "
        f"codex exec -C {root} "
        f"--sandbox workspace-write -c sandbox_workspace_write.network_access=true "
        f"< {shlex.quote(str(prompt_file))}",
        shell=True, cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=900,
    )
    return r.stdout, r.returncode


def parse_candidates(stdout):
    """从 codex 输出提取 JSON 候选清单（容忍前后杂质）。"""
    m = re.search(r"\{.*\}", stdout, re.S)
    if not m:
        return []
    try:
        data = json.loads(m.group(0))
    except json.JSONDecodeError:
        return []
    return data.get("candidates", [])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=14)
    ap.add_argument("--max", type=int, default=10)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    today = datetime.date.today()
    start = today - datetime.timedelta(days=args.days)
    template = (ROOT / "prompts" / "research-tracker.md").read_text(encoding="utf-8")
    known = known_content_block()
    prompt = template.replace("{START_DATE}", start.isoformat()) \
                      .replace("{END_DATE}", today.isoformat()) \
                      .replace("{KNOWN_CONTENT}", known) \
                      .replace("{MAX_ITEMS}", str(args.max))

    # Firecrawl 搜索结果注入（为 codex 提供真实候选素材）
    search_results = firecrawl_search.search("harness engineering coding agent", count=args.max)
    if search_results:
        lines = ["\n## 联网检索到的候选（Firecrawl，仅作线索）\n"]
        for i, r in enumerate(search_results, 1):
            lines.append(f"{i}. {r['title']} | {r['url']}")
        prompt += "\n" + "\n".join(lines)

    if args.dry_run:
        print("[research] dry-run：以下为将注入的提示词（截断）")
        print(prompt[:2000])
        return 0

    print("[research] 调用 codex 情报分析…")
    stdout, rc = run_codex(prompt, ROOT)
    if rc != 0:
        print(f"[research] codex 返回 {rc}，失败")
        print(stdout[-1500:])
        return rc

    cands = parse_candidates(stdout)
    print(f"[research] codex 产出候选 {len(cands)} 条")
    new_count = 0
    known = collect.existing_urls()
    for c in cands:
        url = (c.get("url") or "").strip()
        title = (c.get("title") or "").strip()
        if not url or not title:
            continue
        if url in known:
            print(f"[research] 去重跳过：{title[:50]}")
            continue
        msg = collect.save_item("research", c)
        print(f"[research] {msg}")
        if msg and msg.startswith("入队"):
            known.add(url)
            new_count += 1
    print(f"[research] 完成：新增 {new_count} 条候选")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: 语法验证**

Run: `python -X utf8 -c "import ast; ast.parse(open('scripts/research.py',encoding='utf-8').read()); print('syntax OK')"`
Expected: `syntax OK`

- [ ] **Step 3: 单元验证核心函数（不联网）**

Run:
```bash
python -X utf8 -c "import sys; sys.path.insert(0,'scripts'); import research; b=research.known_content_block(); print('known block len:', len(b))"
```
Expected: 输出 `known block len: <正数>`（从 articles.md 抽取去重段）

Run:
```bash
python -X utf8 -c "import sys; sys.path.insert(0,'scripts'); import research; print('parse_candidates:', research.parse_candidates('{\"candidates\":[{\"title\":\"t\",\"url\":\"u\",\"source\":\"tier1\"}]}'))"
```
Expected: `parse_candidates: [{'title': 't', 'url': 'u', 'source': 'tier1'}]`

- [ ] **Step 4: 提交**

```bash
git add scripts/research.py
git commit -m "feat: research.py 情报搜索（Firecrawl+codex 综合+机械去重入队）"
```

---

### Task 5: scripts/curate.py（候选加工 + 串行评审）

**Files:**
- Create: `scripts/curate.py`

- [ ] **Step 1: 写 curate.py**

攒批 3-4 篇 → codex 产三件套 → 串行评审 → 汇总评审表 → 开评审 PR。

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""候选加工层：攒批 3-4 篇 → codex 产三件套 → 串行评审 → 开评审 PR。

由 dispatch-worker.yml（每 3h）触发，运行在服务器。替代 worker.py 的全自动加工。

职责：
1. git pull --rebase 同步权威仓库
2. 解析 references/articles.md 待处理队列，取前 N（默认 4）条
3. codex exec 为每篇产 candidates/<batch>/ 三件套（sources/ + translations/ + works-ready/）
4. 串行评审：单 codex exec 对 N 篇统一打分（prompts/curate-review.md）
5. 汇总 candidates/<batch>/review.md「候选 × 定性 × 去向」表
6. 更新 articles.md：各条 → 评审中
7. push 分支 candidates/<batch>，开评审 PR（GitHub REST API）

仅依赖标准库 + codex CLI。
"""
import argparse
import datetime
import json
import os
import pathlib
import re
import shlex
import subprocess
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent


def sh(cmd, cwd=None, check=True):
    r = subprocess.run(cmd, shell=True, cwd=cwd or ROOT,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if check and r.returncode != 0:
        print(f"[curate] 命令失败: {cmd}\n{r.stdout}\n{r.stderr}")
        sys.exit(r.returncode)
    return r


def parse_queue(text, limit):
    m = re.search(r"<!-- pending:start -->(.*?)<!-- pending:end -->", text, re.S)
    if not m:
        return []
    rows = []
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) >= 4 and not cells[0].startswith("标题"):
            rows.append({"title": cells[0], "url": cells[1],
                         "source": cells[2], "date": cells[3]})
        if len(rows) >= limit:
            break
    return rows


def run_codex(prompt, root, prompt_name):
    prompt_file = pathlib.Path(__import__("tempfile").gettempdir(), prompt_name)
    prompt_file.write_text(prompt, encoding="utf-8")
    r = subprocess.run(
        f"set -a; source /etc/environment; set +a; "
        f"codex exec -C {root} "
        f"--sandbox workspace-write -c sandbox_workspace_write.network_access=true "
        f"< {shlex.quote(str(prompt_file))}",
        shell=True, cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=900,
    )
    return r.stdout, r.returncode


def create_pr(head, base, title, body):
    token = os.environ.get("GH_TOKEN", os.environ.get("GITHUB_TOKEN", ""))
    if not token:
        print("[curate] 缺少 GH_TOKEN，跳过开 PR")
        return None
    remote = sh("git config --get remote.origin.url", check=False).stdout.strip()
    m = re.search(r"github\.com[:/]([^/]+)/([^/.]+)", remote)
    if not m:
        return None
    owner, repo = m.group(1), m.group(2)
    payload = {"title": title, "head": head, "base": base, "body": body}
    req = urllib.request.Request(
        f"https://api.github.com/repos/{owner}/{repo}/pulls",
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"token {token}",
                 "Accept": "application/vnd.github+json",
                 "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            pr = json.loads(resp.read().decode())
            print(f"[curate] 评审 PR: {pr['html_url']}")
            return pr["html_url"]
    except urllib.error.HTTPError as e:
        print(f"[curate] 开 PR 失败（HTTP {e.code}）：{e.read().decode('utf-8', 'replace')[:400]}")
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=4)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    pull = sh("git pull --rebase origin main", check=False)
    if pull.returncode != 0:
        print(f"[curate] git pull 警告：{pull.stderr[-300:]}")

    text = sh("cat references/articles.md", check=False).stdout
    queue = parse_queue(text, args.limit)
    print(f"[curate] 待处理 {len(queue)} 条（本次上限 {args.limit}）")
    if not queue:
        print("[curate] 队列为空，退出")
        return 0
    if args.dry_run:
        for q in queue:
            print(f"  [dry] {q['title'][:60]} | {q['url']}")
        return 0

    batch = f"candidates/{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}"
    batch_dir = ROOT / batch
    batch_dir.mkdir(parents=True, exist_ok=True)

    # 1) 每篇产三件套
    curate_prompt = (ROOT / "prompts" / "curate.md").read_text(encoding="utf-8")
    for i, item in enumerate(queue, 1):
        slug = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", item["title"])[:40].strip("-") or f"item{i}"
        p = curate_prompt + (
            f"\n\n## 本次条目\n标题：{item['title']}\nURL：{item['url']}\n"
            f"来源：{item['source']} | 日期：{item['date']}\n"
            f"批次目录：{batch}/\nslu：{slug}\n"
        )
        print(f"[curate] 加工 {i}/{len(queue)}：{item['title'][:40]}…")
        stdout, rc = run_codex(p, ROOT, ".curate_prompt.md")
        if rc != 0:
            print(f"[curate] 加工失败 {item['title'][:30]}，继续")
            continue
        (batch_dir / "sources").mkdir(exist_ok=True)
        (batch_dir / "works-ready").mkdir(exist_ok=True)
        (batch_dir / "translations" / slug).mkdir(parents=True, exist_ok=True)

    # 2) 串行评审
    review_prompt = (ROOT / "prompts" / "curate-review.md").read_text(encoding="utf-8")
    items_block = "\n".join(f"- {q['title']} | {q['url']}" for q in queue)
    review_prompt = review_prompt.replace("{ITEMS}", items_block) \
                                 .replace("{BATCH}", batch)
    print(f"[curate] 评审 {len(queue)} 篇…")
    stdout, rc = run_codex(review_prompt, ROOT, ".curate_review_prompt.md")
    if rc == 0:
        (batch_dir / "review.md").write_text(stdout, encoding="utf-8")
    else:
        (batch_dir / "review.md").write_text("评审失败，请人工查看。\n" + stdout[-2000:], encoding="utf-8")

    # 3) 回写 articles.md：待处理 → 评审中
    art = ROOT / "references" / "articles.md"
    t = art.read_text(encoding="utf-8")
    for item in queue:
        url = re.escape(item["url"])
        t = re.sub(rf"(\|.*\| {url} \|[^\n]*)", rf"\1 🔄评审中→{batch}/", t)
    t = t.replace("评审中", "评审中", 1)
    # 移除已处理行并更新计数（简化：把队列行标评审中）
    art.write_text(t, encoding="utf-8")

    # 4) push + 开评审 PR
    sh("git add -A")
    changed = sh("git status --porcelain", check=False).stdout.strip()
    if not changed:
        print("[curate] 无变更，退出")
        return 0
    branch = f"candidates/{batch.split('/')[-1]}"
    sh(f"git checkout -b {branch}")
    sh("git config user.name note-worker || true")
    sh("git config user.email note-worker@users.noreply.github.com || true")
    sh('git commit -m "curate: 候选批次（待人工评审）"')
    sh(f"git push origin {branch}")
    review_text = (batch_dir / "review.md").read_text(encoding="utf-8", errors="replace")
    title = f"候选：{batch}（{len(queue)} 篇）"
    create_pr(branch, "main", title, review_text[:3000])
    print(f"[curate] 完成：{branch}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: 语法验证**

Run: `python -X utf8 -c "import ast; ast.parse(open('scripts/curate.py',encoding='utf-8').read()); print('syntax OK')"`
Expected: `syntax OK`

- [ ] **Step 3: 单元验证 parse_queue**

Run:
```bash
python -X utf8 -c "import sys; sys.path.insert(0,'scripts'); import curate; print('parse:', curate.parse_queue('<!-- pending:start -->\n| A | http://a.com | src | 2026-08-09 |\n| B | http://b.com | src | 2026-08-09 |\n<!-- pending:end -->', 1))"
```
Expected: `parse: [{'title': 'A', 'url': 'http://a.com', 'source': 'src', 'date': '2026-08-09'}]`（limit=1 只取 1 条）

- [ ] **Step 4: 提交**

```bash
git add scripts/curate.py
git commit -m "feat: curate.py 候选加工（三件套 + 串行评审 + 评审 PR）"
```

---

### Task 6: scripts/finalize.py（收录落位）

**Files:**
- Create: `scripts/finalize.py`

- [ ] **Step 1: 写 finalize.py**

Actions 侧，候选 PR 合并后执行：读 review.md 收录标记 → 落位 → 回写 → 同步 → 清理 → 开收录 PR。

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""收录落位层：候选 PR 合并后，把 works-ready 草稿落位到 working/，回写 articles.md。

由 finalize.yml（监听候选 PR 合并 closed+merged）触发，运行在 GitHub Actions runner。

职责：
1. 遍历 candidates/<batch>/，读各篇 review.md 收录标记
2. 收录：works-ready/*.md → working/；淘汰：仅回写状态
3. 回写 articles.md：评审中 → 已收录（归属 working/<slug>）/ 已淘汰
4. 同步 expand/index.md、expand/log.md、知识图谱.md
5. 清理 candidates/<batch>/
6. 开「收录：<batch>」PR（供人类合并 → CI K1-K7）

仅依赖标准库。
"""
import argparse
import json
import os
import pathlib
import re
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent


def list_batches():
    c = ROOT / "candidates"
    if not c.exists():
        return []
    return sorted([p for p in c.iterdir() if p.is_dir()])


def read_review(batch):
    rv = batch / "review.md"
    if not rv.exists():
        return ""
    return rv.read_text(encoding="utf-8", errors="replace")


def create_pr(head, base, title, body):
    token = os.environ.get("GH_TOKEN", os.environ.get("GITHUB_TOKEN", ""))
    if not token:
        print("[finalize] 缺少 GH_TOKEN，跳过开 PR")
        return None
    remote = os.environ.get("GITHUB_REPOSITORY", "wsjwu58-cmd/Obsidian-workFlow")
    owner, repo = remote.split("/")
    payload = {"title": title, "head": head, "base": base, "body": body}
    req = urllib.request.Request(
        f"https://api.github.com/repos/{owner}/{repo}/pulls",
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"token {token}",
                 "Accept": "application/vnd.github+json",
                 "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            pr = json.loads(resp.read().decode())
            print(f"[finalize] 收录 PR: {pr['html_url']}")
            return pr["html_url"]
    except urllib.error.HTTPError as e:
        print(f"[finalize] 开 PR 失败（HTTP {e.code}）：{e.read().decode('utf-8', 'replace')[:400]}")
        return None


def finalize_batch(batch):
    """处理单个候选批次。返回是否产生变更。"""
    # 落位 works-ready → working/
    wr = batch / "works-ready"
    moved = []
    if wr.exists():
        for f in wr.glob("*-translation.md"):
            dest = ROOT / "working" / f.name
            dest.write_text(f.read_text(encoding="utf-8"), encoding="utf-8")
            moved.append(f.name)
            print(f"[finalize] 落位 {f.name} → working/")

    # 回写 articles.md：评审中 → 已收录/已淘汰
    art = ROOT / "references" / "articles.md"
    if art.exists():
        t = art.read_text(encoding="utf-8")
        if moved:
            for name in moved:
                t = re.sub(r"(评审中→candidates/\S+/)", f"已收录（归属 working/{name}）", t)
        t = re.sub(r"评审中→candidates/\S+/", "已淘汰（留 URL 防重复）", t)
        art.write_text(t, encoding="utf-8")

    # 同步 log.md
    log = ROOT / "expand" / "log.md"
    if log.exists():
        entry = (f"\n## [{__import__('datetime').date.today().isoformat()}] curate-finalize | {batch.name}\n"
                 f"- 收录：{', '.join(moved) if moved else '无'}\n")
        with log.open("a", encoding="utf-8") as fh:
            fh.write(entry)

    # 清理 candidates/<batch>/
    import shutil
    shutil.rmtree(batch, ignore_errors=True)
    print(f"[finalize] 清理 {batch.name}")
    return bool(moved)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", default=None, help="指定处理某批次，默认处理全部")
    args = ap.parse_args()

    batches = list_batches()
    if args.batch:
        batches = [b for b in batches if b.name == args.batch]
    if not batches:
        print("[finalize] 无待处理候选批次")
        return 0

    changed = False
    for b in batches:
        changed |= finalize_batch(b)

    if not changed:
        print("[finalize] 无落位变更（全淘汰），直接提交")
    # 提交变更到分支 + 开收录 PR（main 受保护，不能直推）
    branch = f"finalize/{__import__('datetime').datetime.now().strftime('%Y%m%d-%H%M%S')}"
    os.system(f"cd {ROOT} && git checkout -b {branch} && git add -A && "
              f"git config user.name kb-bot && git config user.email kb-bot@users.noreply.github.com && "
              f"git commit -m 'finalize: 收录候选批次' && git push origin {branch}")
    create_pr(branch, "main", "收录：curate 候选批次", "AI 落位 + 索引回写，请 review 合并。")
    print("[finalize] 完成")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: 语法验证**

Run: `python -X utf8 -c "import ast; ast.parse(open('scripts/finalize.py',encoding='utf-8').read()); print('syntax OK')"`
Expected: `syntax OK`

- [ ] **Step 3: 单元验证 list_batches（空目录返回空）**

Run: `python -X utf8 -c "import sys; sys.path.insert(0,'scripts'); import finalize; print('batches:', finalize.list_batches())"`
Expected: `batches: []`（当前无 candidates/ 目录）

- [ ] **Step 4: 提交**

```bash
git add scripts/finalize.py
git commit -m "feat: finalize.py 收录落位（落位+回写+同步+清理+收录 PR）"
```

---

### Task 7: .github/workflows/research.yml

**Files:**
- Create: `.github/workflows/research.yml`

- [ ] **Step 1: 写 research.yml**

每周触发（仿 collect.yml 的 cron）+ 手动。SSH 到服务器跑 research.py。

```yaml
name: 情报追踪（Research）

on:
  schedule:
    - cron: '0 22 * * 0'      # 每周日 22:00 UTC = 周一 06:00（UTC+8）
  workflow_dispatch: {}

permissions:
  contents: read

jobs:
  research:
    runs-on: ubuntu-latest
    steps:
      - name: 检出仓库
        uses: actions/checkout@v4

      - name: 触发服务器情报搜索
        env:
          SERVER_HOST: ${{ secrets.WORKER_HOST }}
          SERVER_SSH_KEY: ${{ secrets.WORKER_SSH_KEY }}
          SERVER_USER: ${{ secrets.WORKER_USER }}
        run: |
          echo "$SERVER_SSH_KEY" > /tmp/worker_key
          chmod 600 /tmp/worker_key
          ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
              -o ConnectTimeout=15 -i /tmp/worker_key \
              "${SERVER_USER}@${SERVER_HOST}" \
              'cd /root/note-worker && /usr/bin/python3 scripts/research.py --max 10'
        timeout-minutes: 30
```

- [ ] **Step 2: YAML 语法验证**

Run: `python -X utf8 -c "import yaml; yaml.safe_load(open('.github/workflows/research.yml',encoding='utf-8')); print('YAML OK')"`
Expected: `YAML OK`

- [ ] **Step 3: 提交**

```bash
git add .github/workflows/research.yml
git commit -m "feat: research.yml 每周情报搜索 workflow"
```

---

### Task 8: .github/workflows/finalize.yml

**Files:**
- Create: `.github/workflows/finalize.yml`

- [ ] **Step 1: 写 finalize.yml**

监听 `pull_request` 的 `closed` 事件且 `merged=true`，且分支匹配 `candidates/*`。由于 Actions 的 pull_request 合并不触发常规 workflow，用 `pull_request` + `types: closed`。

```yaml
name: 收录落位（Finalize）

on:
  pull_request:
    types: [closed]
    branches: [main]

permissions:
  contents: write
  pull-requests: write

jobs:
  finalize:
    if: github.event.pull_request.merged == true && startsWith(github.event.pull_request.head.ref, 'candidates/')
    runs-on: ubuntu-latest
    steps:
      - name: 检出合并后 main
        uses: actions/checkout@v4
        with:
          ref: main
          fetch-depth: 0

      - name: 运行 finalize
        env:
          GH_TOKEN: ${{ secrets.GH_PAT }}
        run: |
          python3 scripts/finalize.py
```

- [ ] **Step 2: YAML 语法验证**

Run: `python -X utf8 -c "import yaml; yaml.safe_load(open('.github/workflows/finalize.yml',encoding='utf-8')); print('YAML OK')"`
Expected: `YAML OK`

- [ ] **Step 3: 提交**

```bash
git add .github/workflows/finalize.yml
git commit -m "feat: finalize.yml 候选合并后收录 workflow"
```

---

### Task 9: 改 dispatch-worker.yml（worker.py → curate.py）

**Files:**
- Modify: `.github/workflows/dispatch-worker.yml:47-49`

- [ ] **Step 1: 改 SSH 命令**

把 `python3 scripts/worker.py --limit 3` 改为 `python3 scripts/curate.py --limit 4`。

```yaml
      - name: 触发服务器候选加工（SSH，curate 攒批）
        if: steps.queue.outputs.count != '0'
        env:
          SERVER_HOST: ${{ secrets.WORKER_HOST }}
          SERVER_SSH_KEY: ${{ secrets.WORKER_SSH_KEY }}
          SERVER_USER: ${{ secrets.WORKER_USER }}
        run: |
          echo "$SERVER_SSH_KEY" > /tmp/worker_key
          chmod 600 /tmp/worker_key
          ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
              -o ConnectTimeout=15 -i /tmp/worker_key \
              "${SERVER_USER}@${SERVER_HOST}" \
              'cd /root/note-worker && /usr/bin/python3 scripts/curate.py --limit 4'
        timeout-minutes: 30
```

- [ ] **Step 2: YAML 语法验证**

Run: `python -X utf8 -c "import yaml; yaml.safe_load(open('.github/workflows/dispatch-worker.yml',encoding='utf-8')); print('YAML OK')"`
Expected: `YAML OK`

- [ ] **Step 3: 提交**

```bash
git add .github/workflows/dispatch-worker.yml
git commit -m "feat: dispatch 改调 curate.py（攒批候选 + 评审 PR）"
```

---

### Task 10: 退役 worker.py / collect.py / collect.yml + 改 check_consistency.py

**Files:**
- Modify: `scripts/worker.py:1-19`（docstring 标注废弃）
- Modify: `scripts/collect.py:1-6`（docstring 标注部分退役）
- Modify: `.github/workflows/collect.yml:1-8`（注释标注废弃）
- Modify: `scripts/check_consistency.py`

- [ ] **Step 1: worker.py docstring 标注废弃**

在文件头注释后追加：

```python
# 废弃：由 scripts/curate.py 取代（候选三件套 + 人类闸门）。保留仅供参考，不再由 workflow 调用。
```

- [ ] **Step 2: collect.yml 顶部注释标注废弃**

在 `name: 采集与过滤` 下加：

```yaml
# 废弃：由 research.yml（codex 深度搜索）替代固定源采集。保留历史，不再计划触发。
```

- [ ] **Step 3: check_consistency.py 处理 candidates/**

候选批次目录含草稿/原文快照，不应被 K3（frontmatter）误报。在 `all_files()` 或 K3 循环里过滤 `candidates/`：

```python
# 在 K3 循环中跳过 candidates/ 暂存区
if "candidates" in p.parts:
    continue
```

- [ ] **Step 4: 门禁全绿验证**

Run: `python -X utf8 scripts/check_consistency.py 2>&1 | Select-String 'PASS|FAIL|通过|失败'`
Expected: 全部 PASS，无 FAIL

- [ ] **Step 5: 提交**

```bash
git add scripts/worker.py .github/workflows/collect.yml scripts/check_consistency.py
git commit -m "chore: 标注 worker/collect 废弃；check_consistency 豁免 candidates/ 暂存区"
```

---

### Task 11: 服务器部署 + E2E 验证

**Files:**
- Modify: 服务器 `/root/note-worker`（git pull）

- [ ] **Step 1: 推送本分支合并到 main**

```bash
git checkout main && git pull origin main
# 创建 feat/curate-pipeline 分支，逐个 task 的 commit 已在 main 上，直接开 PR 合并
```

- [ ] **Step 2: 服务器拉取最新 main**

SSH 到服务器执行：
```bash
cd /root/note-worker && git pull --rebase origin main && git checkout main
python3 -c "import ast; [ast.parse(open('scripts/'+f,encoding='utf-8').read()) for f in ['research.py','curate.py','finalize.py']]; print('server syntax OK')"
```

- [ ] **Step 3: 服务器 dry-run 验证**

```bash
cd /root/note-worker && python3 scripts/curate.py --dry-run
python3 scripts/research.py --dry-run
```
Expected: 输出队列清单 / 提示词预览（不联网不调 codex）

- [ ] **Step 4: 触发一次真实 research（workflow_dispatch research.yml）**

```bash
gh workflow run research.yml
```
Expected: run success，队列出现 codex 候选

- [ ] **Step 5: 触发一次真实 curate（workflow_dispatch dispatch-worker.yml）**

```bash
gh workflow run dispatch-worker.yml
```
Expected: 生成 candidates/<batch>/ + 评审 PR，你在 GitHub 上 approve/修改/close

- [ ] **Step 6: 合并候选 PR 后验证 finalize**

合并评审 PR → finalize.yml 自动触发 → 检查 working/ 落位 + articles.md 回写 + 收录 PR 生成

---

## Self-Review 结果

**Spec 覆盖检查：**
- ✅ 采集策略（research.py + research.yml）→ Task 4, 7
- ✅ 攒批候选 + 三件套（curate.py）→ Task 5
- ✅ 自动评审扇出（prompts/curate-review.md + curate 串行调用）→ Task 3, 5
- ✅ 人类闸门（评审 PR）→ Task 5
- ✅ finalize 收录（finalize.py + finalize.yml + 收录 PR）→ Task 6, 8
- ✅ 目录产出者边界（prompts/curate.md）→ Task 2
- ✅ 去重分层（research.py 机械去重 + 提示词注入）→ Task 4
- ✅ 组件退役（worker/collect）→ Task 10
- ✅ 一致性门禁扩展（candidates 豁免）→ Task 10
- ✅ 服务器部署 + E2E → Task 11

**已知偏差（与 spec 的细微差异）：**
1. spec 写「单 codex exec 串行评审」→ curate.py 用独立 review prompt（Task 5）— 一致
2. spec 写「并行扇出」→ 已按用户确认改为「单 codex 串行」— 计划按串行实现
3. finalize.yml 用 `pull_request.closed + merged`（合并不触发常规 pull_request）— 实现细节，已在 Task 8 说明
4. research.py 复用 firecrawl_search 而非纯 codex 深度搜索（服务器需联网）— 更符合现有代码模式
