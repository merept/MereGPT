from exceptions.exceptions import ReturnInterrupt


def confirm(msg: str):
    s = input(msg).lower()
    while s != 'y':
        if s in ('n', ''):
            return False
        print('输入错误，请重新输入\n')
        s = input(msg).lower()
    return True


def select(max_val: int, min_val=1, name='confirm'):
    while True:
        try:
            s = input('请输入选项 > ')
            if s == '':
                raise ReturnInterrupt(name)
            s = int(s)
            if max_val >= s >= min_val:
                return s
        except ValueError:
            pass
        print('输入错误，请重新输入\n')
