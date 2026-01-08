from app import schemas  #importing the schemas module from the app package
from jose import jwt  #importing jwt from jose to decode the jwt token
from .database import client, session  #importing the client and session fixtures from the database.py file in the tests directory
import pytest  #importing pytest to use the pytest fixtures defined in database.py file
from app.config import settings  #importing settings from the config module to get the SECRET_KEY and ALGORITHM for decoding the jwt token


@pytest.fixture #this creates a test user for each function that needs it
def test_user(client):  #defining a pytest fixture called test_user, this will be used to create a test user for the tests
    user_data = {"email": "nneka_oguh1@gmail.com", "password": "password123"}  #defining the user data for the test user
    res = client.post("/users/", json=user_data)  #using the test client to make a post request to the /users/ endpoint to create a new user, just like what postman does
    assert res.status_code == 201  #asserting that the response status code is 201(created)
    new_user = res.json()  #getting the json response from the post request and setting it to new_user
    new_user['password'] = user_data['password']  #adding the password to the new_user dictionary, so that it can be used in the tests
    return new_user  #returning the new_user dictionary to the caller, so that it can be used in the tests

#COMMENTED OUT COS TEACHER SAID NO NEED TO TEST ROOT ENDPOINT
#def test_root(client): #test function to test the root endpoint from main.py
    #res = client.get("/")  #using the test client to make a get request to the root endpoint
    #print(res.json().get("message"))  #printing the json response message from the get request
    #assert res.json().get("message") == "Hello World!!!"  #asserting that the response status code is 200
    #assert res.status_code == 200  #asserting that the response status code is 200



def test_create_user(client): #test function to test the create user endpoint from user.py
    res = client.post(  #using the test client to make a post request to the /users/ endpoint to create a new user, just like what postman does
        "/users/",
        json={"email": "nneka_oguh1@gmail.com", "password": "password123"})  #sending the email and password in json format in the request body
    new_user = schemas.UserOut(**res.json())   #getting the json response from the post request and setting it to new_user, userout scham will check to see that the data required is being provided as per the requirements in userout in schema file, ** is used to unpack the dictionary returned by res.json() so that the keys and values can be passed as keyword arguments to the UserOut schema
    assert new_user.email == "nneka_oguh1@gmail.com"
    assert res.status_code == 201  #asserting that the response status code is 201(created)
    #this acts like postman, we are creating a user and it is suppised to be stored in the database, but since we are testing, we have to create a testing database


def test_login_user(client, test_user):  #test function to test the get user endpoint from user.py
    res = client.post(  #using the test client to make a post request to the /users/ endpoint to create a new user, just like what postman does
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]})  #sending the email and password in form data format in the request body, instead of json cos we are loggi in, changed from json to data cos login endpoint uses form data
    login_res = schemas.Token(**res.json())  #getting the json response from the post request and setting it to login_res, Token schema will validate the response from the login endpoint, ** is used to unpack the dictionary returned by res.json() so that the keys and values can be passed as keyword arguments to the Token schema
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])  #decoding the jwt token to get the payload, so that we can get the user id from the payload
    id = payload.get("user_id")  #getting the user id from the payload
    assert id == test_user["id"]  #asserting that the user id from the payload is equal to the user id from the test_user fixture
    assert login_res.token_type == "bearer"  #asserting that the token type is bearer, as defined in auth.py file
    assert res.status_code == 200  #asserting that the response status code is 200
    #so test_user fixture is used here to create a user before testing the login endpoint, so that we can test if the user can login with the correct credentials

@pytest.mark.parametrize("email, password, status_code",[  #using pytest parametrize to test multiple incorrect login credentials
    ("wrongemail.gmail.com", "password123", 403),  #wrong email
    ("nneka_oguh1@gmail.com", "wrongpassword", 403),  #wrong password
    ("wrongemail.gmail.com", "wrongpassword", 403),  #both email and password are wrong
    (None, "password123", 422),  #empty email
    ("nneka_oguh1@gmail.com", None, 422),  #empty password
])
def test_incorrect_login(test_user, client, email, password, status_code):  #test function to test the get user endpoint from user.py
    payload = {}
    if email is not None:
        payload["username"] = email
    if password is not None:
        payload["password"] = password
    
    res = client.post(  #using the test client to make a post request to the /users/ endpoint to create a new user, just like what postman does
        "/login",
        data=payload)  #sending the email and password in form data format in the request body, instead of json cos we are loggi in, changed from json to data cos login endpoint uses form data
    assert res.status_code == status_code  #asserting that the response status code is equal to the expected stat
    #assert res.json().get("detail") == "Invalid Credentials"  #asserting that the response detail message is "Invalid Credentials", notice the I and C are capitalized as defined in auth.py file