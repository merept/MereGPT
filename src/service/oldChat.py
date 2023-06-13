import os

from service.selectRoom import room_list
from service.chat import chat


def old_chat(chat_rooms):
    room = room_list(chat_rooms)
    gpt = chat_rooms.gpt(room)
    os.system('cls')
    records = gpt.records
    print(f'当前聊天室名称: {gpt.name}')
    for r in records:
        prefix = '\nInput > ' if r['role'] == 'user' else ''
        print(prefix + r['content'])
    chat(gpt, chat_rooms)
