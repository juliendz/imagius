"""
Folder Manager Window module
author: Julien Dcruz
last edited: 8th April 2017
"""

import sys
import os
from PySide2.QtWidgets import QWidget
from PySide2 import QtCore
from PySide2.QtCore import QDir, QStandardPaths

from imagius.folder_manager import FolderManager
from imagius.ui.ui_slideshowcontrolwidget import Ui_SlideshowControlWidget
from imagius.log import LOGGER


class SlideshowControlWidget(QWidget, Ui_SlideshowControlWidget):

    stop_slideshow = QtCore.Signal()
    start_slideshow = QtCore.Signal()
    next_slide = QtCore.Signal()
    prev_slide = QtCore.Signal()
    slideshow_interval_changed = QtCore.Signal(object)

    def __init__(self, slideshow_interval, parent=None):
        super(SlideshowControlWidget, self).__init__(parent)
        self.setupUi(self)
        self.setMouseTracking(True)

        self._slideshow_interval = slideshow_interval
        self.setSlideshowIntervalLabel()

        self.btn_start_slideshow.pressed.connect(self.start_slideshow)
        self.btn_exit.pressed.connect(self.stop_slideshow)
        self.btn_next_slide.pressed.connect(self.next_slide)
        self.btn_prev_slide.pressed.connect(self.prev_slide)

        self.btn_incre_interval.pressed.connect(self.incre_interval)
        self.btn_decre_interval.pressed.connect(self.decre_interval)

    def incre_interval(self):
        self._slideshow_interval += 1000
        self.setSlideshowIntervalLabel()
        self.slideshow_interval_changed.emit(self._slideshow_interval)

    def decre_interval(self):
        if self._slideshow_interval > 1000:
            self._slideshow_interval -= 1000
            self.setSlideshowIntervalLabel()
            self.slideshow_interval_changed.emit(self._slideshow_interval)

    def setSlideshowIntervalLabel(self):
        self.lbl_display_time.setText(
            "%d" % (int(self._slideshow_interval) / 1000))
