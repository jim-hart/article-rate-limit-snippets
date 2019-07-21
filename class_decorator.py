import functools
import threading
import time
import timeit

timer = timeit.default_timer


class throttle:

    def __init__(self, limit):
        if callable(limit):
            self.wrapped = self._wrap(limit)
            self.limit = -1
        else:
            self.wrapped = None
            self.limit = 1 / limit
        self.lock = threading.Lock()
        self.last = -1

    def __call__(self, *args, **kwargs):
        if self.wrapped is None:
            self.wrapped = self._wrap(args[0])
            return self
        else:
            return self._wait(*args, **kwargs)

    def __get__(self, instance, owner):
        return functools.partial(self, instance)

    def _wait(self, *args, **kwargs):
        with self.lock:
            elapsed = timer() - self.last
            if elapsed < self.limit:
                print(f'\twaiting {self.limit - elapsed:.3f}s')
                time.sleep(self.limit - elapsed)
            else:
                print(f'\tthrottle not required')
            self.last = timer()
        return self.wrapped(*args, **kwargs)

    def _wrap(self, func):
        functools.update_wrapper(self, func)
        return func
