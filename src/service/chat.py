from exceptions.exceptions import ReturnInterrupt
from gpt.gpt import MereGPT


def chat(gpt: MereGPT):
    while True:
        user_input = input('\n\033[32mUser\033[0m > ')
        if user_input == '':
            print('\n\033[33mTip\033[0m > 正在保存对话...', end='')
            gpt.save()
            raise ReturnInterrupt(f'chat{gpt.this_time_tokens}')
        try:
            gpt.send(user_input)
        except ConnectionError as e:
            print(f'\033[31mError\033[0m > {e.args[0]}')
