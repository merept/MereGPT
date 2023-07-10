import json
import os


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
            raise KeyboardInterrupt('apiKey')
    with open(r'.\resource\config.json', 'r', encoding='utf-8') as file:
        config = json.load(file)
    config['apiKey'] = new_api_key
    with open(r'.\resource\config.json', 'w', encoding='utf-8') as file:
        json.dump(config, file, ensure_ascii=False, indent=2)
