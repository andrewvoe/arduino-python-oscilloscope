  const unsigned long INTERVAL = 50000;
  unsigned long next;
    

void setup() {
  Serial.begin(115200);
  next = micros();
}

void loop() {
  if((micros() - next) >= INTERVAL){
    next += INTERVAL;
    Serial.println(analogRead(A0));
  }

}
