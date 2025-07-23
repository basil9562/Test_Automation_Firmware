const float FIRMWARE_VERSION = 1.2;
const int ledPin = 13;

String command = "";

void setup() {
  Serial.begin(9600);
  delay(1000);

  Serial.println("========== BOOT INFO ==========");
  Serial.print("Firmware Version: ");
  Serial.println(FIRMWARE_VERSION, 1);
  Serial.println("System initialized successfully.");
  Serial.println("================================");

  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);  // LED off initially
}

void loop() {
  // Check for incoming serial data
  if (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {
      processCommand(command);
      command = "";
    } else if (c != '\r') {
      command += c;
    }
  }
}

void processCommand(String cmd) {
  cmd.trim();  // Remove any extra whitespace

  if (cmd.equalsIgnoreCase("LED ON")) {
    digitalWrite(ledPin, HIGH);
    Serial.println("LED turned ON");
  } else if (cmd.equalsIgnoreCase("LED OFF")) {
    digitalWrite(ledPin, LOW);
    Serial.println("LED turned OFF");
  } else {
    Serial.println("Unknown command");
  }
}
