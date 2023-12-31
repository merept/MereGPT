import json
import os
import sys

import requests

base_url = 'https://raw.githubusercontent.com/merept/MereGPT/master'
gitee_url = 'https://gitee.com/merept/MereGPT/raw/master'


def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def change_title(title):
    sys.stdout.write(f'\33]0;{title}\a')
    sys.stdout.flush()


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


def update(path, is_existed):
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


def update_config_file(config_file):
    print(f'正在更新文件 {config_file}')
    with open(f'./{config_file}', 'r') as file:
        local_config = json.load(file)
    response = requests.get(f'{base_url}/{config_file}')
    online_config = response.json()
    for key in online_config.keys():
        if key not in local_config:
            local_config[key] = online_config[key]
    with open(f'./{config_file}', 'w') as file:
        json.dump(local_config, file, indent=2, ensure_ascii=False)


def main():
    with open('./src/update/updates.json', 'r') as file:
        updates = json.load(file)
    config_file = 'resource/config.json'

    if config_file in updates:
        update_config_file(config_file)

    for file in updates:
        if file == config_file:
            continue
        print(f'正在更新文件 {file}')
        update(file, os.path.exists(f'./{file}'))

    os.remove('./src/update/updates.json')


if __name__ == '__main__':
    check_dev_edition()
    clear_screen()
    change_title('MereGPT 更新中')
    try:
        requests.get(base_url)
    except Exception as e:
        if 'HTTPSConnectionPool' in str(e.args[0]):
            base_url = gitee_url
        else:
            print(f'更新失败\n出错: {e.args[0]}')
            exit(0)
    main()
