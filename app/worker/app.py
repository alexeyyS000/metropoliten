from celery import Celery
from celery.schedules import crontab
from .worker_config import WorkerSettings
from parser_1 import parse_latest_posts
from db.dal.post import PostDAL

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
    post_repo = PostDAL(session_maker)
    latest_posts = parse_latest_posts()
    latest_posts.reverse()
    for post in latest_posts:
        post_repo.get_or_create(post, id=post["id"])
