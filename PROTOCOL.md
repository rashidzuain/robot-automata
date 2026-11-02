# Protocolo del servidor v1

Base local: `http://127.0.0.1:8000`. JSON UTF-8. Las escrituras requieren cuerpo JSON; no se permite que otro sitio web dirija cambios al panel. Esta etapa no expone el servicio a la red.

## Recibir una muestra

`POST /api/v1/telemetry` con `Content-Type: application/json`:

```json
{
  "robot_id": "robot-01",
  "battery_v": 6.03,
  "distance_cm": 42.5,
  "ir_left": false,
  "ir_right": true,
  "pwm_left": 0,
  "pwm_right": 0
}
```

**Este JSON es un ejemplo**, no una medición realizada. Para probar con datos sintéticos en el panel usar el simulador, que los etiqueta como tales. Enviar el ejemplo al endpoint de ingesta se registra como dato del dispositivo y altera su indicador de conexión.

Los únicos campos son los del ejemplo. Al menos una medición/orden debe ser distinta de `null`. Se puede omitir el resto. Campos desconocidos y el campo `source` se rechazan; el servidor asigna el origen `device` y la hora `received_at` en UTC. También devuelve `id` numérico. Respuesta correcta: **201**. Datos inválidos: **422**.

| Campo | Significado / rango |
|---|---|
| robot_id | `robot-01`; se utiliza por defecto si se omite |
| battery_v | Tensión medida del pack, 0–20 V; `null` si no hay lectura |
| distance_cm | Distancia medida, 0–1000 cm; `null` si no hay lectura |
| ir_left / ir_right | Detección lógica booleana o `null`; su interpretación se calibrará con el sensor real |
| pwm_left / pwm_right | Orden registrada por el dispositivo, −255 a 255; no es velocidad medida ni orden para el servidor |

Los límites son validaciones del formato de datos, no límites eléctricos admisibles del motor. No se aceptan NaN o infinito. Cero es un valor informado; no reemplaza datos ausentes.

## Consultas

- `GET /healthz`: salud de la API y consulta de la base.
- `GET /api/v1/status`: servidor, estado de simulación, conexión del robot físico y conteo total.
- `GET /api/v1/telemetry?source=device&limit=60`: historial real, más reciente primero; `source=demo` para simulación. Límite entre 1 y 500; devuelve `items` y `total` de ese origen.
- `GET /api/v1/events?limit=10`: eventos recientes. Límite 1–100.
- `GET /openapi.json`: definición verificable del contrato.

## Simulación

- `POST /api/v1/demo/start`, cuerpo `{}`: inicia una sola tarea de generación. Repetirlo no crea otra.
- `POST /api/v1/demo/stop`, cuerpo `{}`: espera a que la tarea termine; mantiene las muestras guardadas.
- Ambas respuestas: `{"running": true}` o `{"running": false}` según corresponda.

El simulador utiliza `robot_id=sim-01` y `source=demo`. No abre comunicaciones físicas. En esta versión no hay endpoint para accionar motores.
