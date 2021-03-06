from ast import And
from asyncio.log import logger
from datetime import datetime
import uvicorn
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from session import db_Session,conn 
from databases import Database 
from schema import Room,Airqualityproperty,Door,Light,Window,Ventilator,RoomToDoorRelations
from fastAPI_models import Room_Object,Update_RoomObject,AirQuality_Properties_Object,AirQuality_Temperature_Object,AirQuality_Humidity_Object,AirQuality_Co2_Object,Doors_Object,Door_Operation_Object,Lights_Object,Light_Operation_Object,Windows_Object,Window_Operation_Object,Ventilators_Object,Ventilator_Operation_Object,Room_Door_Relation_Object,Room_Door_Operation_Object
from typing import List
from sqlalchemy import and_

database = Database(settings.DATABASE_URL)

app = FastAPI(title=settings.PROJECT_NAME)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
cur = conn.cursor()
                
# room
@app.post("/Rooms/",response_model=Room_Object, status_code = status.HTTP_201_CREATED)
async def add_Room(addRoom:Room_Object):
    db_classes = Room(room_id=addRoom.room_id,room_size=addRoom.room_size,measurement_unit=addRoom.measurement_unit)
    try:
        db_Session.add(db_classes)
        db_Session.flush()
        db_Session.commit()
    except Exception as ex:
        logger.error(f"{ex.__class__.__name__}: {ex}")
        db_Session.rollback()
   
    return addRoom
 
@app.get("/Rooms/", response_model=List[Room_Object], status_code = status.HTTP_200_OK)
async def get_AllRoom_Details():
    """ query = 'SELECT * FROM room'
    cur.execute(query)
    for i in cur:
        print(i) """
    results=db_Session.query(Room).all()
    return results         

@app.get("/Room/{room_id}/", response_model=List[Room_Object], status_code = status.HTTP_200_OK)
async def get_Specific_Room(room_id:str):
    specificRoomDetail=db_Session.query(Room).filter(Room.room_id==room_id).all()        
    return specificRoomDetail

@app.put("/Room/{room_id}",status_code = status.HTTP_200_OK)
async def update_RoomDetails(room_id:str,request:Update_RoomObject):
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

@app.post("/Room/AirQuality/", response_model=AirQuality_Properties_Object, status_code = status.HTTP_201_CREATED)
async def add_AirQuality_Properties(addAirQuality:AirQuality_Properties_Object):
    db_AQP=Airqualityproperty(room_id=addAirQuality.room_id,ventilator=addAirQuality.ventilator,totalnumberofpeople=addAirQuality.totalnumberofpeople,co2=addAirQuality.co2,co2measurementunit=addAirQuality.co2measurementunit,temperature=addAirQuality.temperature,temperaturemeasurementunit=addAirQuality.temperaturemeasurementunit,humidity=addAirQuality.humidity,humiditymeasurementunit=addAirQuality.humiditymeasurementunit,time=addAirQuality.time)
    try:
        db_Session.add(db_AQP)
        db_Session.flush()
        db_Session.commit()
    except Exception as ex:
        logger.error(f"{ex.__class__.__name__}: {ex}")
        db_Session.rollback()
    return addAirQuality

@app.get("/Room/AirQuality/", response_model=AirQuality_Properties_Object, status_code = status.HTTP_200_OK)
async def get_AirQuality_Rooms():
    
    AQPresults=db_Session.query(Airqualityproperty).all()
      
    return AQPresults         
  
@app.get("/Room/{room_id}/AirQuality/temperature/{timestamp}/", response_model=List[AirQuality_Temperature_Object], status_code = status.HTTP_200_OK)
async def get_AirQuality_Temperature(room_id:str,timestamp:datetime):
    AQPTemperature=db_Session.query(Airqualityproperty.room_id,Airqualityproperty.temperature,Airqualityproperty.temperaturemeasurementunit,Airqualityproperty.totalnumberofpeople,Airqualityproperty.ventilator,Airqualityproperty.time).filter(Airqualityproperty.room_id==room_id,Airqualityproperty.time==timestamp).all()
    return AQPTemperature

