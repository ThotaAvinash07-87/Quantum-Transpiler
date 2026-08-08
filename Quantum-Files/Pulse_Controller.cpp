// Quantum-to-Classical Hardware Bridge
// Maps quantum gate types to physical GPIO pulse widths.

const int PIN_X = 8;    // Green LED (Fastest)
const int PIN_CX = 9;   // Yellow LED (Slower)
const int PIN_CCX = 10; // Red LED (Slowest, highest thermal cost)

void setup() {
  // Open serial communications at 9600 baud
  Serial.begin(9600);
  
  // Configure pins as outputs
  pinMode(PIN_X, OUTPUT);
  pinMode(PIN_CX, OUTPUT);
  pinMode(PIN_CCX, OUTPUT);
  
  // Flash all LEDs to indicate the system is ready
  flashAll(3, 200);
  Serial.println("ARDUINO_READY");
}

void loop() {
  // Check if Python has sent a gate instruction
  if (Serial.available() > 0) {
    // Read the incoming gate string (e.g., "CX_0_1\n")
    String gate = Serial.readStringUntil('\n');
    gate.trim(); // Remove whitespace and carriage returns
    
    if (gate.length() > 0) {
      executeGatePulse(gate);
    }
  }
}

void executeGatePulse(String gate) {
  // CCX Gates (Toffoli) - Massive overhead (5 seconds)
  if (gate.startsWith("CCX")) {
    digitalWrite(PIN_CCX, HIGH);
    delay(5000);
    digitalWrite(PIN_CCX, LOW);
  }
  // CX Gates (CNOT) - Moderate overhead (1 second)
  else if (gate.startsWith("CX")) {
    digitalWrite(PIN_CX, HIGH);
    delay(1000);
    digitalWrite(PIN_CX, LOW);
  }
  // X Gates (NOT) - Low overhead (100 ms)
  else if (gate.startsWith("X")) {
    digitalWrite(PIN_X, HIGH);
    delay(100);
    digitalWrite(PIN_X, LOW);
  }
  
  // Tell Python the physical hardware pulse is complete
  Serial.println("DONE"); 
}

// Helper to flash LEDs on startup or circuit completion
void flashAll(int times, int delayMs) {
  for (int i = 0; i < times; i++) {
    digitalWrite(PIN_X, HIGH);
    digitalWrite(PIN_CX, HIGH);
    digitalWrite(PIN_CCX, HIGH);
    delay(delayMs);
    digitalWrite(PIN_X, LOW);
    digitalWrite(PIN_CX, LOW);
    digitalWrite(PIN_CCX, LOW);
    delay(delayMs);
  }
}
