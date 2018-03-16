"""
Description: Image Properties widget module
author: Julien Dcruz
"""

import sys
import os
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore
from PyQt5.QtCore import QDir, QStandardPaths
from .folder_manager import FolderManager
from .ui.ui_propertieswidget import Ui_PropertiesWidget
from .log import LOGGER


class PropertiesWidget(QWidget, Ui_PropertiesWidget):

    def __init__(self, slideshow_interval, parent=None):
        super(PropertiesWidget, self).__init__(parent)
        self.setupUi(self)