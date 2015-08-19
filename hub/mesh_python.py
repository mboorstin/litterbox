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
    # Yes, we're hardcoding the message length because this is for testing
    data = xbee.read(23)
    print data.encode("hex")
    conn = HTTPConnection(urlparts.netloc, urlparts.port or 80)
    print base64.b64encode(data)
    data = json.dumps({'raw_data': base64.b64encode(data)})
    conn.request("POST", urlparts.path, data, headers)
