# -*- coding: utf-8 -*-
__license__ = 'GPL v3'
__copyright__ = '2019, Julien Dcruz juliendcruz@gmail.com'
__docformat__ = 'restructuredtext en'

"""
application settings module
author: Julien Dcruz
"""

from PySide2 import QtCore
from db import dbmgr
from imagius_types import SettingType, IMAGE_FILETYPES
from packaging.version import Version
from upgrade import upgrade_from_previous_versions
from constants import USER_APPDATA_DIR, APP_NAME, DB_SETTINGS, DB_META, APP_VERSION

SETTINGS = {}


def get_settings_db_path():
    settings_db_file = QtCore.QFileInfo(
        "%s/%s/%s" % (USER_APPDATA_DIR, APP_NAME, DB_SETTINGS))
    return settings_db_file.absoluteFilePath()


def get_meta_db_path():
    meta_db_file = QtCore.QFileInfo(
        "%s/%s/%s" % (USER_APPDATA_DIR, APP_NAME, DB_META))
    return meta_db_file.absoluteFilePath()


def load_settings():
    settings_db_file = QtCore.QFileInfo(
        "%s/%s/%s" % (USER_APPDATA_DIR, APP_NAME, DB_SETTINGS))
    db = dbmgr(settings_db_file.absoluteFilePath())
    db.connect()
    query = 'SELECT * FROM settings'
    dr = db.run_select_query(query)
    db.disconnect()

    for row in dr:
        SETTINGS[row['key']] = row['value']

    # If the version in the db is lesser than the in-code version,
    # that means a new version was installed.
    # So run any version specific upgrade code
    if Version(SETTINGS['VERSION']) < Version(APP_VERSION):
        upgrade_from_previous_versions(
            Version(SETTINGS['VERSION']), get_meta_db_path())
    SETTINGS['VERSION'] = APP_VERSION


def get(setting_type, default='', type='str'):
    if setting_type.name in SETTINGS:
        if type == 'bool':
            if SETTINGS[setting_type.name] == '1' or SETTINGS[setting_type.name] is True:
                SETTINGS[setting_type.name] = True
            else:
                SETTINGS[setting_type.name] = False
        if type == 'int':
            SETTINGS[setting_type.name] = int(SETTINGS[setting_type.name])
        return SETTINGS[setting_type.name]
    return default


def save(setting_type, value):
    SETTINGS[setting_type.name] = value


def get_allowed_image_formats():
    filetype_bmp = get(SettingType.FILETYPE_BMP, False, 'bool')
    filetype_png = get(SettingType.FILETYPE_PNG, False, 'bool')
    img_ext_filter = IMAGE_FILETYPES['jpg']
    if filetype_bmp:
        img_ext_filter += IMAGE_FILETYPES['bmp']
    if filetype_png:
        img_ext_filter += IMAGE_FILETYPES['png']
    return img_ext_filter


def persist_to_disk():
    settings_db_file = QtCore.QFileInfo(
        "%s/%s/%s" % (USER_APPDATA_DIR, APP_NAME, DB_SETTINGS))
    db = dbmgr(settings_db_file.absoluteFilePath())
    db.connect()
    print(SETTINGS)

    select_query = 'SELECT key FROM settings WHERE key = ?'
    update_query = 'UPDATE settings set value = ? WHERE key = ?'
    insert_query = 'INSERT INTO settings (key, value) VALUES (?, ?)'
    for key, value in SETTINGS.items():
        res = db.run_select_query(select_query, (key,))
        if len(res) > 0:
            db.run_query(update_query, (value, key))
        else:
            db.run_insert_query(insert_query, (key, value))

    db.disconnect()
