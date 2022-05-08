#include <SPI.h>
#include <Ethernet.h>
#include <ArduinoJson.h>
#include <Adafruit_SCD30.h>

Adafruit_SCD30  scd30;
byte mac[] = { 0xA8, 0x61, 0x0A, 0xAE, 0x74, 0x2F };
IPAddress ip(192, 168, 1, 113);
EthernetClient client;

int portNumber = 8000;
String HTTP_METHOD = "POST"; // or POST
char server[]  = "https://c257-193-171-38-186.ngrok.io";
const char* resource   = "/Room/AirQuality/";

float co2;
float temperature;
float humidity;
String result;

void setup() {
  initializeSensor();
  initializeEthernet();
}

void loop() {
  getSensorData();
  if (connect(server, portNumber)) {
    if (sendRequest(server, resource) && skipResponseHeaders()) {
      Serial.print("HTTP POST request finished.");
    }
  }
 // disconnect();
  wait();
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
    //jsonObjects["time"]=str(datetime.fromtimestamp(time.time()))
    jsonObjects["data"][0] = scd30.CO2;
    jsonObjects["data"][1] =  scd30.temperature;
    jsonObjects["data"][2] =  scd30.relative_humidity;
    serializeJson(jsonObjects, Serial);

  } else {
    // Serial.println("No data");
  }
  delay(100);

  return;
}
void initializeEthernet() {
  if (!Ethernet.begin(mac)) {
    Serial.println("Failed to configure Ethernet");
    return;
  }
  Serial.println("Ethernet ready");
  delay(1000);
  IPAddress ip = Ethernet.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);
}
bool connect(const char* hostName, int portNumber) {
  Serial.print("Connect to ");
  Serial.println(hostName);

  bool ok = client.connect(hostName, portNumber);

  Serial.println(ok ? "Connected" : "Connection Failed!");
  return ok;
}

// Send the HTTP POST request to the server
bool sendRequest(const char* host, const char* resource) {

  Serial.print("POST ");
  Serial.println(resource);
  client.print("POST ");
  client.print(resource);
  client.println(" HTTP/1.1");
  client.print("Host: ");
  client.println(host);
  client.println("Connection: close\r\nContent-Type: application/json");
  client.print("\r\n");
  client.println();

  while (client.connected()) {
    if (client.available()) {
      //Read incoming byte from the server and print to the serial monitor
      char c = client.read();
      Serial.print(c);
    }
  }

  delay(1000);
  if (client.connected()) {
    client.stop();
  }
  delay(6000);

  return true;
}

// Skip HTTP headers so that we are at the beginning of the response's body
bool skipResponseHeaders() {
  // HTTP headers end with an empty line
  char endOfHeaders[] = "\r\n\r\n";

  // client.setTimeout(HTTP_TIMEOUT);
  bool ok = client.find(endOfHeaders);

  if (!ok) {
    Serial.println("No response or invalid response!");
  }
  return ok;
}

// Close the connection with the HTTP server
void disconnect() {
  Serial.println("Disconnect");
  client.stop();
}

// Pause for a 1 minute
void wait() {
  Serial.println("Wait 60 seconds");
  delay(1000);
}
