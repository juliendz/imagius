"""
File/Folder Watcher module
author: Julien Dcruz
"""

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


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
        self.watch_all_done.emit()
