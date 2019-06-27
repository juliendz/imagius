#include "dir.h"
#include "dirstore.h"

DirManager::DirManager(QObject *parent) : QObject(parent) {
    store_ = new DirStore();
}

DirManager::~DirManager() {
    delete store_;
}

void DirManager::GetWatched(QList<WatchedDirMeta*>& watched){
    store_->GetWatched(watched);
}
