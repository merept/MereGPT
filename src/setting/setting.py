import json

from exceptions.exceptions import ReturnInterrupt
from . import model, apiKey, proxyUrl, devEdition
from update import checkUpdate
import os


def check_dev_edition():
    with open('./resource/config.json', 'r') as file:
        config = json.load(file)
        try:
            is_dev_edition = config['dev']
        except KeyError:
            config['dev'] = False
            is_dev_edition = config['dev']
    return is_dev_edition


def check_version_content(app):
    os.system('cls')
    content = f'v{app["version"]} ({app["dev"]})\n' \
              f'更新内容:\n' \
              f'{app["content"]}'
    print(content, end='')
    input()
    raise ReturnInterrupt('versionContent')


def select():
    while True:
        try:
            s = input('请输入选项 > ')
            if s == '':
                raise ReturnInterrupt('setting')
            s = int(s)
            if 6 >= s >= 1:
                return s
        except ValueError:
            pass
        print('输入错误，请重新输入\n')


def execute(s, app):
    if s == 1:
        model.select_model()
    elif s == 2:
        apiKey.set_key()
    elif s == 3:
        proxyUrl.set_url()
    elif s == 4:
        devEdition.change()
    elif s == 5:
        check_version_content(app)
    elif s == 6:
        checkUpdate.main()
    return s


def main():
    if not os.path.exists('./resource/info.json') or not os.path.exists('./resource/config.json'):
        checkUpdate.main()
        raise ReturnInterrupt()
    with open('./resource/info.json', 'r', encoding='utf-8') as file:
        app = json.load(file)
    while True:
        is_dev_edition = check_dev_edition()
        dev_info = f'测试版本: {app["dev"]}\n' if is_dev_edition else ''
        try:
            os.system('cls')
            os.system('title 设置')
            print(f'{"-" * 50}\n'
                  '\n'
                  f'应用程序版本: v{app["version"]}\n'
                  f'{dev_info}'
                  f'作者: {app["author"][0]}\n'
                  f'许可证: {app["license"]}\n'
                  f'\n'
                  f'{"-" * 50}\n'
                  '1.设置 GPT 模型\n'
                  '2.设置 API Key\n'
                  '3.设置代理地址\n'
                  '4.获取测试版更新\n'
                  '5.查看版本更新内容\n'
                  '6.检查更新(检查文件完整性)')
            s = select()
            execute(s, app)
        except ReturnInterrupt as e:
            if e.args[0] == 'setting':
                raise
            else:
                pass
        finally:
            os.system('cls')
