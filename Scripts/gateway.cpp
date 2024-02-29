//GATEWAY
#include <Arduino.h>
#include <WiFi.h>
#include <WiFiClient.h>
#include <WiFiClientSecure.h>
#include <SPI.h>
#include <LoRa.h>
#include <MQTTClient.h>
#include <random>
#include "lista.h"

const char* ssid = "scraccio";
const char* password = "simone1337";

int col_num = 0;

int counter = 1;

WiFiClientSecure net;
MQTTClient client;

DoublyLinkedList* listaMessaggi;

#define LORA_CS 18
#define LORA_RST 23
#define LORA_DI0 26

void messageReceivedMQTT(String &topic, String &payload) {
  Serial.println("incoming: " + topic + " - " + payload);
  LoRa.beginPacket();
  LoRa.print(topic + " - " + payload);
  LoRa.endPacket();
}

void setup() {

  Serial.begin(115200);

  listaMessaggi = new DoublyLinkedList();
  
  srand (time(NULL));
  LoRa.setPins(LORA_CS, LORA_RST, LORA_DI0);

  while (!LoRa.begin(866E6)) {\
      Serial.print(".");
      delay(500);
  }
  Serial.println();

  LoRa.setSyncWord(0xF3);
  Serial.println("LoRa Initializing OK!");

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.waitForConnectResult() != WL_CONNECTED) {
    Serial.printf("WiFi Failed!\n");
  }

  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  net.setInsecure();

  client.begin("broker.emqx.io", 8883, net);
  //client.onMessage(messageReceivedMQTT);
  while (!client.connect("vkudtckgfj")) {
    Serial.print(".");
    delay(1000);
  }
  Serial.println("MQTT Connected");
  //client.subscribe("sentinel/operators/gateway");

  //client.publish("/sentinel/logs", R"({"col" : 1,"strength": 0.8,"idOp" : 1})");
  //Serial.println("published");
  /*delay(1000);
  client.publish("/sentinel/logs", R"({"col" : 2,"strength": 0.4,"idOp" : 3})");
  Serial.println("published");
  delay(1000);
  client.publish("/sentinel/logs", R"({"col" : 3,"strength": 0.2,"idOp" : 4})");
  Serial.println("published");
  delay(1000);
  client.publish("/sentinel/logs", R"({"col" : 4,"strength": 0.9,"idOp" : 2})");
  Serial.println("published");*/
}

void loop() {
  client.loop();
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    Serial.print("Received packet: ");
    while (LoRa.available()) {
        String LoRaData = LoRa.readString();
        Serial.println(LoRaData);
        if(listaMessaggi->findNode(LoRaData) == NULL){
          listaMessaggi->insertTail(LoRaData);
          client.publish("/sentinel/logs", LoRaData);
          Serial.println("published");
        }
        else{
          Serial.println("Scarto il messaggio");
        }
    }
  }
  
  /*String strength = String(static_cast <float> (rand()) / (static_cast <float> (RAND_MAX/2)) - 1);
  String idOp = String(rand()%4 + 1);
  String bpm = String(rand()%40 + 60);
  String temp = String(random(7) + 35);
  String msg = "{\"type\" : 0, \"col\" : " + String(col_num) + ", \"rssi\": " + strength + ", \"user_addr\" : " + String(idOp) + ", \"msg_counter\": " + String(counter++) + ", \"bpm\": " + bpm + ", \"temp\": " + temp + "}";
  client.publish("/sentinel/logs", msg);
  Serial.println("published: " + msg);*/
}