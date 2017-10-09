"""
MainWindow module
author: Julien Dcruz
last edited: 7th December 2016
"""

import sys
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QSize, QThread, QModelIndex
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFont
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QFileDialog
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
        self._scan_dir_loader_thread = QThread()
        self.folder_mgr = FolderManager()
        self._meta_files_mgr = MetaFilesManager()
        self._scan_dir_loader = ScanDirLoader()

        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        #Connections
        self.action_FolderManager.triggered.connect(self.action_FolderManager_Clicked)
        self._dir_load_start.connect(self._scan_dir_loader.load_scan_dir_images)
        self._scan_dir_loader.dir_image_load_success.connect(self.on_dir_images_load_success)
        self._scan_dir_loader.dir_images_load_ended.connect(self.on_dir_images_load_ended)

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

        #Start the dir watcher thread
        self.folder_mgr.init_watch_thread()

        #Start the image loader thread
        self._scan_dir_loader.moveToThread(self._scan_dir_loader_thread)
        self._scan_dir_loader_thread.start()

        #Begin loading the currently selected dir
        selIndex = self._dirs_list_model.index(0,0)
        self.listView_scandirs.setCurrentIndex(selIndex)
        selected = self.listView_scandirs.selectedIndexes()
        if len(selected) > 0:
            selected_index = selected[0]
            sd_id = selected_index.data(QtCore.Qt.UserRole + 1)
            self._dir_load_start.emit(sd_id)



    def action_FolderManager_Clicked(self):
        self.w = FolderManagerWindow(self.folder_mgr)
        self.w.show()

    
    @pyqtSlot(object)
    def on_dir_images_load_success(self, img):
        LOGGER.debug('Image loaded.' + img["name"])

    @pyqtSlot()
    def on_dir_images_load_ended(self):
        LOGGER.debug('Image loading ended')



