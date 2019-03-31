void setup() {
  Serial.begin(115200);
   pinMode(LED_BUILTIN, OUTPUT);
   digitalWrite(LED_BUILTIN, HIGH);
}
void loop() {
  if(Serial.available() > 0) {
    int data = Serial.read();
    //char str[2];
    //str[0] = data;
    //str[1] = '\0';
    if(data==254){
            digitalWrite(LED_BUILTIN, LOW);
      }
    Serial.println(data);
  }
}
