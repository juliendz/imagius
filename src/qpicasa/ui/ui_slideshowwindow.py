# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qpicasa/ui/slideshowwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SlideshowWindow(object):
    def setupUi(self, SlideshowWindow):
        SlideshowWindow.setObjectName("SlideshowWindow")
        SlideshowWindow.resize(594, 510)
        self.horizontalLayout = QtWidgets.QHBoxLayout(SlideshowWindow)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gfx_slide = QtWidgets.QGraphicsView(SlideshowWindow)
        self.gfx_slide.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.gfx_slide.setLineWidth(0)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.gfx_slide.setBackgroundBrush(brush)
        self.gfx_slide.setInteractive(False)
        self.gfx_slide.setObjectName("gfx_slide")
        self.horizontalLayout.addWidget(self.gfx_slide)

        self.retranslateUi(SlideshowWindow)
        QtCore.QMetaObject.connectSlotsByName(SlideshowWindow)

    def retranslateUi(self, SlideshowWindow):
        _translate = QtCore.QCoreApplication.translate
        SlideshowWindow.setWindowTitle(_translate("SlideshowWindow", "Form"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SlideshowWindow = QtWidgets.QWidget()
    ui = Ui_SlideshowWindow()
    ui.setupUi(SlideshowWindow)
    SlideshowWindow.show()
    sys.exit(app.exec_())

