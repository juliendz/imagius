"""
Slideshow QGraphicsView
author: Julien Dcruz
"""

from imagius.log import LOGGER
from imagius.constants import ScrollDirection
from PySide2.QtWidgets import QListView
from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2.QtCore import QModelIndex, Signal, QPropertyAnimation, QRect, Slot
from PySide2.QtGui import QImage, QStandardItem, QIcon, QPixmap
from PySide2 import QtCore
import sys
import math
from imagius import settings
from imagius.settings import SettingType
from imagius.imagius_types import Thumb_Caption_Type


class ThumbsListView(QtWidgets.QListView):

    load_dir_images_for_scroll_up = QtCore.Signal(int, int)
    load_dir_images_for_scroll_down = QtCore.Signal(int, int)
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

        self._prev_scroll_direction = ScrollDirection.Down
        self._curr_img_serial = 0
        self._last_hidden_thumb_serial = 0

        self.verticalScrollBar().setSingleStep(10)

    def setCurrImgSerial(self, serial: int):
        self._curr_img_serial = serial

    def mousePressEvent(self, event):
        self.clearSelection()
        QtWidgets.QListView.mousePressEvent(self, event)
        self.empty_area_clicked.emit()

    def wheelEvent(self, event):
        if event.angleDelta().y() < 0:
            curr_scroll_direction = ScrollDirection.Down
        else:
            curr_scroll_direction = ScrollDirection.Up

        event.ignore()
        super(type(self), self).wheelEvent(event)

        row = 0
        visible_items_count = 0
        invisible_items = []
        invisible_items_count = 0

        while True:
            item = self.model().item(row, 0)
            if not item:
                break

            item_index = self.model().indexFromItem(item)
            if self.viewport().rect().intersects(self.visualRect(item_index)):
                visible_items_count = visible_items_count + 1
            else:
                invisible_items.append(item)
                invisible_items_count = invisible_items_count + 1
            row = row + 1

        # If this is a first down scroll
        # if self._curr_img_serial == 0:
        #     self._curr_img_serial = row
        # else:
        if curr_scroll_direction != self._prev_scroll_direction:
            self._curr_img_serial = self._last_hidden_thumb_serial

        # Deleting hidden thumbs
        if len(invisible_items) > 0:

            # Before we delete the hidden rows we need to get the serial of the last hidden thumb
            # so we can retrieve it incase of a scroll up or scroll down
            if curr_scroll_direction == ScrollDirection.Up:
                serial = invisible_items[0].data(QtCore.Qt.UserRole + 2)
                self._last_hidden_thumb_serial = serial
            if curr_scroll_direction == ScrollDirection.Down:
                serial = invisible_items[len(
                    invisible_items)-1].data(QtCore.Qt.UserRole + 2)
                self._last_hidden_thumb_serial = serial

            self.model().removeRows(
                invisible_items[0].row(), len(invisible_items))

        curr_thumb_display_size = settings.get(
            SettingType.UI_THUMBS_SIZE, 128, 'int')
        # Calculate the number thumbs need to load to fit the screen
        new_thumbs_load_count = self.get_visible_thumb_count(
            curr_thumb_display_size + 20) - self.model().rowCount()

        if curr_scroll_direction == ScrollDirection.Up:
            new_thumbs_load_count = new_thumbs_load_count + 0
            self.load_dir_images_for_scroll_up.emit(
                self._curr_img_serial, new_thumbs_load_count)
            self._curr_img_serial = self._curr_img_serial - new_thumbs_load_count
        if curr_scroll_direction == ScrollDirection.Down:
            new_thumbs_load_count = new_thumbs_load_count + 0
            self.load_dir_images_for_scroll_down.emit(
                self._curr_img_serial, new_thumbs_load_count)

            self._curr_img_serial = self._curr_img_serial + new_thumbs_load_count

        self._prev_scroll_direction = curr_scroll_direction

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
            if scroll_direction == ScrollDirection.Down:
                self.model().appendRow(item)

    def get_visible_thumb_count(self, thumb_size):
        col_len = float(self.width() / thumb_size)
        row_len = float(self.height() / thumb_size)

        # Add 2 to row_len to load one more row after the last visiable row to be activate scrolling functionality
        row_len = row_len + 2

        visisble_item_count = int(row_len * col_len)
        # Roundup to the nearest 10
        visisble_item_count = math.ceil(visisble_item_count / 10.0) * 10
        return visisble_item_count
