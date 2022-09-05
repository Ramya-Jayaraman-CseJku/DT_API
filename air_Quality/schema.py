# coding: utf-8
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Room(Base):
    __tablename__ = 'room'

    room_id = Column(String, primary_key=True)
    people_count = Column(Integer, nullable=False)
    room_size = Column(Integer, nullable=False)
    measurement_unit = Column(String, nullable=False)


class Airqualityproperty(Base):
    __tablename__ = 'airqualityproperties'

    room_id = Column(ForeignKey('room.room_id'), nullable=False)
    device_id = Column(String, nullable=False)
    ventilator = Column(String, nullable=False)
    co2 = Column(Float(53), nullable=False)
    co2measurementunit = Column(String, nullable=False)
    temperature = Column(Float(53), nullable=False)
    temperaturemeasurementunit = Column(String, nullable=False)
    humidity = Column(Float(53), nullable=False)
    humiditymeasurementunit = Column(String, nullable=False)
    time = Column(DateTime, primary_key=True)

    room = relationship('Room')

class AirqualityEnergyconsumption(Base):
    __tablename__ = 'airquality_energyconsumption'

    room_id = Column(ForeignKey('room.room_id'), nullable=False)
    device_id = Column(String, nullable=False)
    operation = Column(String, nullable=False)
    ventilator = Column(String, nullable=False)
    co2 = Column(Float(53), nullable=False)
    co2measurementunit = Column(String, nullable=False)
    temperature = Column(Float(53), nullable=False)
    temperaturemeasurementunit = Column(String, nullable=False)
    humidity = Column(Float(53), nullable=False)
    humiditymeasurementunit = Column(String, nullable=False)
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
    time = Column(DateTime(True), primary_key=True)

    room = relationship('Room')