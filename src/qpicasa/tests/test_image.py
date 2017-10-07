
"""
#Description: Test module for image
#Author(s): Julien Dcruz
"""

import os
import pytest
from qpicasa import db
from qpicasa import image


def test__generate_thumb():
    abspath = './image.jpg'
    obj = image.ImageManager('../app.db')
    ret = obj._generate_thumb(abspath, (128, 128))
    assert ret.getbuffer().nbytes > 0

def test__add_image_db():
    abspath = './image.jpg'
    obj = image.ImageManager('../app.db')
    thumb = obj._generate_thumb(abspath, (128, 128))
    si_id = obj._add_image_db(-1, abspath, 'image.jpg', thumb)
    print(si_id)
    assert si_id > 0