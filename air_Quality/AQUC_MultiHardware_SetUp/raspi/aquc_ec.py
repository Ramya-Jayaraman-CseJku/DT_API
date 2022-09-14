import time
import board
from adafruit_ina219 import INA219
from datetime import datetime,timezone
import json,requests
from scd30_i2c import SCD30
import sys


i2c_bus = board.I2C()

ina219 = INA219(i2c_bus,addr=0x40)

print("ina219 test")

def getRaspiCurrentData():
# measure and display loop
 while True:
    bus_voltage = ina219.bus_voltage  # voltage on V- (load side)
    shunt_voltage = ina219.shunt_voltage  # voltage between V+ and V- across the shunt
    load_voltage = bus_voltage + (shunt_voltage / 1000)
    current = ina219.current  # current in mA
    power = ina219.power  # power in watts

    # INA219 measure bus voltage on the load side. So PSU voltage = bus_voltage + shunt_voltage
    
#     print("Voltage (VIN+) : {:6.3f}   V".format(bus_voltage + shunt_voltage))
#     print("Voltage (VIN-) : {:6.3f}   V".format(bus_voltage))
#     print("Shunt Voltage  : {:8.5f} V".format(shunt_voltage))
#     print("Shunt Current  : {:7.4f}  A".format(current / 1000))
#     print("Power Calc.    : {:8.5f} W".format(bus_voltage * (current / 1000)))
#     print("Power Register : {:6.3f}   W".format(power))
#     print("")
    currentDataRaspi="{},{:.4e},{:.4f},{},{}".format(bus_voltage,shunt_voltage,load_voltage,current,power)
    print(currentDataRaspi)
    #return currentDataRaspi
    # Check internal calculations haven't overflowed (doesn't detect ADC overflows)
    if ina219.overflow:
        print("Internal Math Overflow Detected!")
        print("")

    time.sleep(2)
    return currentDataRaspi
    
def post_CurrentData_API(arduinoCurrentData):
    print(arduinoCurrentData)
    busV,shuntV,loadV,current,power = arduinoCurrentData.split(",")
   
    jsonObjects={}
    url="http://140.78.42.22:8080/EnergyconsumptionMC/"
    headers = {
    'Content-Type':'application/json', 
    'Accept':'application/json'}

    jsonObjects['device_type']='Raspi-4-1'
    jsonObjects['operation']='aquc'
    jsonObjects['bus_voltage']=float(busV)
    jsonObjects['shunt_voltage']=float(shuntV)
    jsonObjects['load_voltage']=float(loadV)
    jsonObjects['current_consumed']=float(current)
    jsonObjects['power_consumed']=float(power)
    jsonObjects['bus_measurementunit']='v'
    jsonObjects['shunt_measurementunit']='mV'
    jsonObjects['load_measurementunit']='v'
    jsonObjects['current_measurementunit']='mA'
    jsonObjects['power_measurementunit']='mW'
    jsonObjects['time']=str(datetime.now(timezone.utc))
    jsonformat=json.dumps(jsonObjects)
    print('ec')
    print(jsonformat)
    postdata=requests.post(url,headers=headers,data=jsonformat)
    response=postdata.text
     
    if postdata.status_code==201:
        print('Current data successfully sent to server!')
    else:
        print(postdata.text+'Failed to post current data to server!')
    return jsonformat
  

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

def post_SensorData_API(airQualityData,currentData):
    co2, temp, humidity = airQualityData.split(",")
    print(currentData)
    busV,shuntV,loadV,current,power = currentData.split(",")
   
    jsonObjects={}
    url="http://140.78.42.22:8000/Room/AirQuality/"
    headers = {
    'Content-Type':'application/json', 
    'Accept':'application/json'}

    jsonObjects['room_id']='Room_S3_0090'
    jsonObjects['device_id']='Raspi-4-1'
    jsonObjects['ventilator']='no'
    jsonObjects['co2']=float(co2)
    jsonObjects['co2measurementunit']='ppm'
    jsonObjects['temperature']=float(temp)
    jsonObjects['temperaturemeasurementunit']='degree celcius'
    jsonObjects['humidity']=float(humidity)
    jsonObjects['humiditymeasurementunit']='rh'
    jsonObjects['time']=str(datetime.now(timezone.utc))
    jsonformat=json.dumps(jsonObjects)
    print('aquc ec')
    print(jsonformat)
    postdata=requests.post(url,headers=headers,data=jsonformat)
    response=postdata.text
    
    if postdata.status_code==201:
        print('Sensor data successfully sent to server!')
    else:
        print(postdata.text+'Failed to post Sensor data to server!')
    return response
  

def my_server():
    raspiCurrentData=getRaspiCurrentData()
    post_CurrentData_API(raspiCurrentData)
    my_data = sensor_data()
    post_SensorData_API(my_data,raspiCurrentData)
     

if __name__ == '__main__':
        while 1:
            my_server()           