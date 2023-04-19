# -*- coding: utf-8 -*-
__license__ = 'GPL v3'
__copyright__ = '2019, Julien Dcruz juliendcruz@gmail.com'
__docformat__ = 'restructuredtext en'

"""
Test modules for constants
"""

import os
from imagius import constants


def test__get_appdata_dir():
    print(constants.get_appdata_dir())
