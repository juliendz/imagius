#!/usr/bin/python3
# -*- coding: utf-8 -*-
__license__ = 'GPL v3'
__copyright__ = '2019, Julien Dcruz juliendcruz@gmail.com'
__docformat__ = 'restructuredtext en'

"""
Application entry and initialization
"""


import sys
from PySide2 import QtCore
from PySide2.QtWidgets import QApplication
from constants import HUMAN_APP_NAME
from init import init_app_data_dir, init_app_db

if __name__ == '__main__':

    init_app_data_dir()
    init_app_db()

    from log import LOGGER
    LOGGER.info(
        '======================================Imagius starting up=======================================')

    import settings
    settings.load_settings()

    from main_window import MainWindow

    app = QApplication(sys.argv)
    app.setApplicationName(HUMAN_APP_NAME)
    w = MainWindow()
    w.setWindowTitle('Imagius')
    w.showMaximized()

    sys.exit(app.exec_())