@app.get("/Room/{room_id}/AirQuality/humidity/{timestamp}", response_model=List[AirQuality_Humidity_Object], status_code = status.HTTP_200_OK)
async def get_AirQuality_Humidity(room_id:str,timestamp:datetime):
    AQPHumidity=db_Session.query(Airqualityproperty.room_id,Airqualityproperty.humidity,Airqualityproperty.humiditymeasurementunit,Airqualityproperty.totalnumberofpeople,Airqualityproperty.ventilator,Airqualityproperty.time).filter(Airqualityproperty.room_id==room_id,Airqualityproperty.time==timestamp).all()
    return AQPHumidity

@app.get("/Room/{room_id}/AirQuality/co2/{timestamp}/", response_model=List[AirQuality_Co2_Object], status_code = status.HTTP_200_OK)
async def get_AirQuality_Co2(room_id:str,timestamp:datetime):
    AQPCo2=db_Session.query(Airqualityproperty.room_id,Airqualityproperty.co2,Airqualityproperty.co2measurementunit,Airqualityproperty.totalnumberofpeople,Airqualityproperty.ventilator,Airqualityproperty.time).filter(Airqualityproperty.room_id==room_id,Airqualityproperty.time==timestamp).all()
    return AQPCo2    


# lights
@app.post("/Room/Light/", response_model=Lights_Object, status_code=status.HTTP_201_CREATED)
async def add_light(addLight: Lights_Object):
    addLight=Light(room_id=addLight.room_id,light_id=addLight.light_id,turnon=addLight.turnon,energyconsumption=addLight.energyconsumption,energyconsumptionunit=addLight.energyconsumptionunit,time=addLight.time)
    try:
        db_Session.add(addLight)
        db_Session.flush()
        db_Session.commit()
    except Exception as ex:
        logger.error(f"{ex.__class__.__name__}: {ex}")
        db_Session.rollback()
    
    return addLight

@app.get("/Room/{room_id}/Light/", response_model=List[Lights_Object], status_code=status.HTTP_200_OK)
async def get_All_Lights(room_id: str):
    getAllLights=db_Session.query(Light).filter(Light.room_id==room_id).all()
    return getAllLights

@app.get("/Room/{room_id}/Light/{light_id}/", response_model=List[Lights_Object], status_code=status.HTTP_200_OK)
async def get_Specific_Light(room_id: str,light_id: str):
    getSpecificLight=db_Session.query(Light).filter(Light.room_id==room_id,Light.light_id==light_id).all()
    return getSpecificLight

@app.get("/Room{room_id}/Light{light_id}/isOn{timestamp}", response_model=Lights_Object, status_code=status.HTTP_200_OK)
async def check_Light(room_id: str,light_id: str,time:datetime):
    checkLight=db_Session.query(Light).filter(Light.room_id==room_id,Light.light_id==light_id,Light.time==time)
    return checkLight      

@app.put("/Room/{room_id}/Light/{light_id}", status_code=status.HTTP_200_OK)
async def update_light(room_id: str,light_id:str,request: Light_Operation_Object):
    updateLight=db_Session.query(Light).filter(Light.room_id==room_id,Light.light_id==light_id)
    if not updateLight.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Light with the id {light_id} is not available in room {room_id}')
    updateLight.update({'turnon':request.turnon,'time':request.time})
    db_Session.commit()
    return {"code":"success","message":"updated light settings"}
 
@app.delete("/Room/{room_id}/Light/{light_id}", status_code=status.HTTP_200_OK)
async def delete_light(room_id: str,light_id: str):
    deleteLight=db_Session.query(Light).filter(Light.room_id==room_id,Light.light_id==light_id).one()
    if not delete_light:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Light with the id {light_id} is not available in room {room_id}') 
    db_Session.delete(deleteLight)
    db_Session.commit()
    return {"code":"success","message":f"deleted light with id {light_id} from room {room_id}"} 
  
# windows
@app.post("/Room/Windows/", response_model=Windows_Object, status_code=status.HTTP_201_CREATED)
async def create_Windows(addWindows: Windows_Object):
    db_window=Window(room_id=addWindows.room_id,window_id=addWindows.window_id,isopen=addWindows.isopen,time=addWindows.time)
    try:
        db_Session.add(db_window)
        db_Session.flush()
        db_Session.commit()
    except Exception as ex:
        logger.error(f"{ex.__class__.__name__}: {ex}")
        db_Session.rollback()
    
    return addWindows

