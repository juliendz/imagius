#ifndef DIR_H
#define DIR_H

#include <QObject>

class DirManager : public QObject {
    Q_OBJECT

    public:
        explicit DirManager(QObject *parent = nullptr);

    signals:

    public slots:
};

#endif // DIR_H
