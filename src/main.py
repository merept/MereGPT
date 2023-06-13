import os

import dict2str
from gpt.gpt import MereGPT
from gpt.room import ChatRooms

try:
    os.chdir(r'.\src')
    if not os.path.exists(r'..\resource\chats'):
        os.mkdir(r'..\resource\chats')
except FileNotFoundError:
    pass

chat_rooms = ChatRooms()


def new_chat():
    os.system('cls')
    gpt = MereGPT()
    print(f'当前聊天室名称: {gpt.name}')
    while True:
        user_input = input('\nInput > ')
        if user_input == '':
            gpt.save()
            chat_rooms.append(gpt.room_info)
            main()
        try:
            receive = gpt.send(user_input)
            print(receive)
        except ConnectionError as e:
            print(e.args[0])


def old_chat(gpt: MereGPT):
    os.system('cls')
    records = gpt.records
    print(f'当前聊天室名称: {gpt.name}')
    for r in records:
        prefix = '\nInput > ' if r['role'] == 'user' else ''
        print(prefix + r['content'])
    while True:
        user_input = input('\nInput > ')
        if user_input == '':
            gpt.save()
            main()
        try:
            receive = gpt.send(user_input)
            print(receive)
        except ConnectionError as e:
            print(e.args[0])


def none_records():
    os.system('cls')
    print('当前没有聊天记录')
    input()
    main()


def select_room(max_index):
    while True:
        try:
            s = input('输入选项 > ')
            if s == '':
                return -1
            select = int(s)
            if max_index >= select >= 1:
                return select
        except ValueError:
            pass
        print('输入错误，请重新输入')


def room_list():
    os.system('cls')
    print('聊天室:')
    rooms = chat_rooms.rooms
    if len(rooms) == 0:
        none_records()
    for i, r in enumerate(rooms):
        print(f'{i + 1}.{r}')
    room = select_room(len(rooms))
    if room == -1:
        main()
    return room - 1


def change_name(room):
    os.system('cls')
    gpt = chat_rooms.gpt(room)
    print(f'当前修改的聊天室: {gpt.name}')
    new_name = input('输入新名称 > ')
    gpt.change(new_name)
    chat_rooms.change(room, gpt.room_info)


def delete(room):
    os.system('cls')
    gpt = chat_rooms.gpt(room)
    print(f'要删除的聊天室: {gpt.name}')
    confirm = input('是否删除该聊天室?(Y/N)').lower()
    while confirm != 'y':
        if confirm in ('n', ''):
            main()
        print('输入错误，请重新输入\n')
        confirm = input('是否清空记录?(Y/N)').lower()
    chat_rooms.delete(room)


def clear():
    os.system('cls')
    confirm = input('是否清空记录?(Y/N)').lower()
    while confirm != 'y':
        if confirm in ('n', ''):
            main()
        print('输入错误，请重新输入\n')
        confirm = input('是否清空记录?(Y/N)').lower()
    chat_rooms.clear()


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
    s = input('请输入选项 > ')
    if s == '1':
        new_chat()
        return 1
    elif s == '2':
        room = room_list()
        gpt = chat_rooms.gpt(room)
        old_chat(gpt)
        return 2
    elif s == '3':
        room = room_list()
        change_name(room)
        os.system('cls')
        return 3
    elif s == '4':
        room = room_list()
        delete(room)
        os.system('cls')
        return 4
    elif s == '5':
        clear()
        os.system('cls')
        return 5
    else:
        return 0


def log(records):
    records_dict = {index: value for index, value in enumerate(records)}
    print(f'Records: {dict2str.to_string(records_dict)}')


def main():
    os.system('cls')
    selection = -1
    while selection != 0:
        selection = menu()
    exit(0)


if __name__ == '__main__':
    main()
