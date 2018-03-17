"""
Slideshow QGraphicsView
author: Julien Dcruz
"""

import sys
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from .log import LOGGER


class ThumbsListView(QtWidgets.QListView):

    empty_area_clicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(QtWidgets.QListView, self).__init__(parent)
        self.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.setDragEnabled(False)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.setIconSize(QtCore.QSize(0, 0))
        self.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.setMovement(QtWidgets.QListView.Snap)
        self.setLayoutMode(QtWidgets.QListView.Batched)
        self.setViewMode(QtWidgets.QListView.IconMode)
        self.setUniformItemSizes(False)
        self.setObjectName("listView_thumbs")

        self.setIconSize(QtCore.QSize(128, 128))
        self.setGridSize(QtCore.QSize(148, 148))
        # self.listView_thumbs.setSpacing(16)

    def mousePressEvent(self, event):
        self.clearSelection()
        QtWidgets.QListView.mousePressEvent(self, event)
        self.empty_area_clicked.emit()
        