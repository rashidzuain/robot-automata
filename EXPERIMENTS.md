# Registro de experimentos

## E001 — Tensión en vacío de las pilas

Fecha de preparación: 2026-10-07.

Estado: **mediciones individuales y del portapilas registradas; usuario confirma que las cuatro DIA son nuevas**. Capacidad bajo carga y alimentación de lógica pendientes.

### Objetivo

Aprender a medir tensión continua, verificar polaridad y registrar el estado inicial de cada pila. La medida en vacío no determina la capacidad restante ni garantiza que la pila pueda alimentar motores.

### Material disponible

- Multímetro DT-830D y dos puntas.
- Cuatro pilas DIA AA alcalinas, marcadas 1,5 V; la cuarta fue aportada después del inventario fotográfico inicial.
- Una pila Jaiho R6 AA carbón-zinc, marcada 1,5 V.

El conjunto original mezclaba químicas. La Jaiho queda fuera del conjunto de tracción. Las cuatro DIA coinciden en marca, tamaño, química y tensión nominal declarados; el usuario confirmó que las cuatro son nuevas. La capacidad bajo carga todavía no se ha evaluado.

### Procedimiento

1. Desconectar el portapilas del controlador y retirar las cuatro pilas. Mantener Arduino y otros circuitos sin conexión al portapilas.
2. Identificar las pilas como DIA 1, DIA 2, DIA 3 y DIA 4; registrar la Jaiho por separado.
3. Con las puntas sin tocar ningún circuito, colocar cable negro en COM, puerto inferior; rojo en VΩmA, puerto central. Dejar libre el puerto superior 10 A. En la foto recibida los colores están intercambiados.
4. Colocar selector en 20, dentro del sector de tensión continua V⎓, situado arriba a la izquierda. El rango permite medir hasta aproximadamente 20 V; la pila no tiene que medir 20 V.
5. Para cada pila, apoyar punta negra sobre el extremo negativo y roja sobre el positivo. Evitar que las puntas unan ambos polos o contacten objetos metálicos. Leer el valor estable y anotarlo.
6. Si aparece signo negativo, revisar polaridad de contacto y posición de los cables. Si la pantalla queda apagada, comprobar primero selector y batería interna del multímetro.
7. Apagar el multímetro al terminar y conservar el portapilas desconectado.

Para este ejercicio no se usa el sector A ni el puerto 10 A. Medir corriente requiere otra conexión; poner el amperímetro entre los dos polos de una pila puede producir un cortocircuito. No medir resistencia o continuidad sobre el circuito alimentado.

### Resultados

| Identificador | Marca / química | Tensión medida (V) | Observaciones |
|---|---|---|---|
| DIA 1 | DIA / alcalina | 1,48 | Informado por el usuario |
| DIA 2 | DIA / alcalina | 1,48 | Informado por el usuario |
| DIA 3 | DIA / alcalina | 1,60 | Diferencia de 0,12 V respecto del mínimo; usuario confirma que es nueva, como las otras tres |
| DIA 4 | DIA / alcalina | 1,49 | Informado por el usuario |
| Jaiho | Jaiho / carbón-zinc | 1,27 | Fuera del conjunto de tracción |

Suma de las cuatro DIA: **6,05 V**. Es una estimación de tensión en vacío para cuatro celdas en serie, no una medición del portapilas ni una garantía de alimentación bajo carga. Las tres lecturas entre 1,48 y 1,49 V son próximas. El usuario confirmó que las cuatro son nuevas: no se atribuye la lectura de 1,60 V a menor uso que las otras tres.

El usuario informó primero **5,96 V** y después corrigió la lectura a **6,4 V**, indicando que volvió a medir correctamente. Se conserva 5,96 V como lectura anterior, sustituida por la revisión; falta confirmar explícitamente que 6,4 V corresponde a la salida del portapilas desconectado. Respecto de la suma de lecturas individuales anteriores (6,05 V), la revisión difiere 0,35 V. Repetir las cuatro lecturas individuales con la misma configuración si se necesita reconciliar resultados. No atribuir la diferencia a una causa concreta ni estimar resistencia de contactos sin otras mediciones. El usuario confirmó que las cuatro DIA son nuevas; no se ha medido bajo carga.

