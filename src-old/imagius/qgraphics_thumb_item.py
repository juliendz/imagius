"""
QGraphics Thumbnail item module
author: Julien Dcruz
"""

import sys
from PySide2 import QtCore
from PySide2.QtCore import Signal, pyqtSlot, QSize, QThread, QModelIndex
from PySide2.QtGui import QStandardItemModel, QStandardItem, QFont
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QGraphicsPixmapItem, QGraphicsItem
from log import LOGGER


class QGraphicsThumbnailItem(QGraphicsPixmapItem):

    def __init__(self, parent=None):
        super(QGraphicsPixmapItem, self).__init__(parent)
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)

    def hoverEnterEvent(self, event):
        super(QGraphicsPixmapItem, self).hoverEnterEvent(event)

    # def paint(self, painter, option, widget):
    #     super(QGraphicsPixmapItem, self).paint(painter, option, widget)
    #     painter.setText
