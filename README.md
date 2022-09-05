# DT_API
#### UseCase-1: Air_Quality

The air quality data such as co2, humidity, and tempertaure is obtained with the scd-30 sensor for analysing the airquality and creating awareness with led notifications in case of higher co2 values in rooms.

#### UseCase-2: Energy_Consumption

The energy consumption of microcontrollers are measured in terms of current, power, and voltage with the INA_219 current sensor for minimising the energy consumption as much as possible.

#### DT_API

The digital twin represents the api that is created for performing the CRUD operations for the airquality  and energy consumption use-case.

The api is created using the fast api framework in Python. The digital twin api for both the use cases are set up with the [docker-compose.yaml file](https://github.com/Ramya-Jayaraman-CseJku/DT_API/blob/main/docker-compose.yaml). 

#### Docker Installation

##### Pre-requisites:

In order to run the docker compose, the docker needs to be installed in the system.

##### Windows:

Install docker desktop on windows by following the´instructions provided in the [link](https://docs.docker.com/desktop/install/windows-install/).

#### Deployment

After successful installation of the docker in your system, clone the repository and navigate to the project folder for running the docker-compose file with command.

`docker-compose up`

If the build is successful, you can see the services running on the ports as shown in table below. Navigate to the browser and check if the ports are running in localhost, for example the fastapi provides the graphical interface by default for performing the CRUD operations and can be viewed with the 'docs' path. The sample url for the air quality use case will be

 'http://localhost:8000/docs'.

| services                      | port |
| ----------------------------- | ---- |
| fast_api (air quality)        | 8000 |
| fast_api (energy consumption) | 8080 |
| grafana                       | 3000 |
| pgAdmin                       | 5050 |



