"""
File/Folder Watcher module
author: Julien Dcruz
"""

import os
import time
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QDirIterator, qDebug
from PyQt5.QtCore import QDir
from .log import LOGGER
from .meta_files import MetaFilesManager


class Watcher(QObject):
    """
    <TODO>
    """
    watch_all_done = pyqtSignal()
    new_image_found = pyqtSignal(object)

    def __init__(self):
        super(Watcher, self).__init__()

        self._meta_files_mgr = MetaFilesManager()

        self._img_ext_filter = ["*.jpg", "*.jpeg", "*.png"]

    @pyqtSlot()
    def watch_all(self):
        """
        <TODO>
        """
        self.scan_folders()
        self.watch_all_done.emit()

    def scan_folders(self):
        watched_folders = self._meta_files_mgr.get_watched_dirs()

        self._img_integrity_ts = time.time()

        self._meta_files_mgr.connect()

        #Scan the watched directories.
        for idx, folder in enumerate(watched_folders):
            self.scan_folder(folder['abspath'], folder['name'])

        #TODO: Emit list of unclean entries for notification
        # self._meta_files_mgr.get_unclean_entries

        #Finally, remove the non-existent files
        self._meta_files_mgr.clean_db(self._img_integrity_ts)

        self._meta_files_mgr.disconnect()

        LOGGER.debug("Folder scan completed.")

    def scan_folder(self, abs_path, dir_name):
        """
        <TODO>
        """
        sd_id = 0
        sd_info = self._meta_files_mgr.get_scan_dir_id(abs_path)
        if not sd_info or sd_info['id'] <= 0:
            sd_id = self._meta_files_mgr.add_scan_dir(abs_path, dir_name)
        else:
            sd_id = sd_info['id']

        dir_iter = QDirIterator(abs_path, self._img_ext_filter,
                                QDir.AllEntries | QDir.AllDirs | QDir.NoDotAndDotDot,
                                QDirIterator.FollowSymlinks)
        while dir_iter.hasNext():
            dir_iter.next()
            file_info = dir_iter.fileInfo()
            if file_info.isDir():
                LOGGER.debug("Found Directory: %s" %
                             file_info.absoluteFilePath())
                self.scan_folder(file_info.absoluteFilePath(),
                                 file_info.fileName())
            else:
                LOGGER.debug("Found Image: %s" % file_info.absoluteFilePath())

                si_info = self._meta_files_mgr.get_image_id(
                    file_info.absoluteFilePath())

                #file exists
                if si_info and si_info['id'] > 0:
                    latest_mtime = os.path.getmtime(
                        file_info.absoluteFilePath())
                    if latest_mtime > si_info['mtime']:
                        self._meta_files_mgr.update_image_thumb(si_info['id'],
                                                                file_info.absoluteFilePath(),
                                                                latest_mtime,
                                                                self._img_integrity_ts)
                    else:
                        self._meta_files_mgr.update_image(si_info['id'],
                                                          self._img_integrity_ts)

                #new file to add
                elif not si_info:
                    LOGGER.debug("Found New image: %s" % file_info.absoluteFilePath())
                    self._meta_files_mgr.add_image(sd_id,
                                                   file_info.absoluteFilePath(),
                                                   file_info.fileName(),
                                                   self._img_integrity_ts)
