import os

from service.menu import menu


def main():
    try:
        os.system('cls')
        selection = -1
        while selection != 0:
            selection = menu()
        exit(0)
    except KeyError:
        main()


if __name__ == '__main__':
    main()
