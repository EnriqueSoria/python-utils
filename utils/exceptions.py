class MissingKeys(Exception):
    default_message = "Missing required keys: {keys}"

    def __init__(self, keys, *args):
        self.keys = keys
        message = self.default_message.format(keys=self.keys)
        super().__init__(message, *args)