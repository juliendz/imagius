# -*- coding: utf-8 -*-
__license__ = 'GPL v3'
__copyright__ = '2019, Julien Dcruz juliendcruz@gmail.com'
__docformat__ = 'restructuredtext en'

"""
Logging setup
"""

from PySide2 import QtCore
from .constants import USER_APPDATA_DIR, APP_NAME, LOG_FILE
import logging

LOGGER = logging.getLogger(APP_NAME)
LOGGER.setLevel(logging.DEBUG)

LOG_FILE_HANDLER = logging.FileHandler(
    '%s/%s/%s' % (USER_APPDATA_DIR, APP_NAME, LOG_FILE))
LOG_FILE_HANDLER.setLevel(logging.DEBUG)

LOG_FORMATTER = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
LOG_FILE_HANDLER.setFormatter(LOG_FORMATTER)

LOGGER.addHandler(LOG_FILE_HANDLER)
