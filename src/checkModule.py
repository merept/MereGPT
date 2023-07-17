import importlib
import json
import os

from update import checkUpdate

modules = {
  "requests": {
    "package": "requests",
    "version": "2.30.0"
  },
  "sseclient": {
    "package": "sseclient-py",
    "version": "1.7.2"
  }
}

requestsModule = None
files = []
base_url = 'https://raw.githubusercontent.com/merept/MereGPT/master'
gitee_url = 'https://gitee.com/merept/MereGPT/raw/master'


def check_third_party_module(name, info):
    package = info['package']
    version = info['version']
    try:
        importlib.import_module(name)
    except ImportError:
        print(f'\033[34minstall \033[32m{package}\033[0m')
        os.system(f'pip install {package}=={version}')
        print()


def fix(path):
    l_file = f'./{path}'
    base_path = str.join('/', l_file.split('/')[:-1])
    if not os.path.exists(base_path):
        os.mkdir(base_path)
    o_file = requestsModule.get(f'{base_url}/{path}')
    with open(l_file, 'wb') as fs:
        fs.write(o_file.content)


def check_base_file():
    base_files = ['src/update/update.py', 'src/update/files.json']
    for bf in base_files:
        if not os.path.exists(f'./{bf}'):
            print(f'正在修复文件 {bf}')
            fix(bf)


def check_local_module(path):
    if not os.path.exists(f'./{path}'):
        print(f'正在修复文件 {path}')
        fix(path)


if __name__ == '__main__':
    # os.chdir(r'..\..')
    # if not os.path.exists(r'.\resource\modules.json'):
    #     checkUpdate.main()
    # with open(r'.\resource\modules.json', 'r', encoding='utf-8') as file:
    #     modules_dict = json.load(file)
    for key, value in modules.items():
        check_third_party_module(key, value)
    requestsModule = importlib.import_module('requests')

    check_base_file()

    with open('./src/update/files.json', 'r', encoding='utf-8') as file:
        files_list = json.load(file)
    for f in files_list:
        check_local_module(f)
