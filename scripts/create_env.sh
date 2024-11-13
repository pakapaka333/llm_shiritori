set -e

REPO_PATH="/path/to/your/llm-shiritori/repo"

cd $REPO_PATH
python3 -m venv .venv_llm-shiritori

source .venv_llm-shiritori/bin/activate
pip install -r scripts/requirements.txt
deactivate