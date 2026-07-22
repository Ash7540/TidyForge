"""Unit tests for the core Cleaner and Configuration systems."""

import pandas as pd
import pytest

from tidyforge import (
    Cleaner,
    CleanerConfig,
    ConfigurationError,
    ValidationError,
    get_global_config,
    set_global_config,
)


def test_cleaner_init_valid() -> None:
    """Test successful initialization with a valid DataFrame."""
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    cleaner = Cleaner(df)
    assert isinstance(cleaner.to_dataframe(), pd.DataFrame)
    assert cleaner.config == get_global_config()


def test_cleaner_init_invalid() -> None:
    """Test initialization raises ValidationError with invalid input type."""
    with pytest.raises(ValidationError, match="Input must be a pandas DataFrame"):
        Cleaner([1, 2, 3])  # type: ignore[arg-type]


def test_cleaner_custom_config() -> None:
    """Test Cleaner accepts custom CleanerConfig."""
    df = pd.DataFrame({"A": [1, 2]})
    custom_config = CleanerConfig(copy=False, ignore_warnings=True, verbosity=2)
    cleaner = Cleaner(df, config=custom_config)
    assert cleaner.config == custom_config
    assert cleaner.config.copy is False
    assert cleaner.config.ignore_warnings is True
    assert cleaner.config.verbosity == 2


def test_cleaner_copy_behavior() -> None:
    """Test Cleaner copy config flag works."""
    df = pd.DataFrame({"A": [1, 2]})

    # copy=True (default) should isolate cleaner from source DataFrame changes
    cleaner_with_copy = Cleaner(df)
    df.iloc[0, 0] = 99
    assert cleaner_with_copy.to_dataframe().iloc[0, 0] == 1

    # copy=False should reference the source DataFrame
    df2 = pd.DataFrame({"A": [1, 2]})
    cleaner_no_copy = Cleaner(df2, config=CleanerConfig(copy=False))
    df2.iloc[0, 0] = 99
    assert cleaner_no_copy.to_dataframe().iloc[0, 0] == 99


def test_cleaner_copy_method() -> None:
    """Test the Cleaner.copy() method creates a copy of the state."""
    df = pd.DataFrame({"A": [1, 2]})
    cleaner = Cleaner(df)
    cleaner_copied = cleaner.copy()

    assert cleaner_copied is not cleaner
    assert cleaner_copied.to_dataframe() is not cleaner.to_dataframe()
    pd.testing.assert_frame_equal(cleaner_copied.to_dataframe(), cleaner.to_dataframe())
    assert cleaner_copied.config == cleaner.config


def test_cleaner_chaining() -> None:
    """Test that dummy_clean is chainable and returns the same instance."""
    df = pd.DataFrame({"A": [1, 2]})
    cleaner = Cleaner(df)
    result = cleaner.dummy_clean().dummy_clean()
    assert result is cleaner


def test_config_validation() -> None:
    """Test CleanerConfig validates inputs."""
    with pytest.raises(ConfigurationError, match="`copy` parameter must be a boolean"):
        CleanerConfig(copy="yes")  # type: ignore[arg-type]

    with pytest.raises(ConfigurationError, match="`ignore_warnings` parameter must be a boolean"):
        CleanerConfig(ignore_warnings=1)  # type: ignore[arg-type]

    with pytest.raises(ConfigurationError, match="`verbosity` must be an integer in"):
        CleanerConfig(verbosity=3)

    with pytest.raises(ConfigurationError, match="`verbosity` must be an integer in"):
        CleanerConfig(verbosity="high")  # type: ignore[arg-type]


def test_global_config_get_set() -> None:
    """Test retrieving and setting global config."""
    original_global = get_global_config()

    new_global = CleanerConfig(copy=False, verbosity=0)
    set_global_config(new_global)
    assert get_global_config() == new_global

    # Test set_global_config input validation
    with pytest.raises(ConfigurationError, match="Config must be an instance of CleanerConfig"):
        set_global_config({"copy": True})  # type: ignore[arg-type]

    # Restore original global config
    set_global_config(original_global)
