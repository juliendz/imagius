"""
Folder Manager module
author: Julien Dcruz
"""
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from db import dbmgr
from watcher import Watcher


class FolderManager(QObject):

    def __init__(self):
        self.db = dbmgr("app.db")
        self.thread = QThread()
        self.watch = Watcher()

        #Signals
        self.folder_watch_started = pyqtSignal()


    def init_watch_thread(self):
        self.folder_watch_started.connect(self.watch.watch_all)
        self.watch.moveToThread(self.thread)
        self.thread.start()


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
        fid = self.db.run_insert_query(query, params)
        self.db.disconnect()
        return fid


    def edit_watched_folder(self, fid, new_folder_path, new_folder_name):
        query = "UPDATE dir SET fullpath = ?, name = ?  WHERE id = ?"
        params = (new_folder_path, new_folder_name, fid)
        self.db.connect()
        self.db.run_query(query, params)
        self.db.disconnect()


    def delete_watched_folder(self, fid):
        query = "DELETE FROM dir WHERE id = ?"
        params = (fid,)
        self.db.connect()
        self.db.run_query(query, params)
        self.db.disconnect()
