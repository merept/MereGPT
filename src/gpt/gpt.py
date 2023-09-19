import json
import uuid
from datetime import datetime

import requests
from sseclient import SSEClient

from exceptions.exceptions import ConfigError
from setting.card import get_tokens


class MereGPT:
    """
    包含一个聊天室所需所有信息，并可以调用 OpenAI API，向其发送信息

    属性:
        name - 聊天室名称
        records - 聊天室的所有聊天记录
        path - 聊天记录文件路径
        api_key - OpenAI API key
        url - 请求链接
        model - 请求的 GPT 模型
        room_info - 包含 name 及 path 属性的字典

    方法:
        send(record: str) - 向 OpenAI API 发送请求，请求信息为形参 record，并在终端打印响应信息
        save() - 将聊天室的名称及聊天记录保存到 path 属性指向的文件路径
        change(new_name: str) - 将聊天室的 name 属性更改为 new_name 并保存
    """
    __default_url = 'https://api.openai-sb.com/v1/chat/completions'
    __default_gpt = 'gpt-3.5-turbo'

    def __init__(self, name: str = None, records: list = None, path: str = None, max_tokens: int = 1024,
                 api_key: str = None, url: str = None, model: str = None, chatting: bool = False):
        self.name = name
        self.records = records
        self.path = path
        self.api_key = api_key
        self.__max_tokens = max_tokens
        self.url = url
        self.model = model
        if chatting:
            self.__used_tokens = get_tokens(self.api_key)

    @property
    def room_info(self):
        return {
            'name': self.name,
            'file': self.path
        }

    @property
    def this_time_tokens(self):
        return get_tokens(self.api_key) - self.__used_tokens

    @property
    def __headers(self):
        return {
            'Accept': 'text/event-stream',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

    @property
    def __data(self):
        reduce = self.__check_length(-len(self.records))
        return {
            "model": self.model,
            "messages": self.records[reduce:],
            "max_tokens": 2048,
            "stream": True
        }

    def __check_length(self, reduce):
        if reduce < -20:
            reduce = -20
        # length = tokens.counts(self.records[reduce:])
        length = len(self.records[reduce:])
        if length >= self.__max_tokens:
            return self.__check_length(reduce + 1)
        else:
            return reduce

    def __receive(self, record):
        with open('./resource/rooms.json', 'r', encoding='utf-8') as file:
            rooms_dict = json.load(file)
        with open('./resource/rooms.json', 'w', encoding='utf-8') as file:
            json.dump(rooms_dict, file, indent=2, ensure_ascii=False)
        response = {
            'role': 'assistant',
            'content': record
        }
        self.records.append(response)
        self.save()

    def __print(self, client: SSEClient):
        result = ''
        print('\033[34mGPT\033[0m > ', end='')
        for event in client.events():
            if event.data == '[DONE]':
                break
            data = json.loads(event.data)['choices'][0]
            if not data['finish_reason']:
                content = data["delta"]['content']
                result += content
                print(content, end="", flush=True)
        print()
        self.__receive(result)

    def send(self, record: str) -> None:
        self.records.append({"role": "user", "content": record})

        try:
            data = self.__data
            response = requests.post(self.url, stream=True, headers=self.__headers, json=data)
            client = SSEClient(response)
        except requests.exceptions.ConnectionError:
            del self.records[-1]
            raise ConnectionError('请求失败:\n网络连接超时，请检查网络')

        if response.status_code == 200:
            self.__print(client)
        # elif response.status_code == 429:
        #     del self.records[-1]
        #     error_message = response.json()["error"]["message"]
        #     if 'rate limit' in error_message.lower():
        #         raise ConnectionError("短时间内请求次数太多，请稍后 (一般为 20 秒) 重试。")
        #     elif 'plan and billing details' in error_message.lower():
        #         raise ConnectionError(
        #             "您的 API 用量已不足。\n请前往 OpenAI 官网检查您账户中订阅和计费的详细情况。")
        #     else:
        #         raise ConnectionError(f"请求失败: Error {response.status_code}\n{error_message}")
        else:
            del self.records[-1]
            error_message = response.json()["error"]["message"]
            raise ConnectionError(f"请求失败: Error {response.status_code}\n{error_message}")

    def save(self):
        chat = {
            "name": self.name,
            "records": self.records
        }

        with open(f'./resource/chats/{self.path}.json', 'w', encoding='utf-8') as file:
            json.dump(chat, file, indent=2, ensure_ascii=False)

    def change(self, new_name: str):
        self.name = new_name
        self.save()

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not value:
            now = datetime.now().strftime('%m%d%H%M')
            self.__name = f'NewChat_{now}'
        else:
            self.__name = value

    @property
    def records(self):
        return self.__records

    @records.setter
    def records(self, value):
        if not value:
            self.__records = []
        else:
            self.__records = value

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, value):
        if not value:
            file_uuid = uuid.uuid4()
            self.__path = f'{file_uuid}'
        else:
            self.__path = value

    @property
    def api_key(self):
        return self.__api_key

    @api_key.setter
    def api_key(self, value):
        if not value:
            raise ConfigError('apiKey')
        else:
            self.__api_key = value

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, value):
        if not value:
            self.__url = self.__default_url
        else:
            self.__url = value

    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, value):
        if not value:
            self.__model = self.__default_gpt
        else:
            self.__model = value
