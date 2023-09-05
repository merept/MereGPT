import json
import os

from service.menu import menu
from setting.apiKey import set_key
from exceptions.exceptions import ReturnInterrupt, ConfigError, Update
from utils import terminal


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
    except Exception as ex:
        print(f'出错: {ex}\n按任意键继续...')
        input()
        main(lt_tokens)


def old_key():
    with open('./resource/config.json', 'r', encoding='utf-8') as file:
        config = json.load(file)
    if config['apiKey'][:2] == 'sk':
        config['apiKey'] = ''
    with open('./resource/config.json', 'w', encoding='utf-8') as file:
        json.dump(config, file, indent=2)


if __name__ == '__main__':
    print('正在启动 MereGPT...')
    # tokens.count('1')
    if not os.path.exists(r'.\resource\chats'):
        os.mkdir(r'.\resource\chats')
    old_key()
    last_time_tokens = ''
    while True:
        try:
            main(last_time_tokens)
        except ReturnInterrupt as e:
            message = e.args[0]
            if 'chat' in message:
                m = message[4:]
                last_time_tokens = m if m != '0' else last_time_tokens
        except ConfigError:
            set_key(True)
