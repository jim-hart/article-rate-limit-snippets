import functools
import threading
import time
import timeit

timer = timeit.default_timer


def throttle(func):
    lock = threading.Lock()
    limit = 1 / 5
    last = -1

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal last
        with lock:
            elapsed = timer() - last
            if elapsed < limit:
                print(f'\twaiting {limit - elapsed:.3f}s')
                time.sleep(limit - elapsed)
            else:
                print(f'\tthrottle not required')
            last = timer()
        return func(*args, **kwargs)
    return wrapper
