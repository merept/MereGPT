import os

from service import selectRoom, confirm


def delete(chat_rooms):
    os.system('cls')
    os.system('title 删除聊天室')
    room = selectRoom.room_list(chat_rooms)
    gpt = chat_rooms.gpt(room)
    print(f'要删除的聊天室: {gpt.name}')
    if not confirm.confirm('是否删除该聊天室?(Y/N)'):
        raise KeyboardInterrupt()
    chat_rooms.delete(room)
    os.system('cls')
