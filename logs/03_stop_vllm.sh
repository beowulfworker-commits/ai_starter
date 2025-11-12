set -euo pipefail
# Try PID first
if [ -f /mnt/c/local-ai-starter/logs/vllm.pid ]; then
  kill $(cat /mnt/c/local-ai-starter/logs/vllm.pid) || true
  rm -f /mnt/c/local-ai-starter/logs/vllm.pid
fi
# Fallback
pkill -f "vllm serve" || true
echo "vLLM stopped"