@app.get("/Room/{room_id}/Windows/", response_model=List[Windows_Object], status_code=status.HTTP_200_OK)
async def get_All_Windows(room_id: str):
    get_AllWindow=db_Session.query(Window).filter(Window.room_id==room_id).all()
    return get_AllWindow    

@app.get("/Room/{room_id}/Windows/{window_id}/", response_model=List[Windows_Object], status_code=status.HTTP_200_OK)
async def get_Specific_Window(room_id: str,window_id:str):
    get_SpecificWindow=db_Session.query(Window).filter(Window.room_id==room_id,Window.window_id==window_id).all()
    return get_SpecificWindow

@app.put("/Room/{room_id}/Windows/{window_id}", status_code=status.HTTP_200_OK)
async def update_window(room_id: str,window_id:str,request: Window_Operation_Object):
    updateWindow=db_Session.query(Window).filter(Window.room_id==room_id,Window.window_id==window_id)
    if not updateWindow.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Window with the id {window_id} is not available in room {room_id}')
    updateWindow.update({'isopen':request.isopen,'time':request.time})
    db_Session.commit()
    return {"code":"success","message":"updated window settings"}

@app.delete("/Room/{room_id}/Windows/{window_id}", status_code=status.HTTP_200_OK)
async def delete_window(room_id: str,window_id: str):
    deleteWindow=db_Session.query(Window).filter(Window.room_id==room_id,Window.window_id==window_id).one()
    if not deleteWindow:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Window with the id {window_id} is not available in room {room_id}')
    db_Session.delete(deleteWindow)
    db_Session.commit()
    return {"code":"success","message":f"deleted window with id {window_id} from room {room_id}"} 
 
#ventilators
@app.post("/Room/Ventilators/", response_model=Ventilators_Object, status_code=status.HTTP_201_CREATED)
async def create_Ventilators(addVentilators: Ventilators_Object):
    db_ventilator = Ventilator(room_id=addVentilators.room_id,ventilator_id=addVentilators.ventilator_id,turnon=addVentilators.turnon,time=addVentilators.time)
    try:
        db_Session.add(db_ventilator)
        db_Session.flush()
        db_Session.commit()
    except Exception as ex:
        logger.error(f"{ex.__class__.__name__}: {ex}")
        db_Session.rollback()
    return addVentilators 

@app.get("/Room/{room_id}/Ventilators/", response_model=List[Ventilators_Object], status_code=status.HTTP_200_OK)
async def get_All_Ventilators(room_id:str):
    getVentilators=db_Session.query(Ventilator).filter(Ventilator.room_id==room_id).all()
    return getVentilators

@app.get("/Room/{room_id}/Ventilators/{ventilator_id}/", response_model=List[Ventilators_Object], status_code=status.HTTP_200_OK)
async def get_Specific_Ventilator(room_id:str,ventilator_id:str):
    getSpecificVentilators=db_Session.query(Ventilator).filter(Ventilator.room_id==room_id,Ventilator.ventilator_id==ventilator_id).all()
    return getSpecificVentilators

@app.put("/Room/{room_id}/Ventilators/{ventilator_id}", status_code=status.HTTP_200_OK)
async def update_ventilators(room_id:str,ventilator_id:str,request: Ventilator_Operation_Object):
    updateVentilator=db_Session.query(Ventilator).filter(Ventilator.room_id==room_id,Ventilator.ventilator_id==ventilator_id)
    if not updateVentilator.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Ventilator with the id {ventilator_id} is not available in room {room_id}')
    updateVentilator.update({'turnon':request.turnon,'time':request.time})
    db_Session.commit()
    return {"code":"success","message":"updated ventilator settings"}

@app.delete("/Room/{room_id}/Ventilators/{ventilator_id}", status_code=status.HTTP_200_OK)
async def delete_ventilator(room_id: str,ventilator_id:str):
    deleteVentilator=db_Session.query(Ventilator).filter(Ventilator.room_id==room_id,Ventilator.ventilator_id==ventilator_id).one()
    if not deleteVentilator:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Ventilator with the id {ventilator_id} is not available in room {room_id}')
    db_Session.delete(deleteVentilator)
    db_Session.commit()
    return {"code":"success","message":f"deleted ventilator with id {ventilator_id} from room {room_id}"} 

