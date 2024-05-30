import logging
import logging.config
from logging.handlers import RotatingFileHandler


def setup_logging(filename: str):
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            },
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "standard",
            },
            "rotating_file": {
                "level": "DEBUG",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "/home/app/logs/{filename}.log",
                "formatter": "standard",
                "maxBytes": 5 * 1024 * 1024,  # 5 MB
                "backupCount": 5,  # Keep 5 backup files
                "encoding": "utf8",
            },
        },
        "loggers": {
            "": {  # root logger
                "handlers": ["console", "rotating_file"],
                "level": "DEBUG",
                "propagate": True,
            },
        },
    }

    logging.config.dictConfig(logging_config)
