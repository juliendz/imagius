
"""
#Description: Test module for image
#Author(s): Julien Dcruz
"""

import os
import pytest


@pytest.fixture
def db_mgr():
    return db.dbmgr('./src/app.db')


def test_get_status(db_mgr):
    db_mgr.connect()
    obj = apache.get_instance(db_mgr)
    status = obj.get_status()
    assert status['status'] == 1
    db_mgr.disconnect()