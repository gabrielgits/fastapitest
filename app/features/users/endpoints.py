from typing import Optional
from fastapi import APIRouter, HTTPException, Response, status, Depends
from sqlalchemy.orm import Session


from app.core.database import get_db
from app.core import utils
from . import models, schemas 


router = APIRouter(
    prefix="/users",
    tags = ["Users"],
)


@router.get("/", response_model=list[schemas.User])
def read_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(name=user.name, email=user.email, password=user.password)
    hashed_password = utils.hash(user.password)
    db_user.password = hashed_password
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/{id}", response_model=schemas.User)
def read_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user == None:
        raise HTTPException(status_code=404, detail="User with id {id} does not exist")
    else:
        return user
    

@router.put("/{id}", response_model=schemas.User)
def update_user(id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == id)
    if not db_user.first():
        raise HTTPException(status_code=404, detail="User with id {id} does not exist")
    else:
        db_user.update(user.dict())
        db.commit()
        return user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == id)
    if db_user.first() == None:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        db_user.delete()
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)