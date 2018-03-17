"""
Folder Manager module
"""
__license__ = 'MIT'
__copyright__ = '2017, Julien Dcurz <juliendcruz at gmail.com>'

import io
import os
from PyQt5 import QtCore
from PIL import Image
import PIL.ExifTags
from iptcinfo import IPTCInfo
from qpicasa.db import dbmgr
from .log import LOGGER
import exifread


class MetaFilesManager():
    _thumb_size = (256, 256)

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

    def add_image(self, sdid, abs_path, name, int_check, serial):
        thumb_bytes = self._generate_thumb(abs_path, self._thumb_size)
        mtime = os.path.getmtime(abs_path)
        return self._add_image_db(sdid, abs_path, name, thumb_bytes, mtime, int_check, serial)

    def update_image_thumb(self, si_id, abs_path, mtime, int_check):
        thumb_bytes = self._generate_thumb(abs_path, self._thumb_size)
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

    def get_img_exif(self, abspath):
        exif = {}
        try:
            with PIL.Image.open(abspath) as image:
                exif = {
                    PIL.ExifTags.TAGS[k]: v
                    for k, v in image._getexif().items()
                    if k in PIL.ExifTags.TAGS
                }
        except Exception as ex:
            LOGGER.debug("EXIF data for %s could not be loaded." % abspath)
        return exif

    def get_img_properties(self, si_id, sd_id):
        self.connect()
        dr_img = self.get_image_from_id(si_id, sd_id)
        exif = self.get_img_exif(dr_img['abspath'])
        # print(exif)
        self.disconnect()

        properties = {}
        properties['abspath'] = dr_img['abspath']
        properties['filename'] = dr_img['name']
        properties['filesize'] = self.format_size(QtCore.QFileInfo(dr_img['abspath']).size())
        properties['dimensions'] = ''
        if exif:
            if 'DateTime' in exif:
                properties['DateTime'] = exif['DateTime']
            if 'DateTimeDigitized' in exif:
                properties['DateTimeDigitized'] = exif['DateTimeDigitized']
            if 'ImageWidth' in exif:
                properties['ImageWidth'] = exif['ImageWidth']
            if 'ImageLength' in exif:
                properties['ImageLength'] = exif['ImageLength']
            if 'ExifImageWidth' in exif:
                properties['ExifImageWidth'] = exif['ExifImageWidth']
            if 'ExifImageHeight' in exif:
                properties['ExifImageHeight'] = exif['ExifImageHeight']
            if 'Orientation' in exif:
                properties['Orientation'] = exif['Orientation']
            if 'XPKeywords' in exif:
                properties['XPKeywords'] = exif['XPKeywords'].decode("utf-16")
            if 'ImageUniqueID' in exif:
                properties['ImageUniqueID'] = exif['ImageUniqueID']
            if 'ColorSpace' in exif:
                properties['ColorSpace'] = exif['ColorSpace']
            if 'BitsPerSample' in exif:
                properties['BitsPerSample'] = exif['BitsPerSample']
            if 'PhotometricInterpretation' in exif:
                properties['PhotometricInterpretation'] = exif['PhotometricInterpretation']
            if 'ResolutionUnit' in exif:
                properties['ResolutionUnit'] = exif['ResolutionUnit']
            if 'Software' in exif:
                properties['Software'] = exif['Software']
            if 'SamplesPerPixel' in exif:
                properties['SamplesPerPixel'] = exif['SamplesPerPixel']
            if 'XResolution' in exif:
                properties['XResolution'] = exif['XResolution']
            if 'YResolution' in exif:
                properties['YResolution'] = exif['YResolution']

            if 'ImageWidth' in exif:
                properties['dimensions'] = "%sx%s" % (properties['ImageWidth'], properties['ImageLength'])
            elif 'ExifImageWidth' in exif:
                properties['dimensions'] = "%sx%s" % (properties['ExifImageWidth'], properties['ExifImageHeight'])
        else:
            LOGGER.debug("EXIF data for %s not found." % dr_img['abspath'])

        # TODO: IPTC support
        # iptc_info = IPTCInfo(dr_img['abspath'])
        # if len(iptc_info.data) < 4:
        #     LOGGER.debug("IPTC dat for %s not found." % dr_img['abspath'])
        # else:
        #     print(iptc_info)

        return properties

    def _add_image_db(self, sdid, abspath, name, blob, mtime, int_check, serial):
        query = "INSERT INTO scan_img (sdid, abspath, name, thumb, mtime, integrity_check, serial) VALUES (?, ?, ?, ?, ?, ?, ?)"
        params = (sdid, abspath, name, blob.getvalue(), mtime, int_check, serial)
        si_id = self._db.run_insert_query(query, params, False)
        return si_id

    def _update_image_db(self, si_id, int_check):
        query = "UPDATE scan_img set integrity_check = ? WHERE id = ?"
        params = (int_check, si_id)
        self._db.run_query(query, params, False)

    def _update_image_thumb_db(self, si_id, blob, mtime, int_check):
        query = "UPDATE scan_img set thumb = ?, mtime = ?, integrity_check = ? WHERE id = ?"
        params = (blob.getvalue(), mtime, int_check, si_id)
        self._db.run_query(query, params, False)

    def get_image_id(self, abs_path):
        query = "SELECT id, mtime FROM scan_img WHERE abspath = ?"
        params = (abs_path,)
        res = self._db.run_select_query(query, params)
        if not res:
            return None
        return res[0]

    def get_image_from_id(self, si_id, sd_id):
        query = "SELECT * FROM scan_img WHERE id = ? AND sdid  = ?"
        params = (si_id, sd_id)
        res = self._db.run_select_query(query, params)
        if not res:
            return None
        return res[0]

    def get_scan_dir_image(self, sd_id, serial):
        query = "SELECT * FROM scan_img WHERE sdid = ? AND serial = ?"
        params = (sd_id, serial)
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

    def format_size(self, num, suffix='B'):
        for unit in ['', 'Ki', 'Mi']:
            if abs(num) < 1024.0:
                return "%3.1f %s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f %s%s" % (num, 'Gi', suffix)

