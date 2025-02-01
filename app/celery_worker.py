from celery import Celery
from app.tasks import app

if __name__ == "__main__":
    app.start()
