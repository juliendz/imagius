"""
Slideshow QGraphicsView
author: Julien Dcruz
"""

import sys
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

from imagius.log import LOGGER


class SlideshowGraphicsView(QtWidgets.QGraphicsView):

    mouse_moved = QtCore.Signal(object)

    def __init__(self, parent=None):
        super(SlideshowGraphicsView, self).__init__(parent)

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
