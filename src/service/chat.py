from exceptions.exceptions import ReturnInterrupt
from gpt.gpt import MereGPT
from utils.customizeString import CustomizeOption, customize_string


def chat(gpt: MereGPT):
    while True:
        user_input = input(f'\n{customize_string("User", CustomizeOption.GREEN)} > ')
        if user_input == '':
            print(f'\n{customize_string("Tip", CustomizeOption.YELLOW)} > 正在保存对话...', end='')
            gpt.save()
            raise ReturnInterrupt(f'chat{gpt.this_time_tokens}')
        try:
            gpt.send(user_input)
        except ConnectionError as e:
            print(f'{customize_string("Error", CustomizeOption.RED)} > {e.args[0]}')
