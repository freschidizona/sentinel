// BRACCIALETTO
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>
#include <SPI.h>
#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <EloquentTinyML.h>
#include "Neural.h"

#define OLED_SDA 21
#define OLED_SCL 22
#define LORA_CS 18
#define LORA_RST 23
#define LORA_DI0 26
#define BUTTON_C 14
#define WIRE Wire

#define NUMBER_OF_INPUTS 5
#define NUMBER_OF_OUTPUTS 1
#define TENSOR_ARENA_SIZE 2 * 1024
Eloquent::TinyML::TfLite<NUMBER_OF_INPUTS, NUMBER_OF_OUTPUTS, TENSOR_ARENA_SIZE> ml;

Adafruit_SSD1306 display = Adafruit_SSD1306(128, 32, &WIRE);
BLEServer *pServer;
BLECharacteristic *alertCharacteristic;
BLECharacteristic *aggregator;
BLEDescriptor *alertDescriptor;
BLEDescriptor *aggregatorDescriptor;

String deviceName = "operator";
long startTime;
long startTimeAlert;
uint32_t age;
uint32_t sex;
bool alive = true;

static BLEUUID serviceUUID("A28A843A-C062-4ED5-A488-616144F818EC");
static BLEUUID alertUUID("45AF0DA2-4B15-4903-A6B4-99274A7EE68C");
static BLEUUID aggregatorUUID("A847C4E6-9E1C-4AC6-B805-2EC0CDE3A73C");

static BLEUUID desc_alertUUID("4433B5DE-5B4C-47EC-98B7-3C800467EBA0");
static BLEUUID desc_aggregatorUUID("12C2F9AD-6D11-4C73-8350-0BDC112E7A30");

class MyServerCallbacks : public BLEServerCallbacks
{
  void onConnect(BLEServer *pServer)
  {
    Serial.println("A client connected");
  };

  void onDisconnect(BLEServer *pServer)
  {
    Serial.println("A client disconnected");
    BLEDevice::startAdvertising();
  }
};

void displayString(String str)
{
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.println(str);
  display.display();
}

void setup()
{
  Serial.begin(115200);
  startTime = millis();
  startTimeAlert = millis();
  srand(time(NULL));

  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  displayString("Operator ready");

  age = random(20, 60);
  sex = random(100) > 50 ? 0 : 1;
  Serial.println("Age: " + String(age));
  Serial.println("Sex: " + String(sex));

  ml.begin(Neural);

  BLEDevice::init(deviceName.c_str());
  pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());
  BLEService *pService = pServer->createService(serviceUUID);
  if (pService == nullptr)
  {
    for (;;)
    {
      Serial.println("Unable to start service");
      delay(1000);
    }
  }

  alertCharacteristic = pService->createCharacteristic(alertUUID, BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_WRITE | BLECharacteristic::PROPERTY_NOTIFY);
  aggregator = pService->createCharacteristic(aggregatorUUID, BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_NOTIFY);

  alertDescriptor = new BLEDescriptor(desc_alertUUID);
  alertDescriptor->setValue("Alert");
  alertCharacteristic->addDescriptor(alertDescriptor);
  alertCharacteristic->setValue("0");

  aggregatorDescriptor = new BLEDescriptor(desc_aggregatorUUID);
  aggregatorDescriptor->setValue("Data");
  aggregator->addDescriptor(aggregatorDescriptor);
  aggregator->setValue("");

  pService->start();
  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(serviceUUID);
  pAdvertising->setScanResponse(true);
  pAdvertising->setMinPreferred(0x06);
  BLEDevice::startAdvertising();
  Serial.println("Advertising started");
}

void loop()
{
  String value = alertCharacteristic->getValue().c_str();
  if (millis() - startTime > 10000 && value == "0")
  {

    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(0, 0);

    int bpm = alive ? random(40, 202) : 0;
    display.println("BPM: " + String(bpm));
    Serial.println("BPM: " + String(bpm));

    int temp = alive ? random(35, 42) : 20;
    display.println("Temp: " + String(temp));
    Serial.println("Temp: " + String(temp));

    int chol = alive ? random(600) : 0;
    display.println("Chol: " + String(chol));
    Serial.println("Chol: " + String(chol));

    int sug = alive ? random(50, 200) : 0;
    display.println("Sug: " + String(sug));
    Serial.println("Sug: " + String(sug));

    float inputs[5] = {age, sex, float(chol), float(sug > 120 ? 1 : 0), float(bpm)};
    float result = ml.predict(inputs);
    Serial.println("Result: " + String(result));

    if (result >= 0.9)
    {
      alive = false;
      Serial.println("mroto");
    }
    else if (result >= 0.4)
    {
      displayString("Attenzione: valori insoliti.");
      alertCharacteristic->setValue("1");
      Serial.println("'tenzione");
    }

    char buff[100];

    sprintf(buff, "%d;%d;%d;%d;%d\0", bpm, temp, chol, sug, alive ? 0 : 1);

    aggregator->setValue(buff);

    display.display();

    startTime = millis();
  }

  if (millis() - startTimeAlert > 1000 && value == "2")
  {
    Serial.println("alert ACK");
    displayString("I rinforzi sono in arrivo.");
    alertCharacteristic->setValue("0");
    delay(5000);
    startTimeAlert = millis();
  }
}
