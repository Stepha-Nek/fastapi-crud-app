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
from alembic import command  #importing command from alembic to run the migrations on the testing database
#starting here is database setup for testing purposes
#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:xxxx@localhost:5432/fastapi_test"  # use this or add _test to the one below, i used the one below .database url for the testing database, test database is fastapi_test cos databse name is fastapi in main app
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


