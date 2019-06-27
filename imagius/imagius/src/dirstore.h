#ifndef DIRSTORE_H
#define DIRSTORE_H

#include "store.h"
#include "structs.h"
#include <QSqlDatabase>

class DirStore: public IDirStore {
    public:
        DirStore();
        void CheckOpen();

        void Get(QString abs_path, DirMeta* out);
        void GetWatched(QList<WatchedDirMeta*>& out);
        void Add(const DirMeta*);
        void AddWatched(const WatchedDirMeta*);
        void DeleteWatched(long watched_dir_id);
        void Update(const DirMeta*);
        void UpdateLastCheck(QString dir_id, long last_check_ts);
        void Prune(long last_check_ts);


     private:
        QSqlDatabase db_;
};

#endif // DIRSTORE_H
