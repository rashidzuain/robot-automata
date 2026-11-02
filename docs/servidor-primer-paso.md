# Primera práctica con el servidor

## Objetivo

Separar adquisición, almacenamiento y presentación. Una API es el punto donde otro programa entrega o consulta información mediante un contrato. SQLite guarda las muestras para que sobrevivan al cierre del servidor. El panel consulta esa API y presenta los resultados.

## Probar por partes

1. Abrir el panel. El servidor debe responder y el robot físico aparecer sin conexión.
2. Iniciar la simulación. Ver la etiqueta de simulación, las lecturas y el historial creciendo.
3. Cambiar a Robot real: las muestras del simulador no deben aparecer allí.
4. Volver a simulación y detenerla. El historial se conserva y no llegan muestras nuevas.
5. Detener y arrancar el servidor. El historial debe continuar disponible; la simulación no debe arrancar sola.

Las pruebas automatizadas hacen también estas comprobaciones con una base temporal, además de rechazar entradas inválidas y comprobar cuándo una lectura queda antigua.

## Si algo falla

| Síntoma | Comprobación |
|---|---|
| El navegador no abre el panel | Iniciar el servidor y comprobar puerto/dirección de la consola |
| Puerto 8000 ocupado | Abrir el panel existente o arrancar con `--port 8001` |
| Panel indica interrupción | Verificar que el proceso siga vivo; el panel reintenta consultar |
| No aparecen lecturas reales | Es el estado esperado hasta integrar un emisor físico; usar simulación para probar |
| Respuesta 422 | Comparar campos, tipos y rangos con PROTOCOL.md |
| Respuesta 403 | Abrir el panel en el mismo origen que la API; no hacer peticiones desde otro sitio |
| Error SQLite | Revisar ubicación de la base, permisos y registros del proceso |

## Qué aprendiste

- Diferenciar una API, un servidor que la ejecuta y el navegador que la consulta.
- Persistir registros y distinguir la última muestra del historial completo.
- Usar `null` para desconocido y separar datos reales de sintéticos.
- Distinguir disponibilidad del servidor, recepción reciente de telemetría y funcionamiento físico del robot.

## Conceptos para explicar

HTTP/JSON, validación de entrada, contrato versionado, UTC, SQLite, ciclo de vida, prueba de integración y datos antiguos.

## Preguntas de entrevista

- ¿Por qué recibir un HTTP 200 no prueba que un motor esté funcionando?
- ¿Por qué la parada de seguridad debe quedar en el microcontrolador?
- ¿Por qué separar la hora de recepción de la futura hora de medición del robot?
- ¿Qué cambiarías antes de permitir acceso por Wi-Fi desde otros dispositivos?

## Desafío pequeño

Explicá qué debería mostrar cada tarjeta si el sensor deja de enviar datos, si informa cero y si informa `null`. Después localizá en `server/models.py` qué regla rechaza una batería con tensión negativa.
