"""
MainWindow module
author: Julien Dcruz
last edited: 7th December 2016
"""

import sys
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QSize, QThread, QModelIndex
from PyQt5.QtCore import QItemSelectionModel, QItemSelection, QSize, QPointF
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFont, QIcon
from PyQt5.QtGui import QPixmap, QImage, QColor, QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtWidgets import QGridLayout, QLabel, QWidget, QPushButton
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QListView
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QGraphicsGridLayout, QScroller
from .meta_files import MetaFilesManager
from .ui.ui_mainwindow import Ui_MainWindow
from .foldermanager_window import FolderManagerWindow
from .slideshow_window import SlideshowWindow
from .qgraphics_thumb_item import QGraphicsThumbnailItem

from .watcher import Watcher
from .log import LOGGER


class MainWindow(QMainWindow, Ui_MainWindow):

    _batch_count = 50

    _TV_FOLDERS_ITEM_MAP = {}

    # signals
    _dir_load_start = pyqtSignal(object)
    _dir_watcher_start = pyqtSignal()

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.w = None
        self._thumb_row_count = 0
        self._thumb_col_count = 0
        self._thumb_curr_row_width = 0

        # threads
        self._dir_watcher_thread = QThread()

        # helpers
        self._meta_files_mgr = MetaFilesManager()
        self._watch = Watcher()

        # connections
        self._setup_connections()

        self._setup_scan_dir_list_model()

        self.listView_thumbs.setIconSize(QSize(128, 128))
        self.listView_thumbs.setGridSize(QSize(148, 148))
        # self.listView_thumbs.setSpacing(16)

        self.statusBar().showMessage("Ready")

    def resizeEvent(self, event):
        if event.spontaneous():
            # Begin loading the currently selected dir
            folders_index = self._dirs_list_model.indexFromItem(self._TV_FOLDERS_ITEM_MAP[0])
            if self._dirs_list_model.rowCount(folders_index) > 0:
                self._dirs_list_selection_model.select(
                    self._dirs_list_model.index(0, 0).child(0, 0),
                    QItemSelectionModel.Select | QItemSelectionModel.Rows
                )
                selected = self.treeView_scandirs.selectedIndexes()
                sd_id = selected[0].data(QtCore.Qt.UserRole + 1)
                if sd_id > 0:
                    self._load_dir_images(sd_id)
            # Start the dir watcher thread
            self.init_watch_thread()

    def _setup_connections(self):
        # Menu
        self.action_FolderManager.triggered.connect(self.action_FolderManager_Clicked)

        # Btns
        self.btn_slideshow.clicked.connect(self.start_slideshow)

        # Watcher
        self._dir_watcher_start.connect(self._watch.watch_all)
        self._watch.new_img_found.connect(self.on_new_img_found)
        self._watch.watch_all_done.connect(self.on_watch_all_done)
        self._watch.dir_added_or_updated.connect(self.on_dir_added_or_updated)
        self._watch.dir_empty_or_deleted.connect(self.on_dir_empty_deleted)

        # TV
        self.treeView_scandirs.clicked.connect(self.on_scan_dir_treeView_clicked)

    def init_watch_thread(self):
        self._watch.moveToThread(self._dir_watcher_thread)
        self._dir_watcher_thread.start()
        LOGGER.info('Watcher thread started.')
        self._dir_watcher_start.emit()

    def _setup_scan_dir_list_model(self):
        scan_dirs = self._meta_files_mgr.get_scan_dirs()
        self._dirs_list_model = QStandardItemModel()
        self._dirs_list_selection_model = QItemSelectionModel(self._dirs_list_model)
        self._thumbs_view_model = QStandardItemModel()

        self._dirs_list_model.setColumnCount(1)
        # self._dirs_list_model.setRowCount(len(scan_dirs))

        self._root_tree_item = self._dirs_list_model.invisibleRootItem()
        # FOLDERS item
        folder_item = QStandardItem("Folders")
        folder_item_font = QFont()
        folder_item_font.setBold(True)
        folder_item.setFont(folder_item_font)
        folder_item.setSizeHint(QSize(folder_item.sizeHint().width(), 24))
        self._root_tree_item.appendRow(folder_item)
        self._TV_FOLDERS_ITEM_MAP[0] = folder_item

        self.treeView_scandirs.setModel(self._dirs_list_model)
        self.treeView_scandirs.setSelectionModel(self._dirs_list_selection_model)
        self.treeView_scandirs.expandAll()

        if scan_dirs:
            for idx, dir in enumerate(scan_dirs):
                item_title = "%s(%s)" % (dir['name'], dir['img_count'])
                item = QStandardItem(item_title)
                item.setData(dir['id'], QtCore.Qt.UserRole + 1)
                item.setSizeHint(QSize(item.sizeHint().width(), 24))
                item.setIcon(QIcon(':/images/icon_folder'))
                folder_item.appendRow(item)
                self._TV_FOLDERS_ITEM_MAP[dir['id']] = item
    
    def action_FolderManager_Clicked(self):
        self.w = FolderManagerWindow()
        self.w.show()

    def _load_dir_images(self, sd_id):
        LOGGER.debug("Folder(%s) loading starting...." % sd_id)

        dir_info = self._meta_files_mgr.get_scan_dir(sd_id)
        self.lbl_dir_name.setText(dir_info['name'])

        images = self._meta_files_mgr.get_scan_dir_images(sd_id)
        tot_img_count = len(images)
        batch_counter = 0
        img_batch = []


        for img in images:
            img['thumb'] = QImage.fromData(img['thumb'])
            self.add_img_to_scene_graph(img)
            img_batch.append(img)
            batch_counter = batch_counter + 1

            # Call processEvents() every <BATCH_COUNT> images
            # The first condition covers both cases:
            #   1. When <tot_img_count> < <BATCH_COUNT>
            #   2. When <tot_img_count> is not a multiple of <BATCH_COUNT>
            #      thereby leaving a batch of images less than <BATCH_COUNT> at the end
            if batch_counter >= tot_img_count or batch_counter % self._batch_count == 0:
                QApplication.processEvents()

        self.listView_thumbs.setModel(self._thumbs_view_model)
        # self.listView_thumbs.setMovement(QListView.Snap)
        QScroller.grabGesture(self.listView_thumbs.viewport(),
                              QScroller.LeftMouseButtonGesture)
        LOGGER.debug("Folder(%s) loading ended." % sd_id)
        print(self.listView_thumbs.iconSize())

    def add_img_to_scene_graph(self, img):
        LOGGER.debug("Adding Image(%s) to scene graph." % img['name'])
        item = QStandardItem()
        item.setText(img['name'])
        item.setIcon(QIcon(QPixmap.fromImage(img['thumb'])))

        # thumb_shadow_effect = QGraphicsDropShadowEffect()
        # thumb_shadow_effect.setOffset(1.5)
        # thumb_shadow_effect.setColor(QColor(232, 232, 232))
        # item.setGraphicsEffect(thumb_shadow_effect)
        self._thumbs_view_model.appendRow(item)

    def _tv_add_scan_dir(self, dir_info, highlight=False):
        item_title = "%s(%s)" % (dir_info['name'], dir_info['img_count'])
        item = QStandardItem(item_title)
        item.setData(dir_info['id'], QtCore.Qt.UserRole + 1)
        item.setSizeHint(QSize(item.sizeHint().width(), 24))
        item.setIcon(QIcon(':/images/icon_folder'))
        if highlight:
            bold_font = QFont()
            bold_font.setBold(True)
            item.setFont(bold_font)
        folder_item = self._TV_FOLDERS_ITEM_MAP[0]
        folder_item.appendRow(item)
        self._TV_FOLDERS_ITEM_MAP[dir_info['id']] = item

    def _clear_thumbs(self):
        self._thumbs_view_model.clear()

    @pyqtSlot()
    def start_slideshow(self):
        self._slideshow = SlideshowWindow()
        self._slideshow.showFullScreen()

    @pyqtSlot(QModelIndex)
    def on_scan_dir_treeView_clicked(self, index):
        sd_id = index.data(QtCore.Qt.UserRole + 1)
        # Categories tree nodes will not contain 'data'
        if sd_id:
            self._clear_thumbs()
            self._load_dir_images(sd_id)

    @pyqtSlot(object)
    def on_new_img_found(self, img_info):
        self.statusBar().showMessage("Found new image: %s - %s" %
                                     (img_info['dir'],
                                      img_info['filename']))

    @pyqtSlot(object)
    def on_dir_added_or_updated(self, dir_info):
        if dir_info['id'] in self._TV_FOLDERS_ITEM_MAP:
            item = self._TV_FOLDERS_ITEM_MAP[dir_info['id']]
            item_title = "%s(%s)" % (dir_info['name'], dir_info['img_count'])
            item.setText(item_title)
            bold_font = QFont()
            bold_font.setBold(True)
            item.setFont(bold_font)
        else:
            self._tv_add_scan_dir(dir_info, True)

    @pyqtSlot(object)
    def on_dir_empty_deleted(self, dir_info):
        if dir_info['id'] in self._TV_FOLDERS_ITEM_MAP:
            item = self._TV_FOLDERS_ITEM_MAP[dir_info['id']]
            item_index = self._dirs_list_model.indexFromItem(item)
            parent_index = self._dirs_list_model.indexFromItem(self._TV_FOLDERS_ITEM_MAP[0])
            self._dirs_list_model.removeRow(item_index.row(), parent_index)
            self._TV_FOLDERS_ITEM_MAP.pop(dir_info['id'])

    @pyqtSlot()
    def on_watch_all_done(self):
        self.statusBar().clearMessage()
