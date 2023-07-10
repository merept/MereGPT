import os

from service.menu import menu
from setting.apiKey import set_key


def main():
    try:
        os.system('cls')
        selection = -1
        while selection != 0:
            selection = menu()
        exit(0)
    except KeyboardInterrupt:
        raise
    except ValueError:
        raise
    except Exception as e:
        print(f'出错: {e}\n按任意键继续...')
        input()
        main()


if __name__ == '__main__':
    if not os.path.exists(r'.\resource\chats'):
        os.mkdir(r'.\resource\chats')
    while True:
        try:
            main()
        except KeyboardInterrupt:
            pass
        except ValueError:
            set_key(True)
