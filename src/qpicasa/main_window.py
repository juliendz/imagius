"""
MainWindow module
author: Julien Dcruz
last edited: 7th December 2016
"""

import sys
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QSize, QThread, QModelIndex
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFont
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QGridLayout, QLabel
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QGraphicsDropShadowEffect
from .folder_manager import FolderManager
from .meta_files import MetaFilesManager
from .scan_dir_loader import ScanDirLoader
from .ui.ui_mainwindow import Ui_MainWindow
from .foldermanager_window import FolderManagerWindow
from .log import LOGGER


class MainWindow(QMainWindow, Ui_MainWindow):

    #signals
    _dir_load_start = pyqtSignal(object)

    def __init__(self, parent=None):
        self.w = None
        self._img_serial_no = 0
        self._scan_dir_loader_thread = QThread()
        self.folder_mgr = FolderManager()
        self._meta_files_mgr = MetaFilesManager()
        self._scan_dir_loader = ScanDirLoader()

        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        #Connections
        self._setup_connections()

        self._setup_scan_dir_list_model()

        #Start the image loader thread
        self._scan_dir_loader.moveToThread(self._scan_dir_loader_thread)
        self._scan_dir_loader_thread.start()
        LOGGER.info('Image loader thread started.')

        #Setup the thumbs gfx scene
        self._thumbs_gfx_scene = QGraphicsScene()
        self._thumbs_gfx_scene.addText("JULIEN")
        self.gfxview_thumbs.setScene(self._thumbs_gfx_scene)
        self.gfxview_thumbs.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        #Begin loading the currently selected dir
        if self.listView_scandirs.model():
            selIndex = self._dirs_list_model.index(0,0)
            self.listView_scandirs.setCurrentIndex(selIndex)
            selected = self.listView_scandirs.selectedIndexes()
            if len(selected) > 0:
                 self._load_dir_images(selected[0])
        

    def _setup_connections(self):
        self.action_FolderManager.triggered.connect(self.action_FolderManager_Clicked)
        self._dir_load_start.connect(self._scan_dir_loader.load_scan_dir_images)
        self._scan_dir_loader.dir_image_load_success.connect(self.on_dir_images_load_success)
        self._scan_dir_loader.dir_images_load_ended.connect(self.on_dir_images_load_ended)

        self.listView_scandirs.clicked.connect(self.on_scan_dir_listview_clicked)

    def _setup_scan_dir_list_model(self):
        scan_dirs = self._meta_files_mgr.get_scan_dirs()
        if scan_dirs:
            self._dirs_list_model = QStandardItemModel()
            self._dirs_list_model.setColumnCount(1)
            self._dirs_list_model.setRowCount(len(scan_dirs))
            for idx, dir in enumerate(scan_dirs):
                item = QStandardItem(dir["name"])
                item.setData(dir['id'], QtCore.Qt.UserRole + 1)
                # item.setSizeHint(QSize(item.sizeHint().width(), 30));
                self._dirs_list_model.setItem(idx, 0, item)

            self.listView_scandirs.setModel(self._dirs_list_model)

    def action_FolderManager_Clicked(self):
        self.w = FolderManagerWindow(self.folder_mgr)
        self.w.show()

    def _load_dir_images(self, model_index):
        sd_id = model_index.data(QtCore.Qt.UserRole + 1)
        self._dir_load_start.emit(sd_id)

    def _clear_thumbs(self):
        self._thumbs_gfx_scene.clear()
        self._img_serial_no = 0
    
    @pyqtSlot(object)
    def on_dir_images_load_success(self, img):
        LOGGER.debug('Image loaded.' + img["name"])

        item = QGraphicsPixmapItem()
        item.setPixmap(QPixmap.fromImage(img['thumb']))

        thumb_shadow_effect = QGraphicsDropShadowEffect()
        thumb_shadow_effect.setOffset(3.0)
        item.setGraphicsEffect(thumb_shadow_effect)

        item.setPos(self._img_serial_no * 150, 0)
        self._thumbs_gfx_scene.addItem(item)
        self._img_serial_no = self._img_serial_no + 1


    @pyqtSlot()
    def on_dir_images_load_ended(self):
        LOGGER.debug('Image loading ended')
        #Start the dir watcher thread
        self.folder_mgr.init_watch_thread()

    @pyqtSlot(QModelIndex)
    def on_scan_dir_listview_clicked(self, index):
        self._clear_thumbs()
        self._load_dir_images(index)
        


