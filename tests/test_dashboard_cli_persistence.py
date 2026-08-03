from pathlib import Path

from beastos.application import ApplicationSettings, bootstrap_application
from beastos.cli.app import main
from beastos.storage.sqlite.dashboard_repository import (
    DashboardSnapshotRecord,
)


def test_dashboard_cli_reads_latest_snapshot(
    tmp_path: Path,
    monkeypatch,
    capsys,
):
    data_directory = tmp_path / "data"
    database_path = data_directory / "beast.db"

    monkeypatch.setenv("BEAST_DATA_DIR", str(data_directory))
    monkeypatch.setenv("BEAST_DATABASE_PATH", str(database_path))

    application = bootstrap_application(
        ApplicationSettings(
            data_directory=data_directory,
            database_path=database_path,
        )
    )
    application.dashboard_repository.save(
        DashboardSnapshotRecord(
            score=84.5,
            goals_completed=3,
            goals_total=5,
            habits_completed=6,
            habits_target=8,
            planner_completion=82.0,
            focus_minutes=210,
        )
    )

    exit_code = main(["dashboard"])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "=== BEAST OS ===" in output
    assert "Productivity:" in output
    assert "Goals: 3/5" in output
    assert "Habits: 6/8" in output
