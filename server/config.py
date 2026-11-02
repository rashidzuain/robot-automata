"""Configuración portable; los datos activos se guardan fuera de OneDrive."""

import os
from dataclasses import dataclass, field
from pathlib import Path


def default_database_path() -> Path:
    configured = os.getenv("ROBOT_DB_PATH")
    if configured:
        return Path(configured).expanduser().resolve()
    if os.name == "nt":
        root = Path(os.environ.get("LOCALAPPDATA", str(Path.home() / "AppData/Local")))
    else:
        root = Path(os.environ.get("XDG_DATA_HOME", str(Path.home() / ".local/share")))
    return root / "RobotAutomata" / "robot.sqlite3"


@dataclass(frozen=True)
class Settings:
    database_path: Path = field(default_factory=default_database_path)
    device_id: str = "robot-01"
    stale_after_seconds: float = 5.0
    demo_interval_seconds: float = 1.0
    demo_max_seconds: float = 900.0

    def __post_init__(self) -> None:
        for name in ("stale_after_seconds", "demo_interval_seconds", "demo_max_seconds"):
            if getattr(self, name) <= 0:
                raise ValueError(f"{name} debe ser positivo")
