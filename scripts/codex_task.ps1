param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('ingest', 'lint')]
    [string]$Mode
)

# Mode A: scheduled Codex task wrapper.
# Invoked by Windows Task Scheduler:
#   weekly ingest: every Monday 06:30
#   daily lint:    every day 09:00
$ErrorActionPreference = 'Continue'

$root = 'D:\note'
$logDir = Join-Path $root '.codex-runs'
New-Item -ItemType Directory -Force -Path $logDir | Out-Null

$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$log = Join-Path $logDir "$Mode-$stamp.log"
$outFile = Join-Path $logDir "$Mode-$stamp.out.txt"

if ($Mode -eq 'ingest') {
    $prompt = 'Ingest all materials with status=pending in references/raw/ following the rules in agents.md: write AI-generated entries into expand/ under the matching category (wiki/ is read-only), build bidirectional links, sync expand/index.md, expand/log.md and expand/知识图谱.md, then mark references/raw/ materials as processed. Finish with a concise Chinese summary of what was added or updated.'
} else {
    $prompt = 'Run the knowledge base lint: broken links, orphan nodes, duplicate entries, pending backlog, index sync, empty notes. Fix issues that can be safely auto-fixed, then append a lint report summary to expand/log.md. Finish with a concise Chinese summary and recommendations.'
}

$codexArgs = @(
    'exec',
    '-C', $root,
    '-s', 'workspace-write',
    '-c', 'sandbox_workspace_write.network_access=true',
    '-o', $outFile,
    $prompt
)

$header = "[$stamp] start codex task ($Mode)"
$header | Out-File -Encoding utf8 $log
& codex @codexArgs *>> $log
$exitLine = "`n[exit] code=$LASTEXITCODE time=$(Get-Date -Format o)"
$exitLine | Out-File -Append -Encoding utf8 $log
exit $LASTEXITCODE
