import os

from service.selectRoom import room_list


def change_name(chat_rooms):
    os.system('cls')
    os.system('title 修改聊天室名称')
    room = room_list(chat_rooms)
    gpt = chat_rooms.gpt(room)
    os.system('cls')
    print(f'当前修改的聊天室: {gpt.name}')
    new_name = input('输入新名称 > ')
    gpt.change(new_name)
    chat_rooms.change(room, gpt.room_info)
    os.system('cls')
