//ANCHOR
#include <Arduino.h>
#include <LoRa.h>
#include "BLEDevice.h"
#include "BLEScan.h"
#include <SPI.h>
#include <string.h>
#include <vector>
#include <Preferences.h>
#include <AsyncTCP.h>  //https://github.com/me-no-dev/AsyncTCP using the latest dev version from @me-no-dev
#include <DNSServer.h>
#include <ESPAsyncWebServer.h>	//https://github.com/me-no-dev/ESPAsyncWebServer using the latest dev version from @me-no-dev
#include <esp_wifi.h>			//Used for mpdu_rx_disable android workaround

#define ss 18
#define rst 14
#define dio0 26

const char *ssid = "captive";
const char *password = "operator";

int id = 0;
int msg_counter = 1;
long startTime;
long startTimeMsg;
long startTimePing;
Preferences preferences;
String anchor_id;
/*String addrArray[4] = {
  "6a:d9:cc:2b:7c:7a",
  "42:7e:ba:bc:dc:0c",
  "d2:d9:de:8a:37:c4",
  "87:dc:c2:89:76:b5",
  "6dDIHaOrTEETqtiZ",
  "mT90CvzCEvwgnUaM",
  "nmq3ZUv0BShyZC9P",
  "fZLy8NfCmH4KxM5n",
  "MiDa6KHtQjahvkDw",
  "j5PtRCStMab37ACp",
};*/

std::vector<String> specialMessageAddresses;
std::vector<String> listaMessaggi;
BLEClient* pClient;
String specialMessage = "Reinforcements are coming. Stay safe.";

#pragma region CaptivePortal 

const IPAddress localIP(4, 3, 2, 1);		   // the IP address the web server, Samsung requires the IP to be in public space
const IPAddress gatewayIP(4, 3, 2, 1);		   // IP address of the network should be the same as the local IP for captive portals
const IPAddress subnetMask(255, 255, 255, 0);  // no need to change: https://avinetworks.com/glossary/subnet-mask/

const String localIPURL = "http://4.3.2.1";	 // a string version of the local IP with http, used for redirecting clients to your webpage

const char index_html[] PROGMEM = R"=====(
  <!DOCTYPE html> <html>
    <head>
      <title>Sentinel Captive Portal</title>
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <style>
        html, body{
            width: 100%;
            height: 100%;
            font-family: Arial;
            position: relative;
        }
        #container{
            display: flex;
            flex-direction: column;
            align-items: center;
        }
    </style>
    <body>
        <div id="container">
            <h1>Sentinel</h1>
            <h3>Registra un anchor</h3>
            <form action="/get">
                <input type="number" min="1" placeholder="Id" name="id" required><br>
                <input type="submit" value="Concludi setup">
            </form>
        </div>
    </body>
</html>
)=====";

DNSServer dnsServer;
AsyncWebServer server(80);

void setUpDNSServer(DNSServer &dnsServer, const IPAddress &localIP) {
// Define the DNS interval in milliseconds between processing DNS requests
#define DNS_INTERVAL 30
	// Set the TTL for DNS response and start the DNS server
	dnsServer.setTTL(3600);
	dnsServer.start(53, "*", localIP);
}

void startSoftAccessPoint(const char *ssid, const char *password, const IPAddress &localIP, const IPAddress &gatewayIP) {
	// Set the WiFi mode to access point and station
	WiFi.mode(WIFI_MODE_AP);
	// Define the subnet mask for the WiFi network
	const IPAddress subnetMask(255, 255, 255, 0);
	// Configure the soft access point with a specific IP and subnet mask
	WiFi.softAPConfig(localIP, gatewayIP, subnetMask);
	// Start the soft access point with the given ssid, password, channel, max number of clients
	WiFi.softAP(ssid, password, 6, 0, 4);
	// Disable AMPDU RX on the ESP32 WiFi to fix a bug on Android
	esp_wifi_stop();
	esp_wifi_deinit();
	wifi_init_config_t my_config = WIFI_INIT_CONFIG_DEFAULT();
	my_config.ampdu_rx_enable = false;
	esp_wifi_init(&my_config);
	esp_wifi_start();
	vTaskDelay(100 / portTICK_PERIOD_MS);  // Add a small delay
}

