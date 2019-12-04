#!/usr/bin/bash

pyside2-uic -x qpicasa/ui/mainwindow.ui -o qpicasa/ui/ui_mainwindow.py
pyside2-uic -x qpicasa/ui/foldermanager.ui -o qpicasa/ui/ui_foldermanager.py
pyside2-uic -x qpicasa/ui/slideshowwindow.ui -o qpicasa/ui/ui_slideshowwindow.py
pyside2-uic -x qpicasa/ui/slideshowcontrolwidget.ui -o qpicasa/ui/ui_slideshowcontrolwidget.py