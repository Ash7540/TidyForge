"""Custom exception hierarchy for TidyForge."""


class TidyForgeError(Exception):
    """Base exception class for all TidyForge errors."""

    pass


class ValidationError(TidyForgeError):
    """Raised when DataFrame or input validation fails."""

    pass


class ConfigurationError(TidyForgeError):
    """Raised when an invalid configuration is provided."""

    pass


class CleaningError(TidyForgeError):
    """Raised when a cleaning operation fails during execution."""

    pass
