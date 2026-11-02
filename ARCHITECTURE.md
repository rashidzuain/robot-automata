# Arquitectura vigente

## Decisión del 8 de octubre de 2026

Crear el primer servidor local en la computadora actual, de forma independiente del diagnóstico eléctrico. El usuario eligió esta computadora; moverlo a la Acer será un trabajo posterior.

```text
Cliente de telemetría (futuro Arduino/ESP32 o puente serial)
        ↓ HTTP / JSON, protocolo v1
API FastAPI → validación → SQLite
        ↑ consultas cada segundo
Panel web del navegador

Simulador interno → mismo almacenamiento, source=demo
```

La línea del cliente físico es una interfaz preparada, no una conexión ya realizada. Hoy se puede probar toda la parte de servidor con el simulador, sin depender de motores o sensores.

## Responsabilidades

- **UNO:** conservará las tareas locales de movimiento y parada. El servidor no debe convertirse en el mecanismo que garantiza detener los motores a tiempo.
- **ESP32:** futura conectividad y cámara; todavía no se integra.
- **Servidor:** validar muestras, asignar hora UTC de recepción, persistir, exponer estado e historial y servir el panel.
- **Navegador:** consultar y mostrar datos, con etiqueta explícita del origen. No calcula porcentajes de batería a partir de una tensión sin modelo de descarga.

## Elecciones mínimas

- **Python/FastAPI:** tipos y validación del contrato, API documentada y pruebas del servicio. El ciclo de vida inicializa la base y cierra la simulación.
- **SQLite:** una base local sin administrar otro servicio. Conexiones cortas por operación, consultas parametrizadas e índice por origen/ID. La base activa se guarda fuera de OneDrive.
- **HTTP consultado cada segundo:** suficiente para la telemetría inicial, sin introducir todavía un broker o un protocolo de conexión persistente.
- **Panel HTML/CSS/JavaScript local:** sin compilación ni dependencia de recursos externos para el panel. La interfaz `/docs` de FastAPI puede cargar recursos de su CDN.

Referencias: [ciclo de vida de FastAPI](https://fastapi.tiangolo.com/advanced/events/), [sqlite3 de Python](https://docs.python.org/3/library/sqlite3.html).

## Límites de esta etapa

Un solo proceso del servidor y un robot físico (`robot-01`), más `sim-01`. La simulación es manual, dura como máximo 15 minutos y no arranca con el servidor. Los datos sintéticos nunca actualizan la conexión del robot físico.

“Conectado” significa **telemetría real recibida hace menos de cinco segundos**; no demuestra que haya USB conectado ni que el motor funcione. Las muestras conservan la hora de recepción del servidor. La sincronización del reloj del robot, secuencias y detección de paquetes repetidos quedan para la integración del transporte.

No hay autenticación de usuarios en esta primera versión local. Se escucha solo en loopback, se validan los nombres de host y se rechazan cambios de origen web ajeno. No publicar en la red ni cambiar el enlace a 0.0.0.0 sin diseñar acceso, autenticación y comunicaciones del dispositivo.

El protocolo serial existente (`a`, `f`, `r`, `s`) todavía no se usa desde el servidor. Incorporar primero un adaptador de lectura y probarlo por separado; habilitar órdenes físicas después de resolver el ensayo del motor, acordar el protocolo de confirmaciones y verificar parada local.
