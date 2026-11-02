# Inventario de hardware

Actualizado: 2026-10-07.

## Alcance y criterio de identificación

Inventario inicial a partir de catorce fotografías del usuario y de sus descripciones. Las fotos adicionales muestran el chasis, controlador por ambas caras, etiquetas de pilas y multímetro. Las mediciones físicas informadas por el usuario están registradas en EXPERIMENTS.md; no fueron ejecutadas por el asistente. Una identificación por apariencia no confirma tensión admisible, corriente, pinout, revisión ni funcionamiento.

- **Visible:** se reconoce el objeto o su función general en las fotos.
- **Probable:** el aspecto coincide con una familia; falta leer inscripciones.
- **Declarado:** informado por el usuario, sin confirmación visual suficiente.
- **Pendiente:** información necesaria para diseñar conexiones o ensayos.

Las fotografías originales no se incluyen en este repositorio.

## Tracción, control y alimentación

| Elemento | Cantidad visible | Identificación y certeza | Uso / pendiente |
|---|---:|---|---|
| Chasis de cuatro ruedas | 1 | Visible, parcialmente armado | Completar fijación de placas y cables antes de desplazamiento |
| Motorreductores amarillos y ruedas | 8 conjuntos | 4 montados y 4 adicionales; formato TT probable. Usuario declara rango de alimentación 3–6 V | Modelo, relación de reducción y corrientes nominal/de bloqueo sin confirmar; primer ensayo individual breve preparado |
| Controlador rojo con disipador | 1 | Formato típico de módulo L298N; código del integrado no legible. Etiquetas 12V, GND y +5V legibles en reverso | Usuario midió entrada 5,95 V y lógica 4,55 V; se prepara lógica externa desde Arduino USB con puente del regulador retirado |
| Arduino | 1 | Placa marcada UNO; variante compatible visible | Usuario declara Arduino Uno; revisión y microcontrolador pendientes |
| Sensor Shield | 1 | Inscripción Sensor Shield v5.0 visible | Expande conexiones; no sustituye al puente H ni agrega capacidad de procesamiento |
| Portapilas | Al menos 2 | Uno para cuatro AA y otro vacío | Usuario corrigió la lectura de 5,96 V a 6,4 V; confirmar punto y condiciones de la revisión. Evaluación bajo carga pendiente |
| Pilas | 5 disponibles según actualización del usuario | Cuatro DIA AA alcalinas de 1,5 V, todas nuevas según usuario, y una Jaiho R6 AA de 1,5 V, carbón-zinc | DIA: 1,48 / 1,48 / 1,60 / 1,49 V en vacío; Jaiho: 1,27 V. Excluir Jaiho; capacidad bajo carga pendiente |
| Pilas rectangulares de 9 V | Al menos 2 | Visibles sobre la mesa | No se eligen como fuente de los cuatro motores |
| Convertidor DC-DC ajustable | 1 | Módulo azul con bobina y ajuste visible | No confirmado si eleva, reduce o ambas cosas; leer integrado y terminales |
| Fuente para protoboard | 1 | Formato tipo MB102 probable | Confirmar versión y límites; no usar como fuente de potencia de motores |
| Protoboard, jumpers y componentes discretos | Varios | Visibles | Prototipado de señales; dimensionar aparte el cableado de potencia |
| Multímetro digital | 1 | DT-830D visible; disponibilidad confirmada por el usuario | En la foto, cable rojo en COM y negro en VΩmA; intercambiarlos antes del ejercicio de tensión |

## Sensores, interfaces y otros actuadores

