#ifndef DIR_H
#define DIR_H

#include <QObject>
#include "store.h"

class DirManager : public QObject {
    Q_OBJECT

    private:
        IDirStore* store_;

    public:
        explicit DirManager(QObject *parent = nullptr);
        ~DirManager();

        void GetWatched(QList<WatchedDirMeta*>& watched);

    signals:

    public slots:
};

#endif // DIR_H
