import threading
import time
from class_decorator_with_inheritance import throttle


class Example:

    @throttle(limit=2)
    def do_work(self):
        pass


@throttle(limit=5)
def do_work():
    pass


@throttle  # disabled
def do_fast_work():
    pass


def run_example(label, target, times, limit):
    print(f'--- running: {label}, limit: {limit}/s ---')
    time.sleep(1)
    threads = []
    for _ in range(times):
        thread = threading.Thread(target=target)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
    print()


if __name__ == '__main__':
    example = Example()
    run_example('method@do_work', target=example.do_work, times=5, limit=2)
    run_example('function@do_work', target=do_work, times=5, limit=5)
    run_example(
        'function@do_fast_work', target=do_fast_work, times=5, limit='inf')
