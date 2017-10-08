"""
MainWindow module
author: Julien Dcruz
last edited: 7th December 2016
"""

import sys
from PyQt5 import QtCore
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFont
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QSize
from .folder_manager import FolderManager
from .meta_files import MetaFilesManager
from .ui.ui_mainwindow import Ui_MainWindow
from .foldermanager_window import FolderManagerWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        self.w = None
        self.folder_mgr = FolderManager()
        self._meta_files_mgr = MetaFilesManager()


        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.action_FolderManager.triggered.connect(self.action_FolderManager_Clicked)

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

        self.folder_mgr.init_watch_thread()


    def action_FolderManager_Clicked(self):
        self.w = FolderManagerWindow(self.folder_mgr)
        self.w.show()



