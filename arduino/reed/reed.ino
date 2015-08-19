void setup() {
  pinMode(8, INPUT_PULLUP);
  Serial.begin(9600);
}

void loop() {
  Serial.print(digitalRead(8));
  delay(100);
}
