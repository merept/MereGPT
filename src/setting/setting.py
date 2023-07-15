import json

from . import model, apiKey, proxyUrl, devEdition
from update import checkUpdate
import os


def select():
    while True:
        try:
            s = input('请输入选项 > ')
            if s == '':
                raise KeyboardInterrupt('setting')
            s = int(s)
            if 5 >= s >= 1:
                return s
        except ValueError:
            pass
        print('输入错误，请重新输入\n')


def execute(s):
    if s == 1:
        model.select_model()
    elif s == 2:
        apiKey.set_key()
    elif s == 3:
        proxyUrl.set_url()
    elif s == 4:
        devEdition.change()
    elif s == 5:
        checkUpdate.main()
    return s


def main():
    with open('./resource/info.json', 'r') as file:
        app = json.load(file)
    while True:
        try:
            os.system('cls')
            os.system('title 设置')
            print(f'{"-" * 50}\n'
                  '\n'
                  f'应用程序版本: v{app["version"]}\n'
                  f'作者: {app["author"]}\n'
                  f'许可证: {app["license"]}\n'
                  f'\n'
                  f'{"-" * 50}\n'
                  '1.设置 GPT 模型\n'
                  '2.设置 API Key\n'
                  '3.设置代理地址\n'
                  '4.获取测试版更新\n'
                  '5.检查更新(检查文件完整性)')
            s = select()
            execute(s)
        except KeyboardInterrupt as e:
            if e.args[0] == 'setting':
                raise
            else:
                pass
        finally:
            os.system('cls')
