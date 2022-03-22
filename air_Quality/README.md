# AirQuality_UseCase
In this project, we are analyzing the air quality data from scd_30 sensor.

Hardware_Requirements:

<ol>
    <li>RaspberryPi</li>
    <li>SCD_30 Sensor</li>
</ol>

FastAPI for AirQuality_Sensor_Data

The remote connection is established between the raspi and windows through the socket programming and air quality data is stored in the postgresql database using the fastAPI. The SCD_30 sensor is connected with the raspberry pi based on the pin connections as shown below.
The list of API's are used for performing CRUD operations for the air quality use case.  The fastAPI is connected to the PostgreSQL database with the SQLAlchemy library and the data can be stored and retrieved from the database with the CRUD operations in API .

The Http Verbs and its usage are as follows: 

<ul>
    <li> **POST** - Creates the record with the data sent through the request body of this operation.</li>
    <li> **GET**- Retrieves the records from database and data can be filtered with the request parameters. </li>
    <li> **PUT** - Update data for parameters in the request body on already existing records in database. </li>
    <li> **DELETE**- Delete the record from database tables based on request parameters.<br/>
</li>
</ul>

