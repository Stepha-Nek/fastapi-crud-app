from typing import Optional, Union, List
from fastapi import Body, FastAPI,Response, status, HTTPException,Depends #from fastapi library import fastapi, Response is imported so we can get the 404, 200 etc. status will show you all the http codes.
from random import randrange #so random numbers can be assigned as id to our posts in the my_posts array since we arent using a database
from sqlalchemy.orm import Session #importing session from sqlalchemy.orm to create a session for the database
from . import models, schemas, utils #importing models from the current directory, this is not used in this code but it is imported so you can use it later on. models.py contains the database models that will be used to create the tables in the database.
from .database import engine, Base #importing engine and Base from the database module, this
from .routers import post, auth, user, vote #importing the user and post routers from the routers module, this is not used in this code but it is imported so you can use it later on. routers.py contains the routes that will be used to handle the requests to the API.
from .config import settings #importing settings from the config module, this is not used in this code but it is imported so you can use it later on. config.py contains the configuration settings for the application.
from fastapi.middleware.cors import CORSMiddleware #FOR CORS

#print("What is in user module?", dir(user))
#print("Creating tables...")
#Base.metadata.create_all(bind=engine) #this will create all the tables in the database that are defined in the models.py file, it will create the posts table in the database if it does not exist already.
#commented base.metadata.create_all(bind=engine) because alembic is being used for migrations now, so no need to create tables this way anymore.
app = FastAPI() #getting an instance of fastapi and calling it app

#FOR CORS
origins = ["*"] #this allows all origins, you can specify the origins you want to allow like ["http://localhost:3000", "https://yourdomain.com", eg https://google.com] will only allow people accessing from google, you can check when you go to google.com and right click and click inspect then go to console and paste 'fetch('http://localhost:8000'/').then(res => res.json()).then(console.log)', you will see hello world, its just so if you are creating an app for specific people, you can limit the domain that accesses it.

app.add_middleware( #MIDDLEWARE IS A SOFTWARE THAT ACTS AS A BRIDGE BETWEEN AN OPERATING SYSTEM OR DATABASE AND APPLICATIONS, ESPECIALLY ON A NETWORK., before the app functions, it passes through middleware
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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
        #above code i removed because sqlalchemy is used to connect to the database, so no need to use psycopg2 to connect to the database, sqlalchemy will handle that for us. sqlalchemy is an ORM (Object Relational Mapper) that allows us to interact with the database using Python objects instead of SQL queries. it will create a session for us to interact with the database and we can use that session to execute queries on the database.


'''my_posts = [{"title": "title 1", "content": "content 1", "id": 1}, {"title": "title 2", "content": "content 2", "id": 2}]

def find_post(id): #defining a function to help you get a particular post fromthe array
    for p in my_posts:     #iteraring over the posts in the array
        if p["id"] == id: #if the id of the array matches the one that was passed in from the url
            return p #return the data in that post with that id
        
def find_index_post(id):
    for i, p in enumerate(my_posts):# check the diff btw enumeration and iteration
        if p ['id'] == id: # if the id in the array is the same as the id passed in from url
            return i #return the enumerated value'''

app.include_router(user.router) #this will include the user router in the app, so all the routes defined in the user router will be available in the app
app.include_router(post.router) #this will include the post router in the app, so all
app.include_router(auth.router) #this will include the auth router in the app, so all the routes defined in the auth router will be available in the app
app.include_router(vote.router) #this will include the vote router in the app, so all the routes defined in the vote router will be available in the app

@app.get("/") #@ is a decorator referencing the app, get is http function,/ is the rootpath, slash after the url. it makes the function an API
def root():
    return {"message": "Hello World!!!"}


