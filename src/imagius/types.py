"""
Types module
author: Julien Dcruz
"""
from enum import Enum, auto


class Thumb_Caption_Type(Enum):
    NoCaption = 0
    FileName = 1


class SettingType(Enum):

    CHECK_UPDATE_ON_STARTUP = auto()
    FILETYPE_PNG = auto()
    FILETYPE_BMP = auto()

    UI_THUMBS_SIZE = auto()
    UI_METADATA_SHOW_PROPS = auto()
    UI_METADATA_SHOW_TAGS = auto()
    
    SLIDESHOW_LOOP = auto()
    SLIDESHOW_INTERVAL = auto()


IMAGE_FILETYPES = {
    'jpg': ["*.jpg", "*.jpeg", "*.JPG"],
    'png': ["*.png", "*.PNG"],
    'bmp': ["*.bmp", "*.BMP"]
}
