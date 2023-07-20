import json
import os

from exceptions.exceptions import ReturnInterrupt
from service.confirm import confirm


def get_current_url(config):
    current_url = config["proxyUrl"]
    if not current_url:
        return 'https://api.openai.com/v1/chat/completions'
    return current_url


def set_url():
    os.system('cls')
    os.system('title 配置代理地址')
    with open(r'.\resource\config.json', 'r', encoding='utf-8') as file:
        config = json.load(file)
    print(f'当前代理地址: {get_current_url(config)}')
    new_url = input('请输入您的代理地址 > ')
    if new_url == '':
        if not confirm('是否将代理地址设为默认?(Y/N)'):
            raise ReturnInterrupt('proxyUrl')
    config['proxyUrl'] = new_url
    with open(r'.\resource\config.json', 'w', encoding='utf-8') as file:
        json.dump(config, file, ensure_ascii=False, indent=2)
