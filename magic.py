#
# Remember: A comment is a lie waiting to happen.
#

import Queue
import itertools
import os
import threading
import time

from optparse import Option, OptionParser

from pythonfix import *  # pylint: disable=W0401
from my_mock import Uploader
from UploadManager import ThreadedUploadManager as UploadManager
# from UploadManager import UploadManager


class RhnPushError(Exception):
    pass


def listdir(directory):
    directory = os.path.abspath(os.path.normpath(directory))
    if not os.access(directory, os.R_OK | os.X_OK):
        raise RhnPushError("Cannot read from directory %s" % directory)
    if not os.path.isdir(directory):
        raise RhnPushError("%s not a directory" % directory)
    for basename in os.listdir(directory):
        yield os.path.join(directory, basename)


def looks_like_package(filename):
    return any(filename.endswith(ext) for ext in (".rpm", ".mpm", ".deb"))


def gen_filenames(files, dirs):
    iters = itertools.imap(listdir, dirs)
    return itertools.ifilter(
        looks_like_package,
        itertools.chain(files, *iters))  # pylint: disable=W0142


def main():
    optlist = [
        Option('-d', '--dir', action='append', type='string', dest='dirs'),
        ]

    parser = OptionParser(option_list=optlist)
    opts, args = parser.parse_args([
        "-d", "testdir/package-dir",
        "testdir/package-x.rpm"])

    # um = ThreadedUploadManager(Uploader())
    um = UploadManager(Uploader())
    um.upload(gen_filenames(args, opts.dirs))

if __name__ == '__main__':
    main()
