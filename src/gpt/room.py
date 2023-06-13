from .gpt import MereGPT
import json


class ChatRooms:
    @property
    def rooms(self):
        rooms = []
        for room in self.__rooms_dict:
            rooms.append(room['name'])
        return rooms

    def __init__(self):
        with open(r'..\resource\rooms.json', 'r', encoding='utf-8') as file:
            self.__rooms_dict = json.load(file)

    def gpt(self, index):
        file_name = self.__rooms_dict[index]['file']
        file_path = fr'..\resource\chats\{file_name}.json'
        with open(file_path, 'r', encoding='utf-8') as file:
            room = json.load(file)
        return MereGPT(room['name'], room['records'], file_name)

    def append(self, new_room):
        self.__rooms_dict.append(new_room)
        self.save()

    def change(self, index, new_room):
        self.__rooms_dict[index] = new_room
        self.save()

    def save(self):
        with open(r'..\resource\rooms.json', 'w', encoding='utf-8') as file:
            json.dump(self.__rooms_dict, file, indent=2, ensure_ascii=False)

