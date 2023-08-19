import json

import requests

from exceptions.exceptions import ReturnInterrupt
from utils import terminal


def get_total_tokens():
    with open('./resource/config.json', 'r', encoding='utf-8') as file:
        model = json.load(file)['model']
        if '16k' in model:
            billing = '$0.004 / 1K tokens'
        else:
            billing = '$0.002 / 1K tokens'
    with open('./resource/rooms.json', 'r', encoding='utf-8') as file:
        total_tokens = json.load(file)['total_tokens']
        if total_tokens >= 10000:
            total_tokens = f'{total_tokens / 10000:.1f}K'
        if total_tokens >= 1000000:
            total_tokens = f'{total_tokens / 1000000:.1f}M'
    return billing, total_tokens


def check_api_key(api_key, url):
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
        response = requests.post(url, headers=headers, json=data)
    except requests.exceptions.ConnectionError:
        return True
    if response.status_code == 401:
        error_message = response.json()["error"]["message"]
        if 'incorrect api key provided' in error_message.lower():
            return False
    return True


def clear_tokens_count():
    with open('./resource/rooms.json', 'r', encoding='utf-8') as file:
        rooms_dict = json.load(file)
        rooms_dict['total_tokens'] = 0
    with open('./resource/rooms.json', 'w', encoding='utf-8') as file:
        json.dump(rooms_dict, file, ensure_ascii=False)


def set_key(is_first_time=False):
    terminal.clear_screen()
    terminal.change_title('配置 API Key')
    if is_first_time:
        print('在开始前，您需要先配置您的 API Key')
    else:
        billing, total_tokens = get_total_tokens()
        print(f'当前 API 用量: {total_tokens} tokens\n计费标准: {billing}\n')
    new_api_key = input('请输入您的 API Key > ')
    if new_api_key == '':
        if is_first_time:
            return
        else:
            raise ReturnInterrupt('apiKey')
    with open('./resource/config.json', 'r', encoding='utf-8') as file:
        config = json.load(file)
    print('检查 API Key 中...')
    if not check_api_key(new_api_key, config['proxyUrl']):
        print(
            '\n您输入的 API Key 有误\n'
            '请前往 https://platform.openai.com/account/api-keys 重新获取您的 API Key\n\n'
            '回车键继续...', end=''
        )
        input()
        if is_first_time:
            return
        else:
            raise ReturnInterrupt('apiKey')
    config['apiKey'] = new_api_key
    with open('./resource/config.json', 'w', encoding='utf-8') as file:
        json.dump(config, file, ensure_ascii=False, indent=2)
    clear_tokens_count()
