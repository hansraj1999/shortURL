from config import config


def decode_url(encoded_url):
    return config.sqids.decode(encoded_url)
