from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .config import DatabaseSettings

settings = DatabaseSettings()
session_maker = sessionmaker(bind=create_engine(settings.url), expire_on_commit=False)
test_sesson_marker = sessionmaker(bind=create_engine(settings.test_url), expire_on_commit=False)
