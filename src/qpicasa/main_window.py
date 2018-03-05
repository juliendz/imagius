"""
MainWindow module
author: Julien Dcruz
last edited: 7th December 2016
"""

import sys
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QSize, QThread, QModelIndex
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFont, QIcon
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtWidgets import QGridLayout, QLabel, QWidget
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QGraphicsDropShadowEffect
from .meta_files import MetaFilesManager
from .ui.ui_mainwindow import Ui_MainWindow
from .foldermanager_window import FolderManagerWindow
from .qgraphics_thumb_item import QGraphicsThumbnailItem

from .watcher import Watcher
from .log import LOGGER


class MainWindow(QMainWindow, Ui_MainWindow):

    BATCH_COUNT =  50

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

        #threads
        self._dir_watcher_thread = QThread()

        #helpers
        self._meta_files_mgr = MetaFilesManager()
        self._watch = Watcher()

        #connections
        self._setup_connections()

        self._setup_scan_dir_list_model()

        # Setup the thumbs gfx scene
        self._thumbs_gfx_scene = QGraphicsScene()
        self.gfxview_thumbs.setScene(self._thumbs_gfx_scene)
        self.gfxview_thumbs.setAlignment(
            QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

    def resizeEvent(self, event):
        if event.spontaneous():
            # Begin loading the currently selected dir
            if self.treeView_scandirs.model():
                selIndex = self._dirs_list_model.index(4, 0)
                self.treeView_scandirs.setCurrentIndex(selIndex)
                selected = self.treeView_scandirs.selectedIndexes()
                if len(selected) > 0:
                    self._load_dir_images(selected[0])
            else:
                pass
                # Start the dir watcher thread
            self.init_watch_thread()

    def _setup_connections(self):
        self.action_FolderManager.triggered.connect(
            self.action_FolderManager_Clicked)

        #Watcher
        self._dir_watcher_start.connect(self._watch.watch_all)

        self.treeView_scandirs.clicked.connect(
            self.on_scan_dir_treeView_clicked)

    def init_watch_thread(self):
        self._watch.moveToThread(self._dir_watcher_thread)
        self._dir_watcher_thread.start()
        LOGGER.info('Watcher thread started.')
        self._dir_watcher_start.emit()

    def _setup_scan_dir_list_model(self):
        scan_dirs = self._meta_files_mgr.get_scan_dirs()
        if scan_dirs:
            self._dirs_list_model = QStandardItemModel()

            self._dirs_list_model.setColumnCount(1)
            # self._dirs_list_model.setRowCount(len(scan_dirs))

            root_tree_item = self._dirs_list_model.invisibleRootItem()

            #FOLDERS item
            folder_item = QStandardItem("Folders")  
            folder_item_font = QFont()
            folder_item_font.setBold(True)
            folder_item.setFont(folder_item_font)
            folder_item.setSizeHint(QSize(folder_item.sizeHint().width(), 30));
            root_tree_item.appendRow(folder_item)

            for idx, dir in enumerate(scan_dirs):
                item = QStandardItem(dir["name"])
                item.setData(dir['id'], QtCore.Qt.UserRole + 1)
                item.setSizeHint(QSize(item.sizeHint().width(), 30));
                item.setIcon(QIcon(':/images/icon_folder'))
                folder_item.appendRow(item)

            self.treeView_scandirs.setModel(self._dirs_list_model)
            self.treeView_scandirs.expandAll()

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

            #Call processEvents() every <BATCH_COUNT> images
            #The first condition covers both cases:
            #   1. When <tot_img_count> < <BATCH_COUNT>
            #   2. When <tot_img_count> is not a multiple of <BATCH_COUNT>
            #      thereby leaving a batch of images less than <BATCH_COUNT> at the end
            if batch_counter >= tot_img_count or (batch_counter % self.BATCH_COUNT == 0):
                QApplication.processEvents()
        
        LOGGER.debug("Folder(%s) loading ended." % sd_id)

    def add_img_to_scene_graph(self, img):
        LOGGER.debug("Adding Image(%s) to scene graph." % img['name'])
        # item = QGraphicsPixmapItem()
        item = QGraphicsThumbnailItem()
        item.setPixmap(QPixmap.fromImage(img['thumb']))

        thumb_shadow_effect = QGraphicsDropShadowEffect()
        thumb_shadow_effect.setOffset(3.0)
        item.setGraphicsEffect(thumb_shadow_effect)

        if (self._thumb_curr_row_width + 300 > self.gfxview_thumbs.viewport().size().width()):
            self._thumb_row_count = self._thumb_row_count + 1
            self._thumb_col_count = 0
            self._thumb_curr_row_width = 0

        pos_x = (self._thumb_col_count * 150)
        pos_y = (self._thumb_row_count * 140)
        self._thumb_curr_row_width = pos_x
        item.setPos(pos_x, pos_y)

        self._thumbs_gfx_scene.addItem(item)

        self._thumb_col_count = self._thumb_col_count +  1

    def _clear_thumbs(self):
        self._thumbs_gfx_scene.clear()
        self.gfxview_thumbs.viewport().update()
        self.gfxview_thumbs.centerOn(0,0)
        self._thumb_row_count = 0
        self._thumb_col_count = 0

    @pyqtSlot(QModelIndex)
    def on_scan_dir_treeView_clicked(self, index):
        sd_id = index.data(QtCore.Qt.UserRole + 1)
        #Categories tree nodes will not contain 'data'
        if sd_id:
            self._clear_thumbs()
            self._load_dir_images(sd_id)
