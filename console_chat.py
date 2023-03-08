import openai
import os
import json

MODEL = "gpt-3.5-turbo"
WELCOME_MSG = "[New Conversation] Using OpenAI Chat API("+MODEL+")."


def ask(key, msg):
    openai.api_key = key

    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=msg,
        # top_p=0.05
    )
    result = ''
    for choice in response.choices:
        result += choice.message.content
    return result


if __name__ == '__main__':
    print(WELCOME_MSG)
    conversation = []

    with open('config.json', 'r') as f:
        config = json.load(f)
        api_key = config['api_key']

    while True:
        print(">", end="")
        line = input()
        conversation.append({"role": "user", "content": line})
        if line == "clear":
            conversation = []
            os.system('cls' if os.name == 'nt' else 'clear')
            print(WELCOME_MSG)
            continue
        elif line == "q":
            break
        resp = ask(api_key, conversation)
        resp = resp.lstrip('\n')  # remove any \n before the actual reply
        conversation.append({"role": "assistant", "content": resp})
        print(resp)
