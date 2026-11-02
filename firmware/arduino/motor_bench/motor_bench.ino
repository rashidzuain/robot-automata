// Ensayo de UN motor. Cargar y comprobar primero SIN pilas ni motor.
// D5 -> ENA (sin jumper ENA), D7 -> IN1, D8 -> IN2.
// Resistencia 10 kohm entre ENA y GND. 5V-EN retirado.
// Logica: Arduino USB -> +5V/GND del driver. Potencia: fuente aparte.
// No mover hasta verificar tension nominal del motor y alimentacion.

const byte ENABLE_PIN = 5;
const byte INPUT_1_PIN = 7;
const byte INPUT_2_PIN = 8;
const byte TEST_PWM = 96; // Orden PWM; no velocidad medida ni limite de corriente.
const unsigned long PULSE_MS = 250;
const unsigned long ARM_TIMEOUT_MS = 3000;
const unsigned long COOLDOWN_MS = 1000;

bool armed = false;
bool moving = false;
unsigned long armedAt = 0;
unsigned long startedAt = 0;
unsigned long stoppedAt = 0;

void disableMotor() {
  analogWrite(ENABLE_PIN, 0); // Deshabilitar primero el puente.
  digitalWrite(INPUT_1_PIN, LOW);
  digitalWrite(INPUT_2_PIN, LOW);
  armed = false;
  moving = false;
  stoppedAt = millis();
}

void setup() {
  // Fijar nivel bajo antes de configurar como salida.
  digitalWrite(ENABLE_PIN, LOW);
  digitalWrite(INPUT_1_PIN, LOW);
  digitalWrite(INPUT_2_PIN, LOW);
  pinMode(ENABLE_PIN, OUTPUT);
  pinMode(INPUT_1_PIN, OUTPUT);
  pinMode(INPUT_2_PIN, OUTPUT);
  disableMotor();
  Serial.begin(115200);
  Serial.println(F("DESHABILITADO. a=habilitar; f/r=pulso; s=parar"));
}

void loop() {
  const unsigned long now = millis();
  // La resta sin signo tolera el desbordamiento de millis().
  if (moving && now - startedAt >= PULSE_MS) {
    disableMotor();
    Serial.println(F("PULSO TERMINADO. DESHABILITADO"));
  } else if (armed && !moving && now - armedAt >= ARM_TIMEOUT_MS) {
    disableMotor();
    Serial.println(F("HABILITACION VENCIDA"));
  }

  // Un caracter por vuelta mantiene la comprobacion del temporizador frecuente.
  if (Serial.available() == 0) return;
  const char command = Serial.read();
  if (command == '\n' || command == '\r' || command == ' ') return;

  if (command == 's' || command == 'S') {
    disableMotor();
    Serial.println(F("STOP. DESHABILITADO"));
    // No ejecutar caracteres que ya estuvieran en cola tras STOP.
    while (Serial.available() > 0) Serial.read();
  } else if (command == 'a' || command == 'A') {
    const unsigned long commandTime = millis();
    if (!moving && commandTime - stoppedAt >= COOLDOWN_MS) {
      armed = true;
      armedAt = commandTime;
      Serial.println(F("HABILITADO POR 3 s. Enviar f o r"));
    }
  } else if (command == 'f' || command == 'F' || command == 'r' || command == 'R') {
    if (armed && !moving) {
      const bool forward = command == 'f' || command == 'F';
      digitalWrite(INPUT_1_PIN, forward ? HIGH : LOW);
      digitalWrite(INPUT_2_PIN, forward ? LOW : HIGH);
      startedAt = millis();
      moving = true;
      analogWrite(ENABLE_PIN, TEST_PWM);
      Serial.println(F("PULSO 250 ms"));
    }
  } else {
    disableMotor(); // Entrada desconocida: dejar salida deshabilitada.
  }
}
