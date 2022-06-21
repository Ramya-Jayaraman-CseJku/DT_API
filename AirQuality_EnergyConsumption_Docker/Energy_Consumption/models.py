from sqlite3 import Timestamp
from pydantic import BaseModel
from datetime import datetime

class Energyconsumption_Object(BaseModel):
    device_type : str
    operation : str
    time :Timestamp
    total_elapsed_time  :float
    total_processor_energy  :float
    average_process_power  :float
    total_dram_energy  :float
    average_dram_power  :float
  

    class Config:
        orm_mode = True


class Energyconsumption_mc(BaseModel):
    device_type : str
    operation : str
    time :Timestamp
    bus_voltage  :float
    shunt_voltage  :float
    load_voltage  :float
    current_consumed  :float
    power_consumed  :float
    bus_measurementunit:str
    shunt_measurementunit:str
    load_measurementunit:str
    current_measurementunit:str
    power_measurementunit:str
    
  

    class Config:
        orm_mode = True      