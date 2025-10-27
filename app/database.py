from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker
import psycopg2 #importing psycopg2 to connect to the postgres database, this is not used in this code but it is imported so you can use it later on. psycopg2 is a library that allows you to connect to a postgres database and execute SQL queries.
from psycopg2.extras import RealDictCursor
import time #importing time so we can use it to wait for a few seconds before trying to connect to the database again if the connection fails
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 

Base = declarative_base()  # This is the base class for your models, which will be used to create tables in the database.

def get_db():
    db = SessionLocal() #this will create a new session for the database, had to import session local to do this.
    try:
        yield db #this will yield the session to the caller, this is not used in this code but it is imported so you can use it later on.
    finally:
        db.close() #this will close the session after the caller is done with it, this is not used in this code but it is imported so you can use it later on.

#moved from main.py file. wasnt using it cos we used sqlalchemy but kept it here for reference
"""while True:
    try:
        # this is the connection to the database, it will connect to the database and create a cursor to execute queries on the database
        conn = psycopg2.connect(
            host="localhost",
            port="5432", #default port for postgres
            database="fastapi",
            user='postgres',
            password='Houdini@1759',
            cursor_factory=RealDictCursor) #this will allow us to get the data in dictionary format like the columns etc
        cursor = conn.cursor() #this will allow us to execute queries on the database
        print("Connection to database was successful")
        break #if connection is successful, break out of the loop
    except Exception as error:
        print("Connection to database failed")
        print("Error: ", error)
        time.sleep(2) #if connection fails, wait for 2 seconds before trying again"""