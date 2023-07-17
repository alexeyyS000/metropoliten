from celery import Celery
from celery.schedules import crontab
from .worker_config import WorkerSettings
from parser_1 import parse_latest_posts
from db.dal.post_sql_repo import PostDAl

from db.client import session_maker

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
    PostDAl(session_maker).get_or_create(parse_latest_posts())
