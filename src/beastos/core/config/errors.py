from __future__ import annotations


class ConfigurationError(RuntimeError):
    """Base exception for configuration failures."""


class ConfigurationFileError(ConfigurationError):
    """Raised when a configuration file cannot be loaded."""


class MissingConfigurationError(ConfigurationError):
    """Raised when a required configuration value is absent."""


class ConfigurationTypeError(ConfigurationError):
    """Raised when a configuration value has an unexpected type."""
