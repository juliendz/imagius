# -*- coding: utf-8 -*-
__license__ = 'GPL v3'
__copyright__ = '2019, Julien Dcruz juliendcruz@gmail.com'
__docformat__ = 'restructuredtext en'

"""
Static and runtime constants
"""

from PySide2 import QtCore
from enum import Enum
from .exceptions import OsNotDetectedError
import platform

APP_NAME = 'imagius'
HUMAN_APP_NAME = 'Imagius - Photo Manager'
APP_VERSION = '0.8.1'
DB_SETTINGS = 'settings.db'
DB_META = 'meta.db'
LOG_FILE = 'imagius.log'
USER_APPDATA_DIR = QtCore.QStandardPaths.writableLocation(
    QtCore.QStandardPaths.AppDataLocation)


class SortMode(Enum):
    CreationTime = 1
    RecentChanges = 2
    Name = 3
    Size = 4


class OSType(Enum):
    OS_WINDOWS = 1
    OS_LINUX = 2


def get_appdata_dir() -> OSType:
    if platform.system() == 'Windows':
        return OSType.OS_WINDOWS
    if platform.system() == 'Linux':
        return OSType.OS_LINUX
    raise OsNotDetectedError
