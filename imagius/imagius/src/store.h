#ifndef STORE_H
#define STORE_H

#include "structs.h"

class IDirStore {

    public:
        virtual void Get(QString abs_path, DirMeta* out) = 0;
        virtual void GetWatched(QList<WatchedDirMeta*>& out) = 0;
        virtual void Add(const DirMeta* in) = 0;
        virtual void AddWatched(const WatchedDirMeta* in) = 0;
        virtual void DeleteWatched(long watched_dir_id) = 0;
        virtual void Update(const DirMeta* in) = 0;
        virtual void UpdateLastCheck(QString dir_id, long last_check_ts) = 0;
        virtual void Prune(long last_check_ts) = 0;

        IDirStore();
        virtual ~IDirStore() = 0;
};

#endif // STORE_H
