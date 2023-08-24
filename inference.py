import json
import os
from llama_cpp import Llama

GREEN_TEXT = "\033[92m"
RED_TEXT = "\033[91m"
YELLOW_TEXT = "\033[93m"
RESET_TEXT = "\033[0m"


def clear_console():
    os.system("cls" if os.name == "nt" else "clear")


def load_config(filename):
    with open(filename, "r") as file:
        config = json.load(file)
    return config


def complete(llm, prompt, completion_config):
    output = llm.create_completion(prompt=prompt, **completion_config)
    return output


config_filename = "inference.json"
llm_config = load_config(config_filename)
llm = Llama(
    **{key: value for key, value in llm_config.items() if key != "completion_config"}
)

completion_config = llm_config["completion_config"]
last_modified = os.path.getmtime(config_filename)

while True:
    if os.path.getmtime(config_filename) > last_modified:
        new_llm_config = load_config(config_filename)

        if new_llm_config["completion_config"] != llm_config["completion_config"]:
            clear_console()
            print(
                f"{RED_TEXT}---\nModel config changed, reinitializing.\n---\n{RESET_TEXT}"
            )
            completion_config = new_llm_config["completion_config"]
        else:
            clear_console()
            print(
                f"{YELLOW_TEXT}---\nText completion config changed, reloading.\n---\n{RESET_TEXT}"
            )
            llm_config = new_llm_config
            llm = Llama(
                **{
                    key: value
                    for key, value in llm_config.items()
                    if key != "completion_config"
                }
            )

        last_modified = os.path.getmtime(config_filename)

    clear_console()
    prompt = input(f"{GREEN_TEXT}Prompt:\n{RESET_TEXT}")

    output = complete(llm, prompt, completion_config)

    clear_console()
    print(f"{GREEN_TEXT}Output:\n{RESET_TEXT}{prompt}", end="")

    for item in output:
        print(item["choices"][0]["text"], end="", flush=True)

    print(
        f"{YELLOW_TEXT}\n\nText Completion Complete\n------------------------\n{RED_TEXT}Enter to continue..."
    )
    input()
