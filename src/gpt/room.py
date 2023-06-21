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

    # def configure(self, init=False):
    #     if init:
    #         print('在开始前请先配置 API Key')

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
        for f in self.__rooms_dict:
            os.remove(fr'.\resource\chats\{f["file"]}.json')
        self.__rooms_dict = []
        self.save()

    # @property
    # def config(self):
    #     return self.__config
    #
    # @config.setter
    # def config(self, value: dict):
    #     self.__config = {}
    #     for k, v in value.items():
    #         if not v:
    #             self.configure(True)
    #         else:
    #             self.__config[k] = v

