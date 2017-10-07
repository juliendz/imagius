"""
Folder Manager module
"""
__license__ = 'MIT'
__copyright__ = '2017, Julien Dcurz <juliendcruz at gmail.com>'

import io
from PIL import Image
from qpicasa.db import dbmgr


class ImageManager():

    def __init__(self, dbpath):
        self._db = dbmgr(dbpath)

    def add_image(self, sdid, abspath, name):
        THUMB_SIZE = (128, 128)
        thumb_bytes =  self._generate_thumb(abspath, THUMB_SIZE)
        return self._add_image_db(sdid, abspath, name, thumb_bytes)

    def _generate_thumb(self, abspath, thumb_size):
        thumb_bytes = io.BytesIO()
        try:
            with Image.open(abspath) as image:
                image.thumbnail(thumb_size)
                image.save(thumb_bytes, image.format)
        except IOError as err:
            print(err)
        return thumb_bytes

    def _add_image_db(self, sdid, abspath, name, blob):
        query = "INSERT INTO scan_img (sdid, abspath, name, thumb) VALUES (?, ?, ?, ?)"
        params = (sdid, abspath, name, blob.getvalue())
        self._db.connect()
        si_id = self._db.run_insert_query(query, params)
        self._db.disconnect()
        return si_id
