"""
Update Manager module
author: Julien Dcruz
"""
from PyQt5 import QtCore, QtNetwork
from imagius.types import SettingType
import settings
from .log import LOGGER
from packaging.version import Version


class UpdateManager(QtCore.QObject):

    _net_mgr = None

    def __init__(self):
        super(UpdateManager, self).__init__()
        self._net_mgr = QtNetwork.QNetworkAccessManager(self)
        self._net_mgr.finished.connect(self._request_finished)

    def get_updates(self):
        # url = settings.get(SettingType.CHECK_UPDATE_URL, 'https://api.github.com/repos/juliendz/imagius/releases')
        url = 'https://api.github.com/repos/reactiveui/ReactiveUI/releases/latest'
        qurl = QtCore.QUrl(url)
        LOGGER.info("Checking for updates....")
        self._net_mgr.get(QtNetwork.QNetworkRequest(qurl))

    @QtCore.pyqtSlot(QtNetwork.QNetworkReply)
    def _request_finished(self, reply):
        if reply.error() == QtNetwork.QNetworkReply.NoError:
            json_doc = QtCore.QJsonDocument.fromJson(reply.readAll())
            json_obj = json_doc.object()
            latest_release = Version(json_obj['tag_name'].toString())
            if latest_release > settings.app_version:
                LOGGER.info("Update found....")
            else:
                LOGGER.info("No updates found....")
        else:
            LOGGER.error("Error while making update check request!")
