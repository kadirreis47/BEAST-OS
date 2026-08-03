from __future__ import annotations

from dataclasses import asdict
from typing import Any

from .models import DashboardState


def dashboard_to_dict(state: DashboardState) -> dict[str, Any]:
    return asdict(state)
