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
        self.setLayoutMode(QtWidgets.QListView.Batched)
        self.setViewMode(QtWidgets.QListView.IconMode)
        self.setUniformItemSizes(False)
        self.setObjectName("listView_thumbs")

        self.setIconSize(QtCore.QSize(128, 128))
        self.setGridSize(QtCore.QSize(148, 148))
        # self.listView_thumbs.setSpacing(16)

        self._scroll_in_progress = False

        # self.verticalScrollBar().setSingleStep(5)

    def setCurrThumbIndex(self, index: int):
        self._curr_thumb_index = index

    def setCurrImgSerial(self, serial: int):
        self._curr_img_serial = serial

    def updateThumbTileMapUp(self, db_image):
        curr_thumb_display_size = settings.get(
            SettingType.UI_THUMBS_SIZE, 128, 'int')
        # rows = self.get_thumb_row_count(curr_thumb_display_size+20)
        cols = self.get_thumb_col_count(curr_thumb_display_size+20)

        first_row = self._thumb_tilemap[0]

        if len(first_row) < cols:
            first_row.append(db_image)
        else:
            first_row = []
            self._thumb_tilemap.appendleft(first_row)
            first_row.append(db_image)

    def updateThumbTileMapDown(self, db_image):
        curr_thumb_display_size = settings.get(
            SettingType.UI_THUMBS_SIZE, 128, 'int')
        # rows = self.get_thumb_row_count(curr_thumb_display_size+20)
        cols = self.get_thumb_col_count(curr_thumb_display_size+20)
        print(cols)

        last_row = []
        if len(self._thumb_tilemap) > 0:
            last_row = self._thumb_tilemap[len(self._thumb_tilemap)-1]
        else:
            self._thumb_tilemap.append(last_row)

        if len(last_row) < cols:
            last_row.append(db_image)
        else:
            last_row = []
            self._thumb_tilemap.append(last_row)
            last_row.append(db_image)

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
        visible_items = []
        invisible_items = []
        invisible_items_count = 0

        # print(self.gridSize())

        # Detecting thumbs that become invisible so we can delete them
        while True:
            item = self.model().item(row, 0)
            if not item:
                break

            item_index = self.model().indexFromItem(item)

            iserial = item.data(QtCore.Qt.UserRole + 2)
            # print("item serial %d, rect %d" %
            #   (iserial, self.visualRect(item_index).width()))

            thumb_rect = self.visualRect(item_index)
            rect = thumb_rect.adjusted(
                0, 0, 0, (self.gridSize().height() - thumb_rect.height()))
            # print(rect)
            # if self.viewport().rect().intersects(self.visualRect(item_index)):
            if self.viewport().rect().intersects(rect):
                visible_items.append(item)
            else:
                invisible_items.append(item)
                invisible_items_count = invisible_items_count + 1
            row = row + 1

        # If this is a first down scroll
        # if self._curr_img_serial == 0:
            # self._curr_img_serial = row
        # else:
            # if curr_scroll_direction != self._prev_scroll_direction:
            # serial = visible_items[0].data(QtCore.Qt.UserRole + 2)
            # self._curr_img_serial = visible_items[0]
        # serial = 0
        # if curr_scroll_direction == ScrollDirection.Up:
        #     serial = visible_items[0].data(QtCore.Qt.UserRole + 2)
        # if curr_scroll_direction == ScrollDirection.Down:
        #     serial = visible_items[len(
        #         visible_items)-1].data(QtCore.Qt.UserRole + 2)
        # self._curr_img_serial = serial

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

            # for i in invisible_items:
                # print(i.data(QtCore.Qt.UserRole + 2))

            self.model().removeRows(
                invisible_items[0].row(), len(invisible_items))

        # curr_thumb_display_size = settings.get(
        #     SettingType.UI_THUMBS_SIZE, 128, 'int')
        # # Calculate the number thumbs need to load to fit the screen
        # print("visiable thumb count %d " %
        #       self.get_visible_thumb_count(curr_thumb_display_size + 20))
        # print("model rowcount %d" % self.model().rowCount())
        # new_thumbs_load_count = self.get_visible_thumb_count(
        #     curr_thumb_display_size + 20) - self.model().rowCount()

        new_thumbs_load_count = 10

        if curr_scroll_direction == ScrollDirection.Up:
            new_thumbs_load_count = new_thumbs_load_count + 0

            print(self.first_thumb_serial())
            if not self._scroll_in_progress:
                self.load_dir_images_for_scroll_up.emit(
                    self.first_thumb_serial(), new_thumbs_load_count)
            # self._curr_img_serial = self._curr_img_serial - new_thumbs_load_count

        if curr_scroll_direction == ScrollDirection.Down:
            new_thumbs_load_count = new_thumbs_load_count + 0

            load_from_serial = self.last_thumb_serial()
            print(load_from_serial)
            if not self._scroll_in_progress:
                self.load_dir_images_for_scroll_down.emit(
                    load_from_serial, new_thumbs_load_count)
            # self._prev_last_thumb_serial = load_from_serial
            # self._curr_img_serial = self._curr_img_serial + new_thumbs_load_count

        self._scroll_in_progress = True
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

            # while True:
            #     item = self.model().item(row, 0)
            #     if not item:
            #         break

            #     serial = item.data(QtCore.Qt.UserRole + 2)
            #     if
            #     row = row + 1

            if scroll_direction == ScrollDirection.Up:
                self.model().insertRow(0, item)
                # self.updateThumbTileMapUp(img)
                self._first_thumb_serial = images[0]['serial']
            if scroll_direction == ScrollDirection.Down:
                self.model().appendRow(item)
                # self.updateThumbTileMapDown(img)
                self._last_thumb_serial = images[len(images)-1]['serial']

        self._scroll_in_progress = False
        # print(self._thumb_tilemap)

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
