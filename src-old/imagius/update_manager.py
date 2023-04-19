"""
Update Manager module
author: Julien Dcruz
"""
from PySide2 import QtCore, QtNetwork, QtGui, QtWidgets
from PySide2.QtCore import Slot
from packaging.version import Version

from imagius.imagius_types import SettingType
from imagius import settings
from imagius.log import LOGGER


class UpdateManager(QtCore.QObject):

    _net_mgr = None

    def __init__(self):
        super(UpdateManager, self).__init__()
        self._net_mgr = QtNetwork.QNetworkAccessManager(self)
        self._net_mgr.finished.connect(self._request_finished)

    def get_updates(self):
        url = settings.get(SettingType.CHECK_UPDATE_URL,
                           'https://api.github.com/repos/juliendz/imagius/releases/latest')
        qurl = QtCore.QUrl(url)
        LOGGER.info("Checking for updates....")
        self._net_mgr.get(QtNetwork.QNetworkRequest(qurl))

    @Slot(QtNetwork.QNetworkReply)
    def _request_finished(self, reply):
        if reply.error() == QtNetwork.QNetworkReply.NoError:
            json_doc = QtCore.QJsonDocument.fromJson(reply.readAll())
            json_obj = json_doc.object()
            latest_release = Version(json_obj['tag_name'].toString())
            is_draft = json_obj['draft'].toBool()
            assets = json_obj['assets'].toArray()
            asset_url = ''
            if len(assets) > 0:
                asset = assets[0]
                asset_url = asset['browser_download_url']

            if asset_url == '':
                LOGGER.error("Update Manager: Assets object was null or empty")
                self._setup_msgbox("Error checking for Updates",
                                   'No downloads available for this release. Redirect to website downloads page ?',
                                   "Release API 'Assets' object was null or empty")
                self._msgbox.exec()
                if self._msgbox.clickedButton() == self._msgox_btn_ok:
                    QtGui.QDesktopServices.openUrl(QtCore.QUrl(
                        "https://juliendz.github.io/imagius/#download"))
                return

            if latest_release > Version(settings.app_version) and is_draft is False:
                LOGGER.info("Update found. New version(%s) is available" %
                            str(latest_release))
                self._setup_msgbox("Update info !",
                                   'Update found. Latest version is (%s)' % str(
                                       latest_release),
                                   None, "Download", "Later")
                self._msgbox.exec()
                if self._msgbox.clickedButton() == self._msgox_btn_ok:
                    QtGui.QDesktopServices.openUrl(
                        QtCore.QUrl(asset_url.toString()))
            else:
                LOGGER.info("No updates found! Already on latest release.")
                msgbox = QtWidgets.QMessageBox()
                msgbox.setIcon(QtWidgets.QMessageBox.Information)
                msgbox.setWindowTitle('Update Info')
                msgbox.setText("No updates found! Already on latest release.")
                msgbox.exec()
        else:
            LOGGER.error(
                "Update Manager: Unable to retrieve updates from release api (Error: %s)" % error_code)
            self._setup_msgbox("Error checking for Updates",
                               'Unable to load the release api. Redirect to website downloads page ?',
                               'Network Request Error Code: %s' % error_code)
            self._msgbox.exec()
            if self._msgbox.clickedButton() == self._msgox_btn_ok:
                QtGui.QDesktopServices.openUrl(QtCore.QUrl(
                    "https://juliendz.github.io/imagius/#download"))

    def _setup_msgbox(self, title, text, details=None, btn_accept_title="Ok", btn_reject_title="Cancel"):
        self._msgbox = QtWidgets.QMessageBox()
        self._msgbox.setIcon(QtWidgets.QMessageBox.Warning)
        self._msgox_btn_ok = self._msgbox.addButton(
            btn_accept_title, QtWidgets.QMessageBox.AcceptRole)
        self._msgbox_btn_cancel = self._msgbox.addButton(
            btn_reject_title, QtWidgets.QMessageBox.RejectRole)
        self._msgbox.setWindowTitle(title)
        self._msgbox.setText(text)
        if details:
            self._msgbox.setDetailedText(details)
