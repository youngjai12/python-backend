from celery import Celery, signals
import os
import logging
from kombu import Queue, binding, Exchange

from queue_base_server.server.task_base import ServingTask

# Create celery
broker = f"amqp://deploy:iwilab@localhost:5672/local_broker"
app = Celery(task_cls=ServingTask, broker=broker)

TO_IMPORT_QUEUE = [
    "sentence_classification",
    "image_classification"
]

EXCHANGE_NAME = 'ml_exchange'
LOCAL_EXCHANGE = Exchange(EXCHANGE_NAME, type="topic", durable=False)

def route_task(name: str, args, kwargs, options, task=None, **kw):
    """Route Task"""
    for queue_name in TO_IMPORT_QUEUE:
        return {
            'queue': queue_name,
            'exchange': EXCHANGE_NAME,
            'routing_key': name,
        }

TASK_ROUTES = (route_task,)
TASK_QUEUES = [
    Queue(queue_name, [
        binding(exchange=,
                routing_key='{module}.#'.format(module=queue_name)),
    ], durable=False)
    for queue_name in TO_IMPORT_QUEUE
]

app.conf.imports = TO_IMPORT_QUEUE
app.conf.task_routes = TASK_ROUTES
app.conf.task_queues = TASK_QUEUES
app.conf.env = os.environ.get('ENV', 'local')
app.conf.phase = os.environ.get('PHASE', 'beta')
app.conf.update(worker_pool_restarts=True)

app_logger = logging.getLogger(__name__)