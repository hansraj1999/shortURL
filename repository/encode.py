from config import config


def encode_url(counter):
    return config.sqids.encode([counter])
