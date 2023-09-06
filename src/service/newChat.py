from gpt.gpt import MereGPT
from gpt.room import ChatRooms
from service.chat import chat
from utils import terminal


def new_chat(chat_rooms: ChatRooms):
    terminal.clear_screen()
    print('正在加载新对话...')
    gpt = MereGPT(
        max_tokens=chat_rooms.config['maxTokens'],
        api_key=chat_rooms.config['apiKey'],
        url=chat_rooms.config['proxyUrl'],
        model=chat_rooms.config['model']
    )
    gpt.save()
    chat_rooms.append(gpt.room_info)
    terminal.clear_screen()
    terminal.change_title(gpt.name)
    print(f'当前聊天室: {gpt.name}')
    chat(gpt)
