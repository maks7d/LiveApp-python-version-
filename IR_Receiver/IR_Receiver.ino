#include <Wire.h>
#include <dht_nonblocking.h>
#include <LiquidCrystal_I2C.h>
#define VCC13 13
#define DHT_SENSOR_TYPE DHT_TYPE_11
static const int DHT_SENSOR_PIN = 12;
DHT_nonblocking dht_sensor( DHT_SENSOR_PIN, DHT_SENSOR_TYPE );

LiquidCrystal_I2C LCD(0x27, 20, 4);
int i=0;
byte simvol[8] = {
0b01100,
0b10010,
0b10010,
0b01100,
0b00000,
0b00000,
0b00000,
0b00000
};

void setup() {
  Wire.begin();
  LCD.begin();
  LCD.createChar(1, simvol);
  Serial.begin(9600);
  pinMode(VCC13, OUTPUT);  
  digitalWrite(VCC13, HIGH);
}

void loop() {
  
  float temperature, humidity;
  if(dht_sensor.measure(&temperature, &humidity))
  {
    Serial.print("temperature : "); Serial.println(temperature);
    Serial.print("humidity : "); Serial.println(humidity);
    LCD.clear();
    LCD.setCursor(0, 0);
    LCD.print(int(temperature));
    LCD.print(char(1));
    LCD.print("|");
    LCD.setCursor(0,1);
    LCD.print(int(humidity));  
    LCD.print("%|");
    LCD.setCursor(0,2);
    LCD.print("---");
     
  }
 
}