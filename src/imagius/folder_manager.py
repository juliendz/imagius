"""
Folder Manager module
author: Julien Dcruz
"""
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from .db import dbmgr
import settings
from .log import LOGGER


class FolderManager(QObject):

    def __init__(self, dbpath=settings.get_settings_db_path()):
        super(FolderManager, self).__init__()
        self._db = dbmgr(dbpath)

    def get_watched_dirs(self):
        query = "SELECT * FROM dir"
        self._db.connect()
        res = self._db.run_select_query(query)
        self._db.disconnect()
        return res

    def add_watched_folder(self, folder_path, folder_name):
        query = "INSERT INTO dir (abspath, name) VALUES (?, ?)"
        params = (folder_path, folder_name)
        self._db.connect()
        fid = self._db.run_insert_query(query, params)
        self._db.disconnect()
        return fid

    def edit_watched_folder(self, fid, new_folder_path, new_folder_name):
        query = "UPDATE dir SET abspath = ?, name = ?  WHERE id = ?"
        params = (new_folder_path, new_folder_name, fid)
        self._db.connect()
        self._db.run_query(query, params)
        self._db.disconnect()

    def delete_watched_folder(self, fid):
        query = "DELETE FROM dir WHERE id = ?"
        params = (fid,)
        self._db.connect()
        self._db.run_query(query, params)
        self._db.disconnect()

    
