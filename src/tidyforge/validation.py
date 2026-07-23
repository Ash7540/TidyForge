"""Validation layer for TidyForge data and inputs."""

import inspect
from functools import wraps
from typing import Any, Callable, Union

import pandas as pd

from tidyforge.exceptions import ValidationError


def validate_dataframe_non_empty(df: pd.DataFrame) -> None:
    """Validate that the DataFrame is not empty.

    Args:
        df: The pandas DataFrame.

    Raises:
        ValidationError: If the DataFrame has no rows or columns.
    """
    if df.empty:
        raise ValidationError("DataFrame cannot be empty.")
    if len(df.columns) == 0:
        raise ValidationError("DataFrame must have at least one column.")


def validate_no_duplicate_columns(df: pd.DataFrame) -> None:
    """Validate that the DataFrame has no duplicate column names.

    Args:
        df: The pandas DataFrame.

    Raises:
        ValidationError: If there are duplicate column names.
    """
    duplicated = df.columns.duplicated()
    if duplicated.any():
        duplicates = set(df.columns[duplicated])
        raise ValidationError(f"DataFrame contains duplicate column names: {duplicates}")


def validate_columns_exist(
    df: pd.DataFrame, columns: Union[str, list[str], set[str], tuple[str, ...]]
) -> list[str]:
    """Ensure that the specified columns exist in the DataFrame.

    Args:
        df: The pandas DataFrame.
        columns: A column name string or a collection of column names.

    Returns:
        A list of the validated column names.

    Raises:
        ValidationError: If any of the columns do not exist in the DataFrame.
    """
    if isinstance(columns, str):
        cols_list = [columns]
    elif isinstance(columns, (list, tuple, set)):
        cols_list = list(columns)
    else:
        raise ValidationError("Columns parameter must be a string or a collection of strings.")

    if not all(isinstance(c, str) for c in cols_list):
        raise ValidationError("All column names must be strings.")

    missing = [c for c in cols_list if c not in df.columns]
    if missing:
        raise ValidationError(f"The following columns were not found in the DataFrame: {missing}")

    return cols_list


def requires_columns(param_name: str = "columns") -> Callable[..., Any]:
    """Decorator to validate that columns specified in arguments exist in the Cleaner's DataFrame.

    Args:
        param_name: The name of the parameter carrying column name(s). Defaults to 'columns'.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
            sig = inspect.signature(func)
            # Bind args and kwargs to function signature to locate the column parameter value
            bound_args = sig.bind(self, *args, **kwargs)
            bound_args.apply_defaults()

            cols = bound_args.arguments.get(param_name)
            if cols is not None:
                validate_columns_exist(self._df, cols)

            return func(self, *args, **kwargs)

        return wrapper

    return decorator
