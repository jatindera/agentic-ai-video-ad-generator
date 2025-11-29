import logging
import logging.handlers
import os
from typing import Optional
from app.core.config import settings

environment = settings.app_env   # "development" or "production"


def configure_logging(
    log_dir: str = "logs",
    log_level: int = logging.INFO,
    log_filename: str = "app.log",
) -> logging.Logger:
    """
    Production-ready logging:
    - Local/dev: console + rotating file logs
    - Azure/prod: console only (Azure ingests stdout automatically)
    """

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Remove default handlers to avoid duplicates
    root_logger.handlers.clear()

    # -----------------------------
    # 1) ALWAYS add console handler
    # -----------------------------
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s:%(lineno)d | %(message)s"
    ))
    root_logger.addHandler(console_handler)

    # -------------------------------------------------
    # 2) Only write to file in LOCAL DEVELOPMENT
    # -------------------------------------------------
    if environment == "development":
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, log_filename)

        file_handler = logging.handlers.RotatingFileHandler(
            log_path,
            maxBytes=10_000_000,  # 10 MB
            backupCount=5,
        )
        file_handler.setFormatter(logging.Formatter(
            "%(asctime)s %(levelname)s %(name)s:%(lineno)d | %(message)s"
        ))

        root_logger.addHandler(file_handler)

    return root_logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Return a named logger."""
    return logging.getLogger(name)
