from fastapi import FastAPI

from app.features.posts.endpoints import router as post_router
from app.features.users.endpoints import router as user_router
from app.features.users.auth import router as auth_router
from app.core.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post_router)
app.include_router(user_router)
app.include_router(auth_router)
