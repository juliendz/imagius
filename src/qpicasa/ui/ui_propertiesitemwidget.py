# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qpicasa/ui/propertiesitemwidget.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PropertiesItemWidget(object):
    def setupUi(self, PropertiesItemWidget):
        PropertiesItemWidget.setObjectName("PropertiesItemWidget")
        PropertiesItemWidget.resize(400, 38)
        self.horizontalLayout = QtWidgets.QHBoxLayout(PropertiesItemWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(PropertiesItemWidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setContentsMargins(5, 0, 0, 5)
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setVerticalSpacing(5)
        self.gridLayout.setObjectName("gridLayout")
        self.lbl_title = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setBold(True)
        font.setWeight(75)
        self.lbl_title.setFont(font)
        self.lbl_title.setObjectName("lbl_title")
        self.gridLayout.addWidget(self.lbl_title, 0, 0, 1, 1)
        self.lbl_value = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setFamily("Noto Sans")
        font.setPointSize(9)
        self.lbl_value.setFont(font)
        self.lbl_value.setObjectName("lbl_value")
        self.gridLayout.addWidget(self.lbl_value, 1, 0, 1, 1)
        self.horizontalLayout.addWidget(self.frame)

        self.retranslateUi(PropertiesItemWidget)
        QtCore.QMetaObject.connectSlotsByName(PropertiesItemWidget)

    def retranslateUi(self, PropertiesItemWidget):
        _translate = QtCore.QCoreApplication.translate
        PropertiesItemWidget.setWindowTitle(_translate("PropertiesItemWidget", "Form"))
        self.lbl_title.setText(_translate("PropertiesItemWidget", "TextLabel"))
        self.lbl_value.setText(_translate("PropertiesItemWidget", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PropertiesItemWidget = QtWidgets.QWidget()
    ui = Ui_PropertiesItemWidget()
    ui.setupUi(PropertiesItemWidget)
    PropertiesItemWidget.show()
    sys.exit(app.exec_())

