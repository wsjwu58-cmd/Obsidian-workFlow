# wiki → WordPress 草稿同步

GitHub Actions 每天北京时间 02:00（UTC 前一天 18:00）通过 SSH 触发服务器本机导入。GitHub 的定时任务可能延迟。也可以手动运行「Wiki 博客草稿同步」，勾选 preview 只预览。

## 发布范围

`config/blog-sync.yml` 是唯一白名单，初始为 DP动态规划、贪心算法、SpringBoot。只读取已推送至 GitHub 的 wiki Markdown 与其本地图片；不改 wiki，不同步私密目录，不删除博客文章。首次只建草稿，请登录 WordPress 后台「文章 → 草稿」审阅后发布。

扩展范围：在 notes 中新增唯一的 id 和 wiki 内路径，走 PR 合并。改名/移动笔记时保留 id，只改 path。配置允许的 id 永远映射到同一篇文章，不能重新分配给另一篇。白名单中丢失的文件报告异常，不删除博客内容；移出白名单则停止更新。

## 增量、图片与链接

- WordPress 的 `_wiki_sync_key` 保存稳定身份，`_wiki_sync_source_hash` 保存渲染内容哈希，`_wiki_sync_fingerprint` 用于检测博客端人工修改。重复运行不新建相同文章或媒体。
- 博客标题、正文、摘要、分类被人工修改时报告 conflict，保留博客修改。不要直接删除这几个元数据来强制覆盖，先人工比较两边内容。
- 已手动发布的文章保持发布状态，后续 wiki 更新会更新该文；初始草稿不会被脚本自动发布。
- 双链只指向白名单中已发布的文章，其余显示普通文字。目标草稿发布后，下一次同步会补上链接。当前转换不保留双链的段落锚点。
- 本地 PNG/JPEG/GIF/WebP 导入媒体库，按文件内容去重。单张不超过 10 MiB；路径只能在 wiki 内。支持常规 Markdown 图片与 Obsidian 图片嵌入、编码过的空格、当前笔记旁的 attachments 目录。
- 外链图片暂不自动下载，遇到时中止预检并报告 URL；先把图片放进 wiki 下、由用户修改原笔记引用后再加入白名单。缺失/越界图片同样阻止本批导入。SVG 不导入。
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
