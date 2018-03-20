# -*- coding: utf-8 -*-

"""
application settings module
author: Julien Dcruz
"""

from PyQt5 import QtCore
from imagius.db import dbmgr
from imagius.types import SettingType, IMAGE_FILETYPES

app_name = 'imagius'
settings_db_name = 'settings.db'
meta_db_name = 'meta.db'
roaming_dir_path = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.AppDataLocation)
SETTINGS = {}


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


def load_settings():
    settings_db_file = QtCore.QFileInfo("%s/%s/%s" % (roaming_dir_path, app_name, settings_db_name))
    db = dbmgr(settings_db_file.absoluteFilePath())
    db.connect()
    query = 'SELECT * FROM settings'
    dr = db.run_select_query(query)
    db.disconnect()

    for row in dr:
        SETTINGS[row['key']] = row['value']
    
    print(SETTINGS)


def get(setting_type, default='', type='str'):
    if setting_type.name in SETTINGS:
        if type == 'bool' and (SETTINGS[setting_type.name] == '1' or SETTINGS[setting_type.name] is True):
            SETTINGS[setting_type.name] = True
        else:
            SETTINGS[setting_type.name] = False
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
    settings_db_file = QtCore.QFileInfo("%s/%s/%s" % (roaming_dir_path, app_name, settings_db_name))
    db = dbmgr(settings_db_file.absoluteFilePath())
    db.connect()

    select_query = 'SELECT key FROM settings WHERE key = ?'
    update_query = 'UPDATE settings set value = ? WHERE key = ?'
    insert_query = 'INSERT INTO settings (key, value) VALUES (?, ?)'
    # print(SETTINGS)
    for key, value in SETTINGS.items():
        res = db.run_select_query(select_query, (key,))
        if len(res) > 0:
            db.run_query(update_query, (key, value))
        else:
            db.run_insert_query(insert_query, (key, value))

    db.disconnect()
