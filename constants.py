from utils.custom_logger_handler import LogFormatter


LOCK_KEY = "counter_lock"
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "custom_formatter": {
            "()": LogFormatter,
        }
    },
    "handlers": {
        "stream_handler": {
            "class": "logging.StreamHandler",
            "formatter": "custom_formatter",
            "level": "DEBUG",
        }},
    "loggers": {
        "": {
            "handlers": ["stream_handler"],
            "level": "INFO",
            "propagate": True
        }
    }
}
