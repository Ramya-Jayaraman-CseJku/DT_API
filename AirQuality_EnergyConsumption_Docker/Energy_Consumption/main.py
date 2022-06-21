from asyncio.log import logger
from datetime import datetime
from typing import List
from pip import main
import uvicorn
from fastapi import FastAPI, status,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from session import db_Session 
from databases import Database

# import the schema 
from schema import Energyconsumption,Energyconsumptionmicrocontroller

#import db models
from models import Energyconsumption_Object, Energyconsumption_mc
database = Database(settings.DATABASE_URL)



app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# windows
""" @app.post("/Energyconsumption/",response_model=Energyconsumption_Object, status_code = status.HTTP_201_CREATED)

async def add_EnergyConsumption(addEC:Energyconsumption_Object):
    db_classes = Energyconsumption(device_type=addEC.device_type,operation=addEC.operation,time=addEC.time,total_elapsed_time=addEC.total_elapsed_time,total_processor_energy=addEC.total_processor_energy,average_process_power=addEC.average_process_power,total_dram_energy=addEC.total_dram_energy,average_dram_power=addEC.average_dram_power)
    try:
        db_Session.add(db_classes)
        db_Session.flush()
        db_Session.commit()
    except Exception as ex:
        logger.error(f"{ex.__class__.__name__}: {ex}")
        db_Session.rollback()
   
    return addEC
 
@app.get("/Energyconsumption/", response_model=Energyconsumption_Object, status_code = status.HTTP_200_OK)
async def get_Energyconsumption():
    results=db_Session.query(Energyconsumption).order_by(Energyconsumption.time.desc()).first()
    return results         

@app.get("/Energyconsumption/{device_id}/", response_model=Energyconsumption_Object, status_code = status.HTTP_200_OK)
async def get_Energyconsumption_Device(device_id:str):
    specificRoomDetail=db_Session.query(Energyconsumption).filter(Energyconsumption.device_type==device_id)       
    latestRecord=specificRoomDetail.order_by(Energyconsumption.time.desc()).first()
    return latestRecord
 """
# mcu
@app.post("/EnergyconsumptionMC/",response_model=Energyconsumption_mc, status_code = status.HTTP_201_CREATED)

async def add_EnergyConsumption(addECMC:Energyconsumption_mc):
    db_classes = Energyconsumptionmicrocontroller(device_type=addECMC.device_type,operation=addECMC.operation,time=addECMC.time,bus_voltage=addECMC.bus_voltage,shunt_voltage=addECMC.shunt_voltage,load_voltage=addECMC.load_voltage,current_consumed=addECMC.current_consumed,power_consumed=addECMC.power_consumed,bus_measurementunit=addECMC.bus_measurementunit,shunt_measurementunit=addECMC.shunt_measurementunit,load_measurementunit=addECMC.load_measurementunit,current_measurementunit=addECMC.current_measurementunit,power_measurementunit=addECMC.power_measurementunit)
    try:
        db_Session.add(db_classes)
        db_Session.flush()
        db_Session.commit()
    except Exception as ex:
        logger.error(f"{ex.__class__.__name__}: {ex}")
        db_Session.rollback()
    return addECMC

@app.get("/EnergyconsumptionMC/", response_model=Energyconsumption_mc, status_code = status.HTTP_200_OK)
async def get_Energyconsumption():
    results=db_Session.query(Energyconsumptionmicrocontroller).order_by(Energyconsumptionmicrocontroller.time.desc()).first()
    return results         

@app.get("/EnergyconsumptionMC/{device_id}/", response_model=Energyconsumption_mc, status_code = status.HTTP_200_OK)
async def get_Energyconsumption_Device(device_id:str):
    ECSpecificDevice=db_Session.query(Energyconsumptionmicrocontroller).filter(Energyconsumptionmicrocontroller.device_type==device_id)
    latestRecord=ECSpecificDevice.order_by(Energyconsumptionmicrocontroller.time.desc()).first()        
    return latestRecord
