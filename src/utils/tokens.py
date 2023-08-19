import tiktoken


def count(content: str):
    encoding = tiktoken.get_encoding('cl100k_base')
    return len(encoding.encode(content))


def counts(records: list):
    encoding = tiktoken.get_encoding('cl100k_base')
    records_str = ''
    for r in records:
        records_str += r['content']
    return len(encoding.encode(records_str))


if __name__ == '__main__':
    print(count('你好，你是谁'))
    reply = '我是一个由OpenAI开发的人工智能助手，帮助用户提供问题回答和文字生成等服务。我是基于GPT-3模型训练而成，经过大规模的\n' \
            '语言数据训练，可以回答各种问题、提供信息和建议，帮助人们解决问题和获得帮助。如果您有任何问题，我会尽力给予解答。 '
    print(count(reply))
