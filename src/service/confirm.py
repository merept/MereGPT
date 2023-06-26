def confirm(msg):
    s = input(msg).lower()
    while s != 'y':
        if s in ('n', ''):
            return False
        print('输入错误，请重新输入\n')
        s = input(msg).lower()
    return True
