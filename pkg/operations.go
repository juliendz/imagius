package pkg

import (
	"imagius/pkg/dir"
	"imagius/pkg/utils"

	"github.com/pkg/errors"
)

type Operation struct {
	// ID      string      `json:"id"`
	Command string      `json:"cmd"`
	Payload interface{} `json:"payload"`
}

func GetWatchedDirs() (dirs []dir.WatchedDirMeta, err error) {

	db, err := utils.OpenDB()
	if err != nil {
		return dirs, errors.Wrap(err, "pkg.GetWatchedDirs")
	}
	//Note: If close() is called for some reason any subsequent queries always return null values
	//defer db.Close()

	dirMgr := dir.GetDirManager(db)
	dirs, err = dirMgr.Store.GetWatched()
	if err != nil {
		return dirs, errors.Wrap(err, "pkg.GetWatchedDirs")
	}

	return dirs, nil
}

func AddWatchedDir(abspath string) (err error) {

	db, err := utils.OpenDB()
	if err != nil {
		return errors.Wrap(err, "pkg.AddWatchedDir")
	}

	dirMgr := dir.GetDirManager(db)
	_, err = dirMgr.Store.AddWatched(abspath)
	if err != nil {
		return errors.Wrap(err, "pkg.GetWatchedDirs")
	}

	return nil
}

func DeleteWatchedDir(ID int64) (err error) {

	db, err := utils.OpenDB()
	if err != nil {
		return errors.Wrap(err, "pkg.DeleteWatchedDir")
	}

	dirMgr := dir.GetDirManager(db)
	_, err = dirMgr.Store.DeleteWatched(ID)
	if err != nil {
		return errors.Wrap(err, "pkg.DeleteWatchedDirs")
	}

	return nil
}
