#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Application entry module
author: Julien Dcruz
last edited: 7th December 2016
"""

import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
from imagius.main_window import MainWindow
from imagius.log import LOGGER
import settings


if __name__ == '__main__':
    LOGGER.info('======================================qPicasa starting up=======================================')

    settings.init_app_data()

    app = QApplication(sys.argv)
    w = MainWindow()
    w.setWindowTitle('Imagius')
    w.showMaximized()

    sys.exit(app.exec_())
