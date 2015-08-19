/*
 *  Simple HTTP get webclient test
 */

#include <ESP8266WiFi.h>

const char* ssid     = "DropboxGuest2.0";
const char* password = "";

const char* host = "litterbox.moistcake.net";
const char* secret = "1234567890";
String url = "/api/v1.0/stalls";

int led = 0;
int MAX_DISTANCE = 15; // Unknown metrics, cm?

void setup() {
  pinMode(led, OUTPUT);
  digitalWrite(led, HIGH);
  Serial.begin(9600);
  Serial.setTimeout(2000);
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
}

int value = 0;

void loop() {
  ++value;

  if (Serial.available() > 2) {
    clearInput();
    
    int num = Serial.parseInt();
    if (num == 0) {
      // do nothing
    } else if ( num > 0 && num < MAX_DISTANCE ) {
      postToServer(true, 6);
      digitalWrite(led, LOW);
    } else {
      postToServer(false, 6);
      digitalWrite(led, HIGH);
    }
    Serial.println(num);
  }
}

void clearInput() {
  while (Serial.available() > 2) {
    Serial.readStringUntil('\n');
  }
}

void postToServer(bool status, int stallId) {
  String jsonData = "{\"status\": " + String(status) + ", \"secret\": \"1234567890\", \"stall_id\": " + String(stallId) + "}";
  postToServer(host, url, jsonData);
}

void postToServer(const char* host, String url, String postData) {
  // Use WiFiClient class to create TCP connections
  WiFiClient client;
  const int httpPort = 80;
  if (!client.connect(host, httpPort)) {
    Serial.println("connection failed");
    return;
  }

  String output = String("POST ") + url + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" + 
               "Connection: close\r\n"
               "Content-Type: application/json\r\n" +
               "Content-Length: " + postData.length() + "\r\n" +
               + "\r\n" +
               postData;
  client.print(output);

  Serial.println(output);
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
  
//  Serial.println();
//  Serial.println("closing connection");

  return str;
}

