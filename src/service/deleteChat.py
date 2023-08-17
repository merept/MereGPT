from exceptions.exceptions import ReturnInterrupt
from gpt.room import ChatRooms
from service.selectRoom import room_list
from utils import *


def delete(chat_rooms: ChatRooms):
    terminal.clear_screen()
    terminal.change_title('删除聊天室')
    room = room_list(chat_rooms)
    gpt = chat_rooms.gpt(room)
    terminal.clear_screen()
    print(f'要删除的聊天室: {gpt.name}')
    if not read.confirm('是否删除该聊天室?(Y/N)'):
        raise ReturnInterrupt('deleteChat')
    chat_rooms.delete(room)
    terminal.clear_screen()
