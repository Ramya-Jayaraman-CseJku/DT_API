import json
import socket
import threading

import time
from datetime import datetime,timezone
import requests

import psycopg2

HOST = '140.78.42.121'  # The server's hostname or IP address
PORT = 65432  # The port used by the server

#get data from Raspi
def process_data_from_Raspi(airQualityData):
    co2, temp, humidity = airQualityData.split(",")
    print(co2, temp, humidity)
    return co2, temp, humidity
#send data to fastAPI
def post_SensorData_API(co2,temp,hum):
    jsonObjects={}
    url="http://localhost:8080/Room/AirQuality/"
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
    jsonObjects['humidity']=float(hum)
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
# insert data into postgresql database
def database(x_co2, y_temperature, z_humidity):
    currentdatetime = datetime.fromtimestamp(time.time())
    dt_time = currentdatetime.strftime("%Y-%m-%d %H:%M:%S")
    try:

        connection = psycopg2.connect(user="postgres",
                                      password="cdlmint",
                                      host="localhost",
                                      port="5432",
                                      database="AQUC")
        cursor = connection.cursor()

        postgres_insert_query =  """INSERT INTO airqualityproperties (room_id,ventilator,totalnumberofpeople, co2,co2measurementunit, temperature,temperaturemeasurementunit, humidity,humiditymeasurementunit,time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
        record_to_insert = ('Room_S3_0090', 'no',4, x_co2,'ppm', y_temperature,'degree celcius',z_humidity,'rh',currentdatetime)
        print(record_to_insert)
        cursor.execute(postgres_insert_query, record_to_insert)

        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into airqualityproperties table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into airqualityproperties table", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed") 
#receive 
def my_client():
    threading.Timer(11, my_client).start()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((HOST, PORT))
        my = input("Enter command ")
        my_inp = my.encode('utf-8')
        s.sendall(my_inp)
        data = s.recv(1024).decode('utf-8')
        Co2, Temperature, Humidity = process_data_from_Raspi(data)
        
        print("Co2- {}".format(Co2))
        print("Temperature- {}".format(Temperature))
        print("Humidity- {}".format(Humidity))
        post_SensorData_API(Co2, Temperature, Humidity)
        database(Co2, Temperature, Humidity)
        #s.close()
        time.sleep(5)

if __name__ == "__main__":
    while 1:
        my_client()
