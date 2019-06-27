#ifndef STRUCTS_H
#define STRUCTS_H

#include <QString>

struct DirMeta{
        QString Id;
        QString Name;
        QString AbsPath;
        long long ModifiedTime;
        long long LastCheckTime;
        bool IsModified;
        int ImageCount;

};

struct WatchedDirMeta{
        QString Id;
        QString AbsPath;
};


#endif // STRUCTS_H
