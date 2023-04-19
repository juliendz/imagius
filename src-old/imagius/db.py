"""
Description: Database Manager
Created : 08/04/2017
Modified : 08/04/2017
Started by: Julien Dcruz
Contributors: ...
"""


import sqlite3
from .log import LOGGER


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class dbmgr(object):
    errcode = None
    dbpath = None
    conn = None
    is_open = False

    schema_settings = """
        PRAGMA journal_mode=WAL;
        CREATE TABLE IF NOT EXISTS "dir" (
                    "id" INTEGER PRIMARY KEY ,
                    "abspath" TEXT NOT NULL  DEFAULT (null) ,
                    "name" TEXT NOT NULL ,
                    "image_count" INTEGER DEFAULT (0)
        );
        CREATE TABLE `settings` ( 
                    `key` TEXT UNIQUE,
                    `value` TEXT 
        );
    """

    schema_meta = """
        PRAGMA journal_mode=WAL;
        CREATE TABLE IF NOT EXISTS "scan_dir" (
        `id`    INTEGER NOT NULL,
        `parent_dir_id` INTEGER,
        `abspath`       TEXT NOT NULL DEFAULT (null),
        `name`  TEXT NOT NULL,
        `img_count`     INTEGER,
        `mtime` INTEGER,
        `integrity_check`       INTEGER,
        PRIMARY KEY(`id`)
        );
        CREATE TABLE IF NOT EXISTS "scan_img" (
        `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
        `abspath` TEXT NOT NULL UNIQUE, 
        `name` TEXT NOT NULL, 
        `thumb` BLOB NOT NULL, 
        `sdid` INTEGER NOT NULL DEFAULT 0, 
        `mtime` INTEGER, 
        `integrity_check` INTEGER, 
        `serial` INTEGER, 
        FOREIGN KEY(`sdid`) REFERENCES `scan_dir`(`id`) ON DELETE CASCADE )
    """

    def __init__(self, db_path):
        self.dbpath = db_path

    def create_settings_db_from_schema(self):
        try:
            self.connect()
            self.conn.cursor().executescript(self.schema_settings)
            self.disconnect()
        except sqlite3.OperationalError as msg:
            LOGGER.critical('[Error while creating settings db]: %s' % msg)

    def create_meta_db_from_schema(self):
        try:
            self.connect()
            self.conn.cursor().executescript(self.schema_meta)
            self.disconnect()
        except sqlite3.OperationalError as msg:
            LOGGER.critical('[Error while creating meta db ]: %s' % msg)

    def connect(self):
        if not self.is_open:
            self.conn = sqlite3.connect(self.dbpath)
            self.conn.execute("PRAGMA foreign_keys = 1")
            self.is_open = True

    def disconnect(self):
        self.conn.close()
        self.is_open = False

    def commit(self):
        self.conn.commit()

    def run_insert_query(self, query, params, commit=True):
        """
            Description: Executes an insert sql query using Pythons DB-API (Parameter substitution)
            Arguments: 'query': The sql query string
                       'params' : tuple containing parameters
            """
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, params)
            if commit:
                self.conn.commit()
        except sqlite3.OperationalError as msg:
            LOGGER.error('[DB]: %s' % msg)
        except sqlite3.IntegrityError as msg:
            LOGGER.debug('[DB]: %s : %s : %s' % (msg, query, params))
            LOGGER.error('[DB]: %s : %s' % (msg, params))
        return cursor.lastrowid

    def run_query(self, query, params=(), commit=True):
        """
        Description: Executes an update/delete sql query using Pythons DB-API (Parameter substitution)
            Arguments: query: The sql query string
                       'params' : tuple containing parameters
        """
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, params)
            if commit:
                self.conn.commit()
        except sqlite3.OperationalError as msg:
            LOGGER.error('[DB]: %s' % msg)
        except sqlite3.IntegrityError as msg:
            LOGGER.debug('[DB]: %s : %s : %s' % (msg, query, params))
            LOGGER.error('[DB]: %s : %s' % (msg, params))

        return cursor.rowcount

    def run_select_query(self, query, params=()):
        """
            Description: Executes an select sql query using Pythons DB-API (Parameter substitution)
            Arguments: 'query: The sql query string
                       'params' : tuple containing parameters
            # Returns: False on failure | list[row_number][column_name] on success
        """
        self.conn.row_factory = dict_factory

        cursor = self.conn.cursor()
        try:
            cursor.execute(query, params)
        except sqlite3.OperationalError as msg:
            LOGGER.error('[DB]: %s' % msg)

        data = cursor.fetchall()
        return data
