$ErrorActionPreference = "SilentlyContinue"
$repoRoot = (Resolve-Path "$PSScriptRoot\..").Path
Set-Location $repoRoot

# Остановить vLLM внутри WSL
wsl -e bash -lc "cd /mnt/c/local-ai-starter && bash scripts/03_stop_vllm.sh"

# Остановить Qdrant
docker compose down
Write-Host "Остановлено." -ForegroundColor Green
