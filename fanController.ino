#include<avr/wdt.h>

int in = 9;
int out = 10;
int cpu = 11;
int FanSpeed = 128;
int incomingByte = 0;
unsigned long previousMillis = 0;
const long interval = 20000;

void setup()  { 
  Serial.begin(115200);
  analogWrite(in, 64);
  analogWrite(out, 64);
  analogWrite(cpu, 64);
  wdt_disable();
  delay(1000);
  wdt_enable(WDTO_8S);
} 

void loop()  { 
  unsigned long currentMillis = millis();
  
  if (Serial.available() > 0) 
  {
    // read the incoming byte:
    incomingByte = Serial.read();

    // say what you got:
    Serial.print("I received: ");
    Serial.println(incomingByte, DEC);

    analogWrite(in, incomingByte);
    analogWrite(out, incomingByte);
    analogWrite(cpu, (incomingByte * 0.8));
    previousMillis = currentMillis;
    //while(1);
  }
  
  if (currentMillis - previousMillis >= interval)
  {
    analogWrite(in, 160);
    analogWrite(out, 160);
    analogWrite(cpu, 160);
  }
  
  wdt_reset();
}
