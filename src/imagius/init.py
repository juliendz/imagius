# -*- coding: utf-8 -*-
__license__ = 'GPL v3'
__copyright__ = '2019, Julien Dcruz juliendcruz@gmail.com'
__docformat__ = 'restructuredtext en'

"""
Application Data Initialization 
"""
from PySide2 import QtCore
from constants import USER_APPDATA_DIR, APP_NAME, DB_SETTINGS, DB_META, APP_VERSION
from exceptions import AppDataDirReadWriteFailed


def init_app_data_dir():
    data_dir_path = '%s/%s' % (USER_APPDATA_DIR, APP_NAME)
    dir = QtCore.QDir(data_dir_path)
    if not dir.exists(data_dir_path):
        roaming_dir = QtCore.QDir(USER_APPDATA_DIR)
        if not roaming_dir.mkdir(APP_NAME):
            LOGGER.critical(
                'Unable to access or create application data location: %s' % data_dir_path)
            raise AppDataDirReadWriteFailed


def init_app_db():
    from db import dbmgr
    settings_db_file = QtCore.QFileInfo(
        "%s/%s/%s" % (USER_APPDATA_DIR, APP_NAME, DB_SETTINGS))
    if not settings_db_file.exists():
        db = dbmgr(settings_db_file.absoluteFilePath())
        db.create_settings_db_from_schema()

        # Add the current version info
        db = dbmgr(settings_db_file.absoluteFilePath())
        db.connect()
        query = 'INSERT INTO settings (key, value) VALUES (?, ?)'
        params = ('VERSION', APP_VERSION)
        db.run_insert_query(query, params)
        db.disconnect()

    meta_db_file = QtCore.QFileInfo(
        "%s/%s/%s" % (USER_APPDATA_DIR, APP_NAME, DB_META))
    if not meta_db_file.exists():
        db = dbmgr(meta_db_file.absoluteFilePath())
        db.create_meta_db_from_schema()
