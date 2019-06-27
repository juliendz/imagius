#ifndef IMAGE_H
#define IMAGE_H

#include <QObject>

class ImageManager : public QObject {
        Q_OBJECT

    private:

    public:
        explicit ImageManager(QObject *parent = nullptr);
        bool GenerateThumbnail(QString abspath, QString thumb_folder_path);

    signals:

    public slots:
};

#endif // IMAGE_H
