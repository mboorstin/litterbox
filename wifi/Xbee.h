

struct XBee {
  static const int MAX_LEN = 100;
  static const byte START = 0x7E;
  static const byte ESC = 0X7D;
  
  byte packet[MAX_LEN];
  int packetLength = 0;
  char base64Packet[MAX_LEN];
  int base64Length = 0;
  int expecting;
  int pos = 0;

  enum State {
    RESET,
    WAIT_FOR_HEADER,
    WAIT_FOR_LENGTH,
    WAIT_FOR_DATA,
    DATA_READY
  } state;

  XBee() : packet(), packetLength(0), 
           base64Packet(), base64Length(0),
           state(RESET), expecting(1), pos(0) {}

  // Returns true if a valid packet is ready
  bool poll() {
   byte firstByte = 0;
   int incrCount = 0;
   
   if (Serial.available() < expecting)
    return false;
    
    switch (state) {
      case RESET:
        state = WAIT_FOR_HEADER;
        expecting = 1;
        packetLength = 0;
        pos = 0;
        
      case WAIT_FOR_HEADER:
        if (Serial.available() < 1)
          return false;

        do  {
          firstByte = Serial.read();
        } while (firstByte != START);

        if (firstByte != START)
          return false;
          
        expecting = 2;
        packet[0] = firstByte;
        pos = 1;
        state = WAIT_FOR_LENGTH;
        
      case WAIT_FOR_LENGTH:
        if (Serial.available() < 2)
          return false;

        // Read in the two length bytes
        packet[1] = Serial.read();
        packet[2] = Serial.read();
        
        expecting = ( packet[2] & 0xFF) + 1; // Checksum
        expecting += ( (packet[1] & 0xFF) << 8);
        pos = 3;
        
        state = WAIT_FOR_DATA;
      case WAIT_FOR_DATA:
        if (Serial.available() < expecting)
          return false;

        while (Serial.available() > 0 && expecting > 0) {
          byte read = Serial.read();
          packet[pos] = read;
          ++pos;
          
          // increment expecting cuz of escape character
          if (read == ESC)
           ++expecting;
          
          --expecting;
        }

        if (expecting != 0)
          return false;
        
        // Otherwise  We are done
        packetLength = pos;
        state = DATA_READY;

        base64Length = base64_encode(base64Packet, (char *)packet, packetLength);
      case DATA_READY:
        return true;
      default:
        //Error
        state = RESET;
        break;
    }

    return false;
  }

  void reset() {
    state = RESET;
  }
};


