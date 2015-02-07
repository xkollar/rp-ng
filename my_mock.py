import os
import time


class Package(object):
    # pylint: disable=R0903

    def __init__(self, name, checksum_type, checksum):
        self.checksum_type = checksum_type
        self.checksum = checksum
        self.name = os.path.basename(name)


class Uploader(object):
    # pylint: disable=R0903

    @staticmethod
    def upload(package):
        assert isinstance(package, Package), "Won't upload non-packages"
        print "Uploading package: %s..." % package.name,
        time.sleep(4)
        print "done"


def package_from_filename(filename):
    time.sleep(1)
    return Package(
        filename,
        'sha1',
        'da39a3ee5e6b4b0d3255bfef95601890afd80709')
