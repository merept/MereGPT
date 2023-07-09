import json
import os


def select():
    while True:
        try:
            s = input('请输入选项 > ')
            if s == '':
                raise KeyboardInterrupt('model')
            s = int(s)
            if 2 >= s >= 1:
                return s
        except ValueError:
            pass
        print('输入错误，请重新输入\n')


def select_model():
    os.system('cls')
    os.system('title 配置 GPT 模型')
    models = ['gpt-3.5-turbo-0613', 'gpt-3.5-turbo-16k-0613']
    with open(r'.\resource\config.json', 'r', encoding='utf-8') as file:
        config = json.load(file)
        model_now = config['model']
    print(f'当前 GPT 模型: {model_now[:-5]}')
    print('1.gpt-3.5-turbo\n'
          '2.gpt-3.5-turbo-16k')
    s = select()
    model_new = models[s - 1]
    config['model'] = model_new
    with open(r'.\resource\config.json', 'w', encoding='utf-8') as file:
        json.dump(config, file, ensure_ascii=False, indent=2)
