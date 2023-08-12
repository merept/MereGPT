import hashlib
import json
import os
from threading import Thread
from time import sleep

import requests

from exceptions.exceptions import ReturnInterrupt, Update
from utils import *

base_url = 'https://raw.githubusercontent.com/merept/MereGPT/master'
gitee_url = 'https://gitee.com/merept/MereGPT/raw/master'

is_dev_edition = False

loads = ['', '.', '..', '...']
is_checking = False


def check_dev_edition():
    global base_url
    global gitee_url
    global is_dev_edition
    config_file = './resource/config.json'
    if not os.path.exists(config_file):
        update(config_file)
    with open(config_file, 'r') as file:
        config = json.load(file)
        try:
            is_dev_edition = config['dev']
        except KeyError:
            config['dev'] = False
            is_dev_edition = config['dev']
    if is_dev_edition:
        base_url_list = base_url.split('/')
        base_url_list[-1] = 'dev'
        base_url = str.join('/', base_url_list)
        gitee_url_list = gitee_url.split('/')
        gitee_url_list[-1] = 'dev'
        gitee_url = str.join('/', gitee_url_list)


def online_hash(url):
    response = requests.get(url)
    sha = hashlib.sha256(response.content)
    response.close()
    return sha.hexdigest()


def local_hash(path):
    if not os.path.exists(path):
        return ''
    sha = hashlib.sha256()
    with open(path, 'rb') as f:
        content = f.read().decode()
        normalized_content = content.replace("\r\n", "\n").encode()
        sha.update(normalized_content)
    return sha.hexdigest()


def checking():
    i = 0
    while is_checking:
        terminal.clear_screen()
        print(f'正在检查更新{loads[i]}')
        i += 1
        if i > 3:
            i = 0
        sleep(0.5)


def update(path):
    l_file = f'./{path}'
    if os.path.exists(path):
        os.remove(l_file)
    base_path = str.join('/', l_file.split('/')[:-1])
    if not os.path.exists(base_path):
        os.mkdir(base_path)
    o_file = requests.get(f'{base_url}/{path}')
    with open(l_file, 'wb') as file:
        file.write(o_file.content)


def check_update_module(update_module_path):
    global base_url
    global gitee_url
    lh = local_hash(f'./{update_module_path}')
    try:
        oh = online_hash(f'{base_url}/{update_module_path}')
    except Exception as e:
        if 'HTTPSConnectionPool' in str(e.args[0]):
            base_url = gitee_url
            oh = online_hash(f'{base_url}/{update_module_path}')
        else:
            raise
    if lh != oh:
        update(update_module_path)


def check_json_file(json_file):
    lh = local_hash(f'./{json_file}')
    oh = online_hash(f'{base_url}/{json_file}')
    if lh != oh:
        update(json_file)


def check_info_file(info_file):
    lh = local_hash(f'./{info_file}')
    oh = online_hash(f'{base_url}/{info_file}')
    if lh == oh:
        return False, {}, False
    response = requests.get(f'{base_url}/{info_file}')
    online_info = response.json()
    if not lh:
        update(info_file)
        return True, online_info, True
    with open(f'./{info_file}', 'r', encoding='utf-8') as file:
        local_info = json.load(file)
    if int(online_info['version'].split('.')[1]) > int(local_info['version'].split('.')[1]):
        return True, online_info, True
    if online_info['version'] != local_info['version'] or (is_dev_edition and online_info['dev'] != local_info['dev']):
        return True, online_info, False
    return False, {}, False


def check_config_file(config_file):
    with open(f'./{config_file}', 'r') as file:
        local_config = json.load(file)
    response = requests.get(f'{base_url}/{config_file}')
    online_config = response.json()
    for key in online_config.keys():
        if key not in local_config:
            return True


def confirm_update(msg, updates, info_file, online_info):
    if read.confirm(msg):
        with open('./src/update/updates.json', 'w', encoding='utf-8') as file:
            json.dump(updates, file, ensure_ascii=False)
        with open(f'./{info_file}', 'w', encoding='utf-8') as file:
            json.dump(online_info, file, indent=2, ensure_ascii=False)
        raise Update('update')
    else:
        raise ReturnInterrupt('update')


def big_version_update(info):
    base_file = ['resource/info.json', 'src/update/update.py', 'src/update/files.json']
    for bf in base_file[1:]:
        update(bf)
    with open('src/update/files.json', 'r', encoding='utf-8') as file:
        updates = json.load(file)
    updates.append('resource/config.json')
    msg = f'检测到更新:\n' \
          f'v{info["version"]} ({info["dev"]})\n' \
          f'更新内容:\n' \
          f'{info["content"]}\n' \
          f'是否更新?(Y/N)'
    confirm_update(msg, updates, base_file[0], info)


def main():
    global is_checking
    terminal.clear_screen()
    terminal.change_title('检查更新')

    check_dev_edition()

    is_checking = True
    thread = Thread(target=checking, daemon=True)
    thread.start()

    try:
        updates = []
        json_file = 'src/update/files.json'

        check_update_module('src/update/update.py')

        check_json_file(json_file)

        info_file = 'resource/info.json'
        is_old_version, info, is_big_version = check_info_file(info_file)

        if check_config_file('resource/config.json'):
            updates.append('resource/config.json')

        with open(f'./{json_file}', 'r') as file:
            file_list = json.load(file)

        for file in file_list:
            lh = local_hash(f'./{file}')
            oh = online_hash(f'{base_url}/{file}')
            if lh != oh:
                updates.append(file)
    except KeyboardInterrupt:
        is_checking = False
        raise ReturnInterrupt('checkUpdate')
    except Exception:
        is_checking = False
        raise

    is_checking = False

    terminal.clear_screen()
    if is_big_version:
        big_version_update(info)
    elif is_old_version and updates:
        msg = f'检测到更新:\n' \
              f'v{info["version"]} ({info["dev"]})\n' \
              f'更新内容:\n' \
              f'{info["content"]}\n' \
              f'是否更新?(Y/N)'
        confirm_update(msg, updates, info_file, info)
    elif not is_old_version and updates:
        msg = '检测到有文件与最新文件不一致，是否立即修复?(Y/N)'
        confirm_update(msg, updates, info_file, info)
    else:
        print('暂无更新')
        input()
        raise ReturnInterrupt('update')
#
#
# if __name__ == '__main__':
#     os.chdir('../..')
#     try:
#         main()
#     except Update:
#         exit(1)
