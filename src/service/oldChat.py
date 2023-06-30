import os

from service.chat import chat
from service.selectRoom import room_list


def get_size(name):
    path = fr'.\resource\chats\{name}.json'
    return os.path.getsize(path)


def old_chat(chat_rooms):
    room = room_list(chat_rooms)
    gpt = chat_rooms.gpt(room)
    os.system('cls')
    records = gpt.records
    os.system(f'title {gpt.name}')
    print(f'当前聊天室: {gpt.name}')
    for r in records:
        prefix = '\n\033[32mUser\033[0m' if r['role'] == 'user' else '\033[34mGPT\033[0m'
        print(f'{prefix} > {r["content"]}')
    size = get_size(gpt.path)
    if size > 102400:
        print('\n\033[33mTip\033[0m > 当前聊天记录过多，建议重新开始新对话')
    chat(gpt)
