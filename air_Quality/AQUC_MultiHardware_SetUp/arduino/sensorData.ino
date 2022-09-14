#include <SPI.h>
#include <Adafruit_SCD30.h>


Adafruit_SCD30  scd30;

void setup() {
  initializeSensor();
 
}

void loop() {
  getSensorData();
}

void initializeSensor() {
  Serial.begin(9600);
  while (!Serial) delay(10);     // will pause Zero, Leonardo, etc until serial console opens
  //Serial.println("Adafruit SCD30 test!");
  // Try to initialize!
  if (!scd30.begin()) {
    //Serial.println("Failed to find SCD30 chip");
    while (1) {
      delay(10);
    }
  }
  //Serial.println("SCD30 Found!");
  //Serial.print("Measurement Interval: ");
  //Serial.print(scd30.getMeasurementInterval());
  //Serial.println(" seconds");
}
void getSensorData() {
 
  if (scd30.dataReady()) {
    //Serial.println("Data available!");

    if (!scd30.read()) {
      Serial.println("Error reading sensor data");
      return;
    }
    
  
    Serial.print(scd30.CO2);
    Serial.print(",");
    Serial.print(scd30.temperature,4);
    Serial.print(",");
    Serial.println(scd30.relative_humidity,4);
   
  } else {
    // Serial.println("No data");
  }
  delay(100);

  return;
}

