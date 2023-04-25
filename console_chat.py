import sys
import time

import openai
import os
import json
from openai import OpenAIError

import config_field_name_constants as CONFIG_FIELD

CONFIG = []
SPECIFIED_MODEL_SERIES = None
WELCOME_MSG = "[New Conversation] Using OpenAI API. Model: "

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CONVERSATION_LOG_PATH = CURRENT_DIR + '/conversation_log_utf8.json'
CONFIG_PATH = CURRENT_DIR + '/config.json'


def process_response(response):
    print("[" + response.model + "]: ", end="")
    result = ''
    for choice in response.choices:
        result += choice.message.content
    print(result, end="")
    return result


def process_stream_response(responses):
    result = ''
    try:
        for response in responses:
            for choice in response.choices:
                if choice.finish_reason is None:
                    content = choice.delta.get("content")
                    if content is None:
                        print("[" + response.model + "]: ", end="", flush=True)
                    else:
                        print(content, end="", flush=True)
    except KeyboardInterrupt:
        message = "[KeyboardInterrupt]"
        print(message, end="")
    finally:
        responses.close()
    return result


def ask_gpt(msg):
    try:
        response = openai.ChatCompletion.create(
            model=CONFIG[CONFIG_FIELD.MODEL],
            stream=CONFIG[CONFIG_FIELD.IS_STREAM],
            messages=msg,
            # top_p=0.05
        )
    except OpenAIError as e:
        print(e)
        return "OpenAIError"
    except KeyboardInterrupt:
        message = "[KeyboardInterrupt]"
        print(message, end="")
        return ""
    if CONFIG[CONFIG_FIELD.IS_STREAM]:
        return process_stream_response(response)
    else:
        return process_response(response)


def save_conversation(c):
    if len(c) == 0:
        return
    c.insert(0, {"timestamp": int(time.time())})
    with open(CONVERSATION_LOG_PATH, encoding="utf-8", mode='a') as file:
        file.write("\n," + json.dumps(c, ensure_ascii=False))


def chat():
    global CONFIG, SPECIFIED_MODEL_SERIES
    with open(CONFIG_PATH, 'r') as f:
        CONFIG = json.load(f)

    if SPECIFIED_MODEL_SERIES is not None:
        CONFIG[CONFIG_FIELD.MODEL] = SPECIFIED_MODEL_SERIES

    openai.api_key = CONFIG[CONFIG_FIELD.API_KEY]
    print(WELCOME_MSG + CONFIG[CONFIG_FIELD.MODEL])
    conversation = []

    while True:
        line = input(">")
        if line == "":
            continue
        elif line == "clear":
            if CONFIG["enable_conversation_log"]:
                save_conversation(conversation)
            conversation = []
            os.system('cls' if os.name == 'nt' else 'clear')
            print(WELCOME_MSG + CONFIG[CONFIG_FIELD.MODEL])
            continue
        elif line == "q":
            if CONFIG[CONFIG_FIELD.ENABLE_CONVERSATION_LOG]:
                save_conversation(conversation)
            break
        elif line == "m":
            print("[Multi-line input enabled. A new line only including ~~~ for end of input]")
            line = ""
            while True:
                i = input()
                if "~~~" == i:
                    print("[Multi-line input disabled]")
                    break
                line += i + "\n"
        conversation.append({"role": "user", "content": line})

        resp = ask_gpt(conversation)
        resp = resp.lstrip('\n')  # remove any \n before the actual reply
        conversation.append({"role": "assistant", "content": resp})
        print()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "history":
            print(CONVERSATION_LOG_PATH)
            exit()
        elif cmd.lower() == "gpt3":
            SPECIFIED_MODEL_SERIES = "gpt-3.5-turbo"
        elif cmd.lower() == "gpt4":
            SPECIFIED_MODEL_SERIES = "gpt-4"
    chat()
