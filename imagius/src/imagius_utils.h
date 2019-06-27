#ifndef IMAGIUS_UTILS_H
#define IMAGIUS_UTILS_H

#include <QString>

class Imagius_Utils {
    public:
        Imagius_Utils();
        static const char* ToCString(QString);
        static QString FromCString(const char*);
};

#endif // IMAGIUS_UTILS_H
