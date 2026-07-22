"""Main Cleaner class for chainable data cleaning operations."""

from typing import Optional

import pandas as pd

from tidyforge.config import CleanerConfig, get_global_config
from tidyforge.exceptions import ValidationError


class Cleaner:
    """A wrapper for Pandas DataFrames providing chainable cleaning methods."""

    def __init__(self, df: pd.DataFrame, config: Optional[CleanerConfig] = None) -> None:
        """Initialize the Cleaner.

        Args:
            df: The Pandas DataFrame to clean.
            config: Optional local CleanerConfig configuration.

        Raises:
            ValidationError: If `df` is not a Pandas DataFrame.
        """
        if not isinstance(df, pd.DataFrame):
            raise ValidationError("Input must be a pandas DataFrame.")

        self._config = config if config is not None else get_global_config()
        self._df = df.copy() if self._config.copy else df

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
        return Cleaner(self._df.copy(), config=self._config)

    def dummy_clean(self) -> "Cleaner":
        """A placeholder cleaning method to demonstrate the chainable API.

        This method is a no-op placeholder.

        Returns:
            The Cleaner instance for method chaining.
        """
        return self
