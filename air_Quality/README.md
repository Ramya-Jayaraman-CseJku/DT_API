# AirQuality_UseCase

In this project, we are analysing the air quality data from scd_30 sensor in timescale database.  Remote connection is established  between the raspi and windows through the socket programming. The air quality data obtained from sensor is stored in the timescale database in windows machine using the fastAPI. 

Hardware_Requirements:

<ol>
    <li>RaspberryPi</li>
    <li>SCD_30 Sensor</li>
</ol>
##### Software Requirements:

*Install PostgreSQL database in windows based on the instructions.

Download the PostgreSQL installer for windows from the [link]('https://www.postgresql.org/download/windows/'). Follow the installation instructions provided. Choose the components such as PostgreSQL Server, pgAdmin4, command line tools to install. Set up the password, default port for database server and locale.

##### Verify the PostgreSQL Installation:

Open the command line tool of PostgreSQL(psql). Enter the connection details prompted in CLI. Press Enter to accept the default choices in the square brackets.  The default values are Server-(localhost), Database- name of the database, Port-(5432), Username and Password. Once the authentication is complete, you will be logged into the database.

##### Setting Up the Postgresql Database:

With the pgAdmin4, a graphical GUI for postgresql database, we can create database, tables and perform query operations.

Login into the pgAdmin4 with the username(postgres) and password.

After successful login , we can create the database AQUC  by right click on the databases and then create database.

![createDatabase](./images/createDatabasePsql.png) 

##### Create Tables:

Right click on the created database in pgAdmin4 and then go to QueryTool for executing the psql commands. Refer the [schema]('https://github.com/Ramya-Jayaraman-CseJku/DT_API/blob/main/air_Quality/Database_Schema_AirQuality.sql.txt') for creation of these tables. copy paste the schema in the query tool for table creation and press F5 or execute button in the tool bar.

![TableCreation](./images/tableCreation.png)



We need two tables ( room and airqualityproperties ) for storing the airquality data. 

*The **room** table should be created first , since the **room_id** of the table is used as the foreign key in the **airqualityproperties** Table.

#### Installation and SetUp of the Timescale Database:

##### 1. Install docker 

Based on the os, install the docker from the [link]('https://docs.docker.com/get-docker/'). For windows os, we need to install the docker desktop, enable the WSL2 feature and install [linux package]('https://docs.microsoft.com/en-in/windows/wsl/install-manual#step-4---download-the-linux-kernel-update-package'). 

##### 2. Set up the timescale databse

We can also set up the timescale database using docker and access them using psql.

Once the docker desktop is setup, execute the command in command line

``docker pull timescale/timescaledb:latest-pg14``

The command pulls the timescale docker image

![timeScale_Image](./images/pullTimescaleImage.png)

##### Run the timescale image from container

The -p flag in command binds the docker container to port 5432, so we can access the port to access the timescale database container. Set the password for postgresql using the POSTGRES_PASSWORD environment variable. If there is no password specified, then the docker disables the password checks for all the users.

``docker run -d --name timescaledb -p 5432:5432 -e POSTGRES_PASSWORD=password timescale/timescaledb:latest-pg14``

if you have the port allocated already , change the port number as shown below.

![port](./images/runContainer.png)

Connect to the postgresql instance as the postgres user 

``psql -U postgres -h localhost ``

After successful login , we can create the database AQUC  using the command from psql command line

``CREATE DATABASE Database_Name;``

We need two tables ( room and airqualityproperties ) for storing the airquality data. Refer the [schema]('https://github.com/Ramya-Jayaraman-CseJku/DT_API/blob/main/air_Quality/Database_Schema_AirQuality.sql.txt') for creation of these tables. Execute the table schema from psql command line and check if the tables are created as shown below.

![figure](./images/Db&Tables.png) 

Once the tables are created then we can run the server first from raspi and then the client in windows and also the fastAPI for storing the data in the tables.

##### Set up Raspberry pi

The SCD_30 sensor is connected with the raspberry pi based on the [pin connections]('https://github.com/derlehner/IndoorAirQuality_DigitalTwin_Exemplar/tree/main/physical_twin/hardware_setup').

Connect to the raspi using ssh from command line as follows

``ssh username@ip-address-of-raspi``

After logging into the raspi, run the [Server.py]('https://github.com/Ramya-Jayaraman-CseJku/DT_API/blob/main/air_Quality/Server.py') for sending data from raspi to windows.

The client.py establishes  remote connection from raspi to windows machine and sends sensor data. The fastAPI handles the postgreSQL database connection and performs CRUD operations on database.

##### fast API

fastAPI written in python used for performing CRUD operations for the air quality use case.  The fastAPI is connected to the PostgreSQL database with the SQLAlchemy library and the data can be stored and retrieved from the database with the CRUD operations in API .

The Http Verbs and its usage are as follows: 

<ul>
    <li> POST - Creates the record with the data sent through the request body of this operation.</li>
    <li> GET - Retrieves the records from database and data can be filtered with the request parameters. </li>
    <li> PUT - Update data for parameters in the request body on already existing records in database. </li>
    <li> DELETE - Delete the record from database tables based on request parameters.<br/>
</li>
</ul>
##### fast API Setup:

Create the virtual environment using the venv python library as shown below and then install the  necessary libraries to run the fastAPI. The project dependent libraries are present in the [requirements.txt]('https://github.com/Ramya-Jayaraman-CseJku/DT_API/blob/main/air_Quality/fastAPI-AQUC/requirements.txt') file. Open the windows terminal and type the following command to create the virtual env as follows:

In the command below, the library name is venv and env is name of the virtual environment.

``python -m venv env``

Activate the Virtual Environment:

After the virtual environment is created, run the command to activate it.

``env/Scripts/activate``

Install dependencies using Pip:

 Navigate to the [folder]('https://github.com/Ramya-Jayaraman-CseJku/DT_API/tree/main/air_Quality/fastAPI-AQUC') and run the command

``pip install -r requirements.txt``

##### Run the fastAPI:

Navigate to the [project]('https://github.com/Ramya-Jayaraman-CseJku/DT_API/tree/main/air_Quality/fastAPI-AQUC/app') and run [main.py]('https://github.com/Ramya-Jayaraman-CseJku/DT_API/blob/main/air_Quality/fastAPI-AQUC/app/main.py') from your windows. You can see the fastAPI running in the uvicorn server in port 8080. Navigate to the address in browser('http://localhost:8080/docs') to view the fastAPI GUI.

Once the server.py is running in the raspberrypi, it sends data to the client machine and then the fastAPI running in the client will send and receive data from the database. We can perform crud operations from fastAPI to store and retrieve air quality data from raspi to database.



