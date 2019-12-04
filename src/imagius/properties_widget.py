"""
Description: Image Properties widget module
author: Julien Dcruz
"""

from PySide2 import QtCore, QtGui, QtWidgets
from ui.ui_propertieswidget import Ui_PropertiesWidget
from propertiesitem_widget import PropertiesItemWidget


class PropertiesWidget(QtWidgets.QWidget, Ui_PropertiesWidget):

    def __init__(self, parent=None):
        super(PropertiesWidget, self).__init__(parent)
        self.setupUi(self)

        self.vlayout = QtWidgets.QFormLayout(self.gbox_properties)

    def setup_properties(self, props):
        for i in reversed(range(self.vlayout.count())):
            self.vlayout.itemAt(i).widget().setParent(None)

        title = "Properties of %s" % props['filename']
        self.gbox_properties.setTitle(title)
        self.gbox_properties.setToolTip(title)

        for key, value in props.items():
            title = self.get_title(key)
            self.vlayout.addWidget(PropertiesItemWidget(key, value))

    def get_title(self, tag):
        if tag == 'abspath':
            return 'Location'
        elif tag == 'filesize':
            return 'File Size'
        elif tag == 'dimensions':
            return 'Dimensions'
        elif tag == 'DateTimeDigitized':
            return 'Digitized Date'
        elif tag == 'DateTime':
            return 'Modified Date'
        elif tag == 'ColorSpace':
            return 'Color Space'
        elif tag == 'ImageUniqueID':
            return 'Unique ID'
        elif tag == 'BitsPerSample':
            return 'Bits Per Sample'
        elif tag == 'XResolution':
            return 'X Resolution'
        elif tag == 'YResolution':
            return 'Y Resolution'
        elif tag == 'ResolutionUnit':
            return 'Resolution Unit'
        return tag
