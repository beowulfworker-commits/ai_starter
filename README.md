# Local AI Starter (Windows + WSL2) — Qwen2.5‑14B GPTQ‑Int4 + vLLM + Qdrant

Минимальный стек: vLLM (локальный OpenAI‑совместимый сервер) + Qdrant (память) + FastEmbed (эмбеддинги).
Мишень: Windows 11 + WSL2, NVIDIA 24 ГБ. Модель: `Qwen/Qwen2.5-14B-Instruct-GPTQ-Int4`.

## Быстрый старт (без кодинга)
0. **Требования:** NVIDIA драйвер, Docker Desktop (включён WSL 2 backend), включён WSL2 с Ubuntu‑24.04.
1. Распакуйте папку в **C:\local-ai-starter** (важно для путей).
2. Откройте PowerShell **как администратор** и выполните:
   ```powershell
   Set-Location C:\local-ai-starter\scripts
   .\10_start.ps1
   ```
   Скрипт:
   - поднимет Qdrant в Docker,
   - подготовит Python‑среду внутри WSL,
   - запустит vLLM с Qwen 2.5 14B GPTQ‑Int4.
3. Тест:
   ```powershell
   .\chat.ps1 "Привет, проверка связи"
   ```
   Ответ модели появится в консоли.

Остановить всё:
```powershell
Set-Location C:\local-ai-starter\scripts
.	_stop.ps1
```

## Настройка
1. Скопируйте `.env.example` в `.env` и при необходимости укажите `HF_TOKEN` (если HuggingFace требует токен).
2. Параметры по умолчанию:
   - `MODEL_ID=Qwen/Qwen2.5-14B-Instruct-GPTQ-Int4`
   - `CONTEXT_LEN=32768`
   - `GPU_MEM_UTIL=0.90`
   - `EMBEDDING_MODEL=BAAI/bge-m3`

## Память и мимикрия
- Добавить факт/стиль в память:
  ```powershell
  .\seed_memory.ps1 "Мой стиль: краткость, без восклицаний."
  ```
- Модель автоматически подтянет релевантные записи из Qdrant к каждому запросу.

## Проверка GPU и устранение неполадок
- В WSL:
  ```powershell
  wsl -e bash -lc "nvidia-smi"
  ```
  Если GPU не виден, обновите драйвер NVIDIA, убедитесь, что Docker Desktop использует WSL 2 backend и включена интеграция с Ubuntu.
- Если порт 8000 занят — остановите другой сервис или измените порт в `scripts/02_run_vllm.sh` и `app/main.py`.

## Структура
```
C:\local-ai-starter
  ├─ .env.example        # параметры модели и эмбеддингов
  ├─ docker-compose.yml  # Qdrant
  ├─ scripts/            # запуск/остановка
  ├─ app/                # минимальный клиент, память
  └─ models/, logs/      # создаются автоматически
```

## Команды
- Старт всего стека: `scripts\10_start.ps1`
- Стоп всего стека: `scripts\11_stop.ps1`
- Тест‑чат: `scripts\chat.ps1 "вопрос"`
- Добавить память: `scripts\seed_memory.ps1 "текст"`
