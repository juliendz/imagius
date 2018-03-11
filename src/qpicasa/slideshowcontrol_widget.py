"""
Folder Manager Window module
author: Julien Dcruz
last edited: 8th April 2017
"""

import sys
import os
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore
from PyQt5.QtCore import QDir, QStandardPaths
from .folder_manager import FolderManager
from .ui.ui_foldermanager import Ui_SlideshowControlWidget
from .log import LOGGER


class SlideshowControlWidget(QWidget, Ui_SlideshowControlWidget):
    def __init__(self, parent=None):
        super(SlideshowControlWidget, self).__init__(parent)
        self.setupUi(self)

    def closeWindow(self):
        self.close()
