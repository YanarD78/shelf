import logging
import logging.config

def setup_logging(level: str = "INFO", http_level: str = "WARNING") -> None:
    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s %(levelname)-8s %(name)s: %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
        },
        "root": {"level": level, "handlers": ["console"]},
        "loggers": {
            "httpx": {"level": http_level},
            "httpcore": {"level": http_level},
        },
    })