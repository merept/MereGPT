from gpt.room import ChatRooms
from service import newChat, oldChat, changeName, deleteChat, clearCache
from setting import setting
from utils import *


def execute(s, chat_rooms):
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
    elif s == 6:
        setting.main()
    return s


def menu(last_time_tokens):
    terminal.change_title('MereGPT')
    chat_rooms = ChatRooms()
    if last_time_tokens:
        last_time_tokens = f'上次聊天共使用 {last_time_tokens} tokens\n'
    line = '-' * 50
    print(f'{line}\n\n'
          '欢迎使用 MereGPT\n'
          f'{last_time_tokens}'
          '提示: 在任意输入位置直接回车可以返回上一级\n\n'
          f'{line}\n'
          '1.创建新对话\n'
          '2.读取对话记录\n'
          '3.更改聊天室名称\n'
          '4.删除聊天室\n'
          '5.清空聊天记录\n'
          '6.设置\n'
          '0.退出')
    s = read.select(6, min_val=0)
    return execute(s, chat_rooms)
