import hashlib
import json
import os
from threading import Thread
from time import sleep

import requests

from service.confirm import confirm

base_url = 'https://raw.githubusercontent.com/merept/MereGPT/master'
gitee_url = 'https://gitee.com/merept/MereGPT/raw/master'

loads = ['', '.', '..', '...']
is_checking = True


def check_dev_edition():
    global base_url
    global gitee_url
    with open('./resource/config.json', 'r') as file:
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
        os.system('cls')
        print(f'正在检查更新{loads[i]}')
        i += 1
        if i > 3:
            i = 0
        sleep(0.5)


def check_update_module(update_module_path):
    global base_url
    global gitee_url
    # print(f'正在检查文件 {update_module_path}')
    lh = local_hash(f'./{update_module_path}')
    try:
        oh = online_hash(f'{base_url}/{update_module_path}')
    except requests.exceptions.SSLError:
        base_url = gitee_url
        oh = online_hash(f'{base_url}/{update_module_path}')
    if lh != oh:
        # print(f'正在更新文件 {update_module_path}')
        l_file = f'./{update_module_path}'
        # print(f'正在移除文件 {update_module_path}')
        os.remove(l_file)
        # print(f'正在下载文件 {update_module_path}')
        o_file = requests.get(f'{base_url}/{update_module_path}')
        with open(l_file, 'wb') as file:
            file.write(o_file.content)


def check_json_file(json_file):
    # print(f'正在检查文件 {json_file}')
    lh = local_hash(f'./{json_file}')
    oh = online_hash(f'{base_url}/{json_file}')
    if lh != oh:
        return True
    return False


def check_config_file(config_file):
    # print(f'正在检查文件 {config_file}')
    with open(f'./{config_file}', 'r') as file:
        local_config = json.load(file)
    response = requests.get(f'{base_url}/{config_file}')
    online_config = response.json()
    for key in online_config.keys():
        if key not in local_config:
            return True


def confirm_update(updates):
    if confirm('检测到更新，是否更新?(Y/N)'):
        with open('./src/update/updates.json', 'w') as file:
            json.dump(updates, file, ensure_ascii=False)
        raise Update('update')
    else:
        raise KeyboardInterrupt('update')


def main():
    global is_checking
    os.system('cls')
    os.system('title 检查更新')

    check_dev_edition()

    thread = Thread(target=checking, daemon=True)
    thread.start()

    updates = []
    # print('正在检查更新...')
    json_file = 'src/update/files.json'

    check_update_module('src/update/update.py')

    if check_json_file(json_file):
        updates.append(json_file)

    if check_config_file('resource/config.json'):
        updates.append('resource/config.json')

    with open(f'./{json_file}', 'r') as file:
        file_list = json.load(file)

    for file in file_list:
        # print(f'正在检查文件 {file}')
        lh = local_hash(f'./{file}')
        oh = online_hash(f'{base_url}/{file}')
        if lh != oh:
            updates.append(file)

    is_checking = False

    os.system('cls')
    if updates:
        confirm_update(updates)
    else:
        print('暂无更新')
        input()
        raise KeyboardInterrupt('update')


class Update(Exception):
    def __init__(self, message):
        self.message = message
