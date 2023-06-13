import os

from gpt.gpt import MereGPT


def new_chat(chat_rooms):
    os.system('cls')
    gpt = MereGPT()
    print(f'当前聊天室名称: {gpt.name}')
    while True:
        user_input = input('\nInput > ')
        if user_input == '':
            gpt.save()
            chat_rooms.append(gpt.room_info)
            raise KeyError()
        try:
            receive = gpt.send(user_input)
            print(receive)
        except ConnectionError as e:
            print(e.args[0])
