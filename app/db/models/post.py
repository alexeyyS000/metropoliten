from db.base import Base
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String, DateTime
from datetime import datetime


class Post(Base):
    __tablename__ = "posts"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, nullable=False)
    image_url = mapped_column(String, nullable=True)
    created = mapped_column(DateTime, default=datetime.utcnow)  # почему тут передается ссылка?
    updated = mapped_column(DateTime, onupdate=datetime.utcnow)
