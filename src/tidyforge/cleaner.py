"""Main Cleaner class for chainable data cleaning operations."""

from pathlib import Path
from typing import Any, Optional, Union

import pandas as pd

from tidyforge.config import CleanerConfig, get_global_config
from tidyforge.exceptions import ValidationError
from tidyforge.loaders import load_data
from tidyforge.utils.decorators import track_operation
from tidyforge.utils.logging import configure_logging
from tidyforge.validation import validate_dataframe_non_empty, validate_no_duplicate_columns


class Cleaner:
    """A wrapper for Pandas DataFrames providing chainable cleaning methods."""

    def __init__(self, df: pd.DataFrame, config: Optional[CleanerConfig] = None) -> None:
        """Initialize the Cleaner.

        Args:
            df: The Pandas DataFrame to clean.
            config: Optional local CleanerConfig configuration.

        Raises:
            ValidationError: If `df` is not a Pandas DataFrame, is empty,
                             or contains duplicate column names.
        """
        if not isinstance(df, pd.DataFrame):
            raise ValidationError("Input must be a pandas DataFrame.")
        validate_dataframe_non_empty(df)
        validate_no_duplicate_columns(df)

        self._config = config if config is not None else get_global_config()
        self._df = df.copy() if self._config.copy else df

        # Initialize operation execution log history
        self.history: list[dict[str, Any]] = []

        # Sync library logging levels with the configuration
        configure_logging(self._config.verbosity, self._config.ignore_warnings)

    @classmethod
    def from_csv(
        cls,
        filepath: Union[str, Path],
        config: Optional[CleanerConfig] = None,
        **kwargs: Any,
    ) -> "Cleaner":
        """Create a Cleaner instance from a CSV file.

        Args:
            filepath: Path to the CSV file.
            config: Optional CleanerConfig configuration.
            **kwargs: Arguments passed to pd.read_csv.

        Returns:
            A Cleaner instance containing the loaded DataFrame.
        """
        path = Path(filepath)
        if path.suffix.lower() != ".csv":
            raise ValidationError(f"File must be a CSV file. Got: {path.suffix}")
        df = load_data(path, **kwargs)
        return cls(df, config=config)

    @classmethod
    def from_json(
        cls,
        filepath: Union[str, Path],
        config: Optional[CleanerConfig] = None,
        **kwargs: Any,
    ) -> "Cleaner":
        """Create a Cleaner instance from a JSON file.

        Args:
            filepath: Path to the JSON file.
            config: Optional CleanerConfig configuration.
            **kwargs: Arguments passed to pd.read_json.

        Returns:
            A Cleaner instance containing the loaded DataFrame.
        """
        path = Path(filepath)
        if path.suffix.lower() != ".json":
            raise ValidationError(f"File must be a JSON file. Got: {path.suffix}")
        df = load_data(path, **kwargs)
        return cls(df, config=config)

    @classmethod
    def from_dict(
        cls,
        data: dict[Any, Any],
        config: Optional[CleanerConfig] = None,
        **kwargs: Any,
    ) -> "Cleaner":
        """Create a Cleaner instance from a dictionary.

        Args:
            data: A dictionary to construct the DataFrame.
            config: Optional CleanerConfig configuration.
            **kwargs: Arguments passed to pd.DataFrame.

        Returns:
            A Cleaner instance containing the loaded DataFrame.
        """
        df = load_data(data, **kwargs)
        return cls(df, config=config)

    @property
    def config(self) -> CleanerConfig:
        """Get the active configuration for this Cleaner instance."""
        return self._config

    def to_dataframe(self) -> pd.DataFrame:
        """Return the current cleaned Pandas DataFrame.

        Returns:
            The cleaned pandas DataFrame.
        """
        return self._df

    def copy(self) -> "Cleaner":
        """Create a copy of the Cleaner and its underlying DataFrame.

        Returns:
            A new Cleaner instance with a copied DataFrame.
        """
        new_cleaner = Cleaner(self._df.copy(), config=self._config)
        new_cleaner.history = list(self.history)
        return new_cleaner

    @track_operation
    def dummy_clean(self) -> "Cleaner":
        """A placeholder cleaning method to demonstrate the chainable API.

        This method is a no-op placeholder.

        Returns:
            The Cleaner instance for method chaining.
        """
        return self
