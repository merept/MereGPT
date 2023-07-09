import os

from gpt.gpt import MereGPT


def chat(gpt: MereGPT):
    while True:
        user_input = input('\n\033[32mUser\033[0m > ')
        if user_input == '':
            gpt.save()
            raise KeyboardInterrupt()
        try:
            gpt.send(user_input)
        except ConnectionError as e:
            print(f'\033[31mError\033[0m > {e.args[0]}')
