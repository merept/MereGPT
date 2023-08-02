import json

from exceptions.exceptions import ReturnInterrupt
from utils import *


def change():
    terminal.clear_screen()
    terminal.change_title('获取测试版更新')
    with open('./resource/config.json', 'r', encoding='utf-8') as file:
        config = json.load(file)
        try:
            dev_now = config['dev']
        except KeyError:
            config['dev'] = False
            dev_now = config['dev']
    dev_now_str = "测试版" if dev_now else "发行版"
    dev_change_edi = "发行版" if dev_now else "测试版"
    print(f'当前更新获取的版本: {dev_now_str}')
    if read.confirm(f'是否更改为{dev_change_edi}?(Y/N)'):
        config['dev'] = not dev_now
    else:
        raise ReturnInterrupt('devEdition')
    with open('./resource/config.json', 'w', encoding='utf-8') as file:
        json.dump(config, file, ensure_ascii=False, indent=2)
