"""
Folder Manager Window module
author: Julien Dcruz
last edited: 8th April 2017
"""

import sys
import os
from PyQt5 import QtCore
from PyQt5.QtCore import QDir, QStandardPaths
from PyQt5.QtGui import QKeySequence, QPixmap, QImage, QBrush
from PyQt5.QtWidgets import QWidget, QShortcut
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QGraphicsItem

from .ui.ui_slideshowwindow import Ui_SlideshowWindow
from .meta_files import MetaFilesManager
from .log import LOGGER


class SlideshowWindow(QWidget, Ui_SlideshowWindow):
    def __init__(self, slideshow_info, parent=None):
        super(SlideshowWindow, self).__init__(parent)
        self.setupUi(self)

        self._slideshow_info = slideshow_info

        self._shortcut_exit = QShortcut(QKeySequence(QtCore.Qt.Key_Escape), self)

        self._shortcut_exit.activated.connect(self.closeWindow)

        self._gfx_scene = QGraphicsScene()
        self.gfx_slide.setScene(self._gfx_scene)
        # self.gfxview_thumbs.setAlignment(
        #    QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self._meta_files_mgr = MetaFilesManager()
        self._meta_files_mgr.connect()

    def resizeEvent(self, event):
        if event.spontaneous():
            print(self.gfx_slide.viewport().size())
            self.load_image(self._slideshow_info['sd_id'], self._slideshow_info['serial'])

    def load_image(self, sd_id, serial):
        self._gfx_scene.clear()
        self.gfx_slide.viewport().update()
        self.gfx_slide.centerOn(0, 0)

        dr_img = self._meta_files_mgr.get_scan_dir_image(sd_id, serial)
        img_item = QGraphicsPixmapItem()
        pixmap = QPixmap(QImage(dr_img['abspath']))
        pixmap = pixmap.scaled(self.gfx_slide.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        img_item.setPixmap(pixmap)
        self._gfx_scene.addItem(img_item)

    def closeWindow(self):
        self._meta_files_mgr.disconnect()
        self.close()
