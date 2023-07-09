import os

from service.menu import menu
from setting.apiKey import api_key


def main():
    try:
        os.system('cls')
        selection = -1
        while selection != 0:
            selection = menu()
        exit(0)
    except KeyError:
        raise
    except ValueError:
        raise
    except Exception as e:
        print(f'出错: {e}\n按任意键继续...')
        input()
        main()


if __name__ == '__main__':
    while True:
        try:
            main()
        except KeyError:
            pass
        except ValueError:
            api_key(True)
