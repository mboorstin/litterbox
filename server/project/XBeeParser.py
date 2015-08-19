# From https://github.com/serdmanczyk/XBee_802.15.4_APIModeTutorial
# Greatly stripped down and modified to parse a byte array instead of
# reading from serial.

from collections import deque

# Expects a byte array escaped message.
# Returns a (sender, status) tuple, or (None, None) if parsing fails.
def sender_and_status(message):
    if message[0] == 0x7E:
        message = message[1:]
    unescaped = parse(message)
    if unescaped:
        # Example message below.  Note that xbee.Receive() processes out escaping, etc.
        # Byte 2 is the API code, bytes 3 through 10 are sender ID. 
        # Byte 19 is the sensor reading (note that most of our Xbee's have the sensor
        # on pin 1, so we care about its second-to-right bit.
        # For more info, see http://ftp1.digi.com/support/utilities/digi_apiframes.htm.
        # 0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19 20
        # 00 12 92 00 13 a2 00 40 d4 a5 6d 2b 88 41 01 00 02 00 00 02 99
        # print xbee.format(message)
        status = bool(unescaped[-2] & 0x02)
        sender = unescaped[3:11]
        print "Sender", format(sender), "with status", status
        return (sender, status)
    else:
        return (None, None)

def parse(msg):
    """
    Parses a byte or bytearray object to verify the contents are a
      properly formatted XBee message.

    Inputs: An incoming XBee message

    Outputs: The unescaped message, or none if it's not valid
    """
    # 9 bytes is Minimum length to be a valid Rx frame
    #  LSB, MSB, Type, Source Address(2), RSSI,
    #  Options, 1 byte data, checksum
    if (len(msg) - msg.count(bytes(b'0x7D'))) < 9:
        return False

    # All bytes in message must be unescaped before validating content
    frame = unescape(msg)

    LSB = frame[1]
    # Frame (minus checksum) must contain at least length equal to LSB
    if LSB > (len(frame[2:]) - 1):
        return False

    # Validate checksum
    if (sum(frame[2:3+LSB]) & 0xFF) != 0xFF:
        return False

    # print("Rx: " + self.format(bytearray(b'\x7E') + msg))
    return frame

def unescape(msg):
    """
    Helper function to unescaped an XBee API message.

    Inputs:
      msg: An byte or bytearray object containing a raw XBee message
           minus the start delimeter

    Outputs:
      XBee message with original characters.
    """
    if msg[-1] == 0x7D:
        # Last byte indicates an escape, can't unescape that
        return None

    out = bytearray()
    skip = False
    for i in range(len(msg)):
        if skip:
            skip = False
            continue

        if msg[i] == 0x7D:
            out.append(msg[i+1] ^ 0x20)
            skip = True
        else:
            out.append(msg[i])

    return out

def format(msg):
    """
    Formats a byte or bytearray object into a more human readable string
      where each bytes is represented by two ascii characters and a space

    Input:
      msg: A bytes or bytearray object

    Output:
      A string representation
    """
    return " ".join("{:02x}".format(b) for b in msg)
