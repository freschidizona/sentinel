//GATEWAY
#include <Arduino.h>
#include <WiFi.h>
#include <WiFiClient.h>
#include <WiFiClientSecure.h>
#include <SPI.h>
#include <LoRa.h>
#include <MQTTClient.h>
#include <random>

const char* ssid = "";
const char* password = "";

int col_num = 0;
int counter = 1;
int startTime;

WiFiClientSecure net;
MQTTClient client;
std::vector<String> listaMessaggi;

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

  srand (time(NULL));
  startTime = millis();
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
  client.onMessage(messageReceivedMQTT);
  client.subscribe("/sentinel/messages");
  while (!client.connect("vkudtckgfj")) {
    Serial.print(".");
    delay(1000);
  }
  Serial.println("MQTT Connected");
}

void loop() {
  client.loop();
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    Serial.print("Received packet: ");
    while (LoRa.available()) {
        String LoRaData = LoRa.readString();

        std::vector<String>::iterator it = std::find(listaMessaggi.begin(), listaMessaggi.end(), LoRaData);
        Serial.println(LoRaData);

        if (it == listaMessaggi.end()){
          listaMessaggi.push_back(LoRaData);
          client.publish("/sentinel/messages", LoRaData);
          Serial.println("published");
        }
        else{
          Serial.println("Scarto il messaggio");
        }
    }
  }
  
  /*if (millis() - startTime > 2000){
    String strength = String(static_cast <float> (rand()) / (static_cast <float> (RAND_MAX/2)) - 1);
    String col = String(random(9) + 1);
    String idOp = String(rand()%4 + 1);
    String bpm = String(rand()%40 + 60);
    String temp = String(random(7) + 35);
    String resp = String(random(7) + 35);
    String pres = String(random(7) + 35);
    String msg = "{\"type\" : 0, \"col\" : " + col + ", \"rssi\": " + strength + ", \"user_addr\" : " + String(idOp) + ", \"msg_counter\": " + String(counter++) + ", \"bpm\": " + bpm + ", \"temp\": " + temp + ", \"resp\": " + resp + ", \"pres\": " + pres + "}";
    client.publish("/sentinel/logs", msg);
    Serial.println("published: " + msg);
    startTime = millis();
  }*/
}
