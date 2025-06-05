from config import config
import base64


def decode_base62(s):
    num = 0
    for char in s:
        num = num * config.BASE + config.BASE62_ALPHABET.index(char)
    return num
