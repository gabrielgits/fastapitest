from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    content: str
    user_id: int
    published: bool = True

class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int

    class Config:
        orm_mode = True
