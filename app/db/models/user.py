from db.base import Base
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String


class User(Base):
    __tablename__ = "users"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
