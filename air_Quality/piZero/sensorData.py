import time
from scd30_i2c import SCD30
import sys
from datetime import datetime,timezone
import json 
import requests

def sensor_data():          # ANY DATA YOU WANT TO SEND WRITE YOUR SENSOR CODE HERE
    scd30 = SCD30()
    scd30.set_measurement_interval(2)
    scd30.start_periodic_measurement()
    time.sleep(2)
    try:
      while True:
        if scd30.get_data_ready():
         m = scd30.read_measurement()
         if m is not None:
          print("CO2: {m[0]:.2f}ppm, temp: {m[1]:.2f}'C, rh: {m[2]:.2f}%")
          CO2 = round(m[0],2)
          Temp = round(m[1],2)
          Humidity=round(m[2],2)
          my_sensor = "{},{},{}".format(CO2,Temp,Humidity)
          return my_sensor                            # return data seperated by comma
         else:
          print('cannot receive sensor measurements!')
    except KeyboardInterrupt:
          print('Interrupted with keyboard!')
          sys.exit(0)

def post_SensorData_API(airQualityData):
    co2, temp, humidity = airQualityData.split(",")
    jsonObjects={}
    url="https://c06e-140-78-42-122.eu.ngrok.io/Room/AirQuality/"
    headers = {
    'Content-Type':'application/json', 
    'Accept':'application/json'}

    jsonObjects['room_id']='Room_S3_0090'
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
  

def my_server():
   
     my_data = sensor_data()
     post_SensorData_API(my_data)
     

if __name__ == '__main__':
        while 1:
            my_server()       