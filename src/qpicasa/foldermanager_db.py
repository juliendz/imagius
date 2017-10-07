#!/usr/bin/env python3

"""
Folder Manager module
author: Julien Dcruz
"""
from .db import dbmgr


class FolderManagerDB():

    def __init__(self):
        self._db = dbmgr("app.db")

    def get_watched_dirs(self):
        query = "SELECT * FROM dir"
        self._db.connect()
        res = self._db.run_select_query(query)
        self._db.disconnect()
        return res

    def add_watched_folder(self, folder_path, folder_name):
        query = "INSERT INTO dir (abspath, name) VALUES (?, ?)"
        params = (folder_path, folder_name)
        self._db.connect()
        fid = self._db.run_insert_query(query, params)
        self._db.disconnect()
        return fid

    def edit_watched_folder(self, fid, new_folder_path, new_folder_name):
        query = "UPDATE dir SET abspath = ?, name = ?  WHERE id = ?"
        params = (new_folder_path, new_folder_name, fid)
        self._db.connect()
        self._db.run_query(query, params)
        self._db.disconnect()

    def delete_watched_folder(self, fid):
        query = "DELETE FROM dir WHERE id = ?"
        params = (fid,)
        self._db.connect()
        self._db.run_query(query, params)
        self._db.disconnect()

    def get_scan_dir(self, abspath):
        query = "SELECT id FROM scan_dir WHERE abspath = ?"
        params = (abspath,)
        self._db.connect()
        res = self._db.run_select_query(query, params)
        self._db.disconnect()
        return res

    def add_scan_dir(self, path, name):
        """
        <TODO>
        """
        query = "INSERT INTO scan_dir (abspath, name) VALUES (?, ?)"
        params = (path, name)
        self._db.connect()
        sdid = self._db.run_insert_query(query, params)
        self._db.disconnect()
        return sdid

    def add_scan_img(self, sdid):
        """
            sdid: Scanned folder id
        """
        query = "INSERT INTO scan_img (abspath, name, thumb) VALUES (?, ?)"

        params = (path, name)
        self._db.connect()
        sdid = self._db.run_insert_query(query, params)
        self._db.disconnect()
        return sdid


