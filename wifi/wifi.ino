/**
 * This sketch is intended for the  Adafruit ESP8266 Huzzah and requires
 * a Base64 encoding library. Its primary purpose is to read Xbee API
 * frames from Serial and POST them verbatim Jon's website.
 */
#include <Base64.h>
#include <ESP8266WiFi.h>

#include "Xbee.h"

static const bool DEBUG = false;
String myName = "TestingWiFi"; // Used for debug output

const char* ssid     = "DropboxGuest2.0";
const char* password = "";

const char* host = "litterbox.moistcake.net";
const char* secret = "1234567890";
String url_10 = "/api/v1.0/stalls";
String url_15 = "/api/v1.5/stalls";
String url_debug = "/api/v1.0/debug";

int led = 0;
XBee xbee;

void setup() {
  pinMode(led, OUTPUT);
  digitalWrite(led, HIGH);
  Serial.begin(9600);
  delay(10);

  // We start by connecting to a WiFi network
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  if (DEBUG)
    postToDebug("ESP8266 node started up with ip " + String(WiFi.localIP()));
}

// Debug Variables
XBee::State prevState = XBee::WAIT_FOR_HEADER;
int lastLength = 0;
int lastPos = 0;

void loop() {
  bool dataReady = xbee.poll();

  if (DEBUG && prevState != xbee.state) {
    postToDebug("The state changed to " + String((int)xbee.state));
    prevState = xbee.state;
  }

  if (DEBUG && lastLength != xbee.expecting) {
    postToDebug("The expecting length changed to " + String(xbee.expecting));
    lastLength = xbee.expecting;
  }

  if (DEBUG && lastPos != xbee.pos) {
    postToDebug("The position changed to " + String((int)xbee.pos));
    lastPos = xbee.pos;
  }

  if (dataReady) {
    digitalWrite(led, LOW);

    if (DEBUG) {
      char temp[20];
      String str = String(myName) + ": Message Recieved (" + String(xbee.packetLength) + " bytes) -  Bytes: ";
      for (int i = 0; i < xbee.packetLength; ++i) {
        snprintf(temp, sizeof(temp), "0x%x ", xbee.packet[i]);
        str += " " + String(temp);
      }

      str += " - Base64 " + String(xbee.base64Packet);
      postToDebug(str);
    }

    String raw = "{ \"raw_data\": \"" + String(xbee.base64Packet) + "\"}";
    postToServerRaw(raw);
    xbee.reset();
  }

  digitalWrite(led, HIGH);
}

void postToServerRaw(String& raw) {
  postToServer(host, url_15, raw);
}

void postToDebug(String& str) {
  postToServer(host, url_debug, myName + ": " + str);
}

void postToServer(const char* host, String& url, String& postData) {
  // Use WiFiClient class to create TCP connections
  WiFiClient client;
  const int httpPort = 80;
  if (!client.connect(host, httpPort)) {
    Serial.println("connection failed");
    return;
  }

  String header = String("POST ") + url + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" + 
               "Connection: close\r\n"
               "Content-Type: application/json\r\n" +
               "Content-Length: " + postData.length() + "\r\n" +
               + "\r\n";
  client.print(header);
  client.print(postData);
  client.flush();

  Serial.print(header);
  Serial.println(postData);

  delay(100);
}

String getFromServer(const char* host, String url) {
  // Use WiFiClient class to create TCP connections
  WiFiClient client;
  const int httpPort = 80;
  if (!client.connect(host, httpPort)) {
    Serial.println("connection failed");
    return "fail";
  }
  
  // This will send the request to the server
  client.print(String("GET ") + url + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" + 
               "Connection: close\r\n\r\n");
  delay(100);
  
  // Read all the lines of the reply from server
  String str = "";
  while(client.available()){
    str += (char)client.read();
  }

  return str;
}

// Legacy 1.0 support for the Ultrasonic Arduino.
void Version1Loop() {
  if (Serial.available() > 2) {
    clearInput();

    int num = Serial.parseInt();
    if (num == 0) {
      // do nothing
    } else if ( num > 0 && num < 15 ) {
      postToServer(true, 6);
      digitalWrite(led, LOW);
    } else {
      postToServer(false, 6);
      digitalWrite(led, HIGH);
    }
    Serial.println(num);
  }
}

void postToServer(bool status, int stallId) {
  String jsonData = "{\"status\": " + String(status) + ", \"secret\": \"1234567890\", \"stall_id\": " + String(stallId) + "}";
  postToServer(host, url_10, jsonData);
}

void clearInput() {
  while (Serial.available() > 2) {
    Serial.readStringUntil('\n');
  }
}
