# wiki → WordPress 博客同步

GitHub Actions 每天北京时间 02:00（UTC 前一天 18:00）通过 SSH 触发服务器本机导入。GitHub 的定时任务可能延迟。也可以手动运行博客同步工作流，勾选 preview 只预览。

## 发布范围

`config/blog-sync.yml` 默认自动扫描 `wiki/` 下所有 Markdown，并按目录层级创建 WordPress 分类：第一层是模块，后续层级是子文件夹；`生活杂项`、`求职面试` 被排除。当前状态为 `publish`，新笔记和历史同步笔记会进入首页；不改 wiki，不同步私密目录，不删除博客文章。需要先人工审核时，把状态改回 `draft`。

如需改成精确白名单，把 `notes: auto` 改为条目列表，每项填写稳定 id 和 wiki 内路径。自动模式的身份由路径哈希生成；改名/移动笔记会被视为新路径，导入器会先用标题与正文相似度检查博客中的旧文章，避免重复创建。移出自动扫描范围的文件不会删除博客内容。

同步前会检查所有已有文章（包括早期手工文章）：标题规范化一致，或标题与正文相似度达到安全阈值时，记录为 duplicate 并采用原文章作为该笔记的稳定身份，随后补齐路径、模块、子文件夹和评论状态，避免同一篇笔记出现两份。

## 增量、图片与链接

- WordPress 的 `_wiki_sync_key` 保存稳定身份，`_wiki_sync_source_hash` 保存渲染内容哈希，`_wiki_sync_fingerprint` 用于检测博客端人工修改。重复运行不新建相同文章或媒体。
- 博客标题、正文、摘要、分类被人工修改时报告 conflict，保留博客修改。不要直接删除这几个元数据来强制覆盖，先人工比较两边内容。
- `status: publish` 是同步配置的权威状态：新笔记、旧草稿以及从历史文章迁移的笔记都会发布；改为 `draft` 才会暂停公开。
- 双链只指向白名单中已发布的文章，其余显示普通文字。目标草稿发布后，下一次同步会补上链接。当前转换不保留双链的段落锚点。
- 本地 PNG/JPEG/GIF/WebP 导入媒体库，按文件内容去重。单张不超过 10 MiB；路径只能在 wiki 内。支持常规 Markdown 图片与 Obsidian 图片嵌入、编码过的空格、当前笔记旁的 attachments 目录。
- 允许列表中的外链图片（当前包括 Gitee、知乎图床、CSDN、GitHub）会在同步时下载到临时快照，再通过 WordPress 媒体库导入；文章最终只保存本站媒体 URL，避免第三方防盗链或链接失效。其他主机、缺失、越界或不支持的图片会在正文中显示“图片未同步”占位并记录警告，不阻断其他笔记。单张仍不超过 10 MiB，SVG 不导入。
- 同步文章默认开启评论；已有同步文章会在下一次同步中自动修复为可评论，评论状态不参与内容冲突指纹。
- 同步会安装一个 must-use 插件和两个模板：博客首页只展示一级模块；点击模块后按子文件夹分组显示笔记，主题更换后仍保留。
- 保留普通 Markdown 的代码、表格和列表；HTML 在服务器经 WordPress 清洗。Mermaid/公式仅作为原始文本或代码保留，暂未接渲染插件。

## 运行与验证

```bash
python -m pip install -r scripts/requirements-blog.txt
python scripts/sync_wordpress.py                 # 预览，不连接博客
python -m unittest discover -s scripts -p 'test_*.py'
```

预览报告还会列出被过滤的空/短笔记、缺失资源和未发布双链；同步成功后可检查 `/opt/wiki-blog-sync/last-report.json` 中的 `duplicates`、`published`、`conflicts` 和 `errors`。

服务器由 `scripts/run_blog_sync.sh` 管理独立的 `/opt/wiki-blog-sync/repo.git` 与一次性快照，不切换、不 reset 现有 `/root/note-worker`。同步报告保存在 `/opt/wiki-blog-sync/last-report.json`。操作系统锁与 PHP 锁禁止并发写入。

PHP importer 只允许 CLI 调用，安装目录来自配置；通过 WordPress 自身函数更新文章与媒体，**不开放额外 HTTP 接口，也不传输 WordPress 密码**。root 启动脚本时会以 www 用户运行 PHP；已有作者 ID 1 作为文章作者。

工作流复用仓库的 WORKER_HOST / WORKER_USER / WORKER_SSH_KEY Secrets。`.github/blog-known-hosts` 是已核验的服务器公钥；更换服务器或主机密钥后，先独立验证再更新该文件，不关闭主机密钥校验。

首次写入前建议备份数据库及 uploads；本次接入时已在服务器创建备份。回滚某篇：用 WordPress 修订版本或备份还原。停止同步：在 GitHub 禁用此工作流。定时生效前提是工作流已合并至默认分支 main。
