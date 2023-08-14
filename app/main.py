# import FastAPI and other libraries
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# sql driver
import psycopg2
from psycopg2.extras import RealDictCursor
# time library
import time
from .routers import posts

# # creates all the tables in the database
# models.Base.metadata.create_all(bind=engine)

# create FastAPI instance
app = FastAPI()

# check with Guy on origins
origins = ["https://www.google.com"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

# include router for posts
app.include_router(posts.router)


# create a route/path operation
# this is the decorator, which turns the function into a path operation
# it includes a get method, which is the HTTP method and the path of the url.
@app.get("/")
# async is optional before def. Name of function doesn't matter, but should be descriptive
def root():
    # this will have all the code for the path operation
    # fastapi will convert this to json
    return {"message": "Welcome to my API!"}
