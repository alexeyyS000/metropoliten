from celery import Celery
from celery.schedules import crontab
from .config import WorkerSettings

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
    print("test")
