package image

import (
	"database/sql"
	"os"

	"github.com/jmoiron/sqlx"
	_ "github.com/mattn/go-sqlite3"
	"github.com/pkg/errors"
)

type ImgMeta struct {
	ID        int64   `db:"id"`
	Filename  string  `db:"filename"`
	AbsPath   string  `db:"abspath"`
	Thumbnail string  `db:"thumb"`
	Mtime     int64   `db:"mtime"`
	LastCheck int64   `db:"last_check"`
	Serial    float64 `db:"serial"`
}

type ImgStore struct {
	DB *sqlx.DB
}

func (store ImgStore) Get(absPath string) (ImgMeta, error) {
	img := ImgMeta{}

	sqlQuery := `
	SELECT id, filename, abspath, mtime, last_check
	FROM img_meta
	WHERE abspath = $1;`

	err := store.DB.Get(&img, sqlQuery, absPath)
	if err != nil {
		if err != sql.ErrNoRows {
			return img, errors.Wrap(err, "ImgStore.Get")
		}
	}

	return img, nil
}

func (store ImgStore) Add(file os.FileInfo, dirId string, abspath string, thumb string, last_check int64) (int64, error) {

	sqlQuery := `
	INSERT INTO img_meta 
	(dir_id, filename, abspath, thumb, mtime, last_check, serial) 
	VALUES (?, ?, ?, ?, ?, ?, (SELECT IFNULL(MAX(id), 0) + 1 FROM img_meta))` //Serial increments by 1 based on the max value of `id` column

	res, err := store.DB.Exec(sqlQuery, dirId, file.Name(), abspath, thumb, file.ModTime().Unix(), last_check)
	if err != nil {
		return 0, errors.Wrap(err, "ImgStore.Add")
	}
	lastInsertID, _ := res.LastInsertId()

	return lastInsertID, nil
}

func (store ImgStore) Update(imgMeta ImgMeta) error {

	sqlQuery := `
	UPDATE img_meta 
	SET thumb = ?, mtime = ?, last_check = ? 
	WHERE id = ?`

	_, err := store.DB.Exec(sqlQuery, imgMeta.Thumbnail, imgMeta.Mtime, imgMeta.LastCheck, imgMeta.ID)
	if err != nil {
		return errors.Wrap(err, "ImgStore.Update")
	}
	// ret, _ := res.RowsAffected()

	return nil
}

func (store ImgStore) UpdateLastCheck(imgMeta ImgMeta) error {

	sqlQuery := `
	UPDATE img_meta 
	SET last_check = ? 
	WHERE id = ?`

	_, err := store.DB.Exec(sqlQuery, imgMeta.LastCheck, imgMeta.ID)
	if err != nil {
		return errors.Wrap(err, "ImgStore.UpdateLastCheck")
	}
	// ret, _ := res.RowsAffected()

	return nil
}

func (store ImgStore) Prune(dirId string, last_check int64) (int64, error) {

	sqlQuery := `
	DELETE FROM img_meta WHERE dir_id = ? AND last_check < ?`

	res, err := store.DB.Exec(sqlQuery, dirId, last_check)
	if err != nil {
		return 0, errors.Wrap(err, "ImgStore.Prune")
	}
	ret, _ := res.RowsAffected()

	return ret, nil
}

func (store ImgStore) GetCountForDir(dirId string) (int64, error) {

	sqlQuery := `
	SELECT COUNT(id) FROM img_meta WHERE dir_id = ?;`

	var img_count int64
	err := store.DB.Get(&img_count, sqlQuery, dirId)
	if err != nil {
		if err != sql.ErrNoRows {
			return 0, errors.Wrap(err, "ImgStore.GetCountForDir")
		}
	}
	// fmt.Fprintln(os.Stdout, err)

	return img_count, nil
}
