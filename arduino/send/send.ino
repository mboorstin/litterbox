// # Connection:
// #       URM V3.2 ultrasonic sensor TTL connection with Arduino
// #       VCC (Arduino)   -> Pin 1 VCC (URM37 V3.2)
// #       GND (Arduino)   -> Pin 2 GND (URM37 V3.2)
// #       Pin 9 (Arduino) -> Pin 9 TXD (URM37 V3.2)
// #       Pin 8 (Arduino) -> Pin 8 RXD (URM37 V3.2)
// #
// #       Pin 10 Sleep for XBee

#include "URMSerial.h"

#define XBEE_SLEEP 10                // XBee sleep pin on D7

// The measurement we're taking
#define DISTANCE 1
#define TEMPERATURE 2
#define ERROR 3
#define NOTREADY 4
#define TIMEOUT 5

URMSerial urm;

void setup() {

  // Setup XBEE 
  pinMode(XBEE_SLEEP, OUTPUT);     // sleep control
  digitalWrite(XBEE_SLEEP, LOW);  
    
  Serial.begin(9600);                  // Sets the baud rate to 9600
  urm.begin(9,8,9600);                 // RX Pin, TX Pin, Baud Rate
  Serial.println("Init");   // Shameless plug 
}

void loop()
{
  Serial.println(getMeasurement());  // Output measurement
  delay(50);
}

int value; // This value will be populated
int getMeasurement()
{
  // Request a distance reading from the URM37
  switch(urm.requestMeasurementOrTimeout(DISTANCE, value)) // Find out the type of request
  {
  case DISTANCE: // Double check the reading we recieve is of DISTANCE type
    //    Serial.println(value); // Fetch the distance in centimeters from the URM37
    return value;
    break;
  case TEMPERATURE:
    return value;
    break;
  case ERROR:
    Serial.println("-1");
    break;
  case NOTREADY:
    Serial.println("-2");
    break;
  case TIMEOUT:
    Serial.println("-3");
    break;
  } 

  return -1;
}

