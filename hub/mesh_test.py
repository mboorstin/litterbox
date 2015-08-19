#!/usr/bin/env python

import XBee
from urlparse import urlparse
from httplib import HTTPConnection
import json

url = "http://litterbox.moistcake.net/api/v1.0/stalls"
# Not that the secret is being used right now...
headers = {"Content-Type": "application/json"}
urlparts = urlparse(url)

print "Connecting to Xbee..."
xbee = XBee.XBee("/dev/ttyUSB0")
print "Connected to Xbee..."
old_status = {}
while True:
    message = xbee.Receive()
    if message:
        # Example message below.  Note that xbee.Receive() processes out escaping, etc.
        # Byte 2 is the API code, bytes 3 through 10 are sender ID. 
        # Byte 19 is the sensor reading (note that most of our Xbee's have the sensor
        # on pin 1, so we care about its second-to-right bit.
        # For more info, see http://ftp1.digi.com/support/utilities/digi_apiframes.htm.
        # 0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19 20
        # 00 12 92 00 13 a2 00 40 d4 a5 6d 2b 88 41 01 00 02 00 00 02 99
        # print xbee.format(message)
        status = bool(message[-2] & 0x02)
        sender = str(message[3:11])
        if (sender not in old_status) or (status != old_status[sender]):
            print "Status changed to", status, "with sender", sender
            old_status[sender] = status
