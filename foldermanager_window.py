"""
Folder Manager Window module
author: Julien Dcruz
last edited: 8th April 2017
"""

import sys
import os
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox
from PyQt5 import QtCore
from PyQt5.QtCore import QDir, QStandardPaths
from ui import ui_foldermanager
from log import LOGGER
import foldermanager


class FolderManagerWindow(QDialog, ui_foldermanager.Ui_FolderManagerWindow):
    def __init__(self, folder_mgr, parent=None):
        super(FolderManagerWindow, self).__init__(parent)
        self.setupUi(self)

        self.folder_mgr = folder_mgr
        self.model = QStandardItemModel()

        self.btn_AddFolder.clicked.connect(self.add_folder)
        self.btn_EditFolder.clicked.connect(self.edit_folder)
        self.btn_DeleteFolder.clicked.connect(self.delete_folder)
        self.btn_Close.clicked.connect(self.close)

        self.populate_folder_tree()

    def populate_folder_tree(self):
        """
        <TODO>
        """
        watched_folders = self.folder_mgr.get_watched_folders()
        self.model.setColumnCount(1)
        self.model.setRowCount(len(watched_folders))
        for idx, folder in enumerate(watched_folders):
            item = QStandardItem(folder["name"])
            item.setData(folder['id'], QtCore.Qt.UserRole + 1)
            self.model.setItem(idx, 0, item)
        self.listView_FolderList.setModel(self.model)


    def add_folder(self):
        """
        <TODO>
        """
        folder_path = QFileDialog.getExistingDirectory(self)
        folder_name = os.path.basename((folder_path))
        folder_id = self.folder_mgr.add_watched_folder(folder_path, folder_name)
        LOGGER.info('Added watched folder (fid:%s)' % folder_id)

        self.populate_folder_tree()


    def edit_folder(self):
        selected = self.listView_FolderList.selectedIndexes()
        if len(selected) > 0:
            selected_index = selected[0]
            folder_id = selected_index.data(QtCore.Qt.UserRole + 1)

            new_folder_path = QFileDialog.getExistingDirectory(self)
            new_folder_name = os.path.basename((new_folder_path))
            self.folder_mgr.edit_watched_folder(folder_id, new_folder_path, new_folder_name)
            LOGGER.info('Edited watched folder (fid:%s)' % folder_id)

            self.populate_folder_tree()

        else:
            QMessageBox.about(self, "No selection", "Please select an entry to edit")

    def delete_folder(self):
        selected = self.listView_FolderList.selectedIndexes()
        if len(selected) > 0:
            selected_index = selected[0]
            folder_id = selected_index.data(QtCore.Qt.UserRole + 1)
            self.folder_mgr.delete_watched_folder(folder_id)
            LOGGER.info('Deleted watched folder (fid:%s)' % folder_id)

            self.populate_folder_tree()
        else:
            QMessageBox.about(self, "No selection", "Please select an entry to delete")



    def closeWindow(self):
        self.close()



