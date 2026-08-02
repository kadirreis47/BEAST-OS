from __future__ import annotations

from collections.abc import Iterator, Mapping
from copy import deepcopy
from types import MappingProxyType
from typing import Any, TypeVar

from .errors import ConfigurationTypeError, MissingConfigurationError
from .utils import get_path

T = TypeVar("T")
_MISSING = object()
_SECRET_MARKERS = ("password", "secret", "token", "api_key", "private_key")


class Settings(Mapping[str, Any]):
    """Immutable configuration snapshot with typed dotted-path access."""

    def __init__(self, values: Mapping[str, Any]) -> None:
        self._values = _freeze(deepcopy(dict(values)))

    def __getitem__(self, key: str) -> Any:
        return self._values[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._values)

    def __len__(self) -> int:
        return len(self._values)

    def get_value(
        self,
        path: str,
        expected_type: type[T] | tuple[type[Any], ...] | None = None,
        default: Any = _MISSING,
    ) -> T | Any:
        try:
            value = get_path(self._values, path)
        except KeyError as exc:
            if default is not _MISSING:
                return default
            raise MissingConfigurationError(f"Missing configuration value: {path}") from exc

        if expected_type is not None and not isinstance(value, expected_type):
            expected = _type_name(expected_type)
            raise ConfigurationTypeError(
                f"Configuration value '{path}' must be {expected}; got {type(value).__name__}"
            )
        return value

    def to_dict(self) -> dict[str, Any]:
        return _thaw(self._values)

    def redacted(self) -> dict[str, Any]:
        return _redact(self.to_dict())


def _freeze(value: Any) -> Any:
    if isinstance(value, Mapping):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    if isinstance(value, tuple):
        return tuple(_freeze(item) for item in value)
    return value


def _thaw(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: _thaw(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_thaw(item) for item in value]
    return deepcopy(value)


def _redact(value: Any) -> Any:
    if isinstance(value, dict):
        result: dict[str, Any] = {}
        for key, item in value.items():
            if any(marker in key.lower() for marker in _SECRET_MARKERS):
                result[key] = "***REDACTED***"
            else:
                result[key] = _redact(item)
        return result
    if isinstance(value, list):
        return [_redact(item) for item in value]
    return value


def _type_name(expected_type: type[Any] | tuple[type[Any], ...]) -> str:
    if isinstance(expected_type, tuple):
        return " or ".join(item.__name__ for item in expected_type)
    return expected_type.__name__
