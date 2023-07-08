from db.base import Base
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String, DateTime
from datetime import datetime


class News(Base):
    __tablename__ = "new"
    id = mapped_column(String, primary_key=True)
    name = mapped_column(String)
    utl = mapped_column(String)
    date_of_hew = mapped_column(DateTime)
    date_of_save = mapped_column(DateTime, default=datetime.utcnow)  # почему тут передается ссылка?
    date_of_change = mapped_column(DateTime, onupdate=datetime.utcnow)
