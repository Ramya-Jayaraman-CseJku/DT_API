
class Settings:
    PROJECT_NAME:str = "CDL-MINT Project-Perform CRUD operations for storing sensor data in server with the APIs"
    PROJECT_VERSION: str = "1.0.0"

    POSTGRES_USER : str = "postgres"
    POSTGRES_PASSWORD = "cdlmint"
    POSTGRES_SERVER : str = "timeScaledb"
    POSTGRES_PORT : str = "5432"
    POSTGRES_DB : str ="AQUC"
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

#psycopg2 db url format
    psycopg2_DATABASE_URL="user='{}' password='{}' host='{}' dbname='{}' port='{}'".format(POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_SERVER, POSTGRES_DB, POSTGRES_PORT)
   
settings = Settings()