#include "mainwindow.h"
#include <QApplication>
#include <QDebug>
#include <vips/vips8>

using namespace vips;

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;
    w.showMaximized();

    qDebug() << "Starting up";
    if(vips_init("imagius")){
        vips_error_exit("unable to start VIPS");
    }

    qDebug() << vips_version(0);

    return a.exec();
}
