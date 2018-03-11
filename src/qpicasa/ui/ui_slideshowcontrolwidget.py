# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qpicasa/ui/slideshowcontrolwidget.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SlideshowControlWidget(object):
    def setupUi(self, SlideshowControlWidget):
        SlideshowControlWidget.setObjectName("SlideshowControlWidget")
        SlideshowControlWidget.resize(636, 94)
        self.horizontalLayout = QtWidgets.QHBoxLayout(SlideshowControlWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(SlideshowControlWidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btn_exit = QtWidgets.QPushButton(self.frame)
        self.btn_exit.setObjectName("btn_exit")
        self.horizontalLayout_3.addWidget(self.btn_exit)
        self.btn_prev_image = QtWidgets.QPushButton(self.frame)
        self.btn_prev_image.setObjectName("btn_prev_image")
        self.horizontalLayout_3.addWidget(self.btn_prev_image)
        self.btn_play = QtWidgets.QPushButton(self.frame)
        self.btn_play.setObjectName("btn_play")
        self.horizontalLayout_3.addWidget(self.btn_play)
        self.btn_next_image = QtWidgets.QPushButton(self.frame)
        self.btn_next_image.setObjectName("btn_next_image")
        self.horizontalLayout_3.addWidget(self.btn_next_image)
        self.groupBox = QtWidgets.QGroupBox(self.frame)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_decre_time = QtWidgets.QPushButton(self.groupBox)
        self.btn_decre_time.setObjectName("btn_decre_time")
        self.horizontalLayout_2.addWidget(self.btn_decre_time)
        self.lbl_display_time = QtWidgets.QLabel(self.groupBox)
        self.lbl_display_time.setObjectName("lbl_display_time")
        self.horizontalLayout_2.addWidget(self.lbl_display_time)
        self.btn_incre_time = QtWidgets.QPushButton(self.groupBox)
        self.btn_incre_time.setObjectName("btn_incre_time")
        self.horizontalLayout_2.addWidget(self.btn_incre_time)
        self.horizontalLayout_3.addWidget(self.groupBox)
        self.horizontalLayout.addWidget(self.frame)

        self.retranslateUi(SlideshowControlWidget)
        QtCore.QMetaObject.connectSlotsByName(SlideshowControlWidget)

    def retranslateUi(self, SlideshowControlWidget):
        _translate = QtCore.QCoreApplication.translate
        SlideshowControlWidget.setWindowTitle(_translate("SlideshowControlWidget", "Form"))
        self.btn_exit.setText(_translate("SlideshowControlWidget", "Exit"))
        self.btn_prev_image.setText(_translate("SlideshowControlWidget", "Prev"))
        self.btn_play.setText(_translate("SlideshowControlWidget", "Play"))
        self.btn_next_image.setText(_translate("SlideshowControlWidget", "Next"))
        self.groupBox.setTitle(_translate("SlideshowControlWidget", "Display Time"))
        self.btn_decre_time.setText(_translate("SlideshowControlWidget", "-"))
        self.lbl_display_time.setText(_translate("SlideshowControlWidget", "0"))
        self.btn_incre_time.setText(_translate("SlideshowControlWidget", "+"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SlideshowControlWidget = QtWidgets.QWidget()
    ui = Ui_SlideshowControlWidget()
    ui.setupUi(SlideshowControlWidget)
    SlideshowControlWidget.show()
    sys.exit(app.exec_())