void setUpWebserver(AsyncWebServer &server, const IPAddress &localIP) {
	server.on("/connecttest.txt", [](AsyncWebServerRequest *request) { request->redirect("http://logout.net"); });	// windows 11 captive portal workaround
	server.on("/wpad.dat", [](AsyncWebServerRequest *request) { request->send(404); });								// Honestly don't understand what this is but a 404 stops win 10 keep calling this repeatedly and panicking the esp32 :)

	// Background responses: Probably not all are Required, but some are. Others might speed things up?
	// A Tier (commonly used by modern systems)
  server.on("/generate_204", [](AsyncWebServerRequest *request) { request->redirect(localIPURL); });		   // android captive portal redirect
  server.on("/redirect", [](AsyncWebServerRequest *request) { request->redirect(localIPURL); });			   // microsoft redirect
	server.on("/hotspot-detect.html", [](AsyncWebServerRequest *request) { request->redirect(localIPURL); });  // apple call home
  server.on("/canonical.html", [](AsyncWebServerRequest *request) { request->redirect(localIPURL); });	   // firefox captive portal call home
	server.on("/success.txt", [](AsyncWebServerRequest *request) { request->send(200); });					   // firefox captive portal call home
	server.on("/ncsi.txt", [](AsyncWebServerRequest *request) { request->redirect(localIPURL); });			   // windows call home

  server.on("/favicon.ico", [](AsyncWebServerRequest *request) { request->send(404); });	// webpage icon

  server.on("/get", HTTP_GET, [](AsyncWebServerRequest *request) {
    Serial.println("RECEIVED GET");
		String inputMessage;
    if (request->hasParam("id")) {
        inputMessage = request->getParam("id")->value();
        id = inputMessage.toInt();
        preferences.putInt("id", id);
        Serial.println(inputMessage);
    }
    request->send(200, "text/html", R"=====(
        <!DOCTYPE html> <html>
            <head>
            <title>Sentinel Captive Portal</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            </head>
            <style>
                html, body{
                    width: 100%;
                    height: 100%;
                    font-family: Arial;
                    position: relative;
                }
                #container{
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                }
            </style>
            <body>
                <div id="container">
                    <h1>Configurazione terminata</h1>
                    <h3>Puoi chiudere la pagina.</h3>
                </div>
            </body>
        </html>
        )=====");
    ESP.restart();
	});

	server.on("/", HTTP_ANY, [](AsyncWebServerRequest *request) {
		AsyncWebServerResponse *response = request->beginResponse(200, "text/html", index_html);
		response->addHeader("Cache-Control", "public,max-age=31536000");  // save this file to cache for 1 year (unless you refresh)
		request->send(response);
		Serial.println("Served Basic HTML Page");
	});

	server.onNotFound([](AsyncWebServerRequest *request) {
		request->redirect(localIPURL);
		Serial.print("onnotfound ");
		Serial.print(request->host());
		Serial.print(" ");
		Serial.print(request->url());
		Serial.print(" sent redirect to " + localIPURL + "\n");
	});
}

#pragma endregion

void sendMessage(String msg){
  Serial.println("Sending packet: " + msg);
  LoRa.beginPacket();
  LoRa.print(msg);
  LoRa.endPacket();
}

#pragma region BLEClientInit

