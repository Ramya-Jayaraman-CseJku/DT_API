# AirQuality_UseCase

In this project, we are analysing the air quality data from scd_30 sensor in timescale database.

Hardware_Requirements:

<ol>
    <li>RaspberryPi</li>
    <li>SCD_30 Sensor</li>
</ol>

Software Installation:

*Install PostgreSQL database in windows based on the instructions.

Download the PostgreSQL installer for windows from the [link]('https://www.postgresql.org/download/windows/'). Follow the installation instructions provided. Choose the components such as PostgreSQL Server, pgAdmin4, command line tools to install. Set up the password, default port for database server and locale.

Verify the PostgreSQL Installation:

Open the command line tool of PostgreSQL(psql). Enter the connection details prompted in CLI. Press Enter to accept the default choices in the square brackets.  The default values are Server-(localhost), Database- name of the database, Port-(5432), Username and Password. Once the authentication is complete, you will be logged into the database.

FastAPI for AirQuality_Sensor_Data

This project establishes remote connection  between the raspi and windows through the socket programming. The air quality data is obtained from sensor and stored in the postgresql database in windows machine using the fastAPI. 

Run the [client.py]('https://github.com/Ramya-Jayaraman-CseJku/DT_API/blob/main/air_Quality/client.py') from raspi to establish remote connection to fastAPI running in windows machine. The fastAPI handles the postgreSQL database connection and CRUD operations on database.

The SCD_30 sensor is connected with the raspberry pi based on the [pin connections]('https://github.com/derlehner/IndoorAirQuality_DigitalTwin_Exemplar/tree/main/physical_twin/hardware_setup').
The list of API's are used for performing CRUD operations for the air quality use case.  The fastAPI is connected to the PostgreSQL database with the SQLAlchemy library and the data can be stored and retrieved from the database with the CRUD operations in API .

The Http Verbs and its usage are as follows: 

<ul>
    <li> POST - Creates the record with the data sent through the request body of this operation.</li>
    <li> GET - Retrieves the records from database and data can be filtered with the request parameters. </li>
    <li> PUT - Update data for parameters in the request body on already existing records in database. </li>
    <li> DELETE - Delete the record from database tables based on request parameters.<br/>
</li>
</ul>

fastAPI Setup:

The [project]('https://github.com/Ramya-Jayaraman-CseJku/DT_API/tree/main/air_Quality/fastAPI-AQUC')  has the requirements.txt file. It contains the dependent libraries that are necessary to run the project. These libraries need to be installed in advance to run the project. Create the virtual environment using the venv python library to install the  libraries. Open the windows terminal and type the following command to create the virtual env. Here 

the library name is venv and next venv is name of the virtual environment.

``python -m venv venv``

Activate the Virtual Environment:

After the virtual environment is created, run the command to activate it.

``env/Scripts/activate``

Install dependencies using Pip:

 Navigate to the [folder]('https://github.com/Ramya-Jayaraman-CseJku/DT_API/tree/main/air_Quality/fastAPI-AQUC') and run the command

``pip install -r requirements.txt``

Run the fastAPI:

Navigate to the [project]('https://github.com/Ramya-Jayaraman-CseJku/DT_API/tree/main/air_Quality/fastAPI-AQUC/app') and run [main.py]('https://github.com/Ramya-Jayaraman-CseJku/DT_API/blob/main/air_Quality/fastAPI-AQUC/app/main.py') from your windows. You can see the fastAPI running in the uvicorn server in port 8080. Navigate to the address in browser('http://localhost:8080/docs') to view the fastAPI GUI.

Once the database and fastAPI is setup in windows, we can perform crud operations from fastAPI to store and retrieve air quality data from raspi to database.



