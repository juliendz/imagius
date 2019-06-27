#include "image.h"
#include "imagius_utils.h"
#include <QDir>
#include <QFileInfo>
#include <QDebug>
#include <vips/vips.h>


ImageManager::ImageManager(QObject *parent) : QObject(parent) {

}

bool ImageManager::GenerateThumbnail(QString abspath, QString thumb_folder_path) {
    QFileInfo  imgInfo(abspath);


    qDebug() << Imagius_Utils::FromCString(vips_foreign_find_load(Imagius_Utils::ToCString(abspath)));

    VipsImage* img;
    if( !(img =vips_image_new_from_file(Imagius_Utils::ToCString(abspath), NULL))){
        return false;
    }

    VipsImage* thumb;
    if(vips_thumbnail_image(img, &thumb, 256, NULL) == -1){
        return false;
    };

    const char* thumb_save_path = Imagius_Utils::ToCString(thumb_folder_path + "/" + imgInfo.fileName());
    qDebug() << thumb_save_path;
    if(vips_image_write_to_file(thumb, thumb_save_path, NULL) == -1){
        return false;
    }

    return true;
}
