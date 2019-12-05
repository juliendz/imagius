# -*- coding: utf-8 -*-

"""
Application Version Upgrade module
author: Julien Dcruz
"""
from packaging.version import Version
from imagius.log import LOGGER
from imagius.db import dbmgr


def upgrade_from_previous_versions(cur_version, meta_db_path):
    meta_db = dbmgr(meta_db_path)
    meta_db.connect()
    # Upgrade code to Version(0.8.1)
    if cur_version < Version('0.8.1'):
        LOGGER.info('Upgrading from Version:%s to Version:%s' %
                    (cur_version, '0.8.1'))

        queries = [
            'CREATE TEMPORARY TABLE scan_img_backup(a,b,c,d,e,f,g,h);',
            """INSERT INTO scan_img_backup
               SELECT id, abspath, name, thumb, sdid, mtime, integrity_check, serial FROM scan_img;
            """,
            'DROP TABLE scan_img;',
            """CREATE TABLE IF NOT EXISTS "scan_img" (
                `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                `abspath` TEXT NOT NULL UNIQUE,
                `name` TEXT NOT NULL,
                `thumb` BLOB NOT NULL,
                `sdid` INTEGER NOT NULL DEFAULT 0,
                `mtime` INTEGER,
                `integrity_check` INTEGER,
                `serial` INTEGER,
                FOREIGN KEY(`sdid`) REFERENCES `scan_dir`(`id`) ON DELETE CASCADE )
            """,
            'INSERT INTO scan_img SELECT a,b,c,d,e,f,g,h FROM scan_img_backup;',
            'DROP TABLE scan_img_backup;',
        ]

        for query in queries:
            meta_db.run_query(query)
        meta_db.commit()

        cur_version = Version('0.8.1')

    meta_db.disconnect()
    return
