from celery import Task


class ServingTask(Task):
    abstract = True