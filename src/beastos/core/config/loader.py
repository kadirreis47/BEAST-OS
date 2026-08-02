from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from typing import Any

from .errors import MissingConfigurationError
from .settings import Settings
from .sources import ConfigurationSource
from .utils import deep_merge, get_path

ConfigurationValidator = Callable[[Mapping[str, Any]], None]


class ConfigurationLoader:
    """Build immutable settings from ordered configuration sources."""

    def __init__(self) -> None:
        self._sources: list[ConfigurationSource] = []
        self._required_paths: set[str] = set()
        self._validators: list[ConfigurationValidator] = []

    def add_source(self, source: ConfigurationSource) -> ConfigurationLoader:
        self._sources.append(source)
        return self

    def require(self, *paths: str) -> ConfigurationLoader:
        self._required_paths.update(paths)
        return self

    def add_validator(self, validator: ConfigurationValidator) -> ConfigurationLoader:
        self._validators.append(validator)
        return self

    def load(self) -> Settings:
        merged: dict[str, Any] = {}
        for source in self._sources:
            merged = deep_merge(merged, source.load())

        missing = _missing_paths(merged, self._required_paths)
        if missing:
            formatted = ", ".join(sorted(missing))
            raise MissingConfigurationError(f"Missing required configuration: {formatted}")

        for validator in self._validators:
            validator(merged)

        return Settings(merged)


def _missing_paths(values: Mapping[str, Any], paths: Iterable[str]) -> list[str]:
    missing: list[str] = []
    for path in paths:
        try:
            get_path(values, path)
        except KeyError:
            missing.append(path)
    return missing
