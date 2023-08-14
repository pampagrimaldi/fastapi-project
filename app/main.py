# import FastAPI and other libraries
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# time library
from .routers import posts


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
    return {"message": "Welcome to the Team TAM API!!!"}
