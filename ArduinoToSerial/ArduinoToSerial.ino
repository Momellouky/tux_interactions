#include "Ultrasonic.h"

Ultrasonic ultrasonic(7);
void setup() {
    Serial.begin(9600);
    Serial.setTimeout(1);
    pinMode(5, INPUT);
    pinMode(2, INPUT);
}
void loop() {
  // drift
  if (digitalRead(5) == HIGH) {
    Serial.println("dri 1.00");
  }
  else {
    Serial.println("dri 0.00");
  }

  // accélération
  long RangeInCentimeters;
  float power;

  RangeInCentimeters = ultrasonic.MeasureInCentimeters();

  if (RangeInCentimeters > 30.0) {
    power = 0.0;
  }
  else {
    power = (30.0-RangeInCentimeters)/30.0 + 0.03;
    if (power > 1.0) {
      power = 1.0;
    }
  }

  Serial.print("acc ");
  Serial.println(power);

  int vibrationState = digitalRead(2);
  Serial.print("bst ");
  Serial.println(vibrationState);

  delay(10);
}
