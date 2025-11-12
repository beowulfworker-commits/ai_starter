$ErrorActionPreference = "Stop"
$repoRoot = (Resolve-Path "$PSScriptRoot\..").Path
# Требуем строгое расположение для простоты путей
if ($repoRoot -ne "C:\local-ai-starter") {
  Write-Host "Переместите репозиторий в C:\local-ai-starter и запустите снова." -ForegroundColor Yellow
  exit 1
}
Set-Location $repoRoot

# .env
if (-not (Test-Path ".\.env")) {
  Copy-Item ".\.env.example" ".\.env"
}

# Создать каталоги
New-Item -ItemType Directory -Force -Path ".\models" | Out-Null
New-Item -ItemType Directory -Force -Path ".\logs" | Out-Null

# 1) Qdrant
docker compose up -d qdrant

# 2) Bootstrap WSL python env
wsl -e bash -lc "cd /mnt/c/local-ai-starter && bash scripts/01_wsl_bootstrap.sh"

# 3) vLLM serve (detached внутри WSL)
wsl -e bash -lc "cd /mnt/c/local-ai-starter && bash scripts/02_run_vllm.sh"

# 4) Проверка API
Start-Sleep -Seconds 5
try {
  $resp = Invoke-WebRequest -Uri "http://localhost:8000/v1/models" -UseBasicParsing -Method GET -TimeoutSec 10
  Write-Host "vLLM работает. Модель доступна." -ForegroundColor Green
} catch {
  Write-Host "Не удалось связаться с vLLM на порту 8000." -ForegroundColor Yellow
}

Write-Host "Готово. Запустите: scripts\chat.ps1 \"Привет\"" -ForegroundColor Cyan