static BLEUUID serviceUUID("65614e24-b2c1-40db-9329-c656a6efa0d6");
static BLEUUID alertUUID("105ba674-964b-4a26-bbad-e140950a1588");
static BLEUUID deadUUID("2cce3185-3a35-4b4f-b619-186f82868570");
static BLEUUID ageUUID("48cb68d6-dcae-4b7e-86d2-7a983c22ec60");
static BLEUUID sexUUID("824154e8-1492-476a-bce5-3ab66df089fa");
static BLEUUID bpmUUID("3e54bfef-5b68-4c48-8133-11b79592ac0e");
static BLEUUID tempUUID("1d3a79ea-0bdc-4c00-a365-dc4a0eb5e170");
static BLEUUID colUUID("9f99ac59-6d86-4172-ba8a-cd1d2e640a21");
static BLEUUID sugUUID("c3abe5fb-29e8-4c8d-90fe-6c1f7029abb8");

BLERemoteCharacteristic* alertCharacteristic;
BLERemoteCharacteristic* deadCharacteristic;
BLERemoteCharacteristic* ageCharacteristic;
BLERemoteCharacteristic* sexCharacteristic;
BLERemoteCharacteristic* bpmCharacteristic;
BLERemoteCharacteristic* tempCharacteristic;
BLERemoteCharacteristic* colCharacteristic;
BLERemoteCharacteristic* sugCharacteristic;
BLERemoteService* pRemoteService;

#pragma endregion

