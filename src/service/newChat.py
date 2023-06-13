import os

from gpt.gpt import MereGPT
from service.chat import chat


def new_chat(chat_rooms):
    os.system('cls')
    gpt = MereGPT()
    print(f'当前聊天室名称: {gpt.name}')
    chat(gpt, chat_rooms, True)
