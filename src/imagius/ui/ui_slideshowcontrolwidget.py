# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'imagius/ui/slideshowcontrolwidget.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SlideshowControlWidget(object):
    def setupUi(self, SlideshowControlWidget):
        SlideshowControlWidget.setObjectName("SlideshowControlWidget")
        SlideshowControlWidget.resize(592, 72)
        self.horizontalLayout = QtWidgets.QHBoxLayout(SlideshowControlWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(SlideshowControlWidget)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_3.setSpacing(5)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btn_exit = QtWidgets.QPushButton(self.frame)
        self.btn_exit.setObjectName("btn_exit")
        self.horizontalLayout_3.addWidget(self.btn_exit)
        self.btn_prev_slide = QtWidgets.QPushButton(self.frame)
        self.btn_prev_slide.setObjectName("btn_prev_slide")
        self.horizontalLayout_3.addWidget(self.btn_prev_slide)
        self.btn_start_slideshow = QtWidgets.QPushButton(self.frame)
        self.btn_start_slideshow.setObjectName("btn_start_slideshow")
        self.horizontalLayout_3.addWidget(self.btn_start_slideshow)
        self.btn_next_slide = QtWidgets.QPushButton(self.frame)
        self.btn_next_slide.setObjectName("btn_next_slide")
        self.horizontalLayout_3.addWidget(self.btn_next_slide)
        self.groupBox = QtWidgets.QGroupBox(self.frame)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_decre_interval = QtWidgets.QPushButton(self.groupBox)
        self.btn_decre_interval.setObjectName("btn_decre_interval")
        self.horizontalLayout_2.addWidget(self.btn_decre_interval)
        self.lbl_display_time = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("Noto Sans")
        font.setPointSize(12)
        self.lbl_display_time.setFont(font)
        self.lbl_display_time.setObjectName("lbl_display_time")
        self.horizontalLayout_2.addWidget(self.lbl_display_time)
        self.btn_incre_interval = QtWidgets.QPushButton(self.groupBox)
        self.btn_incre_interval.setObjectName("btn_incre_interval")
        self.horizontalLayout_2.addWidget(self.btn_incre_interval)
        self.horizontalLayout_3.addWidget(self.groupBox)
        self.horizontalLayout.addWidget(self.frame)

        self.retranslateUi(SlideshowControlWidget)
        QtCore.QMetaObject.connectSlotsByName(SlideshowControlWidget)

    def retranslateUi(self, SlideshowControlWidget):
        _translate = QtCore.QCoreApplication.translate
        SlideshowControlWidget.setWindowTitle(_translate("SlideshowControlWidget", "Form"))
        self.btn_exit.setText(_translate("SlideshowControlWidget", "Exit"))
        self.btn_prev_slide.setText(_translate("SlideshowControlWidget", "Prev"))
        self.btn_start_slideshow.setText(_translate("SlideshowControlWidget", "Start"))
        self.btn_next_slide.setText(_translate("SlideshowControlWidget", "Next"))
        self.groupBox.setTitle(_translate("SlideshowControlWidget", "Display Time (seconds)"))
        self.btn_decre_interval.setText(_translate("SlideshowControlWidget", "-"))
        self.lbl_display_time.setText(_translate("SlideshowControlWidget", "0"))
        self.btn_incre_interval.setText(_translate("SlideshowControlWidget", "+"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SlideshowControlWidget = QtWidgets.QWidget()
    ui = Ui_SlideshowControlWidget()
    ui.setupUi(SlideshowControlWidget)
    SlideshowControlWidget.show()
    sys.exit(app.exec_())

