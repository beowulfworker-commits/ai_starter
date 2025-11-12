set -euo pipefail
sudo apt-get update -y
sudo apt-get install -y python3-venv python3-pip
python3 -m venv ~/.venvs/localai
source ~/.venvs/localai/bin/activate
python3 -m pip install -U pip wheel

python3 -m pip install -U openai qdrant-client fastembed

python3 -m pip install -U vllm hf_transfer

mkdir -p /mnt/c/local-ai-starter/models
mkdir -p /mnt/c/local-ai-starter/logs

echo "Bootstrap OK"
