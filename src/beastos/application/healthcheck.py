
from __future__ import annotations

from dataclasses import dataclass

@dataclass(slots=True,frozen=True)
class HealthStatus:
    name:str
    healthy:bool
    message:str="OK"

def check_container(container)->list[HealthStatus]:
    return [
        HealthStatus("container",True),
        HealthStatus("services",container.has("dashboard_repository"))
    ]
