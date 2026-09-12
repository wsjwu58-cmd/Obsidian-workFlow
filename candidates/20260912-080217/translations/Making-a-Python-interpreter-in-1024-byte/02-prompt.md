---
created: 2026-09-12
updated: 2026-09-12
type: prompt-draft
status: 过程稿
sources:
  - url: https://austinhenley.com/blog/python1024.html
tags: [C, Python, 解释器, 递归下降解析, 代码高尔夫, 翻译, prompt]
---

# 02 本次翻译使用的提示词（过程稿）

> 本次翻译用如下提示词驱动。原文（英文博客正文）已抓取到
> `candidates/20260912-080217/sources/Making-a-Python-interpreter-in-1024-byte.md`
> （firecrawl 主内容抓取 + 原始 HTML 元数据核对；含 8 个代码块、3 张截图链接与全部外链）。

## 提示词正文

```
你是一名资深技术译者（英→中），翻译 Austin Z. Henley 的技术博客
《Making a Python interpreter in 1024 bytes》（2026-09-06，
https://austinhenley.com/blog/python1024.html）。原文是作者用 C 手写一个
1024 字节 Python 子集解释器的经验记录。

## 输入
- 原文：candidates/20260912-080217/sources/Making-a-Python-interpreter-in-1024-byte.md
  （正文从 "# Making a Python interpreter in 1024 bytes" 标题行之后开始，
   到 "What does your Python in 1024 bytes look like?" 结束；忽略文件头部的采集元信息块。）

## 输出要求
1. 完整逐译正文全部段落与小标题，不压缩、不删节。保留原文的斜体强调（如 _def_、_if_、
   _while_、_for x in range(y)_）与粗体强调（如 **1 + 2**、**1024**、**not**、**a lot**、
   **by hand**），排版层级沿用原文。
2. 保留原文全部超链接（Markdown 链接原样保留，链接文字翻译成中文）：
   Hacker News、r/programming、Lobste.rs、Teeny Tiny、CPython、
   "Tips for golfing in C"、code golf（维基）、GitHub（AZHenley/python1024）。
   3 张截图以 Markdown 图片语法原样保留 URL（python1024.png、codegolfingtips.png、
   python1024running.png）。
3. 代码块原样保留、不翻译、不重排、不改变任何字符：
   - FizzBuzz 样例（python 代码块，`range(101)`、缩进层级）
   - 状态变量片段（char src[999]; int vars[256]; ...）
   - parse_sum 片段
   - 关键字识别片段（注释里的 "for K in range(N):" 等）
   - run_block 片段（到 `pos = line_start; return;` 为止）
   - 单字符变量查找片段（`if (ch > 96) { value = vars[ch]; next(); }`）
   - skip_to_eol 片段（递归跳到行尾）
   - Minify! 一节的 golf 版完整 C 源码单行代码块（必须逐字节保留，特别是
     `c-43u<3`、`c-48u<10`、`c-60u>2`、`k-102?p+=k/4-25` 等按位/无符号运算写法）
   - 以及文中内联代码 `e(){for(z=t();c-43u<3;)y=44-c,z+=y*t();return z;}`、
     `Y(){c&&c-10&&Y(G());}`、`vars[ch]` 等
4. 代码块中作者手写的 C 注释（如 /* Entire program without most spaces. */、
   /* Symbol table. */、/* "for K in range(N):" */、/* Skip "or". */ 等）也要翻译成中文，
   但不得改动放在注释旁边的代码字符与列对齐意图（对齐可因中文宽度适当放宽）。
5. 术语表（必须一致）：
   - Python interpreter → Python 解释器
   - recursive descent parser → 递归下降解析器
   - abstract syntax tree（AST）→ 抽象语法树（AST）
   - bytecode → 字节码
   - tokenize → 词法分析（分词）
   - symbol table → 符号表
   - intermediate representation（IR）→ 中间表示（IR）
   - code golf / golfed → 代码高尔夫 / 高尔夫版
   - minify → 压缩瘦身
   - indentation → 缩进
   - truthiness → 真值性
   - readable version → 可读版
   - FizzBuzz / CPython / Stack Overflow / GNU C89 / libc / GitHub 保留原文
   - C89 / 全局零初始化 / 隐式 int 等按 C 语言社区通行译法
   作者语气词（如 "good ole C"、"macro shenanigans"、"library tomfoolery"、
   "code magicians of yesteryear"、"conventional fiddle-faddle"）在准确前提下译出趣味，
   不逐字硬译也不省译。
6. 数字与结论逐一比对原文，不得改动：512、1024、999、256、4800、800、
   `range(101)`、"no macro shenanigans or library tomfoolery"、特性清单 12 条、
   作者说只求 FizzBuzz 可做到 800 字节以下（"I think I could get below 800 bytes"）。
7. 输出 Markdown，标题层级沿用原文（两级：标题 + 四个 ### 小节）；frontmatter：
   ---
   created: 2026-09-12
   updated: 2026-09-12
   title: 用 1024 字节写一个 Python 解释器
   sourceUrl: https://austinhenley.com/blog/python1024.html
   sourceAuthor: Austin Z. Henley
   translatedAt: 2026-09-12
   sources: [references/articles.md 待处理队列]
   tags: [C, Python, 解释器, 递归下降解析, 代码高尔夫, 编译器, type/翻译]
   ---
```

## 执行备注

- 抓取方式：firecrawl `scrape -f markdown --only-main-content` 取得正文；`curl` 抓原始 HTML
  （13,748 字节）核对 `<title>`、`<meta name="author">`、发布日期与描述元数据。
- 翻译策略：完整逐译 + 代码零改动；作者口语化语气与术语准确并重，代码注释翻译但不动代码。
- 关键数字比对：512/1024/999/256/4800/800 与 `range(101)` 已在译文抽查，与原文一致；
  golf 版源码在译文里逐字节复制自源文件。
- 该提示词本身不直接沉淀进 prompts/（curate 产出边界：不写 prompts/），
  留待评审通过、实测后再考虑复用。
