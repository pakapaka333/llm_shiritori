import argparse
from llm_shiritori import play_shiritori

# Path Settings
PROMPT_PATH = "prompt_template.txt"
ODAI_PATH = "odai.txt"
LOG_PAHT = "results/log.jsonl"
OVERALL_PATH = "results/overall.jsonl"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the model with specified settings.")
    parser.add_argument("model_name", type=str, help="A model to play shiritori")
    args = parser.parse_args()

    with open(ODAI_PATH, mode='r', encoding="utf-8") as odai_file:
        odai = list(map(lambda odai: odai.strip(), odai_file.readlines()))
        odai = list(filter(None, odai))

    with open(PROMPT_PATH, mode='r', encoding="utf-8") as prompt_file:
        prompt_template = prompt_file.read()
        assert "{shiritori}" in prompt_template, "Prompt template must include '{shirotiri}', which acts as a placeholder for the shiritori sequence."

    play_shiritori(
        args.model_name, prompt_template, odai,
        LOG_PAHT, OVERALL_PATH,
    )   