//ANCHOR
#include <Arduino.h>
#include <LoRa.h>
#include "BLEDevice.h"
#include "BLEScan.h"
#include <SPI.h>
#include "lista.h"
#include <string.h>
#include <vector>

int col_num = 1;

std::vector<String> specialMessageAddresses;
String specialMessage = "Reinforcements are coming. Stay safe.";

int msg_counter = 1;
DoublyLinkedList* listaMessaggi;

BLEClient* pClient;

void sendMessage(String msg){
  Serial.println("Sending packet: " + msg);
  LoRa.beginPacket();
  LoRa.print(msg);
  LoRa.endPacket();
  msg_counter++;
}

#pragma region BLEClientInit

static BLEUUID serviceUUID("65614e24-b2c1-40db-9329-c656a6efa0d6");
static BLEUUID    charUUID_1("3e54bfef-5b68-4c48-8133-11b79592ac0e");
static BLEUUID    charUUID_2("1d3a79ea-0bdc-4c00-a365-dc4a0eb5e170");

static BLEAdvertisedDevice* myDevice;
BLERemoteCharacteristic* pRemoteChar_1;
BLERemoteCharacteristic* pRemoteChar_2;
BLERemoteService* pRemoteService;

class MyAdvertisedDeviceCallbacks: public BLEAdvertisedDeviceCallbacks {
  void onResult(BLEAdvertisedDevice advertisedDevice) {
  }
};

#pragma endregion

#define ss 18
#define rst 14
#define dio0 26

long startTime;
long startTimeMsg;

String addArray[10] = {
  "d4PoKWwUlPd9ZwfQ",
  "peN3WiStdYMx5Ru0",
  "H73hd5v9AgfWCzFz",
  "8U6Mq33m2gJ3L1pq",
  "6dDIHaOrTEETqtiZ",
  "mT90CvzCEvwgnUaM",
  "nmq3ZUv0BShyZC9P",
  "fZLy8NfCmH4KxM5n",
  "MiDa6KHtQjahvkDw",
  "j5PtRCStMab37ACp",
};

void setup() {
  Serial.begin(115200);
  startTime = millis();
  startTimeMsg = millis();
  Serial.println("LoRa Sender");
  LoRa.setPins(ss, rst, dio0);
  while (!LoRa.begin(866E6)) {
    Serial.println(".");
    delay(500);
  }
  LoRa.setSyncWord(0xF3);
  Serial.println("LoRa Initializing OK!");

  listaMessaggi = new DoublyLinkedList();
  
  BLEDevice::init("");
  pClient = BLEDevice::createClient();
  BLEScan* pBLEScan = BLEDevice::getScan();
  pBLEScan->setInterval(1349);
  pBLEScan->setWindow(449);
  pBLEScan->setActiveScan(true);
  pBLEScan->setAdvertisedDeviceCallbacks(NULL);
  pBLEScan->start(5);
}

void loop() {
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    Serial.print("Received packet '");
    while (LoRa.available()) {
      String LoRaData = LoRa.readString();
      Serial.println(LoRaData);
      if(LoRaData.substring(LoRaData.indexOf("\"type\": ")+1, LoRaData.indexOf(",")) == "2"){
        specialMessageAddresses.push_back(LoRaData.substring(LoRaData.indexOf("\"user_addr\": ")+1, LoRaData.indexOf(", ")));
        Serial.println("Arrivato un messaggio speciale");
      }
      else if(listaMessaggi->findNode(LoRaData) == NULL){
        listaMessaggi->insertTail(LoRaData);
        Serial.println("Invio in broadcast il messaggio");
        sendMessage(LoRaData);
      }
      else{
        Serial.println("Scarto il messaggio");
      }
    }
  }

  if (millis() - startTimeMsg > 5000){
    //String col = String(rand()%100 + 1);
    String rssi = String(static_cast <float> (rand()) / (static_cast <float> (RAND_MAX/2))*100 - 1);
    String user_addr = addArray[random(10)+1];
    String bpm = String(random(80) + 60);
    String temp = String(random(35) + 7);
    String col = String(random(10) + 1);
    //String msg = "{\"col\" : " + col + ", \"strength\": " + strength + ", \"user_id\" : " + user_addr + ", \"msg_counter\": " + msg_counter + ", \"type\": 0 }";
    String msg = "{\"type\": 0 , \"col\" : " + String(col) + ", \"rssi\": " + rssi + ", \"user_addr\" : \"" + user_addr + "\", \"msg_counter\": " + String(msg_counter) + ", \"bpm\": " + bpm + ", \"temp\": " + temp + " }";
    sendMessage(msg);
    startTimeMsg = millis();
  }
  
  if(millis() - startTime > 5000){
    Serial.println("Scanning for operators...");
    BLEScanResults results = BLEDevice::getScan()->start(5);
    Serial.print(results.getCount());
    Serial.print(" bluetooth devices found:");
    Serial.println("");
    for(int i=0; i < results.getCount(); i++){
      Serial.print(String(i+1));
      Serial.print(") ");
      Serial.print(results.getDevice(i).getAddress().toString().c_str());
      if(results.getDevice(i).haveName()){
        Serial.print(", ");
        Serial.print(results.getDevice(i).getName().c_str());
      }
      Serial.println("");
      
      if(results.getDevice(i).haveName() && String(results.getDevice(i).getName().c_str()) == "operator"){
        Serial.print("Attempting connection to operator ");
        Serial.println(results.getDevice(i).getAddress().toString().c_str());
        pClient->connect(results.getDevice(i).getAddress());
        Serial.print("Connected to operator ");
        Serial.println(results.getDevice(i).getAddress().toString().c_str());

        pRemoteService = pClient->getService(serviceUUID);
        pRemoteChar_1 = pRemoteService->getCharacteristic(charUUID_1);
        pRemoteChar_2 = pRemoteService->getCharacteristic(charUUID_2);

        if(pRemoteChar_1 == nullptr || pRemoteChar_2 == nullptr){
          Serial.print("Disconnected from ");
          Serial.print(results.getDevice(i).getName().c_str());
          Serial.println(". No char UUID found.");
          pClient->disconnect();
          continue;
        }
        Serial.print("BPM: ");
        String bpm = String(pRemoteChar_1->readUInt32());
        Serial.println(bpm);

        Serial.print("Temperature: ");
        String temp = String(pRemoteChar_2->readUInt32());
        Serial.println(temp);

        String user_addr = String(results.getDevice(i).getAddress().toString().c_str());
        String rssi = String(results.getDevice(i).getRSSI());
        String msg = "{\"type\": 0 , \"col\" : " + String(col_num) + ", \"rssi\": " + rssi + ", \"user_addr\" : \"" + user_addr + "\", \"msg_counter\": " + String(msg_counter) + ", \"bpm\": " + bpm + ", \"temp\": " + temp + " }";
        sendMessage(msg);

        std::vector<String>::iterator it = std::find(specialMessageAddresses.begin(), specialMessageAddresses.end(), String(results.getDevice(i).getAddress().toString().c_str()));
        if (it != specialMessageAddresses.end()){
          
          // send message to BLE server somehow :/


          specialMessageAddresses.erase(it);
        }
          

        pClient->disconnect();
      }
    }
    Serial.println("");
    startTime = millis();
  }

}
