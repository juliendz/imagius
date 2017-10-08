"""
Folder Manager module
"""
__license__ = 'MIT'
__copyright__ = '2017, Julien Dcurz <juliendcruz at gmail.com>'

import io, os
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

    def get_scan_dirs(self):
        query = "SELECT * FROM scan_dir"
        self._db.connect()
        res = self._db.run_select_query(query)
        self._db.disconnect()
        return res

    def get_scan_dir_id(self, abs_path):
        query = "SELECT id FROM scan_dir WHERE abspath = ?"
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

    def add_image(self, sdid, abs_path, name):
        THUMB_SIZE = (128, 128)
        thumb_bytes =  self._generate_thumb(abs_path, THUMB_SIZE)
        mtime = os.path.getmtime(abs_path)
        return self._add_image_db(sdid, abs_path, name, thumb_bytes, mtime)

    def update_image(self, si_id, abs_path, mtime):
        THUMB_SIZE = (128, 128)
        thumb_bytes =  self._generate_thumb(abs_path, THUMB_SIZE)
        self._update_image_db(si_id, thumb_bytes, mtime)

    def _generate_thumb(self, abspath, thumb_size):
        thumb_bytes = io.BytesIO()
        try:
            with Image.open(abspath) as image:
                image.thumbnail(thumb_size)
                image.save(thumb_bytes, image.format)
        except IOError as err:
            print(err)
        return thumb_bytes

    def _add_image_db(self, sdid, abspath, name, blob, mtime):
        query = "INSERT INTO scan_img (sdid, abspath, name, thumb, mtime) VALUES (?, ?, ?, ?, ?)"
        params = (sdid, abspath, name, blob.getvalue(), mtime)
        si_id = self._db.run_insert_query(query, params)
        return si_id

    def _update_image_db(self, si_id, blob, mtime):
        query = "UPDATE scan_img set thumb = ?, mtime = ? WHERE id = ?"
        params = (blob.getvalue(), mtime, si_id)
        self._db.run_query(query, params)

    def get_image_id(self, abs_path):
        query = "SELECT id, mtime FROM scan_img WHERE abspath = ?"
        params = (abs_path,)
        res = self._db.run_select_query(query, params)
        if not res:
            return None
        return res[0]

    def get_watched_dirs(self):
        query = "SELECT * FROM dir"
        self._dir_db.connect()
        res = self._dir_db.run_select_query(query)
        self._dir_db.disconnect()
        return res