from pathlib import Path

from beastos.application import ApplicationSettings, bootstrap_application
from beastos.storage.sqlite.dashboard_repository import (
    DashboardSnapshotRecord,
)


def test_bootstrap_creates_database(tmp_path: Path):
    settings = ApplicationSettings(
        data_directory=tmp_path,
        database_path=tmp_path / "beast.db",
    )

    application = bootstrap_application(settings)

    assert application.settings == settings
    assert settings.database_path.exists()


def test_dashboard_repository_roundtrip(tmp_path: Path):
    application = bootstrap_application(
        ApplicationSettings(
            data_directory=tmp_path,
            database_path=tmp_path / "beast.db",
        )
    )
    snapshot = DashboardSnapshotRecord(
        score=84.5,
        goals_completed=3,
        goals_total=5,
        habits_completed=6,
        habits_target=8,
        planner_completion=82.0,
        focus_minutes=210,
    )

    record_id = application.dashboard_repository.save(snapshot)
    loaded = application.dashboard_repository.latest()

    assert record_id > 0
    assert loaded == snapshot
