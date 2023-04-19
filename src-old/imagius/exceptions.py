# -*- coding: utf-8 -*-
__license__ = 'GPL v3'
__copyright__ = '2019, Julien Dcruz juliendcruz@gmail.com'
__docformat__ = 'restructuredtext en'

"""
Application specific exceptions
"""


class OsNotDetectedError(Exception):
    pass


class AppDataDirReadWriteFailed(Exception):
    pass
