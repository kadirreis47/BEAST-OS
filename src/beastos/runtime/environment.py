
from dataclasses import dataclass
from pathlib import Path
import platform,sys

@dataclass(frozen=True,slots=True)
class EnvironmentCheck:
    name:str
    passed:bool
    message:str

def validate_environment(data_directory=".beast"):
    path=Path(data_directory)
    path.mkdir(parents=True,exist_ok=True)
    probe=path/".beast-write-test"
    probe.write_text("ok",encoding="utf-8")
    probe.unlink()
    return (
        EnvironmentCheck("python",sys.version_info>=(3,12),platform.python_version()),
        EnvironmentCheck("platform",True,platform.system()),
        EnvironmentCheck("data_directory",True,str(path.resolve())),
    )
