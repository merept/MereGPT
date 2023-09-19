import json
import os

import requests

from utils import read, terminal
from exceptions.exceptions import ReturnInterrupt

api_key = ''


def error(res_msg, err_msg):
    print(f'{res_msg}\n回车键返回上一级...', end='')
    input()
    raise ReturnInterrupt(err_msg)


def get_tokens(key):
    response = requests.get(f'https://api.openai-sb.com/sb-api/user/status?api_key={key}').json()
    if response['code'] != '0':
        error(f'\n{response["msg"]}', 'get_tokens')
    return response['data']["use_tokens"]


def activate_gpt4():
    print('检测到该 API Key 的 GPT-4 功能暂未激活, ', end='')
    if not read.confirm('是否激活 GPT-4 ?(Y/N)'):
        raise ReturnInterrupt('gpt4')
    terminal.clear_screen()
    print('激活中...')
    response = requests.get(f'https://api.openai-sb.com/sb-api/user/switch_gpt4?api_key={api_key}&enable=1').json()
    terminal.clear_screen()
    if response['code'] != '0':
        error(response['msg'], 'gpt4')


def check_key_status():
    terminal.clear_screen()
    print('检查 API Key 状态中...')
    response = requests.get(f'https://api.openai-sb.com/sb-api/user/status?api_key={api_key}').json()
    terminal.clear_screen()
    if response['code'] == "0":
        if not response['data']['enable_gpt4']:
            activate_gpt4()
    else:
        error(response['msg'], 'gpt4')


def gpt4():
    global api_key
    terminal.clear_screen()
    terminal.change_title('切换到 GPT-4')
    with open('./resource/config.json', 'r', encoding='utf-8') as file:
        config = json.load(file)
        model_now = config["model"]
        api_key = config['apiKey']
    if model_now == 'gpt-4':
        print('当前正在使用 GPT-4 模型\n如需切换回 GPT-3.5, 请直接在 "设置 GPT 模型中" 设置\n\n回车键返回上一级...')
        input()
        raise ReturnInterrupt('gpt4')
    print(f'当前 GPT 模型: {model_now}')
    print('\n'
          '\033[31m请注意！\033[0m\n'
          '\033[33m对于普通用户，建议使用 GPT-3.5 而不是 GPT-4\n'
          '因为 GPT-4 的价格比 GPT-3.5 高出 157.5 ~ 315 倍\n'
          '而且 GPT-3.5 的响应速度是 GPT-4 的四倍多\033[0m')
    if not read.confirm(f'\n是否切换到 GPT-4 ?(Y/N)'):
        raise ReturnInterrupt('gpt4')
    check_key_status()
    config['model'] = 'gpt-4'
    with open('./resource/config.json', 'w', encoding='utf-8') as file:
        json.dump(config, file, indent=2, ensure_ascii=False)


def recharge():
    terminal.clear_screen()
    terminal.change_title('使用卡密充值')
    card = input('请输入你的卡密 > ')
    if card == '':
        raise ReturnInterrupt('recharge')
    terminal.clear_screen()
    print('充值中...')
    response = requests.get(f'https://api.openai-sb.com/sb-api/user/card/use?api_key={api_key}&card={card}').json()
    terminal.clear_screen()
    if response['code'] == '0':
        print(response["msg"])
        if not read.confirm('是否查询 API Key 余额?(Y/N)'):
            raise ReturnInterrupt('recharge')
        check_balance()
    else:
        error(response['msg'], 'recharge')


def check_status():
    terminal.clear_screen()
    terminal.change_title('卡密状态查询')
    card = input('请输入你的卡密 > ')
    if card == '':
        raise ReturnInterrupt('recharge')
    terminal.clear_screen()
    print('查询中...')
    response = requests.get(f'https://api.openai-sb.com/sb-api/user/card/status?api_key={api_key}&card={card}').json()
    terminal.clear_screen()
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
        error(response['msg'], 'status')


def transfer_tokens(tokens):
    if tokens >= 1000:
        tokens = f'{tokens / 1000:,.2f}K'
    return tokens


def check_balance():
    terminal.clear_screen()
    terminal.change_title('查询 API Key 余额')
    print('查询中...')
    response = requests.get(f'https://api.openai-sb.com/sb-api/user/status?api_key={api_key}').json()
    terminal.clear_screen()
    if response['code'] == '0':
        data = response['data']
        credit = float(data["credit"])
        print(f'已使用: {transfer_tokens(data["use_tokens"])} tokens\n'
              f'剩余积分: {credit:.2f} (约 {credit/10000:.2f} 元)\n'
              f'对话次数: {data["use_counts"]}\n'
              f'回车键返回上一级...', end='')
        input()
        raise ReturnInterrupt('balance')
    else:
        error(response['msg'], 'balance')


def main():
    while True:
        global api_key
        terminal.clear_screen()
        terminal.change_title('API Key 余额与充值')
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
