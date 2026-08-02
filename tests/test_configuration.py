from __future__ import annotations

import json
from pathlib import Path

import pytest

from beastos.core.config import (
    ConfigurationFileError,
    ConfigurationLoader,
    ConfigurationTypeError,
    DictionarySource,
    EnvironmentSource,
    JsonSource,
    MissingConfigurationError,
    TomlSource,
)


def test_sources_are_merged_in_registration_order() -> None:
    settings = (
        ConfigurationLoader()
        .add_source(DictionarySource({"database": {"host": "localhost", "port": 5432}}))
        .add_source(DictionarySource({"database": {"port": 6543}, "debug": True}))
        .load()
    )

    assert settings.get_value("database.host", str) == "localhost"
    assert settings.get_value("database.port", int) == 6543
    assert settings.get_value("debug", bool) is True


def test_environment_source_builds_nested_values_and_parses_json() -> None:
    source = EnvironmentSource(
        environ={
            "BEAST_DATABASE__PORT": "5432",
            "BEAST_FEATURES__ENABLED": "true",
            "BEAST_TAGS": '["health", "training"]',
            "OTHER_VALUE": "ignored",
        }
    )

    values = source.load()

    assert values == {
        "database": {"port": 5432},
        "features": {"enabled": True},
        "tags": ["health", "training"],
    }


def test_json_and_toml_sources(tmp_path: Path) -> None:
    json_path = tmp_path / "settings.json"
    json_path.write_text(json.dumps({"app": {"name": "BEAST OS"}}), encoding="utf-8")
    toml_path = tmp_path / "settings.toml"
    toml_path.write_text("[app]\nworkers = 4\n", encoding="utf-8")

    settings = (
        ConfigurationLoader()
        .add_source(JsonSource(json_path))
        .add_source(TomlSource(toml_path))
        .load()
    )

    assert settings.get_value("app.name") == "BEAST OS"
    assert settings.get_value("app.workers") == 4


def test_optional_file_source_returns_empty_mapping(tmp_path: Path) -> None:
    assert JsonSource(tmp_path / "missing.json", optional=True).load() == {}
    assert TomlSource(tmp_path / "missing.toml", optional=True).load() == {}


def test_invalid_json_raises_domain_error(tmp_path: Path) -> None:
    path = tmp_path / "broken.json"
    path.write_text("{broken", encoding="utf-8")

    with pytest.raises(ConfigurationFileError):
        JsonSource(path).load()


def test_required_paths_are_validated_together() -> None:
    loader = ConfigurationLoader().add_source(DictionarySource({"app": {"name": "BEAST"}}))
    loader.require("database.url", "security.secret")

    with pytest.raises(MissingConfigurationError) as exc_info:
        loader.load()

    assert "database.url" in str(exc_info.value)
    assert "security.secret" in str(exc_info.value)


def test_typed_access_rejects_unexpected_type() -> None:
    settings = ConfigurationLoader().add_source(DictionarySource({"workers": "4"})).load()

    with pytest.raises(ConfigurationTypeError):
        settings.get_value("workers", int)


def test_default_is_returned_only_for_missing_value() -> None:
    settings = ConfigurationLoader().add_source(DictionarySource({})).load()

    assert settings.get_value("missing", default=12) == 12


def test_settings_snapshot_is_immutable_and_detached() -> None:
    source = {"features": {"enabled": ["health"]}}
    settings = ConfigurationLoader().add_source(DictionarySource(source)).load()
    source["features"]["enabled"].append("money")

    assert settings.get_value("features.enabled") == ("health",)
    with pytest.raises(TypeError):
        settings["features"]["new"] = True


def test_redacted_hides_nested_secrets() -> None:
    settings = ConfigurationLoader().add_source(
        DictionarySource(
            {
                "database": {"password": "top-secret", "host": "localhost"},
                "auth": {"api_key": "abc", "token_ttl": 3600},
            }
        )
    ).load()

    assert settings.redacted() == {
        "database": {"password": "***REDACTED***", "host": "localhost"},
        "auth": {"api_key": "***REDACTED***", "token_ttl": "***REDACTED***"},
    }


def test_custom_validator_runs_before_snapshot_is_returned() -> None:
    def validate(values: dict[str, object]) -> None:
        if values["workers"] < 1:  # type: ignore[operator]
            raise ValueError("workers must be positive")

    loader = (
        ConfigurationLoader()
        .add_source(DictionarySource({"workers": 0}))
        .add_validator(validate)
    )

    with pytest.raises(ValueError, match="workers must be positive"):
        loader.load()
