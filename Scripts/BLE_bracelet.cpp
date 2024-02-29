//BRACCIALETTO
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>
#include <SPI.h>
#include <Arduino.h>
#include "lista.h"

BLEServer* pServer = NULL;                        // Pointer to the server
BLECharacteristic* pCharacteristic_1 = NULL;      // Pointer to Characteristic 1
BLECharacteristic* pCharacteristic_2 = NULL;      // Pointer to Characteristic 2
BLEDescriptor *pDescr_1;                          // Pointer to Descriptor of Characteristic 1
BLEDescriptor *pDescr_2;                          // Pointer to Descriptor of Characteristic 2
BLE2902 *pBLE2902_1;                              // Pointer to BLE2902 of Characteristic 1

String deviceName = "operator";
long startTime;

int connectedNum = 0;

uint32_t value = 0;

#define SERVICE_UUID          "65614e24-b2c1-40db-9329-c656a6efa0d6"
#define CHARACTERISTIC_UUID_1 "3e54bfef-5b68-4c48-8133-11b79592ac0e"
#define CHARACTERISTIC_UUID_2 "1d3a79ea-0bdc-4c00-a365-dc4a0eb5e170"

class MyServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
      Serial.println("A client connected");
      connectedNum++;
    };

    void onDisconnect(BLEServer* pServer) {
      Serial.println("A client disconnected");
      connectedNum--;
      BLEDevice::startAdvertising();
    }
};

DoublyLinkedList* listaConnessi;

void setup() {
  Serial.begin(115200);
  startTime = millis();
  BLEDevice::init(deviceName.c_str());
  pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());
  BLEService *pService = pServer->createService(SERVICE_UUID);
  pCharacteristic_1 = pService->createCharacteristic(CHARACTERISTIC_UUID_1,BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_NOTIFY);                   
  pCharacteristic_2 = pService->createCharacteristic(CHARACTERISTIC_UUID_2,BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_NOTIFY);                   

  pDescr_1 = new BLEDescriptor(BLEUUID((uint16_t)0x2901));
  pDescr_1->setValue("BPM");
  pCharacteristic_1->addDescriptor(pDescr_1);

  pDescr_2 = new BLEDescriptor(BLEUUID((uint16_t)0x2901));
  pDescr_2->setValue("Temperature");
  pCharacteristic_2->addDescriptor(pDescr_2);

  pService->start();
  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(SERVICE_UUID);
  pAdvertising->setScanResponse(true);
  pAdvertising->setMinPreferred(0x06);
  BLEDevice::startAdvertising();
  Serial.println("Advertising started");
}

void loop() {
  if(millis() - startTime > 2000){
    uint32_t randValue = random(80) + 40;
    Serial.print("Set BPM value: ");
    Serial.println(randValue);
    pCharacteristic_1->setValue(randValue);

    randValue = random(7) + 35;
    Serial.print("Set Temp value: ");
    Serial.println(randValue);
    pCharacteristic_2->setValue(randValue);

    startTime = millis();
  }
}
