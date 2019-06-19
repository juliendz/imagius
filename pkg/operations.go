package pkg

import (
	"imagius/pkg/dir"
	"imagius/pkg/utils"

	"github.com/pkg/errors"
)

func GetWatchedDirs() (dirs []dir.WatchedDirMeta, err error) {

	db, err := utils.OpenDB()
	if err != nil {
		panic(err)
	}
	defer db.Close()

	dirMgr := dir.GetDirManager(db)
	dirs, err = dirMgr.Store.GetWatched()
	if err != nil {
		return dirs, errors.Wrap(err, "pkg.GetWatchedDirs")
	}

	return dirs, nil
}
