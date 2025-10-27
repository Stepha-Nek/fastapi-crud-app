from fastapi import Body, FastAPI,Response, status, HTTPException,Depends, APIRouter #from fastapi library import fastapi, Response is imported so we can get the 404, 200 etc. status will show you all the http codes.
from sqlalchemy.orm import Session #importing session from sqlalchemy.orm to create a session for the database
from .. import models, schemas, utils #importing models not from the current directory called routers but from the app directory which is outside the router directory hence two dots. models.py contains the database models that will be used to create the tables in the database.
from ..database import get_db #importing get_db from the database module, using 2 dots because the file isnt in the routers directory but in the app directory, routers folder is in the app directory too 


router = APIRouter(prefix="/users", tags=["Users"])  # Create a new router instance for user-related operations, prefix is used to group all user related operations under /users, tags is used to group the operations in the documentation.
#new path operation for creating a user

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)  # This endpoint creates a new user. no need for /users cos the router instances already prefixes users, you only need the /
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    #hash the password before storing it in the database User.Password
    hashed_password = utils.hash(user.password)  # Hash the password using bcrypt before storing it in the database
    user.password = hashed_password # Update the user password with the hashed password.
    new_user = models.User(**user.model_dump())  # SO schema stored in user will be converted to a python dictionary by model dumo and unpacked  by ** into the User model.
    db.add(new_user)  # Add the new user to the database session.
    db.commit()
    db.refresh(new_user)

    return new_user  # Return the newly created user object.

# to get a user by their ID
@router.get("/{id}", response_model=schemas.UserOut)  # the userout schema ensures that response follows only what is specified in the userout and  not show password. password isnt part of it, check the schema file. no need to specify /users to, the router already prefixes users so you need only /
def get_user(id: int, db: Session = Depends(get_db)): #if we are going to use the datbbase db: Session = Depends(get_db) must be used.
    user = db.query(models.User).filter(models.User.id == id).first()# get the first user that matches the ID
    if not user: #IF USER ISNT FOUND
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    return user #IF User exsists, return the user object.


print("User router loaded")
print("Router object:", router)