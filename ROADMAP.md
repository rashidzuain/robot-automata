# Hoja de ruta

1. **En curso:** resolver el ensayo de un motor y verificar control/parada local.
2. **Implementado y verificado:** servidor local aislado con telemetría, historial, panel y simulación; 32 pruebas aprobadas. Cierre/reinicio real, persistencia, recuperación del panel y controles de simulación comprobados; revisión visual completada en el navegador integrado (E006).
3. Integrar un sensor y un adaptador de telemetría, primero sin órdenes de movimiento.
4. Confirmar comunicación, frescura de muestras y fallos de enlace.
5. Integrar control remoto con confirmaciones y vencimiento local, después de validar motores/alimentación.
6. Incorporar ESP32-CAM y adquisición de imágenes.
7. Visión clásica y navegación, guiadas por experimentos y necesidades medidas.

El servidor no modifica el estado pendiente del ensayo eléctrico. Para avanzar a órdenes físicas se requieren motor probado, protocolo acordado y parada autónoma del Arduino verificada.
