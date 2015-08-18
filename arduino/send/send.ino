#define XBEE_SLEEP 10                // XBee sleep pin on D7
#define WAKEUP_DELAY 20000
#define SLEEP_DELAY 1000
#define SEND_DELAY 500

void setup() {
   pinMode(XBEE_SLEEP, OUTPUT);     // sleep control
   Serial.begin(9600);

   // Let's start with it awake
   // digitalWrite(XBEE_SLEEP, LOW);   // deassert to keep radio awake when sleep mode selected
   /*if(atCommand("D7", 1) | atCommand("SM", 1)) {
      // AT commands failed, flash frantically
   }*/
}

void loop() {
  digitalWrite(XBEE_SLEEP, LOW);
  delay(WAKEUP_DELAY);
  Serial.print('A');
  delay(SEND_DELAY);
  
  digitalWrite(XBEE_SLEEP, HIGH);
  delay(SLEEP_DELAY);
  Serial.print('B');
  delay(SEND_DELAY);
}
  
