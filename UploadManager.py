#
# Remember: A comment is a lie waiting to happen.
#

from iparamap import iparamap

from pythonfix import *  # pylint: disable=W0401
from my_mock import package_from_filename


class BasicUploadManager(object):
    # pylint: disable=R0903

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


class ThreadedUploadManager(BasicUploadManager):
    # pylint: disable=R0903

    def __init__(self, uploader, queue_size=3):
        super(ThreadedUploadManager, self).__init__(uploader)
        self._queue_size = queue_size

    def upload(self, filenames):
        for package in iparamap(
                package_from_filename,
                filenames,
                self._queue_size):
            self._upload(package)
