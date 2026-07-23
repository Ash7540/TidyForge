"""Unit tests for the TidyForge data loading utilities."""

import json
from pathlib import Path

import pandas as pd
import pytest

from tidyforge import Cleaner, ValidationError, load_data


def test_load_data_dataframe() -> None:
    """Test load_data returns the DataFrame unchanged if already a DataFrame."""
    df = pd.DataFrame({"A": [1, 2]})
    result = load_data(df)
    assert result is df


def test_load_data_dict_and_list() -> None:
    """Test loading from a dictionary or a list."""
    data_dict = {"A": [1, 2], "B": [3, 4]}
    df_dict = load_data(data_dict)
    assert isinstance(df_dict, pd.DataFrame)
    assert list(df_dict.columns) == ["A", "B"]

    data_list = [{"A": 1, "B": 2}, {"A": 3, "B": 4}]
    df_list = load_data(data_list)
    assert isinstance(df_list, pd.DataFrame)
    assert len(df_list) == 2


def test_load_data_unsupported_type() -> None:
    """Test load_data raises ValidationError on unsupported types."""
    with pytest.raises(ValidationError, match="Unsupported data source type"):
        load_data(12345)


def test_load_data_csv(tmp_path: Path) -> None:
    """Test loading from a CSV file."""
    csv_file = tmp_path / "test.csv"
    csv_content = "A,B\n1,2\n3,4"
    csv_file.write_text(csv_content, encoding="utf-8")

    df = load_data(csv_file)
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["A", "B"]
    assert df.loc[0, "A"] == 1


def test_load_data_json(tmp_path: Path) -> None:
    """Test loading from a JSON file."""
    json_file = tmp_path / "test.json"
    data = [{"A": 1, "B": 2}, {"A": 3, "B": 4}]
    json_file.write_text(json.dumps(data), encoding="utf-8")

    df = load_data(json_file)
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["A", "B"]
    assert df.loc[0, "A"] == 1


def test_load_data_file_not_found() -> None:
    """Test load_data raises ValidationError when file does not exist."""
    with pytest.raises(ValidationError, match="File not found"):
        load_data("nonexistent_file_path.csv")


def test_load_data_unsupported_suffix(tmp_path: Path) -> None:
    """Test load_data raises ValidationError for unsupported file suffixes."""
    unsupported_file = tmp_path / "test.txt"
    unsupported_file.write_text("dummy", encoding="utf-8")
    with pytest.raises(ValidationError, match="Unsupported file format"):
        load_data(unsupported_file)


def test_cleaner_from_csv(tmp_path: Path) -> None:
    """Test Cleaner.from_csv factory method."""
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("A,B\n1,2\n3,4", encoding="utf-8")

    cleaner = Cleaner.from_csv(csv_file)
    assert isinstance(cleaner, Cleaner)
    assert list(cleaner.to_dataframe().columns) == ["A", "B"]

    # Test extension validation
    with pytest.raises(ValidationError, match="File must be a CSV file"):
        Cleaner.from_csv(tmp_path / "test.json")


def test_cleaner_from_json(tmp_path: Path) -> None:
    """Test Cleaner.from_json factory method."""
    json_file = tmp_path / "test.json"
    data = [{"A": 1, "B": 2}]
    json_file.write_text(json.dumps(data), encoding="utf-8")

    cleaner = Cleaner.from_json(json_file)
    assert isinstance(cleaner, Cleaner)
    assert list(cleaner.to_dataframe().columns) == ["A", "B"]

    # Test extension validation
    with pytest.raises(ValidationError, match="File must be a JSON file"):
        Cleaner.from_json(tmp_path / "test.csv")


def test_cleaner_from_dict() -> None:
    """Test Cleaner.from_dict factory method."""
    data = {"A": [1, 2], "B": [3, 4]}
    cleaner = Cleaner.from_dict(data)
    assert isinstance(cleaner, Cleaner)
    assert list(cleaner.to_dataframe().columns) == ["A", "B"]
