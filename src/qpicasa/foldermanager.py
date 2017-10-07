"""
Folder Manager module
author: Julien Dcruz
"""
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from .foldermanager_db import FolderManagerDB
from .watcher import Watcher
from .log import LOGGER


class FolderManager(QObject):
    # Signals
    folder_watch_started = pyqtSignal()

    def __init__(self):
        super(FolderManager, self).__init__()
        self._folder_mgr_db = FolderManagerDB()
        self._thread = QThread()
        self._watch = Watcher()
        # Connections
        self.folder_watch_started.connect(self._watch.watch_all)

    def init_watch_thread(self):
        self._watch.moveToThread(self._thread)
        self._thread.start()
        LOGGER.info('Watcher thread started.')
        self.folder_watch_started.emit()

    def get_watched_dirs(self):
        return self._folder_mgr_db.get_watched_dirs()

    def add_watched_folder(self, folder_path, folder_name):
        return self._folder_mgr_db.add_watched_folder(folder_path, folder_name)

    def edit_watched_folder(self, fid, new_folder_path, new_folder_name):
        return self._folder_mgr_db.edit_watched_folder(fid, new_folder_path, new_folder_name)

    def delete_watched_folder(self, fid):
        return self._folder_mgr_db.delete_watched_folder(fid)
