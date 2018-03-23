"""
Types module
author: Julien Dcruz
"""
from enum import Enum, auto


class Thumb_Caption_Type(Enum):
    NoCaption = auto()
    FileName = auto()


class SettingType(Enum):

    CHECK_UPDATE_ON_STARTUP = auto()
    CHECK_UPDATE_URL = auto()

    FILETYPE_PNG = auto()
    FILETYPE_BMP = auto()

    UI_THUMBS_SIZE = auto()
    UI_THUMBS_CAPTION_DISPLAY_MODE = auto()
    UI_METADATA_SHOW_PROPS = auto()
    UI_METADATA_SHOW_TAGS = auto()
    
    SLIDESHOW_LOOP = auto()
    SLIDESHOW_INTERVAL = auto()


IMAGE_FILETYPES = {
    'jpg': ["*.jpg", "*.jpeg", "*.JPG"],
    'png': ["*.png", "*.PNG"],
    'bmp': ["*.bmp", "*.BMP"]
}
