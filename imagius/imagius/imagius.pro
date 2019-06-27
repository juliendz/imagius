#-------------------------------------------------
#
# Project created by QtCreator 2019-06-27T20:27:42
#
#-------------------------------------------------

QT       += core gui sql

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = imagius
TEMPLATE = app

# The following define makes your compiler emit warnings if you use
# any feature of Qt which has been marked as deprecated (the exact warnings
# depend on your compiler). Please consult the documentation of the
# deprecated API in order to know how to port your code away from it.
DEFINES += QT_DEPRECATED_WARNINGS

# You can also make your code fail to compile if you use deprecated APIs.
# In order to do so, uncomment the following line.
# You can also select to disable deprecated APIs only up to a certain version of Qt.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

CONFIG += c++11

SOURCES += \
        src/dir.cpp \
        src/dirstore.cpp \
        src/image.cpp \
        src/image_store.cpp \
        src/imagius_utils.cpp \
        src/main.cpp \
        src/mainwindow.cpp \
        src/store.cpp

HEADERS += \
        src/dir.h \
        src/dirstore.h \
        src/image.h \
        src/image_store.h \
        src/imagius_utils.h \
        src/mainwindow.h \
        src/store.h \
        src/structs.h

FORMS += \
        src/ui/mainwindow.ui

INCLUDEPATH += \
        C:\Users\Julien\Dev\libs\vips-dev-w64-web-8.8.0\vips-dev-8.8\include \
        C:\Users\Julien\Dev\libs\vips-dev-w64-web-8.8.0\vips-dev-8.8\include\glib-2.0


win32:LIBS += \
      -LC:/Users/Julien/Dev/libs/vips-dev-w64-web-8.8.0/vips-dev-8.8/lib -lvips -lgobject-2.0 -lintl -lglib-2.0

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target
