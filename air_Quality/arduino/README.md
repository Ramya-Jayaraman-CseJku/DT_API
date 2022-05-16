# AirQuality_UseCase_Arduino

In this project, we are analysing the air quality data from Arduino_UNO_R3. The air quality data from arduino_uno is sent to the server by establishing serial communication between arduino_uno and raspberry_pi_4.  

**Hardware_Requirements:**

<ol>
    <li>RaspberryPi Pico</li>
    <li>Arduino_UNO_R3</li>
    <li>SCD_30 Sensor</li>
</ol>


Arduino IDE:

Arduino  IDE is used for comiling and running the code  in arduino.  For easy communication, we have installed the arduino ide in raspberry pi. 

##### Serial Communication :

##### Raspberry_pi

To establish serial communication between arduino and raspberry_pi, we are using the usb_cable. Plug the usb cable into arduino and connect to the usb_port of the raspberry_pi.  Now we can identify the port in which arduino is connected with pi by executing the following command in pi terminal. Reboot and again execute the ls command.

``ls /dev/tty*``

``sudo reboot``

You should be able to see the port for instance, in our project it is

``/dev/ttyACM0``

Once the port is known, create a new python file and copy paste the [code](https://github.com/Ramya-Jayaraman-CseJku/DT_API/blob/main/air_Quality/arduino/serialComm_Arduino_Raspi.py). The code has function "getArduinoSensorData" ,it establishes serial communication and reads the output from arduino serial output. The function "post_SensorData_API" gets the sensor data and sends it as post request to the fast_api hosted in web using the ngrok.

##### Arduino

Open a new sketch in arduino and copy paste the [code](https://github.com/Ramya-Jayaraman-CseJku/DT_API/blob/main/air_Quality/arduino/sensorData.ino). set the baud rate (speed of communication over the port) of the port. In our case, we have used 9600. Use the same baud rate in raspberry pi code as well for the serial communication. The code uses the adafruit_scd30 library and gets the sensor data from arduino. The adafruit_scd30 library is installed using the arduino ide. Go to Tools-> Manage libraries-> search for adafruit_scd30 and install it in arduino. 

Connect the scd_30 sensor to the arduino board based on the following pin_connections.

vnn= 3.3v(arduino analog input)

GND= GND(arduino digital)

sda= sda(arduino digital)

scl= scl(arduino digital)

once the library is installed and scd_30 sensor is wired, verify and upload the code to the arduino_board.





