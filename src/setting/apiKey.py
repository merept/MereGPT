import json
import os

import requests

from exceptions.exceptions import ReturnInterrupt


def check_api_key(api_key, url):
    print('检查 API Key 中...', end='')
    if not url:
        url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Accept': 'text/event-stream',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    data = {
        "model": 'gpt-3.5-turbo-0613',
        "messages": [{'role': 'user', 'content': 'test'}]
    }
    try:
        response = requests.post(url, stream=True, headers=headers, json=data)
    except requests.exceptions.ConnectionError:
        return True
    if response.status_code == 401:
        error_message = response.json()["error"]["message"]
        if 'incorrect api key provided' in error_message.lower():
            return False
    return True


def set_key(is_first_time=False):
    os.system('cls')
    os.system('title 配置 API Key')
    if is_first_time:
        print('在开始前，您需要先配置您的 API Key')
    new_api_key = input('请输入您的 API Key > ')
    if new_api_key == '':
        if is_first_time:
            return
        else:
            raise ReturnInterrupt('apiKey')
    with open(r'.\resource\config.json', 'r', encoding='utf-8') as file:
        config = json.load(file)
    if not check_api_key(new_api_key, config['proxyUrl']):
        print(
            '\n\n您输入的 API Key 有误\n'
            '请前往 https://platform.openai.com/account/api-keys 重新获取您的 API Key\n\n'
            '回车键继续...', end=''
        )
        input()
        if is_first_time:
            return
        else:
            raise ReturnInterrupt('apiKey')
    config['apiKey'] = new_api_key
    with open(r'.\resource\config.json', 'w', encoding='utf-8') as file:
        json.dump(config, file, ensure_ascii=False, indent=2)
