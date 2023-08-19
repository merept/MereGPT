import json
import os

from exceptions.exceptions import ConfigError
from .gpt import MereGPT


class ChatRooms:
    @property
    def rooms(self):
        rooms = []
        for room in self.__rooms_dict['rooms']:
            rooms.append(room['name'])
        return rooms

    def __init__(self):
        if not os.path.exists('./resource/rooms.json'):
            self.__rooms_dict = {
                'total_tokens': 0,
                'rooms': []
            }
            with open('./resource/rooms.json', 'w', encoding='utf-8') as file:
                json.dump(self.__rooms_dict, file, indent=2, ensure_ascii=False)
        with open('./resource/rooms.json', 'r', encoding='utf-8') as file:
            rooms_dict = json.load(file)
            if isinstance(rooms_dict, list):
                rooms_dict = {
                    'total_tokens': 0,
                    'rooms': rooms_dict
                }
            self.__rooms_dict = rooms_dict
            self.save()
        with open('./resource/config.json', 'r', encoding='utf-8') as file:
            self.config = json.load(file)
        if not self.config['apiKey']:
            raise ConfigError('apiKey')

    def gpt(self, index: int):
        file_name = self.__rooms_dict['rooms'][index]['file']
        file_path = f'./resource/chats/{file_name}.json'
        with open(file_path, 'r', encoding='utf-8') as file:
            room = json.load(file)
        return MereGPT(room['name'], room['records'], file_name, self.config['maxTokens'],
                       self.config['apiKey'], self.config['proxyUrl'], self.config['model'])

    def append(self, new_room: dict):
        self.__rooms_dict['rooms'].append(new_room)
        self.save()

    def change(self, index: int, new_room: dict):
        self.__rooms_dict['rooms'][index] = new_room
        self.save()

    def save(self):
        with open('./resource/rooms.json', 'w', encoding='utf-8') as file:
            json.dump(self.__rooms_dict, file, indent=2, ensure_ascii=False)

    def delete(self, index: int):
        room = self.__rooms_dict['rooms'].pop(index)
        os.remove(f'./resource/chats/{room["file"]}.json')
        self.save()

    def clear(self):
        for root, dirs, files in os.walk('./resource/chats'):
            for file in files:
                os.remove(os.path.join(root, file))
        total_tokens = self.__rooms_dict['total_tokens']
        self.__rooms_dict = {
            'total_tokens': total_tokens,
            'rooms': []
        }
        self.save()
