import functools
import threading
import time
import timeit

timer = timeit.default_timer


def decorator(decorated):
    def wrapped(*args, **kwargs):
        def wrapper(func):
            partial = decorated(func, *args, **kwargs)
            return functools.update_wrapper(partial, func)
        return wrapper
    return wrapped


@decorator
def throttle(func, limit):
    limit = 1 / limit
    lock = threading.Lock()
    last = -1

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
