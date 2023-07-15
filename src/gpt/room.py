import json
import os

from .gpt import MereGPT


class ChatRooms:
    @property
    def rooms(self):
        rooms = []
        for room in self.__rooms_dict:
            rooms.append(room['name'])
        return rooms

    def __init__(self):
        if not os.path.exists(r'.\resource\rooms.json'):
            self.__rooms_dict = []
            with open(r'.\resource\rooms.json', 'w', encoding='utf-8') as file:
                json.dump(self.__rooms_dict, file, indent=2, ensure_ascii=False)
        with open(r'.\resource\rooms.json', 'r', encoding='utf-8') as file:
            self.__rooms_dict = json.load(file)
        with open(r'.\resource\config.json', 'r', encoding='utf-8') as file:
            self.config = json.load(file)
        if not self.config['apiKey']:
            raise ValueError()

    def gpt(self, index):
        file_name = self.__rooms_dict[index]['file']
        file_path = fr'.\resource\chats\{file_name}.json'
        with open(file_path, 'r', encoding='utf-8') as file:
            room = json.load(file)
        return MereGPT(room['name'], room['records'], file_name,
                       self.config['apiKey'], self.config['proxyUrl'], self.config['model'])

    def append(self, new_room):
        self.__rooms_dict.append(new_room)
        self.save()

    def change(self, index, new_room):
        self.__rooms_dict[index] = new_room
        self.save()

    def save(self):
        with open(r'.\resource\rooms.json', 'w', encoding='utf-8') as file:
            json.dump(self.__rooms_dict, file, indent=2, ensure_ascii=False)

    def delete(self, index):
        room = self.__rooms_dict.pop(index)
        os.remove(fr'.\resource\chats\{room["file"]}.json')
        self.save()

    def clear(self):
        for root, dirs, files in os.walk('./resource/chats'):
            for file in files:
                os.remove(os.path.join(root, file))
        self.__rooms_dict = []
        self.save()
