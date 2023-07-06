import re
from flask import request


forbidden_symbols = r"[~:|#]"


def main(arg, arg_type="str"):
    received_data = request.values.get(arg)

    if received_data is None:
        if arg_type == "str":
            return ""
        elif arg_type == "int":
            return 0
        else:
            return ""

    if arg_type == "str":
        return re.sub(forbidden_symbols, "", received_data)
    elif arg_type == "int":
        try:
            return int(received_data)
        except ValueError:
            return 0
    else:
        return ""


def ip():
    return request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr).split(",")[0]
