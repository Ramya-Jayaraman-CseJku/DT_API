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

CREATE TABLE Light(
	room_id varchar NOT NULL,
	light_id varchar NOT NULL,
	name varchar NOT NULL,
	PRIMARY KEY (room_id, light_id),
	FOREIGN KEY (room_id) REFERENCES Room (room_id)
	ON DELETE CASCADE
);

CREATE TABLE Light_Operation(
	light_id varchar NOT NULL,
	room_id varchar NOT NULL,
	time timestamp NOT NULL,
	turnon BOOLEAN NOT NULL,
	color_x DECIMAL NOT NULL,
	color_y DECIMAL NOT NULL,
	brightness INTEGER NOT NULL,
	PRIMARY KEY (light_id, time),
	FOREIGN KEY (room_id, light_id) REFERENCES Light (room_id, light_id)
	ON DELETE CASCADE
);

SELECT create_hypertable('Light_Operation', 'time');
CREATE INDEX ix_light_id_room_id_time ON Light_Operation (light_id, room_id, time DESC);

CREATE TABLE Motion_Sensor(
    room_id varchar NOT NULL,
	sensor_id varchar NOT NULL,
	name varchar NOT NULL,
	PRIMARY KEY (room_id, sensor_Id),
	FOREIGN KEY (room_id) REFERENCES Room (room_id)
	ON DELETE CASCADE
);

CREATE TABLE Motion_Sensor_Operation(
	sensor_Id varchar NOT NULL,
	room_Id varchar NOT NULL,
	time timestamp NOT NULL,
	detection BOOLEAN NOT NULL,
	PRIMARY KEY (sensor_Id, time),
	FOREIGN KEY(room_id, sensor_id) REFERENCES Motion_Sensor (room_id, sensor_id)
	ON DELETE CASCADE
);

SELECT create_hypertable('Motion_Sensor_Operation', 'time');
CREATE INDEX ix_sensor_id_room_id_time ON Motion_Sensor_Operation (sensor_id, room_id, time DESC);


CREATE TABLE Power_Plug(
	room_Id varchar NOT NULL,
	plug_Id varchar NOT NULL,
	name varchar NOT NULL,
	PRIMARY KEY (room_Id, plug_Id),
	FOREIGN KEY (room_Id) REFERENCES Room (room_Id)
	ON DELETE CASCADE
);

CREATE TABLE Power_Plug_Operation(
	plug_id varchar NOT NULL,
	room_id varchar NOT NULL,
	time timestamp NOT NULL,
	turnon BOOLEAN NOT NULL,
	PRIMARY KEY (plug_id, time),
	FOREIGN KEY (room_id, plug_id) REFERENCES Power_Plug (room_id, plug_id)
	ON DELETE CASCADE
);

SELECT create_hypertable('Power_Plug_Operation', 'time');
CREATE INDEX ix_plug_id_room_id_time ON Power_Plug_Operation (plug_id, room_id, time DESC);
