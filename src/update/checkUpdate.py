import hashlib
import json
import os

import requests

from service.confirm import confirm

base_url = 'https://raw.githubusercontent.com/merept/MereGPT/master'
gitee_url = 'https://gitee.com/merept/MereGPT/raw/master'


def online_hash(url):
    response = requests.get(url)
    sha = hashlib.sha256(response.content)
    return sha.hexdigest()


def local_hash(path):
    sha = hashlib.sha256()
    with open(path, 'rb') as f:
        content = f.read().decode()
        normalized_content = content.replace("\r\n", "\n").encode()
        sha.update(normalized_content)
    return sha.hexdigest()


def check_json_file(json_file):
    global base_url
    global gitee_url
    lh = local_hash(f'./{json_file}')
    try:
        oh = online_hash(f'{base_url}/{json_file}')
    except requests.exceptions.SSLError:
        base_url = gitee_url
        oh = online_hash(f'{base_url}/{json_file}')
    if lh != oh:
        return True
    return False


def main():
    os.system('cls')
    os.system('title 检查更新')
    print('正在检查更新...')
    json_file = 'src/update/files.json'
    if check_json_file(json_file):
        if confirm('检测到更新，是否更新?(Y/N)'):
            raise Update('update')
        else:
            return False
    with open(f'./{json_file}', 'r') as file:
        file_list = json.load(file)
    for file in file_list:
        lh = local_hash(f'./{file}')
        oh = online_hash(f'{base_url}/{file}')
        if lh != oh:
            if confirm('检测到更新，是否更新?(Y/N)'):
                raise Update('update')
            else:
                raise KeyboardInterrupt('update')
    os.system('cls')
    print('暂无更新')
    input()
    raise KeyboardInterrupt('update')


class Update(Exception):
    def __init__(self, message):
        self.message = message
