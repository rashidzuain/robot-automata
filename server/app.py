"""API y panel del servidor local. Ejecutar con python -m server."""

import asyncio
import logging
import math
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.trustedhost import TrustedHostMiddleware

from .config import Settings
from .database import Store
from .demo import Demo
from .models import DemoState, EmptyRequest, Source, TelemetryHistory, TelemetryInput, TelemetryRecord

VERSION = "0.1.0"
STATIC = Path(__file__).parent / "static"
logger = logging.getLogger(__name__)


def create_app(settings: Settings | None = None) -> FastAPI:
    config = settings or Settings()
    store = Store(config.database_path)
    demo = Demo(store, config)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await asyncio.to_thread(store.initialize)
        await asyncio.to_thread(store.event, "Servidor local iniciado. Esperando telemetría del robot.")
        logger.info("Base de datos: %s", config.database_path)
        try:
            yield
        finally:
            await demo.stop()
            await asyncio.to_thread(store.event, "Servidor detenido.")

    app = FastAPI(
        title="Robot Automata · servidor local",
        description="Telemetría persistente y simulación separada. Esta versión no envía órdenes a motores.",
        version=VERSION,
        lifespan=lifespan,
    )
    app.state.store = store
    app.state.demo = demo
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "127.0.0.1", "[::1]", "testserver"])

    @app.exception_handler(RequestValidationError)
    async def invalid_input(request: Request, exc: RequestValidationError):
        # Un NaN rechazado no debe romper a su vez la serialización del error 422.
        def safe(value):
            if isinstance(value, float) and not math.isfinite(value):
                return str(value)
            if isinstance(value, Exception):
                return str(value)
            if isinstance(value, dict):
                return {key: safe(item) for key, item in value.items()}
            if isinstance(value, (list, tuple)):
                return [safe(item) for item in value]
            return value
        return JSONResponse({"detail": safe(exc.errors())}, status_code=422)

    @app.middleware("http")
    async def local_browser_boundary(request: Request, call_next):
        if request.method not in {"GET", "HEAD", "OPTIONS"}:
            origin = request.headers.get("origin")
            expected = f"{request.url.scheme}://{request.headers.get('host', '')}"
            if (origin is not None and origin != expected) or request.headers.get("sec-fetch-site") == "cross-site":
                return JSONResponse({"detail": "Este servidor acepta cambios desde su propio panel local."}, status_code=403)
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        if request.url.path.startswith("/api/"):
            response.headers["Cache-Control"] = "no-store"
        return response

    @app.get("/healthz", tags=["Servidor"])
    def health():
        return {"status": "ok" if store.healthy() else "error", "version": VERSION}

    @app.get("/api/v1/status", tags=["Servidor"])
    def status():
        last_seen, sample_count = store.device_state(config.device_id)
        age = (datetime.now(timezone.utc) - datetime.fromisoformat(last_seen)).total_seconds() if last_seen else None
        return {
            "server": "online", "version": VERSION, "demo_running": demo.running,
            "device": {"robot_id": config.device_id, "connected": age is not None and 0 <= age < config.stale_after_seconds, "last_seen_at": last_seen},
            "active_source": "demo" if demo.running else "device", "sample_count": sample_count,
        }

    @app.post("/api/v1/telemetry", response_model=TelemetryRecord, status_code=201, tags=["Telemetría"])
    def receive_telemetry(sample: TelemetryInput):
        # El origen se asigna aquí: el cliente no puede presentarse como simulador.
        return store.add_sample(sample.model_dump(), "device")

    @app.get("/api/v1/telemetry", response_model=TelemetryHistory, tags=["Telemetría"])
    def telemetry(source: Source = "device", limit: int = Query(default=60, ge=1, le=500)):
        return store.history(source, limit)

    @app.get("/api/v1/events", tags=["Servidor"])
    def events(limit: int = Query(default=10, ge=1, le=100)):
        return store.events(limit)

    @app.post("/api/v1/demo/start", response_model=DemoState, tags=["Simulación"])
    async def start_demo(body: EmptyRequest):
        return {"running": await demo.start()}

    @app.post("/api/v1/demo/stop", response_model=DemoState, tags=["Simulación"])
    async def stop_demo(body: EmptyRequest):
        return {"running": await demo.stop()}

    @app.get("/", include_in_schema=False)
    def dashboard():
        return FileResponse(STATIC / "index.html")

    app.mount("/static", StaticFiles(directory=STATIC, check_dir=False), name="static")
    return app


app = create_app()
