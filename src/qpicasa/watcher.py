"""
File/Folder Watcher module
author: Julien Dcruz
"""

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QDirIterator, qDebug
from PyQt5.QtCore import QDir
from .log import LOGGER
from .foldermanager_db import FolderManagerDB


class Watcher(QObject):
    """
    <TODO>
    """
    watch_all_done = pyqtSignal()

    def __init__(self):
        super(Watcher, self).__init__()
        self._folder_mgr_db = FolderManagerDB()
        self._img_ext_filter = ["*.jpg", "*.jpeg", "*.png"]

    @pyqtSlot()
    def watch_all(self):
        """
        <TODO>
        """
        self.scan_folders()
        self.watch_all_done.emit()

    def scan_folders(self):
        watched_folders = self._folder_mgr_db.get_watched_dirs()
        for idx, folder in enumerate(watched_folders):
            dpath = folder['abspath']
            dname = folder['name']
            sdid = self._folder_mgr_db.get_scan_dir(dpath)
            if not sdid:
                sdid = self._folder_mgr_db.add_scan_dir(dpath, dname)
            self.scan_folder(dpath, sdid)
        LOGGER.info("Folder scan completed.")

    def scan_folder(self, abspath, sdid):
        """
        <TODO>
        """
        dirIter = QDirIterator(abspath, self._img_ext_filter, QDir.AllEntries | QDir.NoDotAndDotDot,
                                   QDirIterator.FollowSymlinks)
        while dirIter.hasNext():
            dirIter.next()
            file_info = dirIter.fileInfo()
            if file_info.isDir():
                LOGGER.info("Found Directory: %s" % dirIter.filePath())
                #self.scan_folder(dirIter.filePath())
            else:
                LOGGER.info("Found image file: %s" % dirIter.filePath())
