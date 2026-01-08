import pytest  #importing the pytest module for testing
from app import models  #importing the schemas module from the app package

@pytest.fixture #this creates a test user for each function that needs it in this file
def test_vote(test_posts, test_user, session):
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user['id'])  #creating a Vote model instance to represent a vote by the test user on the fourth test post
    session.add(new_vote)  #adding the new vote to the database session
    session.commit()  #committing the changes to the database session

def test_vote_on_post(authorized_client, test_posts):#if you want us not to vote on our own post, we can create another user and vote on their post, like test_user2 should be added as argument
    res = authorized_client.post(
        "/vote/",
        json={"post_id": test_posts[3].id, "dir": 1}# voting on the fourth post in the test_posts list, with direction 1 (upvote)
    )  #using the authorized client to make a post request to the /votes/ endpoint to vote on a post
    assert res.status_code == 201  #asserting that the response status code is 201 created

def test_vote_on_post_twice(authorized_client, test_posts, test_vote):#trying to vote on the same post again
    res = authorized_client.post(
        "/vote/",
        json={"post_id": test_posts[3].id, "dir": 1}# voting on the fourth post in the test_posts list, with direction 1 (upvote), after doing it the first time
    )  #using the authorized client to make a post request to the /votes/ endpoint to vote on a post
    assert res.status_code == 409  #asserting that the response status code is 409 conflict

def test_delete_vote(authorized_client, test_posts, test_vote):
    res = authorized_client.post(
        "/vote/",
        json={"post_id": test_posts[3].id, "dir": 0}# deleting the vote on the fourth post in the test_posts list, with direction 0 (remove vote)
    )  #using the authorized client to make a post request to the /votes/ endpoint to delete a vote on a post
    assert res.status_code == 201  #asserting that the response status code is 201 created

def test_delete_vote_non_exist(authorized_client, test_posts): #test_vote is not included here because we are trying to delete a vote that does not exist, so we dont want votes at all
    res = authorized_client.post(
        "/vote/",
        json={"post_id": test_posts[3].id, "dir": 0}# trying to delete a vote on the fourth post in the test_posts list, with direction 0 (remove vote) when no vote exists
    )  #using the authorized client to make a post request to the /votes/ endpoint to delete a vote on a post
    assert res.status_code == 404  #asserting that the response status code is 404 not found

def test_vote_post_non_exist(authorized_client, test_posts):#voting on a post that does not exist
    res = authorized_client.post(
        "/vote/",
        json={"post_id": 9999, "dir": 1}# voting on a non-existent post with id 9999, with direction 1 (upvote)
    )  #using the authorized client to make a post request to the /votes/ endpoint to vote on a post
    assert res.status_code == 404  #asserting that the response status code is 404 not found

def test_unauthorized_user_vote(client, test_posts): #using an unauthorized client to vote on a post, regular client
    res = client.post(
        "/vote/",
        json={"post_id": test_posts[3].id, "dir": 1}# voting on the fourth post in the test_posts list, with direction 1 (upvote) using an unauthorized client
    )  #using the unauthorized client to make a post request to the /votes/ endpoint to vote on a post
    assert res.status_code == 401  #asserting that the response status code is 401 unauthorized