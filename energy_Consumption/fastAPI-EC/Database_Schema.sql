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