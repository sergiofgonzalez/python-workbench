"""Custom exceptions raised from the business layer"""


class OrderNotFoundError(Exception):
    pass


class APIIntegrationError(Exception):
    pass


class InvalidActionError(Exception):
    pass
