# EnergyConsumption_UseCase_Docker

In this project, we are analysing the energy consumption data from INA_219 current sensor in timescale database.  The tools used for this project are set up as docker images and run with the docker container to run the project set up in client machine.

##### Set up Dockerfile: 

The energy consumption use case project is set up as docker image and is built using the [Dockerfile](https://github.com/Ramya-Jayaraman-CseJku/DT_API/blob/main/air_Quality/fastAPI-AQUC/Dockerfile). The fast API is built with python and SQLAlchemy for database connections. The project dependencies can be installed using the requirements.txt file. Set up the Dockerfile with following specifications,  use python image and install the project dependencies through pip. Set up the working directory and copy the project contents and expose the port in which the project should be run.

##### Set up the docker-compose.yaml:

The [docker-compose.yaml](https://github.com/Ramya-Jayaraman-CseJku/DT_API/blob/main/air_Quality/fastAPI-AQUC/docker-compose.yaml) file specifies instructions for running the docker images as containers. The list of services to run are specified along with runtime parameters. The tables that are used in the project are created automaticallay using the [Database_Schema.sql](https://github.com/Ramya-Jayaraman-CseJku/DT_API/blob/main/energy_Consumption/fastAPI-EC/Database_Schema.sql) when the postgresql database is set up.

 It uses the Dockerfile to build the latest version of the docker image before running.  Navigate to the [project directory](https://github.com/Ramya-Jayaraman-CseJku/DT_API/tree/main/energy_Consumption/fastAPI-EC) and run the following command from the commandline to build and run the containers. This is done using the docker-entrypoint-initdb.d/Database_Schema.sql. This script serves as the entry point for table creation, when we add the new web server in pgadmin with the database credentials. Once the docker containers are running successfully, we can see them from commandline as shown in [!figure](./images/dockerRunning.png)

``docker-compose up``

##### Run the container:

Navigate to the web browser to verify if the docker conatainers are running.

For the simplerest service, navigate to the url http://localhost:8000/docs to view the fast api rest interface.

To verify the postgresql database setup, navigate to the url http://localhost:5050 for viewing the pgadmin interface used for the postgresql database.  Login into the pgAdmin with the credentials username as "pgadmin4@pgadmin.org" and password as "admin" as shown in [!figure](./images/pgAdminLoginCredentials.png)

Add a new web server and database with the credentials from docker-compose.yaml as shown in [!figure](./images/pgAdminDbCredentials.png). 

The hostname as the docker container name "timeScaledb", postgres_user as "postgres", password as "cdlmint" and database as "EC". 

*The server in which the postgresql database is running is the docker conatiner name. This has to be specified rather than the localhost server for docker containers to communicate over the network.   

Once the web server is added, we can see that the tables are automatically created with the Database_Schema.sql script as shown in [!figure](./images/TableCreation.png).

