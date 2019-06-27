#include "imagius_utils.h"

Imagius_Utils::Imagius_Utils() {  }

const char* Imagius_Utils::ToCString(QString qstr) {
    return qstr.toStdString().c_str();
}

QString Imagius_Utils::FromCString(const char * cstr){
    return QString::fromUtf8(cstr);
}

QString Imagius_Utils::UserAppDataDir() {
    return "test";
}
