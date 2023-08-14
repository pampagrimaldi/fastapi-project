# import FastAPI and other libraries
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

# create FastAPI instance
app = FastAPI()


# pydantic schema
# it will be used as validation for the content that should be included
class Post(BaseModel):
    title: str
    content: str
    # published with a default value of True
    published: bool = True


# setup database connection
# cursor_factory=RealDictCursor is to get the column names in the response
# create while loop to continuously try to connect to the database
while True:
    try:
        conn = psycopg2.connect(host="localhost",
                                database="fastapi",
                                user="postgres",
                                password="password",
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection established")
        break
    except Exception as error:
        print("Error connecting to database")
        print("Error: ", error)
        time.sleep(2)

# creating hardcoded list of posts
my_posts = [{'title': 'title of post 1', 'content': 'content of post 1', "id": 1},
            {'title': 'favorite foods', 'content': 'I like pizza', "id": 2}]


# post retrieval logic
def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


# find index of post
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            # return index
            return i


# create a route/path operation
# this is the decorator, which turns the function into a path operation
# it includes a get method, which is the HTTP method and the path of the url.
@app.get("/")
# async is optional before def. Name of function doesn't matter, but should be descriptive
def root():
    # this will have all the code for the path operation
    # fastapi will convert this to json
    return {"message": "Welcome to my API!"}


# create a new path operation
@app.get("/posts")
def get_posts():
    # cursor is used to execute SQL queries. This doesnt return anything
    cursor.execute("""SELECT * FROM posts""")
    # this returns all the rows from the query
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # the %s are placeholders for the values, and avoids SQL injection
    # these are staged changes
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    # commit changes
    conn.commit()
    return {"data": new_post}


# retrieve an individual post
# the id is a built-in parameter, and we can add int validation
# make sure that path parameter methods are declared after the other path methods
# to avoid issues

@app.get("/posts/{id}")
def get_post(id: int):
    # note the id is passed into string format
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    return {"post_detail": post}


# delete request
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # find the index in the array of the post with the id
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    # commit change
    conn.commit()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    # delete the post with pop
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# create put request, using the same schema as the post request
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    # commit change
    conn.commit()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")

    return {"message": "post updated"}
