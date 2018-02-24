"""
Scanned Directory Loader module
author: Julien Dcruz
"""

import os
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QDirIterator, qDebug
from PyQt5.QtCore import QDir
from PyQt5.QtGui import QImage
from .log import LOGGER
from .meta_files import MetaFilesManager



class ScanDirLoader(QObject):
    """
    <TODO>
    """
    dir_info_load = pyqtSignal(object)
    dir_images_load_ended = pyqtSignal()
    dir_image_load_success = pyqtSignal(object)

    def __init__(self):
        super(ScanDirLoader, self).__init__()

        self._meta_files_mgr = MetaFilesManager()

    @pyqtSlot(object)
    def load_scan_dir_images(self, sd_id):
        LOGGER.debug('Image loading starting.')
        dir_info = self._meta_files_mgr.get_scan_dir(sd_id)
        self.dir_info_load.emit(dir_info)
        images = self._meta_files_mgr.get_scan_dir_images(sd_id)
        for img in images:
            img['thumb'] = QImage.fromData(img['thumb'])
            self.dir_image_load_success.emit(img)
        self.dir_images_load_ended.emit()
