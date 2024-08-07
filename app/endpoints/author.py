from typing import Optional
from fastapi import APIRouter, HTTPException, Response, status, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from .. import models


router = APIRouter()

#author pydantic model
class Author(BaseModel):
    name: str
    email: str
    bio: Optional[str]


@router.get("/authors")
def read_authors(db: Session = Depends(get_db)):
    authors = db.query(models.Author).all()
    return {"data": authors}


@router.post("/authors", status_code=status.HTTP_201_CREATED)
def create_author(author: Author, db: Session = Depends(get_db)):
    new_author = models.Author(name=author.name, email=author.email, bio=author.bio)
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return {"data": new_author}


@router.get("/authors/{id}")
def read_author(id: int, db: Session = Depends(get_db)):
    author = db.query(models.Author).filter(models.Author.id == id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    else:
        return {"data": author}


@router.put("/authors/{id}")
def update_author(id: int, author: Author, db: Session = Depends(get_db)):
    db_author = db.query(models.Author).filter(models.Author.id == id)
    if not db_author.first():
        raise HTTPException(status_code=404, detail="Author not found")
    else:
        db_author.update(author.dict())
        db.commit()
        return {"data": author}

@router.delete("/authors/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(id: int, db: Session = Depends(get_db)):
    db_author = db.query(models.Author).filter(models.Author.id == id)
    if db_author.first() == None:
        raise HTTPException(status_code=404, detail="Author not found")
    else:
        db_author.delete()
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)