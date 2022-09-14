# AirQuality_UseCase_PiZero

In this project, we are analysing the air quality data with scd_30 sensor from PiZero in timescale database. The air quality data obtained from sensor is stored in the timescale database in windows machine using the fastAPI. 

##### Hardware_Requirements

<ol>
    <li>RaspberryPiZero</li>
    <li>SCD_30 Sensor</li>
</ol>
##### Set UP PiZero

The PiZero W works without ethernet cable as it has built-in wifi module. The PiZero is accessed using the ssh and operates with wifi of the host computer. The ssh is enabled by creating an empty file named ssh without any extension. Similarly the wifi is set up with credentials in [wpa_supplicant.conf](https://github.com/Ramya-Jayaraman-CseJku/DT_API/tree/main/air_Quality/piZero/wpa_supplicant.conf).

The country code, network ssid and password must be changed based on your country and wifi setup.

Once the wifi and ssh is enabled, connect the PiZero to the system with usb data cable and then access the PiZero with the ip address. The ip address of the PiZero can be found by scanning the list of devices attcahed to the wifi network.

##### sensorData.py

The function sensor_data() measures sensor data from scd30 sensor and the measurements are sent as arguments to the function post_SensorData_API(airQualityData). 

post_SensorData_API function splits the string and gets co2, temperature and humidity values separately and these values are sent as post request to the fast api running in windows machine.

##### Connection between windows and PiZero ngrok

The localhost fast api cannot be accessed directly from other machine, in order to overcome this, the localhost fast api running in port 8000 is hosted in public domain using ngrok. The ngrok tunnels the requests from port 8000 to the public domain. The public domain varies accordingly and has to be replaced in the url.



