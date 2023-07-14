from . import model, apiKey, proxyUrl
from update import checkUpdate
import os


def select():
    while True:
        try:
            s = input('请输入选项 > ')
            if s == '':
                raise KeyboardInterrupt('setting')
            s = int(s)
            if 4 >= s >= 1:
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
        checkUpdate.main()
    return s


def main():
    while True:
        try:
            os.system('cls')
            os.system('title 设置')
            print('1.设置 GPT 模型\n'
                  '2.设置 API Key\n'
                  '3.设置代理地址\n'
                  '4.检查更新')
            s = select()
            execute(s)
        except KeyboardInterrupt as e:
            if e.args[0] == 'setting':
                raise
            else:
                pass
        finally:
            os.system('cls')
