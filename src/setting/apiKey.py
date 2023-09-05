import json

import requests

from exceptions.exceptions import ReturnInterrupt
from utils import terminal


def check_api_key(api_key, url):
    try:
        response = requests.get(f'https://api.openai-sb.com/sb-api/user/status?api_key={api_key}')
        response = json.loads(response.text)
    except requests.exceptions.ConnectionError:
        return True
    if response['code'] == '0':
        return True
    return False


def set_key(is_first_time=False):
    terminal.clear_screen()
    terminal.change_title('配置 API Key')
    if is_first_time:
        print('在开始前，您需要先配置您的 API Key')
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
            '请前往 https://openai-sb.com/api/openai-sb/#api-key-%E8%8E%B7%E5%8F%96%E6%96%B9%E5%BC%8F\n'
            '根据教程重新获取您的 API Key\n\n'
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
