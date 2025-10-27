from pydantic import BaseModel,ConfigDict,EmailStr# user, it will be hashed before being stored in the database
# EmailStr is used to validate that the email is in the correct format, it will raise a validation error if the email is not in the correct format.
# BaseModel is the base class for all pydantic models, it provides validation and serialization
from datetime import datetime  # this is used to get the time the post was created, it will be returned as a string, used in the created at for the returning schema
from typing import Optional  # Optional is used to indicate that a field is optional, it can be None or a value of the specified type
from pydantic import conint  # conint is used to constrain an integer field, in this case we use it to constrain the dir field in the Vote model to be either 0 or 1

class PostBase(BaseModel): #notics this post starts with capital p so its not mistaken
    title: str #title has to be string
    content: str #content has to be of type string too
    published: bool = True # so its automatically true unless the user chooses false, if nothing was chosen its still true
    #model_config = ConfigDict(from_attributes=True) 

class PostCreate(PostBase): #this is the post that will be created, it inherits from PostBase, THIS IS INHERITANCE
    pass #we dont need to add anything else here

#WE wouldave done one for update but since create and update are almost the same we just leave the POstCreate as it is, we can use it for both create and update

class UserOut(BaseModel):  # This is the user that will be returned to the user, it does not inherit from UserCreate because it has more fields.
    id: int  # id has to be an integer, this is the id of the user
    email: EmailStr  # Emailstr ensures the email is valid in the right format and not random text
    created_at: datetime  # this is the time the user was created, it will be returned as a string
    #notice we left out password so the user does not see his password given back to him, this is a security measure
    
    model_config = ConfigDict(from_attributes=True) #instead of class config:orm_mode = True below. we can use this line instead, cos its pydantic v2 now

    #class Config:
        #orm_mode = True  # This is used to tell pydantic to treat the model as an ORM model, so it can read the data from the database.



class Post(PostBase):  # This is the post that will be returned to the user, it dosent inhearit from postbase cos its another schema on its own and isnt similar to that.
    id: int #id has to be an integer, this is the id of the post
    created_at: datetime  # this is the time the post was created, it will be returned as a string
    owner_id: int  # this is the id of the user that created the post, it has to be an integer
    owner: UserOut  # this is the user that created the post, it has to be of type UserOut, notice the quotes around UserOut, this is because UserOut is defined later in the file, so we need to use a forward reference to tell pydantic that this is a reference to a model that will be defined later.

    model_config = ConfigDict(from_attributes=True) #instead of class config and orm_mode = True, we can use this line instead, cos its pydantic v2 now

    #class config:  
        #orm_mode = True   This is used to tell pydantic to treat the model as an ORM model, so it can read the data from the database since pydantic can only work with python dictionaries.
        # This is necessary for pydantic to work with SQLAlchemy models.
        # It allows us to use SQLAlchemy models directly in our Pydantic schemas.

class PostOut(BaseModel):  # This is the post that will be returned to the user, it does not inherit from PostBase because it has more fields.
    Post: Post  # This is the class post above that will be returned to the user, it has to be of type Post, notice the capital P in Post, this is because it is a class.
    votes: int  # This is the number of votes that the post has, it has to be an integer

    model_config = ConfigDict(from_attributes=True) #instead of class config and orm_mode = True, we can use this line instead, cos its pydantic v2 now

    #class Config:
        #orm_mode = True  # This is used to tell pydantic to treat the model as an ORM model, so it can read the data from the database.

class UserCreate(BaseModel): #what is required from the user, the information needed
    email: EmailStr  # Emailstr ensures the email is valid in the right format and not random text, 
    password: str  # password has to be a string, this is the password of the
    

class UserLogin(BaseModel):  # This is the user that will be used to log in, it does not inherit from UserCreate because it has more fields.
    email: EmailStr  # Emailstr ensures the email is valid in the right format and not random text
    password: str  # password has to be a string, this is the password of the

class Token(BaseModel):  # This is the token that will be returned to the user after login
    access_token: str  # This is the access token that will be returned to the user after login
    token_type: str  # This is the type of the token, usually "bearer"

class TokenData(BaseModel):  # This is the data that will be returned to the user after login, data embeded into accesstoken
    id: Optional[int] = None  # This is the id of the user, it is optional because it may not be available at the time of login, it will be used to get the user from the database later on.
    

class Vote(BaseModel):
    post_id: int  # This is the id of the post that the user wants to vote on, it has to be an integer
    dir:int = conint(le=1)  # This is the direction of the vote, it can be either 1 or 0, 1 means upvote, 0 means downvote, since we just want only 0 and 1, we imported
    #conint from pydantic