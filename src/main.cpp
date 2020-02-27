#include <Arduino.h>
#include "MPU9250.h"   // https://github.com/bolderflight/MPU9250
#include <SPI.h>

MPU9250 IMU(SPI,2);
MPU9250 IMU2(SPI,3);

int status;

void setup() {
  // serial to display data
  Serial.begin(9600);
  
  delay(1000);
  Serial.println("restart");

  // start communication with IMU 
  
  status = IMU.begin();
  if (status < 0) {
    Serial.println("IMU initialization unsuccessful");
    Serial.println("Check IMU wiring or try cycling power");
    Serial.print("Status: ");
    Serial.println(status);
    while(1) {}
  }
  /*
  status = IMU2.begin();
  if (status < 0) {
    Serial.println("IMU2 initialization unsuccessful");
    Serial.println("Check IMU wiring or try cycling power");
    Serial.print("Status: ");
    Serial.println(status);
    while(1) {}
  }
*/
}

void loop() {
  // read the sensor
  IMU.readSensor();
  //IMU2.readSensor();
  // display the data

  Serial.print(IMU.getAccelX_mss(),6);
  Serial.print("\t");
  Serial.print(IMU.getAccelY_mss(),6);
  Serial.print("\t");
  Serial.println(IMU.getAccelZ_mss(),6);


  delay(100);
}
