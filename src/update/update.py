import hashlib
import json
import os

import requests

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


def update(path, is_existed=True):
    l_file = f'./{path}'
    if is_existed:
        print(f'正在移除文件 {path}')
        os.remove(l_file)
    base_path = str.join('/', l_file.split('/')[:-1])
    if not os.path.exists(base_path):
        os.mkdir(base_path)
    print(f'正在下载文件 {path}')
    o_file = requests.get(f'{base_url}/{path}')
    with open(l_file, 'wb') as file:
        file.write(o_file.content)


def update_json_file(json_file):
    print(f'正在检查文件 {json_file}')
    lh = local_hash(f'./{json_file}')
    oh = online_hash(f'{base_url}/{json_file}')
    if lh != oh:
        update(json_file)


def main():
    json_file = 'src/update/files.json'
    update_json_file(json_file)
    with open(f'./{json_file}') as file:
        file_list = json.load(file)
    for file in file_list:
        print(f'正在检查文件 {file}')
        if not os.path.exists(f'./{file}'):
            update(file, False)
            continue
        lh = local_hash(f'./{file}')
        oh = online_hash(f'{base_url}/{file}')
        if lh != oh:
            update(file)


if __name__ == '__main__':
    # os.chdir(r'..\..')
    os.system('cls')
    os.system('title MereGPT 更新中')
    try:
        main()
    except requests.exceptions.SSLError:
        base_url = gitee_url
        main()
