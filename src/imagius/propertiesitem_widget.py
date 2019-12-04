"""
Description: Image Properties Item widget module
author: Julien Dcruz
"""

import sys
import os
from PySide2 import QtCore, QtGui
from PySide2.QtWidgets import QWidget
from PySide2.QtCore import QDir, QStandardPaths

from folder_manager import FolderManager
from ui.ui_propertiesitemwidget import Ui_PropertiesItemWidget
from log import LOGGER


class PropertiesItemWidget(QWidget, Ui_PropertiesItemWidget):

    def __init__(self, title, value, parent=None):
        super(PropertiesItemWidget, self).__init__(parent)
        self.setupUi(self)

        self.setToolTip(str(value))

        self.lbl_title.setText(title)
        self.lbl_value.setText(str(value))
