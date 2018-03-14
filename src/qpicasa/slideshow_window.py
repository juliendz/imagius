"""
Folder Manager Window module
author: Julien Dcruz
last edited: 8th April 2017
"""

import sys
import os
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import QDir, QStandardPaths, QTimer, pyqtSlot, QPointF, QRectF
from PyQt5.QtGui import QKeySequence, QPixmap, QImage, QBrush
from PyQt5.QtWidgets import QWidget, QShortcut
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QGraphicsItem

from .ui.ui_slideshowwindow import Ui_SlideshowWindow
from .meta_files import MetaFilesManager
from .slideshow_graphicsview import SlideshowGraphicsView
from .log import LOGGER


class SlideshowWindow(QWidget, Ui_SlideshowWindow):
    def __init__(self, sd_id, img_serial, parent=None):
        super(SlideshowWindow, self).__init__(parent)
        self.setupUi(self)

        self._curr_sd_id = sd_id
        self._curr_img_serial = img_serial
        self._slideshow_iterval = 1000
        self._is_slideshow = True

        self._shortcut_exit = QShortcut(QKeySequence(QtCore.Qt.Key_Escape), self)
        self._shortcut_exit.activated.connect(self.closeWindow)

        self._timer = QTimer()
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self.slide_next_img)

        self.gfx_slide = SlideshowGraphicsView()
        self.horizontalLayout.addWidget(self.gfx_slide)

        self._gfx_scene = QGraphicsScene()
        self.gfx_slide.setScene(self._gfx_scene)
        self.gfx_slide.setAlignment(QtCore.Qt.AlignCenter)

        self._meta_files_mgr = MetaFilesManager()
        self._meta_files_mgr.connect()

    def resizeEvent(self, event):
        if event.spontaneous():
            self.slide_start()

    def slide_start(self):
        dr_img = self._meta_files_mgr.get_scan_dir_image(self._curr_sd_id, self._curr_img_serial)
        self.load_image(dr_img['abspath'])
        self._timer.start(self._slideshow_iterval)

    @pyqtSlot()
    def slide_next_img(self):
        self._curr_img_serial += 1
        dr_img = self._meta_files_mgr.get_scan_dir_image(self._curr_sd_id, self._curr_img_serial)
        if not dr_img:
            # TODO: Show end of slideshow message
            print("Slideshow ended")
            self._timer.stop()
        else:
            self.load_image(dr_img['abspath'])
            if self._is_slideshow:
                self._timer.start(self._slideshow_iterval)

    def slide_prev_img(self):
        pass

    def load_image(self, abspath):
        self._gfx_scene.clear()
        self.gfx_slide.viewport().update()
        self.gfx_slide.centerOn(0, 0)

        img_item = QGraphicsPixmapItem()
        img = QImage(abspath)
        pixmap = QPixmap(img)
        pixmap = pixmap.scaled(self.gfx_slide.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        img_item.setPixmap(pixmap)

        self._gfx_scene.addItem(img_item)
        self._gfx_scene.setSceneRect(img_item.sceneBoundingRect())

    def closeWindow(self):
        self._timer.stop()
        self._meta_files_mgr.disconnect()
        self.close()
