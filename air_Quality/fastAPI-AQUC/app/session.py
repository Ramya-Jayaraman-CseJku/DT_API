from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import psycopg2
from config import settings


SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
# Create engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)
engine.connect()
# Create  Session with engine
SessionLocal = sessionmaker(bind=engine)

#instantiation
db_Session=SessionLocal()
##########create engine using psycopg2 ############
""" PSYCOPG2_DATABASE_URL=settings.psycopg2_DATABASE_URL
conn = psycopg2.connect(PSYCOPG2_DATABASE_URL) """