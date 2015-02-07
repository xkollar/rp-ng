#
# Remember: A comment is a lie waiting to happen.
#

import itertools
import os
import sys

from pythonfix import *  # pylint: disable=W0401
from my_mock import Uploader
from UploadManager import ThreadedUploadManager as UploadManager
# from UploadManager import BasicUploadManager

from app_config_declaration import APP_CONFIG_DECLARATION
from ConfigDeclaration import AppConfig


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
    app_config = AppConfig(APP_CONFIG_DECLARATION)
    opts, args = app_config.parse_args(sys.argv[1:])

    upload_manager = UploadManager(Uploader())
    upload_manager.upload(gen_filenames(args, opts.dirs))

if __name__ == '__main__':
    main()