# doors
@app.post("/Room/Doors/", response_model=Doors_Object, status_code=status.HTTP_201_CREATED)
async def add_Doors(addDoors: Doors_Object):
    db_doors = Door(room_id=addDoors.room_id,door_id=addDoors.door_id,door_lock=addDoors.door_lock,connectsdoor=addDoors.connectsdoor,time=addDoors.time)
    try:
        db_Session.add(db_doors)
        db_Session.flush()
        db_Session.commit()
    except Exception as ex:
        logger.error(f"{ex.__class__.__name__}: {ex}")
        db_Session.rollback()
    return addDoors

@app.get("/Room/{room_id}/Doors/", response_model=List[Doors_Object], status_code=status.HTTP_200_OK)
async def get_AllDoors(room_id:str):
    getDoors=db_Session.query(Door).filter(Door.room_id==room_id).all()
    return getDoors
@app.get("/Room/{room_id}/Doors/{door_id}", response_model=List[Doors_Object], status_code=status.HTTP_200_OK)
async def get_SpecificDoor(room_id:str,door_id:str):
    getDoors=db_Session.query(Door).filter(Door.room_id==room_id,Door.door_id==door_id).all()
    return getDoors

@app.put("/Room/{room_id}/Doors/{door_id}", status_code=status.HTTP_200_OK)
async def update_door(room_id:str,door_id:str,request: Door_Operation_Object):
    updateDoor=db_Session.query(Door).filter(Door.room_id==room_id,Door.door_id==door_id)
    if not updateDoor.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Door with the id {door_id} is not available in room {room_id}')
    updateDoor.update({'door_lock':request.door_lock,'time':request.time})
    db_Session.commit()
    return {"code":"success","message":"updated door settings"}

@app.delete("/Room/{room_id}/Doors/{door_id}",status_code=status.HTTP_200_OK)
async def delete_door(room_id: str,door_id: str):
   deleteDoor=db_Session.query(Door).filter(Door.door_id==door_id,Door.room_id==room_id).one()
   if not deleteDoor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Door with the id {door_id} is not available in room {room_id}')
   db_Session.delete(deleteDoor)
   db_Session.commit()
   return {"code":"success","message":f"deleted door with id {door_id} from room {room_id}"}

# room_to_door_relation
@app.post("/Room_to_Door_Relation/", response_model=Room_Door_Relation_Object, status_code=status.HTTP_201_CREATED)
async def add_Room_Door_Relation(addRoomDoorRelation: Room_Door_Relation_Object):
    db_room_door_relation = RoomToDoorRelations(room_id=addRoomDoorRelation.room_id,door_id=addRoomDoorRelation.door_id)
    try:
        db_Session.add(db_room_door_relation)
        db_Session.flush()
        db_Session.commit()
    except Exception as ex:
        logger.error(f"{ex.__class__.__name__}: {ex}")
        db_Session.rollback()
    return addRoomDoorRelation

@app.get("/Room_to_Door_Relation/{room_id}/", response_model=List[Room_Door_Relation_Object], status_code=status.HTTP_200_OK)
async def get_Room_Door_Relation(room_id:str):
    getRoomDoorRelation=db_Session.query(RoomToDoorRelations).filter(RoomToDoorRelations.room_id==room_id).all()
    return getRoomDoorRelation

@app.delete("/Room_to_Door_Relation/{room_id}/{door_id}",status_code=status.HTTP_200_OK)
async def delete_Room_Door_Relation(room_id: str,door_id:str):
   deleteRoomDoorRelation=db_Session.query(RoomToDoorRelations).filter(and_(RoomToDoorRelations.room_id==room_id, RoomToDoorRelations.door_id==door_id)).one()
   if not deleteRoomDoorRelation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Room with the id {room_id} is not available')
   db_Session.delete(deleteRoomDoorRelation)
   db_Session.commit()
   return {"code":"success","message":f"deleted room to door relation with room id {room_id} and door id {door_id}"}

if __name__ == "__main__":
    uvicorn.run("main:app",host="localhost", port=8000, reload=True)