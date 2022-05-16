#!/usr/bin/env python
# -*- coding: utf-8 -*-
# lsusb to check device name
#dmesg | grep "tty" to find port name

import serial,time
from datetime import datetime
import json 
import requests

def getArduinoSensorData():
     with serial.Serial("/dev/ttyACM0", 9600, timeout=1) as arduino:
        time.sleep(0.1) #wait for serial to open
        if arduino.isOpen():
            print("{} connected!".format(arduino.port))
            try:
                while True:
                    if arduino.in_waiting > 0:
                     serialData=arduino.readline().decode('utf-8').rstrip()
                     return serialData
            except KeyboardInterrupt:
                print("KeyboardInterrupt has been caught.")

def post_SensorData_API(airQualityData):
    print(airQualityData)
    co2, temp, humidity = airQualityData.split(",")
    print(co2)
    jsonObjects={}
    url="https://0313-193-171-38-41.ngrok.io/Room/AirQuality/"
    headers = {
    'Content-Type':'application/json', 
    'Accept':'application/json'}

    jsonObjects['room_id']='Room_S3_0090'
    jsonObjects['device_id']='Arduino-1'
    jsonObjects['ventilator']='no'
    jsonObjects['totalnumberofpeople']=3
    jsonObjects['co2measurementunit']='ppm'
    jsonObjects['temperaturemeasurementunit']='degree celcius'
    jsonObjects['humiditymeasurementunit']='rh'
    jsonObjects['co2']=float(co2)
    jsonObjects['temperature']=float(temp)
    jsonObjects['humidity']=float(humidity)
    jsonObjects['time']=str(datetime.fromtimestamp(time.time()))
    jsonformat=json.dumps(jsonObjects)
    print(jsonformat)
    postdata=requests.post(url,headers=headers,data=jsonformat)
    response=postdata.text
    
    if postdata.status_code==201:
        print('Sensor data successfully sent to server!')
    else:
        print(postdata.text+'Failed to post Sensor data to server!')
    return response
  

def getData():
    arduinoData=getArduinoSensorData()
    post_SensorData_API(arduinoData)
if __name__ == '__main__':
    while 1:
        getData()
    
   