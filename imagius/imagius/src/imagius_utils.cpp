#include "imagius_utils.h"
#include <QtDebug>
#include <QStandardPaths>

Imagius_Utils::Imagius_Utils() {  }

const char* Imagius_Utils::ToCString(QString qstr) {
    return qstr.toStdString().c_str();
}

QString Imagius_Utils::FromCString(const char * cstr){
    return QString::fromUtf8(cstr);
}

QString Imagius_Utils::UserAppDataDir() {
    return QStandardPaths::standardLocations(QStandardPaths::AppDataLocation)[0];
}
