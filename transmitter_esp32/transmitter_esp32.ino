#include <Ticker.h>
#define RXD2 16
#define TXD2 17


#define TRIGGER_PIN  32  // Pin connected to the trigger of the ultrasonic sensor
#define ECHO_PIN     33  // Pin connected to the echo of the ultrasonic sensor
float dis_m;
Ticker ticker;
long duration;
float distance;
int orderNumber = 1;  // Initialize order number

bool triggerPulse = false;
unsigned long pulseStartMillis = 0;

void triggerUltrasonic() {
  unsigned long currentMillis = millis();

  if (triggerPulse) {
    if (currentMillis - pulseStartMillis >= 10) { // Pulse duration is 10µs
      digitalWrite(TRIGGER_PIN, LOW);
      triggerPulse = false;

      duration = pulseIn(ECHO_PIN, HIGH);
      distance = duration * 0.034 / 2;
      dis_m = distance/100;
      Serial.println(dis_m);
      Serial2.println(dis_m);

      orderNumber++;
    }
  } else {
    digitalWrite(TRIGGER_PIN, LOW);
    if (currentMillis - pulseStartMillis >= 2) { // Wait for 2µs
      digitalWrite(TRIGGER_PIN, HIGH);
      pulseStartMillis = currentMillis;
      triggerPulse = true;
    }
  }
}


void setup() {
  Serial.begin(9600);
  Serial2.begin(9600, SERIAL_8N1, RXD2, TXD2);
  pinMode(TRIGGER_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  pulseStartMillis = millis();

  ticker.attach_ms(1000, triggerUltrasonic);
}

void loop() {
  // Perform other tasks here
}
