"""
MainWindow module
author: Julien Dcruz
last edited: 7th December 2016
"""

import sys
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from foldermanager import FolderManager
from ui import ui_mainwindow
from foldermanager_window import FolderManagerWindow


class MainWindow(QMainWindow, ui_mainwindow.Ui_MainWindow):
    def __init__(self, parent=None):
        self.w = None
        self.folder_mgr = FolderManager()

        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.action_FolderManager.triggered.connect(self.action_FolderManager_Clicked)

        #self.folder_mgr.init_watch_thread()


    def action_FolderManager_Clicked(self):
        self.w = FolderManagerWindow(self.folder_mgr)
        self.w.show()



