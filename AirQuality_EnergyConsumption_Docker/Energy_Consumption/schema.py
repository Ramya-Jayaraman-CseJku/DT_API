# coding: utf-8
from sqlalchemy import Column, DateTime, Float, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Energyconsumption(Base):
    __tablename__ = 'energyconsumption'

    device_type = Column(String, nullable=False)
    operation = Column(String, nullable=False)
    time = Column(DateTime(True), primary_key=True)
    total_elapsed_time = Column(Float(53), nullable=False)
    total_processor_energy = Column(Float(53), nullable=False)
    average_process_power = Column(Float(53), nullable=False)
    total_dram_energy = Column(Float(53), nullable=False)
    average_dram_power = Column(Float(53), nullable=False)

class Energyconsumptionmicrocontroller(Base):
    __tablename__ = 'energy_consumption_mcu'

    device_type = Column(String, nullable=False)
    operation = Column(String, nullable=False)
    time = Column(DateTime(True), primary_key=True)
    bus_voltage = Column(Float(53), nullable=False)
    shunt_voltage = Column(Float(53), nullable=False)
    load_voltage = Column(Float(53), nullable=False)
    current_consumed = Column(Float(53), nullable=False)
    power_consumed = Column(Float(53), nullable=False)
    bus_measurementunit = Column(String, nullable=False)
    shunt_measurementunit = Column(String, nullable=False)
    load_measurementunit = Column(String, nullable=False)
    current_measurementunit = Column(String, nullable=False)
    power_measurementunit = Column(String, nullable=False)