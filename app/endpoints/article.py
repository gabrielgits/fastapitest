from typing import Optional
from fastapi import APIRouter, HTTPException, Response, status, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from .. import models


router = APIRouter()


#article pydantic model
class Article(BaseModel):
    title: str
    content: str
    author_id: int
    category_id: str
    published: bool = True

@router.get("/articles")
def read_articles(db: Session = Depends(get_db)):
    articles = db.query(models.Article).all()
    return {"data": articles}


@router.post("/articles", status_code=status.HTTP_201_CREATED)
def create_article(article: Article, db: Session = Depends(get_db)):
    new_article = models.Article(title=article.title, content=article.content, author=article.author, category=article.category, published=article.published)
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return {"data": new_article}


@router.get("/articles/{id}")
def read_article(id: int, db: Session = Depends(get_db)):
    article = db.query(models.Article).filter(models.Article.id == id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    else:
        return {"data": article}
    

@router.put("/articles/{id}")
def update_article(id: int, article: Article, db: Session = Depends(get_db)):
    db_article = db.query(models.Article).filter(models.Article.id == id)
    if not db_article.first():
        raise HTTPException(status_code=404, detail="Article not found")
    else:
        db_article.update(article.dict())
        db.commit()
        return {"data": article}

@router.delete("/articles/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_article(id: int, db: Session = Depends(get_db)):
    db_article = db.query(models.Article).filter(models.Article.id == id)
    if db_article.first() == None:
        raise HTTPException(status_code=404, detail="Article not found")
    else:
        db_article.delete()
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)