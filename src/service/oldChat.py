import os

from service.selectRoom import room_list


def old_chat(chat_rooms):
    room = room_list(chat_rooms)
    gpt = chat_rooms.gpt(room)
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
            raise KeyError()
        try:
            receive = gpt.send(user_input)
            print(receive)
        except ConnectionError as e:
            print(e.args[0])
