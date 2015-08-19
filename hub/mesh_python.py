#!/usr/bin/env python

from urlparse import urlparse
from httplib import HTTPConnection
import json
import serial
import base64

url = "http://litterbox.moistcake.net/api/v1.5/stalls"
# Not that the secret is being used right now...
headers = {"Content-Type": "application/json"}
urlparts = urlparse(url)

print "Connecting to Xbee..."
xbee = serial.Serial("/dev/ttyUSB0", 9600)
print "Connected to Xbee..."
while True:
    data = []
    while True:
        for c in xbee.read():
            if ord(c) == 0x7E and len(data) > 1:
                conn = HTTPConnection(urlparts.netloc, urlparts.port or 80)
                data = json.dumps({'raw_data': base64.b64encode(''.join(data))})
                conn.request("POST", urlparts.path, data, headers)
                data = []
                break
            else:
                data.append(c)
