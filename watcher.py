"""
File/Folder Watcher module
author: Julien Dcruz
"""

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QDirIterator, qDebug
from PyQt5.QtCore import QDir
import foldermanager
from log import LOGGER


class Watcher(QObject):
    """
    <TODO>
    """
    watch_all_done = pyqtSignal()

    def __init__(self, folder_mgr):
        super(Watcher, self).__init__()
        self.folder_mgr = folder_mgr

    @pyqtSlot()
    def watch_all(self):
        """
        <TODO>
        """
        self.scan_folders()
        self.watch_all_done.emit()

    def scan_folders(self):
        watched_folders = self.folder_mgr.get_watched_folders()
        for idx, folder in enumerate(watched_folders):
            fpath = folder['fullpath']
            #Add folder to db and pass id to scan_folder
            self.scan_folder(fpath)
        LOGGER.info("Folder scan completed.")

    def scan_folder(self, fpath):
        """
        <TODO>
        """
        dirIter = QDirIterator(fpath, QDir.AllEntries | QDir.NoDotAndDotDot,
                                   QDirIterator.FollowSymlinks)
        while dirIter.hasNext():
            dirIter.next()
            file_info = dirIter.fileInfo()
            if file_info.isDir():
                LOGGER.info("Found Directory: %s" % dirIter.filePath())
                self.scan_folder(dirIter.filePath())
            else:
                LOGGER.info("Found image file: %s" % dirIter.filePath())