| Elemento | Cantidad visible | Identificación y certeza | Uso / pendiente |
|---|---:|---|---|
| Sensores IR con emisor/receptor y ajuste | 2 | Visibles; referencia exacta pendiente | Caracterizar respuesta y geometría; no asumir que son lectores adecuados de encoder |
| Discos en ejes internos del chasis | Varios | Discos ranurados visibles, compatibles con lectura óptica para encoder | No se identifican lectores ópticos instalados ni cableado de realimentación |
| Placa azul pequeña con pines sin soldar | 1 | Posible módulo inercial de familia GY-521; identificación no confirmada | Leer ambas caras antes de contar con IMU o recomendar comprarla |
| Sensor azul perforado | 1 | Probablemente DHT11 | Posible temperatura/humedad; confirmar referencia |
| Módulo rojo con cápsula de micrófono | 1 | Detector de sonido probable | Confirmar modelo y salida; no asumir aptitud para reconocimiento de voz |
| Módulo inalámbrico alargado | 1 | Bluetooth de familia HC-05/HC-06 probable | Referencia y niveles pendientes; no necesario para la primera etapa |
| Joystick | 1 | Visible | Posible mando manual futuro |
| Relé de un canal | 1 | Visible | No sustituye al controlador PWM de motores |
| Microservos | Al menos 2 aparentes | Uno azul claramente visible y otro conjunto en bolsa | Confirmar modelos y cantidades; posible orientación de cámara/sensor |
| Motor paso a paso pequeño | 1 | Tipo 28BYJ-48 probable | Actuador adicional para experimentos |
| Placa verde para paso a paso | 1 | Controlador tipo ULN2003 probable | Confirmar referencia y correspondencia con el motor |
| Pantalla LCD | 1 | Formato 16x2 probable | Diagnóstico local opcional; confirmar interfaz |
| Módulo con portapila de botón | 1 | Posible reloj RTC | Confirmar referencia y circuito antes de instalar o cambiar pila |
| RFID, llavero y tarjeta | 1 conjunto | Inscripción RC522 aparente y accesorios visibles | Identificación opcional futura; no necesario para tracción |
| Control remoto IR | 1 | Visible | Confirmar receptor compatible |
| Módulo pequeño negro y placas en bolsas | Varios | Función o modelo sin confirmar | Primeros planos solo cuando sean necesarios |
| LEDs, displays y otros componentes de kit | Varios | Visibles en organizador | Ejercicios y diagnóstico; inventario detallado posterior |

## Hardware declarado, pendiente de confirmación visual

- **ESP32-CAM + ESP32-CAM-MB:** declaradas por el usuario. La cámara fue escrita como “OV36660”; posible OV3660, pendiente de leer inscripción. No se confirma el sensor, la PSRAM ni la variante de placa a través de las bolsas.
- **Sensor ultrasónico:** declarado en la descripción inicial; no identificado con suficiente claridad en estas fotografías. No se considera ausente.
- **Laptop Acer E5-571-56US:** CPU declarada Intel Core i5-4210U, 1,7 GHz base y hasta 2,7 GHz turbo. El usuario menciona 1792 MB de memoria de video, que no determina la RAM instalada. RAM, sistema operativo, almacenamiento y estado térmico pendientes.
- **Otras computadoras:** disponibles según usuario, todavía sin inventario.
- **Fuente con límite de corriente y otros instrumentos:** disponibilidad no informada; no inferir ausencia por no aparecer en las fotos. Multímetro DT-830D confirmado y registrado arriba.

## Hallazgos que condicionan el primer ensayo

1. El LED rojo del controlador está encendido en las fotos del chasis. Había alimentación presente al fotografiarlo; no se deduce movimiento. Desconectar el portapilas antes de manipular conexiones.
2. Las etiquetas confirmaron tres AA alcalinas DIA y una AA carbón-zinc Jaiho. El usuario aportó una cuarta DIA AA alcalina de 1,5 V y confirmó que las cuatro son nuevas. Las lecturas individuales anteriores suman 6,05 V; el usuario revisó la lectura del conjunto de 5,96 V a 6,4 V, pendiente confirmar punto y condiciones. El estado de uso declarado es comparable; capacidad bajo carga pendiente. Excluir Jaiho del conjunto de tracción.
3. El usuario cree que los motores están conectados de a dos. Las nuevas vistas son compatibles con dos motores por lado conectados a cada salida, probablemente en paralelo; confirmar recorriendo cada cable con alimentación desconectada antes de dar el mapa por definitivo.
4. Si se confirma L298N, habrá dos puentes completos. Dos motores en paralelo comparten una orden y suman corriente. El límite del chip no garantiza la capacidad térmica del módulo comercial.
5. Un L298 presenta caída de tensión en su etapa de potencia. La alimentación disponible y el regulador de lógica deben verificarse; no compensar pérdidas aumentando tensión sin conocer los motores.
6. Reverso recibido: etiquetas de alimentación 12V, GND y +5V confirmadas. La etiqueta 12V identifica la entrada de potencia; no autoriza a alimentar motores desconocidos a 12 V. El puente cercano al regulador está presente en la foto; su ubicación es consistente con habilitación del regulador en esta familia de módulos. Medir +5V respecto de GND sin Arduino ni motores conectados; no inyectar alimentación externa en +5V con ese puente instalado.
7. Los discos aparentes de encoder no implican medición disponible. Faltan identificación, lectores y pruebas antes de registrar velocidad medida.
8. No se aprecian fijaciones del controlador en sus cuatro orificios. Verificar sujeción con separadores y que ningún contacto roce conductores.
9. El DT-830D tiene las puntas intercambiadas en la foto. Para medir tensión: negro en COM (inferior), rojo en VΩmA (central), terminal 10 A libre y selector 20 en tensión continua V⎓. Intercambiar colores entre COM y VΩmA invierte la convención de signo; no constituye por sí solo un cortocircuito al medir tensión.

