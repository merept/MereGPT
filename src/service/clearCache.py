import os

from exceptions.exceptions import ReturnInterrupt
from service.confirm import confirm

units = ('Bytes', 'KB', 'MB')


def alternate_units(num, index=0):
    if num >= 1024 and index < 2:
        return alternate_units(num / 1024, index + 1)
    return f'{num:.2f} {units[index]}'


def get_size():
    chats_path = r'.\resource\chats'
    chats_list = os.listdir(chats_path)
    size = 0
    for chat_file in chats_list:
        file_path = os.path.join(chats_path, chat_file)
        if os.path.isfile(file_path):
            size += os.path.getsize(file_path)
    return alternate_units(size)


def clear(chat_rooms):
    os.system('cls')
    os.system('title 清除聊天记录')
    print(f'当前占用空间 {get_size()}')
    if not confirm('是否清空记录?(Y/N)'):
        raise ReturnInterrupt('clearCache')
    chat_rooms.clear()
    os.system('cls')
