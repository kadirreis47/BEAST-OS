
from dataclasses import dataclass

@dataclass(frozen=True,slots=True)
class HealthItem:
    name:str
    healthy:bool
    message:str

@dataclass(frozen=True,slots=True)
class HealthReport:
    healthy:bool
    items:tuple[HealthItem,...]

def collect_health():
    items=(HealthItem("runtime",True,"BEAST OS runtime is available"),)
    return HealthReport(True,items)
