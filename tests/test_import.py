"""Smoke tests for TidyForge package imports and version."""

import tidyforge
from tidyforge.exceptions import ConfigurationError, TidyForgeError, ValidationError


def test_package_version() -> None:

    assert tidyforge.__version__ == "0.1.0.dev0"


def test_exception_hierarchy() -> None:

    assert issubclass(ValidationError, TidyForgeError)
    assert issubclass(ConfigurationError, TidyForgeError)
