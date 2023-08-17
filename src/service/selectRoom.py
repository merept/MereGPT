from exceptions.exceptions import ReturnInterrupt
from gpt.room import ChatRooms
from utils import *


def none_records():
    terminal.clear_screen()
    print('当前没有聊天记录')
    input()
    raise ReturnInterrupt('selectRoom')


def room_list(chat_rooms: ChatRooms):
    terminal.clear_screen()
    print('聊天室:')
    rooms = chat_rooms.rooms
    if len(rooms) == 0:
        none_records()
    for i, r in enumerate(rooms):
        print(f'{i + 1}.{r}')
    room = read.select(len(rooms))
    return room - 1
