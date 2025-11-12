set -euo pipefail
# Python env, deps
sudo apt-get update -y
sudo apt-get install -y python3-venv python3-pip
python3 -m venv ~/.venvs/localai
source ~/.venvs/localai/bin/activate
python3 -m pip install -U pip wheel

# Deps for app
python3 -m pip install -U openai qdrant-client fastembed

# vLLM
python3 -m pip install -U vllm hf_transfer

# Ensure dirs
mkdir -p /mnt/c/local-ai-starter/models
mkdir -p /mnt/c/local-ai-starter/logs

echo "Bootstrap OK"
