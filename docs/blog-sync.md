# wiki → WordPress 草稿同步

GitHub Actions 每天北京时间 02:00（UTC 前一天 18:00）通过 SSH 触发服务器本机导入。GitHub 的定时任务可能延迟。也可以手动运行「Wiki 博客草稿同步」，勾选 preview 只预览。

## 发布范围

`config/blog-sync.yml` 默认自动扫描 `wiki/` 下所有 Markdown，并按第一层子目录创建 WordPress 分类；`生活杂项`、`求职面试` 被排除。当前状态为 `publish`，新笔记和此前同步但仍为草稿的笔记会进入首页；不改 wiki，不同步私密目录，不删除博客文章。需要先人工审核时，把状态改回 `draft`。

如需改成精确白名单，把 `notes: auto` 改为条目列表，每项填写稳定 id 和 wiki 内路径。自动模式的身份由路径哈希生成；改名/移动笔记会被视为新路径，导入器会先用标题与正文相似度检查博客中的旧文章，避免重复创建。移出自动扫描范围的文件不会删除博客内容。

同步前会检查所有已有文章（包括早期手工文章）：标题规范化一致，或标题与正文相似度达到安全阈值时，记录为 duplicate 并复用原文章，不重复创建。

## 增量、图片与链接

- WordPress 的 `_wiki_sync_key` 保存稳定身份，`_wiki_sync_source_hash` 保存渲染内容哈希，`_wiki_sync_fingerprint` 用于检测博客端人工修改。重复运行不新建相同文章或媒体。
- 博客标题、正文、摘要、分类被人工修改时报告 conflict，保留博客修改。不要直接删除这几个元数据来强制覆盖，先人工比较两边内容。
- 已手动发布的文章保持发布状态，后续 wiki 更新会更新该文；初始草稿不会被脚本自动发布。
- 双链只指向白名单中已发布的文章，其余显示普通文字。目标草稿发布后，下一次同步会补上链接。当前转换不保留双链的段落锚点。
- 本地 PNG/JPEG/GIF/WebP 导入媒体库，按文件内容去重。单张不超过 10 MiB；路径只能在 wiki 内。支持常规 Markdown 图片与 Obsidian 图片嵌入、编码过的空格、当前笔记旁的 attachments 目录。
- 外链图片不会由服务器下载，保留原始 HTTP/HTTPS 地址并在报告中提示；如果要避免第三方图片失效，应先把图片放进 wiki 下。缺失、越界或不支持的图片会在正文中显示“图片未同步”占位并记录警告，不阻断其他笔记。SVG 不导入。
- 保留普通 Markdown 的代码、表格和列表；HTML 在服务器经 WordPress 清洗。Mermaid/公式仅作为原始文本或代码保留，暂未接渲染插件。

## 运行与验证

```bash
python -m pip install -r scripts/requirements-blog.txt
python scripts/sync_wordpress.py                 # 预览，不连接博客
python -m unittest discover -s scripts -p 'test_*.py'
```

服务器由 `scripts/run_blog_sync.sh` 管理独立的 `/opt/wiki-blog-sync/repo.git` 与一次性快照，不切换、不 reset 现有 `/root/note-worker`。同步报告保存在 `/opt/wiki-blog-sync/last-report.json`。操作系统锁与 PHP 锁禁止并发写入。

PHP importer 只允许 CLI 调用，安装目录来自配置；通过 WordPress 自身函数更新文章与媒体，**不开放额外 HTTP 接口，也不传输 WordPress 密码**。root 启动脚本时会以 www 用户运行 PHP；已有作者 ID 1 作为文章作者。

工作流复用仓库的 WORKER_HOST / WORKER_USER / WORKER_SSH_KEY Secrets。`.github/blog-known-hosts` 是已核验的服务器公钥；更换服务器或主机密钥后，先独立验证再更新该文件，不关闭主机密钥校验。

首次写入前建议备份数据库及 uploads；本次接入时已在服务器创建备份。回滚某篇：用 WordPress 修订版本或备份还原。停止同步：在 GitHub 禁用此工作流。定时生效前提是工作流已合并至默认分支 main。
