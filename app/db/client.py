from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .config import DatabaseSettings

settings = DatabaseSettings()
session_maker = sessionmaker(bind=create_engine(settings.url))  # разобраться почему тут url а на url()
