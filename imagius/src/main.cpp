#include "mainwindow.h"
#include "image.h"
#include <QApplication>
#include <QDebug>
#include <QDir>
#include <vips/vips.h>

int main(int argc, char *argv[])
{

    qDebug() << "Starting up";

    if(VIPS_INIT("imagius")){
        vips_error_exit("unable to start VIPS");
    }
    qDebug() << vips_version(0);

    ImageManager imgr;
    QString a = "C:/Users/Julien/Downloads/test/b.png";
    QString b = QDir::cleanPath("C:/Users/Julien/Downloads/thumbs");
    if(!imgr.GenerateThumbnail(a, b)){
        qDebug() << "failed";
    }


    QApplication imagius_app(argc, argv);
    MainWindow w;
    w.showMaximized();



    return imagius_app.exec();
}
