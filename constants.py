from utils.custom_logger_handler import LogFormatter

DATABASE_NAME = "short_url"
LOCK_KEY = "counter_lock"
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "custom_formatter": {
            "()": LogFormatter,
            "format": (
                '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - '
                'trace_id=%(trace_id)s span_id=%(span_id)s trace_flags=%(trace_flags)s - '
                'service_name=%(service_name)s host=%(host)s - %(message)s'
            ),
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
