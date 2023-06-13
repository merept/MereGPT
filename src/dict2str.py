import re


def __str__(dic, tabs, intent, newl, ail):
    bs = ' '
    if ail:
        wrap, sub_tab, main_tab, tab_in_tabs = '', '', '', ''
    else:
        wrap, sub_tab, main_tab = '\n', f'{bs * intent * tabs}', f'{bs * intent * (tabs - 1)}'
        tab_in_tabs = f'{bs * intent * (tabs + 1)}'

    newline = f'{wrap}{main_tab}' if newl else ''
    res = newline + '{' + wrap

    if len(dic) == 0:
        return newline + '{}'

    last_key = list(dic)[-1]
    for key, value in dic.items():
        key_str = f'{sub_tab}{key}'
        end = '' if key == last_key else ', '
        if isinstance(value, dict):
            ds = __str__(value, tabs + 1, intent, newl, ail)
            res += f'{key_str}: {ds}{end}{wrap}'
        else:
            if isinstance(value, str):
                value = string_value(value, wrap, tab_in_tabs)
            res += f'{key_str}: {value}{end}{wrap}'

    return res + main_tab + '}'


def string_value(value, wrap, tab):
    value = '\"' + value
    if wrap:
        wrap = r'\n'
    pattern = re.compile(r'[\r\n]+')
    value = re.sub(pattern, wrap + tab, value)
    return value + '\"'


def to_string(dic: dict, intent=2, newl=False, ail=False):
    return __str__(dic, 1, intent, newl, ail)


if __name__ == '__main__':
    d = {
        "a": 1,
        "b": {
            "b_a": 2.1,
            "b_b": 2.2
        },
        "c": 3,
        "d": {
            "d_a": {
                "d_a_a": 4.1,
                "d_a_b": 4.2
            },
            "d_b": 4.2,
            "d_c": {
                "d_c_a": 4.1
            },
            "d_d": 4.4
        },
        "e": 5,
        "f": {}
    }

    try:
        print(f'd: {to_string(d, intent=4)}')
    except RecursionError:
        print('嵌套层数过多')
