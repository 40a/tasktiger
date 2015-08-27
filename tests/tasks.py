import json
import redis
import time

from .config import *
from .utils import get_tiger

tiger = get_tiger()


def simple_task():
    pass

@tiger.task()
def decorated_task(*args, **kwargs):
    pass

def exception_task():
    raise StandardError('this failed')

@tiger.task(queue='other')
def task_on_other_queue():
    pass

def file_args_task(filename, *args, **kwargs):
    open(filename, 'w').write(json.dumps({
        'args': args,
        'kwargs': kwargs,
    }))

@tiger.task(hard_timeout=DELAY)
def long_task_killed():
    time.sleep(DELAY*2)

@tiger.task(hard_timeout=DELAY*2)
def long_task_ok():
    time.sleep(DELAY)

@tiger.task(unique=True)
def unique_task(value=None):
    conn = redis.Redis(db=TEST_DB)
    conn.lpush('unique_task', value)

@tiger.task(lock=True)
def locked_task(key):
    conn = redis.Redis(db=TEST_DB)
    data = conn.getset(key, 1)
    if data is not None:
        raise StandardError('task failed, key already set')
    time.sleep(DELAY)
    conn.delete(key)
