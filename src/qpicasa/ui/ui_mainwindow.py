# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qpicasa/ui/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(764, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.frame_7 = QtWidgets.QFrame(self.centralwidget)
        self.frame_7.setMaximumSize(QtCore.QSize(16777215, 51))
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_7)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(338, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label_2 = QtWidgets.QLabel(self.frame_7)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.lineEdit = QtWidgets.QLineEdit(self.frame_7)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.gridLayout.addWidget(self.frame_7, 0, 0, 1, 2)
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setMaximumSize(QtCore.QSize(250, 16777215))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.listView_scandirs = QtWidgets.QListView(self.frame_2)
        self.listView_scandirs.setObjectName("listView_scandirs")
        self.verticalLayout.addWidget(self.listView_scandirs)
        self.gridLayout.addWidget(self.frame_2, 1, 0, 1, 1)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setMinimumSize(QtCore.QSize(0, 80))
        self.frame_4.setMaximumSize(QtCore.QSize(16777215, 71))
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.frame_5 = QtWidgets.QFrame(self.frame_4)
        self.frame_5.setMaximumSize(QtCore.QSize(51, 55))
        self.frame_5.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.frame_5)
        self.label.setMaximumSize(QtCore.QSize(45, 39))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/images/icon_folder"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.horizontalLayout_3.addWidget(self.frame_5)
        self.frame_6 = QtWidgets.QFrame(self.frame_4)
        self.frame_6.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lbl_dir_name = QtWidgets.QLabel(self.frame_6)
        font = QtGui.QFont()
        font.setFamily("Trebuchet MS")
        font.setPointSize(16)
        self.lbl_dir_name.setFont(font)
        self.lbl_dir_name.setStyleSheet("color: rgb(170, 170, 127)")
        self.lbl_dir_name.setObjectName("lbl_dir_name")
        self.verticalLayout_2.addWidget(self.lbl_dir_name)
        self.lbl_cdate = QtWidgets.QLabel(self.frame_6)
        self.lbl_cdate.setObjectName("lbl_cdate")
        self.verticalLayout_2.addWidget(self.lbl_cdate)
        self.horizontalLayout_3.addWidget(self.frame_6)
        self.verticalLayout_4.addWidget(self.frame_4)
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setMaximumSize(QtCore.QSize(16777215, 46))
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.btn_slidshow = QtWidgets.QPushButton(self.frame_3)
        self.btn_slidshow.setMaximumSize(QtCore.QSize(31, 34))
        self.btn_slidshow.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/icon_slideshow"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_slidshow.setIcon(icon)
        self.btn_slidshow.setObjectName("btn_slidshow")
        self.verticalLayout_3.addWidget(self.btn_slidshow)
        self.verticalLayout_4.addWidget(self.frame_3)
        self.frame_thumbs_container = QtWidgets.QFrame(self.frame)
        self.frame_thumbs_container.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_thumbs_container.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_thumbs_container.setObjectName("frame_thumbs_container")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_thumbs_container)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gfxview_thumbs = QtWidgets.QGraphicsView(self.frame_thumbs_container)
        self.gfxview_thumbs.setObjectName("gfxview_thumbs")
        self.gridLayout_2.addWidget(self.gfxview_thumbs, 0, 0, 1, 1)
        self.verticalLayout_4.addWidget(self.frame_thumbs_container)
        self.gridLayout.addWidget(self.frame, 1, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 764, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_FolderManager = QtWidgets.QAction(MainWindow)
        self.action_FolderManager.setObjectName("action_FolderManager")
        self.menuTools.addAction(self.action_FolderManager)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "Search"))
        self.lbl_dir_name.setText(_translate("MainWindow", "TextLabel"))
        self.lbl_cdate.setText(_translate("MainWindow", "TextLabel"))
        self.menuFile.setTitle(_translate("MainWindow", "Fi&le"))
        self.menuTools.setTitle(_translate("MainWindow", "&Tools"))
        self.menuAbout.setTitle(_translate("MainWindow", "Abo&ut"))
        self.action_FolderManager.setText(_translate("MainWindow", "&Folder Manager"))

import qpicasa_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

