"""Configuration system for TidyForge."""

from dataclasses import dataclass

from tidyforge.exceptions import ConfigurationError


@dataclass
class CleanerConfig:
    """Configuration settings for the Cleaner.

    Attributes:
        copy: If True, input DataFrames are copied to avoid side-effects.
        ignore_warnings: If True, suppress warning logs.
        verbosity: Logging level (0 = silent, 1 = warnings/errors, 2 = detailed).
    """

    copy: bool = True
    ignore_warnings: bool = False
    verbosity: int = 1

    def __post_init__(self) -> None:
        """Validate configuration values."""
        if not isinstance(self.copy, bool):
            raise ConfigurationError("`copy` parameter must be a boolean.")
        if not isinstance(self.ignore_warnings, bool):
            raise ConfigurationError("`ignore_warnings` parameter must be a boolean.")
        if not isinstance(self.verbosity, int) or self.verbosity not in (0, 1, 2):
            raise ConfigurationError("`verbosity` must be an integer in (0, 1, 2).")


_GLOBAL_CONFIG = CleanerConfig()


def get_global_config() -> CleanerConfig:
    """Get the global CleanerConfig instance."""
    return _GLOBAL_CONFIG


def set_global_config(config: CleanerConfig) -> None:
    """Set the global CleanerConfig instance."""
    global _GLOBAL_CONFIG
    if not isinstance(config, CleanerConfig):
        raise ConfigurationError("Config must be an instance of CleanerConfig.")
    _GLOBAL_CONFIG = config
