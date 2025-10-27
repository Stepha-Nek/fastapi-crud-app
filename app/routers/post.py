from fastapi import Body, FastAPI,Response, status, HTTPException,Depends, APIRouter #from fastapi library import fastapi, Response is imported so we can get the 404, 200 etc. status will show you all the http codes.
from sqlalchemy.orm import Session #importing session from sqlalchemy.orm to create a session for the database
from typing import List, Optional #importing List from typing to specify that the response will be a list of Post objects
from .. import models, schemas, utils #importing models not from the current directory called routers but from the app directory which is outside the router directory hence two dots. models.py contains the database models that will be used to create the tables in the database.
from ..database import get_db #importing get_db from the database module, using 2 dots because the file isnt in the routers directory but in the app directory, routers folder is in the app directory too 
from .. import oauth2 #importing oauth2 from the routers module, this is not used in this code but it is imported so you can use it later on. oauth2.py contains the functions that will be used to handle the authentication and authorization of the users.
from sqlalchemy import func #importing func from sqlalchemy to use sql functions like count, sum, avg etc.

router = APIRouter(prefix="/posts", tags=["Posts"]) #creating a router for the posts, prefix is used to add a prefix to all the routes in this router, tags is used to group the routes in the documentation


@router.get("/", response_model=List[schemas.PostOut]) #list is imported from typing, it is used to specify that the response will be a list of Post objects, response_model collects the model of data response from the post in the schemas.py file defined schema for response. so this isnt getting just one post cos one post is in one model, this is getting all the posts, so more than one post
def get_posts(db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user), limit:int = 10, skip: int = 0, search: Optional[str] = ""): # db: Session = Depends(get_db) IS PART OF THE NEW SQLALCHEMY CODE otherwise it was just get_posts(),this will get all the posts from the database, db is a session that will be used to query the database, it is a dependency that will be injected into the function
    #THIS IS THE OLD CODE THAT USES POSTGRESQL DATABASE DRIVER, I COMMENTED IT OUT
    #cursor.execute("""SELECT * FROM posts""") //gets all post from database when using database driver
    #Posts = cursor.fetchall() #this will fetch all the posts from the database and return them as a list of dictionaries
    #NEW CODE USING SQLALCHEMY ORM
    #*posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() #commented this out cos we used the one below .this will query the database for all the posts and return them as a list of Post objects which returns sql
    #what you will see there. it will run second because it is recognised by fastapi as the secon code, the first code will run first, people wiill see hello wrld first. so the order matters
    #return posts #return all the posts from the database, commented out cos we are using the code below to get posts with votes

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts #commented the one above out*

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.Post)# so that when a post is created, it shows 201. response model collects the model of data response from the post in the schemas.py file defined schema for response.
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)): #db: Session = Depends(get_db) is part of the new sqlalchemy code, before it was just create_posts(post:post),post is a Post object that will be created, db is a session that will be used to query the database, it is a dependency that will be injected into the function.db: Session = Depends(get_db) gives us access to the database
    # user_id:int = Depends(oauth2.get_current_user) is used to get the current user from the access token that is passed in from the request header, it will return the user id of the user that is creating the post, this is used to associate the post with the user that created it, so that we can know which user created which post. it will be used to create a foreign key relationship between the post and the user in the database.
    #THIS IS THE OLD CODE THAT USES POSTGRESQL DATABASE DRIVER psycopg2, I COMMENTED IT OUT
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",(post.title, post.content, post.published)) #this will insert the post into the database and return the post that was inserted. the %s are placeholders for the values that will be passed in from the post object
    #new_post = cursor.fetchone() #this will fetch the post that was just inserted into the database
    #conn.commit() #this will commit the changes to the database, so that the post is saved in the database and wont show only on postman when tested
    #NEW CODE USING SQLALCHEMY ORM
    #new_post = models.Post(title=post.title, content=post.content, published=post.published) insted of this, use the one below
    print(f'user id is {current_user.id}') #this will print the user id of the user that is creating the post, it is used for testing purposes, to see if the user id is being passed in correctly
    #the user_id is the id of the user that is creating the post, it is passed in from the oauth2.get_current_user function, which gets the user id from the access token that is passed in from the request header. this is used to associate the post with the user that created it, so that we can know which user created which post.
    new_post = models.Post(owner_id = current_user.id, **post.model_dump()) # the ** will unpack the python dictionary into sqlalchemy model after converting pydsntic model post into python dictionary. this will create a new Post object with the values from the post object that was passed in from the request body, it will convert the post object to a dictionary and then unpack it into the Post object
    db.add(new_post) #this will add the new post to the database session
    db.commit() #this will commit the changes to the database, so that the post is saved in the database and wont show only on postman when tested. similar to conn.commit() but this is for the sqlalchemy session
    db.refresh(new_post) #this will refresh the new post object with the values from the database. its is similar to the returning in the cursor.execute() method. it will get the new values and store it in the new_post object
    return new_post # will send back to the poster, used for testing so it returns what was just posted into the array
    
