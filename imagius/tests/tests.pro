QT += testlib
QT -= gui

CONFIG += qt console warn_on depend_includepath testcase
CONFIG -= app_bundle

TEMPLATE = app

SOURCES +=  tst_test_imagius_utils.cpp \
    ../imagius/src/imagius_utils.cpp

HEADERS += \
    ../imagius/src/imagius_utils.h
