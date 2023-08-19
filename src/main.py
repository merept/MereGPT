import os

from service.menu import menu
from setting.apiKey import set_key
from exceptions.exceptions import ReturnInterrupt, ConfigError, Update
from utils import terminal, tokens


def main(lt_tokens):
    try:
        terminal.clear_screen()
        selection = -1
        while selection != 0:
            selection = menu(lt_tokens)
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
        main(lt_tokens)


if __name__ == '__main__':
    print('正在启动 MereGPT...')
    tokens.count('1')
    if not os.path.exists(r'.\resource\chats'):
        os.mkdir(r'.\resource\chats')
    last_time_tokens = ''
    while True:
        try:
            main(last_time_tokens)
        except ReturnInterrupt as e:
            message = e.args[0]
            if 'chat' in message:
                m = message[4:]
                last_time_tokens = m if m != '0' else ''
        except ConfigError:
            set_key(True)
