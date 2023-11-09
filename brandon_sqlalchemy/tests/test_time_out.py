import time
from brandon_sqlalchemy.timeout import timeout

def test_time_out():
    timeout_sec = 2
    with timeout(seconds=timeout_sec):
        for i in range(100):
            print(i)
            time.sleep(0.5)