# -*- coding: utf-8 -*-

"""
Application Version Upgrade module
author: Julien Dcruz
"""
from packaging.version import Version
from log import LOGGER


def upgrade_from_previous_versions(cur_version):
    # Upgrade code to Version(0.8.1)
    if cur_version < Version('0.8.1'):
        LOGGER.info('Upgrading from Version:%s to Version:%s' % (cur_version, '0.8.1'))
        # No db changes in this version
        cur_version = Version('0.8.1')
    return
