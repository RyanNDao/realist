class DataParsingError(Exception):
    pass

class CursorError(Exception):
    def __init__(self, message, cause=None, type=None):
        super().__init__(message)
        self.cause = cause
        self.type = type