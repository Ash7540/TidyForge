"""TidyForge: A modular, high-performance data cleaning library for Pandas DataFrames."""

from tidyforge.cleaner import Cleaner
from tidyforge.config import CleanerConfig, get_global_config, set_global_config
from tidyforge.constants import NA_MARKERS
from tidyforge.exceptions import CleaningError, ConfigurationError, TidyForgeError, ValidationError
from tidyforge.loaders import load_data
from tidyforge.validation import (
    requires_columns,
    validate_columns_exist,
    validate_dataframe_non_empty,
    validate_no_duplicate_columns,
)

__version__ = "0.1.0.dev0"

__all__ = [
    "Cleaner",
    "CleanerConfig",
    "CleaningError",
    "ConfigurationError",
    "NA_MARKERS",
    "TidyForgeError",
    "ValidationError",
    "get_global_config",
    "load_data",
    "requires_columns",
    "set_global_config",
    "validate_columns_exist",
    "validate_dataframe_non_empty",
    "validate_no_duplicate_columns",
    "__version__",
]
