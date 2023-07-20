class ReturnInterrupt(Exception):
    def __init__(self, message):
        self.message = message


class ConfigError(Exception):
    def __init__(self, message):
        self.message = message


class Update(Exception):
    def __init__(self, message):
        self.message = message
