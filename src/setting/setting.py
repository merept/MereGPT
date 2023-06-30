from . import model
import os


def select():
    while True:
        try:
            s = input('请输入选项 > ')
            if s == '':
                raise KeyError('setting')
            s = int(s)
            if 1 >= s >= 1:
                return s
        except ValueError:
            pass
        print('输入错误，请重新输入\n')


def execute(s):
    if s == 1:
        model.select_model()
    return s


def main():
    while True:
        try:
            os.system('cls')
            os.system('title 设置')
            print('1.设置 GPT 模型')
            s = select()
            execute(s)
        except KeyError as e:
            if e.args[0] == 'setting':
                raise
            else:
                pass
        finally:
            os.system('cls')
