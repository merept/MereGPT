from gpt.gpt import MereGPT
from gpt.room import ChatRooms


def chat(gpt: MereGPT):
    print(gpt.gpt)
    while True:
        user_input = input('\n\033[32mUser\033[0m > ')
        if user_input == '':
            gpt.save()
            raise KeyError()
        try:
            gpt.send(user_input)
        except ConnectionError as e:
            print(f'\033[31mError\033[0m > {e.args[0]}')
