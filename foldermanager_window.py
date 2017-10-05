"""
Folder Manager Window module
author: Julien Dcruz
last edited: 8th April 2017
"""

import sys
import os
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.QtCore import QDir, QStandardPaths
from ui import ui_foldermanager
import foldermanager


class FolderManagerWindow(QDialog, ui_foldermanager.Ui_FolderManagerWindow):
    def __init__(self, parent=None):
        super(FolderManagerWindow, self).__init__(parent)
        self.setupUi(self)

        self.model = QStandardItemModel()

        self.btn_AddFolder.clicked.connect(self.add_folder)
        self.btn_EditFolder.clicked.connect(self.edit_folder)
        self.btnbox_okcancel.accepted.connect(self.accept)
        self.btnbox_okcancel.rejected.connect(self.reject)

        self.populate_folder_tree()

    def populate_folder_tree(self):
        """
        <TODO>
        """
        watched_folders = foldermanager.get_watched_folders()
        self.model.setColumnCount(1)
        self.model.setRowCount(len(watched_folders))
        for idx, folder in enumerate(watched_folders):
            item = QStandardItem(folder["name"])
            #item.setData("HELLO")
            self.model.setItem(idx, 0, item)
        self.listView_FolderList.setModel(self.model)


    def add_folder(self):
        """
        <TODO>
        """
        folder_path = QFileDialog.getExistingDirectory(self)
        folder_name = os.path.basename((folder_path))
        foldermanager.add_watched_folder(folder_path, folder_name)


    def edit_folder(self):
        selected = self.listView_FolderList.selectedIndexes()
        if len(selected) > 0:
            new_folder_path = QFileDialog.getExistingDirectory(self)
            selected_index = selected[0]
            print(selected_index.data())

    def delete_folder(self):
        pass


    def accept(self):
        pass



