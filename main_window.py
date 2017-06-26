"""
MainWindow module
author: Julien Dcruz
last edited: 7th December 2016
"""

import sys
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QFileDialog
from ui import ui_mainwindow
from foldermanager_window import FolderManagerWindow


class MainWindow(QMainWindow, ui_mainwindow.Ui_MainWindow):
    def __init__(self, parent=None):
        self.w = 0

        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.action_FolderManager.triggered.connect(self.action_FolderManager_Clicked)


    def action_FolderManager_Clicked(self):
        self.w = FolderManagerWindow()
        self.w.show()



