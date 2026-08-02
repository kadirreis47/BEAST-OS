from __future__ import annotations

import io
import json
import logging

from beastos.core.logging import (
    LoggingSettings,
    bind_context,
    clear_context,
    configure_logging,
    get_context,
    logging_context,
)


def read_json(stream: io.StringIO) -> dict:
    return json.loads(stream.getvalue().strip())


def setup_function() -> None:
    clear_context()


def test_json_log_contains_core_fields() -> None:
    stream = io.StringIO()
    logger = configure_logging(LoggingSettings(), stream=stream)
    logger.info("started")
    item = read_json(stream)
    assert item["level"] == "INFO"
    assert item["logger"] == "beastos"
    assert item["message"] == "started"
    assert item["timestamp"].endswith("+00:00")


def test_context_is_added_to_record() -> None:
    stream = io.StringIO()
    logger = configure_logging(LoggingSettings(), stream=stream)
    bind_context(request_id="req-1", user_id="u-7")
    logger.warning("slow")
    item = read_json(stream)
    assert item["request_id"] == "req-1"
    assert item["user_id"] == "u-7"


def test_context_manager_restores_previous_context() -> None:
    bind_context(request_id="outer")
    with logging_context(request_id="inner", job_id="job-1"):
        assert get_context() == {"request_id": "inner", "job_id": "job-1"}
    assert get_context() == {"request_id": "outer"}


def test_clear_selected_context_keys() -> None:
    bind_context(a=1, b=2)
    clear_context("a")
    assert get_context() == {"b": 2}


def test_sensitive_event_data_is_redacted() -> None:
    stream = io.StringIO()
    logger = configure_logging(LoggingSettings(), stream=stream)
    logger.info("login", extra={"event_data": {"token": "abc", "profile": {"password": "x", "name": "Ada"}}})
    data = read_json(stream)["data"]
    assert data["token"] == "***REDACTED***"
    assert data["profile"]["password"] == "***REDACTED***"
    assert data["profile"]["name"] == "Ada"


def test_exception_is_serialized() -> None:
    stream = io.StringIO()
    logger = configure_logging(LoggingSettings(), stream=stream)
    try:
        raise RuntimeError("boom")
    except RuntimeError:
        logger.exception("failed")
    assert "RuntimeError: boom" in read_json(stream)["exception"]


def test_configuration_is_idempotent() -> None:
    logger = configure_logging()
    configure_logging()
    assert len(logger.handlers) == 1


def test_plain_text_mode() -> None:
    stream = io.StringIO()
    logger = configure_logging(LoggingSettings(json_output=False, level=logging.DEBUG), stream=stream)
    logger.debug("debug message")
    assert "DEBUG beastos debug message" in stream.getvalue()
