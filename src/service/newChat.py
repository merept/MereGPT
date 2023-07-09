import os

from gpt.gpt import MereGPT
from gpt.room import ChatRooms
from service.chat import chat


def new_chat(chat_rooms: ChatRooms):
    os.system('cls')
    gpt = MereGPT(
        api_key=chat_rooms.config['apiKey'],
        url=chat_rooms.config['proxyUrl'],
        model=chat_rooms.config['model']
    )
    gpt.save()
    chat_rooms.append(gpt.room_info)
    os.system(f'title {gpt.name}')
    print(f'当前聊天室: {gpt.name}')
    chat(gpt)
