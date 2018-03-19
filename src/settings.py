# -*- coding: utf-8 -*-

"""
application settings module
author: Julien Dcruz
"""

from PyQt5 import QtCore
from imagius.db import dbmgr

app_name = 'imagius'
settings_db_name = 'settings.db'
meta_db_name = 'meta.db'
roaming_dir_path = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.AppDataLocation)


def init_app_data():
    data_dir_path = '%s/%s' % (roaming_dir_path, app_name)
    dir = QtCore.QDir(data_dir_path)
    if not dir.exists(data_dir_path):
        roaming_dir = QtCore.QDir(roaming_dir_path)
        if not roaming_dir.mkdir(app_name):
            LOGGER.critical('Unable to access or create application data location: %s' % data_dir_path)

    settings_db_file = QtCore.QFileInfo("%s/%s/%s" % (roaming_dir_path, app_name, settings_db_name))
    if not settings_db_file.exists():
        db = dbmgr(settings_db_file.absoluteFilePath())
        db.create_settings_db_from_schema()

    meta_db_file = QtCore.QFileInfo("%s/%s/%s" % (roaming_dir_path, app_name, meta_db_name))
    if not meta_db_file.exists():
        db = dbmgr(meta_db_file.absoluteFilePath())
        db.create_meta_db_from_schema()


def get_settings_db_path():
    settings_db_file = QtCore.QFileInfo("%s/%s/%s" % (roaming_dir_path, app_name, settings_db_name))
    return settings_db_file.absoluteFilePath()


def get_meta_db_path():
    meta_db_file = QtCore.QFileInfo("%s/%s/%s" % (roaming_dir_path, app_name, meta_db_name))
    return meta_db_file.absoluteFilePath()
