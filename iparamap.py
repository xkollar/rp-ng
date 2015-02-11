
__all__ = ['iparamap']

import Queue
import threading


NO_MORE_TASKS = object()


def iparamap(fun, iterator, queue_size=3):
    def worker(queue):
        try:
            for in_item in iterator:
                value = fun(in_item)
                queue.put(value)
        except Exception, exn:  # pylint: disable=W0703
            queue.put(exn)
        queue.put(NO_MORE_TASKS)

    queue = Queue.Queue(queue_size)
    thread = threading.Thread(target=worker, args=(queue,))
    thread.start()

    ret_item = queue.get()
    while ret_item is not NO_MORE_TASKS:
        if isinstance(ret_item, Exception):
            raise ret_item
        yield ret_item
        ret_item = queue.get()
    thread.join()

# TEST

if __name__ == '__main__':
    import time

    def fun1(val):
        time.sleep(1)
        return val + 100

    def fun2(_val):
        time.sleep(1)
        raise Exception("WHOA!")

    def my_gen():
        raise Exception("Whoa gen!")

    try:
        for x_item in iparamap(fun1, iparamap(fun1, xrange(10))):
            print 'Main: Processing %s...' % x_item
            time.sleep(5)
    except Exception, exn:  # pylint: disable=W0703
        print 'PFS!', exn.message
