"""
Image/Properties Loader module
author: Julien Dcruz
"""

import os
import time
from PySide2.QtCore import QObject, Signal, Slot, QDirIterator
from PySide2.QtCore import QDir, QFileInfo, qDebug

from imagius import settings
from imagius.log import LOGGER
from imagius.meta_files import MetaFilesManager
from imagius.imagius_types import SettingType, IMAGE_FILETYPES


class ImageLoader(QObject):
    """
    <TODO>
    """
    load_scandir_success = Signal(object, object)
    load_scan_dir_info_success = Signal(object)
    load_images_success = Signal(object)

    batch_size = 50

    def __init__(self):
        super(ImageLoader, self).__init__()

        self._meta_files_mgr = MetaFilesManager()
        self._img_ext_filter = settings.get_allowed_image_formats()

    @Slot(object)
    def load_scandir(self, sd_id):
        """
        <TODO>
        """
        self._img_integrity_ts = start_time = time.time()
        self._meta_files_mgr.connect()

        LOGGER.debug('Load Scan Dir started.')

        dir_info = self._meta_files_mgr.get_scan_dir(sd_id)
        self.load_scan_dir_info_success.emit(dir_info)

        images = self._meta_files_mgr.get_scan_dir_images(sd_id)

        total_img_count = len(images)
        if total_img_count < self.batch_size:
            self.load_images_success.emit(images)
        else:
            batch_start_index = 0
            curr_img_count = 0
            for img in images:
                print(batch_start_index)
                curr_img_count += 1
                if curr_img_count % 50 == 0 or curr_img_count == total_img_count:
                    self.load_images_success.emit(
                        images[batch_start_index:curr_img_count])
                    batch_start_index = curr_img_count

        elapsed = round(time.time() - start_time, 2)
        suffix = 'seconds'
        if elapsed > 60:
            elapsed /= 60
            suffix = 'minutes'
        LOGGER.debug('Loading Scan Dir completed in %.2f %s.' %
                     (elapsed, suffix))

        self.load_scandir_success.emit(elapsed, suffix)

    @Slot()
    def free_resources(self):
        self._meta_files_mgr.disconnect()
