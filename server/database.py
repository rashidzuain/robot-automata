"""SQLite con consultas parametrizadas y una conexión corta por operación."""

import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


class Store:
    def __init__(self, path: Path):
        self.path = path

    @contextmanager
    def connection(self):
        db = sqlite3.connect(self.path, timeout=5)
        db.row_factory = sqlite3.Row
        try:
            with db:
                yield db
        finally:
            db.close()

    def initialize(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connection() as db:
            db.execute("PRAGMA journal_mode=WAL")
            db.executescript("""
                CREATE TABLE IF NOT EXISTS telemetry (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    robot_id TEXT NOT NULL,
                    source TEXT NOT NULL CHECK(source IN ('device', 'demo')),
                    received_at TEXT NOT NULL,
                    battery_v REAL,
                    distance_cm REAL,
                    ir_left INTEGER,
                    ir_right INTEGER,
                    pwm_left INTEGER,
                    pwm_right INTEGER
                );
                CREATE INDEX IF NOT EXISTS telemetry_source_id ON telemetry(source, id DESC);
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    level TEXT NOT NULL,
                    message TEXT NOT NULL
                );
                PRAGMA user_version=1;
            """)

    @staticmethod
    def record(row):
        item = dict(row)
        for key in ("ir_left", "ir_right"):
            if item[key] is not None:
                item[key] = bool(item[key])
        return item

    def add_sample(self, sample: dict, source: str) -> dict:
        if source not in {"device", "demo"}:
            raise ValueError("Origen de telemetría inválido")
        record = {**sample, "received_at": utc_now(), "source": source}
        columns = ("robot_id", "source", "received_at", "battery_v", "distance_cm", "ir_left", "ir_right", "pwm_left", "pwm_right")
        with self.connection() as db:
            cursor = db.execute(
                "INSERT INTO telemetry (robot_id,source,received_at,battery_v,distance_cm,ir_left,ir_right,pwm_left,pwm_right) VALUES (?,?,?,?,?,?,?,?,?)",
                tuple(record.get(key) for key in columns),
            )
            row = db.execute("SELECT * FROM telemetry WHERE id=?", (cursor.lastrowid,)).fetchone()
            return self.record(row)

    def history(self, source: str, limit: int) -> dict:
        with self.connection() as db:
            total = db.execute("SELECT COUNT(*) FROM telemetry WHERE source=?", (source,)).fetchone()[0]
            rows = db.execute("SELECT * FROM telemetry WHERE source=? ORDER BY id DESC LIMIT ?", (source, limit)).fetchall()
            return {"items": [self.record(row) for row in rows], "total": total}

    def device_state(self, device_id: str) -> tuple[str | None, int]:
        with self.connection() as db:
            row = db.execute(
                "SELECT received_at FROM telemetry WHERE source='device' AND robot_id=? ORDER BY id DESC LIMIT 1", (device_id,)
            ).fetchone()
            count = db.execute("SELECT COUNT(*) FROM telemetry").fetchone()[0]
            return (row[0] if row else None, count)

    def event(self, message: str, level: str = "info") -> None:
        with self.connection() as db:
            db.execute("INSERT INTO events(created_at,level,message) VALUES (?,?,?)", (utc_now(), level, message))

    def events(self, limit: int) -> dict:
        with self.connection() as db:
            rows = db.execute("SELECT * FROM events ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
            return {"items": [dict(row) for row in rows]}

    def healthy(self) -> bool:
        with self.connection() as db:
            return db.execute("SELECT COUNT(*) FROM telemetry").fetchone() is not None
