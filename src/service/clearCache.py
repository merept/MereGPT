import os

from service.confirm import confirm


def clear(chat_rooms):
    os.system('cls')
    if not confirm('是否清空记录?(Y/N)'):
        raise KeyError()
    chat_rooms.clear()
    os.system('cls')
