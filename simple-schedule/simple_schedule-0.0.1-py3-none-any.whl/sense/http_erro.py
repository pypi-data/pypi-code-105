
from simple_schedule import error_message

@error_message("40x")
def my_40x_page(message: str, explain=""):
    return {"code": 400, "desc": "not found task"}


@error_message("50x")
def my_40x_page(message: str, explain=""):
    return {"code": 400, "desc": "not found task"}

@error_message
def my_error_message(code, message, explain=""):
    return f"{code}-{message}-{explain}"