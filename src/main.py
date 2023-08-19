import os

from service.menu import menu
from setting.apiKey import set_key
from exceptions.exceptions import ReturnInterrupt, ConfigError, Update
from utils import terminal, tokens


def main():
    try:
        terminal.clear_screen()
        selection = -1
        while selection != 0:
            selection = menu()
        exit(0)
    except ReturnInterrupt:
        raise
    except ConfigError:
        raise
    except Update:
        exit(1)
    except Exception as e:
        print(f'出错: {e}\n按任意键继续...')
        input()
        main()


if __name__ == '__main__':
    print('正在启动 MereGPT...')
    tokens.count('1')
    if not os.path.exists(r'.\resource\chats'):
        os.mkdir(r'.\resource\chats')
    while True:
        try:
            main()
        except ReturnInterrupt:
            pass
        except ConfigError:
            set_key(True)