La marca 1,5 V expresa tensión nominal. La tensión medida depende del estado de la pila y no tiene que coincidir exactamente con ese valor. No se fija un umbral universal de aprobación para motores con una lectura en vacío.

### Criterio de finalización

- Cinco valores individuales y tensión del portapilas registrados; cuatro DIA nuevas confirmadas por el usuario.
- El usuario puede explicar qué significa el rango 20 V y por qué una lectura en vacío no demuestra capacidad bajo carga.
- El conjunto mezclado queda fuera de los ensayos de tracción.

### Siguiente experimento, después de revisar resultados

La medición del portapilas ya está registrada. El siguiente ensayo verifica alimentación de lógica, etiquetas y puentes del controlador antes de conectar Arduino. Primero identificar inequívocamente GND y 5 V y confirmar configuración del regulador. Desconectar motores antes de energizar el módulo para medir: los puentes de habilitación y entradas abiertas podrían permitir movimiento indeseado. No modificar puentes con alimentación presente ni medir por posiciones supuestas. La corriente de motores y la capacidad del driver siguen pendientes de identificación.

### Fuente

[Fluke: cómo medir tensión continua](https://www.fluke.com/en-us/learn/blog/digital-multimeters/how-to-measure-dc-voltage-with-a-digital-multimeter).

## E002 — Entrada y tensión de lógica del controlador

Estado: **ejecutado por el usuario; mediciones registradas**.

### Objetivo

Comprobar la tensión que llega al módulo y qué tensión obtiene su circuito de lógica con el portapilas actual. Las nuevas fotos permiten leer las etiquetas 12V, GND y +5V en el reverso. El código del chip de potencia sigue oculto, pero formato y topología coinciden con módulos L298N comunes.

### Preparación y procedimiento

1. Desconectar el portapilas. Mantener Arduino y ESP32 desconectados.
2. Fotografiar y marcar los grupos de cables en las dos borneras laterales de motores; retirarlos de esas borneras y aislar sus extremos. Esto impide movimiento mientras se prueba la electrónica, cuyas entradas no tienen aún control definido.
3. Mantener los puentes tal como aparecen en la foto. El puente próximo al regulador está instalado; no conectar una fuente externa al terminal +5V durante esta prueba.
4. Apoyar y sujetar el módulo sobre superficie aislante. No manipularlo energizado ni apoyar puntas en el reverso donde puedan unir soldaduras.
5. Identificar los tres terminales por las etiquetas. En la orientación de la foto frontal recibida —disipador arriba, bornera de tres tornillos abajo— corresponden a 12V, GND y +5V de izquierda a derecha. Guiarse por etiquetas, no por posición si se gira la placa.
6. Con alimentación aún desconectada, conectar positivo del portapilas al terminal 12V y negativo a GND. Dejar +5V sin cable. La etiqueta 12V es el nombre de la entrada de potencia de este módulo; este ensayo usa el pack de aproximadamente 6,4 V, no una fuente de 12 V.
7. Verificar que los conductores estén sujetos y que no haya hilos sueltos. Configurar DT-830D en 20 V⎓, negro en COM y rojo en VΩmA, con 10 A libre.
8. Energizar desde el portapilas. Medir primero entre GND (negro) y 12V (rojo); luego entre GND (negro) y +5V (rojo). Evitar que las puntas puenteen tornillos contiguos.
9. Anotar ambas lecturas y desconectar el portapilas al terminar. No conectar Arduino ni motores hasta revisar resultados.

### Resultados

| Medida | Resultado (V) |
|---|---|
| Entrada 12V respecto de GND | 5,95 |
| Terminal +5V respecto de GND | 4,55 |

### Interpretación

Con entrada de 5,95 V, el terminal de lógica midió 4,55 V. El resultado es compatible con falta de margen de entrada del regulador; no demuestra por sí solo un regulador averiado. Para un L298, la hoja de datos indica 4,5 V como mínimo de alimentación de lógica: la medida queda solo 0,05 V por encima, sin considerar incertidumbre del multímetro ni futuras caídas. No se acepta esta configuración como alimentación de lógica confiable para integrar motores. Un LED encendido no acredita regulación correcta. Este ensayo no demuestra estabilidad bajo carga de motores ni capacidad térmica del módulo.

Decisión de banco: alimentar la lógica desde el pin 5 V del Arduino alimentado por USB, retirando previamente el puente del regulador del módulo. Las pilas seguirán destinadas a la etapa de potencia en el ensayo posterior; no alimentar motores desde Arduino. La diferencia entre 6,4 V revisados anteriormente y 5,95 V actuales no se atribuye a una causa concreta sin medidas consecutivas comparables.

### Referencias

- [Handson Technology: módulo L298N, esquema y regulador](https://handsontec.com/dataspecs/module/L298N%20Motor%20Driver.pdf).
- [STMicroelectronics: alimentación de lógica y potencia del L298](https://www.st.com/resource/en/datasheet/l298.pdf).

## E003 — Alimentación externa de lógica para pruebas de banco

Estado: **lectura de 5,00 V informada por el usuario tras el procedimiento de alimentación externa de lógica**. No se ha probado movimiento ni estabilidad bajo carga de motores.

### Objetivo

Verificar alimentación de lógica cercana a 5 V sin depender del regulador del módulo y del portapilas. Es una configuración temporal de banco con USB, no el diseño final autónomo.

### Procedimiento

1. Desconectar portapilas y USB. Mantener los motores retirados de sus borneras y los cables de control sin conectar a Arduino.
2. Retirar solamente el puente del regulador (5V-EN). En la foto frontal del 21.51.07 está colocado horizontalmente debajo del capacitor izquierdo, encima del lado izquierdo de la bornera de tres tornillos. No confundirlo con los dos puentes de habilitación de canales que flanquean el conector de cuatro cables. Si la posición real no coincide, detenerse y revisar la identificación.
3. Con todo sin alimentación, conectar pin 5V de Arduino al terminal +5V del módulo, y GND de Arduino al terminal GND del módulo. No usar VIN ni 3,3V y no conectar 5V de Arduino al terminal 12V.
4. Mantener el portapilas desconectado; energizar solo Arduino mediante USB.
5. En 20 V⎓, medir entre GND del módulo (negro) y +5V del módulo (rojo). Registrar la lectura y desconectar USB al terminar.

No inyectar 5 V externos con el puente del regulador colocado. Los motores no se alimentan desde USB/Arduino. La etapa de potencia del módulo permanece sin alimentación de pilas durante este ensayo; no se pretende mover nada.

### Resultado

| Medida | Resultado (V) |
|---|---|
| +5V del módulo respecto de GND con Arduino por USB | 5,00 |

Resultado: tensión de lógica nominal obtenida en esta condición de banco. El usuario adjuntó una anotación sobre el puente del regulador, sin comentario adicional; recordar que debe quedar retirado mientras se utiliza alimentación externa de 5 V. La lectura no confirma por sí sola la posición del puente ni estabilidad durante movimiento.

### Siguiente paso

Después de comprobar la tensión de lógica, revisar preparación del firmware, habilitación segura y un único motor. Antes de movimiento, conectar alimentación de potencia desde pilas y repetir ambas tensiones; comprobar límites del motor y el driver. No habilitar entradas flotantes con motores conectados.

### Referencias

- [Handson Technology: ejemplo de lógica alimentada desde Arduino con puente de regulador retirado](https://handsontec.com/dataspecs/module/L298N%20Motor%20Driver.pdf).
- [Arduino: documentación del Uno R3](https://docs.arduino.cc/resources/datasheets/A000066-datasheet.pdf).

## E004 — Programación y ejecución básica de Arduino

Estado: **completado según observación del usuario**.

El usuario cargó el ejemplo Blink desde Arduino IDE, informó carga completa y confirmó parpadeo del LED integrado L. La prueba se indicó con alimentación USB, portapilas y motores desconectados.

Resultado: comunicación de programación y ejecución del programa básico comprobadas. Esta prueba no verifica todavía control de motores ni tiempos de parada.

## Preparación del primer ensayo de un motor

Siguiente objetivo: un único motor, mecanismos suspendidos, orden explícita por USB, movimiento breve y parada local. No ejecutar movimiento automáticamente al encender.

Para evitar habilitación flotante durante reset del Uno, preparar una resistencia de 10 kΩ entre ENA y GND del controlador, retirar el puente ENA para controlar ese canal desde Arduino y mantener el canal no utilizado deshabilitado. La disponibilidad de resistencia apropiada y las etiquetas ENA/IN1/IN2 se confirman antes de energizar la tracción. Mantener retirado el puente del regulador 5V-EN al utilizar lógica externa desde Arduino.

Pinout propuesto para un canal: D5 (PWM) hacia ENA, D7 hacia IN1, D8 hacia IN2. Es una propuesta pendiente de comprobar etiquetas y preparar cableado, no una prueba ya realizada. Motor único entre OUT1 y OUT2. Alimentación de potencia desde portapilas; lógica desde Arduino USB, con GND común.

El usuario confirmó disponer de resistencia de 10 kΩ. Se preparó `firmware/arduino/motor_bench/motor_bench.ino`: arranque deshabilitado; habilitación explícita `a` con vigencia de 3 s; `f`/`r` producen un pulso de 250 ms con PWM 96/255; `s` detiene y deshabilita. Cada pulso requiere nueva habilitación y hay espera electrónica mínima de 1 s entre ensayos. Esta espera no mide detención física; comprobar que la rueda se detuvo antes de invertir. PWM no es un limitador de corriente.

Estado del firmware: el usuario confirmó carga en el Uno y la secuencia del Monitor serie: DESHABILITADO -> HABILITADO -> PULSO 250 ms -> PULSO TERMINADO / DESHABILITADO. Compilación realizada por el usuario mediante Arduino IDE; no se encontró compilador Arduino en el entorno de comandos del asistente. Motores y portapilas permanecían desconectados según el procedimiento. No se ha verificado todavía movimiento físico, corriente ni distancia/tiempo de parada.

Antes de alimentar el primer motor: confirmar su tensión nominal mediante inscripción, referencia del kit o ficha del vendedor; seleccionar un único motor para OUT1/OUT2 y sujetarlo con eje/rueda libres. Las pruebas seriales de STOP, vencimiento de habilitación y rechazo de movimiento sin habilitación aún deben registrarse; no se deducen de la prueba a/f.

## E005 — Primer pulso físico de un motor

Estado: **ensayo informado por el usuario: el motor no se movió; diagnóstico de conexiones pendiente**.

El usuario declara rango de alimentación de motores **3–6 V**. No se dispone todavía de referencia de fabricante ni corriente de bloqueo. El ensayo es corto, con un solo motor sin carga mecánica de desplazamiento; no valida el controlador para cuatro motores o funcionamiento prolongado.

Actualización: el usuario informó **que el motor no se movió** y aportó tres fotos del montaje del 23.29.27/41/49. No se confirmó todavía qué mensajes aparecieron durante ese intento, si zumbó o si hubo reinicios. No aumentar PWM ni duración antes de revisar conexiones.

Revisión prioritaria: en esta familia de módulos, al quitar ENA quedan dos pines del puente; uno es la alimentación +5 V y el otro la entrada ENA. La instrucción anterior no explicitó esta distinción. Identificar por esquema/continuidad con el módulo completamente desenergizado y aislado del Arduino antes de conectar D5 y la resistencia al pin de habilitación. Las fotos no permiten confirmar que esos cables estén en el pin correcto. Comprobar también D7->IN1, D8->IN2 y motor en OUT1/OUT2. Un PWM bajo y pulso corto también pueden no alcanzar para arrancar, pero no se atribuye aún el fallo a esa causa.

Procedimiento de identificación propuesto: retirar pilas y USB, aislar el módulo de las conexiones Arduino y dejar libres los dos pines del puente ENA. DT-830D en 200 Ω, negro en COM y rojo en VΩmA: medir cada pin respecto del terminal +5V del módulo. Una conexión directa cercana a 0 Ω identifica el pin de alimentación; no conectar D5 allí. El otro pin se contrasta con el esquema como entrada ENA. Registrar cuál es cercano al borde y cuál al disipador; si ambos parecen conectados directamente, detenerse y revisar si queda el puente u otra unión. No medir resistencia con alimentación presente.

El usuario informó: pin del puente ENA hacia el centro del módulo **0,7–0,8 Ω** respecto de +5V; pin hacia el borde **“1”**. La primera lectura identifica conexión directa a +5V, incluida resistencia de puntas/contactos. Si “1” es el indicador de fuera de escala a la izquierda en 200 Ω, el pin hacia el borde corresponde a la entrada ENA de esta topología; no interpretar ese indicador como 1 Ω. Con todo apagado, conectar D5 y la resistencia de 10 kΩ a GND en el pin hacia el borde y dejar libre el pin hacia el centro. No quedó confirmado en qué pin estaba D5 durante el ensayo fallido.

### Preparación

1. USB y pilas desconectados. Un único motor entre OUT1 y OUT2; los demás motores desconectados. Sujetar el montaje con rueda y disco libres; fijar módulo sobre superficie aislante, sin cables cerca de la rueda.
2. Verificar resistencia 10 kΩ de ENA a GND y señales D5->ENA, D7->IN1, D8->IN2. Puentes 5V-EN y ENA retirados; lógica +5V/GND desde Arduino. Mantener ESP32 y otros sensores fuera de este ensayo.
3. Conectar positivo del portapilas a 12V y negativo a GND del controlador. Esta misma GND ya debe estar conectada a GND de Arduino. Preparar conexiones con el portapilas sin pilas o su interruptor apagado; si no hay interruptor, terminar el montaje antes de insertar la última pila. No cambiar cables energizados.
4. Energizar Arduino por USB, abrir Monitor serie a 115200 y confirmar estado DESHABILITADO. Después energizar el portapilas. No tocar rueda ni disco.
5. Antes de mandar movimiento, medir +5V respecto de GND y entrada 12V respecto de GND. Esperar lógica cercana a los 5,00 V comprobados y entrada similar a medición actual del portapilas. Si hay variación importante de lógica o reinicios, desconectar pilas y registrar; no ejecutar movimiento.

### Ensayo mínimo

- Enviar f sin a: no debe girar.
- Enviar a y, dentro de tres segundos, f: PWM 96/255 durante 250 ms y desactivación automática.
- Si gira, esperar al menos cinco segundos y verificar detención física. Enviar a y luego r para probar el otro sentido.
- Si no gira o solo zumba, cortar alimentación de pilas y registrar. No aumentar PWM ni reiterar pulsos hasta revisar causa.
- Una orden s deshabilita el canal. La expiración deshabilita eléctricamente el puente; la rueda puede terminar de detenerse por inercia.
- Al finalizar, desconectar primero pilas y después USB. No ensayar inversiones mientras la rueda siga girando.

PWM 96/255 equivale aproximadamente a 38 % de ciclo útil, no a 38 % de velocidad, y no limita corriente. Este primer ensayo no mide regulación de velocidad ni demuestra los requisitos de latencia electrónica. La caída del puente y el ciclo útil pueden hacer que el primer pulso no alcance para arrancar: ese resultado debe diagnosticarse antes de cambiar parámetros.

### Resultados pendientes

| Observación | Resultado |
|---|---|
| Entrada 12V antes de movimiento | Pendiente |
| Lógica +5V antes de movimiento | Pendiente |
| f sin habilitación | Pendiente |
| Pulso a/f: gira y se desactiva | Pendiente |
| Pulso a/r tras detención | Pendiente |
| Reinicios, zumbido, calentamiento u otros problemas | Pendiente |

Para el primer envío de resultados se solicita primero a/f; no es necesario realizar toda la matriz si aparece un problema.

Siguiente acción física: con USB y pilas desconectados, retirar ENA y preparar D5->ENA, D7->IN1, D8->IN2 y resistencia de ENA a GND. Dejar motores y pilas desconectados para primera carga y prueba serial. Mantener 5V-EN retirado para lógica externa. Antes de alimentar un motor, confirmar tension nominal/referencia del motor, mapa OUT1/OUT2, deshabilitación del canal no usado y alimentación; no sustituir esa revisión por PWM bajo.

### Actualización del diagnóstico — 2026-10-08

El usuario informó nuevamente ausencia de movimiento después de las instrucciones de conexión. Confirmó que el monitor serie muestra aceptación y finalización del pulso. Lecturas posteriores informadas: +5V respecto de GND = **5,00 V** (USB, pilas desconectadas); entrada 12V respecto de GND = **6,03 V** (en reposo con pilas); ENA respecto de GND = **−0,01 V** (reposo, USB y sin pilas). No se midieron señales durante el pulso ni tensión de potencia bajo carga. IN1 e IN2 en reposo siguen pendientes.

El usuario solicitó diagramas para 1, 2 y 4 motores y un dibujo de conexiones. Se prepararon en `diagramas/`. El montaje de un motor conserva D5/D7/D8 del programa actual. Los de dos y cuatro proponen añadir D6/ENB, D9/IN3, D10/IN4 y una segunda resistencia de 10 kΩ; requieren modificar el programa y confirmar el pin de señal ENB. La topología de cuatro motores muestra dos en paralelo por lado; su corriente, alimentación y disipación siguen pendientes de validar. El firmware no se modificó.

## E006 — Primer servidor local, 2026-10-08

El usuario pidió crear el servidor y eligió utilizar esta computadora por ahora. Se implementó FastAPI, SQLite, panel web y fuente de simulación separada; sin puerto serie, sin integración de sensores y sin órdenes físicas.

Resultado automatizado: **32 pruebas aprobadas** (`.venv/Scripts/python.exe -m pytest server/tests -q`). Cubren validación, errores NaN/infinito, persistencia entre instancias de la aplicación, separación de fuentes, vencimiento de conexión, simulador único, detención y cierre del ciclo de vida, límites y bloqueo de origen ajeno. Se observó una advertencia de deprecación de Starlette sobre su adaptador de pruebas HTTPX; no hubo fallos. La sintaxis del JavaScript del panel fue verificada con Node.

Prueba del proceso real: `GET /healthz` devolvió `status=ok`; una simulación iniciada/detenida mediante la API produjo una muestra `source=demo`, preservó `device.connected=false` y quedó detenida. Última comprobación: servidor online en 127.0.0.1:8000, una muestra sintética guardada, sin muestras físicas. Base activa: `%LOCALAPPDATA%/RobotAutomata/robot.sqlite3`.

Limitación inicial, resuelta en la continuación: Ordenador detuvo su navegación al no poder determinar la URL de Chrome con suficiente certeza; no se continuó manejando esa ventana. La revisión visual quedó pendiente. Una comprobación adicional de cierre/reinicio del proceso mediante el nuevo lanzador fue bloqueada por la revisión automática, sin razón adicional a “blocked by policy”; el proceso quedó funcionando. La persistencia entre instancias y la limpieza de tareas sí se habían comprobado con TestClient y bases temporales.

Los archivos Iniciar servidor.cmd y Detener servidor.cmd están preparados. La integración física sigue pendiente de E005 y de un protocolo/adaptador de telemetría.

### Comprobación pendiente completada — 2026-10-08

A pedido del usuario se completó el ensayo real con los dos lanzadores y el navegador integrado:

- `Detener servidor.cmd` envió la solicitud de cierre. Se comprobó que `/healthz` dejó de responder y que Uvicorn registró cierre completo del proceso; no se confundió la solicitud con la terminación efectiva.
- El panel abierto mostró «Servidor sin respuesta», «Conexión interrumpida» y estado del robot «Sin verificar».
- `Iniciar servidor.cmd` volvió a iniciar el servidor en `127.0.0.1:8000`. `/healthz` respondió `status=ok` y el panel recuperó «Servidor en línea» automáticamente, sin recargar la página.
- SQLite conservó la muestra original: id 1, origen `demo`, batería 6,02 V y distancia 75,0 cm. Los eventos registraron cierre a las 22:55:50 e inicio a las 22:56:15, hora de Buenos Aires.
- Los botones del panel iniciaron y detuvieron la simulación. El total pasó de 1 a 15 muestras sintéticas; la simulación quedó detenida y el historial se conservó. La vista «Robot real» mostró 0 lecturas y campos sin datos, mientras «Simulación» mostró su historial separado.
- Se revisó visualmente el panel en el ancho disponible del navegador integrado: controles, avisos, lecturas, gráfico, actividad y tabla. No se observó desbordamiento horizontal de la página; la tabla dispone de desplazamiento propio. Captura local: `.runtime/panel-verificado.jpg`.

Estado al finalizar: servidor funcionando, simulación detenida, 15 muestras de ejemplo y ninguna muestra física. No se modificó ni se cargó firmware y no se abrieron puertos serie. Esta comprobación completa E006; el diagnóstico físico E005 sigue pendiente.
