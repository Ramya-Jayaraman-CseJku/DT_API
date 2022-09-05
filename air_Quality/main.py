from asyncio.log import logger
from datetime import datetime
from typing import List
from pip import main
import uvicorn
from fastapi import FastAPI, status,HTTPException,Depends
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from session import db_Session
#from session import conn
from databases import Database
from sqlalchemy.orm import Session
# import the schema 
from schema import Room,Airqualityproperty,AirqualityEnergyconsumption

#import db models
import models as _models

database = Database(settings.DATABASE_URL)

app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
#cur = conn.cursor()
# room
@app.post("/Rooms/",response_model=_models.Room_Object, status_code = status.HTTP_201_CREATED)

async def add_Room(addRoom:_models.Room_Object):
    db_classes = Room(room_id=addRoom.room_id,people_count=addRoom.people_count,room_size=addRoom.room_size,measurement_unit=addRoom.measurement_unit)
    try:
        db_Session.add(db_classes)
        db_Session.flush()
        db_Session.commit()
    except Exception as ex:
        logger.error(f"{ex.__class__.__name__}: {ex}")
        db_Session.rollback()
   
    return addRoom
 
@app.get("/Rooms/", response_model=List[_models.Room_Object], status_code = status.HTTP_200_OK)
async def get_AllRoom_Details():
    results=db_Session.query(Room).all()
    return results         

@app.get("/Room/{room_id}/", response_model=List[_models.Room_Object], status_code = status.HTTP_200_OK)
async def get_Specific_Room(room_id:str):
    specificRoomDetail=db_Session.query(Room).filter(Room.room_id==room_id).all()        
    return specificRoomDetail

@app.put("/Room/{room_id}",status_code = status.HTTP_200_OK)
async def update_RoomDetails(room_id:str,request:_models.Update_RoomObject):
    updateRoomDetail=db_Session.query(Room).filter(Room.room_id==room_id)
    if not updateRoomDetail.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Room with the id {room_id} is not available')
    updateRoomDetail.update({'room_size':request.room_size,'measurement_unit':request.measurement_unit})
    db_Session.commit()
    return {"code":"success","message":"updated room"}

@app.delete("/Room/{room_id}", status_code = status.HTTP_200_OK)
async def delete_Room(room_id:str):
    deleteRoom=db_Session.query(Room).filter(Room.room_id==room_id).one()
    if not deleteRoom:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Room with the room id {room_id} is not found')
    db_Session.delete(deleteRoom)
    db_Session.commit()
    return {"code":"success","message":f"deleted room with id {room_id}"} 

# airQualityinRoom

@app.post("/Room/AirQuality/", response_model=_models.AirQuality_Properties_Object, status_code = status.HTTP_201_CREATED)
async def add_AirQuality_Properties(addAirQuality:_models.AirQuality_Properties_Object):
    db_AQP=Airqualityproperty(room_id=addAirQuality.room_id,device_id=addAirQuality.device_id,ventilator=addAirQuality.ventilator,co2=addAirQuality.co2,co2measurementunit=addAirQuality.co2measurementunit,temperature=addAirQuality.temperature,temperaturemeasurementunit=addAirQuality.temperaturemeasurementunit,humidity=addAirQuality.humidity,humiditymeasurementunit=addAirQuality.humiditymeasurementunit,time=addAirQuality.time)
    try:
        db_Session.add(db_AQP)
        db_Session.flush()
        db_Session.commit()
    except Exception as ex:
        logger.error(f"{ex.__class__.__name__}: {ex}")
        db_Session.rollback()
        
    return addAirQuality

@app.get("/Room/{room_id}/AirQuality/", response_model=_models.AirQuality_Properties_Object, status_code = status.HTTP_200_OK)
async def get_AirQuality_Rooms(room_id:str):
    filteredAQPresults= db_Session.query(Airqualityproperty).filter(Airqualityproperty.room_id==room_id)
    AQPresults=filteredAQPresults.order_by(Airqualityproperty.time.desc()).first()
    return AQPresults
    
