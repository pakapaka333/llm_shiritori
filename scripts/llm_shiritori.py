import pandas as pd
import re
import time
from utils import get_pipeline, generate_answer


def play_shiritori(model_name:str, prompt_template:str, odai:list[str], log_path:str, overall_path:str, max_chains:int=10, max_new_tokens:int=21, force_greedy:bool=True):
    # get a pipeline
    pipe = get_pipeline(model_name)


    # play shiritori
    small_letters = ['ぁ', 'ぃ', 'ぅ', 'ぇ', 'ぉ', 'ゃ', 'ゅ', 'ょ', 'ゎ']
    small2big_table = str.maketrans(
        'ぁぃぅぇぉゃゅょゎ',
        'あいうえおやゆよわ'
    )
    chains = []
    scores = []
    for i, odai in enumerate(odai, 1):
        # init
        prev_word_view = odai
        prev_word = prev_word_view.rstrip('ー')
        prev_word = prev_word[:-1]+prev_word[-1].translate(small2big_table) if len(prev_word)>1 else prev_word

        shiritori = f"{prev_word_view} -> "
        word_history = [prev_word_view]
        num_chains = 0

        # show the progress
        print(f"Odai{i}: '{odai}'\n{odai} -> ", end='')
        shiritori_view = shiritori

        while num_chains < max_chains:
            # get a next word
            prompt = prompt_template.replace('{shiritori}', shiritori)
            gen_ans, _ = generate_answer([{'role': 'user', 'content': prompt}], pipe, max_new_tokens, force_greedy)
            next_word_view = re.split(r'\s', gen_ans.replace('\\n', '\n'))[0]

            # correction
            next_word = next_word_view.rstrip('ー')
            next_word = next_word[:-1]+next_word[-1].translate(small2big_table) if len(next_word)>1 else next_word

            # assess the next word
            failure_types = []
            if len(next_word)==0:
                failure_types.append("Failed to extract a model answer")

            else:
                if not (re.fullmatch(r'[ぁ-ゖー]+', next_word)):
                    failure_types.append("The word is not hiragana")

                if not (next_word[-1]!='ん'):
                    failure_types.append("The word ends with 'ん'")

                if not (next_word_view not in word_history):
                    failure_types.append("The word appeared twice.")
                
                if not (next_word[0]==prev_word[-1]):
                    if (prev_word_view[-1] in small_letters) and (len(prev_word)>=2 and len(next_word)>=2):
                        # check two letters ending with a small letter (e.g. 'しゃ')
                        prev_word_view_wo_longsymbol = prev_word_view[:-1] if prev_word_view[-1]=="ー" else prev_word_view
                        if not(prev_word_view_wo_longsymbol[-2:] == next_word_view[:2]):
                            failure_types.append(f"The word does not start with the last character of the previous word.{prev_word_view_wo_longsymbol[-2:]} {next_word_view[:2]}")
                    else:
                        failure_types.append(f"The word does not start with the last character of the previous word.")

            if len(failure_types)==0:
                if num_chains+1<max_chains:
                    shiritori_view = f"{next_word_view}\n-> " if (num_chains+1)%5==0 else f"{next_word_view} -> "
                else:
                    shiritori_view = f"{next_word_view}\nSucceeded: {max_chains} chains.\n"
                print(shiritori_view,  end='')
                
                # step
                prev_word_view = next_word_view
                prev_word = next_word
                shiritori = f"{shiritori}{next_word_view} -> "
                word_history.append(next_word_view)
                num_chains += 1
                
            else:
                # show the progress
                failure_types_oneline = ', '.join(failure_types)
                shiritori_view = f"{next_word_view}\nFailed: {failure_types_oneline}\n"
                print(shiritori_view, end='')

                # step
                shiritori = f"{shiritori}{next_word_view}"
                break

            # time.sleep(1)

        # record
        chains.append(shiritori)
        scores.append(num_chains)
        print(f"Score: {num_chains}/{max_chains}\n")


    # aggregate results
    current_date_time = time.strftime("%m/%d/%H:%M:%S")
    df_log = pd.DataFrame(
        data = {
            "model": model_name,
            "odai": odai,
            "scores": scores,
            "chains": chains,
            "prompt": prompt_template,
            "date": current_date_time,            
        }
    )
    total_score = df_log['scores'].sum()
    print(f"Total Score: {total_score}/{len(odai)*max_chains}")

    df_overall = pd.DataFrame(
        data  = [
            {
                "model": model_name,
                "score": total_score,
                "date": current_date_time,
                "prompt": prompt_template,
            }
        ]
    )


    # output the results
    df_log.to_json(log_path, orient='records', lines=True, force_ascii=False, mode='a')
    df_overall.to_json(overall_path, orient='records', lines=True, force_ascii=False, mode='a')
