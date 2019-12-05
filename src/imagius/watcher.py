"""
File/Folder Watcher module
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


class Watcher(QObject):
    """
    <TODO>
    """
    watch_all_done = Signal(object, object)
    new_img_found = Signal(object)
    dir_added_or_updated = Signal(object)
    dir_empty_or_deleted = Signal(object)
    watch_empty_or_deleted_done = Signal()

    def __init__(self):
        super(Watcher, self).__init__()

        self._meta_files_mgr = MetaFilesManager()

        self._img_ext_filter = settings.get_allowed_image_formats()

        print(self._img_ext_filter)

    @Slot()
    def watch_all(self):
        """
        <TODO>
        """
        self._img_integrity_ts = start_time = time.time()

        LOGGER.info('Watch all started.')

        self._meta_files_mgr.connect()

        self.scan_folders()

        elapsed = round(time.time() - start_time, 2)
        suffix = 'seconds'
        if elapsed > 60:
            elapsed /= 60
            suffix = 'minutes'
        LOGGER.info('Watch all completed in %.2f %s.' % (elapsed, suffix))

        self.watch_all_done.emit(elapsed, suffix)

        orphaned_scan_dirs = self._meta_files_mgr.get_orphaned_scan_dirs(
            self._img_integrity_ts)
        for dir in orphaned_scan_dirs:
            self.dir_empty_or_deleted.emit({'id': dir['id']})
            self._meta_files_mgr.prune_scan_dir(dir['id'])
        self.watch_empty_or_deleted_done.emit()

        self._meta_files_mgr.disconnect()

    def scan_folders(self):
        watched_folders = self._meta_files_mgr.get_watched_dirs()

        # Scan the watched directories.
        for idx, folder in enumerate(watched_folders):
            self.scan_folder(folder['id'], folder['abspath'], folder['name'])

        # TODO: Emit list of unclean entries for notification
        # self._meta_files_mgr.get_unclean_entries

        # Finally, remove the non-existent files
        # self._meta_files_mgr.clean_db(self._img_integrity_ts)

        LOGGER.debug("Folder scan completed.")

    def scan_folder(self, parent_id, abs_path, dir_name):
        """
        <TODO>
        """
        is_new_or_modified = False
        if not os.path.isdir(abs_path):
            return
        modified_time = os.path.getmtime(abs_path)
        sd_id = 0
        sd_info = self._meta_files_mgr.get_scan_dir_id(abs_path)
        if not sd_info or sd_info['id'] <= 0:
            sd_id = self._meta_files_mgr.add_scan_dir(
                parent_id, abs_path, dir_name, self._img_integrity_ts)
            sd_info = self._meta_files_mgr.get_scan_dir_id(abs_path)
            is_new_or_modified = True
        else:
            sd_id = sd_info['id']
            self._meta_files_mgr.update_scan_dir_integrity_check(
                sd_id, self._img_integrity_ts)
            if not sd_info['mtime'] or (modified_time > sd_info['mtime']):
                LOGGER.debug("Folder(%s):(%s) has changed since last scan." %
                             (sd_id, sd_info['abspath']))
                is_new_or_modified = True

        if is_new_or_modified is True:
            dir_iter = QDirIterator(abs_path, self._img_ext_filter,
                                    QDir.AllEntries |
                                    QDir.AllDirs |
                                    QDir.NoDotAndDotDot,
                                    QDirIterator.FollowSymlinks)
        else:
            dir_iter = QDirIterator(abs_path,
                                    QDir.AllDirs |
                                    QDir.NoDotAndDotDot,
                                    QDirIterator.FollowSymlinks)
        has_new_images = False
        img_serial = self._meta_files_mgr.get_scan_dir_img_next_serial(sd_id)
        while dir_iter.hasNext():
            dir_iter.next()
            file_info = dir_iter.fileInfo()

            if file_info.isDir():
                LOGGER.debug("Found Directory: %s" %
                             file_info.absoluteFilePath())
                self.scan_folder(parent_id, file_info.absoluteFilePath(),
                                 file_info.fileName())
            else:

                si_info = self._meta_files_mgr.get_image_id(
                    file_info.absoluteFilePath())

                # file exists
                if si_info and si_info['id'] > 0:
                    LOGGER.debug("Found Image: %s" %
                                 file_info.absoluteFilePath())
                    latest_mtime = os.path.getmtime(
                        file_info.absoluteFilePath())
                    if latest_mtime > si_info['mtime']:
                        self._meta_files_mgr.update_image_thumb(
                            si_info['id'],
                            file_info.absoluteFilePath(),
                            latest_mtime,
                            self._img_integrity_ts)
                    else:
                        self._meta_files_mgr.update_image(
                            si_info['id'],
                            self._img_integrity_ts)

                # new file to add
                elif not si_info:
                    LOGGER.debug("Found New image: %s" %
                                 file_info.absoluteFilePath())
                    self.new_img_found.emit(
                        {'dir': dir_name, 'filename': file_info.fileName()})
                    self._meta_files_mgr.add_image(
                        sd_id,
                        file_info.absoluteFilePath(),
                        file_info.fileName(),
                        self._img_integrity_ts,
                        img_serial)
                    has_new_images = True
                    img_serial = img_serial + 1

        self._meta_files_mgr.commit()

        if is_new_or_modified is True:
            img_del_count = self._meta_files_mgr.prune_scan_img(
                sd_id, self._img_integrity_ts)
            img_count = self._meta_files_mgr.get_scan_dir_img_count(sd_id)
            self._meta_files_mgr.update_scan_dir_img_count(sd_id, img_count)
            if has_new_images or img_del_count > 0:
                self.dir_added_or_updated.emit(
                    {'id': sd_id, 'name': dir_name, 'img_count': img_count})
            # Only update `mtime` if the scan_dir is new or modified
            if img_count > 0:
                self._meta_files_mgr.update_scan_dir_mtime(
                    sd_id, modified_time)
            else:
                self._meta_files_mgr.remove_scan_dir(sd_id)
                self.dir_empty_or_deleted.emit({'id': sd_id})
