from typing import Optional
from fastapi import APIRouter, HTTPException, Response, status, Depends
from sqlalchemy.orm import Session

from app.core import oauth2
from app.core.database import get_db
from . import models, schemas 


router = APIRouter(
    prefix="/posts",
    tags = ["Posts"],
)



@router.get("/", response_model=list[schemas.Post])
def read_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), 
                   current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(title=post.title, content=post.content, category_id=post.category_id, published=post.published)
    new_post.user_id = current_user.id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.Post)
def read_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post == None:
        raise HTTPException(status_code=404, detail="Post not found")
    else:
        return post
    

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), 
                   current_user: int = Depends(oauth2.get_current_user)):
    db_post = db.query(models.Post).filter(models.Post.id == id)
    if not db_post.first():
        raise HTTPException(status_code=404, detail="Post not found")
    else:
        db_post.update(post.dict())
        db.commit()
        return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    db_post = db.query(models.Post).filter(models.Post.id == id)
    if db_post.first() == None:
        raise HTTPException(status_code=404, detail="Post not found")
    else:
        db_post.delete()
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)