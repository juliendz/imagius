"""
Folder Manager Window module
author: Julien Dcruz
last edited: 8th April 2017
"""

import sys
import os
from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtWidgets import QDialog, QFileDialog, QMessageBox
from PySide2 import QtCore
from PySide2.QtCore import QDir, QStandardPaths
from imagius.folder_manager import FolderManager
from imagius.ui.ui_settingswindow import Ui_SettingsWindow
from imagius.log import LOGGER
from imagius import settings


class SettingsWindow(QDialog, Ui_SettingsWindow):
    def __init__(self, parent=None):
        super(SettingsWindow, self).__init__(parent)
        self.setupUi(self)

        self.chkbox_updates_on_startup.setChecked(settings.get(
            settings.SettingType.CHECK_UPDATE_ON_STARTUP, False, 'bool'))

        self.chkbox_formats_bmp.setChecked(settings.get(
            settings.SettingType.FILETYPE_BMP, False, 'bool'))
        self.chkbox_formats_png.setChecked(settings.get(
            settings.SettingType.FILETYPE_PNG, False, 'bool'))

        self.chkbox_loop_slideshow.setChecked(settings.get(
            settings.SettingType.SLIDESHOW_LOOP, False, 'bool'))

        self.btnBox_AcceptCancel.accepted.connect(self.settings_accepted)

    def settings_accepted(self):

        settings.save(settings.SettingType.CHECK_UPDATE_ON_STARTUP,
                      self.chkbox_updates_on_startup.isChecked())

        settings.save(settings.SettingType.FILETYPE_BMP,
                      self.chkbox_formats_bmp.isChecked())
        settings.save(settings.SettingType.FILETYPE_PNG,
                      self.chkbox_formats_png.isChecked())

        settings.save(settings.SettingType.SLIDESHOW_LOOP,
                      self.chkbox_loop_slideshow.isChecked())

        print(settings.SETTINGS)

        settings.persist_to_disk()

    def closeWindow(self):
        self.close()
