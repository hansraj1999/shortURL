from config import config
import logging

logger = logging.getLogger(__name__)


def encode_url(num):
    if num == 0:
        return config.BASE62_ALPHABET[0]
    encoded = []
    while num > 0:
        num, rem = divmod(num, config.BASE)
        encoded.append(config.BASE62_ALPHABET[rem])
    logger.info(f"encoded: {encoded}")
    return "".join(reversed(encoded))
