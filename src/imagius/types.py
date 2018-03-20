"""
Types module
author: Julien Dcruz
"""
from enum import Enum


class Thumb_Caption_Type(Enum):
    NoCaption = 0
    FileName = 1


class SettingType(Enum):

    CHECK_UPDATE_ON_STARTUP = 0

    FILETYPE_PNG = 100
    FILETYPE_BMP = 101

    LOOP_SLIDESHOW = 200


IMAGE_FILETYPES = {
    'jpg': ["*.jpg", "*.jpeg", "*.JPG"],
    'png': ["*.png", "*.PNG"],
    'bmp': ["*.bmp", "*.BMP"]
}
