param([Parameter(Mandatory=$true)][string]$text)
$repoRoot = (Resolve-Path "$PSScriptRoot\..").Path
if ($repoRoot -ne "C:\local-ai-starter") {
  Write-Host "Переместите репозиторий в C:\local-ai-starter." -ForegroundColor Yellow
  exit 1
}
wsl -e bash -lc "cd /mnt/c/local-ai-starter && ~/.venvs/localai/bin/python3 app/seed_memory.py \"$($text.Replace('"','\"'))\""
