from fastapi.testclient import TestClient
import pytest
from app.main import app  #importing the app=FastAPI() instance from main.py file
from app import schemas  #importing schemas from app to use the UserOut schema to validate the response from the create user endpoint
from app.config import settings
from sqlalchemy import create_engine #importing create_engine from sqlalchemy to create a database engine
from sqlalchemy.ext.declarative import declarative_base #importing declarative_base to create a base class for the models
from sqlalchemy.orm import sessionmaker#importing sessionmaker to create a session for the database
from app.database import get_db  #importing the get_db function from database.py file to override it for testing purposes
from app.database import Base  #importing Base from database.py file to create the tables in the testing database
from app.oauth2 import create_access_token
from app import models
from alembic import command  #importing command from alembic to run the migrations on the testing database

# starting here is database setup for testing purposes
#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Houdini@1759@localhost:5432/fastapi_test"  # use this or add _test to the one below, i used the one below .database url for the testing database, test database is fastapi_test cos databse name is fastapi in main app
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #creating a sessionmaker instance for the testing database

#Base.metadata.create_all(bind=engine), removed cos its now used within the pytest fixture.  #this will create all the tables in the testing database that are defined in the models.py file. we need to build the tables in the testing database before running the tests, so that the tests can interact with the database tables.
#Base = declarative_base()  # This is the base class for your models, which will be used to create tables in the database., wasnt needed here cos imported from database.py

#END of database setup for testing purposes, IMPORTED what was needed too
@pytest.fixture
def session():  #defining a pytest fixture called session, this will be used to create a database session for the tests, so i can run tests in one session, test if user can create and test if user can login befroe destroying the database
    Base.metadata.drop_all(bind=engine)  #this will drop all the tables in the testing database before the tests are run, so that the next time the tests are run, they start with a clean slate.
    Base.metadata.create_all(bind=engine)  #this will create all the tables in the testing database before the tests are run, so that the tests can interact with the database tables.
    db = TestingSessionLocal()  #creating a new database session for the tests
    try:
        yield db  #yielding the database session to the caller, so that it can be used in the tests. yield is used to pause the function and return the value to the caller, and then resume the function. similar to return, but yield allows us to do something after the test is done.
    finally:
        db.close()  #this will close the session after the caller is done with it, this is useful for cleaning up after tests, like deleting test data from the database etc.

# client = TestClient(app)  # commented out cos we are defining a function called client in the pytest fixture already.creating a test client instance using the FastAPI app instance, setting it to client
@pytest.fixture #this allows the defined fixture to be used in multiple test functions within the same module, so i can create a database sessio, test if it creates a user, and tests if that user can login, before destroying the database session after all tests in the module are done.
def client(session): #defining a pytest fixture called client, this will be used to create a test client instance for the tests
    def override_get_db_test():  #defining a function to override the get_db function in the main.py file for testing purposes, so that when the app needs a database session, it will use the testing database session instead of the regular database session
        try:
            yield session  #yielding the testing database session to the caller, so that it can be used in the tests. yield is used to pause the function and return the value to the caller, and then resume the function. similar to return, but yield allows us to do something after the test is done.
        finally:
            session.close()  #this will close the session after the caller is done with it, this is useful for cleaning up after tests, like deleting test data from the database etc.
    app.dependency_overrides[  #overriding the get_db dependency in the main.py file with the override_get_db_test function defined above, so that when the app needs a database session, it will use the testing database session instead of the regular database session
        get_db] = override_get_db_test  #this will overide the old database with
   
    yield TestClient(app)  #yielding the test client instance to the caller, so that it can be used in the tests. yield is used to pause the function and return the value to the caller, and then resume the function. similar to return, but yield allows us to do something after the test is done.

@pytest.fixture
def test_user2(client):
    user_data = {"email": "nneka_oguh17@gmail.com",
                 "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture #this creates a test user for each function that needs it
def test_user(client):  #defining a pytest fixture called test_user, this will be used to create a test user for the tests
    user_data = {"email": "nneka_oguh1@gmail.com", "password": "password123"}  #defining the user data for the test user
    res = client.post("/users/", json=user_data)  #using the test client to make a post request to the /users/ endpoint to create a new user, just like what postman does
    assert res.status_code == 201  #asserting that the response status code is 201(created)
    new_user = res.json()  #getting the json response from the post request and setting it to new_user
    new_user['password'] = user_data['password']  #adding the password to the new_user dictionary, so that it can be used in the tests
    return new_user  #returning the new_user dictionary to the caller, so that it can be used in the tests

@pytest.fixture
def token(test_user):#defining a pytest fixture called token, this will be used to create a token for the test user
    return create_access_token({"user_id": test_user['id']}) #creating a token for the test user using the create_access_token function defined in the app/auth.py file, passing the user id of the test user as the payload

@pytest.fixture
def authorized_client(client, token): #defining a pytest fixture called authorized_client, this will be used to create a test client instance with the authorization header set
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"} #setting the authorization header for the test client instance, so that it can be used in the tests, the authorisation is in dictionary format
    #authenticated client will be used to test endpoints that require authentication
    return client  #returning the test client instance to the caller, so that it can be used in the tests

@pytest.fixture
def test_posts(test_user, session, test_user2):  #defining a pytest fixture called test_posts, 
    posts_data = [  #defining a list of dictionaries to hold the post data for the test posts
        {"title": "First Post", "content": "Content of first post", "owner_id": test_user['id']},
        {"title": "Second Post", "content": "Content of second post", "owner_id": test_user['id']},
        {"title": "Third Post", "content": "Content of third post", "owner_id": test_user['id']},
        {"title": "3rd title","content": "3rd content","owner_id": test_user2['id']
    } #the fourth post is owned by test_user2 to test authorization scenarios
    ]

    def create_post_model(post):  #defining a function to create a Post model instance from a dictionary
        return models.Post(**post)  #unpacking the dictionary using ** so that the keys and values can be passed as keyword arguments to the Post model
    
    post_map = map(create_post_model, posts_data)  #using the map function to apply the create_post_model function to each post in the posts_data list  
    posts = list(post_map)  #converting the map object to a list and setting it to posts

    session.add_all(posts)  #adding all the test posts to the database session
    session.commit()  #committing the changes to the database session
    posts = session.query(models.Post).all()  #querying the database to get all the posts and setting it to posts
    return posts  #returning the list of test posts to the caller, so that it can be used in the tests