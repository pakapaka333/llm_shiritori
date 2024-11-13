set -e

REPO_PATH="/path/to/your/llm-shiritori/repo"
MODEL_NAME_OR_PATH=$1
DEVICES=${2:-}

cd $REPO_PATH
source .venv_llm-shiritori/bin/activate
echo "Launching LLM Shiritori (model: ${MODEL_NAME_OR_PATH} / devices: ${DEVICES})"
CUDA_VISIBLE_DEVICES=$DEVICES python scripts/evaluate.py $MODEL_NAME_OR_PATH
deactivate