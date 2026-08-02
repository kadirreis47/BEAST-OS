from datetime import UTC, datetime

import pytest

from beastos.scheduler import IntervalSchedule, RetryPolicy


def test_interval_schedule_produces_next_run() -> None:
    start = datetime(2026, 8, 2, 12, 0, tzinfo=UTC)
    assert IntervalSchedule(60).next_run(start).isoformat() == "2026-08-02T12:01:00+00:00"


def test_retry_policy_uses_capped_exponential_backoff() -> None:
    policy = RetryPolicy(base_delay_seconds=10, multiplier=2, max_delay_seconds=25)
    assert [policy.delay_for(i) for i in (1, 2, 3, 4)] == [10, 20, 25, 25]


def test_naive_datetime_is_rejected() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        IntervalSchedule(60).next_run(datetime(2026, 8, 2, 12, 0))
