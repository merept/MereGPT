import os

from gpt.room import ChatRooms
from service import newChat, oldChat, changeName, deleteChat, clearCache

try:
    os.chdir(r'.\src')
    if not os.path.exists(r'../resource/chats'):
        os.mkdir(r'../resource/chats')
except FileNotFoundError:
    pass

chat_rooms = ChatRooms()


def select():
    while True:
        try:
            s = int(input('请输入选项 > '))
            if 5 >= s >= 0:
                return s
        except ValueError:
            pass
        print('输入错误，请重新输入\n')


def execute(s):
    if s == 1:
        newChat.new_chat(chat_rooms)
    elif s == 2:
        oldChat.old_chat(chat_rooms)
    elif s == 3:
        changeName.change_name(chat_rooms)
    elif s == 4:
        deleteChat.delete(chat_rooms)
    elif s == 5:
        clearCache.clear(chat_rooms)
    return s


def menu():
    line = '-' * 50
    print(f'{line}\n\n'
          '欢迎使用 MereGPT\n'
          '提示: 在任意输入位置直接回车可以返回上一级\n\n'
          f'{line}\n'
          '1.创建新对话\n'
          '2.读取对话记录\n'
          '3.更改聊天室名称\n'
          '4.删除聊天室\n'
          '5.清空聊天记录\n'
          '0.退出')
    s = select()
    return execute(s)
