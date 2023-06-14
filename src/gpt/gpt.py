import json
import os
from datetime import datetime

import requests
from sseclient import SSEClient


class MereGPT:
    __default_key = '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'
    __default_url = 'https://service-1x003fok-1318250575.hk.apigw.tencentcs.com/v1/chat/completions'

    def __init__(self, name: str = None, records: list = None, path: str = None,
                 api_key: str = None, url: str = None):
        self.name = name
        self.records = records
        self.path = path
        self.api_key = api_key
        self.url = url

    @property
    def room_info(self):
        return {
            'name': self.name,
            'file': self.path
        }

    @property
    def headers(self):
        return {
            'Accept': 'text/event-stream',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

    @property
    def data(self):
        reduce = self.check_length(-len(self.records))
        return {
            "model": "gpt-3.5-turbo-16k-0613",
            "messages": self.records[reduce:],
            "max_tokens": 2048,
            "stream": True
        }

    def check_length(self, reduce):
        if abs(reduce) > 40:
            reduce = -40
        length = len(str(self.records[reduce:]))
        if length >= 2048:
            return self.check_length(reduce + 1)
        else:
            return reduce

    def receive(self, record):
        response = {
            'role': 'assistant',
            'content': record
        }
        self.records.append(response)

    def send(self, record):
        self.records.append({"role": "user", "content": record})

        # response = requests.post(self.url, stream=True, headers=self.headers, json={'prompt': record})
        response = requests.post(self.url, stream=True, headers=self.headers, json=self.data)
        client = SSEClient(response)

        if response.status_code == 200:
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
            self.receive(result)
        elif response.status_code == 429:
            del self.records[-1]
            raise ConnectionError(
                "短时间内请求次数太多。\n本程序默认 API Key 为免费使用，使用频率被限制为 3 次/分钟。请 20 秒之后重试")
        else:
            del self.records[-1]
            error_message = response.json()["error"]["message"]
            raise ConnectionError(f"请求失败: Error {response.status_code}\n{error_message}")

    def save(self):
        chat = {
            "name": self.name,
            "records": self.records
        }

        with open(fr'..\resource\chats\{self.path}.json', 'w', encoding='utf-8') as file:
            json.dump(chat, file, indent=2, ensure_ascii=False)

    def change(self, new_name):
        os.remove(fr'..\resource\chats\{self.path}.json')
        self.name = new_name
        self.path = new_name.lower().replace(' ', '_')
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
            file_name = self.name.lower().replace(' ', '_')
            self.__path = f'{file_name}'
        else:
            self.__path = value

    @property
    def api_key(self):
        return self.__api_key

    @api_key.setter
    def api_key(self, value):
        if not value:
            self.__api_key = self.__default_key
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
