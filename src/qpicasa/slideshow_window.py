"""
Folder Manager Window module
author: Julien Dcruz
last edited: 8th April 2017
"""

import sys
import os
from PyQt5.QtWidgets import QWidget, QShortcut
from PyQt5 import QtCore
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import QDir, QStandardPaths
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsItem

from .ui.ui_slideshowwindow import Ui_SlideshowWindow
from .log import LOGGER


class SlideshowWindow(QWidget, Ui_SlideshowWindow):
    def __init__(self, parent=None):
        super(SlideshowWindow, self).__init__(parent)
        self.setupUi(self)

        self._shortcut_exit = QShortcut(QKeySequence(QtCore.Qt.Key_Escape), self)

        self._shortcut_exit.activated.connect(self.closeWindow)

        self._gfx_scene = QGraphicsScene()
        self.gfx_slide.setScene(self._gfx_scene)
        # self.gfxview_thumbs.setAlignment(
            # QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)


    def closeWindow(self):
        self.close()
