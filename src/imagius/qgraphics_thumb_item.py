"""
QGraphics Thumbnail item module
author: Julien Dcruz
"""

import sys
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QSize, QThread, QModelIndex
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFont
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsItem
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

