"""Data loading utilities for TidyForge."""

from pathlib import Path
from typing import Any

import pandas as pd

from tidyforge.exceptions import ValidationError


def load_data(source: Any, **kwargs: Any) -> pd.DataFrame:
    """Load data from various formats into a pandas DataFrame.

    Args:
        source: A DataFrame, file path (str or Path), dictionary, or list.
        **kwargs: Keyword arguments passed to the underlying Pandas reader function.

    Returns:
        A pandas DataFrame.

    Raises:
        ValidationError: If the source format is unsupported or file loading fails.
    """
    if isinstance(source, pd.DataFrame):
        return source

    if isinstance(source, (str, Path)):
        path = Path(source)
        suffix = path.suffix.lower()

        try:
            if suffix == ".csv":
                return pd.read_csv(path, **kwargs)
            elif suffix in (".xlsx", ".xls"):
                return pd.read_excel(path, **kwargs)
            elif suffix == ".json":
                return pd.read_json(path, **kwargs)
            elif suffix == ".parquet":
                return pd.read_parquet(path, **kwargs)
            else:
                raise ValidationError(f"Unsupported file format: {suffix}")
        except FileNotFoundError as e:
            raise ValidationError(f"File not found: {path}") from e
        except Exception as e:
            if isinstance(e, ValidationError):
                raise
            raise ValidationError(f"Error loading file {path}: {e}") from e

    if isinstance(source, (dict, list)):
        try:
            return pd.DataFrame(source, **kwargs)
        except Exception as e:
            raise ValidationError(f"Error constructing DataFrame from dict/list: {e}") from e

    raise ValidationError(
        f"Unsupported data source type: {type(source).__name__}. "
        "Must be a DataFrame, file path (str or Path), dictionary, or list."
    )