## Decisiones vigentes

- Primer objetivo: un motor/canal identificado, con mecanismo suspendido, mando por Arduino, movimientos breves, STOP y vencimiento local.
- Conservar provisionalmente el controlador existente; su aptitud se decide después de identificar alimentación y corrientes.
- E002 registró lógica de 4,55 V con entrada de 5,95 V: margen insuficiente para integrar motores de forma confiable. E003 prepara alimentación de lógica desde Arduino USB retirando el puente del regulador, sin motores ni pilas conectados. Mantener potencia de motores separada del Arduino.
- Resultado E003 informado: 5,00 V en +5V del controlador. Mantener retirado el puente del regulador al usar 5 V externos; verificación bajo carga de motores pendiente.
- Identificación de los dos pines del puente ENA por medición respecto de +5V: el pin hacia el centro dio 0,7–0,8 Ω (alimentación +5V); el del borde dio “1” (pendiente interpretar como fuera de escala, no 1 Ω). D5 y resistencia de pull-down deben ir al pin ENA del borde, dejando libre el pin de +5V del centro; aplicar esta ubicación solo a la orientación del módulo inspeccionado.
- Control por lados es una etapa inicial aceptable si los pares corresponden a izquierda/derecha. No equivale a cuatro motores independientes.
- No recomendar aún compras de IMU, servos o sensores ambientales: pueden estar presentes y deben identificarse primero.
- Cámara, Bluetooth, pantalla, relé y demás módulos se incorporarán según necesidades de etapas posteriores.

## Próximas evidencias necesarias

1. Fotos de ambas caras y E002 completos: entrada 5,95 V, lógica 4,55 V. El código del chip sigue oculto. Próximo: E003, alimentación externa de lógica de banco, sin motores conectados.
2. Mediciones individuales y del portapilas ya registradas en EXPERIMENTS.md. Cuatro DIA nuevas confirmadas. Siguiente paso: verificar alimentación de lógica del controlador con motores desconectados, después de identificar etiquetas y función de puentes.
3. Mapa escrito de cada motor hacia sus bornes; continuidad solo sin energía y con instrumento apropiado.
4. Inscripción o referencia de compra de los motores, si existe.
5. Posteriormente: ambas caras del convertidor y de la posible IMU, e identificación de placas fuera de las bolsas.

## Referencias

- [STMicroelectronics: ficha del L298](https://www.st.com/resource/en/datasheet/l298.pdf). Aplicable si se confirma el integrado; no identifica ni certifica este módulo concreto.
- [Energizer: cuidado de pilas](https://energizer.com/about-batteries/battery-care/).
- [Espressif: controlador y sensores de cámara compatibles](https://github.com/espressif/esp32-camera).
- [Intel: i5-4210U](https://www.intel.com/content/www/us/en/products/sku/81016/intel-core-i54210u-processor-3m-cache-up-to-2-70-ghz/specifications.html).
- [Fluke: medición de tensión continua](https://www.fluke.com/en-us/learn/blog/digital-multimeters/how-to-measure-dc-voltage-with-a-digital-multimeter). El procedimiento general se aplica al ejercicio; los puertos y rango del DT-830D se identificaron en la foto.
- [Handson Technology: esquema de módulo L298N de esta familia](https://handsontec.com/dataspecs/module/L298N%20Motor%20Driver.pdf). Referencia de topología y regulador; no certifica fabricante ni capacidad de este ejemplar.

## Fotografías de referencia

Fotos tomadas durante el relevamiento (no publicadas):

- Vista general
- Vista superior con portapilas
- Vista general alternativa
- Placas y módulos
- Motores adicionales y sensores
- Chasis y controlador
- Módulos y accesorios
- Chasis, nueva vista
- Controlador, detalle
- Motores y discos ranurados
- Etiquetas de pilas
- Multímetro DT-830D
- Reverso del controlador y etiquetas
- Frente del controlador sin alimentación conectada
