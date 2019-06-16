package dir

import (
	"imagius/pkg/image"
	"imagius/pkg/utils"
	"io/ioutil"
	"os"
	"path/filepath"

	"github.com/jmoiron/sqlx"
	log "github.com/sirupsen/logrus"
)

type DirManager struct {
	Store DirStore
}

var DirMgr *DirManager

//Not thread safe
func GetDirManager(db *sqlx.DB) *DirManager {

	if DirMgr == nil {
		DirMgr = &DirManager{DirStore{db}}
	}
	return DirMgr
}

func (dirMgr DirManager) Scan(path string, lastCheckTs int64) {

	// log.Info("[INFO]: Current dir: %v+", path)

	var isNewOrModified bool
	imgMgr := image.GetImgManager(dirMgr.Store.DB)

	//See if this dir has been previously saved to db
	dirMeta, err := dirMgr.Store.Get(path)
	if err != nil {
		log.Errorf("%v+", err)
		panic(err)
	}

	var currDirId string
	mtime := utils.GetModifiedTime(path)

	if dirMeta.ID == "" {
		currDirId = utils.GenerateGUID()

		isNewOrModified = true

	} else {
		currDirId = dirMeta.ID
		//Check if the dir has been modified
		if mtime.Unix() > dirMeta.Mtime {
			isNewOrModified = true
		}
	}

	//Starting walking the current dir
	children, err := ioutil.ReadDir(path)
	if err != nil {
		log.Errorf("%v+", err)
		panic(err)
	}
	for _, child := range children {

		if child.IsDir() {

			childAbsPath := filepath.Join(path, child.Name())
			dirMgr.Scan(childAbsPath, lastCheckTs)

		} else {
			if isNewOrModified {

				if utils.IsSupportedImageFormat(child) {
					imgMgr.ProcessImage(child, path, currDirId, lastCheckTs)
				}
			} else {
				continue
			}
		}
	} // End of directory walk

	//Final phase of current dir
	if isNewOrModified {

		imgMgr.Store.Prune(currDirId, lastCheckTs)

		imgCount, err := imgMgr.Store.GetCountForDir(currDirId)
		if err != nil {
			log.Errorf("%v+", err)
			panic(err)
		}

		if imgCount > 0 {

			if dirMeta.ID == "" {

				dirInfo, err := os.Stat(path)
				if err != nil {
					panic(err)
				}
				newDirMeta := DirMeta{
					ID:         currDirId,
					Name:       dirInfo.Name(),
					AbsPath:    path,
					Mtime:      dirInfo.ModTime().Unix(),
					LastCheck:  lastCheckTs,
					IsModified: true,
					ImageCount: imgCount,
				}
				_, err = dirMgr.Store.Add(newDirMeta)
				if err != nil {
					log.Errorf("%v+", err)
					panic(err)
				}
			} else {

				_, err := dirMgr.Store.Update(currDirId, mtime.Unix(), lastCheckTs, true, imgCount)
				if err != nil {
					log.Errorf("%v+", err)
					panic(err)
				}

			}
		}

	} else {

		_, err := dirMgr.Store.UpdateLastCheck(currDirId, lastCheckTs)
		if err != nil {
			log.Errorf("%v+", err)
			panic(err)
		}

	}

	return

}
