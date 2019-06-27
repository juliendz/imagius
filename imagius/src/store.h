#ifndef STORE_H
#define STORE_H

#include "structs.h"

class IDirStore {

    public:
        virtual void Get(QString abs_path, DirMeta* out);
        virtual void GetWatched(QList<WatchedDirMeta*>& out);
        virtual void Add(const DirMeta* in);
        virtual void AddWatched(const WatchedDirMeta* in);
        virtual void Update(const DirMeta* in);
        virtual void UpdateLastCheck(QString dir_id, long last_check_ts);
        virtual void Prune(long last_check_ts);
        virtual void DeleteWatched(long watched_dir_id);

        virtual ~IDirStore() = 0;
};

#endif // STORE_H
