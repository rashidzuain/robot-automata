# Robot Automata

Laboratorio personal de robótica: Arduino UNO para control local, ESP32-CAM para futura conectividad/cámara y una computadora para datos y procesamiento.

## Servidor local disponible

Abrí **http://127.0.0.1:8000** cuando esté iniciado. Para arrancarlo en Windows, hacé doble clic en **Iniciar servidor.cmd**. Para detenerlo, usá **Detener servidor.cmd** o **Ctrl+C** en la ventana donde lo iniciaste. Si ya hay un servidor en ese puerto, usá el que está abierto y evitá iniciar otro.

Esta primera versión incluye:

- API que recibe y valida telemetría.
- Historial y eventos guardados en SQLite.
- Panel con tensión de batería, distancia, lecturas IR e historial.
- Actualización del panel aproximadamente cada segundo.
- Simulación que se inicia y detiene a pedido, separada de los datos del robot. Se detiene automáticamente a los 15 minutos y al cerrar el servidor; nunca se reanuda sola.
- Documentación interactiva de la API en **http://127.0.0.1:8000/docs**.

El robot físico aún no transmite datos. El programa actual del UNO es una prueba de motor por caracteres seriales, no el protocolo de telemetría de este servidor. Esta versión **no abre puertos serie ni envía órdenes a motores**. El ensayo físico del motor sigue pendiente.

## Instalar en otra computadora o recrear el entorno

Python 3.11 o posterior; la instalación actual usa Python 3.12.1.

Windows, desde la carpeta del proyecto:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r server\requirements.lock.txt
.\.venv\Scripts\python.exe -m server
```

Linux:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r server/requirements.lock.txt
.venv/bin/python -m server
```

El archivo de versiones fijadas reproduce el entorno comprobado, incluidas las herramientas de prueba. `requirements.txt` y `requirements-dev.txt` expresan las dependencias directas para actualizaciones futuras.

Para usar otro puerto: `python -m server --port 8001`, usando el Python de `.venv`; para pedir su cierre: `python -m server --port 8001 --stop`. El cierre por archivo de control solo corresponde al mismo proyecto y puerto; no termina otros programas. El servidor escucha únicamente en **127.0.0.1**: funciona en esta computadora. No se configuraron arranque automático, acceso desde Internet, firewall ni acceso desde otros equipos.

## Datos y configuración

Por defecto, la base está fuera de OneDrive para evitar sincronizar un archivo SQLite mientras se está escribiendo:

- Windows: `%LOCALAPPDATA%\RobotAutomata\robot.sqlite3`.
- Linux: `${XDG_DATA_HOME:-~/.local/share}/RobotAutomata/robot.sqlite3`.

Se puede elegir otra ubicación con la variable **ROBOT_DB_PATH** antes de iniciar. Para una copia manual, detener primero el servidor y copiar la base y los archivos auxiliares que sigan presentes, o utilizar la API de backup de SQLite. Copiar solamente el archivo principal durante una escritura puede omitir datos del WAL.

Los registros reales y los de simulación se distinguen por `source`, además de usar identificadores diferentes. No se borran al detener una simulación. El historial de esta versión no tiene borrado automático: habrá que definir retención antes de una operación continua prolongada.

## Probar

```powershell
.\.venv\Scripts\python.exe -m pytest server\tests -q
```

Las pruebas usan bases temporales y no necesitan Arduino ni alteran la base del panel. En el navegador, **Iniciar simulación** permite ver el flujo completo; **Detener simulación** conserva el historial. En **Robot real**, no deben aparecer esos datos sintéticos.

## Estructura

```text
server/
  app.py          API y ciclo de vida
  models.py       Contrato y validación
  database.py     Persistencia SQLite
  demo.py         Fuente sintética independiente
  config.py       Configuración
  static/         Panel web
  tests/          Pruebas del servidor
firmware/arduino/motor_bench/  Prueba física actual
diagramas/        Conexiones de 1, 2 y 4 motores
docs/             Guías de aprendizaje
```

Leé **ARCHITECTURE.md** para entender las decisiones, **PROTOCOL.md** para enviar datos y **docs/servidor-primer-paso.md** para la práctica guiada. **HARDWARE.md** y **EXPERIMENTS.md** conservan las observaciones del montaje físico.
