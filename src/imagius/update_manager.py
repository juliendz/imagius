"""
Update Manager module
author: Julien Dcruz
"""
from PyQt5 import QtCore, QtNetwork, QtGui, QtWidgets
from packaging.version import Version

from imagius_types import SettingType
import settings
from log import LOGGER


class UpdateManager(QtCore.QObject):

    _net_mgr = None

    def __init__(self):
        super(UpdateManager, self).__init__()
        self._net_mgr = QtNetwork.QNetworkAccessManager(self)
        self._net_mgr.finished.connect(self._request_finished)

    def get_updates(self):
        # url = settings.get(SettingType.CHECK_UPDATE_URL, 'https://api.github.com/repos/juliendz/imagius/releases')
        # url = 'https://api.github.com/repos/reactiveui/ReactiveUI/releases/latest'
        url = 'https://api.github.com/repos/reactiveui/ReactiveiUI/releases/latest'
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
                LOGGER.info("Update found. New version(%s) is available" % latest_release)
            else:
                LOGGER.info("No updates found! Already on latest release.")
        else: 
            LOGGER.error("Update Manager: Unable to retrieve updates from release api (Error: %s)" % reply.error())
            msgbox = QtWidgets.QMessageBox()
            msgbox.setText('Unable to load the release api. Redirecting to website downloads page.')
            msgbox.setDetailedText('Network Request Error Code: %s' % reply.error())
            msgbox.exec()
            QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://juliendz.github.io/imagius/#download"))
