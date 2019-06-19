package dir

import (
	"database/sql"

	"github.com/jmoiron/sqlx"
	_ "github.com/mattn/go-sqlite3"
	"github.com/pkg/errors"
)

type DirMeta struct {
	ID         string `db:"id"`
	Name       string `db:"name"`
	AbsPath    string `db:"abspath"`
	Mtime      int64  `db:"mtime"`
	LastCheck  int64  `db:"last_check"`
	IsModified bool   `db:"is_modified"`
	ImageCount int64  `db:"img_count"`
}

type WatchedDirMeta struct {
	ID      string `db:"id"`
	Name    string `db:"name"`
	AbsPath string `db:"abspath"`
}

type DirStore struct {
	DB *sqlx.DB
}

func (store DirStore) Get(absPath string) (DirMeta, error) {
	dir := DirMeta{}

	sqlQuery := `
	SELECT id, name, abspath, mtime
	FROM dir_meta
	WHERE abspath = $1;`

	err := store.DB.Get(&dir, sqlQuery, absPath)
	if err != nil {
		if err != sql.ErrNoRows {
			return dir, errors.Wrap(err, "DirStore.Get")
		}
	}

	return dir, nil
}

func (store DirStore) GetWatched() (dirs []WatchedDirMeta, err error) {

	sqlQuery := `
	SELECT id, name, abspath
	FROM watched_meta`

	err = store.DB.Select(&dirs, sqlQuery)
	if err != nil {
		if err != sql.ErrNoRows {
			return dirs, errors.Wrap(err, "DirStore.GetWatched")
		}
	}

	return dirs, nil
}

func (store DirStore) Add(dirMeta DirMeta) (int64, error) {

	sqlQuery := `
	INSERT INTO dir_meta
	(id, name, abspath, mtime, last_check, is_modified, img_count)
	VALUES (?, ?, ?, ?, ?, ?, ?)`

	res, err := store.DB.Exec(sqlQuery,
		dirMeta.ID,
		dirMeta.Name,
		dirMeta.AbsPath,
		dirMeta.Mtime,
		dirMeta.LastCheck,
		dirMeta.IsModified,
		dirMeta.ImageCount)
	if err != nil {
		return 0, errors.Wrap(err, "DirStore.Add")
	}
	lastInsertID, _ := res.LastInsertId()

	return lastInsertID, nil
}

func (store DirStore) AddWatched(watchedDirMeta WatchedDirMeta) (int64, error) {

	sqlQuery := `
	INSERT INTO watched_meta
	(id, name, abspath)
	VALUES (?, ?)`

	res, err := store.DB.Exec(sqlQuery,
		watchedDirMeta.ID,
		watchedDirMeta.Name,
		watchedDirMeta.AbsPath)
	if err != nil {
		return 0, errors.Wrap(err, "DirStore.Add")
	}
	lastInsertID, _ := res.LastInsertId()

	return lastInsertID, nil
}

func (store DirStore) Update(dirId string, mtime int64, lastCheck int64, isModified bool, imgCount int64) (int64, error) {

	sqlQuery := `
	UPDATE dir_meta
	SET mtime= ?, 
		last_check = ?, 
		is_modified = ?, 
		img_count = ?
	WHERE id = ?`

	res, err := store.DB.Exec(sqlQuery,
		mtime,
		lastCheck,
		isModified,
		imgCount,
		dirId)
	if err != nil {
		return 0, errors.Wrap(err, "DirStore.Update")
	}
	ret, err := res.RowsAffected()

	return ret, err
}

func (store DirStore) UpdateLastCheck(dirId string, lastCheck int64) (int64, error) {

	sqlQuery := `
	UPDATE dir_meta
	SET last_check = ?
	WHERE id = ?`

	res, err := store.DB.Exec(sqlQuery,
		lastCheck,
		dirId)
	if err != nil {
		return 0, errors.Wrap(err, "DirStore.UpdateLastCheck")
	}
	ret, err := res.RowsAffected()

	return ret, err
}

func (store DirStore) Prune(lastCheck int64) (int64, error) {

	sqlQuery := `
	DELETE FROM dir_meta WHERE last_check < ?`

	res, err := store.DB.Exec(sqlQuery, lastCheck)
	if err != nil {
		return 0, errors.Wrap(err, "DirStore.Prune")
	}
	ret, _ := res.RowsAffected()

	return ret, nil
}
