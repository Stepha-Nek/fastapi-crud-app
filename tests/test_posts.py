from app import schemas  #importing the schemas module from the app package
import pytest  #importing the pytest module for testing

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")  #using the authorized client to make a get request to the /posts/ endpoint to get all posts
    def validate(post):  #defining a function to validate the post data using the PostOut schema
        return schemas.PostOut(**post)  #unpacking the dictionary using ** so that the keys and values can be passed as keyword arguments to the PostOut schema
    posts_map = map(validate, res.json())  #using the map function to apply the validate function to each post in the response json
    posts_list = list(posts_map)  #converting the map object to a list and setting it to posts
    assert len(res.json()) == len(test_posts)  #asserting that the length of the response json is equal to the length of the test posts
    assert res.status_code == 200  #asserting that the response status code is 200

def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")  #using the unauthorized client to make a get request to the /posts/ endpoint to get all posts
    assert res.status_code == 401  #asserting that the response status code is 401 unauthorized

def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")  #using the unauthorized client to make a get request to the /posts/{id} endpoint to get a specific post
    assert res.status_code == 401  #asserting that the response status code is 401 unauthorized

def test_get_one_post_not_exsist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/9999")  #using the authorized client to make a get request to the /posts/{id} endpoint with a non-existent id
    assert res.status_code == 404  #asserting that the response status code is 404 not found    
    #so this client is authorized but the post with id 9999 does not exist

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")  #using the authorized client to make a get request to the /posts/{id} endpoint to get a specific post
    post = schemas.PostOut(**res.json())  #validating the response json using the PostOut schema
    assert post.Post.id == test_posts[0].id  #asserting that the id of the post in the response is equal to the id of the test post
    assert post.Post.title == test_posts[0].title  #asserting that the title of the post in the response is equal to the title of the test post
    assert post.Post.content == test_posts[0].content  #asserting that the content of the post in the response is equal to the content of the test post
    assert res.status_code == 200  #asserting that the response status code is 200

@pytest.mark.parametrize("title, content, published", [
    ("My first title", "My first content", True),  
    ("My second title", "My second content", False),
    ("My third title", "My third content", True)
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post(
        "/posts/",
        json={"title": title, "content": content, "published": published}
    )  #using the authorized client to make a post request to the /posts/ endpoint to create a new post with the given title, content, and published status
    created_post = schemas.Post(**res.json())  #validating the response json using the Post schema
    assert res.status_code == 201  #asserting that the response status code is 201 created
    assert created_post.title == title  #asserting that the title of the created post is equal to the given title
    assert created_post.content == content  #asserting that the content of the created post is equal to the given content
    assert created_post.published == published  #asserting that the published status of the created post is equal to the given published status
    assert created_post.owner_id == test_user['id']  #asserting that the owner id of the created post is equal to the id of the test user

def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post(
        "/posts/",
        json={"title": "arbitrary title", "content": "lookatmenow"}
    )  #using the authorized client to make a post request to the /posts/ endpoint to create a new post with the given title, content, and published status
    created_post = schemas.Post(**res.json())  #validating the response json using the Post schema
    assert res.status_code == 201  #asserting that the response status code is 201 created
    assert created_post.title == "arbitrary title"  #asserting that the title of the created post is equal to the given title
    assert created_post.content == "lookatmenow"  #asserting that the content of the created post is equal to the given content
    assert created_post.published == True  #asserting that the published status of the created post is equal to True by default
    assert created_post.owner_id == test_user['id']  #asserting that the owner id of the created post is equal to the id of the test user

def test_unauthorized_user_create_post(client, test_user, test_posts):
    res = client.post(
        "/posts/",
        json={"title": "arbitrary title", "content": "lookatmenow"}
    )  #using the unauthorized client to make a post request to the /posts/ endpoint to create a new post
    assert res.status_code == 401  #asserting that the response status code is 401 unauthorized

def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")  #using the authorized client to make a delete request to the /posts/{id} endpoint to delete a specific post
    assert res.status_code == 401  #asserting that the response status code is 401 unauthorized

def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")  #using the authorized client to make a delete request to the /posts/{id} endpoint to delete a specific post
    assert res.status_code == 204  #asserting that the response status code is 204 no content

def test_delete_post_not_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/9999")  #using the authorized client to make a delete request to the /posts/{id} endpoint with a non-existent id
    assert res.status_code == 404  #asserting that the response status code is 404 not found

def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")  #using the authorized client to make a delete request to delete a post owned by another user, 4th post is owned by test_user2
    assert res.status_code == 403  #asserting that the response status code is 403 forbidden

def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "Updated Title",
        "content": "Updated Content",
        "id": test_posts[0].id #the id of the post to be updated
    }  #defining the data to update the post with 
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)  #using the authorized client to make a put request to the /posts/{id} endpoint to update a specific post
    updated_post = schemas.Post(**res.json())  #validating the response json using the Post schema
    assert res.status_code == 200  #asserting that the response status code is 200
    assert updated_post.title == data['title']  #asserting that the title of the updated post is equal to the given title
    assert updated_post.content == data['content']  #asserting that the content of the updated post is equal to the given content

def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "Hacked Title",
        "content": "Hacked Content",
        "id": test_posts[3].id   #the id of the post to be updated
    }  #defining the data to update the post with 
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)  #using the authorized client to make a put request to update a post owned by another user, 4th post is owned by test_user2
    assert res.status_code == 403  #asserting that the response status code is 403 forbidden

def test_unauthorized_user_update_post(client, test_user, test_posts):
    res = client.put(f"/posts/{test_posts[0].id}")  #using the unauthorized client to make a put request to the /posts/{id} endpoint to update a specific post
    assert res.status_code == 401  #asserting that the response status code is 401 unauthorized

def test_update_post_not_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "Non-existent Title",
        "content": "Non-existent Content",
        "id": 9999  #non-existent id
    }  #defining the data to update the post with 
    res = authorized_client.put(f"/posts/9999", json=data)  #using the authorized client to make a put request to the /posts/{id} endpoint with a non-existent id
    assert res.status_code == 404  #asserting that the response status code is 404 not found