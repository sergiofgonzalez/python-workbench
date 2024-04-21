"""Data layer errors"""


class MissingError(Exception):
    pass


class DuplicateError(Exception):
    pass


class InvalidStateError(Exception):
    pass
