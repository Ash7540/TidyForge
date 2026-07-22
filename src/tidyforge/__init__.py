"""TidyForge: A modular, high-performance data cleaning library for Pandas DataFrames."""

from tidyforge.cleaner import Cleaner
from tidyforge.config import CleanerConfig, get_global_config, set_global_config
from tidyforge.exceptions import CleaningError, ConfigurationError, TidyForgeError, ValidationError

__version__ = "0.1.0.dev0"

__all__ = [
    "Cleaner",
    "CleanerConfig",
    "CleaningError",
    "ConfigurationError",
    "TidyForgeError",
    "ValidationError",
    "get_global_config",
    "set_global_config",
    "__version__",
]
