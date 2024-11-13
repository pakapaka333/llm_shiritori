from typing import Union
from transformers import pipeline
import torch

def get_pipeline(model_name:str) -> pipeline:
    # create a pipe
    pipe = pipeline(
        "text-generation",
        model = model_name, 
        tokenizer = model_name,
        model_kwargs = {
            "torch_dtype": torch.bfloat16,
            },
        device_map="auto"
    )

    # You need to write additional codes here for some LLMs (e.g. models without chattemplate)

    return pipe


def generate_answer(messages:list[dict[str ,str]], pipe:pipeline, max_new_tokens:int, force_greedy:bool=True) -> Union[str, list[dict[str, str]]]:
    # sanity check
    assert all(list(m.keys())==['role', 'content'] for m in messages), f"All messages should have \'role\' and \'content\':\n\'\'\'{messages}\'\'\'"
    assert messages[-1]['role']=='user', f"The last message should be a user message, but actually the role is \'{messages[-1]['role']}\'"
    assert len(messages[-1]['content'])>0, f"The last message should not be empty"


    # detect if a model is instruction or base
    INSTRUCTION_MODEL_PATTERNS = [
        "instruct", "it", "chat", 
    ]
    is_instruct_model = any(pattern in pipe.model.config.name_or_path for pattern in INSTRUCTION_MODEL_PATTERNS)


    # generate an answer
    pipe_inputs = messages if is_instruct_model else messages[-1]['content']
    if force_greedy:
        pipe_outputs = pipe(
            pipe_inputs,
            max_new_tokens = max_new_tokens,
            pad_token_id = pipe.tokenizer.eos_token_id,
            do_sample = False,
            temperature = None,
            top_p = None,
            )
    else:
        pipe_outputs = pipe(
            pipe_inputs,
            max_new_tokens = max_new_tokens,
            pad_token_id = pipe.tokenizer.eos_token_id,
        )


    # extract generated text based on the model type
    generated_text = pipe_outputs[0]["generated_text"][-1]['content'] if is_instruct_model else pipe_outputs[0]["generated_text"][len(pipe_inputs):]


    # update messages
    messages.append({
            'role': 'assistant',
            'content': generated_text,
        })

    return generated_text, messages