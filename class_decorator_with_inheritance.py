import functools
import threading
import time
import timeit

timer = timeit.default_timer


class Decorator:

    def __init__(self, wrapped=None):
        self.wrapped = self._wrap(wrapped) if callable(wrapped) else None

    def __call__(self, *args, **kwargs):
        if self.wrapped is None:
            self.wrapped = self._wrap(args[0])
            return self
        else:
            return self._call_wrapped(*args, **kwargs)  # --------------- 1.

    def _call_wrapped(self, *args, **kwargs):
        return self.wrapped(*args, **kwargs)

    def __get__(self, instance, owner):
        return functools.partial(self, instance)

    def _wrap(self, func):
        functools.update_wrapper(self, func)
        return func


class throttle(Decorator):

    def __init__(self, limit):
        super().__init__(limit)
        self.limit = 1 / limit if self.wrapped is None else -1
        self.lock = threading.Lock()
        self.last = -1

    def _call_wrapped(self, *args, **kwargs):
        with self.lock:
            elapsed = timer() - self.last
            if elapsed < self.limit:
                print(f'\twaiting {self.limit - elapsed:.3f}s')
                time.sleep(self.limit - elapsed)
            else:
                print(f'\tthrottle not required')
            self.last = timer()
        return self.wrapped(*args, **kwargs)
