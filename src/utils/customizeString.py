class CustomizeOption:
    __reset = "\033[0m"
    __bold = "\033[1m"
    __underline = "\033[4m"
    __black = "\033[30m"
    __red = "\033[31m"
    __green = "\033[32m"
    __yellow = "\033[33m"
    __blue = "\033[34m"
    __purple = "\033[35m"
    __cyan = "\033[36m"
    __white = "\033[37m"
    __grey = "\033[90m"
    __bright_red = "\033[91m"
    __bright_green = "\033[92m"
    __bright_yellow = "\033[93m"
    __bright_blue = "\033[94m"
    __bright_purple = "\033[95m"
    __bright_cyan = "\033[96m"
    __bright_white = "\033[97m"

    @property
    def RESET(self):
        return CustomizeOption.__reset

    @property
    def BOLD(self):
        return self.__bold

    @property
    def UNDERLINE(self):
        return self.__underline

    @property
    def BLACK(self):
        return self.__black

    @property
    def RED(self):
        return self.__red

    @property
    def GREEN(self):
        return self.__green

    @property
    def YELLOW(self):
        return self.__yellow

    @property
    def BLUE(self):
        return self.__blue

    @property
    def PURPLE(self):
        return self.__purple

    @property
    def CYAN(self):
        return self.__cyan

    @property
    def WHITE(self):
        return self.__white

    @property
    def GREY(self):
        return self.__grey

    @property
    def BRIGHT_RED(self):
        return self.__bright_red

    @property
    def BRIGHT_GREEN(self):
        return self.__bright_green

    @property
    def BRIGHT_YELLOW(self):
        return self.__bright_yellow

    @property
    def BRIGHT_BLUE(self):
        return self.__bright_blue

    @property
    def BRIGHT_PURPLE(self):
        return self.__bright_purple

    @property
    def BRIGHT_CYAN(self):
        return self.__bright_cyan

    @property
    def BRIGHT_WHITE(self):
        return self.__bright_white


def customize_string(content: str, option):
    Option = CustomizeOption()
    if option != CustomizeOption.RESET:
        return option + content + Option.RESET
    return option + content
