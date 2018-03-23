#!/usr/bin/bash

pyuic5 -x qpicasa/ui/mainwindow.ui -o qpicasa/ui/ui_mainwindow.py
pyuic5 -x qpicasa/ui/foldermanager.ui -o qpicasa/ui/ui_foldermanager.py
pyuic5 -x qpicasa/ui/slideshowwindow.ui -o qpicasa/ui/ui_slideshowwindow.py
pyuic5 -x qpicasa/ui/slideshowcontrolwidget.ui -o qpicasa/ui/ui_slideshowcontrolwidget.py