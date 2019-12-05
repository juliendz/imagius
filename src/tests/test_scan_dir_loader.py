
"""
#Description: Test module for meta_files
#Author(s): Julien Dcruz
"""
import os
from qpicasa import scan_dir_loader


def test_load_scan_dir_images():
    abspath = './image.jpg'
    obj = meta_files.MetaFilesManager("../meta-files.db")
    ret = obj._generate_thumb(abspath, (128, 128))
    assert ret.getbuffer().nbytes > 0