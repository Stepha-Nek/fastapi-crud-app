from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone  # Importing datetime and timedelta to handle token expiration and current time
from typing import Optional  # Importing Optional to allow optional fields in the TokenData schema
from . import schemas, database, models  # Importing the schemas module to use the TokenData schema for token data validation
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session  # Importing Session to interact with the database
from .config import settings  # Importing settings to access configuration variables

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")  # This is used to get the token from the request, it will be used in the get_current_user function to get the token from the request header.
# The tokenUrl is the endpoint where the token can be obtained, in this case, it is "auth/login". This means that when a user logs in, they will receive a token that can be used to access protected routes by including it in the Authorization header as a Bearer token.
# This is used to handle the OAuth2 password flow, which is a common way to authenticate users in web applications. It allows users to log in with their username and password and receive a token that can be used to access protected routes.
# The OAuth2PasswordBearer class is a FastAPI security utility that provides a way to extract the token from the request header. It is used to handle the OAuth2 password flow, which is a common way to authenticate users in web applications.
# It extracts the token from the request header and validates it. If the token is valid, it returns the token; otherwise, it raises an HTTPException with a 401 Unauthorized status code. This is used to protect routes that require authentication, ensuring that only authenticated users can access them.
# This is used to handle the OAuth2 password flow, which is a common way to authenticate users in web applications. It allows users to log in with their username and password and receive a token that can be used to access protected routes.
# This token can then be used to access protected routes by including it in the Authorization header as a Bearer token. The OAuth2PasswordBearer class is a FastAPI security utility that provides a way to extract the token from the request header.
#SECRET_KEY
SECRET_KEY = settings.secret_key  # This is the secret key used to sign the JWT token. It should be kept secret and not shared with anyone.

#algorithm
ALGORITHM = settings.algorithm  # This is the algorithm used to sign the JWT token. It should be a secure algorithm such as HS256 or RS256.

#experation_time 
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
# This is the time in minutes after which the access token will expire.
# It is used to set the expiration time for the access token when it is created.

def create_access_token(data: dict):
    """
    Create a JWT access token.
    :param data: The data to include in the token payload.
    :param expires_delta: Optional timedelta for token expiration.
    :return: The encoded JWT access token.
    """
    to_encode = data.copy()  # Create a copy of the data to avoid modifying the original dictionary
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # Set the expiration time for the token
    to_encode.update({"exp": expire})  # Add the expiration time to the token payload
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # Encode the token using the secret key and algorithm and information provided # The jwt.encode function takes the payload, secret key, and algorithm as arguments and returns
    return encoded_jwt  # Return the encoded JWT access token

def verify_access_token(token: str, credentials_exception):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # Decode the token using the secret key and algorithm
        id: str = payload.get("user_id")  # Get the user ID from the token payload
        if id is None:
            raise credentials_exception  # If the user ID is not found in the token payload, raise the credentials exception
        token_data = schemas.TokenData(id=id)  # Create a TokenData object with the user ID
    except JWTError:
        raise credentials_exception  # If there is an error decoding the token, raise the credentials exception
    return token_data  # Return the TokenData object containing the user ID

def get_current_user(token: str  = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    """
    Get the current user based on the provided access token.
    :param token: The access token from the request header.
    :return: The TokenData object containing the user ID.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    #so instead of showing the user the token we just save it and compare it with the one they provided and the one in the database
    token = verify_access_token(token, credentials_exception)  # Verify the access token and get the user ID
    user = db.query(models.User).filter(models.User.id == token.id).first()  # Query the database to get the user with the provided user ID
    return user