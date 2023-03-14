import time

import openai
import os
import json
from openai import OpenAIError

MODEL = "gpt-3.5-turbo"
WELCOME_MSG = "[New Conversation] Using OpenAI Chat API(" + MODEL + ")."

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CONVERSATION_LOG_PATH = CURRENT_DIR + '/conversation_log.json'
CONFIG_PATH = CURRENT_DIR + '/config.json'


def ask(key, msg):
    openai.api_key = key

    try:
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=msg,
            # top_p=0.05
        )
    except OpenAIError as e:
        print(e)
        return "null"

    result = ''
    for choice in response.choices:
        result += choice.message.content
    return result


def save_conversation(c):
    with open(CONVERSATION_LOG_PATH, encoding="utf-8", mode='a') as file:
        c.insert(0, {"timestamp": int(time.time())})
        file.write("\n," + json.dumps(c))


if __name__ == '__main__':
    print(WELCOME_MSG)
    conversation = []

    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)
        api_key = config['api_key']

    while True:
        line = input(">")
        if line == "":
            continue
        elif line == "clear":
            save_conversation(conversation)
            conversation = []
            os.system('cls' if os.name == 'nt' else 'clear')
            print(WELCOME_MSG)
            continue
        elif line == "q":
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

        resp = ask(api_key, conversation)
        resp = resp.lstrip('\n')  # remove any \n before the actual reply
        conversation.append({"role": "assistant", "content": resp})
        print(resp)
