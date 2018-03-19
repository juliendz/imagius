# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qpicasa/ui/propertieswidget.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PropertiesWidget(object):
    def setupUi(self, PropertiesWidget):
        PropertiesWidget.setObjectName("PropertiesWidget")
        PropertiesWidget.resize(270, 465)
        self.verticalLayout = QtWidgets.QVBoxLayout(PropertiesWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gbox_properties = QtWidgets.QGroupBox(PropertiesWidget)
        font = QtGui.QFont()
        font.setFamily("Noto Sans")
        font.setPointSize(10)
        self.gbox_properties.setFont(font)
        self.gbox_properties.setObjectName("gbox_properties")
        self.verticalLayout.addWidget(self.gbox_properties)

        self.retranslateUi(PropertiesWidget)
        QtCore.QMetaObject.connectSlotsByName(PropertiesWidget)

    def retranslateUi(self, PropertiesWidget):
        _translate = QtCore.QCoreApplication.translate
        PropertiesWidget.setWindowTitle(_translate("PropertiesWidget", "Form"))
        self.gbox_properties.setTitle(_translate("PropertiesWidget", "Select and item to show the properties"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PropertiesWidget = QtWidgets.QWidget()
    ui = Ui_PropertiesWidget()
    ui.setupUi(PropertiesWidget)
    PropertiesWidget.show()
    sys.exit(app.exec_())

