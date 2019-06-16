package pkg

import (
	"imagius/pkg/dir"
	"imagius/pkg/utils"
	"path/filepath"
	"time"

	"github.com/labstack/gommon/log"
)

func ScanDirs() error {

	//Get the list of all folders to scan
	FoldersToScan := []string{filepath.FromSlash("C:/Users/Julien/Downloads/test")}

	db, err := utils.OpenDB()
	if err != nil {
		panic(err)
	}

	dirMgr := dir.GetDirManager(db)

	lastCheckTs := time.Now().Unix()

	//Begin the scan
	for _, dir := range FoldersToScan {
		dirMgr.Scan(dir, lastCheckTs)
	}

	//Prune the img_dir table
	_, err = dirMgr.Store.Prune(lastCheckTs)
	if err != nil {
		log.Errorf("%v+", err)
		panic(err)
	}

	db.Close()

	return nil
}
