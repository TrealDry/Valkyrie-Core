import re


def char_clean(value):
    return re.sub(r"[^A-Za-z0-9 ]", "", value)


def clear_prohibited_chars(value):
    return re.sub(r"[~:|#]", "", value)
