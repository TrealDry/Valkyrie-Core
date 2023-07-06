import base64
import itertools


def base64_encode(string):
    return base64.urlsafe_b64encode(string.encode()).decode()


def base64_decode(string):
    return base64.urlsafe_b64decode(string.encode()).decode()


def xor(string, key):
    result = ""
    for string_char, key_char in zip(string, itertools.cycle(key)):
        result += chr(ord(string_char) ^ ord(key_char))
    return result
