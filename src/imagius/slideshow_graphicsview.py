"""
Slideshow QGraphicsView
author: Julien Dcruz
"""

import sys
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from .log import LOGGER


class SlideshowGraphicsView(QtWidgets.QGraphicsView):

    mouse_moved = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super(QtWidgets.QGraphicsView, self).__init__(parent)

        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setLineWidth(0)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.setBackgroundBrush(brush)
        self.setInteractive(False)
        self.setObjectName("gfx_slide")
        self.setInteractive(True)
        self.setMouseTracking(True)
        self.setAttribute(QtCore.Qt.WA_Hover)

    def mouseMoveEvent(self, event):
        self.mouse_moved.emit(event.pos())

    # def drawBackground(self, painter, rect):
    #     self.setCacheMode(self.CacheNone)

    #     painter.save()
    #     painter.setPen(QtGui.QPen(QtCore.Qt.red, 5))
    #     painter.drawRect(self.scene().sceneRect())
    #     painter.restore()
