import os

from gpt.room import ChatRooms
from service.chat import chat
from service.selectRoom import room_list
from utils import terminal
from utils.customizeString import CustomizeOption, customize_string


def get_size(name):
    path = f'./resource/chats/{name}.json'
    return os.path.getsize(path)


def old_chat(chat_rooms: ChatRooms):
    option = CustomizeOption()
    room = room_list(chat_rooms)
    print('\n正在加载聊天室...', end='')
    gpt = chat_rooms.gpt(room, True)
    terminal.clear_screen()
    records = gpt.records
    terminal.change_title(gpt.name)
    print(f'当前聊天室: {gpt.name}')
    for r in records:
        prefix = f'\n{customize_string("User", option.GREEN)}' if r['role'] == 'user' else \
            f'{customize_string("GPT", option.BLUE)} '
        print(f'{prefix} > {r["content"]}')
    size = get_size(gpt.path)
    if size > 102400:
        print(f'\n{customize_string("Tip", option.YELLOW)} > 当前聊天记录过多，建议重新开始新对话')
    chat(gpt)
