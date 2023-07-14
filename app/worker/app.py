from celery import Celery
from celery.schedules import crontab
from .config import WorkerSettings
<<<<<<< HEAD
from parser_1 import parse_latest_posts
from SqlAlchemyRepository import Get_or_create
from sqlalchemy.orm import sessionmaker  # не знаю как-подругому передать sessionmaker
from sqlalchemy import create_engine

session_maker = sessionmaker(bind=create_engine("postgresql+psycopg://username:password@localhost:5432/database"))
=======
from parser_1 import parser
>>>>>>> d73ce71e5b856a4f67c1038299419d59ac2c2f50

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
<<<<<<< HEAD
    Get_or_create(session_maker).get_or_create(parse_latest_posts())
=======
    # print("test")
    parser()
>>>>>>> d73ce71e5b856a4f67c1038299419d59ac2c2f50
