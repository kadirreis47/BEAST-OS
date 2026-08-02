from __future__ import annotations

from collections.abc import Mapping
from copy import deepcopy
from typing import Any


def deep_merge(base: Mapping[str, Any], override: Mapping[str, Any]) -> dict[str, Any]:
    """Return a recursive merge where override values have precedence."""
    merged = deepcopy(dict(base))
    for key, value in override.items():
        current = merged.get(key)
        if isinstance(current, Mapping) and isinstance(value, Mapping):
            merged[key] = deep_merge(current, value)
        else:
            merged[key] = deepcopy(value)
    return merged


def get_path(data: Mapping[str, Any], path: str) -> Any:
    current: Any = data
    for segment in path.split("."):
        if not isinstance(current, Mapping) or segment not in current:
            raise KeyError(path)
        current = current[segment]
    return current


def set_path(data: dict[str, Any], path: str, value: Any) -> None:
    segments = path.split(".")
    current = data
    for segment in segments[:-1]:
        child = current.get(segment)
        if not isinstance(child, dict):
            child = {}
            current[segment] = child
        current = child
    current[segments[-1]] = value
