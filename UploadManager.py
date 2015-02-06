#
# Remember: A comment is a lie waiting to happen.
#

import Queue
import threading

from pythonfix import *  # pylint: disable=W0401
from my_mock import package_from_filename


class UploadManager(object):
    # pylint: disable=R0201,R0903
    """Mostly for testing purposes and as a debugging replacement
       for ThreadedUploadManager."""
    def __init__(self, uploader):
        self._uploader = uploader

    def _upload(self, package):
        self._uploader.upload(package)

    def upload(self, filenames):
        for filename in filenames:
            package = package_from_filename(filename)
            self._upload(package)

# This is internal do not import it from elsewhere
# (make your own, its easy)
END_OF_TASKS = object()

class ThreadedUploadManager(UploadManager):
    # pylint: disable=R0201,R0903
    def __init__(self, filename, queuesize=3):
        UploadManager.__init__(self, filename)
        self._queue = Queue.Queue(queuesize)

    def upload(self, filenames):

        def worker():
            package = self._queue.get()
            while package is not END_OF_TASKS:
                self._upload(package)
                self._queue.task_done()
                package = self._queue.get()
            self._queue.task_done()

        t = threading.Thread(target=worker)
        t.start()

        for filename in filenames:
            package = package_from_filename(filename)
            self._queue.put(package)

        self._queue.put(END_OF_TASKS)
        self._queue.join()
        t.join()
