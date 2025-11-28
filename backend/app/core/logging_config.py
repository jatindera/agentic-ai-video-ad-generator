# app/core/logging_config.py (fragment)

import logging
import logging.config

def setup_logging():
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "standard",
            },
            "adk_file": {
                "class": "logging.FileHandler",
                "formatter": "standard",
                "filename": "logs/adk.log",
                "encoding": "utf-8",
            },
        },
        "loggers": {
            "backend": {  # your app logger
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            },
            "google_adk": {  # 👈 ADK namespace
                "handlers": ["console", "adk_file"],
                "level": "INFO",    # use DEBUG for very detailed traces
                "propagate": False,
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "WARNING",
        },
    }

    logging.config.dictConfig(logging_config)
