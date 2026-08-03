
from dataclasses import dataclass
from .environment import validate_environment
from .health import collect_health
from .version import get_version

@dataclass(frozen=True,slots=True)
class DoctorReport:
    version:str
    environment:tuple
    health:object

    @property
    def healthy(self):
        return all(x.passed for x in self.environment) and self.health.healthy

def run_doctor(data_directory=".beast"):
    return DoctorReport(get_version(),validate_environment(data_directory),collect_health())
