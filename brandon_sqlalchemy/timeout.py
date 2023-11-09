import errno
import os
import signal
from contextlib import contextmanager


class TimeoutException(Exception):
    pass


@contextmanager
def timeout(seconds, err_msg=os.strerror(errno.ETIME)):
    def handle_timeout(signum, frame):
        raise TimeoutException(err_msg)

    signal.signal(signal.SIGALRM, handle_timeout)
    signal.setitimer(signal.ITIMER_REAL, seconds)

    try:
        yield
    finally:
        signal.alarm(0)
