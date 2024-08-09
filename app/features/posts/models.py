from app.core.database import Base

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    published = Column(Boolean, default=True)
    #created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
