# coding: utf-8
from sqlalchemy import Boolean, Column, Float, DateTime, ForeignKey, Integer, String, Table, ForeignKeyConstraint
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


class Light(Base):
    __tablename__ = 'light'

    room_id = Column(ForeignKey('room.room_id'), primary_key=True)
    light_id = Column(String, primary_key = True)
    name = Column(String, nullable=False) 
    
    room = relationship('Room')

class Light_Operation(Base):
    __tablename__ = "light_operation"

    light_id = Column(String, primary_key=True)
    room_id = Column(String, nullable=False)
    time = Column(DateTime, primary_key=True)
    turnon = Column(Boolean, nullable=False)
    color_y = Column(Float, nullable=False)
    color_x = Column(Float, nullable=False)
    brightness = Column(Integer, nullable=False)

    __table_args__ = (ForeignKeyConstraint([light_id, room_id], [Light.light_id, Light.room_id]), {})

    light = relationship('Light')
    

class Motion_Sensor(Base):
    __tablename__ = 'motion_sensor'

    room_id = Column(ForeignKey('room.room_id'), primary_key=True)
    sensor_id = Column(String, primary_key=True)
    name = Column(String, nullable = False)

    room = relationship('Room')

class Motion_Sensor_Operation(Base):
    __tablename__ = "motion_sensor_operation"

    sensor_id = Column(String, primary_key=True)
    room_id = Column(String, nullable=False)
    time = Column(DateTime, primary_key=True)
    detection = Column(Boolean, nullable=False)

    __table_args__ = (ForeignKeyConstraint([sensor_id, room_id], [Motion_Sensor.sensor_id, Motion_Sensor.room_id]), {})

    motion_sensor = relationship('Motion_Sensor')

class Power_Plug(Base):
    __tablename__ = 'power_plug'

    room_id = Column(ForeignKey('room.room_id'), primary_key=True)
    plug_id = Column(String, primary_key=True)
    name = Column(String, nullable = False)

    room = relationship('Room')

class Power_Plug_Operation(Base):
    __tablename__ = "power_plug_operation"

    plug_id = Column(String, primary_key=True)
    room_id = Column(String, nullable=False)
    time = Column(DateTime, primary_key=True)
    turnon = Column(Boolean, nullable=False)

    __table_args__ = (ForeignKeyConstraint([plug_id, room_id], [Power_Plug.plug_id, Power_Plug.room_id]), {})

    power_plug = relationship('Power_Plug')


