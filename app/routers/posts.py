from sqlalchemy.orm import Session
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List
from ..database import get_db
from .. import models, schemas


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


# create a new path operation
@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # unpack the model variables with ** to pass them as arguments
    new_post = models.Post(**post.model_dump())
    # add and commit to the database
    db.add(new_post)
    db.commit()
    # retrieve the post from the database and store it back in new_post
    db.refresh(new_post)
    return new_post


# retrieve an individual post
# the id is a built-in parameter, and we can add int validation
# make sure that path parameter methods are declared after the other path methods
# to avoid issues

@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # filter the posts by id
    post = (db.query(models.Post)
            .filter(models.Post.id == id)
            .first())
    # error handling
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    return post


# delete request
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # filter the posts by id, but only the query (no first)
    post_query = (db.query(models.Post)
                  .filter(models.Post.id == id))

    # error handling
    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")

    # if post does exist
    post_query.delete(synchronize_session=False)
    # commit change
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# create put request, using the same schema as the post request
@router.put("/{id}", response_model=schemas.Post)
# note I've changed the post to updated_post to avoid issues with pydantic
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # set query to find post by id
    post_query = db.query(models.Post).filter(models.Post.id == id)
    # grab the post
    post = post_query.first()

    # error handling
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")

    # update the post
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    # commit change
    db.commit()
    return post_query.first()