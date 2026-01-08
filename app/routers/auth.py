from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import schemas, models, utils, oauth2  # Importing schemas, models, and utils from the parent directory
from ..database import get_db  # Importing the get_db function to get a database session

router = APIRouter(tags=["Authentication"])#tags are used to group the operations in the documentation, prefix is used to group all authentication related operations under /auth


@router.post("/login", status_code=status.HTTP_200_OK, response_model=schemas.Token)  # Endpoint for user login, post request is ususally used when data has to be sent in one direction, here the user will send login details to the server.
#def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):# we will get data from the database to compare so we need database. or if you just import databse you can do database.db, but we imported the db library from database so no need
#also the code bwlow was used, so now the schema for collecting the user info is contained in OAuth2PasswordRequestForm, which is a class from fastapi.security.oauth2 that handles the form data for user login. it dosent store the email  as user_credentials.email but stores it as username, so we have to use that in the code below.
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):   
    #user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first() #here the username is used instead of email because OAuth2PasswordRequestForm uses username to store the email. it dosent care if its a name or emmail, it stores it as username
    if not user:  # If user is not found
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    # Create a token for the user
    access_token = oauth2.create_access_token(data={"user_id": user.id})  #this is the information from user, asides uderid you can add more stuff if you want to, like email, but user id is enough for now.
    return {"access_token": access_token, "token_type": "bearer"}  # Return the access token and token type
