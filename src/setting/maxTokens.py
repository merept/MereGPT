import json

from exceptions.exceptions import ReturnInterrupt
from utils import *


def read_int(msg):
    while True:
        try:
            i = input(f'{msg} > ')
            if i == '':
                if not read.confirm('是否将上下文数量设为默认?(Y/N)'):
                    raise ReturnInterrupt('maxTokens')
                else:
                    i = '1024'
            n = int(i)
            if n >= 2000:
                if not read.confirm('当上下文数量大于两千时，很有可能请求出错，是否继续?(Y/N)'):
                    raise ReturnInterrupt('maxTokens')
            return n
        except ValueError:
            pass
        print('输入错误，请输入一个整数\n')


def set_max_tokens():
    terminal.clear_screen()
    terminal.change_title('配置上下文数量')
    with open('./resource/config.json', 'r', encoding='utf-8') as file:
        config = json.load(file)
        max_tokens = config['maxTokens']
    print(f'当前上下文数量: {max_tokens} tokens')
    max_tokens = read_int('请输入新的上下文数量')
    if max_tokens == '':
        if not read.confirm('是否将上下文数量设为默认?(Y/N)'):
            raise ReturnInterrupt('maxTokens')
        else:
            max_tokens = 1024
    config['maxTokens'] = max_tokens
    with open('./resource/config.json', 'w', encoding='utf-8') as file:
        json.dump(config, file, ensure_ascii=False, indent=2)
