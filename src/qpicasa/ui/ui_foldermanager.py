# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/foldermanager.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FolderManagerWindow(object):
    def setupUi(self, FolderManagerWindow):
        FolderManagerWindow.setObjectName("FolderManagerWindow")
        FolderManagerWindow.resize(570, 527)
        self.verticalLayout = QtWidgets.QVBoxLayout(FolderManagerWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(FolderManagerWindow)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.frame)
        self.groupBox.setMaximumSize(QtCore.QSize(300, 16777215))
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.frame_3 = QtWidgets.QFrame(self.groupBox)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_3)
        self.gridLayout.setObjectName("gridLayout")
        self.btn_AddFolder = QtWidgets.QPushButton(self.frame_3)
        self.btn_AddFolder.setObjectName("btn_AddFolder")
        self.gridLayout.addWidget(self.btn_AddFolder, 0, 0, 1, 1)
        self.btn_EditFolder = QtWidgets.QPushButton(self.frame_3)
        self.btn_EditFolder.setObjectName("btn_EditFolder")
        self.gridLayout.addWidget(self.btn_EditFolder, 0, 1, 1, 1)
        self.btn_DeleteFolder = QtWidgets.QPushButton(self.frame_3)
        self.btn_DeleteFolder.setObjectName("btn_DeleteFolder")
        self.gridLayout.addWidget(self.btn_DeleteFolder, 0, 2, 1, 1)
        self.verticalLayout_4.addWidget(self.frame_3)
        self.listView_FolderList = QtWidgets.QListView(self.groupBox)
        self.listView_FolderList.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.listView_FolderList.setObjectName("listView_FolderList")
        self.verticalLayout_4.addWidget(self.listView_FolderList)
        self.horizontalLayout.addWidget(self.groupBox)
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setMaximumSize(QtCore.QSize(250, 16777215))
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_3.setContentsMargins(9, -1, -1, -1)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(self.frame_4)
        self.label.setMaximumSize(QtCore.QSize(16777215, 50))
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.groupBox_2 = QtWidgets.QGroupBox(self.frame_4)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3.addWidget(self.groupBox_2)
        self.horizontalLayout.addWidget(self.frame_4)
        self.verticalLayout.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(FolderManagerWindow)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.btn_Close = QtWidgets.QPushButton(self.frame_2)
        self.btn_Close.setObjectName("btn_Close")
        self.verticalLayout_2.addWidget(self.btn_Close)
        self.verticalLayout.addWidget(self.frame_2)

        self.retranslateUi(FolderManagerWindow)
        QtCore.QMetaObject.connectSlotsByName(FolderManagerWindow)

    def retranslateUi(self, FolderManagerWindow):
        _translate = QtCore.QCoreApplication.translate
        FolderManagerWindow.setWindowTitle(_translate("FolderManagerWindow", "Dialog"))
        self.groupBox.setTitle(_translate("FolderManagerWindow", "Folder List"))
        self.btn_AddFolder.setText(_translate("FolderManagerWindow", "Add"))
        self.btn_EditFolder.setText(_translate("FolderManagerWindow", "Edit"))
        self.btn_DeleteFolder.setText(_translate("FolderManagerWindow", "Delete"))
        self.label.setText(_translate("FolderManagerWindow", "Choose the folders which contain pictures that you want to import. They will be also watched for new pictures."))
        self.groupBox_2.setTitle(_translate("FolderManagerWindow", "For the current folder"))
        self.btn_Close.setText(_translate("FolderManagerWindow", "Close"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FolderManagerWindow = QtWidgets.QDialog()
    ui = Ui_FolderManagerWindow()
    ui.setupUi(FolderManagerWindow)
    FolderManagerWindow.show()
    sys.exit(app.exec_())

