from fastapi import Body, FastAPI,Response, status, HTTPException,Depends, APIRouter
from .. import models, schemas, oauth2, database
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(Vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == Vote.post_id).first() #check if the post that is being voted on exists in the database
    if not post: #if the post does not exist
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {Vote.post_id} does not exist") #raise an error if the post does not exist



    vote_query = db.query(models.Vote).filter(models.Vote.post_id == Vote.post_id, models.Vote.user_id == current_user.id) # models.Vote.post_id == Vote.post_id checks if this particular posy has been voted on, models.Vote.user_id == current_user.id checks if the current user has voted on it
    found_vote = vote_query.first() #query the database collect the first result
    
    if (Vote.dir == 1): #if the user wants to like or add a vote
        if found_vote: #the data base is queried, saved in variable found_vote
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {Vote.post_id}") #if the user has voted on this post before
        
        new_vote = models.Vote(post_id=Vote.post_id, user_id=current_user.id) #if user hasnt voted on this post before
        db.add(new_vote) #add the new vote to the database session, like add in git
        db.commit() #commit the changes to the database, like git commit
        return {"message": "successfully added vote"} #return a message to the user
    else: #if the user wants to remove a like or vote
        if not found_vote: # if the user hasnt voted on this post before, he cannot delete or unvote if he hasnt voted before
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist") #if the user hasnt voted on this post before
        
        vote_query.delete(synchronize_session=False) #delete the vote from the database, synchronize_session=False is used to avoid a warning message
        db.commit() #commit the changes to the database, like git commit,  no adding cos there is nothing to add
        return {"message": "successfully deleted vote"} #message to user