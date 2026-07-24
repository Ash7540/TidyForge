"""Unit tests for TidyForge utility, logging, and decorator systems."""

import logging

import pandas as pd
import pytest

from tidyforge import Cleaner
from tidyforge.constants import LOGGER_NAME
from tidyforge.utils.helpers import format_bytes, get_dataframe_memory_usage
from tidyforge.utils.logging import configure_logging, get_logger


def test_format_bytes() -> None:
    """Test format_bytes correctly formats size values."""
    assert format_bytes(0) == "0 B"
    assert format_bytes(500) == "500 B"
    assert format_bytes(1024) == "1.00 KB"
    assert format_bytes(1024 * 1024 * 1.5) == "1.50 MB"
    assert format_bytes(1024 * 1024 * 1024 * 3.25) == "3.25 GB"

    with pytest.raises(ValueError, match="Byte size cannot be negative"):
        format_bytes(-1)


def test_get_dataframe_memory_usage() -> None:
    """Test get_dataframe_memory_usage returns a positive float size."""
    df = pd.DataFrame({"A": [1, 2, 3], "B": ["x", "y", "z"]})
    mem = get_dataframe_memory_usage(df)
    assert isinstance(mem, float)
    assert mem > 0


def test_configure_logging() -> None:
    """Test logger configuration matches verbosity levels."""
    logger = get_logger()
    assert logger.name == LOGGER_NAME

    # Silent mode (verbosity 0)
    configure_logging(verbosity=0)
    assert logger.level == logging.CRITICAL

    # Warning mode (verbosity 1)
    configure_logging(verbosity=1)
    assert logger.level == logging.WARNING

    # Debug/Info mode (verbosity 2)
    configure_logging(verbosity=2)
    assert logger.level == logging.INFO

    # Suppress warnings (ignore_warnings=True)
    configure_logging(verbosity=2, ignore_warnings=True)
    assert logger.level == logging.ERROR


def test_track_operation_history() -> None:
    """Test the @track_operation decorator logs entries in self.history."""
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    cleaner = Cleaner(df)

    assert len(cleaner.history) == 0

    # Run tracked operation
    cleaner.dummy_clean()

    assert len(cleaner.history) == 1
    record = cleaner.history[0]
    assert record["operation"] == "dummy_clean"
    assert record["rows_before"] == 2
    assert record["rows_after"] == 2
    assert record["columns_before"] == 2
    assert record["columns_after"] == 2
    assert isinstance(record["time_taken_seconds"], float)
    assert record["time_taken_seconds"] >= 0.0
    assert isinstance(record["memory_before"], float)
    assert isinstance(record["memory_after"], float)


def test_cleaner_copy_preserves_history() -> None:
    """Test Cleaner.copy() copies history list by value."""
    df = pd.DataFrame({"A": [1, 2]})
    cleaner = Cleaner(df)
    cleaner.dummy_clean()

    copied = cleaner.copy()
    assert len(copied.history) == 1

    # Modify copy history, original should remain unaffected
    copied.dummy_clean()
    assert len(copied.history) == 2
    assert len(cleaner.history) == 1
