from app.core.database import Base

from sqlalchemy import TIMESTAMP, Column, Integer, String, func


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
