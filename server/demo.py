"""Fuente de datos sintéticos. No importa ni abre puertos de hardware."""

import asyncio
import logging
import math
import time

from .config import Settings
from .database import Store

logger = logging.getLogger(__name__)


class Demo:
    def __init__(self, store: Store, settings: Settings):
        self.store = store
        self.settings = settings
        self._task: asyncio.Task | None = None
        self._stop = asyncio.Event()
        self._lock = asyncio.Lock()

    @property
    def running(self) -> bool:
        return self._task is not None and not self._task.done()

    async def start(self) -> bool:
        async with self._lock:
            if not self.running:
                self._stop = asyncio.Event()
                await asyncio.to_thread(self.store.event, "Simulación iniciada; no controla el robot físico.")
                self._task = asyncio.create_task(self._run(), name="robot-demo")
            return self.running

    async def stop(self) -> bool:
        async with self._lock:
            if self.running:
                self._stop.set()
                await self._task
            self._task = None
            return False

    async def _run(self) -> None:
        started = time.monotonic()
        try:
            while not self._stop.is_set():
                elapsed = time.monotonic() - started
                if elapsed >= self.settings.demo_max_seconds:
                    break
                sample = {
                    "robot_id": "sim-01",
                    "battery_v": round(6.02 - 0.10 * math.sin(elapsed / 18), 2),
                    "distance_cm": round(75 + 40 * math.sin(elapsed / 7), 1),
                    "ir_left": elapsed % 18 < 2,
                    "ir_right": 9 < elapsed % 18 < 11,
                    "pwm_left": 0,
                    "pwm_right": 0,
                }
                await asyncio.to_thread(self.store.add_sample, sample, "demo")
                try:
                    await asyncio.wait_for(self._stop.wait(), timeout=self.settings.demo_interval_seconds)
                except TimeoutError:
                    pass
            await asyncio.to_thread(self.store.event, "Simulación detenida. El historial queda guardado.")
        except Exception:
            logger.exception("La fuente de simulación se detuvo por un error")
            try:
                await asyncio.to_thread(self.store.event, "Error en la simulación. Consultá el registro del servidor.", "error")
            except Exception:
                logger.exception("No se pudo registrar el error de simulación")
