from pydantic import BaseModel
from datetime import datetime


# pydantic schemas
# it will be used as validation for the content that should be included
# defining the structure we need from frontend


# This handles the shape of the user sending data to the API
# base class.
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


# same as post base
class PostCreate(PostBase):
    pass


# This handles the format of the API response
class Post(PostBase):
    id: int
    created_at: datetime

    # this will avoid potential errors (although I didn't get it)
    class Config:
        orm_mode = True
