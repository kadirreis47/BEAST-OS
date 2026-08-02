from __future__ import annotations

import json
import os
import tomllib
from abc import ABC, abstractmethod
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from .errors import ConfigurationFileError
from .utils import set_path


class ConfigurationSource(ABC):
    @abstractmethod
    def load(self) -> Mapping[str, Any]:
        """Load configuration values from this source."""


class DictionarySource(ConfigurationSource):
    def __init__(self, values: Mapping[str, Any]) -> None:
        self._values = dict(values)

    def load(self) -> Mapping[str, Any]:
        return self._values


class JsonSource(ConfigurationSource):
    def __init__(self, path: str | Path, *, optional: bool = False) -> None:
        self.path = Path(path)
        self.optional = optional

    def load(self) -> Mapping[str, Any]:
        if not self.path.exists() and self.optional:
            return {}
        try:
            with self.path.open("r", encoding="utf-8") as handle:
                value = json.load(handle)
        except (OSError, json.JSONDecodeError) as exc:
            raise ConfigurationFileError(f"Cannot load JSON configuration: {self.path}") from exc
        if not isinstance(value, dict):
            raise ConfigurationFileError(f"JSON configuration root must be an object: {self.path}")
        return value


class TomlSource(ConfigurationSource):
    def __init__(self, path: str | Path, *, optional: bool = False) -> None:
        self.path = Path(path)
        self.optional = optional

    def load(self) -> Mapping[str, Any]:
        if not self.path.exists() and self.optional:
            return {}
        try:
            with self.path.open("rb") as handle:
                value = tomllib.load(handle)
        except (OSError, tomllib.TOMLDecodeError) as exc:
            raise ConfigurationFileError(f"Cannot load TOML configuration: {self.path}") from exc
        return value


class EnvironmentSource(ConfigurationSource):
    def __init__(
        self,
        *,
        prefix: str = "BEAST_",
        delimiter: str = "__",
        environ: Mapping[str, str] | None = None,
    ) -> None:
        self.prefix = prefix
        self.delimiter = delimiter
        self.environ = environ

    def load(self) -> Mapping[str, Any]:
        environment = self.environ if self.environ is not None else os.environ
        result: dict[str, Any] = {}
        for name, raw_value in environment.items():
            if not name.startswith(self.prefix):
                continue
            raw_path = name[len(self.prefix) :]
            if not raw_path:
                continue
            path = ".".join(part.lower() for part in raw_path.split(self.delimiter))
            set_path(result, path, _parse_environment_value(raw_value))
        return result


def _parse_environment_value(raw_value: str) -> Any:
    normalized = raw_value.strip()
    try:
        return json.loads(normalized)
    except json.JSONDecodeError:
        return raw_value
