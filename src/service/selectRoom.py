import os


def none_records():
    os.system('cls')
    print('当前没有聊天记录')
    input()
    raise KeyError()


def select_room(max_index):
    while True:
        try:
            s = input('请输入选项 > ')
            if s == '':
                return -1
            select = int(s)
            if max_index >= select >= 1:
                return select
        except ValueError:
            pass
        print('输入错误，请重新输入\n')


def room_list(chat_rooms):
    os.system('cls')
    print('聊天室:')
    rooms = chat_rooms.rooms
    if len(rooms) == 0:
        none_records()
    for i, r in enumerate(rooms):
        print(f'{i + 1}.{r}')
    room = select_room(len(rooms))
    if room == -1:
        raise KeyError()
    return room - 1
