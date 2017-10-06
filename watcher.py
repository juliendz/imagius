"""
File/Folder Watcher module
author: Julien Dcruz
"""

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QDirIterator
import foldermanager
from log import LOGGER


class Watcher(QObject):
    """
    <TODO>
    """
    watch_all_done = pyqtSignal()

    @pyqtSlot()
    def watch_all(self):
        """
        <TODO>
        """
        self.scan_folders()
        self.watch_all_done.emit()
    
    def scan_folders(self):
        """
        <TODO>
        """
        watched_folders = foldermanager.get_watched_folders()
        for idx, folder in enumerate(watched_folders):
            fpath = folder['fullpath']
            dirIter = QDirIterator(fpath, QDirIterator.Subdirectories, QDirIterator.FollowSymlinks)
            while dirIter.hasNext():
                LOGGER.info(dirIter.next())
                