@app.get("/Room/{room_id}/AirQuality/temperature/{timestamp}/", response_model=List[_models.AirQuality_Temperature_Object], status_code = status.HTTP_200_OK)
async def get_AirQuality_Temperature(room_id:str,timestamp:datetime):
    AQPTemperature=db_Session.query(Airqualityproperty.room_id,Airqualityproperty.temperature,Airqualityproperty.temperaturemeasurementunit,Airqualityproperty.ventilator,Airqualityproperty.time).filter(Airqualityproperty.room_id==room_id,Airqualityproperty.time==timestamp).all()
    return AQPTemperature

@app.get("/Room/{room_id}/AirQuality/humidity/{timestamp}", response_model=List[_models.AirQuality_Humidity_Object], status_code = status.HTTP_200_OK)
async def get_AirQuality_Humidity(room_id:str,timestamp:datetime):
    AQPHumidity=db_Session.query(Airqualityproperty.room_id,Airqualityproperty.humidity,Airqualityproperty.humiditymeasurementunit,Airqualityproperty.ventilator,Airqualityproperty.time).filter(Airqualityproperty.room_id==room_id,Airqualityproperty.time==timestamp).all()
    return AQPHumidity

@app.get("/Room/{room_id}/AirQuality/co2/{timestamp}/", response_model=List[_models.AirQuality_Co2_Object], status_code = status.HTTP_200_OK)
async def get_AirQuality_Co2(room_id:str,timestamp:datetime):
    AQPCo2=db_Session.query(Airqualityproperty.room_id,Airqualityproperty.co2,Airqualityproperty.co2measurementunit,Airqualityproperty.ventilator,Airqualityproperty.time).filter(Airqualityproperty.room_id==room_id,Airqualityproperty.time==timestamp).all()
    return AQPCo2    

#Devices_EnergyConsumption_UseCaseBased

@app.post("/Device/AirQualityEnergyConsumption/", response_model=_models.AirQuality_EnergyConsumption, status_code = status.HTTP_201_CREATED)
async def add_Device_EC(addAirQualityEC:_models.AirQuality_EnergyConsumption):
    db_AQ_EC=AirqualityEnergyconsumption(room_id=addAirQualityEC.room_id,device_id=addAirQualityEC.device_id,operation=addAirQualityEC.operation,ventilator=addAirQualityEC.ventilator,co2=addAirQualityEC.co2,co2measurementunit=addAirQualityEC.co2measurementunit,temperature=addAirQualityEC.temperature,temperaturemeasurementunit=addAirQualityEC.temperaturemeasurementunit,humidity=addAirQualityEC.humidity,humiditymeasurementunit=addAirQualityEC.humiditymeasurementunit,bus_voltage=addAirQualityEC.bus_voltage,shunt_voltage=addAirQualityEC.shunt_voltage,load_voltage=addAirQualityEC.load_voltage,current_consumed=addAirQualityEC.current_consumed,power_consumed=addAirQualityEC.power_consumed,bus_measurementunit=addAirQualityEC.bus_measurementunit,shunt_measurementunit=addAirQualityEC.shunt_measurementunit,load_measurementunit=addAirQualityEC.load_measurementunit,current_measurementunit=addAirQualityEC.current_measurementunit,power_measurementunit=addAirQualityEC.power_measurementunit,time=addAirQualityEC.time)
    try:
        db_Session.add(db_AQ_EC)
        db_Session.flush()
        db_Session.commit()
    except Exception as ex:
        logger.error(f"{ex.__class__.__name__}: {ex}")
        db_Session.rollback()
        
    return addAirQualityEC

@app.get("/Device/{device_id}/AirQualityEnergyConsumption/", response_model=_models.AirQuality_EnergyConsumption, status_code = status.HTTP_200_OK)
async def get_Device_EC(device_id:str):
        filteredECresults= db_Session.query(AirqualityEnergyconsumption).filter(AirqualityEnergyconsumption.device_id==device_id)
        ECresults=filteredECresults.order_by(AirqualityEnergyconsumption.time.desc()).first()
        return ECresults
    
