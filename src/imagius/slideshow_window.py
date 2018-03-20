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
from .slideshowcontrol_widget import SlideshowControlWidget
from .log import LOGGER
import settings
from settings import SettingType


class SlideshowWindow(QWidget, Ui_SlideshowWindow):

    def __init__(self, sd_id, img_serial, parent=None):
        super(SlideshowWindow, self).__init__(parent)
        self.setupUi(self)

        self._curr_sd_id = sd_id
        self._curr_img_serial = img_serial
        self._is_slideshow_looped = settings.get(SettingType.SLIDESHOW_LOOP, False, 'bool')
        self._slideshow_iterval = settings.get(SettingType.SLIDESHOW_INTERVAL, 1000, 'int')
        self._mouse_idle_interval = 1000
        self._is_slideshow = True
        self._gfx_item = None
        self._last_mouse_pos = QtCore.QPoint()
        self._curr_mouse_pos = QtCore.QPoint()

        self._shortcut_exit = QShortcut(QKeySequence(QtCore.Qt.Key_Escape), self)
        self._shortcut_exit.activated.connect(self.closeWindow)

        self._timer = QTimer()
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self.slide_next_img)

        self._idle_timer = QTimer()
        self._timer.setSingleShot(True)
        self._idle_timer.timeout.connect(self.hide_slideshow_controls)

        self.gfx_slide = SlideshowGraphicsView()
        self.gfx_slide.mouse_moved.connect(self.on_mouse_moved)
        self.horizontalLayout.addWidget(self.gfx_slide)

        self._gfx_scene = QtWidgets.QGraphicsScene()
        self.gfx_slide.setScene(self._gfx_scene)
        self.gfx_slide.setAlignment(QtCore.Qt.AlignCenter)

        self._meta_files_mgr = MetaFilesManager()
        self._meta_files_mgr.connect()

    def resizeEvent(self, event):
        if event.spontaneous():
            self._control_widget = SlideshowControlWidget(self._slideshow_iterval)
            self._control_widget.stop_slideshow.connect(self.closeWindow)
            self._control_widget.start_slideshow.connect(self.slideshow_start)
            self._control_widget.next_slide.connect(self.slide_next_img)
            self._control_widget.prev_slide.connect(self.slide_prev_img)
            self._control_widget.slideshow_interval_changed.connect(self.on_slideshow_interval_changed)

            self._control_widget_proxy = self._gfx_scene.addWidget(self._control_widget)
            self._control_widget_proxy.setY(self.gfx_slide.size().height() - self._control_widget_proxy.size().height())
            self._control_widget_proxy.setZValue(1)
            self._control_widget_proxy.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, True)

            self.slideshow_start()

    @pyqtSlot(object)
    def on_mouse_moved(self, mouse_pos):
        self.show_slideshow_controls()
        self.slideshow_stop()
        self._idle_timer.stop()
        self._idle_timer.start(self._mouse_idle_interval)

    @pyqtSlot()
    def slideshow_start(self):
        self.hide_slideshow_controls()
        dr_img = self._meta_files_mgr.get_scan_dir_image(self._curr_sd_id, self._curr_img_serial)
        self.load_image(dr_img['abspath'])
        self._timer.start(self._slideshow_iterval)

    def slideshow_stop(self):
        self._timer.stop()

    @pyqtSlot()
    def slide_next_img(self):
        self._curr_img_serial += 1
        dr_img = self._meta_files_mgr.get_scan_dir_image(self._curr_sd_id, self._curr_img_serial)
        if not dr_img:
            if self._is_slideshow_looped:
                self._curr_img_serial = 0
                self._timer.start(self._slideshow_iterval)
            else:
                self._curr_img_serial -= 1
                self._timer.stop()
        else:
            self.load_image(dr_img['abspath'])
            if self._is_slideshow:
                self._timer.start(self._slideshow_iterval)

    @pyqtSlot()
    def slide_prev_img(self):
        self._curr_img_serial -= 1
        dr_img = self._meta_files_mgr.get_scan_dir_image(self._curr_sd_id, self._curr_img_serial)
        if not dr_img:
            self._curr_img_serial += 1
        else:
            self.load_image(dr_img['abspath'])

    @pyqtSlot(object)
    def on_slideshow_interval_changed(self, interval):
        self._slideshow_iterval = interval

    def load_image(self, abspath):
        if self._gfx_item:
            self._gfx_scene.removeItem(self._gfx_item)
        self.gfx_slide.viewport().update()
        self.gfx_slide.centerOn(0, 0)

        self._gfx_item = QGraphicsPixmapItem()
        img = QImage(abspath)
        pixmap = QPixmap(img)
        pixmap = pixmap.scaled(self.gfx_slide.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self._control_widget_proxy.setX((pixmap.width() / 2) - (self._control_widget_proxy.size().width() / 2))
        self._gfx_item.setPixmap(pixmap)

        self._gfx_scene.addItem(self._gfx_item)
        self._gfx_scene.setSceneRect(self._gfx_item.sceneBoundingRect())

    @pyqtSlot()
    def show_slideshow_controls(self):
        self.setCursor(QtCore.Qt.ArrowCursor)
        self._control_widget.show()

    @pyqtSlot()
    def hide_slideshow_controls(self):
        self.setCursor(QtCore.Qt.BlankCursor)
        self._control_widget.hide()

    @QtCore.pyqtSlot()
    def closeWindow(self):
        self._timer.stop()
        self._meta_files_mgr.disconnect()
        self.close()
