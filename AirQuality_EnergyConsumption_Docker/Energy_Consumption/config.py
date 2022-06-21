


class Settings:
    PROJECT_NAME:str = "CDL-MINT Project-Perform CRUD operations for storing energy consumption of devices in server with the APIs"
    PROJECT_VERSION: str = "1.0.0"

    POSTGRES_USER : str = "postgres"
    POSTGRES_PASSWORD = "cdlmint"
    POSTGRES_SERVER : str = "timeScaleDatabase"
    POSTGRES_PORT : str = "5432" # default postgres port is 5432
    POSTGRES_DB : str = "CDL-MINT"
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

settings = Settings()