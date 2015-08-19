#include "XBee.h"

XBee xbee;
XBeeAddress64 coordinator = XBeeAddress64(0x0013a200, 0x40E82B30);

void setup() {
  xbee = XBee();
  
  // Start the serial port
  Serial.begin(9600);
  xbee.setSerial(Serial);
}

void loop() {
  // Create an array for holding the data you want to send.
  uint8_t payload[] = { 'H', 'i' };
  // Create a TX Request
  ZBTxRequest zbTx = ZBTxRequest(coordinator, payload, sizeof(payload));
  // Send your request
  xbee.send(zbTx);
  delay(1000);
}
