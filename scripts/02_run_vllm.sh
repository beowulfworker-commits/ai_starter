set -euo pipefail
cd /mnt/c/local-ai-starter
source ~/.venvs/localai/bin/activate

set -a
. ./.env
set +a

export HF_HUB_ENABLE_HF_TRANSFER=1
if [ -n "${HF_TOKEN:-}" ]; then
  export HUGGING_FACE_HUB_TOKEN="$HF_TOKEN"
fi

pkill -f "vllm serve" || true

nohup vllm serve "${MODEL_ID:-Qwen/Qwen2.5-14B-Instruct-GPTQ-Int4}" \
  --host 0.0.0.0 \
  --port 8000 \
  --download-dir /mnt/c/local-ai-starter/models \
  --max-model-len "${CONTEXT_LEN:-32768}" \
  --gpu-memory-utilization "${GPU_MEM_UTIL:-0.90}" \
  --quantization gptq \
  --dtype auto \
  > /mnt/c/local-ai-starter/logs/vllm.log 2>&1 &
echo $! > /mnt/c/local-ai-starter/logs/vllm.pid
echo "vLLM started"
