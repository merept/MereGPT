from gpt.gpt import MereGPT
from gpt.room import ChatRooms


def chat(gpt: MereGPT, chat_rooms: ChatRooms, new: bool = False):
    while True:
        user_input = input('\nInput > ')
        if user_input == '':
            gpt.save()
            if new:
                chat_rooms.append(gpt.room_info)
            raise KeyError()
        try:
            receive = gpt.send(user_input)
            print(receive)
        except ConnectionError as e:
            print(e.args[0])
