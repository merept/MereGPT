import json
import os

import requests

from utils import read, terminal
from exceptions.exceptions import ReturnInterrupt

api_key = ''


def recharge():
    terminal.clear_screen()
    terminal.change_title('卡密充值')
    card = input('请输入你的卡密 > ')
    if card == '':
        raise ReturnInterrupt('recharge')
    terminal.clear_screen()
    print('充值中...')
    response = requests.get(f'https://api.openai-sb.com/sb-api/user/card/use?api_key={api_key}&card={card}')
    terminal.clear_screen()
    response = json.loads(response.text)
    if response['code'] == '0':
        print(response["msg"])
        if read.confirm('是否查询 API Key 余额?(Y/N)'):
            check_balance()
        else:
            raise ReturnInterrupt('recharge')
    else:
        print(f'{response["msg"]}\n回车键返回上一级...', end='')
        input()
        raise ReturnInterrupt('recharge')


def check_status():
    terminal.clear_screen()
    terminal.change_title('卡密状态查询')
    card = input('请输入你的卡密 > ')
    if card == '':
        raise ReturnInterrupt('recharge')
    terminal.clear_screen()
    print('查询中...')
    response = requests.get(f'https://api.openai-sb.com/sb-api/user/card/status?api_key={api_key}&card={card}')
    terminal.clear_screen()
    response = json.loads(response.text)
    if response['code'] == '0':
        data = response['data']
        status = '已使用' if data['status'] else '未使用'
        print(f'卡密: {data["key"]}\n'
              f'金额: {data["value"]} 元\n'
              f'状态: {status}\n'
              f'回车键返回上一级...', end='')
        input()
        raise ReturnInterrupt('status')
    else:
        print(f'{response["msg"]}\n回车键返回上一级...', end='')
        input()
        raise ReturnInterrupt('status')


def check_balance():
    terminal.clear_screen()
    terminal.change_title('卡密状态查询')
    print('查询中...')
    response = requests.get(f'https://api.openai-sb.com/sb-api/user/status?api_key={api_key}')
    terminal.clear_screen()
    response = json.loads(response.text)
    if response['code'] == '0':
        data = response['data']
        print(f'剩余积分: {float(data["credit"]): .2f}\n'
              f'使用次数: {data["use_counts"]}\n'
              f'使用的 tokens: {data["use_tokens"]}\n'
              f'回车键返回上一级...', end='')
        input()
        raise ReturnInterrupt('balance')
    else:
        print(f'{response["msg"]}\n回车键返回上一级...', end='')
        input()
        raise ReturnInterrupt('balance')


def main():
    while True:
        global api_key
        terminal.clear_screen()
        terminal.change_title('卡密设置')
        with open('./resource/config.json', 'r', encoding='utf-8') as file:
            api_key = json.load(file)['apiKey']
        print('卡密获取教程: https://openai-sb.com/guide/pricing.html\n\n'
              '1.使用卡密充值\n'
              '2.卡密状态查询\n'
              '3.查询 API Key 余额')
        try:
            s = read.select(3, name='card')
            if s == 1:
                recharge()
            elif s == 2:
                check_status()
            elif s == 3:
                check_balance()
        except ReturnInterrupt as e:
            if e.args[0] == 'card':
                raise
            else:
                pass


if __name__ == '__main__':
    os.chdir('../..')
    main()
