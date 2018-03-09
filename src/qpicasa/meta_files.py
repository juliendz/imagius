"""
Folder Manager module
"""
__license__ = 'MIT'
__copyright__ = '2017, Julien Dcurz <juliendcruz at gmail.com>'

import io
import os
from PIL import Image
from qpicasa.db import dbmgr


class MetaFilesManager():

    def __init__(self, dbpath="meta-files.db", dir_dbpath="app.db"):
        self._db = dbmgr(dbpath)
        self._dir_db = dbmgr(dir_dbpath)

    def connect(self):
        self._db.connect()

    def disconnect(self):
        self._db.disconnect()

    def commit(self):
        self._db.commit()

    def get_watched_dirs(self):
        query = "SELECT * FROM dir"
        self._dir_db.connect()
        res = self._dir_db.run_select_query(query)
        self._dir_db.disconnect()
        return res

    def get_scan_dirs(self):
        query = "SELECT * FROM scan_dir"
        self._db.connect()
        res = self._db.run_select_query(query)
        self._db.disconnect()
        return res

    def get_scan_dir(self, id):
        query = "SELECT * FROM scan_dir WHERE id = ?"
        params = (id,)
        self._db.connect()
        res = self._db.run_select_query(query, params)
        self._db.disconnect()
        if not res:
            return None
        return res[0]

    def get_scan_dir_id(self, abs_path):
        query = "SELECT * FROM scan_dir WHERE abspath = ?"
        params = (abs_path,)
        res = self._db.run_select_query(query, params)
        if not res:
            return None
        return res[0]

    def add_scan_dir(self, path, name):
        """
        <TODO>
        """
        query = "INSERT INTO scan_dir (abspath, name) VALUES (?, ?)"
        params = (path, name)
        sd_id = self._db.run_insert_query(query, params)
        return sd_id

    def remove_scan_dir(self, id):
        """
        <TODO>
        """
        query = "DELETE FROM scan_dir WHERE id = ?"
        params = (id,)
        return self._db.run_query(query, params)

    def update_scan_dir_mtime(self, sd_id, mtime):
        """
        <TODO>
        """
        query = "UPDATE scan_dir SET mtime = ? WHERE id = ?"
        params = (mtime, sd_id)
        sd_id = self._db.run_query(query, params)
        return sd_id

    def update_scan_dir_img_count(self, sd_id, count):
        """
        <TODO>
        """
        query = "UPDATE scan_dir SET img_count = ? WHERE id = ?"
        params = (count, sd_id)
        sd_id = self._db.run_query(query, params)
        return sd_id

    def add_image(self, sdid, abs_path, name, int_check):
        THUMB_SIZE = (128, 128)
        thumb_bytes = self._generate_thumb(abs_path, THUMB_SIZE)
        mtime = os.path.getmtime(abs_path)
        return self._add_image_db(sdid, abs_path, name, thumb_bytes, mtime, int_check)

    def update_image_thumb(self, si_id, abs_path, mtime, int_check):
        THUMB_SIZE = (128, 128)
        thumb_bytes = self._generate_thumb(abs_path, THUMB_SIZE)
        self._update_image_thumb_db(si_id, thumb_bytes, mtime, int_check)

    def update_image(self, si_id, int_check):
        self._update_image_db(si_id, int_check)

    def _generate_thumb(self, abspath, thumb_size):
        thumb_bytes = io.BytesIO()
        try:
            with Image.open(abspath) as image:
                image.thumbnail(thumb_size, Image.ANTIALIAS)
                image.save(thumb_bytes, image.format)
        except IOError as err:
            print(err)
        return thumb_bytes

    def _add_image_db(self, sdid, abspath, name, blob, mtime, int_check):
        query = "INSERT INTO scan_img (sdid, abspath, name, thumb, mtime, integrity_check) VALUES (?, ?, ?, ?, ?, ?)"
        params = (sdid, abspath, name, blob.getvalue(), mtime, int_check)
        si_id = self._db.run_insert_query(query, params)
        return si_id

    def _update_image_db(self, si_id, int_check):
        query = "UPDATE scan_img set integrity_check = ? WHERE id = ?"
        params = (int_check, si_id)
        self._db.run_query(query, params)

    def _update_image_thumb_db(self, si_id, blob, mtime, int_check):
        query = "UPDATE scan_img set thumb = ?, mtime = ?, integrity_check = ? WHERE id = ?"
        params = (blob.getvalue(), mtime, int_check, si_id)
        self._db.run_query(query, params)

    def get_image_id(self, abs_path):
        query = "SELECT id, mtime FROM scan_img WHERE abspath = ?"
        params = (abs_path,)
        res = self._db.run_select_query(query, params)
        if not res:
            return None
        return res[0]

    def get_scan_dir_images(self, sd_id):
        query = "SELECT * FROM scan_img WHERE sdid = ?"
        params = (sd_id,)
        self._db.connect()
        res = self._db.run_select_query(query, params)
        self._db.disconnect()
        return res

    def get_unclean_entries(self, int_check):
        query = "SELECT abspath FROM scan_img WHERE integrity_check < ?"
        params = (int_check,)
        res = self._db.run_select_query(query, params)
        return res

    def clean_db(self, int_check):
        query = "DELETE FROM scan_img WHERE integrity_check < ?"
        params = (int_check,)
        return self._db.run_query(query, params, True)

    def prune_scan_dir(self, sd_id, int_check):
        query = "DELETE FROM scan_img WHERE sdid = ? AND integrity_check < ?"
        params = (sd_id, int_check)
        return self._db.run_query(query, params, True)

    def get_scan_dir_img_count(self, sd_id):
        query = "select COUNT(id) AS 'img_count' from scan_img WHERE sdid = ?"
        params = (sd_id,)
        res = self._db.run_select_query(query, params)
        print(res)
        return res[0]['img_count']

