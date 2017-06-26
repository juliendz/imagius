"""
Folder Manager module
author: Julien Dcruz
"""
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from db import dbmgr

class FolderManager:
    scan_folders = pyqtSignal()

    def __init__(self):
        self.db = dbmgr("app.db")


    def init_watch_thread(self):
        pass

    def get_watched_folders(self):
        query = "SELECT * FROM dir"
        self.db.connect()
        res = self.db.run_select_query(query)
        self.db.disconnect()
        return res

    def add_watched_folder(self, folder_path, folder_name):
        query = "INSERT INTO dir (fullpath, name) VALUES (?, ?)"
        params = (folder_path, folder_name)
        self.db.connect()
        self.db.run_insert_query(query, params)
        self.db.disconnect()
    



