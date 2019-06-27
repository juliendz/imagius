 #include "dirstore.h"
#include "imagius_utils.h"
#include <QtDebug>
#include <QSqlQuery>
#include <QSqlDatabase>
#include <QSqlError>
#include <QThread>
#include <QString>

DirStore::DirStore() {

    auto conn_name = "db_conn_" + QString::number((quint64)QThread::currentThread(), 16);
    qDebug() << conn_name;

    if(QSqlDatabase::contains(conn_name)){

        qDebug() << QString("Connection(%1) already exists. Reusing..").arg(conn_name);
        db_ = QSqlDatabase::database(conn_name);

    }else{

        qDebug() << QString("Creating a new connection(%1)").arg(conn_name);
        db_ = QSqlDatabase::addDatabase("QSQLITE", conn_name);
        db_.setDatabaseName()
    }
}

void DirStore::CheckOpen(){
    if(db_.isOpen()){
        qDebug() << QString("Connection(%1) seems to be closed. Connecting again").arg(db_.connectionName());
        db_.open();
    }
}

void DirStore::Get(QString abs_path, DirMeta* out){
    this->CheckOpen();

    QString queryStr =
            "SELECT id, name, abspath, mtime "
            "FROM dir_meta "
            "WHERE abspath = ?";

    QSqlQuery query(db_);
    query.prepare(queryStr);
    query.bindValue(0, abs_path);
    if(!query.exec()){
        throw std::runtime_error(Imagius_Utils::ToCString(query.lastError().text()));
    }

    while(query.next()){
        out->Id = query.value(0).toString();
        out->Name = query.value(1).toString();
        out->AbsPath = query.value(2).toString();
        out->ModifiedTime = query.value(3).toLongLong();
        break;
    }
}


void DirStore::GetWatched(QList<WatchedDirMeta*>& out){
    this->CheckOpen();

    QString queryStr =
            "SELECT id, abspath "
            "FROM watched_meta";

    QSqlQuery query(db_);
    query.prepare(queryStr);
    if(!query.exec()){
        throw std::runtime_error(Imagius_Utils::ToCString(query.lastError().text()));
    }

    WatchedDirMeta* meta = new WatchedDirMeta();
    while(query.next()){
        meta->Id = query.value(0).toString();
        meta->AbsPath = query.value(1).toString();

        out.append(meta);
    }
}


void DirStore::Add(const DirMeta* in) {
    this->CheckOpen();

    QString queryStr =
            "INSERT INTO dir_meta "
            "(id, name, abspath, mtime, last_check, is_modified, img_count) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)";

    QSqlQuery query(db_);
    query.prepare(queryStr);
    query.bindValue(0, in->Id);
    query.bindValue(1, in->Name);
    query.bindValue(2, in->AbsPath);
    query.bindValue(3, in->ModifiedTime);
    query.bindValue(4, in->LastCheckTime);
    query.bindValue(5, in->IsModified);
    query.bindValue(6, in->ImageCount);

    if(!query.exec()){
        throw std::runtime_error(Imagius_Utils::ToCString(query.lastError().text()));
    }
}

void DirStore::AddWatched(const WatchedDirMeta* in){
    this->CheckOpen();

    QString queryStr =
            "INSERT INTO watched_meta "
            "(abspath) "
            "VALUES (?)";


    QSqlQuery query(db_);
    query.prepare(queryStr);
    query.bindValue(0, in->AbsPath);

    if(!query.exec()){
        throw std::runtime_error(Imagius_Utils::ToCString(query.lastError().text()));
    }
}

void DirStore::DeleteWatched(long watched_dir_id) {
    this->CheckOpen();

    QString queryStr =  "DELETE FROM watched_meta WHERE ID = ?";

    QSqlQuery query(db_);
    query.prepare(queryStr);
    query.bindValue(0, QVariant::fromValue(watched_dir_id));

    if(!query.exec()){
        throw std::runtime_error(Imagius_Utils::ToCString(query.lastError().text()));
    }
}

void DirStore::Update(const DirMeta* in) {
    this->CheckOpen();

    QString queryStr =
            "UPDATE dir_meta "
            "SET mtime= ?, "
                "last_check = ?, "
                "is_modified = ?, "
                "img_count = ? "
            "WHERE id = ?`";


    QSqlQuery query(db_);
    query.prepare(queryStr);
    query.bindValue(0, in->ModifiedTime);
    query.bindValue(1, in->IsModified);
    query.bindValue(2, in->ImageCount);
    query.bindValue(4, in->Id);

    if(!query.exec()){
        throw std::runtime_error(Imagius_Utils::ToCString(query.lastError().text()));
    }
}

void DirStore::UpdateLastCheck(QString dir_id, long last_check_ts) {
    this->CheckOpen();

    QString queryStr =
            "UPDATE dir_meta "
            "SET last_check = ? "
            "WHERE id = ?";

    QSqlQuery query(db_);
    query.prepare(queryStr);
    query.bindValue(0, QVariant::fromValue(last_check_ts));
    query.bindValue(1, dir_id);

    if(!query.exec()){
        throw std::runtime_error(Imagius_Utils::ToCString(query.lastError().text()));
    }
}

void DirStore::Prune(long last_check_ts){
    this->CheckOpen();

    QString queryStr = "DELETE FROM dir_meta WHERE last_check < ?";

    QSqlQuery query(db_);
    query.prepare(queryStr);
    query.bindValue(0, QVariant::fromValue(last_check_ts));

    if(!query.exec()){
        throw std::runtime_error(Imagius_Utils::ToCString(query.lastError().text()));
    }
}

