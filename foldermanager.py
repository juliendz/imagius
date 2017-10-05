"""
Folder Manager module
author: Julien Dcruz
"""
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from db import dbmgr
from watcher import Watcher

scan_folders = pyqtSignal()
thread = QThread()
watch = Watcher()

db = dbmgr("app.db")


def init_watch_thread():
    watch.moveToThread(thread)


def get_watched_folders():
    query = "SELECT * FROM dir"
    db.connect()
    res = db.run_select_query(query)
    db.disconnect()
    return res


def add_watched_folder(folder_path, folder_name):
    query = "INSERT INTO dir (fullpath, name) VALUES (?, ?)"
    params = (folder_path, folder_name)
    db.connect()
    db.run_insert_query(query, params)
    db.disconnect()
