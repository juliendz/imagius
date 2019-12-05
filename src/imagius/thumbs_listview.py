"""
Slideshow QGraphicsView
author: Julien Dcruz
"""

import sys
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

from imagius.log import LOGGER


class ThumbsListView(QtWidgets.QListView):

    empty_area_clicked = QtCore.Signal()

    def __init__(self, parent=None):
        super(ThumbsListView, self).__init__(parent)
        self.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.setDragEnabled(False)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.setIconSize(QtCore.QSize(0, 0))
        self.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.setHorizontalScrollMode(
            QtWidgets.QAbstractItemView.ScrollPerPixel)
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
