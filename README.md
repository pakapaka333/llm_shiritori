# LLM Shiritori (LLM しりとり)
## Setup
### Specify REPO_PATH
Set the REPO_PATH variable in `scripts/create_env.sh` and `scripts/run.sh`.

### Specify the Torch Version (if necessary)
If needed, specify the version of Torch available on your device in `scripts/create_env.sh`.

### Run the Setup Script
```
bash scripts/create_env.sh
```

### Set Your Hugging Face Token
```
echo (Your HF token) > scripts/.hftoken
```

<br>

## Evaluate
You can run the code on the CPU:
```
bash scripts/run.sh (Model Name)
```
Or you can specify the GPU devices you want to use:
```
bash scripts/run.sh (Model Name) (Device)
```

<br>

## Customize
### Create Your Own Odai (Starting Words)
You can change odai (the starting words) by editing `odai.txt`.


### Create Your Own Prompt Template
You can customize the prompt template by editing `prompt_template.txt`. \
Be sure to include '{shiritori}', which acts as a placeholder for the shiritori sequence.

Example prompt template:
```
しりとりをしてください。出力はひらがなで書いてください。

{shiritori}
```

Example prompt passed to an LLM:
```
しりとりをしてください。出力はひらがなで書いてください。

かいしゃ -> しゃかい -> 
```
