import time

import openai
import os
import json
from openai import OpenAIError

CONFIG = []
WELCOME_MSG = "[New Conversation] Using OpenAI Chat API."

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CONVERSATION_LOG_PATH = CURRENT_DIR + '/conversation_log.json'
CONFIG_PATH = CURRENT_DIR + '/config.json'


def process_response(response):
    result = ''
    for choice in response.choices:
        result += choice.message.content
    print(result, end="")
    return result


def process_stream_response(responses):
    result = ''
    for response in responses:
        for choice in response.choices:
            if choice.finish_reason != "null":
                content = choice.delta.get("content")
                if content is None:
                    pass
                else:
                    print(choice.delta.content, end="")
    return result


def ask_gpt(msg):
    try:
        response = openai.ChatCompletion.create(
            model=CONFIG["model"],
            stream=CONFIG["is_stream"],
            messages=msg,
            # top_p=0.05
        )
    except OpenAIError as e:
        print(e)
        return "null"
    if CONFIG["is_stream"]:
        return process_stream_response(response)
    else:
        return process_response(response)


def save_conversation(c):
    with open(CONVERSATION_LOG_PATH, encoding="utf-8", mode='a') as file:
        c.insert(0, {"timestamp": int(time.time())})
        file.write("\n," + json.dumps(c))


if __name__ == '__main__':
    with open(CONFIG_PATH, 'r') as f:
        CONFIG = json.load(f)

    openai.api_key = CONFIG["api_key"]
    print(WELCOME_MSG)
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
            print(WELCOME_MSG)
            continue
        elif line == "q":
            if CONFIG["enable_conversation_log"]:
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
