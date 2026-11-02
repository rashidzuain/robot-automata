"""Entrada deliberadamente local: no publica el robot en la red."""

import argparse
import asyncio
from contextlib import suppress
import logging
from pathlib import Path
import uuid

import uvicorn

parser = argparse.ArgumentParser(description="Servidor local de Robot Automata")
parser.add_argument("--port", type=int, default=8000, help="Puerto local (por defecto: 8000)")
parser.add_argument("--stop", action="store_true", help="Pedir el cierre del servidor de este proyecto y puerto")
args = parser.parse_args()
if not 1 <= args.port <= 65535:
    parser.error("El puerto debe estar entre 1 y 65535")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
runtime = Path(__file__).resolve().parent.parent / ".runtime"
runtime.mkdir(exist_ok=True)
stop_file = runtime / f"stop-{args.port}.request"


def stop_marker() -> str:
    try:
        return stop_file.read_text(encoding="ascii")
    except FileNotFoundError:
        return ""


async def serve() -> None:
    initial_marker = stop_marker()
    server = uvicorn.Server(uvicorn.Config("server.app:app", host="127.0.0.1", port=args.port, workers=1, access_log=False))

    async def watch_stop():
        while not server.should_exit:
            await asyncio.sleep(0.5)
            if stop_marker() != initial_marker:
                server.should_exit = True

    watcher = asyncio.create_task(watch_stop())
    try:
        await server.serve()
    finally:
        watcher.cancel()
        with suppress(asyncio.CancelledError):
            await watcher


if args.stop:
    pending = stop_file.with_suffix(".tmp")
    pending.write_text(uuid.uuid4().hex, encoding="ascii")
    pending.replace(stop_file)
    print(f"Solicitud de cierre enviada al servidor de este proyecto en el puerto {args.port}.")
else:
    asyncio.run(serve())
