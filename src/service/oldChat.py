import os

from service.chat import chat
from service.selectRoom import room_list


def old_chat(chat_rooms):
    room = room_list(chat_rooms)
    gpt = chat_rooms.gpt(room)
    os.system('cls')
    records = gpt.records
    print(f'当前聊天室名称: {gpt.name}')
    for r in records:
        prefix = '\n\033[32mUser\033[0m' if r['role'] == 'user' else '\033[34mGPT\033[0m'
        print(f'{prefix} > {r["content"]}')
    chat(gpt)
