param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('ingest', 'lint')]
    [string]$Mode
)

# 模式 A：Codex 定时任务包装脚本
# 由 Windows 任务计划程序调用（周加工 周一 06:30 / 日巡检 每天 09:00）
$ErrorActionPreference = 'Continue'

$root = 'D:\note'
$logDir = Join-Path $root '.codex-runs'
New-Item -ItemType Directory -Force -Path $logDir | Out-Null

$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$log = Join-Path $logDir "$Mode-$stamp.log"
$outFile = Join-Path $logDir "$Mode-$stamp.out.txt"

if ($Mode -eq 'ingest') {
    $prompt = @'
摄入 raw/ 中所有 status=pending 的素材，按 agents.md 规则入库：
AI 生成条目写入 expand/ 对应分类（wiki/ 只读），建立双向链接，同步 expand/index.md、expand/log.md、expand/知识图谱.md，并将 raw/ 素材标记为 processed。最后用中文输出变更摘要（新增/更新了哪些条目）。
'@
} else {
    $prompt = @'
检查知识库：断链 / 孤立节点 / 重复条目 / pending 积压 / index 同步 / 空笔记。
修复可自动修复的项目（如断链改名、补链接），并将巡检报告摘要追加到 expand/log.md。
最后用中文输出摘要与建议。
'@
}

$codexArgs = @(
    'exec',
    '-C', $root,
    '-s', 'workspace-write',
    '-c', 'sandbox_workspace_write.network_access=true',
    '-o', $outFile,
    $prompt
)

"[$stamp] 开始运行 Codex 定时任务（$Mode）" | Out-File -Encoding utf8 $log
& codex @codexArgs *>> $log
"`n[exit] code=$LASTEXITCODE time=$(Get-Date -Format o)" | Out-File -Append -Encoding utf8 $log
exit $LASTEXITCODE
