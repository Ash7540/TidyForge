"""Unit tests for the validation functions and decorators."""

import pandas as pd
import pytest

from tidyforge import (
    ValidationError,
    requires_columns,
    validate_columns_exist,
    validate_dataframe_non_empty,
    validate_no_duplicate_columns,
)


def test_validate_dataframe_non_empty() -> None:
    """Test validate_dataframe_non_empty detects empty/invalid shapes."""
    df_valid = pd.DataFrame({"A": [1, 2]})
    validate_dataframe_non_empty(df_valid)  # Should not raise

    df_empty_rows = pd.DataFrame(columns=["A"])
    with pytest.raises(ValidationError, match="DataFrame cannot be empty"):
        validate_dataframe_non_empty(df_empty_rows)

    df_empty_cols = pd.DataFrame()
    with pytest.raises(ValidationError, match="DataFrame cannot be empty"):
        validate_dataframe_non_empty(df_empty_cols)


def test_validate_no_duplicate_columns() -> None:
    """Test validate_no_duplicate_columns detects duplicate column names."""
    df_valid = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    validate_no_duplicate_columns(df_valid)  # Should not raise

    # Construct DataFrame with duplicate columns manually to bypass pandas dict deduplication
    df_dup = pd.DataFrame([[1, 2], [3, 4]], columns=["A", "A"])
    with pytest.raises(ValidationError, match="DataFrame contains duplicate column names"):
        validate_no_duplicate_columns(df_dup)


def test_validate_columns_exist() -> None:
    """Test validate_columns_exist checks for existence and type."""
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})

    # Valid check
    assert validate_columns_exist(df, "A") == ["A"]
    assert validate_columns_exist(df, ["A", "B"]) == ["A", "B"]
    assert validate_columns_exist(df, {"A", "B"}) == ["A", "B"] or ["B", "A"]
    assert validate_columns_exist(df, ("A",)) == ["A"]

    # Invalid column checks
    with pytest.raises(ValidationError, match="The following columns were not found"):
        validate_columns_exist(df, "C")

    with pytest.raises(ValidationError, match="The following columns were not found"):
        validate_columns_exist(df, ["A", "C"])

    # Invalid argument types
    with pytest.raises(ValidationError, match="Columns parameter must be a string or a collection"):
        validate_columns_exist(df, 123)  # type: ignore[arg-type]

    with pytest.raises(ValidationError, match="All column names must be strings"):
        validate_columns_exist(df, ["A", 123])  # type: ignore[list-item]


# Mock class to test decorator behavior
class MockCleaner:
    def __init__(self, df: pd.DataFrame) -> None:
        self._df = df

    @requires_columns("columns")
    def clean_columns_default(self, columns: str) -> str:
        return "success"

    @requires_columns("cols")
    def clean_columns_custom(self, cols: list[str], other_arg: int = 1) -> str:
        return f"success-{other_arg}"


def test_requires_columns_decorator() -> None:
    """Test the @requires_columns decorator validations."""
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    mock = MockCleaner(df)

    # Valid inputs
    assert mock.clean_columns_default("A") == "success"
    assert mock.clean_columns_custom(["A", "B"], other_arg=42) == "success-42"

    # Missing column inputs
    with pytest.raises(ValidationError, match="The following columns were not found"):
        mock.clean_columns_default("C")

    with pytest.raises(ValidationError, match="The following columns were not found"):
        mock.clean_columns_custom(["A", "C"])