@router.get("/{id}", response_model=schemas.PostOut)#id is a path parameter that will hold the specific data, to get a particular/specific post
def get_post(id: int, db: Session = Depends(get_db)): # rether than just id:int,db: Session = Depends(get_db) was added from sqlalchemy, this will get a specific post from the database, id is an integer that will be passed in from the url, db is a session that will be used to query the database, it is a dependency that will be injected into the function
    #THIS IS THE OLD CODE THAT USES POSTGRESQL DATABASE DRIVER psycopg2, I COMMENTED IT OUT
    #cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),)) #id has to be converted to a string so it can be used in the query, the %s is a placeholder for the id that will be passed in from the url. it will be converted to an integer after as it is a valid id number
    #post = cursor.fetchone() #this will fetch the post with the id that was passed in from the url, it will return a dictionary
    #NEW CODE USING SQLALCHEMY ORM
    #post = db.query(models.Post).filter(models.Post.id == id).first() #, we used the one below.filter is similar to the where statement in sql lingo. .first is used to get the first post that matches the filter, it will return a Post object or None if no post was found with the id that was passed in from the url. this is similar to the cursor.fetchone() method. . all would return all
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} was not found")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)# so yopu know what post to delete, hence the id
def delete_post(id: int, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)): #db: Session = Depends(get_db) is part of the new sqlalchemy code, before it was just delete_post(id:int), this will delete a specific post from the database, id is an integer that will be passed in from the url, db is a session that will be used to query the database, it is a dependency that will be injected into the function
    #THIS IS THE OLD CODE THAT USES POSTGRESQL DATABASE DRIVER psycopg2, I COMMENTED IT OUT
    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),)) #this will delete the post with the id that was passed in from the url, it will return the post that was deleted
    #deleted_post = cursor.fetchone() #this will fetch the post that was just deleted from the database
    #conn.commit() #this will commit the changes to the database, so that the post is deleted from the database and wont show only on postman when tested
    #NEW CODE USING SQLALCHEMY ORM
    post = db.query(models.Post).filter(models.Post.id == id) #this will delete the post with the id that was passed in from the url, it will return the post that was deleted, synchronize_session=False is used to avoid a warning that is raised when deleting a post, querying the post to be deleted
    if post.first() == None: #this will check if the post with the id that was passed in from the url exists, if it does not exist, it will return None
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post with id: {id} does not exsist')#if the id selected isnt in the array or has been remnoved before
    if post.owner_id != current_user.id: #this will check if the user that is trying to delete the post is the owner of the post, if not, it will raise an exception
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action") #403 means forbidden, the user is not allowed to delete the post if he is not the owner of the post
    post.delete(synchronize_session=False) #this will delete the post from the database if it exsists, synchronize_session=False is used to avoid a warning that is raised when deleting a post
    db.commit() #this will commit the changes to the database, so that the post is deleted from the database and wont show only on postman when tested. this is similar to conn.commit() but this is for the sqlalchemy session
    #return Response(status_code=status.HTTP_204_NO_CONTENT)# no need to return data if yiu are deleting something, it will throw an error.

@router.put("/{id}", response_model=schemas.Post)#put method updates and shows all the fields, so if you update title, content will still show cos it will show how everything looks like after updating
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):# class post is imported from schemas.py, it is a pydantic model that will be used to validate the data that is passed in from the request body, id is an integer that will be passed in from the url, updated_post is a Post object that will be passed in from the request body, db: Session = Depends(get_db) is part of the new sqlalchemy code, before it was just update_post(id:int, updated_post:post), this will update a specific post in the database, it will return the updated post
    #THIS IS THE OLD CODE THAT USES POSTGRESQL DATABASE DRIVER psycopg2, I COMMENTED IT OUT
    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id))) #this will update the post with the id that was passed in from the url, it will return the post that was updated. the %s are placeholders for the values that will be passed in from the post object
    #updated_post = cursor.fetchone() #this will fetch the post that was just updated from the database
    #conn.commit() #this will commit the changes to the database, so that the post is updated in the database and wont show only on postman when tested
    #NEW CODE USING SQLALCHEMY ORM
    post_query = db.query(models.Post).filter(models.Post.id == id) #this will get the post with the id that was passed in from the url, it will return a Post object or None if no post was found with the id that was passed in from the url
    post = post_query.first() #this will get the first post that matches the filter, it will return a Post object or None
    if post == None: #if the index is not in the array
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exsist')#if the id selected isnt in the array or has been remnoved before
    if post.owner_id != current_user.id: #this will check if the user that is trying to delete the post is the owner of the post, if not, it will raise an exception
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action") #403 means forbidden, the user is not allowed to update the post if he is not the owner of the post
    post_query.update(updated_post.model_dump(), synchronize_session=False) #this will update the post with the values from the post object that was passed in from the request will be saved as python dictionary.model_dump helps convert it to python dictionary. synchronize_session=False is used to avoid a warning that is raised when updating a post. post is the pydantic schema and has the fields for data already so its used then changed to python dict using model dump
    db.commit() #this will commit the changes to the database, so that the post is updated in the database and
    return post_query.first() #this will return the updated post, it will return a Post object with the updated values, it is similar to the returning in the cursor.execute() method. it will get the new values and store it in the post object, so you can see what was just updated
# this code is a simple fastapi application that connects to a postgres database and allows you to create, read, update and delete posts.
# anytime you make changes to this code, you have to restart the server with uvicorn main:app, to avoid this do  uvicorn main:app --reload.
# note always save after adjusting the code. //check about using async keyword
