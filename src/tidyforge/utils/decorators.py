"""Decorators for tracking, monitoring, and logging Cleaner operations."""

import time
from functools import wraps
from typing import Any, Callable

from tidyforge.utils.helpers import format_bytes, get_dataframe_memory_usage
from tidyforge.utils.logging import get_logger


def track_operation(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to track and log execution details of a Cleaner operation.

    Tracks execution time, changes in row/column count, changes in memory usage,
    and logs diagnostic info. It also appends record dictionary to the Cleaner
    instance's `history` list.
    """

    @wraps(func)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        logger = get_logger()

        # Capture pre-run state
        df_before = self._df
        rows_before = len(df_before)
        cols_before = len(df_before.columns)
        mem_before = get_dataframe_memory_usage(df_before)

        start_time = time.perf_counter()

        # Execute method
        result = func(self, *args, **kwargs)

        elapsed = time.perf_counter() - start_time

        # Capture post-run state
        df_after = self._df
        rows_after = len(df_after)
        cols_after = len(df_after.columns)
        mem_after = get_dataframe_memory_usage(df_after)

        record = {
            "operation": func.__name__,
            "time_taken_seconds": elapsed,
            "rows_before": rows_before,
            "rows_after": rows_after,
            "columns_before": cols_before,
            "columns_after": cols_after,
            "memory_before": mem_before,
            "memory_after": mem_after,
        }

        if hasattr(self, "history") and isinstance(self.history, list):
            self.history.append(record)

        logger.info(
            f"Operation '{func.__name__}' completed in {elapsed:.4f}s. "
            f"Rows: {rows_before} -> {rows_after} ({rows_after - rows_before:+d}), "
            f"Cols: {cols_before} -> {cols_after} ({cols_after - cols_before:+d}), "
            f"Memory: {format_bytes(mem_before)} -> {format_bytes(mem_after)}"
        )

        return result

    return wrapper
