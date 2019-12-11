"""
Slideshow QGraphicsView
author: Julien Dcruz
"""

from imagius.log import LOGGER
from imagius.constants import ScrollDirection
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2.QtCore import QModelIndex, Signal, QPropertyAnimation, QRect, Slot, QPointF
from PySide2.QtWidgets import QListView, QScroller
from PySide2.QtGui import QImage, QStandardItem, QIcon, QPixmap
import sys
import math
from collections import deque
from imagius import settings
from imagius.settings import SettingType
from imagius.imagius_types import Thumb_Caption_Type


class ThumbsListView(QtWidgets.QListView):

    load_dir_images_for_scroll_up = QtCore.Signal(int, int)
    load_dir_images_for_scroll_down = QtCore.Signal(int, int)
    empty_area_clicked = QtCore.Signal()

    _thumb_tilemap = deque()

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

        # Batched causes repaints every time new items are added so we have keep this at SinglePass
        # self.setLayoutMode(QtWidgets.QListView.Batched)
        self.setLayoutMode(QtWidgets.QListView.SinglePass)

        self.setViewMode(QtWidgets.QListView.IconMode)
        self.setUniformItemSizes(False)
        self.setObjectName("listView_thumbs")

        # self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.setIconSize(QtCore.QSize(128, 128))
        self.setGridSize(QtCore.QSize(148, 148))
        # self.listView_thumbs.setSpacing(16)

        # self._scroller = QScroller.scroller(self)

        self._scroll_in_progress = False

        # self.verticalScrollBar().setSingleStep(5)
        # self.setFixedHeight(1700)
        # self._scrollY = QPointF(0, 0)

    def mousePressEvent(self, event):
        self.clearSelection()
        QtWidgets.QListView.mousePressEvent(self, event)
        self.empty_area_clicked.emit()

    def wheelEvent(self, event):
        # event.accept()
        event.ignore()
        super(type(self), self).wheelEvent(event)

        if event.angleDelta().y() < 0:
            curr_scroll_direction = ScrollDirection.Down

            # self._scrollY.setY(self._scrollY.y() + 50)
            # print(self._scrollY)
            # self._scroller.scrollTo(self._scrollY)
        else:
            curr_scroll_direction = ScrollDirection.Up

            # self._scrollY.setY(self._scrollY.y() - 50)
            # print(self._scrollY)
            # self._scroller.scrollTo(self._scrollY)

        row = 0
        visible_items = []
        invisible_items = []
        invisible_items_count = 0

        # Detecting thumbs that become invisible so we can delete them
        while True:
            item = self.model().item(row, 0)
            if not item:
                break

            item_index = self.model().indexFromItem(item)

            iserial = item.data(QtCore.Qt.UserRole + 2)

            thumb_rect = self.visualRect(item_index)
            rect = thumb_rect.adjusted(
                0, 0, 0, (self.gridSize().height() - thumb_rect.height()))

            if self.viewport().rect().intersects(rect):
                visible_items.append(item)
            else:
                invisible_items.append(item)
                invisible_items_count = invisible_items_count + 1
            row = row + 1

        # Deleting hidden thumbs
        if len(invisible_items) > 0:
            self.model().removeRows(
                invisible_items[0].row(), len(invisible_items))

        curr_thumb_display_size = settings.get(
            SettingType.UI_THUMBS_SIZE, 128, 'int')
        new_thumbs_load_count = self.get_thumb_col_count(
            curr_thumb_display_size + 20)

        if curr_scroll_direction == ScrollDirection.Up:
            new_thumbs_load_count = new_thumbs_load_count + 0

            if not self._scroll_in_progress:
                self.load_dir_images_for_scroll_up.emit(
                    self.first_thumb_serial(), new_thumbs_load_count)

        if curr_scroll_direction == ScrollDirection.Down:
            new_thumbs_load_count = new_thumbs_load_count + 0

            load_from_serial = self.last_thumb_serial()
            if not self._scroll_in_progress:
                self.load_dir_images_for_scroll_down.emit(
                    load_from_serial, new_thumbs_load_count)

        self._scroll_in_progress = True

    @Slot(object, int)
    def render_thumbs(self, images, scroll_direction):
        img_count = len(images)
        print('Recevied %s images' % img_count)
        LOGGER.debug('Recevied %s images' % img_count)
        for img in images:
            img['thumb'] = QImage.fromData(img['thumb'])
            item = QStandardItem()

            thumb_caption_type = settings.get(
                SettingType.UI_THUMBS_CAPTION_DISPLAY_MODE, Thumb_Caption_Type.NoCaption.name)
            if thumb_caption_type == Thumb_Caption_Type.FileName.name:
                item.setText(img['name'])

            item.setData(img['id'], QtCore.Qt.UserRole + 1)
            item.setData(img['serial'], QtCore.Qt.UserRole + 2)
            item.setIcon(QIcon(QPixmap.fromImage(img['thumb'])))
            item.setText(str(img['serial']))

            if scroll_direction == ScrollDirection.Up:
                self.model().insertRow(0, item)
                self._first_thumb_serial = images[0]['serial']
            if scroll_direction == ScrollDirection.Down:
                self.model().appendRow(item)
                self._last_thumb_serial = images[len(images)-1]['serial']

        # self._scrollY.setY(self._scrollY.y() + 10)
        # print(self._scrollY)
        # self._scroller.scrollTo(self._scrollY)

        self._scroll_in_progress = False

    def first_thumb_serial(self):
        item = self.model().item(0, 0)
        return item.data(QtCore.Qt.UserRole + 2)

    def last_thumb_serial(self):
        item = self.model().item(self.model().rowCount()-1, 0)
        return item.data(QtCore.Qt.UserRole + 2)

    def get_thumb_col_count(self, thumb_size):
        return int(self.width() / thumb_size)

    def get_thumb_row_count(self, thumb_size):
        row_len = float(self.height() / thumb_size)

    def get_visible_thumb_count(self, thumb_size):
        col_len = float(self.width() / thumb_size)
        row_len = float(self.height() / thumb_size)

        # Add 2 to row_len to load one more row after the last visiable row to be activate scrolling functionality
        row_len = row_len + 0

        visisble_item_count = int(row_len * col_len)
        # Roundup to the nearest 10
        visisble_item_count = math.ceil(visisble_item_count / 10.0) * 10
        return visisble_item_count
