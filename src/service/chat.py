import json

from gpt.gpt import MereGPT
from gpt.room import ChatRooms
from sseclient import SSEClient


def chat(gpt: MereGPT, chat_rooms: ChatRooms, new: bool = False):
    while True:
        user_input = input('\n\033[32mUser\033[0m > ')
        if user_input == '':
            gpt.save()
            if new:
                chat_rooms.append(gpt.room_info)
            raise KeyError()
        try:
            gpt.send(user_input)
        except ConnectionError as e:
            print(f'\033[31mError\033[0m > {e.args[0]}')
