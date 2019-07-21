import functools
import threading
import time
import timeit

timer = timeit.default_timer


def throttle(limit):
    limit = 1 / limit
    lock = threading.Lock()
    last = -1

    def wrapped(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal last
            with lock:
                elapsed = timer() - last
                if elapsed < limit:
                    print(f'waiting {limit - elapsed:.3f}s')
                    time.sleep(limit - elapsed)
                last = timer()
            return func(*args, **kwargs)
        return wrapper
    return wrapped
