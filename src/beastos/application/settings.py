from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os


@dataclass(frozen=True, slots=True)
class ApplicationSettings:
    data_directory: Path
    database_path: Path

    @classmethod
    def from_environment(cls) -> "ApplicationSettings":
        data_directory = Path(
            os.getenv("BEAST_DATA_DIR", ".beast")
        ).expanduser().resolve()
        database_path = Path(
            os.getenv(
                "BEAST_DATABASE_PATH",
                str(data_directory / "beast.db"),
            )
        ).expanduser().resolve()
        return cls(
            data_directory=data_directory,
            database_path=database_path,
        )

    def ensure_directories(self) -> None:
        self.data_directory.mkdir(parents=True, exist_ok=True)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
