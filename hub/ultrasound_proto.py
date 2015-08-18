#!/usr/bin/env python

import serial
from urlparse import urlparse
from httplib import HTTPConnection
import json

THRESHOLD = 15

url = "http://litterbox.moistcake.net/api/v1.0/stalls"
# Not that the secret is being used right now...
headers = {"Content-Type": "application/json"}
urlparts = urlparse(url)
conn = HTTPConnection(urlparts.netloc, urlparts.port or 80)

print "Connecting to Xbee..."
xbee = serial.Serial("/dev/ttyUSB0", 9600)
print "Connected to Xbee..."
old_status = None
while True:
    data = xbee.readline()
    try:
        distance = int(data)
    except:
        print "Unable to parse data: ", data
        continue

    print distance
    status = distance >= 0 and distance < THRESHOLD
    
    if status != old_status:
        print "Status changed to", status
        data = json.dumps({'secret': '1234567890', 'stall_id': 0, 'status': True})
        # conn.request("POST", urlparts.path, data, headers)

    old_status = status
