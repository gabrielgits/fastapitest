from fastapi import FastAPI
# from app import endpoints
from app import models

from app.endpoints.author import router as author_router
from app.endpoints.article import router as article_router
from app.endpoints.category import router as category_router
from app.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(category_router)
app.include_router(author_router)
app.include_router(article_router)

@app.get("/")
def read_root():
    return {"Hello": "Hey Adalberto, how are you?"} 
