"""Logging utilities for TidyForge."""

import logging

from tidyforge.constants import DEFAULT_LOG_FORMAT, LOGGER_NAME


def get_logger() -> logging.Logger:
    """Get the standard TidyForge logger.

    Returns:
        The TidyForge logger instance.
    """
    logger = logging.getLogger(LOGGER_NAME)

    # Initialize handler if not already present to prevent duplicate logs
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(DEFAULT_LOG_FORMAT)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.WARNING)

    return logger


def configure_logging(verbosity: int, ignore_warnings: bool = False) -> None:
    """Configure the TidyForge logger based on config settings.

    Args:
        verbosity: Logging level (0 = silent, 1 = warnings, 2 = detailed/info).
        ignore_warnings: If True, suppress warning logs (level set to ERROR).
    """
    logger = get_logger()

    if verbosity == 0:
        logger.setLevel(logging.CRITICAL)
    elif ignore_warnings:
        logger.setLevel(logging.ERROR)
    elif verbosity == 1:
        logger.setLevel(logging.WARNING)
    elif verbosity == 2:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARNING)
