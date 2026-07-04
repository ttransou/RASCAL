"""Utility helpers (logging, common helpers)."""
import logging
from typing import Optional

def get_logger(name: Optional[str] = None) -> logging.Logger:
    name = name or __name__
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
