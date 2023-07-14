from celery import Celery
from celery.schedules import crontab
from .config import WorkerSettings
from parser_1 import parse_latest_posts
from SqlAlchemyRepository import Get_or_create
from sqlalchemy.orm import sessionmaker  # не знаю как-подругому передать sessionmaker
from sqlalchemy import create_engine

session_maker = sessionmaker(bind=create_engine("postgresql+psycopg://username:password@localhost:5432/database"))

settings = WorkerSettings()
app = Celery("tasks", backend=settings.celery_result_backend, broker=settings.celery_broker_url)

app.conf.beat_schedule = {
    "hello": {
        "task": "app.add",
        "schedule": crontab(minute="*/1"),
    },
}
app.conf.timezone = "Europe/Moscow"


@app.task(name="app.add")
def add():
    Get_or_create(session_maker).get_or_create(parse_latest_posts())
