
"""
#Description: Test module for meta_files
"""
import os
from imagius.meta_files import MetaFilesManager


def test__get_scan_dirs():
    mgr = MetaFilesManager()
    assert len(mgr.get_scan_dirs()) > 0


def test__generate_thumb():
    abspath = './image.jpg'
    obj = meta_files.MetaFilesManager("../meta-files.db")
    ret = obj._generate_thumb(abspath, (128, 128))
    assert ret.getbuffer().nbytes > 0


def test__add_image_db():
    abspath = './image.jpg'
    obj = meta_files.MetaFilesManager("../meta-files.db")
    obj.connect()
    thumb = obj._generate_thumb(abspath, (128, 128))
    si_id = obj._add_image_db(-1, abspath, 'image.jpg',
                              thumb, os.path.getmtime(abspath))
    obj.disconnect()
    print(si_id)
    assert si_id > 0
