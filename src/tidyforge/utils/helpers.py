"""Helper utility functions for data processing and conversions."""

import pandas as pd


def get_dataframe_memory_usage(df: pd.DataFrame) -> float:
    """Calculate the memory footprint of a pandas DataFrame in bytes.

    Args:
        df: The pandas DataFrame.

    Returns:
        The total memory footprint in bytes.
    """
    # Use deep=True to accurately measure object type memory usage
    return float(df.memory_usage(index=True, deep=True).sum())


def format_bytes(size_in_bytes: float) -> str:
    """Convert bytes to a human-readable string representation.

    Args:
        size_in_bytes: The size in bytes.

    Returns:
        A formatted string (e.g., '12.5 KB', '1.2 MB').
    """
    if size_in_bytes < 0:
        raise ValueError("Byte size cannot be negative.")

    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_in_bytes < 1024.0:
            # Format to 2 decimal places, or integer if B
            if unit == "B":
                return f"{int(size_in_bytes)} B"
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024.0

    return f"{size_in_bytes:.2f} PB"
