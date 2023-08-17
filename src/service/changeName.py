from gpt.room import ChatRooms
from service.selectRoom import room_list
from utils import terminal


def change_name(chat_rooms: ChatRooms):
    terminal.clear_screen()
    terminal.change_title('修改聊天室名称')
    room = room_list(chat_rooms)
    gpt = chat_rooms.gpt(room)
    terminal.clear_screen()
    print(f'当前修改的聊天室: {gpt.name}')
    new_name = input('输入新名称 > ')
    gpt.change(new_name)
    chat_rooms.change(room, gpt.room_info)
    terminal.clear_screen()
