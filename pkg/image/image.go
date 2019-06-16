package image

import (
	"bytes"
	"encoding/gob"
	"imagius/pkg/utils"
	"os"
	"path/filepath"

	"github.com/disintegration/imaging"
	"github.com/jmoiron/sqlx"
	log "github.com/sirupsen/logrus"
)

type ImgManager struct {
	Store ImgStore
}

var ImgMgr *ImgManager

//Not thread safe
func GetImgManager(db *sqlx.DB) *ImgManager {

	if ImgMgr == nil {
		ImgMgr = &ImgManager{ImgStore{db}}
	}
	return ImgMgr
}

func (mgr ImgManager) ProcessImage(file os.FileInfo, parentPath string, dirId string, last_check_ts int64) error {

	abspath := filepath.Join(parentPath, file.Name())

	imgMeta, err := mgr.Store.Get(abspath)
	if err != nil {
		log.Errorf("%v+", err)
		return err
	}

	if imgMeta.ID == 0 {

		log.Info("Generating thumbnail")
		thumb, err := mgr.GenerateThumb(abspath)
		if err != nil {
			log.Errorf("%s", err)
			return err
		}

		_, err = mgr.Store.Add(file, dirId, abspath, thumb, last_check_ts)
		if err != nil {
			log.Errorf("%v ", err)
			return err
		}

	} else {

		mtime := utils.GetModifiedTime(abspath)
		imgMeta.LastCheck = last_check_ts

		if mtime.Unix() > imgMeta.Mtime {

			//Renegrate the thumb and update it
			thumb, err := mgr.GenerateThumb(abspath)
			if err != nil {
				return err
			}
			imgMeta.Thumbnail = thumb
			imgMeta.Mtime = mtime.Unix()

			err = mgr.Store.Update(imgMeta)
			if err != nil {
				log.Errorf("%v ", err)
				return err
			}

		} else {

			err = mgr.Store.UpdateLastCheck(imgMeta)
			if err != nil {
				log.Errorf("%v ", err)
				return err
			}
		}

	}

	return nil
}

func (mgr ImgManager) GenerateThumb(abspath string) ([]byte, error) {
	img, err := imaging.Open(abspath)
	if err != nil {
		return nil, err
	}

	thumb := imaging.Thumbnail(img, 256, 256, imaging.NearestNeighbor)

	var buffer bytes.Buffer
	enc := gob.NewEncoder(&buffer)

	err = enc.Encode(thumb)
	if err != nil {
		return nil, err
	}

	return buffer.Bytes(), nil
}
