from rest_framework.exceptions import APIException


class InsufficientFunds(Exception):
    pass


class TickerMissmatch(Exception):
    pass


class APIInsufficientFunds(APIException):
    status_code = 422
    default_detail = "Insufficient founds available in the balance."
    default_code = "insufficient_founds"


class APITickerMissmatch(APIException):
    status_code = 400
    default_detail = "Origin and Destination balances do not have the same ticker."
    default_code = "ticker_missmatch"


class APIUnknownBalance(APIException):
    status_code = 403
    default_detail = "Unknown balance."
    default_code = "unknown_balance"
