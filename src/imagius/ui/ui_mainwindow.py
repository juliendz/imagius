# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'imagius/ui/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1002, 626)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
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
        self.verticalLayout_4.addWidget(self.frame_7)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.splitter_2 = QtWidgets.QSplitter(self.frame)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.frame_2 = QtWidgets.QFrame(self.splitter_2)
        self.frame_2.setMaximumSize(QtCore.QSize(250, 16777215))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.treeView_scandirs = QtWidgets.QTreeView(self.frame_2)
        self.treeView_scandirs.setIndentation(10)
        self.treeView_scandirs.setObjectName("treeView_scandirs")
        self.treeView_scandirs.header().setVisible(False)
        self.verticalLayout.addWidget(self.treeView_scandirs)
        self.frame_main_container = QtWidgets.QFrame(self.splitter_2)
        self.frame_main_container.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame_main_container.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_main_container.setObjectName("frame_main_container")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.frame_main_container)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.splitter = QtWidgets.QSplitter(self.frame_main_container)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.frame_thumbs = QtWidgets.QFrame(self.splitter)
        self.frame_thumbs.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_thumbs.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_thumbs.setObjectName("frame_thumbs")
        self.vlayout_frame_thumbs = QtWidgets.QVBoxLayout(self.frame_thumbs)
        self.vlayout_frame_thumbs.setObjectName("vlayout_frame_thumbs")
        self.frame_4 = QtWidgets.QFrame(self.frame_thumbs)
        self.frame_4.setMinimumSize(QtCore.QSize(0, 80))
        self.frame_4.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame_4.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_6 = QtWidgets.QFrame(self.frame_4)
        self.frame_6.setMaximumSize(QtCore.QSize(16777215, 56))
        self.frame_6.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_6)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setHorizontalSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame_5 = QtWidgets.QFrame(self.frame_6)
        self.frame_5.setMaximumSize(QtCore.QSize(51, 55))
        self.frame_5.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_5)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.frame_5)
        self.label.setMaximumSize(QtCore.QSize(45, 39))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/images/icon_folder"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.gridLayout_2.addWidget(self.frame_5, 0, 0, 2, 1)
        self.lbl_dir_name = QtWidgets.QLabel(self.frame_6)
        font = QtGui.QFont()
        font.setFamily("Trebuchet MS")
        font.setPointSize(16)
        self.lbl_dir_name.setFont(font)
        self.lbl_dir_name.setStyleSheet("color: rgb(170, 170, 127)")
        self.lbl_dir_name.setText("")
        self.lbl_dir_name.setObjectName("lbl_dir_name")
        self.gridLayout_2.addWidget(self.lbl_dir_name, 0, 1, 1, 1)
        self.lbl_cdate = QtWidgets.QLabel(self.frame_6)
        self.lbl_cdate.setText("")
        self.lbl_cdate.setObjectName("lbl_cdate")
        self.gridLayout_2.addWidget(self.lbl_cdate, 1, 1, 1, 1)
        self.verticalLayout_2.addWidget(self.frame_6)
        self.btn_slideshow = QtWidgets.QPushButton(self.frame_4)
        self.btn_slideshow.setMaximumSize(QtCore.QSize(32, 34))
        self.btn_slideshow.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/icon_slideshow"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_slideshow.setIcon(icon)
        self.btn_slideshow.setObjectName("btn_slideshow")
        self.verticalLayout_2.addWidget(self.btn_slideshow)
        self.vlayout_frame_thumbs.addWidget(self.frame_4)
        self.frame_metadata = QtWidgets.QFrame(self.splitter)
        self.frame_metadata.setMaximumSize(QtCore.QSize(300, 16777215))
        font = QtGui.QFont()
        font.setFamily("Noto Sans")
        font.setPointSize(12)
        self.frame_metadata.setFont(font)
        self.frame_metadata.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_metadata.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_metadata.setObjectName("frame_metadata")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_metadata)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.toolBox_metadata = QtWidgets.QToolBox(self.frame_metadata)
        self.toolBox_metadata.setObjectName("toolBox_metadata")
        self.toolbox_metadata_properties = QtWidgets.QWidget()
        self.toolbox_metadata_properties.setGeometry(QtCore.QRect(0, 0, 298, 308))
        self.toolbox_metadata_properties.setObjectName("toolbox_metadata_properties")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/images/icon_properties"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolBox_metadata.addItem(self.toolbox_metadata_properties, icon1, "")
        self.toolBox_metadata_tags = QtWidgets.QWidget()
        self.toolBox_metadata_tags.setGeometry(QtCore.QRect(0, 0, 298, 308))
        self.toolBox_metadata_tags.setObjectName("toolBox_metadata_tags")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/images/icon_folder"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolBox_metadata.addItem(self.toolBox_metadata_tags, icon2, "")
        self.gridLayout_3.addWidget(self.toolBox_metadata, 0, 0, 1, 1)
        self.horizontalLayout_7.addWidget(self.splitter)
        self.horizontalLayout_3.addWidget(self.splitter_2)
        self.verticalLayout_4.addWidget(self.frame)
        self.frame_8 = QtWidgets.QFrame(self.centralwidget)
        self.frame_8.setMaximumSize(QtCore.QSize(16777215, 100))
        self.frame_8.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setLineWidth(2)
        self.frame_8.setMidLineWidth(0)
        self.frame_8.setObjectName("frame_8")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_8)
        self.gridLayout.setObjectName("gridLayout")
        self.frame_9 = QtWidgets.QFrame(self.frame_8)
        self.frame_9.setAutoFillBackground(False)
        self.frame_9.setStyleSheet("color: white;\n"
"background-color: rgb(86, 144, 182);\n"
"font-weight: bold")
        self.frame_9.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_9.setObjectName("frame_9")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_9)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem1 = QtWidgets.QSpacerItem(201, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.lbl_selection_summary = QtWidgets.QLabel(self.frame_9)
        font = QtGui.QFont()
        font.setFamily("Noto Sans")
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_selection_summary.setFont(font)
        self.lbl_selection_summary.setText("")
        self.lbl_selection_summary.setObjectName("lbl_selection_summary")
        self.horizontalLayout_4.addWidget(self.lbl_selection_summary)
        spacerItem2 = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.gridLayout.addWidget(self.frame_9, 0, 0, 1, 1)
        self.frame_10 = QtWidgets.QFrame(self.frame_8)
        self.frame_10.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_10.setObjectName("frame_10")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame_10)
        self.horizontalLayout_6.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_6.setSpacing(1)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem3 = QtWidgets.QSpacerItem(518, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem3)
        self.hslider_thumb_size = QtWidgets.QSlider(self.frame_10)
        self.hslider_thumb_size.setMaximumSize(QtCore.QSize(140, 16777215))
        self.hslider_thumb_size.setMinimum(64)
        self.hslider_thumb_size.setMaximum(256)
        self.hslider_thumb_size.setSingleStep(20)
        self.hslider_thumb_size.setPageStep(64)
        self.hslider_thumb_size.setProperty("value", 128)
        self.hslider_thumb_size.setSliderPosition(128)
        self.hslider_thumb_size.setOrientation(QtCore.Qt.Horizontal)
        self.hslider_thumb_size.setInvertedAppearance(False)
        self.hslider_thumb_size.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.hslider_thumb_size.setTickInterval(0)
        self.hslider_thumb_size.setObjectName("hslider_thumb_size")
        self.horizontalLayout_6.addWidget(self.hslider_thumb_size)
        self.frame_metdata_toolbar = QtWidgets.QFrame(self.frame_10)
        self.frame_metdata_toolbar.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_metdata_toolbar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_metdata_toolbar.setObjectName("frame_metdata_toolbar")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_metdata_toolbar)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.toolbutton_tags = QtWidgets.QToolButton(self.frame_metdata_toolbar)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/images/icon_tags"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolbutton_tags.setIcon(icon3)
        self.toolbutton_tags.setIconSize(QtCore.QSize(32, 32))
        self.toolbutton_tags.setCheckable(True)
        self.toolbutton_tags.setObjectName("toolbutton_tags")
        self.buttonGroup_metadata = QtWidgets.QButtonGroup(MainWindow)
        self.buttonGroup_metadata.setObjectName("buttonGroup_metadata")
        self.buttonGroup_metadata.setExclusive(False)
        self.buttonGroup_metadata.addButton(self.toolbutton_tags)
        self.horizontalLayout_5.addWidget(self.toolbutton_tags)
        self.toolbutton_properties = QtWidgets.QToolButton(self.frame_metdata_toolbar)
        self.toolbutton_properties.setText("")
        self.toolbutton_properties.setIcon(icon1)
        self.toolbutton_properties.setIconSize(QtCore.QSize(32, 32))
        self.toolbutton_properties.setCheckable(True)
        self.toolbutton_properties.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.toolbutton_properties.setAutoRaise(False)
        self.toolbutton_properties.setObjectName("toolbutton_properties")
        self.buttonGroup_metadata.addButton(self.toolbutton_properties)
        self.horizontalLayout_5.addWidget(self.toolbutton_properties)
        self.horizontalLayout_6.addWidget(self.frame_metdata_toolbar)
        self.gridLayout.addWidget(self.frame_10, 1, 0, 1, 1)
        self.verticalLayout_4.addWidget(self.frame_8)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1002, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuThumbnail_Captions = QtWidgets.QMenu(self.menuView)
        self.menuThumbnail_Captions.setObjectName("menuThumbnail_Captions")
        self.menuFolder_View = QtWidgets.QMenu(self.menuView)
        self.menuFolder_View.setObjectName("menuFolder_View")
        self.menuFolder = QtWidgets.QMenu(self.menubar)
        self.menuFolder.setObjectName("menuFolder")
        self.menuPicture = QtWidgets.QMenu(self.menubar)
        self.menuPicture.setObjectName("menuPicture")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_folder_manager = QtWidgets.QAction(MainWindow)
        self.action_folder_manager.setObjectName("action_folder_manager")
        self.actionSmall_Thumbnails = QtWidgets.QAction(MainWindow)
        self.actionSmall_Thumbnails.setCheckable(True)
        self.actionSmall_Thumbnails.setObjectName("actionSmall_Thumbnails")
        self.actionNormal_Thumbnails = QtWidgets.QAction(MainWindow)
        self.actionNormal_Thumbnails.setCheckable(True)
        self.actionNormal_Thumbnails.setChecked(True)
        self.actionNormal_Thumbnails.setObjectName("actionNormal_Thumbnails")
        self.action_properties = QtWidgets.QAction(MainWindow)
        self.action_properties.setCheckable(True)
        self.action_properties.setObjectName("action_properties")
        self.action_tags = QtWidgets.QAction(MainWindow)
        self.action_tags.setCheckable(True)
        self.action_tags.setObjectName("action_tags")
        self.actionSlideshow = QtWidgets.QAction(MainWindow)
        self.actionSlideshow.setObjectName("actionSlideshow")
        self.actionFilename = QtWidgets.QAction(MainWindow)
        self.actionFilename.setCheckable(True)
        self.actionFilename.setObjectName("actionFilename")
        self.actionFilename_2 = QtWidgets.QAction(MainWindow)
        self.actionFilename_2.setObjectName("actionFilename_2")
        self.actionFlat_View = QtWidgets.QAction(MainWindow)
        self.actionFlat_View.setCheckable(True)
        self.actionFlat_View.setObjectName("actionFlat_View")
        self.actionOptions = QtWidgets.QAction(MainWindow)
        self.actionOptions.setObjectName("actionOptions")
        self.actionProperties = QtWidgets.QAction(MainWindow)
        self.actionProperties.setObjectName("actionProperties")
        self.actionView_Slideshow = QtWidgets.QAction(MainWindow)
        self.actionView_Slideshow.setObjectName("actionView_Slideshow")
        self.action_folder_locate = QtWidgets.QAction(MainWindow)
        self.action_folder_locate.setObjectName("action_folder_locate")
        self.action_add_folder = QtWidgets.QAction(MainWindow)
        self.action_add_folder.setObjectName("action_add_folder")
        self.action_file_locate = QtWidgets.QAction(MainWindow)
        self.action_file_locate.setObjectName("action_file_locate")
        self.action_exit = QtWidgets.QAction(MainWindow)
        self.action_exit.setObjectName("action_exit")
        self.actionDocumentation = QtWidgets.QAction(MainWindow)
        self.actionDocumentation.setObjectName("actionDocumentation")
        self.actionCheck_for_Updates = QtWidgets.QAction(MainWindow)
        self.actionCheck_for_Updates.setObjectName("actionCheck_for_Updates")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuFile.addAction(self.action_add_folder)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.action_file_locate)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.action_exit)
        self.menuTools.addAction(self.action_folder_manager)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.actionOptions)
        self.menuAbout.addAction(self.actionDocumentation)
        self.menuAbout.addAction(self.actionCheck_for_Updates)
        self.menuAbout.addSeparator()
        self.menuAbout.addAction(self.actionAbout)
        self.menuThumbnail_Captions.addAction(self.actionFilename)
        self.menuThumbnail_Captions.addAction(self.actionFilename_2)
        self.menuFolder_View.addAction(self.actionFlat_View)
        self.menuView.addAction(self.actionSmall_Thumbnails)
        self.menuView.addAction(self.actionNormal_Thumbnails)
        self.menuView.addSeparator()
        self.menuView.addAction(self.action_properties)
        self.menuView.addAction(self.action_tags)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionSlideshow)
        self.menuView.addSeparator()
        self.menuView.addAction(self.menuThumbnail_Captions.menuAction())
        self.menuView.addAction(self.menuFolder_View.menuAction())
        self.menuFolder.addAction(self.actionView_Slideshow)
        self.menuFolder.addSeparator()
        self.menuFolder.addAction(self.action_folder_locate)
        self.menuPicture.addAction(self.actionProperties)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuFolder.menuAction())
        self.menubar.addAction(self.menuPicture.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "Search"))
        self.toolBox_metadata.setItemText(self.toolBox_metadata.indexOf(self.toolbox_metadata_properties), _translate("MainWindow", "Properties"))
        self.toolBox_metadata.setItemText(self.toolBox_metadata.indexOf(self.toolBox_metadata_tags), _translate("MainWindow", "Tags"))
        self.toolbutton_tags.setText(_translate("MainWindow", "..."))
        self.toolbutton_properties.setToolTip(_translate("MainWindow", "<html><head/><body><p>Show/Hide Properties Window</p></body></html>"))
        self.toolbutton_properties.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.menuFile.setTitle(_translate("MainWindow", "Fi&le"))
        self.menuTools.setTitle(_translate("MainWindow", "&Tools"))
        self.menuAbout.setTitle(_translate("MainWindow", "Help"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.menuThumbnail_Captions.setTitle(_translate("MainWindow", "Thumbnail Captions"))
        self.menuFolder_View.setTitle(_translate("MainWindow", "Folder View"))
        self.menuFolder.setTitle(_translate("MainWindow", "Folder"))
        self.menuPicture.setTitle(_translate("MainWindow", "Picture"))
        self.action_folder_manager.setText(_translate("MainWindow", "&Folder Manager"))
        self.actionSmall_Thumbnails.setText(_translate("MainWindow", "Small Thumbnails"))
        self.actionNormal_Thumbnails.setText(_translate("MainWindow", "Normal Thumbnails"))
        self.action_properties.setText(_translate("MainWindow", "Properties"))
        self.action_tags.setText(_translate("MainWindow", "Tags"))
        self.actionSlideshow.setText(_translate("MainWindow", "Slideshow"))
        self.actionFilename.setText(_translate("MainWindow", "None"))
        self.actionFilename_2.setText(_translate("MainWindow", "Filename"))
        self.actionFlat_View.setText(_translate("MainWindow", "Flat Folder View"))
        self.actionOptions.setText(_translate("MainWindow", "Options"))
        self.actionProperties.setText(_translate("MainWindow", "Properties"))
        self.actionView_Slideshow.setText(_translate("MainWindow", "View Slideshow"))
        self.action_folder_locate.setText(_translate("MainWindow", "Locate on Disk"))
        self.action_add_folder.setText(_translate("MainWindow", "Add Folder to Imagius"))
        self.action_file_locate.setText(_translate("MainWindow", "Locate on Disk"))
        self.action_exit.setText(_translate("MainWindow", "Exit"))
        self.actionDocumentation.setText(_translate("MainWindow", "Documentation"))
        self.actionCheck_for_Updates.setText(_translate("MainWindow", "Check for Updates"))
        self.actionAbout.setText(_translate("MainWindow", "About"))

import qpicasa_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

