#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Application entry module
author: Julien Dcruz
last edited: 7th December 2016
"""

import sys
from PyQt5.QtWidgets import QApplication
from qpicasa.main_window import MainWindow
from qpicasa.log import LOGGER


if __name__ == '__main__':
    LOGGER.info('======================================qPicasa starting up=======================================')
    app = QApplication(sys.argv)
    w = MainWindow()
    w.setWindowTitle('qPicasa')
    w.showMaximized()

    sys.exit(app.exec_())
