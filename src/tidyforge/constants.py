"""Shared constants for TidyForge library."""

from typing import Final

# Common string representations of missing values
NA_MARKERS: Final[tuple[str, ...]] = (
    "",
    "na",
    "n/a",
    "nan",
    "null",
    "none",
    "?",
    "-",
    "null",
    "nil",
)

# Logging constants
DEFAULT_LOG_FORMAT: Final[str] = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOGGER_NAME: Final[str] = "tidyforge"
