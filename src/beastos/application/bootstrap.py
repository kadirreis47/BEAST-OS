from __future__ import annotations

from dataclasses import dataclass

from beastos.storage.sqlite.dashboard_repository import DashboardRepository

from .settings import ApplicationSettings


@dataclass(slots=True)
class Application:
    settings: ApplicationSettings
    dashboard_repository: DashboardRepository


def bootstrap_application(
    settings: ApplicationSettings | None = None,
) -> Application:
    resolved = settings or ApplicationSettings.from_environment()
    resolved.ensure_directories()

    return Application(
        settings=resolved,
        dashboard_repository=DashboardRepository(
            resolved.database_path
        ),
    )
