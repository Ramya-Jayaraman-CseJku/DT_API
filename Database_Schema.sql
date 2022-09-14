CREATE TABLE Room(
	room_Id varchar PRIMARY KEY NOT NULL,
    	people_count int NOT NULL,
	room_Size int NOT NULL,
	measurement_Unit varchar NOT NULL
);

CREATE TABLE AirQualityProperties(
	room_Id varchar  NOT NULL,
    	device_id varchar  NOT NULL,
	ventilator varchar NOT NULL,
	co2 float NOT NULL,
	co2MeasurementUnit varchar NOT NULL,
	temperature float NOT NULL,
	temperatureMeasurementUnit varchar NOT NULL,
	humidity float NOT NULL,
	humidityMeasurementUnit varchar NOT NULL,
	time timestamp with time zone PRIMARY KEY NOT NULL,
	FOREIGN KEY (room_Id) REFERENCES Room (room_Id)
);

CREATE TABLE energy_consumption_mcu
(
    device_type character varying NOT NULL,
    operation character varying NOT NULL,
    "time" timestamp with time zone NOT NULL,
    bus_voltage double precision NOT NULL,
    shunt_voltage double precision NOT NULL,
    load_voltage double precision NOT NULL,
    current_consumed double precision NOT NULL,
    power_consumed double precision NOT NULL,
    bus_measurementunit character varying NOT NULL,
    shunt_measurementunit character varying NOT NULL,
    load_measurementunit character varying NOT NULL,
    current_measurementunit character varying NOT NULL,
    power_measurementunit character varying NOT NULL,
    CONSTRAINT energy_consumption_mcu_pkey PRIMARY KEY ("time")
);

