# Diagramas de conexiones — 8 de octubre de 2026

Los dibujos agrupan y reubican conectores para facilitar la lectura. No son plantillas a escala de las placas: seguir siempre las etiquetas reales. Los colores representan conexiones; no obligan a usar cables de ese color.

## Archivos

- `diagrama-1-motor.png`: alimentación, señales del canal A y salida a un motor.
- `diagrama-2-motores.png`: un motor por canal; ampliación propuesta.
- `diagrama-4-motores.png`: dos motores en paralelo por lado; conexión conceptual pendiente de validar eléctricamente.
- `dibujo-montaje-un-motor.png` y `.svg`: dibujo completo del montaje actual.

## Alimentación común a las tres vistas

| Origen | Destino |
|---|---|
| USB de laptop | USB del Arduino UNO |
| 5V del UNO | Borne +5V del L298N |
| GND del UNO | Borne GND del L298N |
| Positivo del portapilas de cuatro AA alcalinas | Borne 12V del L298N |
| Negativo del portapilas | Mismo borne GND del L298N |

El borne llamado 12V recibe el pack de aproximadamente 6 V; la etiqueta no indica que estos motores deban alimentarse con 12 V. El puente 5V-EN del regulador queda retirado al alimentar la lógica desde el UNO. La corriente de los motores circula por el portapilas y el driver, sin pasar por 5V del UNO ni por la protoboard.

Preparar conexiones con USB y pilas desconectados. Para el ensayo de un motor, energizar primero la lógica por USB y después las pilas; retirar primero las pilas al terminar. Ruedas levantadas.

## Un motor: programa actual

- D5 → señal ENA.
- D7 → IN1.
- D8 → IN2.
- Resistencia R1 de 10 kΩ entre ENA y GND.
- Un único motor entre OUT1 y OUT2. OUT3/OUT4 quedan sin motores.
- Puente ENA retirado. El pin vecino de +5V del puente queda libre.

En el módulo inspeccionado, las mediciones del usuario son compatibles con ENA de señal hacia el borde y el pin +5V hacia el centro. Esta orientación no se debe generalizar a otra placa. El pin de señal ENB aún no está identificado mediante medición.

Unión de protoboard: ENA→a10, D5→b10, una pata de R1→c10 y la otra→c15, GND del UNO→a15. Los agujeros a–e de cada fila están unidos. Solo se insertan las dos patas de la resistencia; su cuerpo no conecta agujeros intermedios.

## Dos motores: ampliación propuesta

Mantener canal A y añadir:

- D6 → señal ENB, con puente ENB retirado.
- D9 → IN3.
- D10 → IN4.
- Segunda resistencia R2 de 10 kΩ entre ENB y GND.
- Segundo motor entre OUT3 y OUT4.

El usuario solo confirmó disponer de una resistencia. Hace falta verificar una segunda y adaptar el programa para ambos canales; el firmware actual utiliza únicamente D5/D7/D8. No se cambió el firmware al crear estos dibujos.

## Cuatro motores: dos por lado

- Izquierda: delantero y trasero en paralelo entre OUT1 y OUT2.
- Derecha: delantero y trasero en paralelo entre OUT3 y OUT4.
- Cada motor se conecta a las dos salidas de su canal, nunca a GND. No unir salidas A y B.
- Los dos motores de cada lado deben impulsar el robot en el mismo sentido. La orientación mecánica puede exigir intercambiar los dos cables de uno de ellos; verificar cada motor antes de agruparlos.
- El control sigue siendo por dos lados, no por cuatro ruedas independientes.

Este esquema muestra la topología; todavía no autoriza ensayar cuatro motores. La corriente de arranque/bloqueo de los TT, la capacidad del portapilas bajo carga y la disipación del módulo siguen sin verificar. Las corrientes de dos motores en paralelo se suman. El máximo del chip no garantiza esa capacidad continua en el módulo comercial. No aumentar tensión para compensar la caída del L298N sin evaluar motores y corriente.

## Estado del diagnóstico

Lecturas informadas por el usuario con el cableado actual: lógica +5V = 5,00 V; entrada 12V = 6,03 V en reposo; ENA en reposo = −0,01 V. El monitor serie muestra aceptación y finalización del pulso. El motor aún no se movió. Estas lecturas no confirman las señales durante el pulso ni la alimentación bajo carga. Las mediciones en reposo de IN1/IN2 siguen pendientes.

## Referencias y comprobación

- [Handson Technology: módulo L298N, conectores y alimentación externa de lógica](https://handsontec.com/dataspecs/module/L298N%20Motor%20Driver.pdf).
- [STMicroelectronics: L298, dos canales y límites eléctricos](https://www.st.com/resource/en/datasheet/l298.pdf).

Se revisó el trazado de conexiones y se renderizaron las tres vistas. Se comprobó que las etiquetas caben a anchos de 320, 360 y 736 píxeles y que el selector cambia entre 1, 2 y 4 motores sin errores de JavaScript. Esto comprueba los dibujos, no el montaje físico.
