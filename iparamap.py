
__all__ = ['iparamap']

import Queue
import threading


NO_MORE_TASKS = object()


def iparamap(fun, iterator, queue_size=3):
    def worker(queue):
        try:
            for item in iterator:
                value = fun(item)
                queue.put(value)
        except Exception, e:
            queue.put(e)
        queue.put(NO_MORE_TASKS)

    queue = Queue.Queue(queue_size)
    thread = threading.Thread(target=worker, args=(queue,))
    thread.start()

    item = queue.get()
    while item is not NO_MORE_TASKS:
        if isinstance(item, Exception):
            raise item
        yield item
        item = queue.get()
    thread.join()


if __name__ == '__main__':
    import time

    def fun1(x):
        time.sleep(1)
        return x + 100

    def fun2(x):
        raise Exception("WHOA!")
        time.sleep(1)
        return x * 2

    def my_gen():
        raise Exception("Whoa gen!")
        yield 0

    try:
        for item in iparamap(fun1, iparamap(fun1, xrange(10))):
            print 'Main: Processing %s...' % item
            time.sleep(5)
    except Exception, e:
        print 'PFS!', e.message
