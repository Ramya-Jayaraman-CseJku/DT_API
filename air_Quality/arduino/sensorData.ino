#include <SPI.h>
#include <Ethernet.h>
#include <ArduinoJson.h>
#include <Adafruit_SCD30.h>

Adafruit_SCD30  scd30;
byte mac[] = { 0xA8, 0x61, 0x0A, 0xAE, 0x74, 0x2F };
IPAddress ip(192, 168, 1, 113);
EthernetClient client;

int HTTP_PORT = 80;
String HTTP_METHOD = "POST"; // or POST
char HOST_NAME[]  = "https://58df-140-78-42-122.ngrok.io";
String PATH_NAME   = "/Room/AirQuality/";
char json[50];
float co2;
float temperature;cd
float humidity;
String result;

void setup() {
  initializeSensor();
 
  sendRequest();
}

void loop() {
  getSensorData();
  
  //wait();
}

void initializeSensor() {
  Serial.begin(9600);
  while (!Serial) delay(10);     // will pause Zero, Leonardo, etc until serial console opens
  Serial.println("Adafruit SCD30 test!");
  // Try to initialize!
  if (!scd30.begin()) {
    Serial.println("Failed to find SCD30 chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("SCD30 Found!");
  Serial.print("Measurement Interval: ");
  Serial.print(scd30.getMeasurementInterval());
  Serial.println(" seconds");
}
void getSensorData() {
  // allocate the memory for the document
  StaticJsonDocument<256> jsonObjects;

  if (scd30.dataReady()) {
    Serial.println("Data available!");

    if (!scd30.read()) {
      Serial.println("Error reading sensor data");
      return;
    }
    jsonObjects["room_id"] = "Room_S3_0090";
    jsonObjects["ventilator"] = "no";
    jsonObjects["totalnumberofpeople"] = 3;
    jsonObjects["co2measurementunit"] = "ppm";
    jsonObjects["temperaturemeasurementunit"] = "degree celcius";
    jsonObjects["humiditymeasurementunit"] = "rh";
    jsonObjects["co2"] = (float)scd30.CO2;
    jsonObjects["temperature"] = scd30.temperature;
    jsonObjects["humidity"] = scd30.relative_humidity;
    jsonObjects["time"]="2022-05-10T00:24:17.863Z";
    //jsonObjects["data"][0] = scd30.CO2;
    //jsonObjects["data"][1] =  scd30.temperature;
   // jsonObjects["data"][2] =  scd30.relative_humidity;
    serializeJson(jsonObjects, client);
    
    
  } else {
    // Serial.println("No data");
  }
  delay(100);

  return;
}

void sendRequest() {
   if (!Ethernet.begin(mac)) {
    Serial.println("Failed to configure Ethernet");
    return;
  }
  Serial.println("Ethernet ready");
  delay(1000);
  IPAddress ip = Ethernet.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);
  
  if (client.connect(HOST_NAME, HTTP_PORT)) {
    // if connected:
    Serial.println("Connected to server");
    String room_id = "Room_S3_0089";
    String queryString = String("?room_id=") + String(room_id);
    // HTTP GET Request send HTTP header
    client.println(HTTP_METHOD + " " + PATH_NAME + " HTTP/1.1");
    client.println("Host: " + String(HOST_NAME));
    client.println("Content-Type:application/json");
    client.println("Accept:application/json");
    client.println("Connection: close");
    client.println(); // end HTTP header
    client.println(queryString);
    Serial.print(HTTP_METHOD + " " + PATH_NAME + " HTTP/1.1");
    Serial.println();
    Serial.print("Host: " + String(HOST_NAME));
    Serial.println();
    while (client.connected()) {
      if (client.available()) {
        // read an incoming byte from the server and print it to serial monitor:
        char c = client.read();
        Serial.print(c);
      }
    }
    // the server's disconnected, stop the client:
    client.stop();
    Serial.println();
    Serial.println("disconnected");
  } else {// if not connected:
    Serial.println("connection failed");
  }
  return;
}
