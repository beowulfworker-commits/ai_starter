param(
  [Parameter(Mandatory=$true, ValueFromRemainingArguments=$true)]
  [string[]]$q
)
$repoRoot = (Resolve-Path "$PSScriptRoot\.." ).Path
if ($repoRoot -ne "C:\local-ai-starter") { Write-Host "Переместите репозиторий в C:\local-ai-starter."; exit 1 }

$txt = [string]::Join(' ', $q)
wsl -e env TXT="$txt" bash -lc 'cd /mnt/c/local-ai-starter && ~/.venvs/localai/bin/python3 app/main.py "$TXT"'