void initializedRoutine(){
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    Serial.print("Received packet: ");
    while (LoRa.available()) {
      String LoRaData = LoRa.readString();
      std::vector<String>::iterator it = std::find(listaMessaggi.begin(), listaMessaggi.end(), LoRaData);
      Serial.println(LoRaData);

      if(LoRaData.indexOf("\"type\": 2") >= 0){
        String operator_addr = LoRaData.substring(LoRaData.indexOf("\"worker_addr\": ")+16, LoRaData.indexOf("\", "));
        std::vector<String>::iterator addrIterator = std::find(specialMessageAddresses.begin(), specialMessageAddresses.end(), operator_addr);

        if (addrIterator != specialMessageAddresses.end()){
          specialMessageAddresses.push_back(operator_addr);
          Serial.println("Arrivato un ack per " + operator_addr);
        }
        
      }
      else if (it != listaMessaggi.end()){
        listaMessaggi.push_back(LoRaData);
        Serial.println("Invio in broadcast il messaggio");
        sendMessage(LoRaData);
      }
      else{
        Serial.println("Scarto il messaggio");
      }
    }
  }


  /*if (millis() - startTimeMsg > 2000){
    String user_addr = addrArray[random(4)];
    String bpm = String(random(80) + 60);
    String temp = String(random(7) + 35);
    String col = String(random(10) + 1);
    String msg = "{\"type\": " + String(random(100) > 90 ? "1" : "0")  + ", \"anchor_id\" : " + String(col) + ", \"user_addr\" : \"" + user_addr + "\", \"msg_counter\": " + String(msg_counter) + ", \"bpm\": " + bpm + ", \"temp\": " + temp + " }";
    sendMessage(msg);
    startTimeMsg = millis();
  }*/
  
  if(millis() - startTime > 5000){
    Serial.println("Scanning for operators...");
    BLEScanResults results = BLEDevice::getScan()->start(5);
    Serial.print(results.getCount());
    Serial.println(" bluetooth devices found");
    for(int i=0; i < results.getCount(); i++){
      BLEAdvertisedDevice device = results.getDevice(i);
      String deviceAddress = device.getAddress().toString().c_str();
      String deviceName = device.getName().c_str();
      
      if(device.haveName() && String(deviceName) == "operator"){
        pClient->connect(device.getAddress());
        Serial.print("Connected to operator ");
        Serial.println(deviceAddress);

        pRemoteService = pClient->getService(serviceUUID);
        alertCharacteristic = pRemoteService->getCharacteristic(alertUUID);
        deadCharacteristic = pRemoteService->getCharacteristic(deadUUID);
        ageCharacteristic = pRemoteService->getCharacteristic(ageUUID);
        sexCharacteristic = pRemoteService->getCharacteristic(sexUUID);
        bpmCharacteristic = pRemoteService->getCharacteristic(bpmUUID);
        tempCharacteristic = pRemoteService->getCharacteristic(tempUUID);
        colCharacteristic = pRemoteService->getCharacteristic(colUUID);
        sugCharacteristic = pRemoteService->getCharacteristic(sugUUID);

        String alert = String(alertCharacteristic->readValue().c_str());
        Serial.println("Alert: " + alert);
        if(alert == "1"){
          Serial.println("Sending alert to gateway");
          sendMessage("{\"type\": 1, \"anchor_id\": \"" + anchor_id + "\", \"worker_addr\": \"" + deviceAddress + "\", \"msg_counter\": " + String(msg_counter) + " }");
          msg_counter++;
        }

        String dead = String(deadCharacteristic->readValue().c_str());
        Serial.println("Dead: " + dead);
        if(dead == "1"){
          sendMessage("{\"type\": 5, \"worker_addr\": \"" + deviceAddress + "\", \"anchor_id\": \"" + anchor_id + "\", \"msg_counter\": " + String(msg_counter) + " }");
          msg_counter++;
        }

        String bpm = "50";//String(bpmCharacteristic->readValue().c_str());
        Serial.println("BPM: " + bpm);

        String temp = "50";//String(tempCharacteristic->readValue().c_str());
        Serial.println("Temp: " + temp);

        String chol = "50";//String(colCharacteristic->readValue().c_str());
        Serial.println("Cholesterol: " + chol);

        String sug = "50";//String(sugCharacteristic->readValue().c_str());
        Serial.println("Sugar: " + sug);

        String msg = "{\"type\": 0, \"anchor_id\": \"" + anchor_id + "\", \"worker_addr\": \"" + deviceAddress + "\", \"msg_counter\": " + String(msg_counter) + ", \"bpm\": " + bpm + ", \"temp\": " + temp + ", \"chol\": " + chol + ", \"sug\": " + sug + " }";
        sendMessage(msg);
        msg_counter++;

        std::vector<String>::iterator it = std::find(specialMessageAddresses.begin(), specialMessageAddresses.end(), String(results.getDevice(i).getAddress().toString().c_str()));
        if (it != specialMessageAddresses.end()){
          Serial.println(specialMessage);
          alertCharacteristic->writeValue("2");
          specialMessageAddresses.erase(it);
        }

        pClient->disconnect();
      }
    }
    Serial.println("");
    startTime = millis();
  }

  if (millis() - startTimePing > 10000){
    String msg = "{\"type\": 6, \"anchor_id\" : " + anchor_id + ", \"msg_counter\": " + String(msg_counter) + " }";
    sendMessage(msg);
    msg_counter++;
    startTimePing = millis();
  }
}

void setup() {
  Serial.begin(115200);
  startTime = millis();
  startTimeMsg = millis();
  startTimePing = millis();
  preferences.begin("mangiatorella", false);
  id = preferences.getInt("id");
  Serial.println("Id: " + String(id));

  if(id == 0){
    Serial.println("Activating captive portal");
    startSoftAccessPoint(ssid, password, localIP, gatewayIP);

    setUpDNSServer(dnsServer, localIP);

    setUpWebserver(server, localIP);
    server.begin();
  }
  else{
    LoRa.setPins(ss, rst, dio0);
    while (!LoRa.begin(866E6)) {
      Serial.println(".");
      delay(500);
    }
    LoRa.setSyncWord(0xF3);
    Serial.println("LoRa Initializing OK!");

    BLEDevice::init("");
    anchor_id = String(ESP.getEfuseMac());

    pClient = BLEDevice::createClient();
    BLEScan* pBLEScan = BLEDevice::getScan();
    pBLEScan->setInterval(1349);
    pBLEScan->setWindow(449);
    pBLEScan->setActiveScan(true);
    pBLEScan->start(5);
  }
}

void loop() {
  if(id != 0){
    initializedRoutine();
  }
  else{
    dnsServer.processNextRequest();
  }
}
